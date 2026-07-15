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
try:
    from . import skills
except ImportError:
    import skills
try:
    import config
except ImportError:
    from .. import config

# O(1)メンバーシップテストのための定数定義 (ガイドライン2.4に準拠し、線形探索を回避して高速化)
_SPECIAL_MODES: frozenset[str] = frozenset({"isekiai", "genei"})

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

def get_job_dmg(job, chara, weapon_dmg):
    """
    職業に応じたプレイヤーの基礎ダメージを算出します (battle.pl の syokuzero〜syokuthirty に相当)
    """
    def r(attr):
        val = chara.get(attr, 1)
        return random.randrange(max(1, int(val)))

    # 7=str, 8=int, 9=dex, 10=vit, 11=agi, 12=mnd, 13=lck
    if job == 0: return r("str") + weapon_dmg
    elif job == 1: return r("int") + weapon_dmg
    elif job == 2: return r("dex") + weapon_dmg
    elif job == 3: return r("vit") + weapon_dmg
    elif job == 4: return r("int") + weapon_dmg
    elif job == 5: return r("int") + weapon_dmg
    elif job == 6: return r("dex") + r("lck") + weapon_dmg
    elif job == 7: return r("int") + r("lck") + weapon_dmg
    elif job == 8: return r("str") + r("vit") + weapon_dmg
    elif job == 9: return r("int") + r("dex") + weapon_dmg
    elif job == 10: return r("str") + r("dex") + weapon_dmg
    elif job == 11: return r("str") + r("int") + weapon_dmg
    elif job == 12: return r("str") + r("vit") + weapon_dmg
    elif job == 13: return r("str") + r("agi") + weapon_dmg
    elif job == 14: return r("str") + r("int") + weapon_dmg
    elif job == 15: return r("str") + r("int") + weapon_dmg
    elif job == 16: return r("str") + r("agi") + weapon_dmg
    elif job == 17: return r("int") + r("dex") + r("lck") + weapon_dmg
    elif job == 18:
        # 学者 (全パラメータの合計)
        total = sum(int(chara.get(k, 0)) for k in ["str", "int", "dex", "vit", "agi", "mnd", "lck", "lp"])
        return random.randrange(max(1, total)) + weapon_dmg
    elif job == 19:
        # バーサーカー (力のみ極大)
        return r("str") * 2 + weapon_dmg
    elif job >= 20 and job <= 29:
        # 上級職: 各種能力値を複合したダメージ
        return r("str") + r("int") + r("dex") + weapon_dmg
    else:
        # その他/マスター職
        total_kiso = r("str") + r("int") + r("dex") + r("vit") + r("agi") + r("mnd") + r("lck")
        return int(total_kiso * 1.5) + weapon_dmg

