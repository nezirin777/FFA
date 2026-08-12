#------------------------------------------------------#
#  FFA改 Vips Ver 3.00
#  作成者: ねじりん
#------------------------------------------------------#
#------------------------------------------------------#
#　本スクリプトの著作権は下記の4人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE 改i v2.1
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE v0.21
#　programed by CUMRO
#　http://cgi.members.interq.or.jp/sun/cumro/mm/
#　cumro@sun.interq.or.jp
#------------------------------------------------------#
#  FF ADVENTURE(改) v1.021
#  remodeling by GUN
#  http://www2.to/meeting/
#  gun24@j-club.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#
"""
FFA Python/CGI - 戦闘シミュレーターモジュール (battle_logic.py)
"""

import sys

# エントリポイントで標準入出力を UTF-8 に構成 (ガイドライン3.2に準拠)
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8')
# if hasattr(sys.stdin, 'reconfigure'):
#     sys.stdin.reconfigure(encoding='utf-8')
import os
import random
import time
import json
import html
import copy
try:
    from . import common, skills
except ImportError:
    import common, skills
try:
    import config
except ImportError:
    from .. import config

# O(1)メンバーシップテストのための定数定義 (ガイドライン2.4に準拠し、線形探索を回避して高速化)
_SPECIAL_MODES: frozenset[str] = frozenset({"isekiai", "genei"})
_ACCESSORY_BONUS_STATS = common.STAT_KEYS

def _with_accessory_bonus(chara, accessory):
    """旧版 acs_add 相当。戦闘用コピーにだけ通常ステータスボーナスを加算する。"""
    effective = copy.deepcopy(chara)
    bonus = (accessory or {}).get("bonus", {})
    for key in _ACCESSORY_BONUS_STATS:
        effective[key] = int(effective.get(key, 0)) + int(bonus.get(key, 0))
    return effective

class BattleState:
    """
    戦闘中のすべての一時状態（バフ、デバフ、ダメージ、ログ）を管理するクラス。
    """
    def __init__(self, mode, chara, item, enemy_data, is_player_enemy=False):
        self.mode = mode  # "monster", "genei", "isekiai", "boss", "battle"
        self.chara = chara
        self.item = item
        
        self.is_player_enemy = is_player_enemy
        
        # 対戦相手がプレイヤーの場合
        if is_player_enemy:
            self.winner = enemy_data
            self.winner_item = enemy_data.get("equipped_item") # プレイヤーの装備
            self.mname = enemy_data["name"]
            self.mhp = enemy_data["hp"]
            self.mhp_flg = enemy_data["max_hp"]
            self.mgold = 0
            self.mex = 0
            self.mdmg = 0
            self.mkahi = 0
            self.monstac = "0"
            self.mons_ritu = 0
        # 対戦相手がモンスターの場合
        else:
            self.winner = {"id": "sys", "name": "モンスター"}
            self.mname = enemy_data["name"]
            self.mex = enemy_data["ex"]
            self.mrand = enemy_data["rand"]
            self.msp = enemy_data["sp"]
            self.mdmg = enemy_data["dmg"]
            self.mkahi = enemy_data["kahi"]
            self.monstac = enemy_data["stac"]
            self.mons_ritu = enemy_data["ritu"]
            self.mgold = enemy_data["gold"]
            
            # モンスターのHP決定
            self.mhp = random.randrange(max(1, self.mrand)) + self.msp
            self.mhp_flg = self.mhp
            
        # プレイヤー状態
        self.khp = chara["hp"]

        # 戦闘中の金銭変動。旧版の盗み技は戦闘後の報酬を増減させる。
        self.player_gold = max(0, int(chara.get("gold", 0)))
        self.gold_base = max(0, int(self.mgold))
        self.gold_reward_bonus = 0
        self.gold_reward_penalty = 0
        
        # ターンごとの計算用
        self.dmg1 = 0 # プレイヤーから敵へのダメージ
        self.dmg2 = 0 # 敵からプレイヤーへのダメージ
        self.dmgme1 = 0 # プレイヤー自傷ダメージ
        self.com1 = "" # プレイヤーの行動ログ
        self.com2 = "" # 敵の行動ログ
        self.clit1 = ""
        self.clit2 = ""
        self.sake1 = 0
        self.sake2 = 0
        self.waza_ritu = 0
        self.wwaza_ritu = 0  # 対人戦の相手(王者)側の必殺率(setupで算出)
        self.wd_dmg = 0      # 特殊技の追加ダメージ枠(既定0)
        self.kaihuku1 = ""
        self.kaihuku2 = ""
        self.huin = 0
        
        # バフ・制限数など
        self.syukuhuku = 0
        self.ora = 0
        self.a_22lmt = 0
        self.a_23lmt = 0
        self.wa_22lmt = 0
        self.hpplus1 = 0
        self.hpplus2 = 0
        self.charadown = {}
        
        # ターンカウンタ
        self.i = 1
        self.j = 0
        self.turn = config.Config['max_turns']
        
        # 回避率などの事前計算用補正
        self.a_hitup = 0
        self.a_kaihiup = 0
        self.a_wazaup = 0

    def available_gold(self):
        return self.player_gold

    def penalize_reward(self, amount):
        amount = max(0, int(amount))
        self.gold_reward_penalty += amount
        return amount

