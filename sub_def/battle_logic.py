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
import os
import random
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
_TACTIC_ACTIVATION_DENOMINATORS = {
    "激高": 60,
    "高": 80,
    "中": 100,
    "低": 120,
    "超低": 180,
    "激低": 200,
}


def _load_tactic_activation_denominators():
    """戦術説明の発動率表記を、判定に使う乱数幅へ変換する。"""
    result = {}
    try:
        path = os.path.join(common.BASE_DIR, config.Config["tac_file"])
        with open(path, "r", encoding="utf-8") as file:
            tactics = common.decode_html_entities(json.load(file))
    except (OSError, TypeError, ValueError, KeyError):
        return result

    # 長い表記を先に確認する（「激低」を「低」と誤認しないため）。
    labels = ("激高", "超低", "激低", "高", "中", "低")
    for tactic in tactics:
        if tactic.get("activation_denominator") is not None:
            result[int(tactic["no"])] = max(1, int(tactic["activation_denominator"]))
            continue
        description = str(tactic.get("desc", ""))
        for label in labels:
            if f"発動率{label}" in description:
                result[int(tactic["no"])] = _TACTIC_ACTIVATION_DENOMINATORS[label]
                break
    return result


_TACTIC_ACTIVATION_DENOMINATORS_BY_ID = _load_tactic_activation_denominators()


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
            self.monster_gold_reward = 0
            self.monster_exp_reward = 0
            self.monster_random_range = 0
            self.monster_hp_base = 0
            self.monster_base_damage = 0
            self.monster_evasion_rate = 0
            self.monster_special_skill_id = "0"
            self.monster_special_rate = 0
        # 対戦相手がモンスターの場合
        else:
            self.winner = {"id": "sys", "name": "モンスター"}
            self.mname = enemy_data["name"]
            self.monster_exp_reward = enemy_data["exp_reward"]
            self.monster_random_range = enemy_data["random_range"]
            self.monster_hp_base = enemy_data["hp_base"]
            self.monster_base_damage = enemy_data["base_damage"]
            self.monster_evasion_rate = enemy_data["evasion_rate"]
            self.monster_special_skill_id = enemy_data["special_skill_id"]
            self.monster_special_rate = enemy_data["special_rate"]
            self.monster_gold_reward = enemy_data["gold_reward"]
            
            # モンスターのHP決定
            self.mhp = random.randrange(max(1, self.monster_random_range)) + self.monster_hp_base
            self.mhp_flg = self.mhp
            
        # プレイヤー状態
        self.khp = chara["hp"]

        # 戦闘中の金銭変動。旧版の盗み技は戦闘後の報酬を増減させる。
        self.player_gold = max(0, int(chara.get("gold", 0)))
        self.gold_base = max(0, int(self.monster_gold_reward))
        self.gold_reward_bonus = 0
        self.gold_reward_penalty = 0
        self.steal_success_count = 0
        self.steal_limit_reported = False
        self.steal_reward_cap = max(
            0,
            int(
                self.gold_base
                * config.Config.get("monster_steal_reward_cap_multiplier", 1)
            ),
        )
        self.steal_max_successes = max(
            0, int(config.Config.get("monster_steal_max_successes", 3))
        )
        
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
        self.damage_heal_ratio1 = 0
        self.damage_heal_ratio2 = 0
        self.charadown = {}
        
        # ターンカウンタ
        self.i = 1
        self.j = 0
        self.turn = config.Config['max_turns']
        
        # 回避率などの事前計算用補正
        self.a_hitup = 0
        self.a_kaihiup = 0
        self.a_wazaup = 0
        self.player_activation_denominator = None
        self.winner_activation_denominator = None

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
            r("dex") + r("agi") + r("cha") +
            int(chara.get("karma", 0))
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


def get_tactic_id(chara):
    """戦闘で使用する戦術IDを取得する（旧版 chara[30] / winner[37] 相当）。"""
    try:
        return max(0, int((chara or {}).get("tactic_id", 0)))
    except (TypeError, ValueError):
        return 0