class BattleSimulator:
    """
    戦闘実行シミュレーター。
    """
    def __init__(self, mode, chara, item, enemy_data, is_player_enemy=False):
        self.state = BattleState(mode, chara, item, enemy_data, is_player_enemy)
        self.battle_logs = []
        
    def simulate(self):
        s = self.state
        
        # アクセサリーによるパッシブ補正 (acs_add 相当)
        # 命中率や回避率などの上昇値を設定
        s.a_hitup = int(s.item["accessory"]["bonus"]["dex"])
        s.a_kaihiup = int(s.item["accessory"]["bonus"]["agi"])
        s.a_wazaup = int(s.item["accessory"]["bonus"]["lp"])
        
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
            s.waza_ritu = int(s.chara["lp"] / 15) + 10 + s.chara["job_level"]
            if s.waza_ritu > 75: s.waza_ritu = 75
            s.waza_ritu += s.a_wazaup
            if s.waza_ritu > 95: s.waza_ritu = 95
            
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
                # 敵プレイヤーの必殺技
                skills.run_skill("wtech", s.winner["job"], "hissatu", s)
            else:
                # 敵モンスターのスキル (mons_X.mons_waza)
                skills.run_skill("mons", s.monstac, "mons_waza", s)
                
            # === 4. アクセサリー効果の発動 (acs_waza / wacs_waza) ===
            skills.run_skill("acstech", s.item["accessory"]["effect_id"], "hissatu", s)
            if s.is_player_enemy:
                skills.run_skill("wacstech", s.winner_item["accessory"]["effect_id"], "hissatu", s)
                
            # === 5. クリティカル判定 (mons_clt / clt) ===
            kclt_ritu = 100 - int(s.khp / s.chara["max_hp"] * 100) if s.chara["max_hp"] > 0 else 0
            if kclt_ritu > random.randrange(100):
                s.com1 += f"<br><span class=\"red u-text-medium\"><b>クリティカルヒット！！</b>「{s.chara['comment']}」</span>"
                s.dmg1 = s.dmg1 * 3
                
            if s.is_player_enemy:
                mclt_ritu = 100 - int(s.mhp / s.winner["max_hp"] * 100) if s.winner["max_hp"] > 0 else 0
                if mclt_ritu > random.randrange(100):
                    s.com2 += f"<br><span class=\"red u-text-medium\"><b>クリティカルヒット！！</b>「{s.winner['comment']}」</span>"
                    s.dmg2 = s.dmg2 * 3
            else:
                mclt_ritu = 100 - int(s.mhp / s.mhp_flg * 100) if s.mhp_flg > 0 else 0
                if mclt_ritu > random.randrange(200):
                    s.com2 += f"<br><span class=\"red\"><b>クリティカルヒット！！</b></span>"
                    s.dmg2 = s.dmg2 + s.item["armor"]["def"] # 防御無視相当の加算
                    
            # === 6. 防御力による減算・回避判定 (mons_kaihi) ===
            # 防護効果
            ci_plus = s.item["weapon"]["effect"] + s.item["accessory"]["attrib"]
            cd_plus = s.item["armor"]["effect"] + s.item["accessory"]["spare1"]
            
            # 命中率・回避率
            hit_ritu = int(s.chara["agi"] / 10) + 51 + ci_plus
            sake1 = int(s.chara["mnd"] / 20) + cd_plus + s.sake1
            sake2 = s.mkahi - hit_ritu + s.sake2
            
            # 防御力による被ダメ減算
            if s.dmg2 < 0:
                pass
            elif s.dmg2 < s.item["armor"]["def"]:
                s.dmg2 = 0
            else:
                s.dmg2 = s.dmg2 - s.item["armor"]["def"]
                
            # 上級職による防御ボーナス
            if s.chara["job"] > 17:
                s.dmg2 = int(s.dmg2 / 4)
            elif s.chara["job"] > 7:
                s.dmg2 = int(s.dmg2 / 2)
                
            # プレイヤー回避判定
            if sake1 > random.randrange(300):
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
            if s.mhp <= 0:
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
    sy_limits = [0] * 8 # str, int, dex, vit, agi, mnd, lck, lp
    if job_idx < len(jobs):
        job_data = jobs[job_idx]
        sy_limits[0] = job_data.get("limit_str", 0)
        sy_limits[1] = job_data.get("limit_int", 0)
        sy_limits[2] = job_data.get("limit_dex", 0)
        sy_limits[3] = job_data.get("limit_vit", 0)
        sy_limits[4] = job_data.get("limit_agi", 0)
        sy_limits[5] = job_data.get("limit_mnd", 0)
        sy_limits[6] = job_data.get("limit_lck", 0)
        sy_limits[7] = job_data.get("limit_lp", 0)

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
        attrs = ["str", "int", "dex", "vit", "agi", "mnd", "lck"]
        for idx, attr in enumerate(attrs):
            limit_val = sy_limits[idx]
            if limit_val > 0 and random.randrange(2) == 0:
                up_val = random.randint(0, limit_val - 1) + 1
                chara[attr] += up_val
                if chara[attr] > config.Config['max_param']:
                    chara[attr] = config.Config['max_param']
                    
        # LP上昇判定
        limit_lp = sy_limits[7]
        if limit_lp > 0 and random.randrange(2) == 0:
            up_lp = random.randint(0, limit_lp - 1) + 1
            chara["lp"] += up_lp
            if chara["lp"] > config.Config['max_param']:
                chara["lp"] = config.Config['max_param']

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