def get_job_dmg(job, chara, weapon_dmg):
    """
    職業に応じたプレイヤーの基礎ダメージを算出します (battle.pl の syokuzero〜syokuthirty に相当)
    """
    def r(attr):
        val = chara.get(attr, 1)
        return random.randrange(max(1, int(val)))

    # 7=str, 8=int, 9=mnd, 10=vit, 11=dex, 12=agi, 13=cha
    if job == 0: return r("str") + weapon_dmg
    elif job == 1: return r("int") + weapon_dmg
    elif job == 2: return r("mnd") + weapon_dmg
    # 旧版 syokuthree は chara[11]（器用さ）を参照する。
    elif job == 3: return r("dex") + weapon_dmg
    elif job == 4: return r("int") + weapon_dmg
    elif job == 5: return r("int") + weapon_dmg
    elif job == 6: return r("mnd") + r("cha") + weapon_dmg
    elif job == 7: return r("int") + r("cha") + weapon_dmg
    elif job == 8: return r("str") + r("vit") + weapon_dmg
    elif job == 9: return r("int") + r("mnd") + weapon_dmg
    elif job == 10: return r("str") + r("mnd") + weapon_dmg
    elif job == 11: return r("str") + r("int") + weapon_dmg
    elif job == 12: return r("str") + r("vit") + weapon_dmg
    elif job == 13: return r("str") + r("dex") + weapon_dmg
    elif job == 14: return r("str") + r("int") + weapon_dmg
    elif job == 15: return r("str") + r("int") + weapon_dmg
    elif job == 16: return r("str") + r("dex") + weapon_dmg
    elif job == 17: return r("int") + r("mnd") + r("cha") + weapon_dmg
    # 旧版の syokueighteen〜syokuthirty を、能力値の意味を保ったまま移植する。
    # 旧版の [7..13] は str,int,信仰心,vit,器用さ,速さ,魅力、[20] はカルマ。
    def all_stats():
        return (
            r("str") + r("int") + r("mnd") + r("vit") +
            r("dex") + r("agi") + r("cha") + int(chara.get("karma", 0))
        )

    if job in (18, 19, 20, 21, 28, 29, 30):
        return all_stats() + weapon_dmg
    elif job in (22, 26, 27):
        return all_stats() * 2 + weapon_dmg
    elif job == 23:
        return r("str") + weapon_dmg
    elif job == 24:
        return (r("vit") + r("dex") + r("agi") + r("cha") + int(chara.get("karma", 0))) * 2 + weapon_dmg
    elif job == 25:
        return (
            r("str") + r("int") + r("mnd") + r("vit") +
            r("dex") * 5 + r("agi") + r("cha") + int(chara.get("karma", 0))
        ) * 2 + weapon_dmg
    else:
        return all_stats() + weapon_dmg