def get_tactic_activation_denominator(chara):
    """選択中の戦術に設定された発動率の乱数幅を返す。"""
    return _TACTIC_ACTIVATION_DENOMINATORS_BY_ID.get(get_tactic_id(chara))

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
        self.state.player_activation_denominator = get_tactic_activation_denominator(self.state.chara)
        if is_player_enemy:
            self.state.winner_activation_denominator = get_tactic_activation_denominator(self.state.winner)
        self.battle_logs = []
        
    def simulate(self):
        s = self.state
        
        # アクセサリーによる特殊補正 (旧版 acs: hitup, kaihiup, wazaup)
        s.a_hitup = int(s.item["accessory"].get("hit_rate", 0))
        s.a_kaihiup = int(s.item["accessory"].get("evasion_rate", 0))
        s.a_wazaup = int(s.item["accessory"].get("special_rate", 0))
        
        # モンスター戦の時間切れは引き分け(2)、対人戦の時間切れは
        # 相打ち引き分けと区別する専用結果(3)を返す。
        win = 3 if s.is_player_enemy else 2
        
        for turn_idx in range(1, s.turn + 1):
            s.i = turn_idx
            
            # === 1. ターン初期化 (shokika) ===
            # プレイヤーダメージ
            s.dmg1 = get_job_dmg(s.chara["job"], s.chara, s.item["weapon"]["atk"])
            # 敵ダメージ
            if s.is_player_enemy:
                # 対人戦の場合、相手の職業ダメージを計算
                s.dmg2 = get_job_dmg(s.winner["job"], s.winner, s.winner_item["weapon"]["atk"])
                s.com2 = f"{s.mname}の攻撃！"
            else:
                s.dmg2 = s.monster_base_damage + random.randrange(max(1, s.monster_random_range))
                # 旧版 genei は各ターン開始時に、防具の防御力を敵攻撃へ加算していた。
                if s.mode == "genei":
                    s.dmg2 += s.item["armor"]["defense"]
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
            s.damage_heal_ratio1 = 0
            s.damage_heal_ratio2 = 0
            s.huin = 0
            
            # === 2. プレイヤー必殺技発動判定 (tyosenwaza / hissatu) ===
            s.waza_ritu = int(s.chara["karma"] / 15) + 10 + s.chara["job_level"]
            if s.waza_ritu > 75: s.waza_ritu = 75
            s.waza_ritu += s.a_wazaup
            if s.waza_ritu > 95: s.waza_ritu = 95

            # 対人戦の相手(王者)側の必殺率。プレイヤー側と同じ式で算出する。
            # モンスター戦では winner に karma/job_level が無いため 0 起点となり、実際には monster_special_rate が使われる。
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
                
            # 戦術必殺技の動的実行。職業IDではなく選択中の戦術IDを使う。
            # 旧版 battle.pl は chara[30]、対人戦の王者側は winner[37] を
            # tech/wtech のファイル番号として読み込んでいた。
            skills.run_skill("tech", get_tactic_id(s.chara), "hissatu", s)
            
            # === 3. 敵スキル発動判定 ===
            if s.is_player_enemy:
                # 旧版 wbattle.pl の winwaza 相当。王者側にもHPピンチ時の
                # リミットブレイク判定がある。
                if int(s.winner["max_hp"] / 10) > s.mhp and random.randrange(4) > 1:
                    s.wwaza_ritu += 999
                    s.com2 += "<br><font class=\"red\" size=4><b>LIMIT BREAK!!</b></font>"
                # 敵プレイヤーの必殺技も、王者側の選択戦術を使用する。
                skills.run_skill("wtech", get_tactic_id(s.winner), "whissatu", s)
            else:
                # 敵モンスターのスキル (mons_X.mons_waza)
                skills.run_skill("mons", s.monster_special_skill_id, "mons_waza", s)
                
            # === 4. 職業の後発効果とアクセサリー効果 (acs_waza / wacs_waza) ===
            # 旧版では必殺技(hissatu)とは別に、通常攻撃後の atowaza と
            # アクセサリー固有効果の acskouka をこの順で実行していた。
            skills.run_skill("tech", get_tactic_id(s.chara), "atowaza", s)
            skills.run_skill("acstech", s.item["accessory"]["effect_id"], "acskouka", s)
            if s.is_player_enemy:
                skills.run_skill("wtech", get_tactic_id(s.winner), "watowaza", s)
                skills.run_skill("wacstech", s.winner_item["accessory"]["effect_id"], "wacskouka", s)
            else:
                skills.run_skill("mons", s.monster_special_skill_id, "mons_atowaza", s)

            # 旧版 wbattle.pl battle_clt の初手逆転必殺判定。
            if s.is_player_enemy and s.i == 1:
                counterattack_level_gap = int(config.Config.get("counterattack_level_gap", 15))
                counterattack_damage_multiplier = int(config.Config.get("counterattack_damage_multiplier", 100))
                player_weapon_dmg = s.item["weapon"]["atk"]
                winner_weapon_dmg = s.winner_item["weapon"]["atk"]
                if (
                    int(s.winner.get("level", 0)) - int(s.chara.get("level", 0)) >= counterattack_level_gap
                    or player_weapon_dmg < winner_weapon_dmg
                ):
                    s.dmg1 = s.dmg1 * counterattack_damage_multiplier
                    s.sake2 -= 999999
                    s.winner_item["weapon"]["atk"] = 0
                    s.com1 += "<font color=\"blue\" size=5>逆転必殺技発動！！</font><br>"
                if (
                    int(s.chara.get("level", 0)) - int(s.winner.get("level", 0)) >= counterattack_level_gap
                    or s.winner_item["weapon"]["atk"] < s.item["armor"]["defense"]
                ):
                    s.dmg2 = s.dmg2 * 100
                    s.sake1 -= 999999
                    s.com2 += "<font color=\"red\" size=5>逆転必殺技発動！！</font><br>"
                
            # === 5. クリティカル判定 (mons_clt / clt) ===
            # 回復・補助技は dmg1/dmg2 を 0 にするため、実ダメージがある攻撃だけ判定する。
            # これを無条件で行うと、ケアルガ等にもクリティカル表示が付き、
            # 0 ダメージへ補正値が加算されて攻撃扱いになる。
            if s.dmg1 > 0:
                kclt_ritu = 100 - int(s.khp / s.chara["max_hp"] * 100) if s.chara["max_hp"] > 0 else 0
                if kclt_ritu > random.randrange(100):
                    s.com1 += f"<br><span class=\"red text-medium\"><b>クリティカルヒット！！</b>「{html.escape(str(s.chara.get('comment', '')))}」</span>"
                    if s.is_player_enemy:
                        # 旧版 wbattle.pl: 挑戦者の攻撃は2倍し、王者の武器攻撃力を加算。
                        s.dmg1 = s.dmg1 * 2 + s.winner_item["weapon"]["atk"]
                    else:
                        s.dmg1 = s.dmg1 * 3

            if s.is_player_enemy:
                if s.dmg2 > 0:
                    mclt_ritu = 100 - int(s.mhp / s.winner["max_hp"] * 100) if s.winner["max_hp"] > 0 else 0
                    if mclt_ritu > random.randrange(100):
                        s.com2 += f"<br><span class=\"red text-medium\"><b>クリティカルヒット！！</b>「{html.escape(str(s.winner.get('comment', '')))}」</span>"
                        # 旧版 wbattle.pl: 王者の攻撃は2倍し、挑戦者の防具防御力を加算。
                        s.dmg2 = s.dmg2 * 2 + s.item["armor"]["defense"]
            elif s.dmg2 > 0:
                mclt_ritu = 100 - int(s.mhp / s.mhp_flg * 100) if s.mhp_flg > 0 else 0
                if mclt_ritu > random.randrange(200):
                    s.com2 += f"<br><span class=\"red\"><b>クリティカルヒット！！</b></span>"
                    s.dmg2 = s.dmg2 + s.item["armor"]["defense"] # 防御無視相当の加算
                    
            # === 6. 防御力による減算・回避判定 ===
            ci_plus = s.item["weapon"]["hit_rate"] + s.item["accessory"]["hit_rate"]
            cd_plus = s.item["armor"]["evasion_rate"] + s.item["accessory"]["evasion_rate"]
            hit_ritu = int(s.chara["dex"] / 10) + 51 + ci_plus
            defense_blocked1 = False
            defense_blocked2 = False
            player_evaded = False
            enemy_evaded = False

            if s.is_player_enemy:
                # 対人戦は旧版 wbattle.pl の双方計算を使う。
                winner_ci_plus = (
                    s.winner_item["weapon"]["hit_rate"] +
                    s.winner_item["accessory"]["hit_rate"]
                )
                winner_cd_plus = (
                    s.winner_item["armor"]["evasion_rate"] +
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
                sake2 = s.monster_evasion_rate - hit_ritu + s.sake2

            # 被ダメージの防御力減算。対人戦は相手防具にも同じ処理を行う。
            raw_dmg2 = s.dmg2
            if s.dmg2 < 0:
                pass
            elif s.dmg2 < s.item["armor"]["defense"]:
                s.dmg2 = 1 if s.is_player_enemy else 0
            else:
                s.dmg2 = s.dmg2 - s.item["armor"]["defense"]

            if s.is_player_enemy:
                raw_dmg1 = s.dmg1
                if s.dmg1 < 0:
                    pass
                elif s.dmg1 < s.winner_item["armor"]["defense"]:
                    s.dmg1 = 1
                else:
                    s.dmg1 = s.dmg1 - s.winner_item["armor"]["defense"]

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
            defense_blocked2 = raw_dmg2 > 0 and s.dmg2 == 0
            defense_blocked1 = (
                s.is_player_enemy and raw_dmg1 > 0 and s.dmg1 == 0
            )

            # プレイヤー回避判定
            evade_roll_max = 100 if s.is_player_enemy else 300
            if s.dmg2 > 0 and sake1 > random.randrange(evade_roll_max):
                s.dmg2 = 0
                player_evaded = True
                s.com2 += f"<br><span class=\"red text-small\"><b>{s.chara['name']}は攻撃をかわした！</b></span>"
                
            # 敵回避判定
            if s.dmg1 > 0 and sake2 > random.randrange(100):
                s.dmg1 = 0
                enemy_evaded = True
                s.com1 += f"<br><span class=\"red text-small\"><b>{s.mname}は攻撃をかわした！</b></span>"

            if defense_blocked1 and not enemy_evaded:
                s.com1 += (
                    f"<br><span class=\"yellow text-small\"><b>"
                    f"{s.chara['name']}は {s.mname} にダメージを与えることができなかった！"
                    f"</b></span>"
                )
            # 先制攻撃で敵が倒れた場合は、敵の攻撃を不発として明示する。
            enemy_will_be_defeated = s.mhp - s.dmg1 + s.hpplus2 <= 0
            if enemy_will_be_defeated and not enemy_evaded:
                s.dmg2 = 0
                s.com2 = (
                    f"<span class=\"yellow text-small\"><b>"
                    f"{s.mname}はすでに倒れていた！"
                    f"</b></span>"
                )
            elif defense_blocked2 and not player_evaded:
                s.com2 += (
                    f"<br><span class=\"yellow text-small\"><b>"
                    f"{s.mname}は {s.chara['name']} にダメージを与えることができなかった！"
                    f"</b></span>"
                )

            # ドレイン系は「実際に与えたダメージ」を基準に回復する。
            # 防御・回避後に計算することで、空振り時の不正な回復を防ぐ。
            if s.damage_heal_ratio1:
                damage_heal1 = max(0, int(s.dmg1 * s.damage_heal_ratio1))
                s.hpplus1 += damage_heal1
                if damage_heal1:
                    s.kaihuku1 += f"{s.chara['name']} のＨＰが {damage_heal1} 回復した！♪"
            if s.damage_heal_ratio2:
                damage_heal2 = max(0, int(s.dmg2 * s.damage_heal_ratio2))
                s.hpplus2 += damage_heal2
                if damage_heal2:
                    s.kaihuku2 += f"{s.winner['name']} のＨＰが {damage_heal2} 回復した！♪"
                
            # === 7. HPの減算処理 (hp_sum) ===
            # 現行・Ver2互換の同時精算。先攻・後攻を導入する場合は、
            # モンスター側を含む行動順の仕様を別途定義してから行う。
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
    # Ver2と同じく職業熟練度はMasterとなるLv60を上限にする。
    # 過去に60を超えて保存されたデータも、次の戦闘処理で正規化する。
    chara["job_level"] = min(60, max(0, int(chara.get("job_level", 0))))

    chara["exp"] += exp_gained
    lvup_count = 0
    comment = ""
    levelup_changes = {attr: 0 for attr in ("str", "int", "mnd", "vit", "dex", "agi", "cha", "karma")}
    hp_increase = 0
    
    # 職業マスターが読めない場合も、レベルアップ自体は継続する。
    jobs = common.load_json_list(config.Config["syoku_file"])
        
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
    level_up_exp_coeff = config.Config['level_up_exp_coeff']
    
    while chara["level"] < config.Config['max_level'] and chara["exp"] >= (chara["level"] * level_up_exp_coeff):
        chara["exp"] -= int(chara["level"] * level_up_exp_coeff)
        lvup_count += 1
        chara["level"] += 1
        
        # HP上昇量: vitをベースとしたランダム値 (rand(vit) * 3 + vit)
        vit_val = chara.get("vit", 1)
        hpup = random.randint(0, max(0, vit_val - 1)) * 3 + vit_val

        old_max_hp = chara["max_hp"]
        chara["max_hp"] += hpup
        if chara["max_hp"] > config.Config['max_hp']:
            chara["max_hp"] = config.Config['max_hp']
        hp_increase += chara["max_hp"] - old_max_hp
            
        # ステータス上昇判定 (50%の確率で上昇)
        attrs = ["str", "int", "mnd", "vit", "dex", "agi", "cha"]
        for idx, attr in enumerate(attrs):
            limit_val = sy_limits[idx]
            if limit_val > 0 and random.randrange(2) == 0:
                up_val = random.randint(0, limit_val - 1) + 1
                old_value = chara[attr]
                chara[attr] += up_val
                if chara[attr] > config.Config['max_param']:
                    chara[attr] = config.Config['max_param']
                levelup_changes[attr] += chara[attr] - old_value
                    
        # カルマ上昇判定
        limit_karma = sy_limits[7]
        if limit_karma > 0 and random.randrange(2) == 0:
            up_karma = random.randint(0, limit_karma - 1) + 1
            old_karma = chara["karma"]
            chara["karma"] += up_karma
            if chara["karma"] > config.Config['max_param']:
                chara["karma"] = config.Config['max_param']
            levelup_changes["karma"] += chara["karma"] - old_karma

    if lvup_count > 0:
        comment += f'<font class=red size=5>レベルが {lvup_count} 上がりました！</font><br>'

        stat_labels = {
            "str": "力",
            "int": "知能",
            "mnd": "信仰心",
            "vit": "生命力",
            "dex": "器用さ",
            "agi": "速さ",
            "cha": "魅力",
            "karma": "カルマ",
        }
        change_text = [
            f'{stat_labels[attr]}+{amount}'
            for attr, amount in levelup_changes.items()
            if amount > 0
        ]
        if hp_increase > 0:
            change_text.insert(0, f'最大HP+{hp_increase}')
        if change_text:
            comment += (
                '<span class="green">上昇した能力値: '
                + "、".join(change_text)
                + '</span><br>'
            )
        
        # 職業熟練度(job_level)の上昇
        old_job_level = chara["job_level"]
        chara["job_level"] = min(60, old_job_level + lvup_count)
        
        # 熟練度が60に達し、マスター登録される場合
        job_name = config.Config['chara_jobs'].get(job_idx, "不明な職業")
        if chara["job_level"] >= 60 and old_job_level < 60:
            comment += f'<font class=red size=5>{job_name}をマスターしました！！</font><br>'
            if syoku_master is not None:
                syoku_master[str(job_idx)] = 60
                
    return comment, lvup_count