class BattleSimulator:
    """
    戦闘実行シミュレーター。
    """
    def __init__(self, mode, chara, item, enemy_data, is_player_enemy=False):
        # 現行キー形式のデータをコピーして戦闘用の補正を適用する。
        effective_item = copy.deepcopy(item)
        effective_chara = copy.deepcopy(chara)
        effective_chara = _with_accessory_bonus(effective_chara, effective_item.get("accessory", {}))
        effective_enemy = copy.deepcopy(enemy_data)
        if is_player_enemy:
            enemy_accessory = effective_enemy.get("equipped_item", {}).get("accessory", {})
            effective_enemy = _with_accessory_bonus(effective_enemy, enemy_accessory)
        self.state = BattleState(mode, effective_chara, effective_item, effective_enemy, is_player_enemy)
        self.battle_logs = []
        
    def simulate(self):
        s = self.state
        
        # アクセサリーによる特殊補正 (旧版 acs: hitup, kaihiup, wazaup)
        s.a_hitup = int(s.item["accessory"].get("hit_rate", 0))
        s.a_kaihiup = int(s.item["accessory"].get("evasion_rate", 0))
        s.a_wazaup = int(s.item["accessory"].get("special_rate", 0))
        
        win = 2 # デフォルト引き分け
        
        for turn_idx in range(1, s.turn + 1):
            s.i = turn_idx
            
            # === 1. ターン初期化 (shokika) ===
            # プレイヤーダメージ
            s.dmg1 = get_job_dmg(s.chara["job"], s.chara, s.item["weapon"]["dmg"])
            # 敵ダメージ
            if s.is_player_enemy:
                # 対人戦の場合、相手の職業ダメージを計算
                s.dmg2 = get_job_dmg(s.winner["job"], s.winner, s.winner_item["weapon"]["dmg"])
                s.com2 = f"{s.mname}の攻撃！"
            else:
                s.dmg2 = s.mdmg + random.randrange(max(1, s.mrand))
                # 旧版 genei は各ターン開始時に、防具の防御力を敵攻撃へ加算していた。
                if s.mode == "genei":
                    s.dmg2 += s.item["armor"]["def"]
                s.com2 = f"{s.mname}の攻撃！"
                
            s.clit1 = ""
            s.clit2 = ""
            s.sake1 = 0
            s.sake2 = 0
            s.com1 = f"{s.chara['name']}は {s.item['weapon']['name']} で攻撃！"
            s.kaihuku1 = ""
            s.kaihuku2 = ""
            s.dmgme1 = 0
            s.hpplus1 = 0
            s.hpplus2 = 0
            s.huin = 0
            
            # === 2. プレイヤー必殺技発動判定 (tyosenwaza / hissatu) ===
            s.waza_ritu = int(s.chara["karma"] / 15) + 10 + s.chara["job_level"]
            if s.waza_ritu > 75: s.waza_ritu = 75
            s.waza_ritu += s.a_wazaup
            if s.waza_ritu > 95: s.waza_ritu = 95

            # 対人戦の相手(王者)側の必殺率。プレイヤー側と同じ式で算出する。
            # モンスター戦では winner に karma/job_level が無いため 0 起点となり、実際には mons_ritu が使われる。
            s.wwaza_ritu = int(s.winner.get("karma", 0) / 15) + 10 + s.winner.get("job_level", 0)
            if s.wwaza_ritu > 75: s.wwaza_ritu = 75
            if s.is_player_enemy:
                # 旧版 winwaza の winner[36]（アクセサリー必殺率補正）。
                s.wwaza_ritu += int(s.winner_item["accessory"].get("special_rate", 0))
            if s.wwaza_ritu > 95: s.wwaza_ritu = 95
            # 特殊技の追加ダメージ枠(旧版で未実装だった変数)。既定 0。
            s.wd_dmg = 0
            
            # モードに応じた技確率減衰 (O(1) frozenset ルックアップで判定)
            if s.mode in _SPECIAL_MODES:
                s.waza_ritu = int(s.waza_ritu / 3)
            elif s.mode == "boss":
                s.waza_ritu = int(s.waza_ritu / 2)
                
            # ピンチの時のリミットブレイク (HP10%未満)
            if int(s.chara["max_hp"] / 10) > s.khp and random.randrange(4) > 1:
                s.waza_ritu += 999
                s.com1 += "<br><font class=\"red\" size=4><b>LIMIT BREAK!!</b></font>"
                
            # ジョブ必殺技の動的実行 (tech_X.hissatu)
            skills.run_skill("tech", s.chara["job"], "hissatu", s)
            
            # === 3. 敵スキル発動判定 ===
            if s.is_player_enemy:
                # 旧版 wbattle.pl の winwaza 相当。王者側にもHPピンチ時の
                # リミットブレイク判定がある。
                if int(s.winner["max_hp"] / 10) > s.mhp and random.randrange(4) > 1:
                    s.wwaza_ritu += 999
                    s.com2 += "<br><font class=\"red\" size=4><b>LIMIT BREAK!!</b></font>"
                # 敵プレイヤーの必殺技
                skills.run_skill("wtech", s.winner["job"], "hissatu", s)
            else:
                # 敵モンスターのスキル (mons_X.mons_waza)
                skills.run_skill("mons", s.monstac, "mons_waza", s)
                
            # === 4. 職業の後発効果とアクセサリー効果 (acs_waza / wacs_waza) ===
            # 旧版では必殺技(hissatu)とは別に、通常攻撃後の atowaza と
            # アクセサリー固有効果の acskouka をこの順で実行していた。
            skills.run_skill("tech", s.chara["job"], "atowaza", s)
            skills.run_skill("acstech", s.item["accessory"]["effect_id"], "acskouka", s)
            if s.is_player_enemy:
                skills.run_skill("wtech", s.winner["job"], "watowaza", s)
                skills.run_skill("wacstech", s.winner_item["accessory"]["effect_id"], "wacskouka", s)
            else:
                skills.run_skill("mons", s.monstac, "mons_atowaza", s)

            # 旧版 wbattle.pl battle_clt の初手逆転必殺判定。
            if s.is_player_enemy and s.i == 1:
                level_sa = int(config.Config.get("level_sa", 15))
                gyakuten = int(config.Config.get("gyakuten", 100))
                player_weapon_dmg = s.item["weapon"]["dmg"]
                winner_weapon_dmg = s.winner_item["weapon"]["dmg"]
                if (
                    int(s.winner.get("level", 0)) - int(s.chara.get("level", 0)) >= level_sa
                    or player_weapon_dmg < winner_weapon_dmg
                ):
                    s.dmg1 = s.dmg1 * gyakuten
                    s.sake2 -= 999999
                    s.winner_item["weapon"]["dmg"] = 0
                    s.com1 += "<font color=\"blue\" size=5>逆転必殺技発動！！</font><br>"
                if (
                    int(s.chara.get("level", 0)) - int(s.winner.get("level", 0)) >= level_sa
                    or s.winner_item["weapon"]["dmg"] < s.item["armor"]["def"]
                ):
                    s.dmg2 = s.dmg2 * 100
                    s.sake1 -= 999999
                    s.com2 += "<font color=\"red\" size=5>逆転必殺技発動！！</font><br>"
                
            # === 5. クリティカル判定 (mons_clt / clt) ===
            kclt_ritu = 100 - int(s.khp / s.chara["max_hp"] * 100) if s.chara["max_hp"] > 0 else 0
            if kclt_ritu > random.randrange(100):
                s.com1 += f"<br><span class=\"red u-text-medium\"><b>クリティカルヒット！！</b>「{html.escape(str(s.chara.get('comment', '')))}」</span>"
                if s.is_player_enemy:
                    # 旧版 wbattle.pl: 挑戦者の攻撃は2倍し、王者の武器攻撃力を加算。
                    s.dmg1 = s.dmg1 * 2 + s.winner_item["weapon"]["dmg"]
                else:
                    s.dmg1 = s.dmg1 * 3
                
            if s.is_player_enemy:
                mclt_ritu = 100 - int(s.mhp / s.winner["max_hp"] * 100) if s.winner["max_hp"] > 0 else 0
                if mclt_ritu > random.randrange(100):
                    s.com2 += f"<br><span class=\"red u-text-medium\"><b>クリティカルヒット！！</b>「{html.escape(str(s.winner.get('comment', '')))}」</span>"
                    # 旧版 wbattle.pl: 王者の攻撃は2倍し、挑戦者の防具防御力を加算。
                    s.dmg2 = s.dmg2 * 2 + s.item["armor"]["def"]
            else:
                mclt_ritu = 100 - int(s.mhp / s.mhp_flg * 100) if s.mhp_flg > 0 else 0
                if mclt_ritu > random.randrange(200):
                    s.com2 += f"<br><span class=\"red\"><b>クリティカルヒット！！</b></span>"
                    s.dmg2 = s.dmg2 + s.item["armor"]["def"] # 防御無視相当の加算
                    
            # === 6. 防御力による減算・回避判定 ===
            ci_plus = s.item["weapon"]["effect"] + s.item["accessory"]["hit_rate"]
            cd_plus = s.item["armor"]["effect"] + s.item["accessory"]["evasion_rate"]
            hit_ritu = int(s.chara["dex"] / 10) + 51 + ci_plus

            if s.is_player_enemy:
                # 対人戦は旧版 wbattle.pl の双方計算を使う。
                winner_ci_plus = (
                    s.winner_item["weapon"]["effect"] +
                    s.winner_item["accessory"]["hit_rate"]
                )
                winner_cd_plus = (
                    s.winner_item["armor"]["effect"] +
                    s.winner_item["accessory"]["evasion_rate"]
                )
                winner_hit_ritu = int(s.winner["dex"] / 10) + 51 + winner_ci_plus
                winner_kaihi_ritu = int(s.winner["agi"] / 20)
                if winner_kaihi_ritu > 50:
                    winner_kaihi_ritu = 50
                winner_kaihi_ritu += winner_cd_plus
                player_kaihi_ritu = int(s.chara["agi"] / 20)
                if player_kaihi_ritu > 50:
                    player_kaihi_ritu = 50
                player_kaihi_ritu += cd_plus
                sake1 = 100 - int(winner_hit_ritu - player_kaihi_ritu) + s.sake1
                sake2 = 100 - int(hit_ritu - winner_kaihi_ritu) + s.sake2
            else:
                # モンスター戦は旧版 mbattle.pl の計算を使う。
                sake1 = int(s.chara["agi"] / 20) + cd_plus + s.sake1
                sake2 = s.mkahi - hit_ritu + s.sake2

            # 被ダメージの防御力減算。対人戦は相手防具にも同じ処理を行う。
            if s.dmg2 < 0:
                pass
            elif s.dmg2 < s.item["armor"]["def"]:
                s.dmg2 = 1 if s.is_player_enemy else 0
            else:
                s.dmg2 = s.dmg2 - s.item["armor"]["def"]

            if s.is_player_enemy:
                if s.dmg1 < 0:
                    pass
                elif s.dmg1 < s.winner_item["armor"]["def"]:
                    s.dmg1 = 1
                else:
                    s.dmg1 = s.dmg1 - s.winner_item["armor"]["def"]

            # 上級職による防御ボーナス
            if s.chara["job"] > 17:
                s.dmg2 = int(s.dmg2 / 4)
            elif s.chara["job"] > 7:
                s.dmg2 = int(s.dmg2 / 2)
            if s.is_player_enemy:
                if s.winner["job"] > 17:
                    s.dmg1 = int(s.dmg1 / 4)
                elif s.winner["job"] > 7:
                    s.dmg1 = int(s.dmg1 / 2)

            # プレイヤー回避判定
            evade_roll_max = 100 if s.is_player_enemy else 300
            if sake1 > random.randrange(evade_roll_max):
                s.dmg2 = 0
                s.com2 += f"<br><span class=\"red u-text-small\"><b>{s.chara['name']}は攻撃をかわした！</b></span>"
                
            # 敵回避判定
            if sake2 > random.randrange(100):
                s.dmg1 = 0
                s.com1 += f"<br><span class=\"red u-text-small\"><b>{s.mname}は攻撃をかわした！</b></span>"
                
            # === 7. HPの減算処理 (hp_sum) ===
            s.khp = s.khp - s.dmg2 - s.dmgme1 + s.hpplus1
            if s.khp > s.chara["max_hp"]:
                s.khp = s.chara["max_hp"]
                
            s.mhp = s.mhp - s.dmg1 + s.hpplus2
            if s.mhp > s.mhp_flg:
                s.mhp = s.mhp_flg
                
            # === 8. ログの追記 ===
            # ターンログを構築
            turn_log = {
                "turn": s.i,
                "player_hp": max(0, s.khp),
                "player_max_hp": s.chara["max_hp"],
                "enemy_hp": max(0, s.mhp),
                "enemy_max_hp": s.mhp_flg,
                "com1": s.com1,
                "com2": s.com2,
                "dmg1": s.dmg1,
                "dmg2": s.dmg2,
                "kaihuku1": s.kaihuku1,
                "kaihuku2": s.kaihuku2
            }
            self.battle_logs.append(turn_log)
            
            # === 9. 勝敗判定 (winlose) ===
            if s.is_player_enemy and s.mhp <= 0 and s.khp <= 0:
                win = 2 # 旧版 wbattle.pl の相打ち
                break
            elif s.mhp <= 0:
                win = 1 # プレイヤー勝利
                break
            elif s.khp <= 0:
                win = 0 # プレイヤー敗北
                break
                
        return win, self.battle_logs


def process_levelup(chara, exp_gained, syoku_master=None):
    """
    経験値を加算し、必要に応じてレベルアップ処理を行います。
    chara: キャラクターデータの辞書 (chara.json)
    exp_gained: 獲得経験値
    syoku_master: 職業熟練度データの辞書 (syoku.json)

    戻り値:
      comment (str): レベルアップ時のログ（HTML）
      lvup_count (int): レベルアップした回数
    """
    chara["exp"] += exp_gained
    lvup_count = 0
    comment = ""
    
    # 職業データのロード
    base_dir = os.path.dirname(os.path.abspath(__file__))
    syoku_file_path = os.path.join(base_dir, config.Config['syoku_file'])
    if not os.path.exists(syoku_file_path):
        syoku_file_path = os.path.join(os.path.dirname(base_dir), config.Config['syoku_file'])
        
    jobs = []
    try:
        with open(syoku_file_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except Exception:
        pass
        
    job_idx = chara.get("job", 0)
    sy_limits = [0] * 8 # str, int, mnd, vit, dex, agi, cha, karma
    if job_idx < len(jobs):
        job_data = jobs[job_idx]
        sy_limits[0] = job_data.get("limit_str", 0)
        sy_limits[1] = job_data.get("limit_int", 0)
        sy_limits[2] = job_data.get("limit_mnd", 0)
        sy_limits[3] = job_data.get("limit_vit", 0)
        sy_limits[4] = job_data.get("limit_dex", 0)
        sy_limits[5] = job_data.get("limit_agi", 0)
        sy_limits[6] = job_data.get("limit_cha", 0)
        sy_limits[7] = job_data.get("limit_karma", 0)

    # レベルアップ基本係数
    lv_up_coeff = config.Config['level_up_coeff']
    
    while chara["level"] < config.Config['max_level'] and chara["exp"] >= (chara["level"] * lv_up_coeff):
        chara["exp"] -= int(chara["level"] * lv_up_coeff)
        lvup_count += 1
        chara["level"] += 1
        
        # HP上昇量: vitをベースとしたランダム値 (rand(vit) * 3 + vit)
        vit_val = chara.get("vit", 1)
        hpup = random.randint(0, max(0, vit_val - 1)) * 3 + vit_val
        
        chara["max_hp"] += hpup
        if chara["max_hp"] > config.Config['max_hp']:
            chara["max_hp"] = config.Config['max_hp']
            
        # ステータス上昇判定 (50%の確率で上昇)
        attrs = ["str", "int", "mnd", "vit", "dex", "agi", "cha"]
        for idx, attr in enumerate(attrs):
            limit_val = sy_limits[idx]
            if limit_val > 0 and random.randrange(2) == 0:
                up_val = random.randint(0, limit_val - 1) + 1
                chara[attr] += up_val
                if chara[attr] > config.Config['max_param']:
                    chara[attr] = config.Config['max_param']
                    
        # カルマ上昇判定
        limit_karma = sy_limits[7]
        if limit_karma > 0 and random.randrange(2) == 0:
            up_karma = random.randint(0, limit_karma - 1) + 1
            chara["karma"] += up_karma
            if chara["karma"] > config.Config['max_param']:
                chara["karma"] = config.Config['max_param']

    if lvup_count > 0:
        comment += f'<font class=red size=5>レベルが {lvup_count} 上がりました！</font><br>'
        
        # 職業熟練度(job_level)の上昇
        old_job_level = chara.get("job_level", 0)
        chara["job_level"] += lvup_count
        
        # 熟練度が60に達し、マスター登録される場合
        job_name = config.Config['chara_jobs'][job_idx] if job_idx < len(config.Config['chara_jobs']) else "不明な職業"
        if chara["job_level"] >= 60 and old_job_level < 60:
            comment += f'<font class=red size=5>{job_name}をマスターしました！！</font><br>'
            if syoku_master is not None:
                syoku_master[str(job_idx)] = 60
                
    return comment, lvup_count
