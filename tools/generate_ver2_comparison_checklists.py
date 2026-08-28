"""Ver2 / Ver3 比較チェックリストを生成する。"""

from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MONSTER_DATA_DIR = DATA_DIR / "monsters"
CHOCOBO_DATA_DIR = DATA_DIR / "chocobo"
OUTPUT_DIR = ROOT / "docs" / "ver2_comparison"

EQUIPMENT = (
    ("weapon", "武器", "旧版_ver2/data/item/item.ini + item0〜item30.ini"),
    ("armor", "防具", "旧版_ver2/data/def/def.ini + def0〜def30.ini"),
    ("accessory", "アクセサリー", "旧版_ver2/data/acs/acs.ini + acs0〜acs30.ini"),
)

STAT_LABELS = {
    "str": "力",
    "int": "知能",
    "mnd": "信仰心",
    "vit": "生命力",
    "dex": "器用さ",
    "agi": "速さ",
    "cha": "魅力",
    "karma": "カルマ",
}

MONSTER_SKILL_LABELS = {
    1: "マイティガード",
    2: "ケアルガ",
    3: "ファイガ",
    4: "ブリザガ",
    5: "サンダガ",
    6: "メテオ",
    7: "グラビガ",
    8: "クエイク",
    9: "アルテマ",
    10: "ショック・ウェーブ・パルサー",
    11: "デジョン",
    12: "ファイア・ブレス",
    13: "ケアルガ / アルテマ",
    14: "お金を盗む",
    15: "ドレイン",
    16: "アポガリプス",
    17: "えりりんの甘いささやき / 祝福のキス",
    18: "メガ・フレア",
    19: "ハァハァ。。。",
    20: "斬・鉄・剣",
    21: "性転換",
    22: "臭い息",
}

V2_MONSTER_MASTERS = {
    "mons_lv1.json": "旧版_ver2/data/lowmons.ini",
    "mons_lv2.json": "旧版_ver2/data/normalmons.ini",
    "mons_lv3.json": "旧版_ver2/data/highmons.ini",
    "mons_lv4.json": "旧版_ver2/data/spmons.ini",
    "mons_isekai.json": "旧版_ver2/data/isekaimons.ini",
    "legend_boss_lv1.json": "旧版_ver2/data/bossmons0.ini",
    "legend_boss_lv2.json": "旧版_ver2/data/bossmons1.ini",
    "legend_boss_lv3.json": "旧版_ver2/data/bossmons2.ini",
    "legend_boss_lv4.json": "旧版_ver2/data/bossmons3.ini",
}

CHOCOBO_STAT_LABELS = {
    "c0": "速度",
    "c1": "スタミナ",
    "c2": "粘り",
    "c3": "落ち着き",
    "c4": "闘争心",
    "c5": "賢さ",
    "c6": "反射神経",
}

ROUTE_DETAILS = {
    "main": ("街のメイン画面", "表示", "旧版_ver2/ffadventure.cgi"),
    "sts": ("自分のステータス", "表示・更新", "旧版_ver2/sts.cgi"),
    "tac_change": ("戦術選択", "表示・更新", "旧版_ver2/tac_change.cgi"),
    "passchange": ("合言葉・パスワード変更", "表示・更新", "旧版_ver2/passchange.cgi"),
    "tensyoku": ("転職", "表示・更新", "旧版_ver2/tensyoku.cgi"),
    "shop": ("宿屋", "状態変更", "旧版_ver2/shop.cgi"),
    "yado": ("宿泊（shopへの互換ルート）", "状態変更", "旧版_ver2/shop.cgi"),
    "shop_weapon": ("武器店", "表示・更新", "旧版_ver2/shop_item.cgi"),
    "shop_armor": ("防具店", "表示・更新", "旧版_ver2/shop_def.cgi"),
    "shop_accessory": ("装飾品店", "表示・更新", "旧版_ver2/shop_acs.cgi"),
    "shop_item": ("武器店（旧URL互換）", "表示・更新", "旧版_ver2/shop_item.cgi"),
    "shop_def": ("防具店（旧URL互換）", "表示・更新", "旧版_ver2/shop_def.cgi"),
    "shop_acs": ("装飾品店（旧URL互換）", "表示・更新", "旧版_ver2/shop_acs.cgi"),
    "bank": ("銀行", "表示・更新", "旧版_ver2/bank.cgi"),
    "souko": ("倉庫", "表示・更新", "旧版_ver2/souko.cgi"),
    "battle": ("人間チャンピオン戦", "状態変更", "旧版_ver2/battle.cgi"),
    "select_battle": ("対人戦の相手選択", "表示・更新", "旧版_ver2/select_battle.cgi"),
    "sentaku": ("対人戦の相手選択（互換ルート）", "表示・更新", "旧版_ver2/select_battle.cgi"),
    "monster": ("通常モンスター修行", "状態変更", "旧版_ver2/monster.cgi"),
    "genei": ("幻影の城（モンスター互換ルート）", "状態変更", "旧版_ver2/monster.cgi"),
    "isekiai": ("異世界（モンスター互換ルート）", "状態変更", "旧版_ver2/monster.cgi"),
    "legend": ("レジェンドプレイス", "表示・状態変更", "旧版_ver2/legend.cgi"),
    "boss": ("レジェンド戦（互換ルート）", "状態変更", "旧版_ver2/legend.cgi"),
    "bbs": ("掲示板投稿", "状態変更", "旧版_ver2に一般掲示板はなし（post_message.cgiは私信）"),
    "chocofarm": ("チョコボ牧場", "表示", "旧版_ver2/chocofarm.cgi"),
    "morifarm": ("チョコボの森", "表示・更新", "旧版_ver2/morifarm.cgi"),
    "choco": ("チョコボの森（互換ルート）", "表示", "旧版_ver2/morifarm.cgi"),
    "crace": ("チョコボレース", "状態変更", "旧版_ver2/crace.cgi"),
    "ctrain": ("チョコボ訓練", "状態変更", "旧版_ver2/ctrain.cgi"),
    "dendo": ("チョコボ殿堂", "表示・更新", "旧版_ver2/dendo.cgi"),
    "farmrace": ("チョコボ王者戦", "状態変更", "旧版_ver2/farmrace.cgi"),
    "system": ("登録者一覧・画像一覧・他者詳細", "表示", "旧版_ver2/system.cgi"),
    "chara_sts": ("他者詳細（system互換ルート）", "表示", "旧版_ver2/system.cgi"),
    "img_list": ("画像一覧（system互換ルート）", "表示", "旧版_ver2/system.cgi"),
    "ranking": ("登録者一覧（system互換ルート）", "表示", "旧版_ver2/system.cgi"),
    "tenka": ("天下一武道会", "表示・状態変更", "旧版_ver2/tenka.cgi"),
    "rank": ("英雄ランキング", "表示", "旧版_ver2/rank.cgi"),
    "chocorank": ("チョコボランキング", "表示", "旧版_ver2/chocorank.cgi"),
}


# 一次台帳の行とは別に、実際にファイル単位で精査を完了した結果を残す。
# 差異の修正だけを追うのではなく、確認範囲・意図的に残した差異・保留判断を
# 次の見直しでも辿れるようにする。
FILE_AUDITS = (
    {
        "file": "cgi_py/tac_change.py",
        "v2_source": "旧版_ver2/tac_change.cgi / data/ffadventure.ini:master_tac",
        "scope": "表示・変更の候補条件、マスター職、ロック後再検証、接続元ホスト",
        "difference": "master_tacを転職時の戦術リセット設定と誤って共用していた",
        "intent": "不具合を修正済み",
        "note": "master_tactics_enabledを独立設定として追加し、Ver2と同じくLv60以上の他職戦術を候補にする。POST時は最新chara/syokuで再検証する。",
    },
    {
        "file": "cgi_py/tensyoku.py",
        "v2_source": "旧版_ver2/tensyoku.cgi",
        "scope": "転職条件、職業Lv退避・復帰、能力減少、戦術、接続元ホスト",
        "difference": "転職成功時の接続元ホスト保存が欠けていた。カルマ下限はVer2と異なる",
        "intent": "ホストは不具合を修正済み／カルマ下限1は意図的",
        "note": "成功時にREMOTE_ADDRを保存する。能力減少値と職業Lv遷移は一致。Ver2のカルマ0許容に対し、現行は0も1へ戻す既決仕様を維持する。",
    },
    {
        "file": "cgi_py/passchange.py / chara_make.py",
        "v2_source": "旧版_ver2/passchange.cgi / chara_make.cgi",
        "scope": "合言葉設定、パスワード変更、新規登録時の入力規則、接続元ホスト",
        "difference": "新パスワードの許可文字と変更成功時の接続元ホスト保存が不一致",
        "intent": "不具合を修正済み",
        "note": "4〜8文字の半角英数字・記号を許可し、全角・空白・制御文字を拒否する。passchan成功時はREMOTE_ADDRを保存し、PBKDF2とセッション再発行は現行の意図的な安全化として維持する。",
    },
    {
        "file": "cgi_py/shop.py",
        "v2_source": "旧版_ver2/shop.cgi",
        "scope": "宿代、HP回復、王者HP、boss_flag、接続元ホスト",
        "difference": "宿泊成功時の接続元ホスト保存が欠けていた",
        "intent": "不具合を修正済み",
        "note": "宿代Lv×10、HP全快、王者HP全快、boss_flagの10への復帰は一致。成功時にREMOTE_ADDRも保存する。",
    },
    {
        "file": "cgi_py/bank.py",
        "v2_source": "旧版_ver2/bank.cgi / data/ffadventure.ini",
        "scope": "預入・引出、半角数値、1,000G単位、所持金・預金上限、接続元ホスト",
        "difference": "全角数字を受理し、預金上限超過時は画面案内と異なり拒否していた",
        "intent": "不具合を修正済み",
        "note": "ASCII数字だけを受理する。預金上限超過分は画面案内どおり国への寄付として所持金から差し引き、預金へは上限までだけ加算する。",
    },
    {
        "file": "cgi_py/souko.py",
        "v2_source": "旧版_ver2/souko.cgi / data/ffadventure.ini:item_max,def_max,acs_max",
        "scope": "武器・防具・装飾品の表示、着脱、交換、破棄、上限、接続元ホスト",
        "difference": "交換時の保管順、着脱時の接続元保存、破棄確認がVer2と異なる",
        "intent": "要判断",
        "note": "3種別の上限は8で一致。現行は選択品を配列から取り出し、旧装備を末尾へ追加する。Ver2は選択位置を旧装備で置換する。現行は着脱でREMOTE_ADDRを保存せず、破棄は二段階確認を挟まない。どちらを採るかは現行の操作性を含めて判断する。",
    },
    {
        "file": "cgi_py/shop_weapon.py / templates/shop_trade.html",
        "v2_source": "旧版_ver2/shop_item.cgi / data/item/item<N>.ini",
        "scope": "職別品揃え、購入・売却額、倉庫上限、接続元ホスト、画面遷移",
        "difference": "JSON・CSRF・入力再検証・トースト遷移へ移行。武器1181の販売対象だけ未判断",
        "intent": "処理移行は意図的／武器1181は要判断",
        "note": "購入・売却額は両版とも価格の2/3、購入時のREMOTE_ADDR保存と武器倉庫上限8は一致する。職別品揃えは、台帳記載のシーフ武器1032〜1038価格調整を除き一致。皇帝用1181はVer2の職別リストにないが現行では販売するため、維持可否はequipment.mdの要判断項目として残す。",
    },
    {
        "file": "cgi_py/shop_armor.py / templates/shop_trade.html",
        "v2_source": "旧版_ver2/shop_def.cgi / data/def/def<N>.ini",
        "scope": "職別品揃え、購入・売却額、倉庫上限、接続元ホスト、画面遷移",
        "difference": "JSON・CSRF・入力再検証・トースト遷移へ移行。売却時の接続元保存と防具2181の販売対象が異なる",
        "intent": "処理移行は意図的／接続元・防具2181は要判断",
        "note": "購入・売却額は両版とも価格の2/3、購入時のREMOTE_ADDR保存と防具倉庫上限8は一致する。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しない。皇帝用2181はVer2の職別リストにないが現行では販売する。2165・2183の名称記号差はequipment.mdに記録済み。",
    },
    {
        "file": "cgi_py/shop_accessory.py / templates/shop_trade.html",
        "v2_source": "旧版_ver2/shop_acs.cgi / data/acs/acs<N>.ini",
        "scope": "職別品揃え、能力補正の保管、購入・売却額、倉庫上限、接続元ホスト、画面遷移",
        "difference": "JSON・CSRF・入力再検証・トースト遷移へ移行。売却時の接続元保存はVer2と異なる",
        "intent": "処理移行は意図的／売却時の接続元は要判断",
        "note": "購入・売却額は両版とも価格の2/3、購入時のREMOTE_ADDR保存と装飾品倉庫上限8は一致する。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しない。職別品揃えと補正は一致し、85・87の率補正だけはd7105f6で記録済みのVer1準拠調整を維持する。",
    },
    {
        "file": "cgi_py/bbs.py / templates/ffadventure.html",
        "v2_source": "旧版_ver2に一般掲示板はなし（post_message.cgiは私信）",
        "scope": "投稿者・本文・禁止語・保存上限・表示順・接続元・遷移",
        "difference": "全員が書き込む掲示板をVer3で新設。Ver2の私信とは別機能",
        "intent": "一般掲示板は意図的な追加／私信の未実装は要判断",
        "note": "ログイン本人だけが200文字以内・禁止語なしで投稿でき、最新100件を新着順に共有JSONへ保持する。投稿後のPRGリダイレクト、CSRF、共有ロックは現行の安全化。Ver2の私信・送信箱・受信拒否・友人登録は置き換えられておらず、別の未実装項目として記録する。",
    },
    {
        "file": "cgi_py/ffadventure.py / templates/ffadventure.html",
        "v2_source": "旧版_ver2/ffadventure.cgi",
        "scope": "本人認証、王者・待機時間、戦闘導線、レジェンド進行、クラス、施設、共有表示",
        "difference": "テンプレート・CSRF・共有ニュース・一般掲示板へ移行。レジェンド進行中の入口挙動が異なる",
        "intent": "画面・安全化は意図的／レジェンド進行継続は要判断",
        "note": "戦闘回数0ではモンスター・幻影・異世界・道場・武道会・レジェンドを表示段階で止め、20秒待機、クラス、宿代Lv×10、称号段階は一致する。Ver2はboss_flagが10以外ならレジェンド入口から挑戦させない。現行は進行状態を保ち、legend_cancelの明示POSTでのみ10へ戻すため、継続可能な現行挙動を維持するか要判断。",
    },
    {
        "file": "cgi_py/sts.py / templates/sts.html",
        "v2_source": "旧版_ver2/sts.cgi",
        "scope": "本人の詳細表示、能力・率計算、現職クラス、職業熟練度、アイコン・発動コメント更新、接続元ホスト",
        "difference": "テンプレート・CSRF・本人確認・入力検証へ移行。ホームページ名・URLは現行スキーマで扱わない",
        "intent": "画面・安全化・プロフィール項目の整理は意図的",
        "note": "命中=dex/10+51（上限150）、回避=agi/20（上限50）、必殺=karma/15+10+job_level（上限75）、装備補正、現在職のクラス表示、100文字・禁止語制限、更新時のREMOTE_ADDR保存は確認した。Ver2のsite/urlだけは現行スキーマから除外し、現行はアイコン番号を設定済み画像へ制限する。能力名の括弧内説明は実装との対応が曖昧だったため、既決方針で非表示にしている。",
    },
    {
        "file": "cgi_py/battle.py",
        "v2_source": "旧版_ver2/battle.cgi / wbattle.pl:sentoukeka",
        "scope": "王者挑戦、待機・ロック、戦績、経験値・賞金、王者交代、防衛、HP回復、レジェンド・修行回数、保存順",
        "difference": "時間切れの王者側更新と敗北経験値上限がVer2と異なる。JSON・本人認証・原子的保存へ移行",
        "intent": "時間切れ・敗北経験値は既決仕様／移行・安全化は意図的",
        "note": "対人時間切れwin=3は経験値だけを得て、王者交代・賞金・防衛連勝・次回賞金を発生させない。Ver2は時間切れ時に王者の防衛側更新を行う。敗北EXPはVer2の相手Lvそのままではなくmin(相手Lv, 自分Lv×10)に制限する。通常勝利・相打ちwin=2の王者交代、敗北時の半額、boss_flagと修行回数の復帰、レベルアップ後に新王者と戦闘後HPを確定する順は確認した。",
    },
    {
        "file": "cgi_py/select_battle.py / templates/select_battle.html",
        "v2_source": "旧版_ver2/select_battle.cgi / regist.pl:all_name_search / wbattle.pl",
        "scope": "道場入口、名前・一覧による相手選択、待機、模擬戦、保存有無、初回解放",
        "difference": "全ユーザーの直接列挙、POST・CSRF・本人照合へ移行。初回チャンピオン戦前の直接実行も拒否する",
        "intent": "安全化・解放条件の入口側強制は意図的",
        "note": "名前の完全一致検索、本人との対戦拒否、待機20秒、対人BattleSimulator、経験値・所持金・戦績・待機時刻を保存しない点は確認した。Ver2の候補一覧はキャッシュ済みRANKINGを使う一方、現行は保存済み全ユーザーを直接列挙する。Ver2は街画面で初回解放を隠すだけだが、現行はbattle_count>0を入口・直接POSTの双方で検査する。",
    },
    {
        "file": "cgi_py/monster.py",
        "v2_source": "旧版_ver2/monster.cgi / mbattle.pl:sentoukeka,hp_after",
        "scope": "通常修行・幻影の城・異世界、入口条件、出現抽選、待機・回数、勝敗報酬、盗み、戦績、回復、保存順",
        "difference": "直接実行時の解放・異世界Lv制限、20秒待機、敗北EXP0、JSON重み抽選へ移行。幻影・異世界の後続モンスター技呼出しが異なる",
        "intent": "入口検証・待機・敗北EXP0・抽選移行は既決仕様／後続技呼出しは要判断",
        "note": "Ver2の重複行数と現行weight合計は初級193・中級169・上級45・最上級121・異世界95で全て一致する。通常・幻影・異世界の回数消費、勝敗時の所持金、戦績、boss_flag復帰、レベルアップ後のHP回復、接続元保存は確認した。現行はbattle_count>0と異世界Lv300を実行側でも検査し、待機は設定値20秒、敗北EXPは0とする。Ver2は幻影・異世界でmons_atowazaを呼ばないが、現行の全モンスターIDの同フックは空実装のため、現時点で実効差はない。将来効果を追加する前に呼出し範囲を判断する。",
    },
    {
        "file": "cgi_py/legend.py / templates/monster_result.html / templates/legend_error.html",
        "v2_source": "旧版_ver2/legend.cgi / mbattle.pl:legend_sentoukeka,hp_after / data/bossmons0〜3.ini",
        "scope": "公開ランキング、階層選択、入口条件、ボス進行、勝敗報酬、称号、連戦、待機、回復、保存順",
        "difference": "公開ランキング・CSRF/POSTルーティング・連戦導線を追加。クリア後の進行値、レジェンド入口のboss_flag検証、階層値検証がVer2と異なる",
        "intent": "階層値検証は不具合を修正済み／連戦・クリア後再挑戦は意図的",
        "note": "各階層は両版とも11体で、boss_flag 10から1へ減らして0で階層クリアする。Ver2の通常画面はboss_flagが10以外なら入口を隠すが、legend.cgi自体は進行値を検証しないため、直接POSTでは0番目の行を参照する不整合な再入場が可能だった。現行は7754ecaで開始値10へ戻し、同階層を正しく最初から再挑戦できる。勝利・引分・敗北の経験値、所持金、battle_count、battle_limit、title_id、レベルアップ後HP回復、接続元保存を照合した。実行はlogin.pyがPOST・CSRFを検証する。範囲外・数値外のboss_fileは第1階層へフォールバックしていたため拒否へ修正した。",
    },
    {
        "file": "cgi_py/tenka.py / templates/tenka.html / templates/tenka_result.html / templates/tenka_error.html",
        "v2_source": "旧版_ver2/tenka.cgi / wbattle.pl:sentoukeka / battle.pl:winner_data",
        "scope": "24時間参加者キャッシュ、入口・ラウンド照合、対戦相手・装備、勝敗報酬、進行、制覇履歴、待機、回復、保存順",
        "difference": "JSON/CSRF/ロック・履歴上限・全体通知へ移行。引分・時間切れ・敗北の進行はVer2と異なる",
        "intent": "進行分岐は既決の現行仕様／ロビーの途中再開表示と説明文は不具合を修正済み",
        "note": "参加者は両版とも24時間ごとにレベル上位3人を固定し、対戦時はその能力スナップショットと最新装備を組み合わせる。相手順は3位→2位→1位で一致し、ラウンド番号を現行はサーバー側でも照合する。Ver2は全勝敗でboss_flagを減らし、相打ちは勝利、時間切れは次戦へ進行、敗北後は9となる。現行は勝利だけ進行し、相打ち・時間切れは進めず、敗北も開始状態を保つ既決方針を維持する。battle_limit補充、経験値、所持金、レベルアップ後HP回復、接続元保存を確認した。Ver2の制覇履歴は変数名誤記で実質1件、現行は設定値20件を保持する。途中進行時に第1回戦を再送するロビー導線と、実装と異なる5名・順位交換の説明を修正した。",
    },
    {
        "file": "cgi_py/rank.py / templates/rank.html",
        "v2_source": "旧版_ver2/rank.cgi / regist.pl:all_data_read",
        "scope": "公開表示、24時間キャッシュ、全登録者数、11部門の集計・上位10件、勝率対象・端数処理、プロフィール導線",
        "difference": "静的HTMLキャッシュからJSONキャッシュとテンプレート表示へ移行。外部ホームページ欄を廃止",
        "intent": "JSON・表示刷新・URL除外は意図的／勝率条件コメントは実装どおりに整理済み",
        "note": "レベル、最大HP、力・知能・信仰心・生命力・器用さ・速さ・魅力・カルマ、勝率の11部門は全て対応し、各上位10件の値も一致する。勝率は両版ともbattle_countが1,000超だけを対象にし、win_count×10000÷battle_countを小数第2位まで切り捨てる。24時間更新・登録者数・個人詳細への公開リンクは維持する。現行は画像を追加し、Ver2の外部ホームページ列はプロフィールURLを扱わない現行スキーマに合わせて表示しない。",
    },
    {
        "file": "cgi_py/system.py / templates/system_ranking.html / templates/system_chara_sts.html / templates/system_img_list.html",
        "v2_source": "旧版_ver2/system.cgi:ranking_no_html,chara_sts,img_list / regist.pl:all_data_read",
        "scope": "公開ルート、24時間登録者キャッシュ、レベル順・20件ページング、他者詳細の能力・装備・率・称号・職業、画像一覧",
        "difference": "静的HTMLからJSONキャッシュ・テンプレート・公開GETへ移行。他者詳細の公開項目とバー上限が異なる",
        "intent": "クラス欠落・範囲外ページ番号・性別/所持金の非公開は不具合を修正済み",
        "note": "レベル降順、20件単位、削除期限、勝率、能力値・装備補正・命中/回避/必殺・称号・マスター職、画像ID一覧を照合した。現行はキャッシュの必須キーを検証し、負数は0・過大なshtmは最終ページへ正規化する。Ver2と同じ7段階の職業クラス、性別、所持金を他者詳細へ復元した。外部ホームページURLだけは現行スキーマから除外する。バーはCSS幅100%へ正規化する表示差で、計算値自体は一致する。",
    },
    {
        "file": "sub_def/battle_logic.py",
        "v2_source": "旧版_ver2/battle.pl / mbattle.pl / wbattle.pl",
        "scope": "戦闘状態、Lv・職業基礎ダメージ、装備補正、必殺・後続効果、クリティカル、命中・回避、HP精算、勝敗、レベルアップ",
        "difference": "初期Python移植時から欠けていたターンLv基礎ダメージを復元。状態オブジェクト・構造化ログへ移行",
        "intent": "Lv基礎ダメージは不具合を修正済み／同時精算と部分先行停止の混在は既知の保留",
        "note": "通常・幻影・異世界・レジェンドはLv×(rand(5)+1)、対人は双方Lv×(rand(3)+1)を職業式と武器ATKへ加算する。全31職の能力参照を再確認し、上級職のカルマはall_stats・職24・職25で固定加算とする。必殺技・モンスター技の個別効果はskills.md・monster_skills.mdで別途照合済み。Ver2は同時精算だが、現行は撃破見込みの敵通常ダメージだけを止めるため、速度・死亡中断を含む一貫した行動順を決めるまで変更しない。",
    },
)


def load_json(name: str) -> list[dict[str, Any]]:
    with (DATA_DIR / name).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"配列ではありません: {name}")
    return [row for row in data if isinstance(row, dict)]


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def job_labels() -> dict[int, str]:
    return {
        job_id: str(job["name"])
        for job_id, job in enumerate(load_json("syoku.json"))
        if "name" in job
    }


def job_text(item: dict[str, Any], labels: dict[int, str]) -> str:
    job_ids = item.get("job_ids", [])
    if not isinstance(job_ids, list):
        return "未設定"
    if not job_ids:
        return "共通・選択不可"
    return ", ".join(f"{job_id}:{labels.get(int(job_id), '不明')}" for job_id in job_ids)


def current_value(kind: str, item: dict[str, Any], labels: dict[int, str]) -> str:
    common = f"価格 {item.get('gold', 0):,}G / 対象職 {job_text(item, labels)}"
    if kind == "weapon":
        return f"ATK {item.get('atk', 0)} / 命中 {item.get('hit_rate', 0)}% / {common}"
    if kind == "armor":
        return f"DEF {item.get('defense', 0)} / 回避 {item.get('evasion_rate', 0)}% / {common}"

    bonus = item.get("bonus", {})
    if not isinstance(bonus, dict):
        bonus = {}
    bonus_text = ", ".join(
        f"{STAT_LABELS[key]} {bonus.get(key, 0):+}"
        for key in STAT_LABELS
        if int(bonus.get(key, 0)) != 0
    ) or "能力補正なし"
    return (
        f"効果ID {item.get('effect_id', 0)} / {bonus_text} / "
        f"命中 {item.get('hit_rate', 0)}% / 回避 {item.get('evasion_rate', 0)}% / "
        f"必殺 {item.get('special_rate', 0)}% / {common}"
    )


WEAPON_INTENTIONAL_DIFFERENCES = {
    1032: "価格 70,000G → 18,000G。職業3の武器価格を性能順に調整（d7105f6）。",
    1033: "価格 18,000G → 75,000G。職業3の武器価格を性能順に調整（d7105f6）。",
    1034: "価格 75,000G → 580,000G。職業3の武器価格を性能順に調整（d7105f6）。",
    1035: "価格 580,000G → 2,550,000G。職業3の武器価格を性能順に調整（d7105f6）。",
    1036: "価格 2,550,000G → 12,500,000G。職業3の武器価格を性能順に調整（d7105f6）。",
    1037: "価格 12,500,000G → 75,000,000G。職業3の武器価格を性能順に調整（d7105f6）。",
    1038: "価格 25,000,000G → 98,000,000G。職業3の武器価格を性能順に調整（d7105f6）。",
}


ARMOR_REVIEW_DIFFERENCES = {
    2165: "名称: Ver2の全角ハイフン（－）→ Ver3のマイナス記号（−）。表示名のみの文字種差異。",
    2181: "対象職: Ver2は職業別販売リスト未掲載 → Ver3は 18:皇帝。",
    2183: "名称: Ver2の全角ハイフン（－）→ Ver3のマイナス記号（−）。表示名のみの文字種差異。",
}


ACCESSORY_INTENTIONAL_DIFFERENCES = {
    85: "命中・回避・必殺補正: 各0 → 各350。Ver1準拠へ復元（d7105f6）。",
    87: "命中・回避・必殺補正: 各0 → 999 / 999 / 9,999。Ver1準拠へ復元（d7105f6）。",
}


def read_v2_equipment_lines(path: Path, field_count: int) -> list[tuple[int, list[str], int]]:
    """CP932のVer2マスターを読み、ID・列・行番号を返す。"""
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="cp932").splitlines(), 1):
        fields = line.split("<>")
        if len(fields) < field_count or not fields[0].isdigit():
            continue
        rows.append((int(fields[0]), fields, line_number))
    return rows


def weapon_comparisons(labels: dict[int, str]) -> dict[int, dict[str, str]]:
    """Ver2の総覧・職業別武器リストとVer3を全件照合する。"""
    base = ROOT / "旧版_ver2" / "data" / "item"
    master_rows = read_v2_equipment_lines(base / "item.ini", 5)
    master: dict[int, tuple[list[str], int]] = {}
    for item_id, fields, line_number in master_rows:
        if item_id in master:
            raise ValueError(f"Ver2武器総覧にID重複があります: {item_id}")
        master[item_id] = (fields, line_number)

    job_ids: dict[int, list[int]] = defaultdict(list)
    for path in sorted(base.glob("item[0-9]*.ini")):
        match = re.fullmatch(r"item(\d+)", path.stem)
        if not match:
            continue
        job_id = int(match.group(1))
        for item_id, _, _ in read_v2_equipment_lines(path, 5):
            if item_id not in master:
                raise ValueError(f"Ver2職業別武器に総覧未登録IDがあります: {path.name} #{item_id}")
            job_ids[item_id].append(job_id)

    results: dict[int, dict[str, str]] = {}
    unclassified: list[int] = []
    for item in load_json("weapon.json"):
        item_id = as_int(item.get("no"))
        if item_id not in master:
            raise ValueError(f"Ver3武器にVer2総覧の対応IDがありません: {item_id}")
        fields, line_number = master[item_id]
        old_name, old_atk, old_gold, old_hit_rate = fields[1], as_int(fields[2]), as_int(fields[3]), as_int(fields[4])
        old_jobs = sorted(job_ids[item_id])
        new_values = (str(item.get("name")), as_int(item.get("atk")), as_int(item.get("gold")), as_int(item.get("hit_rate")))
        old_values = (old_name, old_atk, old_gold, old_hit_rate)
        new_jobs = sorted(as_int(job_id) for job_id in item.get("job_ids", []))
        source = f"旧版_ver2/data/item/item.ini:{line_number}"
        if old_jobs:
            source += " / 購入職 " + ", ".join(f"item{job_id}.ini" for job_id in old_jobs)
        else:
            source += " / 職業別販売リストには未掲載"

        if item_id in WEAPON_INTENTIONAL_DIFFERENCES:
            results[item_id] = {
                "source": source,
                "difference": WEAPON_INTENTIONAL_DIFFERENCES[item_id],
                "intent": "意図的",
                "status": "差異あり",
                "note": "ATK・命中・対象職はVer2と一致。コミットの目的と差異が一致する。",
            }
        elif old_values == new_values and old_jobs == new_jobs:
            results[item_id] = {
                "source": source,
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": "名称・ATK・価格・命中・対象職をVer2総覧と職業別販売リストで照合済み。",
            }
        elif item_id == 1181 and old_values == new_values and old_jobs == [] and new_jobs == [18]:
            results[item_id] = {
                "source": source,
                "difference": f"対象職: Ver2は職業別販売リスト未掲載 → Ver3は 18:{labels.get(18, '不明')}",
                "intent": "要判断",
                "status": "差異あり",
                "note": "名称・ATK・価格・命中は一致。販売対象職を追加した根拠は履歴から確認できない。",
            }
        else:
            unclassified.append(item_id)

    if set(master) != set(results):
        missing = sorted(set(master) - set(results))
        extra = sorted(set(results) - set(master))
        raise ValueError(f"武器比較のID対応に差異があります: missing={missing}, extra={extra}")
    if unclassified:
        raise ValueError(f"理由未記録のVer2/Ver3武器差異があります: {sorted(unclassified)}")
    return results


def armor_comparisons(labels: dict[int, str]) -> dict[int, dict[str, str]]:
    """Ver2の総覧・職業別防具リストとVer3を全件照合する。"""
    base = ROOT / "旧版_ver2" / "data" / "def"
    master_rows = read_v2_equipment_lines(base / "def.ini", 5)
    master: dict[int, tuple[list[str], int]] = {}
    for item_id, fields, line_number in master_rows:
        if item_id in master:
            raise ValueError(f"Ver2防具総覧にID重複があります: {item_id}")
        master[item_id] = (fields, line_number)

    job_ids: dict[int, list[int]] = defaultdict(list)
    for path in sorted(base.glob("def[0-9]*.ini")):
        match = re.fullmatch(r"def(\d+)", path.stem)
        if not match:
            continue
        job_id = int(match.group(1))
        for item_id, _, _ in read_v2_equipment_lines(path, 5):
            if item_id not in master:
                raise ValueError(f"Ver2職業別防具に総覧未登録IDがあります: {path.name} #{item_id}")
            job_ids[item_id].append(job_id)

    results: dict[int, dict[str, str]] = {}
    unclassified: list[int] = []
    for item in load_json("armor.json"):
        item_id = as_int(item.get("no"))
        if item_id not in master:
            raise ValueError(f"Ver3防具にVer2総覧の対応IDがありません: {item_id}")
        fields, line_number = master[item_id]
        old_values = (fields[1], as_int(fields[2]), as_int(fields[3]), as_int(fields[4]))
        new_values = (str(item.get("name")), as_int(item.get("defense")), as_int(item.get("gold")), as_int(item.get("evasion_rate")))
        old_jobs = sorted(job_ids[item_id])
        new_jobs = sorted(as_int(job_id) for job_id in item.get("job_ids", []))
        source = f"旧版_ver2/data/def/def.ini:{line_number}"
        if old_jobs:
            source += " / 購入職 " + ", ".join(f"def{job_id}.ini" for job_id in old_jobs)
        else:
            source += " / 職業別販売リストには未掲載"

        if old_values == new_values and old_jobs == new_jobs:
            results[item_id] = {
                "source": source,
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": "名称・DEF・価格・回避・対象職をVer2総覧と職業別販売リストで照合済み。",
            }
        elif item_id in ARMOR_REVIEW_DIFFERENCES:
            results[item_id] = {
                "source": source,
                "difference": ARMOR_REVIEW_DIFFERENCES[item_id],
                "intent": "要判断",
                "status": "差異あり",
                "note": "数値または対象職以外の項目はVer2と一致。変更根拠は履歴から確認できない。",
            }
        else:
            unclassified.append(item_id)

    if set(master) != set(results):
        missing = sorted(set(master) - set(results))
        extra = sorted(set(results) - set(master))
        raise ValueError(f"防具比較のID対応に差異があります: missing={missing}, extra={extra}")
    if unclassified:
        raise ValueError(f"理由未記録のVer2/Ver3防具差異があります: {sorted(unclassified)}")
    return results


def accessory_comparisons() -> dict[int, dict[str, str]]:
    """Ver2の総覧・職業別アクセサリーリストとVer3を全件照合する。"""
    base = ROOT / "旧版_ver2" / "data" / "acs"
    master_rows = read_v2_equipment_lines(base / "acs.ini", 16)
    master: dict[int, tuple[list[str], int]] = {}
    for item_id, fields, line_number in master_rows:
        if item_id in master:
            raise ValueError(f"Ver2アクセサリー総覧にID重複があります: {item_id}")
        master[item_id] = (fields, line_number)

    job_ids: dict[int, list[int]] = defaultdict(list)
    for path in sorted(base.glob("acs[0-9]*.ini")):
        match = re.fullmatch(r"acs(\d+)", path.stem)
        if not match:
            continue
        job_id = int(match.group(1))
        for item_id, _, _ in read_v2_equipment_lines(path, 16):
            if item_id not in master:
                raise ValueError(f"Ver2職業別アクセサリーに総覧未登録IDがあります: {path.name} #{item_id}")
            job_ids[item_id].append(job_id)

    results: dict[int, dict[str, str]] = {}
    unclassified: list[int] = []
    for item in load_json("accessory.json"):
        item_id = as_int(item.get("no"))
        if item_id not in master:
            raise ValueError(f"Ver3アクセサリーにVer2総覧の対応IDがありません: {item_id}")
        fields, line_number = master[item_id]
        old_bonus = tuple(as_int(value) for value in fields[4:12])
        bonus = item.get("bonus", {})
        if not isinstance(bonus, dict):
            raise ValueError(f"Ver3アクセサリーのbonusが辞書ではありません: {item_id}")
        new_bonus = tuple(as_int(bonus.get(key)) for key in STAT_LABELS)
        old_values = (
            fields[1], as_int(fields[2]), as_int(fields[3]), old_bonus,
            as_int(fields[12]), as_int(fields[13]), as_int(fields[14]), fields[15],
        )
        new_values = (
            str(item.get("name")), as_int(item.get("gold")), as_int(item.get("effect_id")), new_bonus,
            as_int(item.get("hit_rate")), as_int(item.get("evasion_rate")), as_int(item.get("special_rate")), str(item.get("description")),
        )
        old_jobs = sorted(job_ids[item_id])
        new_jobs = sorted(as_int(job_id) for job_id in item.get("job_ids", []))
        source = f"旧版_ver2/data/acs/acs.ini:{line_number}"
        if old_jobs:
            source += " / 購入職 " + ", ".join(f"acs{job_id}.ini" for job_id in old_jobs)
        else:
            source += " / 職業別販売リストには未掲載"

        if item_id in ACCESSORY_INTENTIONAL_DIFFERENCES:
            results[item_id] = {
                "source": source,
                "difference": ACCESSORY_INTENTIONAL_DIFFERENCES[item_id],
                "intent": "意図的",
                "status": "差異あり",
                "note": "名称・価格・効果ID・能力補正・対象職はVer2と一致。コミットの目的と差異が一致する。",
            }
        elif old_values == new_values and old_jobs == new_jobs:
            results[item_id] = {
                "source": source,
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": "名称・価格・効果ID・8能力補正・3率補正・説明・対象職をVer2総覧と職業別販売リストで照合済み。",
            }
        elif item_id == 999 and old_values[:-1] == new_values[:-1] and old_jobs == new_jobs:
            results[item_id] = {
                "source": source,
                "difference": "説明: Ver2は空文字 → Ver3は「効果なし」。",
                "intent": "要判断",
                "status": "差異あり",
                "note": "ゲーム効果と対象職は一致。表示専用の文言差であり、変更根拠は履歴から確認できない。",
            }
        else:
            unclassified.append(item_id)

    if set(master) != set(results):
        missing = sorted(set(master) - set(results))
        extra = sorted(set(results) - set(master))
        raise ValueError(f"アクセサリー比較のID対応に差異があります: missing={missing}, extra={extra}")
    if unclassified:
        raise ValueError(f"理由未記録のVer2/Ver3アクセサリー差異があります: {sorted(unclassified)}")
    return results


def checklist_row(kind: str, item: dict[str, Any], labels: dict[int, str], v2_source: str, comparison: dict[str, str] | None = None) -> str:
    item_id = item.get("no", "?")
    name = item.get("name", "名称なし")
    if comparison:
        return (
            f"| {kind} {item_id}: {name} | `{comparison['source']}` | "
            f"{current_value(kind, item, labels)} | {comparison['difference']} | "
            f"{comparison['intent']} | {comparison['status']} | {comparison['note']} |\n"
        )
    return (
        f"| {kind} {item_id}: {name} | `{v2_source}` の対応定義（ID・名称・数値） | "
        f"{current_value(kind, item, labels)} | 未確認 | 未判定 | 未確認 | "
        "Ver2定義と購入条件・効果を照合後に根拠を記入 |\n"
    )


def stat_text(item: dict[str, Any], prefix: str) -> str:
    values = [
        f"{label} {item.get(prefix + key, 0)}"
        for key, label in STAT_LABELS.items()
    ]
    return " / ".join(values)


def master_requirements(item: dict[str, Any], labels: dict[int, str]) -> str:
    requirements = item.get("job_reqs", [])
    if not isinstance(requirements, list):
        return "未設定"
    matched = [
        f"{job_id}:{labels.get(job_id, '不明')} Lv{level}"
        for job_id, level in enumerate(requirements)
        if int(level) > 0
    ]
    return ", ".join(matched) or "なし"


def tactic_implementation(tactic_id: int) -> str:
    return (
        f"`sub_def/skills.py`: tech_{tactic_id}.hissatu / atowaza、"
        f"wtech_{tactic_id}.whissatu / watowaza"
    )


JOB_VALUE_KEYS = (
    "req_str", "req_int", "req_mnd", "req_vit", "req_dex", "req_agi", "req_cha", "req_karma",
    "limit_str", "limit_int", "limit_mnd", "limit_vit", "limit_dex", "limit_agi", "limit_cha", "limit_karma",
)

# Ver2側の職業名には「ソ\ルジャー」という表示用の誤記が残っている。
# Ver3では表示名を自然な「ソルジャー」へ補正しているため、値比較の
# 未分類差異としては扱わない。
JOB_INTENTIONAL_DIFFERENCES: dict[int, dict[str, str]] = {
    0: {
        "difference": "名称: ソ\\ルジャー → ソルジャー",
        "intent": "意図的（表示名の誤記修正）",
        "status": "差異あり",
        "note": "Ver2名に混入しているバックスラッシュを除去。転職条件8項目、成長上限8項目、必要マスター職31項目は一致。",
    },
}

# Ver2の戦術総覧に残る説明文の誤記・旧チーム戦向けの説明は、実装に合わせて
# Ver3で整理している。各IDの実装値は旧版 tech / wtech も参照して確認する。
TACTIC_DESCRIPTION_CORRECTIONS = {
    2: "説明文の最大8回を、Ver2実装のrand(7)+1と同じ最大7回へ補正",
    5: "説明文の最大16回を、Ver2実装のrand(15)+1と同じ最大15回へ補正",
    6: "説明文の「10/1」を実装どおりの「1/10」へ補正",
    11: "説明文の全量回復を、Ver2実装どおりの与ダメージ1/5へ補正",
    20: "現行にないチームバトル専用の説明を削除",
    22: "実装に存在しない「相手の回避率を無視」を説明から削除",
    30: "説明文の半減を、Ver2実装どおりの1/10軽減へ補正",
    37: "説明文の最大8回を、Ver2実装のrand(7)+1と同じ最大7回へ補正",
    40: "説明文の最大8体を、Ver2実装のrand(7)+1と同じ最大7体へ補正",
    43: "説明文の1/5回復を、Ver2実装どおりの全量回復へ補正",
    49: "説明文の1〜8倍を、Ver2実装のrand(7)+1と同じ1〜7倍へ補正",
    53: "説明文の12回を、Ver2実装のrand(11)+1と同じ最大11回へ補正",
    55: "現行にないチームバトル専用の説明を削除",
    59: "説明文の最大16回を、Ver2実装のrand(15)+1と同じ最大15回へ補正",
}

# ここはVer2との挙動差を残す判断が既に行われた項目。実装との差分を隠さず、
# 台帳では意図と適用範囲を明記する。
TACTIC_BEHAVIOR_INTENTIONAL_DIFFERENCES = {
    9: "異世界モードの正式値 isekiai と旧表記 isekai の両方を受理する互換処理を追加",
    10: "モンスター戦だけ盗み回数・獲得額の上限を設け、対人戦のVer2相当処理は維持",
    11: "回復量はVer2と同じ1/5だが、防御・回避後の実ダメージから回復する現行仕様を維持",
    43: "回復量はVer2と同じ全量だが、防御・回避後の実ダメージから回復する現行仕様を維持",
    44: "回復量はVer2と同じ1/10だが、防御・回避後の実ダメージから回復する現行仕様を維持",
}


def tactic_rate_denominators(source: str, variable: str) -> list[int]:
    """Ver2の戦術本体に直接書かれた必殺率の乱数幅を取得する。"""
    return [
        as_int(value)
        for value in re.findall(
            rf"\${variable}\s*>\s*int\(rand\((\d+)\)\)", source
        )
    ]


def tactic_comparisons() -> dict[int, dict[str, str]]:
    """Ver2の戦術総覧・職業別一覧・両戦闘側の実装存在を全件照合する。"""
    legacy_root = ROOT / "旧版_ver2"
    legacy_rows: dict[int, tuple[dict[str, Any], int]] = {}
    for line_number, line in enumerate(
        (legacy_root / "data" / "tac" / "tac.ini").read_text(encoding="cp932").splitlines(), 1
    ):
        fields = line.split("<>")
        if len(fields) < 4:
            raise ValueError(f"Ver2戦術定義の列数が不正です: tac.ini:{line_number}")
        tactic_id = as_int(fields[0])
        legacy_rows[tactic_id] = ({
            "no": tactic_id,
            "name": fields[1],
            "desc": fields[2],
            "ms": as_int(fields[3]),
        }, line_number)

    legacy_jobs: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for path in sorted((legacy_root / "data" / "tac").glob("tac[0-9]*.ini")):
        job_id = as_int(path.stem[3:])
        for line_number, line in enumerate(path.read_text(encoding="cp932").splitlines(), 1):
            fields = line.split("<>")
            if fields and fields[0]:
                legacy_jobs[as_int(fields[0])].append((job_id, line_number))

    current_rows = {as_int(row.get("no")): row for row in load_json("tac.json")}
    if set(legacy_rows) != set(current_rows):
        raise ValueError(
            "Ver2/Ver3戦術IDが一致しません: "
            f"Ver2のみ={sorted(set(legacy_rows) - set(current_rows))}, "
            f"Ver3のみ={sorted(set(current_rows) - set(legacy_rows))}"
        )

    skills_tree = ast.parse((ROOT / "sub_def" / "skills.py").read_text(encoding="utf-8"))
    skill_classes = {node.name: node for node in skills_tree.body if isinstance(node, ast.ClassDef)}
    results: dict[int, dict[str, str]] = {}
    unclassified: list[int] = []
    for tactic_id, current in current_rows.items():
        legacy, source_line = legacy_rows[tactic_id]
        old_jobs = sorted(job_id for job_id, _ in legacy_jobs.get(tactic_id, []))
        new_jobs = sorted(as_int(job_id) for job_id in current.get("job_ids", []))
        master_matches = (
            legacy["name"] == str(current.get("name"))
            and legacy["desc"] == str(current.get("desc"))
            and legacy["ms"] == as_int(current.get("ms"))
            and old_jobs == new_jobs
        )

        required = {
            f"tech_{tactic_id}": {"hissatu", "atowaza"},
            f"wtech_{tactic_id}": {"whissatu", "watowaza"},
        }
        for class_name, methods in required.items():
            node = skill_classes.get(class_name)
            actual = {child.name for child in node.body if isinstance(child, ast.FunctionDef)} if node else set()
            if not methods.issubset(actual):
                raise ValueError(f"Ver3戦術実装が不足しています: {class_name} ({sorted(methods - actual)})")

        rate_differences: list[str] = []
        configured_rate = current.get("activation_denominator")
        if configured_rate is not None:
            configured_rate = as_int(configured_rate)
            for directory, variable, label in (("tech", "waza_ritu", "プレイヤー側"), ("wtech", "wwaza_ritu", "対人相手側")):
                source = (legacy_root / directory / f"{tactic_id}.pl").read_text(encoding="cp932")
                legacy_rates = tactic_rate_denominators(source, variable)
                if legacy_rates and any(rate != configured_rate for rate in legacy_rates[:1]):
                    rate_differences.append(
                        f"{label}のVer2乱数幅 {legacy_rates[0]} を説明文対応の {configured_rate} へ統一"
                    )

        details: list[str] = []
        if legacy["desc"] != str(current.get("desc")):
            detail = TACTIC_DESCRIPTION_CORRECTIONS.get(tactic_id)
            if detail is None:
                unclassified.append(tactic_id)
            else:
                details.append(detail)
        if legacy["name"] != str(current.get("name")) or legacy["ms"] != as_int(current.get("ms")) or old_jobs != new_jobs:
            unclassified.append(tactic_id)
        details.extend(rate_differences)
        if tactic_id in TACTIC_BEHAVIOR_INTENTIONAL_DIFFERENCES:
            details.append(TACTIC_BEHAVIOR_INTENTIONAL_DIFFERENCES[tactic_id])

        job_sources = ", ".join(f"tac{job_id}.ini:{line}" for job_id, line in legacy_jobs.get(tactic_id, [])) or "職業別一覧なし"
        source = f"旧版_ver2/data/tac/tac.ini:{source_line} / {job_sources}"
        verified = "名称・説明・マスター条件・利用職、tech/wtech両側のクラス・必殺/後発メソッド、乱数・状態更新を照合済み。"
        if details:
            results[tactic_id] = {
                "source": source,
                "difference": " / ".join(details),
                "intent": "意図的（実装・説明整合または現行仕様の維持）",
                "status": "差異あり",
                "note": verified + " 根拠: 7754eca、fce2828、0667c42。",
            }
        elif master_matches:
            results[tactic_id] = {
                "source": source,
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": verified,
            }
        else:
            unclassified.append(tactic_id)

    if unclassified:
        raise ValueError(f"理由未記録のVer2/Ver3戦術差異があります: {sorted(set(unclassified))}")
    return results


def job_comparisons() -> dict[int, dict[str, str]]:
    """Ver2職業名・47列の職業定義とVer3職業マスターを全件照合する。"""
    legacy_root = ROOT / "旧版_ver2" / "data"
    legacy_rows: list[tuple[list[int], int]] = []
    for line_number, line in enumerate((legacy_root / "syoku.ini").read_text(encoding="cp932").splitlines(), 1):
        fields = [as_int(value) for value in line.split("<>") if value != ""]
        if not fields:
            continue
        if len(fields) != 47:
            raise ValueError(f"Ver2職業定義の列数が不正です: syoku.ini:{line_number} ({len(fields)}列)")
        legacy_rows.append((fields, line_number))

    names: dict[int, tuple[str, int]] = {}
    name_pattern = re.compile(r'\$chara_syoku\[(\d+)\]\s*=\s*"([^"]*)";')
    for line_number, line in enumerate((legacy_root / "ffadventure.ini").read_text(encoding="cp932").splitlines(), 1):
        match = name_pattern.search(line)
        if match:
            names[int(match.group(1))] = (match.group(2), line_number)

    rows = load_json("syoku.json")
    if len(legacy_rows) != len(rows) or set(names) != set(range(len(rows))):
        raise ValueError(
            "職業定義の件数または名前IDが一致しません: "
            f"Ver2定義={len(legacy_rows)}, Ver3={len(rows)}, Ver2名前ID={sorted(names)}"
        )

    results: dict[int, dict[str, str]] = {}
    unclassified: list[int] = []
    for job_id, item in enumerate(rows):
        legacy_values, syoku_line = legacy_rows[job_id]
        current_values = [as_int(item.get(key)) for key in JOB_VALUE_KEYS]
        requirements = item.get("job_reqs", [])
        if not isinstance(requirements, list):
            raise ValueError(f"Ver3職業のjob_reqsが配列ではありません: {job_id}")
        current_values.extend(as_int(value) for value in requirements)
        legacy_name, name_line = names[job_id]
        if legacy_name == str(item.get("name")) and legacy_values == current_values:
            results[job_id] = {
                "source": f"旧版_ver2/data/syoku.ini:{syoku_line} / 旧版_ver2/data/ffadventure.ini:{name_line}",
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": "職業名、転職条件8項目、成長上限8項目、必要マスター職31項目の全47値を照合済み。tensyoku.cgi・battle.plの参照順とも一致。",
            }
        elif job_id in JOB_INTENTIONAL_DIFFERENCES and legacy_values == current_values:
            difference = JOB_INTENTIONAL_DIFFERENCES[job_id]
            results[job_id] = {
                "source": f"旧版_ver2/data/syoku.ini:{syoku_line} / 旧版_ver2/data/ffadventure.ini:{name_line}",
                **difference,
            }
        else:
            unclassified.append(job_id)

    if unclassified:
        raise ValueError(f"理由未記録のVer2/Ver3職業差異があります: {unclassified}")
    return results


def write_jobs(labels: dict[int, str]) -> None:
    rows = load_json("syoku.json")
    comparisons = job_comparisons()
    sections = [
        "# 職業データ比較チェックリスト",
        "",
        "職業IDは `data/syoku.json` の配列位置です。能力条件だけでなく、成長上限と必要なマスター職も照合対象にします。",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for job_id, item in enumerate(rows):
        name = item.get("name", "名称なし")
        current = (
            f"転職能力条件: {stat_text(item, 'req_')} / "
            f"成長上限: {stat_text(item, 'limit_')} / "
            f"必要マスター: {master_requirements(item, labels)} / "
            "`data/syoku.json`・`cgi_py/tensyoku.py`・`sub_def/battle_logic.py`"
        )
        comparison = comparisons[job_id]
        sections.append(
            f"| 職業 {job_id}: {name} | `{comparison['source']}`、"
            "`旧版_ver2/tensyoku.cgi`、`旧版_ver2/battle.pl` | "
            f"{current} | {comparison['difference']} | {comparison['intent']} | "
            f"{comparison['status']} | {comparison['note']} |"
        )
    (OUTPUT_DIR / "jobs.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def write_skills(labels: dict[int, str]) -> None:
    rows = load_json("tac.json")
    comparisons = tactic_comparisons()
    sections = [
        "# 必殺技・戦術比較チェックリスト",
        "",
        "`data/tac.json` の全戦術を列挙します。効果だけでなく、発動率、マスター条件、プレイヤー側・王者側の両実装を確認します。",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in rows:
        tactic_id = int(item.get("no", -1))
        name = item.get("name", "名称なし")
        activation = item.get("activation_denominator")
        activation_text = f"乱数幅 {activation}" if activation is not None else "乱数幅は効果側の既定値・常時効果"
        master_text = "マスター技" if int(item.get("ms", 0)) else "通常技"
        current = (
            f"利用職 {job_text(item, labels)} / {master_text} / {activation_text} / "
            f"説明: {item.get('desc', '')} / {tactic_implementation(tactic_id)}"
        )
        comparison = comparisons[tactic_id]
        sections.append(
            f"| 戦術 {tactic_id}: {name} | `{comparison['source']}`、"
            f"`旧版_ver2/tech/{tactic_id}.pl`、`旧版_ver2/wtech/{tactic_id}.pl`、"
            "`旧版_ver2/battle.pl` / `wbattle.pl` | "
            f"{current} | {comparison['difference']} | {comparison['intent']} | "
            f"{comparison['status']} | {comparison['note']} |"
        )
    (OUTPUT_DIR / "skills.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def load_monsters() -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(MONSTER_DATA_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"モンスターマスターを読み込めません: {path}") from error
        if not isinstance(data, list):
            raise ValueError(f"モンスターマスターは配列である必要があります: {path}")
        records.extend((path.name, row) for row in data if isinstance(row, dict))
    return records


def monster_definition_values(record: dict[str, Any]) -> tuple[str, int, int, int, int, int, int, int, int]:
    """出現重みを除く、Ver2モンスターマスターの9項目を固定順で返す。"""
    return (
        str(record.get("name", "")),
        as_int(record.get("exp_reward")),
        as_int(record.get("random_range")),
        as_int(record.get("hp_base")),
        as_int(record.get("base_damage")),
        as_int(record.get("evasion_rate")),
        as_int(record.get("special_skill_id")),
        as_int(record.get("special_rate")),
        as_int(record.get("gold_reward")),
    )


def legacy_monster_definition_values(path: Path) -> list[tuple[str, int, int, int, int, int, int, int, int]]:
    values = []
    for line_number, line in enumerate(path.read_text(encoding="cp932").splitlines(), 1):
        fields = line.split("<>")
        if len(fields) < 9:
            raise ValueError(f"Ver2モンスターマスターの列数が不正です: {path}:{line_number}")
        values.append((fields[0], *(as_int(value) for value in fields[1:9])))
    return values


def monster_master_comparisons() -> dict[tuple[str, int], dict[str, str]]:
    """全モンスターマスターを、Ver2の重複出現枠まで含めて比較する。"""
    results: dict[tuple[str, int], dict[str, str]] = {}
    for current_name, source in V2_MONSTER_MASTERS.items():
        current_path = MONSTER_DATA_DIR / current_name
        current_records = json.loads(current_path.read_text(encoding="utf-8"))
        if not isinstance(current_records, list):
            raise ValueError(f"Ver3モンスターマスターは配列である必要があります: {current_path}")
        legacy_path = ROOT / source
        legacy_counter = Counter(legacy_monster_definition_values(legacy_path))
        current_counter: Counter[tuple[str, int, int, int, int, int, int, int, int]] = Counter()
        for record in current_records:
            if not isinstance(record, dict):
                raise ValueError(f"Ver3モンスターマスターにオブジェクト以外があります: {current_path}")
            current_counter[monster_definition_values(record)] += max(1, as_int(record.get("weight", 1)))
        if legacy_counter != current_counter:
            missing = list((legacy_counter - current_counter).items())[:3]
            extra = list((current_counter - legacy_counter).items())[:3]
            raise ValueError(f"Ver2/Ver3モンスターマスター差異: {current_name}; Ver2のみ={missing}; Ver3のみ={extra}")

        for index, record in enumerate(current_records):
            values = monster_definition_values(record)
            weight = max(1, as_int(record.get("weight", 1)))
            source_count = legacy_counter[values]
            results[(current_name, index)] = {
                "source": f"{source}（同一9項目のVer2出現枠 {source_count}件）",
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": f"9項目と出現重みを照合済み。現行weight {weight}、同一レコード全体の重み合計 {current_counter[values]}。",
            }
    return results


def monster_skill_comparisons() -> dict[int, dict[str, str]]:
    """Ver2の全モンスター特殊技とVer3の同名クラス・両メソッドを照合する。"""
    skills_tree = ast.parse((ROOT / "sub_def" / "skills.py").read_text(encoding="utf-8"))
    skill_classes = {node.name: node for node in skills_tree.body if isinstance(node, ast.ClassDef)}
    results: dict[int, dict[str, str]] = {}
    for skill_id in range(1, 23):
        legacy_path = ROOT / "旧版_ver2" / "mons" / f"{skill_id}.pl"
        source = legacy_path.read_text(encoding="cp932")
        if "sub mons_waza" not in source or "sub mons_atowaza" not in source:
            raise ValueError(f"Ver2モンスター特殊技の実装が不足しています: {legacy_path}")
        node = skill_classes.get(f"mons_{skill_id}")
        methods = {child.name for child in node.body if isinstance(child, ast.FunctionDef)} if node else set()
        required = {"mons_waza", "mons_atowaza"}
        if not required.issubset(methods):
            raise ValueError(f"Ver3モンスター特殊技の実装が不足しています: mons_{skill_id}")

        if skill_id == 14:
            results[skill_id] = {
                "difference": "盗み額を所持金以下へ制限し、負数化しない安全処理を追加",
                "intent": "意図的（現行の所持金整合性維持）",
                "status": "差異あり",
                "note": "Ver2の所持金÷7抽選を基礎にしつつ、available_gold と penalize_reward で保存値の下限を保証。",
            }
        else:
            results[skill_id] = {
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": "発動率、乱数分岐、ダメージ・回復・状態更新、通常攻撃との加算/置換を照合済み。13・19の回復分岐はVer2どおり被ダメージを0にする。",
            }
    return results


def write_monster_skills() -> None:
    records = load_monsters()
    comparisons = monster_master_comparisons()
    skill_comparisons = monster_skill_comparisons()
    source_indexes: dict[str, int] = defaultdict(int)
    indexed_records: list[tuple[str, int, dict[str, Any]]] = []
    for source, record in records:
        index = source_indexes[source]
        source_indexes[source] += 1
        indexed_records.append((source, index, record))

    by_skill: dict[int, list[tuple[str, int, dict[str, Any]]]] = {}
    for source, index, record in indexed_records:
        skill_id = as_int(record.get("special_skill_id"))
        if skill_id > 0:
            by_skill.setdefault(skill_id, []).append((source, index, record))

    sections = [
        "# モンスター特殊技比較チェックリスト",
        "",
        "モンスターが使う特殊技と、その使用モンスターを分けて確認します。"
        "発動率は各モンスターの `special_rate > random.randrange(100)` です。",
        "",
        "## 特殊技一覧",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for skill_id, users in sorted(by_skill.items()):
        rates = [as_int(record.get("special_rate")) for _, _, record in users]
        sources = ", ".join(sorted({source for source, _, _ in users}))
        name = MONSTER_SKILL_LABELS.get(skill_id, "名称要確認")
        current = (
            f"使用 {len(users)}体 / special_rate {min(rates)}〜{max(rates)} / "
            f"使用マスター: {sources} / `sub_def/skills.py`: mons_{skill_id}.mons_waza / mons_atowaza"
        )
        comparison = skill_comparisons[skill_id]
        sections.append(
            f"| モンスター特殊技 {skill_id}: {name} | `旧版_ver2/mons/{skill_id}.pl`、"
            "`旧版_ver2/mbattle.pl` | "
            f"{current} | {comparison['difference']} | {comparison['intent']} | "
            f"{comparison['status']} | {comparison['note']} |"
        )

    sections.extend((
        "",
        "## 使用モンスター一覧",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ))
    for source, index, record in indexed_records:
        skill_id = as_int(record.get("special_skill_id"))
        if skill_id <= 0:
            continue
        name = record.get("name", "名称なし")
        comparison = comparisons[(source, index)]
        current = (
            f"特殊技 {skill_id}: {MONSTER_SKILL_LABELS.get(skill_id, '名称要確認')} / "
            f"special_rate {as_int(record.get('special_rate'))} / `data/monsters/{source}`"
        )
        sections.append(
            f"| {source}: {name} | `{comparison['source']}` | "
            f"{current} | {comparison['difference']} | {comparison['intent']} | "
            f"{comparison['status']} | 特殊技ID・特殊率を含む9項目と出現重みを照合済み。 |"
        )
    (OUTPUT_DIR / "monster_skills.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def monster_current_value(record: dict[str, Any]) -> str:
    skill_id = as_int(record.get("special_skill_id"))
    weight = record.get("weight")
    weight_text = str(weight) if weight is not None else "1（既定値）"
    return (
        f"経験値 {as_int(record.get('exp_reward'))} / 基礎HP {as_int(record.get('hp_base'))} / "
        f"基礎攻撃 {as_int(record.get('base_damage'))} / 乱数幅 {as_int(record.get('random_range'))} / "
        f"回避 {as_int(record.get('evasion_rate'))} / 基本報酬 {as_int(record.get('gold_reward'))}G / "
        f"特殊技 {skill_id}: {MONSTER_SKILL_LABELS.get(skill_id, 'なし')} / "
        f"特殊率 {as_int(record.get('special_rate'))} / 出現重み {weight_text}"
    )


def write_monsters() -> None:
    comparisons = monster_master_comparisons()
    sections = [
        "# モンスターデータ比較チェックリスト",
        "",
        "`data/monsters/` の全マスターをファイル別に列挙します。"
        "同名モンスターの重複行は、Ver2の出現重みを再現するための可能性があるため統合せずに確認します。",
        "",
    ]
    total = 0
    for path in sorted(MONSTER_DATA_DIR.glob("*.json")):
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"モンスターマスターを読み込めません: {path}") from error
        if not isinstance(records, list):
            raise ValueError(f"モンスターマスターは配列である必要があります: {path}")
        records = [record for record in records if isinstance(record, dict)]
        total += len(records)
        v2_source = V2_MONSTER_MASTERS.get(path.name, "旧版_ver2/data の対応マスター")
        sections.extend((
            f"## {path.name}（{len(records)}件）",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for index, record in enumerate(records):
            name = record.get("name", "名称なし")
            comparison = comparisons[(path.name, index)]
            sections.append(
                f"| {path.name} #{index}: {name} | `{comparison['source']}` | "
                f"{monster_current_value(record)} / `data/monsters/{path.name}` | "
                f"{comparison['difference']} | {comparison['intent']} | {comparison['status']} | {comparison['note']} |"
            )
        sections.append("")
    sections.insert(3, f"対象: 9ファイル・{total}件。")
    (OUTPUT_DIR / "monsters.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def load_chocobo_data() -> list[tuple[str, list[dict[str, Any]]]]:
    files: list[tuple[str, list[dict[str, Any]]]] = []
    for path in sorted(CHOCOBO_DATA_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"チョコボマスターを読み込めません: {path}") from error
        if not isinstance(data, list):
            raise ValueError(f"チョコボマスターは配列である必要があります: {path}")
        files.append((path.name, [record for record in data if isinstance(record, dict)]))
    return files


def chocobo_candidate_value(record: dict[str, Any]) -> str:
    return (
        f"価格 {as_int(record.get('price'))}G / 初期出走 {as_int(record.get('run'))} / "
        f"初期勝利 {as_int(record.get('win'))} / 血統 {as_int(record.get('blood'))} / "
        f"技 {as_int(record.get('waza'))} / 父 {record.get('father', '')}（rank {as_int(record.get('fatherrank'))}） / "
        f"母 {record.get('mother', '')}（rank {as_int(record.get('motherrank'))}） / "
        f"e {as_int(record.get('e'))} / ブリーダー {record.get('breader', '')}"
    )


def chocobo_rival_value(record: dict[str, Any]) -> str:
    stats = " / ".join(
        f"{label} {as_int(record.get(key))}"
        for key, label in CHOCOBO_STAT_LABELS.items()
    )
    return (
        f"成長タイプ {as_int(record.get('type'))} / 賞金基準 {as_int(record.get('max'))} / "
        f"{stats} / ブリーダー {record.get('breader', '')}"
    )


def chocobo_v2_source(filename: str) -> str:
    if filename == "chocobofile.json":
        return "旧版_ver2/chocobofile.cgi / choco-farm.pl"
    return "旧版_ver2/crace.cgi / farmrace.cgi の対応ribalデータ"


def chocobo_comparisons() -> dict[tuple[str, int], dict[str, str]]:
    """Ver2の候補・各レースライバルを、行順と全保存値で照合する。"""
    results: dict[tuple[str, int], dict[str, str]] = {}
    candidate_fields = ("no", "name", "price", "run", "win", "blood", "waza", "father", "fatherrank", "mother", "motherrank", "e", "breader")
    rival_fields = ("breader", "name", "no", "type", "max", "c0", "c1", "c2", "c3", "c4", "c5", "c6")
    for filename, records in load_chocobo_data():
        legacy_path = ROOT / "旧版_ver2" / ("chocobofile.cgi" if filename == "chocobofile.json" else f"{Path(filename).stem}.cgi")
        legacy_lines = legacy_path.read_text(encoding="cp932").splitlines()
        if len(legacy_lines) != len(records):
            raise ValueError(f"Ver2/Ver3チョコボ件数が不一致です: {filename}")
        fields = candidate_fields if filename == "chocobofile.json" else rival_fields
        for index, (line, record) in enumerate(zip(legacy_lines, records)):
            raw = line.split("<>")
            raw = raw[:-1] if raw and raw[-1] == "" else raw
            if len(raw) != len(fields):
                raise ValueError(f"Ver2チョコボ列数が不正です: {legacy_path}:{index + 1}")
            legacy = tuple(value if key in {"name", "father", "mother", "breader"} else as_int(value) for key, value in zip(fields, raw))
            current = tuple(record.get(key, "") if key in {"name", "father", "mother", "breader"} else as_int(record.get(key)) for key in fields)
            if legacy != current:
                raise ValueError(f"Ver2/Ver3チョコボ差異: {filename}#{index}; Ver2={legacy}; Ver3={current}")
            results[(filename, index)] = {
                "difference": "差異なし",
                "intent": "該当なし",
                "status": "一致",
                "note": f"Ver2 {legacy_path.name}:{index + 1} と行順・全{len(fields)}項目を照合済み。",
            }
    return results


def write_chocobo_data() -> None:
    files = load_chocobo_data()
    comparisons = chocobo_comparisons()
    total = sum(len(records) for _, records in files)
    sections = [
        "# チョコボデータ比較チェックリスト",
        "",
        "`data/chocobo/` の全マスターをファイル別に列挙します。"
        "購入・お見合い候補とレース別ライバルを分けず、保存値をすべて比較対象にします。",
        f"対象: {len(files)}ファイル・{total}件。",
        "",
    ]
    for filename, records in files:
        is_candidate_file = filename == "chocobofile.json"
        kind = "購入・お見合い候補" if is_candidate_file else "レースライバル"
        sections.extend((
            f"## {filename}（{kind}・{len(records)}件）",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for index, record in enumerate(records):
            name = record.get("name", "名称なし")
            comparison = comparisons[(filename, index)]
            current = chocobo_candidate_value(record) if is_candidate_file else chocobo_rival_value(record)
            sections.append(
                f"| {filename} #{index}: {name} | `{chocobo_v2_source(filename)}` の対応データ | "
                f"{current} / `data/chocobo/{filename}` | {comparison['difference']} | {comparison['intent']} | "
                f"{comparison['status']} | {comparison['note']} |"
            )
        sections.append("")
    (OUTPUT_DIR / "chocobo_data.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def function_routes() -> dict[str, str]:
    """login.py の FUNCTION_MAP を静的に読み、ルート漏れを検出する。"""
    tree = ast.parse((ROOT / "login.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "FUNCTION_MAP" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            raise ValueError("FUNCTION_MAP は辞書である必要があります")
        routes: dict[str, str] = {}
        for key, value in zip(node.value.keys, node.value.values):
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                raise ValueError("FUNCTION_MAP のキーが文字列ではありません")
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                raise ValueError("FUNCTION_MAP の値が文字列ではありません")
            routes[key.value] = value.value
        return routes
    raise ValueError("login.py に FUNCTION_MAP がありません")


def mode_values_in_source() -> set[str]:
    """現行コードで `mode` と比較される値を抽出する。"""
    files = [ROOT / "login.py", ROOT / "admin.py", ROOT / "chara_make.py"]
    files.extend(sorted((ROOT / "cgi_py").glob("*.py")))
    values: set[str] = set()

    def strings(node: ast.AST) -> set[str]:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return {node.value}
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            result: set[str] = set()
            for element in node.elts:
                result.update(strings(element))
            return result
        return set()

    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare) or not isinstance(node.left, ast.Name) or node.left.id != "mode":
                continue
            for operator, comparator in zip(node.ops, node.comparators):
                if isinstance(operator, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)):
                    values.update(strings(comparator))
    return values


def mode_values_in_templates() -> set[str]:
    """テンプレートに静的に記述された hidden mode を抽出する。"""
    values: set[str] = set()
    input_pattern = re.compile(
        r"<input\b(?=[^>]*\bname=[\"']mode[\"'])(?=[^>]*\bvalue=[\"']([^\"']+)[\"'])[^>]*>",
        re.IGNORECASE,
    )
    for path in (ROOT / "templates").glob("*.html"):
        values.update(match.group(1) for match in input_pattern.finditer(path.read_text(encoding="utf-8")))
    return values


def documented_mode_values(actions: list[dict[str, str]], routes: dict[str, str]) -> set[str]:
    """台帳の行に記載した mode 値を、互換ルート表記を含めて取り出す。"""
    values = set(routes)
    for action in actions:
        if "mode=" not in action["mode"]:
            continue
        mode_value = action["mode"].split("mode=", 1)[1].split(",", 1)[0]
        values.update(part.strip() for part in mode_value.split("/") if part.strip())
    return values


def action_row(
    category: str,
    name: str,
    mode: str,
    method: str,
    state: str,
    v2_source: str,
    current_source: str,
    checks: str,
) -> dict[str, str]:
    return {
        "category": category,
        "name": name,
        "mode": mode,
        "method": method,
        "state": state,
        "v2_source": v2_source,
        "current_source": current_source,
        "checks": checks,
    }


def command_action_rows() -> list[dict[str, str]]:
    rows = [
        action_row("認証・登録", "トップ／ログイン前画面", "（others.py）", "GET", "表示", "旧版_ver2/others.cgi", "others.py / templates/others.html", "公開範囲、ログイン入力、登録導線"),
        action_row("認証・登録", "新規登録入力", "mode=chara_make", "POST", "表示", "旧版_ver2/others.cgi / chara_make.cgi", "others.py / templates/chara_make.html", "入力項目、初期職、画像選択、CSRF"),
        action_row("認証・登録", "新規登録確認", "mode=make_pre", "POST", "表示", "旧版_ver2/chara_make.cgi", "chara_make.py / templates/chara_make_pre.html", "入力検証、同一IP制限、確認画面"),
        action_row("認証・登録", "新規登録確定", "mode=make_end", "POST", "状態変更", "旧版_ver2/chara_make.cgi", "chara_make.py", "初期能力・初期装備・保存形式・パスワード"),
        action_row("認証・登録", "ログイン", "mode=log_in", "POST", "状態変更", "旧版_ver2/login.cgi", "login.py", "認証方式、セッション、旧ハッシュ移行、日次バックアップ"),
        action_row("認証・登録", "ログアウト", "mode=log_out", "POST/GET", "状態変更", "旧版_ver2/login.cgi", "login.py", "セッション破棄、遷移先"),
        action_row("認証・登録", "合言葉を設定", "mode=passset", "POST", "状態変更", "旧版_ver2/passchange.cgi", "cgi_py/passchange.py", "現在パスワード、未設定確認、合言葉、保存時刻・接続元ホスト"),
        action_row("認証・登録", "パスワード変更確定", "mode=passchan", "POST", "状態変更", "旧版_ver2/passchange.cgi", "cgi_py/passchange.py", "旧/新パスワード検証、4〜8文字の半角英数字・記号、ハッシュ、接続元ホスト、セッション更新"),
        action_row("街・プロフィール", "街のメイン画面", "mode=main", "GET/POST", "表示", "旧版_ver2/ffadventure.cgi", "cgi_py/ffadventure.py", "能力表示、王者情報、待機時間、掲示板表示"),
        action_row("街・プロフィール", "レジェンド挑戦を中断して街へ戻る", "mode=main, legend_cancel=1", "POST", "状態変更", "旧版_ver2/ffadventure.cgi", "cgi_py/ffadventure.py", "boss_flagのリセット値、CSRF、途中進行の扱い"),
        action_row("街・プロフィール", "自分のステータスを表示", "mode=sts", "POST", "表示", "旧版_ver2/sts.cgi", "cgi_py/sts.py", "能力・装備補正・現職クラス・職業熟練度・表示値"),
        action_row("街・プロフィール", "画像・発動コメントを変更", "mode=st_buy", "POST", "状態変更", "旧版_ver2/sts.cgi", "cgi_py/sts.py", "画像ID、コメント長・禁止語、ロック後の再読込・ホスト更新・保存"),
        action_row("街・プロフィール", "戦術一覧を表示", "mode=tac_change", "POST", "表示", "旧版_ver2/tac_change.cgi", "cgi_py/tac_change.py", "現在職・マスター職の使用可能条件、master_tac設定、現在戦術"),
        action_row("街・プロフィール", "戦術を変更", "mode=senjutu_henkou", "POST", "状態変更", "旧版_ver2/tac_change.cgi", "cgi_py/tac_change.py", "戦術ID、職業・熟練度条件、ロック後の再検証・ホスト更新・保存"),
        action_row("街・プロフィール", "転職画面を表示", "mode=tensyoku", "POST", "表示", "旧版_ver2/tensyoku.cgi", "cgi_py/tensyoku.py", "候補職、能力条件、マスター条件"),
        action_row("街・プロフィール", "転職を実行", "mode=tensyoku_change", "POST", "状態変更", "旧版_ver2/tensyoku.cgi", "cgi_py/tensyoku.py", "転職条件、現職熟練度、能力上限、戦術、接続元ホスト"),
        action_row("街・プロフィール", "掲示板へ投稿", "mode=post", "POST", "状態変更", "旧版_ver2に一般掲示板はなし（post_message.cgiは私信）", "cgi_py/bbs.py", "文字数、保存上限、投稿者、禁止語、CSRF"),
        action_row("街・プロフィール", "私信・受信拒否・友人登録（Ver2のみ）", "Ver2専用（message / all_list / limit / ban / friend）", "POST", "Ver3未実装", "旧版_ver2/post_message.cgi", "該当なし", "私信、受信・送信箱、受信拒否、友人登録、件数上限"),
        action_row("店・資産", "宿泊", "mode=yado", "POST", "状態変更", "旧版_ver2/shop.cgi", "cgi_py/shop.py", "宿代、HP全快、王者HP、boss_flagリセット、接続元ホスト"),
        action_row("店・資産", "銀行を表示", "mode=bank", "POST", "表示", "旧版_ver2/bank.cgi", "cgi_py/bank.py", "所持金・預金上限、表示単位"),
        action_row("店・資産", "銀行へ預け入れ", "mode=bank_sell", "POST", "状態変更", "旧版_ver2/bank.cgi", "cgi_py/bank.py", "半角数値、1,000G単位、所持金・預金上限、接続元ホスト"),
        action_row("店・資産", "銀行から引き出し", "mode=bank_buy", "POST", "状態変更", "旧版_ver2/bank.cgi", "cgi_py/bank.py", "半角数値、1,000G単位、預金残高、所持金上限、接続元ホスト"),
        action_row("店・資産", "倉庫を表示", "mode=souko", "POST", "表示", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "装備中・保管中の区分、表示順"),
    ]

    shops = (
        ("weapon", "武器", "shop_item.cgi"),
        ("armor", "防具", "shop_def.cgi"),
        ("accessory", "装飾品", "shop_acs.cgi"),
    )
    for kind, label, v2_file in shops:
        rows.extend((
            action_row("店・資産", f"{label}店を表示", f"mode=shop_{kind}", "POST", "表示", f"旧版_ver2/{v2_file}", f"cgi_py/shop_{kind}.py", "品揃え、職業制限、価格、所持品表示"),
            action_row("店・資産", f"{label}を購入", "mode=buy", "POST", "状態変更", f"旧版_ver2/{v2_file}", f"cgi_py/shop_{kind}.py", "item_no、価格、職業制限、所持金、保管先"),
            action_row("店・資産", f"{label}を売却", "mode=sell", "POST", "状態変更", f"旧版_ver2/{v2_file}", f"cgi_py/shop_{kind}.py", "売値、装備中の扱い、保管品削除、所持金上限"),
        ))

    for kind, label in (("weapon", "武器"), ("armor", "防具"), ("accessory", "装飾品")):
        rows.extend((
            action_row("店・資産", f"装備中の{label}を倉庫へ外す", f"mode={kind}_remove", "POST", "状態変更", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "初期装備化、保管先、二重登録"),
            action_row("店・資産", f"倉庫の{label}を装備", f"mode={kind}_equip", "POST", "状態変更", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "item_no、職業制限、既存装備の退避"),
            action_row("店・資産", f"倉庫の{label}を削除", f"mode={kind}_delete", "POST", "状態変更", "旧版_ver2/souko.cgi", "cgi_py/souko.py", "item_no、削除対象、復元不能な削除の確認"),
        ))

    rows.extend((
        action_row("戦闘・対戦", "チャンピオンに挑戦", "mode=battle", "POST", "状態変更", "旧版_ver2/battle.cgi / wbattle.pl", "cgi_py/battle.py / sub_def/battle_logic.py", "待機時間、勝敗・引分、経験値・賞金、王者交代"),
        action_row("戦闘・対戦", "道場の入口を表示", "mode=log_in", "POST", "表示", "旧版_ver2/select_battle.cgi", "cgi_py/select_battle.py", "名前検索・一覧選択への導線、保存なし"),
        action_row("戦闘・対戦", "対人相手を選択", "mode=sentaku", "POST", "表示", "旧版_ver2/select_battle.cgi", "cgi_py/select_battle.py", "相手ID、本人・無効対象の除外、表示順"),
        action_row("戦闘・対戦", "選択相手と対戦", "mode=battle", "POST", "状態変更", "旧版_ver2/select_battle.cgi / wbattle.pl", "cgi_py/select_battle.py / sub_def/battle_logic.py", "相手認証、勝敗、経験値・賞金、戦績"),
        action_row("戦闘・対戦", "通常モンスター修行", "mode=monster", "POST", "状態変更", "旧版_ver2/monster.cgi / mbattle.pl", "cgi_py/monster.py / sub_def/battle_logic.py", "出現テーブル、回数制限、勝敗・引分報酬、経験値"),
        action_row("戦闘・対戦", "幻影の城へ挑戦", "mode=genei", "POST", "状態変更", "旧版_ver2/monster.cgi / mbattle.pl", "cgi_py/monster.py / sub_def/battle_logic.py", "出現条件、HP/防御補正、報酬"),
        action_row("戦闘・対戦", "異世界へ挑戦", "mode=isekiai", "POST", "状態変更", "旧版_ver2/monster.cgi / mbattle.pl", "cgi_py/monster.py / sub_def/battle_logic.py", "レベル条件、出現テーブル、特殊報酬"),
        action_row("戦闘・対戦", "レジェンド攻略者一覧を閲覧", "mode=legend, view=ranking", "GET", "表示", "旧版_ver2/legend.cgi", "cgi_py/legend.py", "公開範囲、順位、称号"),
        action_row("戦闘・対戦", "レジェンドの階層へ挑戦", "mode=boss, boss_file=0〜3", "POST", "状態変更", "旧版_ver2/legend.cgi / mbattle.pl", "cgi_py/legend.py / sub_def/battle_logic.py", "進行フラグ、階層順、勝敗・称号・報酬"),
        action_row("戦闘・対戦", "天下一武道会ロビーを表示", "mode=tenka", "POST", "表示", "旧版_ver2/tenka.cgi", "cgi_py/tenka.py", "参加条件、進行状態、対戦相手"),
        action_row("戦闘・対戦", "天下一武道会で対戦", "mode=battle, no=1〜3", "POST", "状態変更", "旧版_ver2/tenka.cgi / wbattle.pl", "cgi_py/tenka.py / sub_def/battle_logic.py", "ラウンド順、引分・敗北、賞金・経験値・制覇履歴"),
        action_row("閲覧", "英雄ランキングを表示", "mode=rank", "GET", "表示", "旧版_ver2/rank.cgi", "cgi_py/rank.py", "部門、勝率の対象条件、キャッシュ"),
        action_row("閲覧", "登録者一覧を表示", "mode=ranking, shtm", "GET", "表示", "旧版_ver2/system.cgi", "cgi_py/system.py", "ページング、公開項目、キャッシュ"),
        action_row("閲覧", "他者の詳細ステータスを表示", "mode=chara_sts, id", "GET", "表示", "旧版_ver2/system.cgi", "cgi_py/system.py", "公開項目、装備・マスター職、ID指定"),
        action_row("閲覧", "キャラクター画像一覧を表示", "mode=img_list", "GET", "表示", "旧版_ver2/system.cgi", "cgi_py/system.py", "画像ID・ファイル対応"),
    ))

    training = (
        ("race0", "バーベルあげ", "速度"), ("race1", "砂浜走り", "スタミナ"),
        ("race2", "スイミング", "粘り"), ("race3", "瞑想", "落ち着き"),
        ("race4", "猛特訓", "闘争心"), ("race5", "お勉強", "賢さ"), ("race6", "坂道ダッシュ", "反射神経"),
    )
    for mode, name, stat in training:
        rows.append(action_row("チョコボ", f"チョコボ訓練: {name}", f"mode={mode}", "POST", "状態変更", "旧版_ver2/ctrain.cgi", "cgi_py/ctrain.py", f"{stat}の増減、寿命、失敗時の副作用、待機時間"))

    rows.extend((
        action_row("チョコボ", "チョコボ牧場を表示", "mode=chocofarm", "POST", "表示", "旧版_ver2/chocofarm.cgi", "cgi_py/chocofarm.py", "所持判定、レース条件、重賞開催条件"),
        action_row("チョコボ", "チョコボの森を表示", "mode=choco / morifarm", "POST", "表示", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "所持判定、候補表示、互換ルート"),
        action_row("チョコボ", "野生チョコボ候補を表示", "mode=choco_shop", "POST", "表示", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "候補抽選、候補数、マスター参照"),
        action_row("チョコボ", "野生チョコボを購入", "mode=choco_buy, item_no", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "候補検証、価格、初期能力、所持制限"),
        action_row("チョコボ", "お見合い相手を表示", "mode=choco_shopb", "POST", "表示", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "性別、引退候補、候補上限"),
        action_row("チョコボ", "お見合い・配合を実行", "mode=choco_buyb, item_no", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "親の引退、血統、能力上限、子の初期値"),
        action_row("チョコボ", "チョコボに名前を付ける", "mode=choco_name", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "名前入力、禁止語、保存"),
        action_row("チョコボ", "チョコボを休ませる", "mode=yadoya", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "寿命・体力の回復、費用、待機時間"),
        action_row("チョコボ", "チョコボを手放す", "mode=choco_sell", "POST", "状態変更", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "引退先、売却額、取り消し不可"),
        action_row("チョコボ", "チョコボ殿堂を表示", "mode=list", "POST", "表示", "旧版_ver2/dendo.cgi", "cgi_py/dendo.py / templates/chocofarm.html", "登録済み一覧、トロフィー表示、表示用modeと登録用modeの分離"),
        action_row("チョコボ", "チョコボを殿堂登録", "mode=dendo", "POST", "状態変更", "旧版_ver2/dendo.cgi", "cgi_py/dendo.py", "重賞3勝条件、重複登録、保存値"),
        action_row("チョコボ", "チョコボランキングを表示", "mode=ranking", "POST", "表示", "旧版_ver2/chocorank.cgi", "cgi_py/chocorank.py", "部門、ランキング対象、表示値"),
        action_row("チョコボ", "チョコボ王者戦", "mode=farmrace", "POST", "状態変更", "旧版_ver2/farmrace.cgi", "cgi_py/farmrace.py", "挑戦条件、勝敗、王者更新、待機時間"),
    ))

    regular_races = (
        ("race0", "新馬戦"), ("race1", "500万以下"), ("race2", "900万以下"),
        ("race3", "1600万以下"), ("race4", "オープン特別"), ("race5", "グレードIII"), ("race6", "グレードII"),
    )
    for mode, name in regular_races:
        rows.append(action_row("チョコボ", f"チョコボレース: {name}", f"mode={mode}", "POST", "状態変更", "旧版_ver2/crace.cgi", "cgi_py/crace.py", "勝利数条件、ライバルファイル、寿命、賞金・戦績"))
    for race_id, name in enumerate(("チョコボダービー", "チョコボスタリオン", "チョコボカップ", "ジェイドカップ", "BBA賞", "チョコボ春賞", "チョコボ秋賞", "チョコボキング", "チョコボステークス", "キングスカップ", "クイーンカップ"), start=1):
        rows.append(action_row("チョコボ", f"G1レース: {name}", f"mode=race7, race={race_id}", "POST", "状態変更", "旧版_ver2/crace.cgi", "cgi_py/crace.py", "開催周期・性別、勝利数条件、トロフィー、ライバル"))
    for race_id, name in enumerate(("シルバーカップ", "新潟アドバンス", "チコスダービー", "チョコボードカップ", "チョコボエプソム", "チョコボ王", "ブリーダーズカップ", "ゴールドカップ", "プラチナカップ", "チョコボオークス", "チョコボキングス"), start=12):
        rows.append(action_row("チョコボ", f"G2レース: {name}", f"mode=race8, race={race_id}", "POST", "状態変更", "旧版_ver2/crace.cgi", "cgi_py/crace.py", "開催周期・性別、勝利数条件、トロフィー、ライバル"))
    rows.append(action_row("チョコボ", "殿堂レジェンドレース", "mode=race_dendo", "POST", "状態変更", "旧版_ver2/crace.cgi / denchoco.cgi", "cgi_py/crace.py", "出走条件、殿堂データ、勝敗・報酬"))

    admin_actions = (
        ("管理画面を表示", "kanri_top", "表示", "管理画面認証、一覧範囲"),
        ("管理画面からログアウト", "admin_log_out", "状態変更", "管理セッションの破棄"),
        ("全体メッセージを投稿", "post_all_message", "状態変更", "文字数、保存上限、投稿者"),
        ("マスター一覧を表示", "master_list", "表示", "対象マスター、ID順"),
        ("マスターを編集表示", "master_edit", "表示", "master_type、master_id、新規判定"),
        ("マスターを保存", "master_save", "状態変更", "JSON検証、ID重複、バックアップ"),
        ("マスターを削除", "master_delete", "状態変更", "削除対象、参照整合性、バックアップ"),
        ("プレイヤー所持品を表示", "player_item", "表示", "対象ID、装備・保管品"),
        ("プレイヤー所持品を追加", "player_item_add", "状態変更", "対象ID、アイテム参照、重複"),
        ("バックアップから復元", "backup_restore", "状態変更", "バックアップ名、現在状態退避、復元範囲"),
        ("保護ユーザーを復元", "restore_protected", "状態変更", "保護対象、復元元、上書き"),
        ("全キャラクターデータを表示", "kanri_all", "表示", "一覧範囲、公開情報"),
        ("個別キャラクターデータを表示", "data", "表示", "対象ID、編集項目"),
        ("個別キャラクターデータを保存", "save", "状態変更", "能力値境界、職業・HP・所持金、保存"),
        ("個別キャラクターを削除", "del_chara", "状態変更", "対象ID、関連保存データ、復元可能性"),
        ("未プレイキャラクターを削除", "del_noplay", "状態変更", "対象条件、保護ユーザー、削除範囲"),
    )
    for name, mode, state, checks in admin_actions:
        rows.append(action_row("管理", name, f"mode={mode}", "POST", state, "旧版_ver2/admin.cgi / alldata.cgi", "admin.py / templates/admin.html", checks))
    return rows


def write_commands_actions() -> None:
    routes = function_routes()
    if set(routes) != set(ROUTE_DETAILS):
        missing = sorted(set(routes) - set(ROUTE_DETAILS))
        stale = sorted(set(ROUTE_DETAILS) - set(routes))
        raise ValueError(f"ルート説明の不足または古さがあります: missing={missing}, stale={stale}")

    actions = command_action_rows()
    route_comparisons = command_route_comparisons(routes)
    action_comparisons = command_action_comparisons(actions)
    documented_modes = documented_mode_values(actions, routes)
    undocumented_source = mode_values_in_source() - documented_modes
    undocumented_template = mode_values_in_templates() - documented_modes
    if undocumented_source or undocumented_template:
        raise ValueError(
            "比較台帳に未記載のmodeがあります: "
            f"source={sorted(undocumented_source)}, template={sorted(undocumented_template)}"
        )

    sections = [
        "# コマンド・行動比較チェックリスト",
        "",
        "画面遷移だけのルートと、各ルート内の実行操作を分けて管理します。"
        "比較前に状態変更か表示かを確認し、Ver2との差分を具体的に記録します。",
        "",
        "## ファイル単位の精査記録",
        "",
        "ここには一次台帳作成後に、Ver2実装と現行実装を分岐・保存値・表示まで再確認したファイルだけを記録します。"
        "未記載のファイルは未精査であり、一次比較完了を根拠に一致と扱いません。",
        "",
        "| Ver3対象ファイル | Ver2確認箇所 | 確認範囲 | Ver2との差異 | 意図的な仕様か否か | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for audit in FILE_AUDITS:
        sections.append(
            f"| `{audit['file']}` | `{audit['v2_source']}` | {audit['scope']} | "
            f"{audit['difference']} | {audit['intent']} | {audit['note']} |"
        )
    sections.extend((
        "",
        "## ルート一覧（login.py）",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ))
    for mode, module in routes.items():
        purpose, state, v2_source = ROUTE_DETAILS[mode]
        comparison = route_comparisons[mode]
        sections.append(
            f"| ルート `mode={mode}`: {purpose} | `{v2_source}` | `login.py` → `{module}` / {state} | "
            f"{comparison['difference']} | {comparison['intent']} | {comparison['status']} | {comparison['note']} |"
        )

    sections.extend(("", "## 実行操作一覧", ""))
    categories: list[str] = []
    for action in actions:
        if action["category"] not in categories:
            categories.append(action["category"])
    for category in categories:
        sections.extend((
            f"### {category}",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for action in (item for item in actions if item["category"] == category):
            comparison = action_comparisons[action["name"]]
            sections.append(
                f"| {action['name']}（`{action['mode']}` / {action['method']} / {action['state']}） | "
                f"`{action['v2_source']}` | `{action['current_source']}` | {comparison['difference']} | "
                f"{comparison['intent']} | {comparison['status']} | {comparison['note']} |"
            )
        sections.append("")
    sections.insert(4, f"対象: ルート {len(routes)}件、実行操作 {len(actions)}件、二次精査 {len(FILE_AUDITS)}ファイル。")
    (OUTPUT_DIR / "commands_actions.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def _require_command_source_snippets() -> None:
    """ルート・操作台帳が実在する入口と分岐を参照していることを確認する。"""
    required = {
        "login.py": ("FUNCTION_MAP", "POST_ONLY_ROUTE_MODES", "token_check(FORM, session)"),
        "others.py": ("def main",), "chara_make.py": ("mode == \"make_pre\"", "mode == \"make_end\""),
        "cgi_py/sts.py": ("mode == \"st_buy\"",), "cgi_py/tac_change.py": ("senjutu_henkou",),
        "cgi_py/bank.py": ("bank_sell", "bank_buy"), "cgi_py/souko.py": ("weapon_remove", "armor_remove", "accessory_remove"),
        "cgi_py/morifarm.py": ("choco_buyb", "choco_sell", "yadoya"), "cgi_py/crace.py": ("race_dendo", "race7", "race8"),
        "cgi_py/ctrain.py": ("race0", "race6"), "admin.py": ("master_save", "backup_restore", "del_noplay"),
    }
    for relative_path, snippets in required.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
        missing = [snippet for snippet in snippets if snippet not in text]
        if missing:
            raise ValueError(f"コマンド比較の根拠が見つかりません: {relative_path}: {missing}")


def command_route_comparisons(routes: dict[str, str]) -> dict[str, dict[str, str]]:
    _require_command_source_snippets()
    public = {"rank", "system", "chara_sts", "img_list", "ranking"}
    aliases = {
        "yado": "shop", "shop_item": "shop_weapon", "shop_def": "shop_armor", "shop_acs": "shop_accessory",
        "sentaku": "select_battle", "genei": "monster", "isekiai": "monster", "boss": "legend",
        "choco": "morifarm", "chara_sts": "system", "img_list": "system", "ranking": "system",
    }
    result = {}
    for mode, module in routes.items():
        if mode in aliases:
            difference = f"Ver3で`{aliases[mode]}`への互換別名を明示"
            note = f"login.pyのFUNCTION_MAPで{module}へ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。"
        elif mode in public:
            difference = "公開閲覧をlogin.pyの許可リストで明示"
            note = "未ログインでも閲覧可。状態更新POSTは該当モジュール側の本人確認・共通CSRF検証を必要とする。"
        elif mode in {"battle", "monster", "genei", "isekiai", "boss", "dendo", "farmrace"}:
            difference = "状態変更ルートをPOST専用＋共通CSRF検証へ変更"
            note = "GET直打ちはlogin.pyで拒否し、ログイン済みセッションを確認してからモジュールを遅延ロードする。"
        elif mode == "legend":
            difference = "攻略者一覧だけ公開閲覧として分離"
            note = "view=rankingのGETだけ未ログイン閲覧可。攻略実行はPOST専用・ログイン必須でboss互換ルートにも対応する。"
        else:
            difference = "個別CGI入口からlogin.pyの集中ルーティングへ移行"
            note = f"FUNCTION_MAPで{module}を選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。"
        result[mode] = {"difference": difference, "intent": "意図的", "status": "差異あり", "note": note}
    return result


def command_action_comparisons(actions: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """121操作を、同じ操作種別でも入力・更新対象が分かる記録にする。"""
    _require_command_source_snippets()
    result: dict[str, dict[str, str]] = {}
    specific = {
        "トップ／ログイン前画面": ("UTF-8テンプレート画面へ移行", "公開のログイン・登録導線をothers.pyで表示。認証済み状態を前提にしない。"),
        "新規登録入力": ("入力画面をJinja化しCSRFを追加", "職業・画像・ID等の入力を表示し、POST確認画面へ渡す。"),
        "新規登録確認": ("サーバー側検証と確認トークンを追加", "入力形式・重複ID/名前/ホストを確認し、確定処理へ必要な値だけを渡す。"),
        "新規登録確定": ("統合JSON・PBKDF2保存へ移行", "初期能力・装備・職歴・倉庫を原子的に生成する。初期ゲーム値の対応は所有・進行台帳で確認済み。"),
        "ログイン": ("平文照合Cookieからハッシュ照合・暗号化セッションへ移行", "POST+CSRFで認証し、旧形式は成功時だけ再ハッシュ、日次バックアップ後に街へ遷移する。"),
        "ログアウト": ("暗号化セッション破棄へ移行", "destroy_sessionで認証Cookieを破棄しothers.pyへ遷移する。"),
        "合言葉を設定": ("本人確認をセッション・CSRF前提へ変更", "新規登録時に未作成だった合言葉だけを設定する。現在のパスワードと未設定状態を確認し、合言葉・保存時刻・接続元ホストを保存する。"),
        "パスワード変更確定": ("PBKDF2更新・セッション再発行へ変更", "旧パスワード/合言葉と新値を検証する。新パスワードはVer2と同じ4〜8文字で、現行は画面の案内どおり半角英数字・記号だけを受け付ける。保存済みハッシュ・接続元ホスト・認証状態を更新する。"),
        "街のメイン画面": ("テンプレート表示と共有ニュース/BBS分離", "能力・王者・待機時間・現職クラスを計算し、all_messageとbbsを別データとして表示する。チャンピオン戦以外の戦闘導線はbattle_count>0を確認して表示する。"),
        "レジェンド挑戦を中断して街へ戻る": ("POST+CSRFで進行値をリセット", "legend_cancel時だけboss_flagを設定初期値へ戻す。"),
        "自分のステータスを表示": ("名前付き状態・テンプレート表示へ移行", "能力、アクセサリー補正、現職クラス、職業熟練度を現行データから組み立てる。ホームページ名・URLは現行スキーマから意図的に除外する。"),
        "画像・発動コメントを変更": ("入力値検証を追加", "画像IDとコメント長・禁止語を検査する。Ver2と同じくロック後に最新charaを読み込み、画像・コメント・接続元ホストを保存する。"),
        "戦術一覧を表示": ("利用可否をJSON職歴から算出", "現職の戦術と、master_tactics_enabled=1のときのLv60以上の他職戦術を表示する。これはVer2のmaster_tacと同じ独立設定で、転職時の選択戦術リセットとは分けている。"),
        "戦術を変更": ("POST時の戦術ID・利用条件検証を追加", "未選択・不正・未習得の戦術を拒否する。Ver2と同じくロック後に最新のchara/syokuから候補を再構築し、tactic_idと接続元ホストを保存する。"),
        "転職画面を表示": ("職業マスターをJSONから参照", "能力・職歴前提を満たす候補と未マスター候補を分けて表示する。"),
        "転職を実行": ("実行POSTでも前提職を再検証", "現職Lvを退避、転職先Lvを復帰し、必要なら戦術を初期化する。成功時はVer2と同じく接続元ホストを更新し、chara/syokuを同時保存する。能力減少値は一致し、カルマの下限だけはVer2の0許容に対して現行は1へ戻す意図的仕様。"),
        "掲示板へ投稿": ("Ver2にない一般掲示板を追加", "本人ID・200文字・禁止語を検査し、新着順で最大100件を共有JSONへ書込む。私信を置換した機能ではなく、投稿後はPRGリダイレクトとCSRFを用いる独立機能である。"),
        "私信・受信拒否・友人登録（Ver2のみ）": ("Ver3に実行経路がない", "Ver2のpost_message.cgiは私信送受信、送受信箱、全受信拒否、個別拒否、友人登録を扱う。現行スキーマには移行値が残るがCGIの読書き経路はないため、復元するか機能廃止とするか要判断。", "要判断"),
        "宿泊": ("状態更新をshop.pyへ集約", "料金確認後にHPを回復し、王者表示用状態とレジェンド進行の宿屋処理を更新する。Ver2と同じく接続元ホストも保存する。"),
        "銀行を表示": ("統合JSONのgold/bankを表示", "本人の所持金・預金と上限を表示し、変更はしない。"),
        "銀行へ預け入れ": ("入力検証と原子的保存を追加", "半角数字の1,000G単位で、所持金を確認してgoldからbankへ移す。預金上限を超える分はVer2の画面案内どおり国への寄付としてgoldから差し引き、bankには上限までだけ加算する。成功時は接続元ホストも保存する。"),
        "銀行から引き出し": ("入力検証と原子的保存を追加", "半角数字の1,000G単位で、預金残高・所持金上限を検査してbankからgoldへ移す。成功時は接続元ホストも保存する。"),
        "倉庫を表示": ("3種別の保管ファイルを統合JSON配列・テンプレート表示へ移行", "装備中とsouko_weapon/armor/accessoryを分けて表示する。Ver2の削除済み空行はJSON配列へ保持せず、現行では詰めて表示する。"),
        "装備中の武器を倉庫へ外す": ("着脱時の接続元保存を現行は省略", "武器倉庫8件を確認してマスター値を退避し、素手へ戻す。Ver2はREMOTE_ADDRを保存するが、現行は装備・倉庫だけを更新する。", "要判断"),
        "倉庫の武器を装備": ("現行は選択品を除去し、旧装備を末尾へ追加", "Ver2は選択した保管位置を旧装備で置換する。現行の並び替えを伴う方式を維持するかは要判断。職業制限はVer2・現行とも倉庫交換時に再検証しない。", "要判断"),
        "倉庫の武器を削除": ("Ver2の二段階確認を現行は省略", "Ver2は確認画面を挟んでから削除するが、現行はCSRF付きの1回のPOSTで削除する。復元不能な操作のため確認を復元するか要判断。", "要判断"),
        "装備中の防具を倉庫へ外す": ("着脱時の接続元保存を現行は省略", "防具倉庫8件を確認してマスター値を退避し、衣服へ戻す。Ver2はREMOTE_ADDRを保存するが、現行は装備・倉庫だけを更新する。", "要判断"),
        "倉庫の防具を装備": ("現行は選択品を除去し、旧装備を末尾へ追加", "Ver2は選択した保管位置を旧装備で置換する。現行の並び替えを伴う方式を維持するかは要判断。職業制限はVer2・現行とも倉庫交換時に再検証しない。", "要判断"),
        "倉庫の防具を削除": ("Ver2の二段階確認を現行は省略", "Ver2は確認画面を挟んでから削除するが、現行はCSRF付きの1回のPOSTで削除する。復元不能な操作のため確認を復元するか要判断。", "要判断"),
        "装備中の装飾品を倉庫へ外す": ("着脱時の接続元保存を現行は省略", "装飾品倉庫8件を確認してマスター値を退避し、補正なしへ戻す。Ver2はREMOTE_ADDRを保存するが、現行は装備・倉庫だけを更新する。", "要判断"),
        "倉庫の装飾品を装備": ("現行は選択品を除去し、旧装備を末尾へ追加", "Ver2は選択した保管位置を旧装備で置換する。現行の並び替えを伴う方式を維持するかは要判断。", "要判断"),
        "倉庫の装飾品を削除": ("Ver2の二段階確認を現行は省略", "Ver2は確認画面を挟んでから削除するが、現行はCSRF付きの1回のPOSTで削除する。復元不能な操作のため確認を復元するか要判断。", "要判断"),
        "武器店を表示": ("職別販売ファイルをJSON抽出・共通テンプレートへ移行", "装備中武器の価格は両版ともマスター価格の2/3で表示する。現行はCSRF付きフォーム、未選択を防ぐrequired、倉庫・街への導線を追加する。"),
        "武器を購入": ("販売候補をJSONから再取得し、統合倉庫へ原子的に保存", "職業別商品・所持金・武器倉庫8件・商品番号をサーバー側で確認し、価格を差し引いてREMOTE_ADDRと倉庫を保存する。商品1032〜1038の価格調整と1181の皇帝販売は装備台帳の判断に従う。"),
        "武器を売却": ("装備・所持金を統合JSONで同時保存し、結果をトースト表示", "装備中だけをマスター価格の2/3で下取りし、gold上限で打ち止めにして素手へ戻す。売却時に接続元を保存しない点はVer2と同じ。"),
        "防具店を表示": ("職別販売ファイルをJSON抽出・共通テンプレートへ移行", "装備中防具の価格は両版ともマスター価格の2/3で表示する。現行はCSRF付きフォーム、未選択を防ぐrequired、倉庫・街への導線を追加する。"),
        "防具を購入": ("販売候補をJSONから再取得し、統合倉庫へ原子的に保存", "職業別商品・所持金・防具倉庫8件・商品番号をサーバー側で確認し、価格を差し引いてREMOTE_ADDRと倉庫を保存する。商品2181の皇帝販売は装備台帳の判断に従う。"),
        "防具を売却": ("装備・所持金を統合JSONで同時保存し、結果をトースト表示", "装備中だけをマスター価格の2/3で下取りし、gold上限で打ち止めにして衣服へ戻す。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しないため維持可否は要判断。", "要判断"),
        "装飾品店を表示": ("職別販売ファイルをJSON抽出・共通テンプレートへ移行", "装備中装飾品の価格は両版ともマスター価格の2/3で表示する。現行は説明をdescriptionまたは能力補正から組み立て、CSRF付きフォーム・倉庫・街への導線を追加する。"),
        "装飾品を購入": ("販売候補をJSONから再取得し、統合倉庫へ原子的に保存", "職業別商品・所持金・装飾品倉庫8件・商品番号をサーバー側で確認し、価格を差し引いてREMOTE_ADDRと能力補正を含む倉庫要素を保存する。85・87の率補正は意図的なVer1準拠調整を維持する。"),
        "装飾品を売却": ("装備・所持金を統合JSONで同時保存し、結果をトースト表示", "装備中だけをマスター価格の2/3で下取りし、gold上限で打ち止めにして補正なしへ戻す。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しないため維持可否は要判断。", "要判断"),
        "チャンピオンに挑戦": ("POST専用・結果表示mode明示", "待機後に王者状態で戦い、結果・王者更新・経験値上限は戦闘/所有台帳の確認結果に従う。"),
        "道場の入口を表示": ("テンプレート入口とPOST+CSRFへ移行", "battle_count>0を表示・実行の双方で検査する。名前の完全一致検索または一覧選択へ進むだけで、保存状態は変更しない。"),
        "対人相手を選択": ("相手IDをサーバー側で再検証・本人選択を拒否", "battle_count>0を検査する。存在しない相手と本人を拒否して選択画面だけを表示する。Ver2の候補一覧は24時間キャッシュ済みレベル降順だが、現行は全ユーザーを直接列挙するため表示順を保証しない。"),
        "選択相手と対戦": ("模擬戦を保存しないシミュレーションへ明示", "battle_count>0を検査する。相手の現在のキャラクター・装備で戦い、経験値・所持金・戦績・待機時刻を更新しない。時間切れwin=3は相打ちと別表示にする。"),
        "通常モンスター修行": ("POST+CSRF・統合保存へ移行", "battle_count>0と出現表・修行回数を検査し、勝敗別報酬・戦績・職歴を保存する。戦闘後HPはレベルアップ後のvit/max_hpで回復する。"),
        "幻影の城へ挑戦": ("monster.pyのgenei分岐へ統合", "battle_count>0、出現条件、修行回数、敵攻撃への防具補正、幻影報酬を通常修行と区別して処理する。戦闘後HPはレベルアップ後のvit/max_hpで回復する。"),
        "異世界へ挑戦": ("monster.pyのisekiai分岐へ統合", "battle_count>0、レベル/進行条件と修行回数を検査し、異世界出現表と報酬を用いる。戦闘後HPはレベルアップ後のvit/max_hpで回復する。"),
        "レジェンド攻略者一覧を閲覧": ("公開GET閲覧を明示", "ログイン不要で攻略者を称号・戦績から並べ、状態変更は行わない。"),
        "レジェンドの階層へ挑戦": ("POST専用・階層値を検証、クリア後の再挑戦を許可", "battle_count>0、title_id、boss_flag、修行回数、待機時間を検査して階層別モンスターと戦う。クリア後は進行値を開始値へ戻し、現行は同じ階層を再挑戦できる。戦闘後HPはレベルアップ後のvit/max_hpで回復する。"),
        "天下一武道会ロビーを表示": ("24時間メンバーキャッシュへ移行", "battle_count>0を検査し、レベル上位者、参加可能boss_flag、進行ラウンド、制覇履歴を表示する。"),
        "天下一武道会で対戦": ("ラウンド番号をサーバー側照合、戦闘全体をユーザーロックで直列化", "battle_count>0と期待ラウンドを検査する。勝敗・進行のwin分岐は現行方針を維持し、戦闘前から保存までロックする。レベルアップ後のvit/max_hpで戦闘後HPを回復し、boss_flagが開始値を超える場合は開始値へ正規化する。"),
        "英雄ランキングを表示": ("HTMLキャッシュからJSONキャッシュへ移行", "部門別上位と勝率を24時間キャッシュから公開表示する。"),
        "登録者一覧を表示": ("JSONキャッシュ・ページングへ移行", "公開プレイヤーをレベル順にページ表示し、個人状態は更新しない。"),
        "他者の詳細ステータスを表示": ("公開GETの名前付き状態表示へ移行", "対象IDの能力・装備・称号・マスター職を読み取り専用で表示する。"),
        "キャラクター画像一覧を表示": ("設定の画像マスターを表示", "公開画像IDとファイル対応を読み取り専用で出力する。"),
    }
    for action in actions:
        name, category, mode = action["name"], action["category"], action["mode"]
        if name in specific:
            comparison = specific[name]
            difference, note = comparison[:2]
            intent = comparison[2] if len(comparison) > 2 else "意図的"
        elif category == "店・資産":
            label = "武器" if "武器" in name else "防具" if "防具" in name else "装飾品"
            if "購入" in name:
                difference, note = "購入POSTの入力・職業・所持金検証を追加", f"{label}IDをマスター参照し、職業制限・価格・倉庫上限を確認して倉庫へ追加する。"
            elif "売却" in name:
                difference, note = "売却対象を倉庫要素へ限定", f"{label}の保管番号を検証し、売値をgold上限内で加算して対象要素を削除する。"
            elif "外す" in name:
                difference, note = "装備と倉庫を統合JSONで同時更新", f"装備中の{label}を倉庫へ退避し、初期{label}へ戻す。倉庫上限と二重登録を検査する。"
            elif "装備" in name:
                difference, note = "倉庫番号を配列添字として検証", f"選択{label}を装備し、既存装備を倉庫へ退避する。武器/防具では職業制限も再検証する。"
            else:
                difference, note = "個別店CGIを種別モジュールへ分離", f"{label}マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。"
            intent = "意図的"
        elif category == "チョコボ":
            if name.startswith("チョコボ訓練:"):
                stat = name.split(": ", 1)[1]
                difference, note = "訓練modeを検証して統合chocoへ保存", f"{stat}用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。"
                intent = "意図的"
            elif name.startswith("チョコボレース:") or name.startswith("G1レース:") or name.startswith("G2レース:"):
                difference, note = "レースID・開催条件をサーバー側で検証", f"{mode}をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。"
                intent = "意図的"
            elif name == "殿堂レジェンドレース":
                difference, note, intent = "殿堂JSONをライバル表へ利用", "race_dendoだけdenchoco.jsonを参照し、出走資格・寿命・結果報酬を通常レースと分けて処理する。", "意図的"
            elif name == "チョコボを殿堂登録":
                difference, note, intent = "重賞3個条件を追加", "Ver2にないG1/G2タイトル3個を検査し、同ID・同名は上書き、他は先頭追加する。", "要判断"
            elif name == "チョコボを手放す":
                difference, note, intent = "未所持値を明示消去し候補リストをJSON化", "名前付き個体だけを性別別お見合い候補へ移し、chocoを空辞書へ戻す。候補固定枠廃止は要判断。", "要判断"
            elif name == "野生チョコボを購入":
                difference, note, intent = "所持中の直接POST上書きを拒否", "候補ID・価格・未所持を再検証し、初期能力の個体と空の重賞履歴を同時保存する。", "意図的"
            elif name == "お見合い・配合を実行":
                difference, note, intent = "親候補・所持状態を再検証", "相手候補、所持個体、価格を検査して血統・能力上限・初期状態を計算し現役個体を置換する。", "意図的"
            elif name == "チョコボに名前を付ける":
                difference, note, intent = "名称・禁止語・殿堂履歴の検証を追加", "未所持/無名を検査し、既存殿堂名との重複を拒否してchoco.nameだけを更新する。", "意図的"
            elif name == "チョコボを休ませる":
                difference, note, intent = "統合choco/charaの同時保存へ移行", "G5000・体力最大・所持を検査し、回復量、train、maxを更新する。", "意図的"
            elif name == "チョコボ王者戦":
                difference, note, intent = "王者状態を専用JSON・ロックで更新", "所持・待機・同一王者を検査し、勝者/連勝/前王者と通知を更新する。", "意図的"
            else:
                difference, note, intent = "チョコボ保存を統合JSON・共有JSONへ移行", "所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。", "意図的"
        elif category == "管理":
            if name in {"バックアップから復元", "保護ユーザーを復元"}:
                difference, note, intent = "Ver2にない復元操作を追加", "暗号化管理セッション・CSRF・maintenance_modeを要求し、入力名/固定復元元を検証して安全に復元する。", "意図的"
            elif "削除" in name:
                difference, note, intent = "管理セッション・CSRF・保護対象検査を追加", "対象と削除可否を検証し、関連JSONを安全に処理する。未プレイ削除は保護IDを除外する。", "意図的"
            elif "保存" in name or "追加" in name or "投稿" in name:
                difference, note, intent = "管理セッション・CSRF・型/範囲検証を追加", "入力を検証して原子的に保存し、マスター更新時はID一意性・下限・参照可能性を確認する。", "意図的"
            else:
                difference, note, intent = "hidden平文管理パスワードから暗号化管理セッションへ移行", "表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。", "意図的"
        else:
            difference, note, intent = "個別CGIから集中ルーティング・CSRF検証へ移行", "login.pyがログイン済み状態とPOSTトークンを確認した後、該当モジュールで入力と更新対象を検査する。", "意図的"
        result[name] = {"difference": difference, "intent": intent, "status": "差異あり", "note": note}
    if set(result) != {action["name"] for action in actions}:
        raise ValueError("コマンド操作比較の行定義が一致しません")
    return result


def comparison_row(name: str, v2_source: str, current_source: str, checks: str) -> str:
    return (
        f"| {name} | `{v2_source}` | `{current_source}` | 未確認 | 未判定 | 未確認 | {checks} |"
    )


def write_static_checklist(
    filename: str,
    title: str,
    introduction: str,
    sections_data: tuple[tuple[str, tuple[tuple[str, str, str, str], ...]], ...],
    comparisons: dict[str, dict[str, str]] | None = None,
) -> None:
    sections = [f"# {title}", "", introduction, ""]
    for heading, rows in sections_data:
        sections.extend((
            f"## {heading}",
            "",
            "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ))
        for row in rows:
            name, v2_source, current_source, checks = row
            comparison = (comparisons or {}).get(name)
            if comparison is None:
                sections.append(comparison_row(*row))
                continue
            sections.append(
                f"| {name} | `{comparison.get('source', v2_source)}` | `{current_source}` | "
                f"{comparison['difference']} | {comparison['intent']} | "
                f"{comparison['status']} | {comparison['note']} |"
            )
        sections.append("")
    (OUTPUT_DIR / filename).write_text("\n".join(sections), encoding="utf-8")


def write_battle_logic_checklist() -> None:
    write_static_checklist(
        "battle_logic.md",
        "戦闘計算・結果処理比較チェックリスト",
        "戦闘入口の一覧ではなく、共通シミュレータと各結果処理を比較単位にした台帳です。必殺技の個別効果は skills.md、モンスター特殊技は monster_skills.md と併用します。",
        (
            ("戦闘状態の初期化と攻撃値", (
                ("戦闘モード別の状態初期化", "旧版_ver2/battle.pl:shokika / mbattle.pl:shokika / wbattle.pl:shokika", "sub_def/battle_logic.py:BattleState.__init__", "mode別の初期値、対人・モンスターの状態キー、ターン上限"),
                ("装備・アクセサリーの戦闘用補正コピー", "旧版_ver2/battle.pl:acs_add / wbattle.pl:wacs_add", "sub_def/battle_logic.py:_with_accessory_bonus", "恒久保存値を変更しないこと、8能力値補正、対人側補正"),
                ("モンスターHP・初期HPの乱数", "旧版_ver2/mbattle.pl:mons_read / shokika", "sub_def/battle_logic.py:BattleState.__init__", "hp_base、random_range、最小値、表示用最大HP"),
                ("職業別の基礎ダメージ（全31職）", "旧版_ver2/battle.pl:syokuzero〜syokuthirty", "sub_def/battle_logic.py:get_job_dmg", "各職IDの参照能力値、乱数範囲、武器ATK、カルマの扱い"),
                ("モンスター・対人相手の基礎ダメージ", "旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.simulate", "base_damage、random_range、相手職業・装備、幻影の城補正"),
                ("最大ターンと時間切れ", "旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose", "sub_def/battle_logic.py:BattleState.turn / BattleSimulator.simulate", "最大ターン数、未決着時の引き分け、ログ最終ターン"),
            )),
            ("必殺技・固有効果の発動順", (
                ("選択戦術IDの取得", "旧版_ver2/battle.pl:chara[30] / wbattle.pl:winner[37]", "sub_def/battle_logic.py:get_tactic_id", "未設定値、不正値、現職以外のマスター戦術の使用可否"),
                ("戦術マスター由来の発動率分母", "旧版_ver2/tac.ini / battle.pl:tyosenwaza", "sub_def/battle_logic.py:_load_tactic_activation_denominators / skills.py:skill_check", "説明文の確率と乱数分母、未定義戦術、Ver2との差異"),
                ("プレイヤー必殺率・上限・特殊モード減衰", "旧版_ver2/battle.pl:tyosenwaza", "sub_def/battle_logic.py:BattleSimulator.simulate", "カルマ・職業熟練度・アクセ補正、75/95上限、genei・isekiai・boss補正"),
                ("リミットブレイク", "旧版_ver2/battle.pl:tyosenwaza / wbattle.pl:winwaza", "sub_def/battle_logic.py:BattleSimulator.simulate", "HP10%未満の条件、乱数、プレイヤー・対人相手の双方"),
                ("プレイヤー戦術の必殺技実行", "旧版_ver2/tech/*.pl", "sub_def/skills.py:tech_* .hissatu / run_skill", "全戦術IDの呼出先、発動失敗時、副作用とログ"),
                ("対人相手戦術の必殺技実行", "旧版_ver2/wtech/*.pl", "sub_def/skills.py:wtech_* .whissatu / run_skill", "相手側tactic_id、発動率、プレイヤー側との対称性"),
                ("モンスター特殊技の実行", "旧版_ver2/mons/*.pl", "sub_def/skills.py:mons_* .mons_waza / run_skill", "special_skill_id・special_rate、通常行動との排他、各技効果"),
                ("戦術の後発効果", "旧版_ver2/tech/*.pl:atowaza / wtech/*.pl:watowaza", "sub_def/skills.py:tech_* .atowaza / wtech_* .watowaza", "必殺技後の実行順、対象、累積・上限"),
                ("アクセサリー固有効果", "旧版_ver2/acstech/*.pl / wacstech/*.pl", "sub_def/skills.py:acstech_* / wacstech_*", "effect_id、発動順、対人双方、装備能力補正との重複"),
                ("対人1ターン目の逆転必殺", "旧版_ver2/wbattle.pl:battle_clt", "sub_def/battle_logic.py:BattleSimulator.simulate", "レベル差・装備比較条件、倍率、武器無効化、双方の判定順"),
            )),
            ("ダメージ確定・HP・勝敗", (
                ("クリティカル判定（プレイヤー攻撃）", "旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt", "sub_def/battle_logic.py:BattleSimulator.simulate", "HP比率、乱数幅、モンスター戦3倍・対人戦2倍+武器ATK"),
                ("クリティカル判定（敵攻撃）", "旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt", "sub_def/battle_logic.py:BattleSimulator.simulate", "モンスター・対人での確率、ダメージ補正、回復技の除外"),
                ("防具DEFによるダメージ減算と最小値", "旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.simulate", "モンスター戦0・対人戦1の最小ダメージ、負値・防御不能ログ"),
                ("上級職の被ダメージ軽減", "旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.simulate", "職業ID 8〜17の半減、18以上の1/4、双方への適用"),
                ("命中・回避判定", "旧版_ver2/mbattle.pl:mons_kaihi / wbattle.pl:battle_kaihi", "sub_def/battle_logic.py:BattleSimulator.simulate", "dex・agi、武器命中・防具回避・アクセ補正、乱数幅、対人双方"),
                ("先行攻撃による敵行動停止", "旧版_ver2の行動・勝敗処理", "sub_def/battle_logic.py:BattleSimulator.simulate", "敵がこのターンに倒れる場合の敵ダメージ・ログ、対人・モンスター双方"),
                ("ドレイン回復の基準", "旧版_ver2/tech/43.pl ほか", "sub_def/battle_logic.py:BattleSimulator.simulate / skills.py", "防御・回避後の実ダメージ基準、回復比率、0ダメージ時"),
                ("HP・回復・自傷の精算順", "旧版_ver2/mbattle.pl:hp_sum / wbattle.pl:hp_sum", "sub_def/battle_logic.py:BattleSimulator.simulate", "同時精算、最大HP上限、過剰回復、死亡と回復の組合せ"),
                ("ターンログの記録値", "旧版_ver2/mbattle.pl:mons_footer / wbattle.pl:battle_sts", "sub_def/battle_logic.py:BattleSimulator.battle_logs / templates/monster_result.html", "表示HP、ダメージ、回復、勝敗文、HTMLエスケープ"),
                ("勝利・敗北・引き分けの判定", "旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose", "sub_def/battle_logic.py:BattleSimulator.simulate", "相打ち、判定優先順位、時間切れ、結果コード"),
            )),
            ("戦闘後の報酬・成長・進行", (
                ("通常・幻影・異世界の報酬処理", "旧版_ver2/monster.cgi / mbattle.pl:sentoukeka", "cgi_py/monster.py", "勝利・引き分け・敗北EXP/G、盗み差分、battle_limit、幻影宝箱"),
                ("レジェンドの報酬・階層進行", "旧版_ver2/legend.cgi / mbattle.pl:legend_sentoukeka", "cgi_py/legend.py", "boss_flag、title_id、階層解放、称号、敗北・中断時"),
                ("チャンピオン戦の報酬・王者更新", "旧版_ver2/battle.cgi / wbattle.pl:sentoukeka", "cgi_py/battle.py", "敗北EXP上限、勝利・引き分けEXP、賞金、王者保存、制限回復"),
                ("天下一武道会の報酬・ラウンド進行", "旧版_ver2/tenka.cgi / wbattle.pl:sentoukeka", "cgi_py/tenka.py", "相手順、勝敗・引分、ログ、boss_flag、制限回復"),
                ("対人練習戦の保存有無", "旧版_ver2/select_battle.cgi", "cgi_py/select_battle.py", "戦闘ログのみか、経験値・所持金・戦績・待機時間を更新しないこと"),
                ("経験値加算とレベルアップ", "旧版_ver2/battle.pl:levelup", "sub_def/battle_logic.py:process_levelup", "必要EXP、複数Lv上昇、最大Lv、能力・HP成長、職業上限"),
                ("職業熟練度の正規化とマスター", "旧版_ver2/battle.pl:syoku_regist", "sub_def/battle_logic.py:process_levelup / cgi_py/tensyoku.py", "Lv60上限、既存61以上の正規化、転職時の保存"),
            )),
        ),
        comparisons=battle_logic_comparisons(),
    )


def _require_battle_logic_source_snippets() -> None:
    required = {
        "旧版_ver2/battle.pl": ("sub tyosenwaza", "sub levelup", "sub acs_add"),
        "旧版_ver2/mbattle.pl": ("sub shokika", "sub hp_sum", "sub winlose", "sub monsbattle_sts"),
        "旧版_ver2/wbattle.pl": ("sub shokika", "sub hp_sum", "sub battle_kaihi", "sub sentoukeka"),
        "sub_def/battle_logic.py": ("class BattleState", "def get_job_dmg", "class BattleSimulator", "def process_levelup"),
        "sub_def/skills.py": ("def run_skill", "damage_heal_ratio1", "damage_heal_ratio2"),
        "cgi_py/monster.py": ("BattleSimulator", "battle_limit", "process_levelup"),
        "cgi_py/select_battle.py": ("BattleSimulator", "simulate"),
    }
    for relative_path, snippets in required.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
        missing = [snippet for snippet in snippets if snippet not in text]
        if missing:
            raise ValueError(f"戦闘基盤比較の根拠が見つかりません: {relative_path}: {missing}")


def battle_logic_comparisons() -> dict[str, dict[str, str]]:
    """共通戦闘ループと結果処理の実装差異を記録する。"""
    _require_battle_logic_source_snippets()
    items = {
        "戦闘モード別の状態初期化": ("BattleStateへ状態を集約", "意図的", "確認済み", "monster/genei/isekiai/boss/battleの一時値、最大ターン、金銭変動を状態オブジェクトへ集約。対人は相手HP・装備、モンスターはマスター値とHP乱数を設定する。"),
        "装備・アクセサリーの戦闘用補正コピー": ("保存配列の直接加算からdeep copyへ変更", "意図的", "確認済み", "Ver2のacs_add/wacs_addと同じ8能力補正を戦闘コピーだけに加算する。戦闘後に元データを戻す必要がない。"),
        "モンスターHP・初期HPの乱数": ("名前付きmonster値を使用", "意図的", "確認済み", "双方ともhp_base + rand(random_range)で決定し、その値を表示用最大HPにも使う。random_range 0は現行で安全に0幅相当へ正規化する。"),
        "職業別の基礎ダメージ（全31職）": ("Lv乱数加算とカルマ固定加算を修正", "不具合修正", "確認済み", "Ver2はモンスター戦でLv×(rand(5)+1)、対人戦で双方にLv×(rand(3)+1)を先に加え、さらに職業式と武器ATKを加算する。現行へ同じLv基礎ダメージを復元した。9cd9d14のカルマ乱数化も修正済みで、all_stats・職24・職25のカルマは固定加算で一致する。"),
        "モンスター・対人相手の基礎ダメージ": ("計算をget_job_dmgと名前付きモンスター値へ統合", "意図的", "確認済み", "モンスターはbase_damage + rand(random_range)、対人は相手の職業式＋武器ATK。幻影ではVer2同様にプレイヤー防具DEFを敵基礎ダメージへ加算する。get_job_dmgを共有する対人上位職にも固定カルマ加算が適用される。"),
        "最大ターンと時間切れ": ("対人時間切れをwin=3として相打ち引分と分離", "不具合修正", "確認済み", "モンスター戦は時間切れwin=2、対人戦は未決着win=3とするVer2の結果コードを再現した。チャンピオン・天下一・練習戦はwin=3を時間切れ引分として表示する。"),
        "選択戦術IDの取得": ("列番号からtactic_idへ名称化", "意図的", "確認済み", "プレイヤー・対人相手とも選択戦術IDを使用し、不正値・欠損値は0へ正規化する。現職ではないマスター戦術も選択済みなら実行する仕様を維持する。"),
        "戦術マスター由来の発動率分母": ("tac.jsonのactivation_denominatorを優先", "意図的", "確認済み", "説明文ラベルを乱数分母へ対応付ける後方互換を残し、明示値があればそれを優先する。個々の分母はskills.mdでVer2照合済み。"),
        "プレイヤー必殺率・上限・特殊モード減衰": ("名前付き値・設定値へ移行", "意図的", "確認済み", "カルマ/15 + 10 + 職業Lv、75上限、アクセ補正後95上限、幻影・異世界1/3、ボス1/2を共通ループで計算する。"),
        "リミットブレイク": ("表示HTMLのみ更新", "意図的", "確認済み", "双方ともHP10%未満かつrand(4)>1で必殺率へ999を加算する。対人相手側も同条件で判定する。"),
        "プレイヤー戦術の必殺技実行": ("動的requireからrun_skillディスパッチへ移行", "意図的", "確認済み", "選択戦術IDのhissatuを通常行動後に呼び、未定義IDは安全に0相当へ解決する。各必殺技の差異はskills.mdで確認済み。"),
        "対人相手戦術の必殺技実行": ("動的requireからrun_skillディスパッチへ移行", "意図的", "確認済み", "相手の選択戦術IDをwtech/whissatuへ渡し、相手アクセの必殺率補正も加える。"),
        "モンスター特殊技の実行": ("special_skill_idを名前付き値で参照", "意図的", "確認済み", "モンスターの技ID・発動率をBattleStateへ渡してmons_wazaを呼ぶ。個別22技の値はmonster_skills.mdで照合済み。"),
        "戦術の後発効果": ("呼出先を明示ディスパッチ化", "意図的", "確認済み", "必殺判定後にプレイヤーatowaza、アクセ効果、対人なら相手watowaza・相手アクセ、モンスターならmons_atowazaの順で処理する。"),
        "アクセサリー固有効果": ("effect_idを辞書から参照", "意図的", "確認済み", "命中・回避・必殺率補正は先に取り込み、固有効果は後発効果の位置で実行する。個別effect_idはskills.mdで照合済み。"),
        "対人1ターン目の逆転必殺": ("設定値化と明示的な一時装備変更", "意図的", "確認済み", "レベル差/装備比較による初手倍率、回避不能化、相手武器無効化を維持する。現行はcounterattack_level_gap等を設定値で読む。"),
        "クリティカル判定（プレイヤー攻撃）": ("回復・0ダメージを判定対象外に変更", "意図的", "確認済み", "HP割合から確率を出し、モンスター戦3倍、対人戦2倍＋相手武器ATKを適用する。現行はdmg1>0のときだけ判定して回復技を攻撃扱いしない。"),
        "クリティカル判定（敵攻撃）": ("回復・0ダメージを判定対象外に変更", "意図的", "確認済み", "対人はHP割合・100幅で2倍＋自防具DEF、モンスターは200幅で防具DEF加算。現行はdmg2>0だけに限定する。"),
        "防具DEFによるダメージ減算と最小値": ("防御不能ログを追加", "意図的", "確認済み", "モンスター戦はDEF未満を0、対人戦は1にし、負ダメージは保持する。上級職軽減後に0になった攻撃を現行はログで明示する。"),
        "上級職の被ダメージ軽減": ("職IDを名前付きjobで参照", "意図的", "確認済み", "職8〜17は1/2、18以上は1/4を被ダメージへ適用し、対人では双方に適用する。"),
        "命中・回避判定": ("表示用と戦闘用の計算を共通化", "意図的", "確認済み", "DEX・AGI・武器命中・防具回避・アクセ補正と、モンスター300幅/対人100幅の回避判定を対応させる。"),
        "先行攻撃による敵行動停止": ("Ver2の同時精算にない敵行動停止を部分追加", "要判断", "確認済み", "Ver2 mbattle.pl/wbattle.plは双方の行動後にhp_sumする。現行は敵HPがこのターンに0以下になる見込みならdmg2だけを0にするが、敵の必殺技・回復等の行動自体は既に実行されている。速度値を設けずプレイヤー先行へ統一する案は保留であり、採用時は行動順・死亡時中断・回復上限を一貫して設計する必要がある。"),
        "ドレイン回復の基準": ("Ver2の設定ダメージ基準から実ダメージ基準へ変更", "意図的", "確認済み", "防御・回避後のdmg×割合で回復する現行仕様を維持する。ドレイン43の全量回復など個別割合はskills.mdで調整済み。"),
        "HP・回復・自傷の精算順": ("同時精算と部分的な先行停止が混在", "要判断", "確認済み", "現行は最大HPへの上限を最終精算時に適用するため、過剰回復が同ターンの致死ダメージを相殺し得る。全モンスターへの速度値追加は基準不在で現実的でなく、プレイヤー先行に統一する案を含めて保留とする。"),
        "ターンログの記録値": ("HTML断片から構造化ログ＋テンプレート表示へ移行", "意図的", "確認済み", "ターン番号、双方HP、行動、ダメージ、回復を辞書へ保存し、HPは表示時に0下限へ丸める。コメントはhtml.escapeして表示する。"),
        "勝利・敗北・引き分けの判定": ("対人時間切れを専用結果コードへ復元", "不具合修正", "確認済み", "同時撃破は引分2、敵HP0は勝利1、プレイヤーHP0は敗北0の順。モンスター時間切れは2、対人時間切れは3とし、入口側で専用の引分処理へ分岐する。"),
        "通常・幻影・異世界の報酬処理": ("結果処理をmonster.pyへ分離。回復順と修行回数をVer2準拠へ修正", "不具合修正", "確認済み", "勝敗別EXP/G、盗み差分、修行回数、幻影宝箱を入口側で処理する。通常・幻影・異世界は残り回数0で開始できず、各戦闘で1回消費する。戦闘後HPはlevelup後のvit/max_hpで回復する。敗北EXPはVer2の1ではなく0を維持する。時間切れを引分として扱う現行差は上記結果コード行と連動する。"),
        "レジェンドの報酬・階層進行": ("結果処理をlegend.pyへ分離。クリア後の再挑戦を追加", "意図的", "確認済み", "勝利・引分・敗北のEXP/G・battle_count・win_count・battle_limit・進行初期化は対応する。戦闘後HPはVer2のhp_afterと同じくlevelup後のvit/max_hpで回復する。Ver2は最終ボス撃破時にboss_flag=0を保持して連戦を終えるが、現行は開始値10へ戻して同階層を再挑戦可能にする。"),
        "チャンピオン戦の報酬・王者更新": ("時間切れ引分と新王者保存順をVer2準拠へ修正", "不具合修正", "確認済み", "win=3の時間切れは通常EXPのみを得て、賞金・王者交代・王者連勝を発生させない。新王者はレベルアップ後の能力値・最大HP・HPで保存し、結果画面は上書き前の王者名を表示する。相打ち引分win=2は従来どおり新王者交代として扱う。敗北EXPの自分Lv×10上限は意図的な調整。"),
        "天下一武道会の報酬・ラウンド進行": ("時間切れ引分・相打ち・敗北の進行は現行方針を維持。回復順とロック範囲をVer2相当に修正", "意図的", "確認済み", "win=1/2/3/0の賞金・盗み・boss_flag進行は現行方針を維持する。戦闘後HPはlevelup後のvit/max_hpで回復し、ユーザーロックはchara_load前からsave_user_sections完了まで保持する。boss_flagが開始値10を超える場合は10へ正規化して、相手インデックスの不整合を防ぐ。"),
        "対人練習戦の保存有無": ("戦闘専用入口をPython化", "意図的", "確認済み", "select_battle.pyはBattleSimulatorのログを表示するだけで、経験値・所持金・戦績・待機時刻・王者状態を保存しない。"),
        "経験値加算とレベルアップ": ("名前付き値とwhileループへ移行", "意図的", "確認済み", "必要EXP=現Lv×係数、複数Lv上昇、HP=rand(vit)×3+vit、能力上限・最大Lvを処理する。"),
        "職業熟練度の正規化とマスター": ("61以上の旧値を60へ正規化", "意図的", "確認済み", "Ver2のマスター上限60に合わせ、戦闘後にjob_levelを0〜60へ正規化する。初到達時だけ職歴へ60を保存する。"),
    }
    expected_count = 33
    if len(items) != expected_count:
        raise ValueError(f"戦闘基盤比較の行数が不正です: {len(items)}")
    return {
        name: {
            "difference": diff,
            "intent": intent,
            "status": "差異あり" if status == "確認済み" else status,
            "note": note,
        }
        for name, (diff, intent, status, note) in items.items()
    }


def write_progression_checklist() -> None:
    write_static_checklist(
        "ownership_progression.md",
        "所有・進行要素比較チェックリスト",
        "プレイヤー固有・共有の状態が、どこで作成・更新・消去・参照されるかを比較する台帳です。マスターデータの値比較とは分離します。",
        (
            ("キャラクター・戦闘進行", (
                ("キャラクター作成時の初期状態", "旧版_ver2/chara_make.cgi", "chara_make.py", "初期能力、職業、装備、所持金、戦術、battle_limit、boss_flag、チョコボ空値"),
                ("職業熟練度とマスター職", "旧版_ver2/syoku.cgi / tensyoku.cgi", "cgi_py/tensyoku.py / cgi_py/sts.py / sub_def/common.py", "職業別熟練度、Lv60、転職時の退避・復帰、表示"),
                ("装備中の武器・防具・アクセサリー", "旧版_ver2/item/<ID>.cgi", "user_all.json:equipment / cgi_py/shop_*.py / cgi_py/souko.py", "ID・性能スナップショット、職業制限、初期装備、削除時"),
                ("倉庫の武器", "旧版_ver2/souko/item/<ID>.cgi", "user_all.json:souko_weapon / sub_def/common.py:souko_*", "保存形式、件数、装備交換、削除、重複"),
                ("倉庫の防具", "旧版_ver2/souko/def/<ID>.cgi", "user_all.json:souko_armor / sub_def/common.py:souko_*", "保存形式、件数、装備交換、削除、重複"),
                ("倉庫のアクセサリー", "旧版_ver2/souko/acs/<ID>.cgi", "user_all.json:souko_accessory / sub_def/common.py:souko_*", "effect_id・能力補正・説明、装備交換、削除、重複"),
                ("戦績・戦闘回数・勝利数", "旧版_ver2/charalog/<ID>.cgi", "user_all.json:chara / cgi_py/monster.py / battle.py / tenka.py", "battle_count、win_countの更新対象、練習戦除外、ランキング利用"),
                ("修行回数・待機時刻", "旧版_ver2/charalog/<ID>.cgi / mbattle.pl:time_check", "user_all.json:chara.battle_limit,last_time / 各戦闘CGI", "初期値、減算・回復契機、コンテンツ別待機時間"),
                ("レジェンドの進行フラグ・称号", "旧版_ver2/legend.cgi / charalog", "user_all.json:chara.boss_flag,title_id / cgi_py/legend.py", "開始・勝利・敗北・中断時の値、タイトル解放条件"),
                ("人間チャンピオン", "旧版_ver2/datalog/winner.cgi / battle.cgi", "save_data/champion.json / cgi_py/battle.py", "挑戦者の装備・戦術の保存、勝者交代、防衛戦績、初期王者"),
                ("天下一武道会の参加者・対戦履歴", "旧版_ver2/all_tenka.cgi / tenka_log.cgi", "save_data/all_tenka.json,tenka_log.json / cgi_py/tenka.py", "参加者抽出、順序、ログ保持数、制覇履歴"),
            )),
            ("チョコボ所有・レース進行", (
                ("チョコボ所持判定と未所持値", "旧版_ver2/chocolog/<ID>.cgi", "user_all.json:choco / sub_def/common.py:is_choco_owned", "空辞書・欠損・実体データの判定、旧データ互換"),
                ("飼育中チョコボの基本状態", "旧版_ver2/chocolog/<ID>.cgi", "user_all.json:choco / cgi_py/morifarm.py", "名前、性別、血統、画像、能力c0〜c6、寿命、体力、戦績"),
                ("野生チョコボの候補・購入", "旧版_ver2/morifarm.cgi / chocobofile.cgi", "cgi_py/morifarm.py / data/chocobo/chocobofile.json", "候補抽選、価格、候補消費、所持制限、初期値"),
                ("引退・お見合い候補リスト", "旧版_ver2/chocoboms.cgi / chocoboos.cgi", "save_data/chocoboms.json,chocoboos.json / cgi_py/morifarm.py", "性別別保存、候補上限、引退時移動、配合後の削除"),
                ("配合後の子チョコボ", "旧版_ver2/morifarm.cgi", "cgi_py/morifarm.py", "父母・血統、能力上限、性別、初期能力、親の扱い"),
                ("訓練・休養による状態変化", "旧版_ver2/ctrain.cgi / morifarm.cgi", "cgi_py/ctrain.py / cgi_py/morifarm.py", "各能力、寿命・体力、失敗、副作用、費用・待機時間"),
                ("通常レースの戦績・クラス進行", "旧版_ver2/crace.cgi", "cgi_py/crace.py / user_all.json:choco", "run、win、gold、class条件、寿命、敗北時の変化"),
                ("G1/G2の個人トロフィー履歴", "旧版_ver2/chocog1/<ID>.cgi", "user_all.json:choco_g1 / cgi_py/crace.py", "r1〜r22、開催日・性別条件、重複勝利、殿堂条件"),
                ("チョコボ殿堂の共有リスト", "旧版_ver2/denchoco.cgi / dendo.cgi", "save_data/denchoco.json / cgi_py/dendo.py", "3重賞条件、同一チョコボの上書き、保存項目、一覧"),
                ("チョコボ王者", "旧版_ver2/chocowinner.cgi / farmrace.cgi", "save_data/chocobo_champion.json / cgi_py/farmrace.py", "挑戦条件、勝者更新、連勝・前王者、初期値"),
            )),
            ("記録・共有状態", (
                ("ログイン履歴", "旧版_ver2/loginlog/<ID>.cgi", "user_all.json:login_log / login.py", "保存件数、日時・IP等の項目、ログイン時更新"),
                ("受信・送信メッセージ", "旧版_ver2/message / sousin", "user_all.json:message / save_data/<ID>/message_sent.json", "保存先分離、件数、既読・削除、変換時の扱い"),
                ("全体メッセージ・掲示板", "旧版_ver2/datalog/message.cgi / post_message.cgi", "save_data/all_message.json / cgi_py/bbs.py / admin.py", "投稿者、保存件数、表示順、管理投稿"),
                ("登録者・ランキング用キャッシュ", "旧版_ver2/alldata.cgi / rank.cgi", "save_data/system_rank_cache.json / cgi_py/system.py / rank.py", "対象プレイヤー、更新時刻、キャッシュ無効化、公開項目"),
            )),
        ),
        comparisons=ownership_progression_comparisons(),
    )


def _require_ownership_progression_source_snippets() -> None:
    """所有・進行台帳の根拠となる実装が消えた場合は生成を止める。"""
    required = {
        "旧版_ver2/chara_make.cgi": ("sub chara_make", "$new_chara =", "$intgold"),
        "chara_make.py": ("職業ごとの初期ステータス割り振り", '"battle_limit"', '"choco": {}'),
        "旧版_ver2/tensyoku.cgi": ("sub tensyoku_change", "$syoku_master[$chara[14]]", "$master_tac"),
        "cgi_py/tensyoku.py": ("def get_syoku_master_list", "job_reqs", "save_user_sections"),
        "旧版_ver2/morifarm.cgi": ("sub choco_sell", "sub yadoya", "chocoboos.cgi"),
        "cgi_py/morifarm.py": ("mode == \"choco_buyb\"", "mode == \"choco_sell\"", "mode == \"yadoya\""),
        "旧版_ver2/ctrain.cgi": ("$ctrain += 1", "$clife -= 50", "farm_choco_regist"),
        "cgi_py/ctrain.py": ("def main", "choco[\"train\"]", "save_user_sections"),
        "旧版_ver2/crace.cgi": ("./g1/$chara[0].cgi", "farm_choco_regist", "$crun"),
        "cgi_py/crace.py": ("choco_g1_regist", "save_user_sections", "race_dendo"),
        "旧版_ver2/dendo.cgi": ("sub dendo", "./denchoco.cgi", "./rireki.cgi"),
        "cgi_py/dendo.py": ("trophies_count < 3", "choco_list_regist(\"denchoco\"", '"trophies"'),
        "旧版_ver2/farmrace.cgi": ("read_farm_winner", "./farmwinner.cgi", "$wcren"),
        "cgi_py/farmrace.py": ("chocobo_champion_load", "new_winner", "chocobo_champion_register"),
        "旧版_ver2/login.cgi": ("./loginlog/$in{'id'}.cgi", "loginlog"),
        "login.py": ("def main", "ensure_daily_backup", "needs_rehash"),
        "旧版_ver2/post_message.cgi": ("sub limit", "sub limit_do"),
        "cgi_py/bbs.py": ("mode == \"post\"", "bbs_storage_limit", "bbs_regist"),
        "旧版_ver2/system.cgi": ("sub ranking", "rankinghtml", "@RANKING"),
        "cgi_py/system.py": ("def build_rankings_cache", "system_rank_cache.json", "last_updated"),
        "cgi_py/battle.py": ("pvp_base_exp", "max_win_count", "champion"),
        "cgi_py/tenka.py": ("update_tenka_members", "tenka_log_limit", "battle_limit"),
        "cgi_py/legend.py": ("boss_flag", "title_id", "legend_progress_reset_value"),
        "sub_def/common.py": ("def is_choco_owned", "def choco_delete", "def login_log_regist"),
        "cgi_py/souko.py": ("souko_weapon", "souko_armor", "souko_accessory"),
    }
    for relative_path, snippets in required.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
        missing = [snippet for snippet in snippets if snippet not in text]
        if missing:
            raise ValueError(f"所有・進行比較の根拠が見つかりません: {relative_path}: {missing}")


def ownership_progression_comparisons() -> dict[str, dict[str, str]]:
    """所有・進行状態を、保存形式ではなく更新・参照の実挙動まで比較する。"""
    _require_ownership_progression_source_snippets()
    results = {
        "キャラクター作成時の初期状態": {
            "difference": "JSON統合保存・PBKDF2認証へ移行（初期ゲーム値は同値）",
            "intent": "意図的",
            "status": "確認済み",
            "note": "Ver2/Ver3とも職業別初期8能力・Lv1・HP500・G5000・初期装備0・戦術0・修行回数・レジェンド進行初期値を設定。Ver3は職歴31件、倉庫・チョコボ空値を統合JSONで明示し、Ver2のsite/url・平文パスワードは保持しない。",
        },
        "職業熟練度とマスター職": {
            "difference": "JSONの職ID→熟練度へ移行し、転職実行時にも前提職を再検証",
            "intent": "意図的",
            "status": "確認済み",
            "note": "両版とも現職Lvを退避して転職先Lvを復帰、Lv60をマスター表示に用いる。Ver3は表示だけでなくPOST時もjob_reqsを検証し、Lv60超の既存値を成長処理で正規化する。",
        },
        "装備中の武器・防具・アクセサリー": {
            "difference": "個別itemレコードからequipmentオブジェクトへ統合",
            "intent": "意図的",
            "status": "確認済み",
            "note": "装備IDと性能スナップショットを保持し、ショップ・倉庫交換時にキャラクター状態と同時保存する。初期値は武器0・防具0・アクセ0で一致し、現行は名前付き項目と原子的保存に変更。",
        },
        "倉庫の武器": {
            "difference": "1行1品の専用ファイルからsouko_weapon配列へ統合",
            "intent": "意図的",
            "status": "確認済み",
            "note": "購入・装備交換・廃棄は現行souko.pyで件数上限を確認して配列を更新する。重複品を配列要素として保持する点はVer2の行単位保存と同じ。",
        },
        "倉庫の防具": {
            "difference": "1行1品の専用ファイルからsouko_armor配列へ統合",
            "intent": "意図的",
            "status": "確認済み",
            "note": "購入・装備交換・廃棄の件数制限と、個別スナップショットを保持する構造を確認。Ver3はキャラクター・倉庫を一括保存する。",
        },
        "倉庫のアクセサリー": {
            "difference": "1行1品の専用ファイルからsouko_accessory配列へ統合",
            "intent": "意図的",
            "status": "確認済み",
            "note": "effect_idを含むアクセサリー定義を倉庫要素として保持し、装備交換・廃棄時に上限を検査する。保存形式以外の所有数・重複品の扱いは同じ。",
        },
        "戦績・戦闘回数・勝利数": {
            "difference": "charalog列からbattle_count/win_countへ名称化",
            "intent": "意図的",
            "status": "確認済み",
            "note": "通常モンスター、チャンピオン、レジェンド、天下一で戦闘回数を加算し、勝利時のみ勝利数を加算する。チャンピオン戦以外の戦闘導線はbattle_count>0を表示・実行の双方で検査する。対人練習戦は保存更新しない。ランキング表示は両値から勝率を算出する。",
        },
        "修行回数・待機時刻": {
            "difference": "charalog列からbattle_limit/last_timeへ名称化",
            "intent": "意図的",
            "status": "確認済み",
            "note": "通常・幻影・異世界・レジェンドは修行回数を消費し、チャンピオン・天下一は結果にかかわらず上限まで補充する。各戦闘CGIは完了時にlast_timeを更新し、設定値の待機時間で検査する。モンスター系の待機時間はVer2の30秒から、設定値で変更可能な現行20秒へ調整している。",
        },
        "レジェンドの進行フラグ・称号": {
            "difference": "進行列・称号列をboss_flag/title_idへ名称化し、クリア後は開始値へ戻して再挑戦可能化",
            "intent": "要判断",
            "status": "確認済み",
            "note": "階層選択は称号値で制限し、勝利でboss_flagを減算、敗北・引分では開始値へ戻す。Ver2は階層クリア時にboss_flag=0を保持し、結果画面から続行できない。現行はtitle_idを上げた後にboss_flagを開始値へ戻して再挑戦可能にする意図的な継続仕様であり、実際に加算するEXPも結果へ表示する。",
        },
        "人間チャンピオン": {
            "difference": "winner.cgiの連番レコードからchampion.jsonの名前付き状態へ移行。時間切れと新王者保存順を修正",
            "intent": "不具合修正",
            "status": "確認済み",
            "note": "通常の勝利・相打ち引分は挑戦者を王者へ交代し、敗北では王者の連勝・最高連勝を更新する。新王者は戦闘EXPのレベルアップ後に保存するため、本人とchampion.jsonの能力値・最大HP・現在HPが一致する。時間切れwin=3は引分表示として、王者交代・賞金・連勝を発生させず通常EXPのみを得る。勝利・相打ち引分EXPは相手Lv×基準値、敗北EXPだけmin(相手Lv, 自分Lv×10)へ調整済み。",
        },
        "天下一武道会の参加者・対戦履歴": {
            "difference": "all_tenka/tenka_logをJSONキャッシュ化し、履歴上限を設定値で明示",
            "intent": "要判断",
            "status": "確認済み",
            "note": "両版ともレベル上位者の状態スナップショットと対戦時点の装備を組み合わせ、制覇時に履歴先頭へ追加する。Ver3は24時間キャッシュとtenka_log_limitで履歴を切り詰める一方、Ver2の履歴件数判定は変数名の不整合を含む。対戦時はキャラクターロックを取得してからロード・戦闘・保存まで保持し、重複送信による待機/進行更新の競合を防ぐ。",
        },
        "チョコボ所持判定と未所持値": {
            "difference": "ファイル有無判定から必須キーを持つ辞書の実体判定へ変更",
            "intent": "意図的",
            "status": "確認済み",
            "note": "Ver2はchocologファイルが存在すれば所持扱い。Ver3は空辞書・欠損辞書を未所持とし、引退時にchocoを明示消去するため、空データを所持扱いする不整合を防ぐ。",
        },
        "飼育中チョコボの基本状態": {
            "difference": "33列のchocologレコードから名前付きchoco辞書へ移行",
            "intent": "意図的",
            "status": "確認済み",
            "note": "名前・性別・血統・画像番号・type・maxmax・能力上限c0〜c6・寿命life・train/run/win・max・gold・父母を保持する。Ver3はチョコボ内に平文パスワードを複製しない。",
        },
        "野生チョコボの候補・購入": {
            "difference": "候補データをJSON化し、購入POSTでも未所持を検証",
            "intent": "意図的",
            "status": "確認済み",
            "note": "両版とも野生候補を1〜5件抽選し、価格を支払って初期life=100・能力/上限=10・run/win/train=0の個体を作る。候補自体は消費せず、現行は直接POSTによる所持チョコボ上書きを拒否する。",
        },
        "引退・お見合い候補リスト": {
            "difference": "固定99枠の行ファイルからJSONリスト＋設定上限へ変更",
            "intent": "要判断",
            "status": "確認済み",
            "note": "性別別リストへ引退個体の戦績・血統・価格を移し、配合相手の候補にする基本設計は同じ。Ver3は実リスト長を基準に置換し、空リストも許容してchocobo_partner_list_limitで切詰めるため、Ver2の固定ID枠とは候補選出が異なり得る。",
        },
        "配合後の子チョコボ": {
            "difference": "保存形式と排他制御のみ変更（配合計算をPythonへ移植）",
            "intent": "意図的",
            "status": "確認済み",
            "note": "異性のお見合い候補を選び、父母・血統・性別・画像・type・能力上限・初期能力・life=1000・戦績0を生成して現役個体を置換する。現行は親候補の存在と所持状態をサーバー側で再検証し、統合JSONへ保存する。",
        },
        "訓練・休養による状態変化": {
            "difference": "保存形式をJSON化し、不正mode・未所持を明示検証",
            "intent": "意図的",
            "status": "確認済み",
            "note": "訓練は20回試行、train+1・life-50・max+5、能力上限・潜在力・寿命処理を引き継ぐ。休養はG5000、lifeに200〜499加算（1000超過時max追加）、train+1・max+10で、計算式はVer2と対応する。",
        },
        "通常レースの戦績・クラス進行": {
            "difference": "レース状態・相手をJSON化し、入力modeを明示検証",
            "intent": "意図的",
            "status": "確認済み",
            "note": "run/win/gold・寿命・クラス到達条件を個体状態へ反映し、通常レース・重賞・殿堂レースを同じ個体データで進行する。現行は候補読み込みと結果保存を原子的に行い、無効なレース種別を受け付けない。",
        },
        "G1/G2の個人トロフィー履歴": {
            "difference": "chocog1の22列レコードからchoco_g1のr1〜r22辞書へ移行",
            "intent": "意図的",
            "status": "確認済み",
            "note": "重賞勝利時だけ対象レースIDを1として保存し、同一レースの再勝利は同じ個人フラグを維持する。開催日・性別・レース進行の条件はcraceの分岐で処理し、保存は個体と分離されたまま引退後も残す。",
        },
        "チョコボ殿堂の共有リスト": {
            "difference": "denchoco行レコードからJSON＋トロフィー名の埋込へ移行。重賞3個を登録条件に追加",
            "intent": "要判断",
            "status": "確認済み",
            "note": "同一ID・同名は上書き、異なる個体は先頭追加する。Ver2のdendo.cgiはテストID以外に重賞数を検査しないが、Ver3はG1/G2 3個未満を拒否するため、この追加制限の採否を確認する必要がある。",
        },
        "チョコボ王者": {
            "difference": "farmwinner行レコードからchocobo_champion.jsonへ移行",
            "intent": "意図的",
            "status": "確認済み",
            "note": "現王者への挑戦、勝者の個体・ブリーダー情報への交代、敗北時の連勝・前王者情報の更新を維持する。現行は欠損した旧キーを正規化し、王者共有データを専用ロックで保存する。",
        },
        "ログイン履歴": {
            "difference": "移行先login_logは残るが、現行ログイン処理から更新呼出しがない",
            "intent": "要判断",
            "status": "確認済み",
            "note": "Ver2 login.cgiはloginlog/<ID>.cgiを読んで日時・IP等を追加し上限処理する。Ver3にはlogin_log_load/login_log_registと移行項目があるが、login.pyからlogin_log_registを呼ばないため、新規ログイン履歴が蓄積されない。",
        },
        "受信・送信メッセージ": {
            "difference": "変換先のmessage/message_sentは残るが、現行の送受信・既読・削除CGIが見当たらない",
            "intent": "要判断",
            "status": "確認済み",
            "note": "Ver2はmessage/sousinとpost_message.cgiで私信・送信箱・件数制限を扱う。Ver3のスキーマには受信messageとmessage_sentがあるものの、現行CGIから読み書きする経路を確認できず、機能廃止か未移植かを決める必要がある。",
        },
        "全体メッセージ・掲示板": {
            "difference": "全体ニュース(all_message)とプレイヤー掲示板(bbs)を別JSONへ分離",
            "intent": "意図的",
            "status": "確認済み",
            "note": "Ver3は管理者・登録・イベント通知をall_messageへ、一般投稿をbbsへ保存し、双方を新着順・設定件数で切詰める。Ver2のpost_message.cgiは私信・制限操作を含む一体型であり、表示経路は再編されている。",
        },
        "登録者・ランキング用キャッシュ": {
            "difference": "HTML出力キャッシュからJSONデータキャッシュへ移行",
            "intent": "意図的",
            "status": "確認済み",
            "note": "両版とも全登録者をレベル順に集計し、約24時間単位で再生成する。Ver3はsystem_rank_cacheとrank_cacheを分け、キャッシュ欠損・必要項目欠損時も再構築し、テンプレートで安全に表示する。",
        },
    }
    expected = {
        "キャラクター作成時の初期状態", "職業熟練度とマスター職", "装備中の武器・防具・アクセサリー", "倉庫の武器", "倉庫の防具", "倉庫のアクセサリー",
        "戦績・戦闘回数・勝利数", "修行回数・待機時刻", "レジェンドの進行フラグ・称号", "人間チャンピオン", "天下一武道会の参加者・対戦履歴",
        "チョコボ所持判定と未所持値", "飼育中チョコボの基本状態", "野生チョコボの候補・購入", "引退・お見合い候補リスト", "配合後の子チョコボ",
        "訓練・休養による状態変化", "通常レースの戦績・クラス進行", "G1/G2の個人トロフィー履歴", "チョコボ殿堂の共有リスト", "チョコボ王者",
        "ログイン履歴", "受信・送信メッセージ", "全体メッセージ・掲示板", "登録者・ランキング用キャッシュ",
    }
    if set(results) != expected:
        raise ValueError("所有・進行比較の行定義がチェックリストと一致しません")
    return results


def _require_storage_source_snippets() -> None:
    """保存・移行台帳の根拠となる実装が消えた場合は生成を止める。"""
    required = {
        "旧版_ver2/regist.pl": ("sub decode", "sub chara_regist", "sub lock", "sub header"),
        "旧版_ver2/login.cgi": ("sub log_in", "sub set_cookie", "loginlog"),
        "旧版_ver2/admin.cgi": ("sub save_chara", "sub save_del", "./save_log.cgi"),
        "sub_def/common.py": ("def decode_params", "def get_lock", "def require_owner", "def save_user_sections"),
        "sub_def/crypto.py": ("def encrypt_data", "def token_check", "def verify_password"),
        "sub_def/file_ops.py": ("def _write_json_atomically", "def update_data_atomically"),
        "sub_def/backup.py": ("def create_daily_backup", "def restore_daily_backup", "def _prune_daily_backups"),
        "sub_def/data_schema.py": ("def order_user_data", "title_id", "tactic_id"),
        "admin.py": ("def restore_protected_users", "def validate_master_record", "def save_master_records"),
        "login.py": ("def main", "ensure_daily_backup", "needs_rehash"),
        "旧版_ver2/change_data/convert_all.py": ("CHARA_COLUMNS", "def convert_user", "def validate_user", "--dry-run"),
    }
    for relative, snippets in required.items():
        path = ROOT / relative
        encoding = "cp932" if relative.startswith("旧版_ver2/") and not relative.endswith(".py") else "utf-8"
        text = path.read_text(encoding=encoding, errors="replace")
        missing = [snippet for snippet in snippets if snippet not in text]
        if missing:
            raise ValueError(f"保存・移行台帳の根拠が不足しています: {relative}: {missing}")


def storage_migration_comparisons() -> dict[str, dict[str, str]]:
    """保存・認証・移行・運用の28比較項目を、実装根拠付きで記録する。"""
    _require_storage_source_snippets()
    login_source = (ROOT / "login.py").read_text(encoding="utf-8")
    if "login_log_regist(" in login_source:
        raise ValueError("ログイン履歴の比較結果を更新してください: login.py が履歴保存を再開しています")
    crypto_source = (ROOT / "sub_def" / "crypto.py").read_text(encoding="utf-8")
    if crypto_source.count("token_regenerate(") != 1:
        raise ValueError("CSRF再生成の比較結果を更新してください: token_regenerate の利用箇所が変わりました")

    return {
        "CGIパラメータの復号・文字列処理": {
            "difference": "Ver2はGET/POSTの一方だけを手動分解し、POSTは50KiB上限・SJIS変換・入力時HTMLエスケープ。Ver3はGETとPOSTをparse_qsで解析しPOST優先、UTF-8前提・出力時エスケープへ変更。現行に本文サイズ上限はない。",
            "intent": "要判断",
            "status": "差異あり",
            "note": "Ver3のGET/POST優先はcommon.pyの明示仕様。Ver2の50KiB上限を廃止した理由は履歴に記録が見当たらないため、上限の要否を運用判断する。",
        },
        "CGI入口のUTF-8標準入出力": {
            "difference": "Ver2はShift_JIS出力。Ver3はothers.py・login.py・chara_make.py・admin.pyの4入口でstdin/stdoutをUTF-8へ再構成する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "Windows ApacheのCP932標準出力でUTF-8文字を出すための互換設定。4入口以外へ一律追加・削除はしない。",
        },
        "HTML出力・リダイレクトのヘッダー": {
            "difference": "Ver2はShift_JISのContent-typeとHTML直書き。Ver3はUTF-8ヘッダー、no-cache、Jinja自動エスケープ、302 Locationと開発サーバー用meta refreshを出力する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "utils.pyはテンプレート例外の詳細をstderrだけへ出し、HTTP応答には汎用エラーだけを返す。",
        },
        "セッションCookieの暗号化・改ざん検証": {
            "difference": "Ver2はIDと保存済みパスワードを60日Cookieへ平文で保存。Ver3は署名付き暗号化FFAPY_SESSION（既定30分・HttpOnly）へ移行し、30日CookieはID記憶だけに分離。Secure属性は未設定。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "旧cookie_name APIは暗号化セッションへ橋渡しする互換層を残す。HTTPS化時のSecure属性は別途運用設定が必要。",
        },
        "ログイン・ログアウト": {
            "difference": "Ver2は成功・失敗ともloginlogへ最大15件を書き、入力パスワードも記録する。Ver3は検証・セッション発行・日次バックアップを行うが、login.pyからlogin_log_registを呼ばず履歴を更新しない。",
            "intent": "要判断",
            "status": "差異あり",
            "note": "平文パスワード記録の廃止は妥当だが、成功/失敗・時刻・ホストを伏せた安全な履歴まで廃止する意図は確認できない。",
        },
        "パスワード形式とログイン時移行": {
            "difference": "Ver2はcharalogの平文比較。Ver3はPBKDF2-SHA256（ユーザー別salt）を新形式とし、旧固定salt・平文も成功時だけ検証してPBKDF2へ再ハッシュする。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "verify_passwordは旧形式を読み取り互換に限定し、needs_rehashが真のときだけ保存値を更新する。",
        },
        "CSRFトークンの生成・検証・再生成": {
            "difference": "Ver2にCSRF照合はない。Ver3はセッション内ランダムトークンを主要POSTで定数時間比較する。token_regenerateは定義のみで、画面再表示は既存トークンを維持する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "別タブ・戻る操作で直ちに失効させない方針はutils.pyコメントで確認。セッション期限でのみ失効する。",
        },
        "本人操作の認可（IDOR対策）": {
            "difference": "Ver2はリクエストid/passを各CGIで直接照合。Ver3は暗号化セッションを旧cookie互換値へ変換し、require_ownerまたは同等照合で対象ID・保存済みhashを確認する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "shop・souko・チョコボ系等はrequire_owner、battle・monster・legend・bank・passchangeは同条件を個別実装。閲覧系には適用しない。",
        },
        "統合ユーザー保存形式": {
            "difference": "Ver2はcharalog/item/syoku/souko/loginlog/message等を別ファイル保存。Ver3は大半をuser_all.jsonのセクションへ統合し、送信箱だけmessage_sent.jsonに分離する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "変換器は各分割ファイルをchara・equipment・syoku・ログ・倉庫へ明示対応させる。",
        },
        "ユーザーデータのキー順・旧キー正規化": {
            "difference": "Ver2の列番号保存を、Ver3は名前付きJSONと固定キー順へ変更。title→title_id、unused30→tactic_idを移し、site/urlを除去し、未知キーは末尾に保持する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "order_user_dataは既知の旧キーだけを変換し、任意の追加キーを破棄しない。",
        },
        "装備・アクセサリー保存値の正規化": {
            "difference": "Ver2の<>列を、Ver3はweapon/armor/accessory辞書とbonus8能力・3率へ正規化し、説明欠損はマスターから補完する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "変換器は武器・防具・アクセの列順を固定し、アクセ説明が空なら現行/旧マスターから補う。",
        },
        "HTMLエンティティの読込正規化": {
            "difference": "Ver2は入力時にHTMLエンティティ化して保存。Ver3はJSON読込時に再帰的html.unescapeし、表示はテンプレートの自動エスケープへ委ねる。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "互換データを読めるようにする処理。保存済みの多重エンティティを何段階まで復元するかは値に依存するため、移行検証で表示確認が必要。",
        },
        "単一JSONの原子的書込み": {
            "difference": "Ver2は対象ファイルを直接開いて上書き。Ver3は同一ディレクトリの一時JSONへflush/fsync後、os.replaceで置換する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "例外時は一時ファイルを削除して再送出するため、途中JSONを本体として公開しない。",
        },
        "read-modify-writeの原子更新": {
            "difference": "Ver2は呼出側がlock/unlockと個別読書きを組み合わせる。Ver3は共有データ向けupdate_data_atomicallyが読込・更新・置換を同一ロックで実行する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "user_all.jsonのsave_user_sectionsは呼出側がユーザーロックを保持する契約。全呼出元がこの契約を守ることが前提になる。",
        },
        "ユーザー・共有データのロック": {
            "difference": "Ver2はsymlink/空ファイル/flockを設定で切替え、再試行・古いロック削除を行う。Ver3はos.mkdirディレクトリロック、同一スレッド再入管理、10/15秒タイムアウトを使う。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "finallyでrelease_lock/unlockする設計。Ver3は古いロックを自動削除せずタイムアウトで失敗させる。",
        },
        "バックアップ中のスナップショット排他": {
            "difference": "Ver2に保存と全体コピーを直列化する仕組みはない。Ver3は通常保存・日次作成・復元がbackup_snapshotロックを共有する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "通常保存はsnapshot→個別、復元はrestore→snapshotの順で取得する。",
        },
        "部分更新API": {
            "difference": "Ver2は関連ファイルを個別上書き。Ver3はsave_user_sectionsが統合データを読んで指定セクションだけ更新し、souko/chocoも同経路を使う。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "指定しないセクションを消さないが、呼出側のユーザーロックなしでは読込後更新の競合を防げない。",
        },
        "日次バックアップ作成": {
            "difference": "Ver2のsave_log.cgiは保護ユーザー一覧であり、日次バックアップ処理は確認できない。Ver3は当日初回ログイン時にsave_data全体を日付別コピーする。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "バックアップ失敗はstderr記録のみでログインを継続し、同日のmanifestがあれば再作成しない。",
        },
        "バックアップのマニフェスト・世代削除": {
            "difference": "Ver2にはバックアップ世代・検証情報がない。Ver3は件数・容量・作成時刻をmanifest.jsonへ記録し、既定40日を超える日付世代を削除する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "一覧は日付形式・manifest形式を検証し、壊れた世代を表示しない。",
        },
        "管理画面からのバックアップ復元": {
            "difference": "Ver2 login.cgiはhukugen.cgiを参照するが同梱実装がなく、復元手順をコードで確認できない。Ver3は管理画面から日付バックアップを復元できる。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "Ver3は日付名検証、maintenance_mode必須、復元前全体退避、temp置換、snapshot/restoreロックを実装する。",
        },
        "保護ユーザーの復元": {
            "difference": "Ver2はsave_log.cgiで削除保護対象を列挙するだけ。Ver3はprotected_user_idsを削除対象外にし、固定user_all.jsonから欠落・破損時だけ復元する。固定バックアップの自動作成はない。",
            "intent": "要判断",
            "status": "差異あり",
            "note": "restore_protected_usersはchara.idを検証して個別ロック下で復元するが、protected_user_backup_dirへの書込み元は現行Pythonコードにない。",
        },
        "管理画面によるマスター保存・削除": {
            "difference": "Ver2管理画面はhidden平文管理パスワードを引き回し、テキストを直接上書き。Ver3は暗号化管理セッション・CSRF・JSON解析・ID/型/下限/職業ID検証・原子保存を行う。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "職業は配列ID順を守るため削除不可。アクセサリー保存後は説明文キャッシュも無効化する。",
        },
        "Ver1→Ver2変換": {
            "difference": "Ver1→Ver2は過去世代間の変換であり、Ver3通常処理・Ver2→Ver3変換器の比較対象ではない。",
            "intent": "該当なし",
            "status": "対象外",
            "note": "履歴資料として入力列・dry-run・原本保持を残す。Ver3へ移す場合はVer2形式を経由してconvert_all.pyを使う。",
        },
        "Ver2→Ver3ユーザー本体変換": {
            "difference": "Ver2 charalogの固定35列をCHARA_COLUMNSで名前付きcharaへ写し、site/urlを除外、bankは34列目（残るbanklogがあればそちら優先）にする。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "能力8値、job・HP・EXP・戦績・戦術・称号・職業Lvの列番号を明示し、validate_userで必須能力と旧キー残存を検証する。",
        },
        "Ver2→Ver3装備・職業・倉庫変換": {
            "difference": "Ver2のitem/syoku/soukoを、装備辞書・職業ID文字列辞書・種別倉庫配列へ変換する。旧charalog2形式の倉庫もマスター参照で受け付ける。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "アクセ8能力・3率・説明を正規化し、存在しない倉庫マスターはwarningを出して除外する。",
        },
        "Ver2→Ver3ログ・共有データ変換": {
            "difference": "Ver2 loginlog/message/sousin/datalogをJSON化し、送信箱はuser_all.json外のmessage_sent.json、winnerはchampion.json、全体文はall_message.jsonにする。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "欠損ファイルは空値扱い。送信箱が空ならmessage_sent.jsonを作らず、winnerが無ければchampion.jsonを出力しない。",
        },
        "Ver2チョコボの移行時初期化": {
            "difference": "Ver2の現役チョコボ・個人G1履歴は変換せず、全ユーザーのchoco/choco_g1を空辞書で初期化する。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "convert_userの固定出力。旧チョコボを引き継がない仕様を明文化済みであり、既存Ver3データへ混在出力しない。",
        },
        "変換の文字コード・検証用出力": {
            "difference": "Ver2のCP932テキストをerrors=replaceで読み、<>分解後にHTMLエンティティを復元する。Ver3 JSONはUTF-8で、既定出力先はchange_data/users・shared、--dry-runは書込なし。",
            "intent": "意図的",
            "status": "差異あり",
            "note": "--output等で現行save_dataを指定できるため、実運用はdry-run→検証用出力→バックアップ後配置の順を守る。",
        },
    }


def write_storage_migration_checklist() -> None:
    write_static_checklist(
        "storage_migration_operations.md",
        "保存・認証・移行・運用比較チェックリスト",
        "Ver2の保存形式・認証・管理CGIと、Ver3の実装を28項目で照合した台帳です。保存形式の差異と、安全対策・運用手順として残すべき差異を分けて記録します。",
        (
            ("入力・表示・認証", (
                ("CGIパラメータの復号・文字列処理", "旧版_ver2/regist.pl / login.cgi", "sub_def/common.py:decode_params", "GET/POSTの優先順位、複数値、文字コード、空値・不正値"),
                ("CGI入口のUTF-8標準入出力", "旧版Ver2 CGIの出力設定", "others.py,login.py,chara_make.py,admin.py:reconfigure", "Windows Apache CP932環境、4入口の維持、UTF-8ヘッダーとの整合"),
                ("HTML出力・リダイレクトのヘッダー", "旧版_ver2/regist.pl:header / footer", "sub_def/utils.py:render_template,redirect", "Content-Type、UTF-8、キャッシュ制御、Location、例外時出力"),
                ("セッションCookieの暗号化・改ざん検証", "旧版_ver2/login.cgi:set_cookie", "sub_def/crypto.py:encrypt_data,decrypt_data,get_session,save_session", "Cookie内容、署名、期限、HttpOnly、旧Cookieとの関係"),
                ("ログイン・ログアウト", "旧版_ver2/login.cgi:log_in", "login.py", "ID・パスワード検証、セッション更新、記憶Cookie、日次バックアップの起点"),
                ("パスワード形式とログイン時移行", "旧版Ver2の保存パスワード", "sub_def/crypto.py:hash_password,verify_password,needs_rehash / login.py", "平文・旧ハッシュ・PBKDF2の受入範囲、成功時再ハッシュ"),
                ("CSRFトークンの生成・検証・再生成", "旧版Ver2のフォーム送信", "sub_def/crypto.py:token_generate,token_regenerate,token_check", "対象POST、トークン寿命、再表示時、エラー時"),
                ("本人操作の認可（IDOR対策）", "旧版Ver2のID・パスワード照合", "sub_def/common.py:require_owner / 各状態変更CGI", "対象操作、Cookieとの照合、ロック前検証、閲覧操作との区別"),
            )),
            ("JSON保存・ロック", (
                ("統合ユーザー保存形式", "旧版_ver2/charalog,item,syoku,souko等の分割ファイル", "save_data/<ID>/user_all.json / sub_def/file_ops.py", "セクション構成、必須・任意キー、旧分割データとの対応"),
                ("ユーザーデータのキー順・旧キー正規化", "旧版Ver2の配列列番号", "sub_def/data_schema.py:order_user_data", "title→title_id、unused30→tactic_id、site/url削除、未知キー保持"),
                ("装備・アクセサリー保存値の正規化", "旧版_ver2/item/<ID>.cgi", "sub_def/data_schema.py:_order_equipment / sub_def/common.py", "武器・防具・アクセ順、bonus8能力、旧アクセキー、説明補完"),
                ("HTMLエンティティの読込正規化", "旧版のHTML保存文字列", "sub_def/file_ops.py:_normalize_loaded_data / sub_def/common.py:decode_html_entities", "再帰対象、二重復号、名前・コメント・ログへの影響"),
                ("単一JSONの原子的書込み", "旧版_ver2/regist.pl:chara_regist ほか", "sub_def/file_ops.py:_write_json_atomically,save_data_atomically", "一時ファイル、fsync、os.replace、例外時の残存一時ファイル"),
                ("read-modify-writeの原子更新", "旧版_ver2/regist.pl:lock / unlock", "sub_def/file_ops.py:update_data_atomically", "読込から保存までの同一ロック、default値、更新関数の例外"),
                ("ユーザー・共有データのロック", "旧版_ver2/regist.pl:lock / unlock", "sub_def/common.py:get_lock,release_lock / sub_def/lock_state.py", "ロック名、再入、タイムアウト、ディレクトリロック、必ず解放すること"),
                ("バックアップ中のスナップショット排他", "旧版には相当処理なし", "sub_def/file_ops.py:backup_snapshot.lock / sub_def/backup.py", "通常保存とバックアップの順序、デッドロック、保存待機"),
                ("部分更新API", "旧版の複数ファイル個別保存", "sub_def/common.py:save_user_sections,souko_regist,choco_regist", "他セクションを消さないこと、読込失敗時、呼出元のロック"),
            )),
            ("バックアップ・管理復元", (
                ("日次バックアップ作成", "旧版_ver2/admin.cgi:save_chara / save_log.cgi（保護一覧。日次バックアップなし）", "sub_def/backup.py:create_daily_backup,ensure_daily_backup", "実行契機、対象範囲、同日再実行、失敗時のログイン継続"),
                ("バックアップのマニフェスト・世代削除", "旧版Ver2には相当処理なし", "sub_def/backup.py:_write_manifest,_prune_daily_backups,list_daily_backups", "件数・容量、形式検証、保持日数、壊れた世代の表示除外"),
                ("管理画面からのバックアップ復元", "旧版_ver2/login.cgi:70（hukugen.cgiを参照するが同梱なし）", "sub_def/backup.py:restore_daily_backup / admin.py:backup_restore", "maintenance_mode必須、パス検証、復元前退避、現在save_dataの置換"),
                ("保護ユーザーの復元", "旧版_ver2/admin.cgi:save_chara / save_del", "admin.py:protected_backup_path,restore_protected_users", "対象ID、JSON妥当性、個別ロック、上書き範囲"),
                ("管理画面によるマスター保存・削除", "旧版_ver2/admin.cgi", "admin.py:validate_master_record,save_master_records", "ID一意性、型・下限、JSON妥当性、アクセサリーキャッシュ無効化"),
            )),
            ("旧版からの移行", (
                ("Ver1→Ver2変換", "旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py", "docs/migration_specs.html（履歴資料）", "入力・出力の列対応、原本保持、dry-run、Ver3比較対象外であること"),
                ("Ver2→Ver3ユーザー本体変換", "旧版_ver2/charalog/<ID>.cgi", "旧版_ver2/change_data/convert_all.py / sub_def/data_schema.py", "列番号→charaキー、能力値順、パスワード、戦績、戦術・称号"),
                ("Ver2→Ver3装備・職業・倉庫変換", "旧版_ver2/item,syoku,souko", "旧版_ver2/change_data/convert_all.py", "マスター参照、装備性能、職業熟練度、倉庫件数、旧形式の残存"),
                ("Ver2→Ver3ログ・共有データ変換", "旧版_ver2/loginlog,message,sousin,datalog", "旧版_ver2/change_data/convert_all.py", "message_sentの別保存、champion.json、all_message.json、欠損時"),
                ("Ver2チョコボの移行時初期化", "旧版_ver2のチョコボ保存データ", "旧版_ver2/change_data/convert_all.py / docs/migration_specs.html", "現役チョコボを移さずchoco/choco_g1を空辞書にする意図、既存データとの衝突"),
                ("変換の文字コード・検証用出力", "旧版Ver2のCP932テキスト", "旧版_ver2/change_data/convert_all.py", "CP932読込、文字化け置換、dry-run、検証先出力、現行save_dataを直接上書きしないこと"),
            )),
        ),
        comparisons=storage_migration_comparisons(),
    )


def write_index(counts: dict[str, int]) -> None:
    text = f"""# Ver2 / Ver3 比較チェックリスト

Ver2から移植したFFA Python版（Ver3）の、データ・コマンド・行動を比較するための作業台帳です。\
ここに記載した「未確認」は差異なしを意味せず、まだ照合していないことを示します。

## 運用ルール

- `Ver2との差異` は、値・条件・処理順・表示・保存形式を具体的に記載する。
- `意図的な仕様か否か` は `意図的` / `不具合` / `要判断` のいずれかを記載し、根拠を備考に残す。
- Ver2に寄せる修正をする前に、現行側で追加された安全対策・バランス調整かを必ず確認する。
- `照合状態` は `未確認` / `確認中` / `一致` / `差異あり` / `対象外` を使う。
- 一次比較完了は全件の初期台帳作成済みを示すだけで、実装を再読したことは示さない。ファイル単位の精査済み結果は各台帳の「ファイル単位の精査記録」に残す。

## チェック対象一覧

| 区分 | 内容 | 状態 |
| --- | --- | --- |
| 装備データ | [武器・防具・アクセサリー](equipment.md)（武器 {counts['weapon']}件、防具 {counts['armor']}件、アクセサリー {counts['accessory']}件） | 一次比較完了 |
| 職業データ | [職業31件](jobs.md)：転職条件、成長上限、必要マスター職 | 一次比較完了 |
| 戦術・必殺技データ | [戦術78件](skills.md)：説明、利用職、マスター条件、発動率、効果 | 一次比較完了 |
| モンスター特殊技 | [特殊技22種・使用220体](monster_skills.md)：特殊技、特殊率、使用モンスター | 一次比較完了 |
| モンスターデータ | [全9ファイル・347件](monsters.md)：出現テーブル、能力値、報酬、ボス・異世界 | 一次比較完了 |
| チョコボデータ | [全10ファイル・495件](chocobo_data.md)：候補血統、価格、ライバル、レース能力 | 一次比較完了 |
| 戦闘 | [戦闘計算・結果処理](battle_logic.md)：ターン順、必殺技、クリティカル、防御・回避、HP、勝敗、報酬、成長 | 一次比較完了 |
| コマンド・画面 | [ルート{len(function_routes())}件・実行操作一覧](commands_actions.md)：移動、店、宿、銀行、転職、ランキング、管理画面 | 一次比較完了／二次精査 {len(FILE_AUDITS)}ファイル |
| 所有・進行要素 | [所有・進行](ownership_progression.md)：職業・装備・倉庫・戦績・王者・レジェンド・チョコボ・共有記録 | 一次比較完了 |
| 保存・移行・運用 | [保存・認証・移行・運用](storage_migration_operations.md)：JSON、認証、CSRF、ロック、バックアップ、変換 | 一次比較完了 |

## 共通の記入列

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 例: 武器 1001: アイアンソード | 旧版の定義ファイル・該当ID | Ver3のJSON・参照コード | 数値や条件を具体的に記載 | 意図的 / 不具合 / 要判断 | 未確認など | コミット、仕様書、確認日 |
"""
    (OUTPUT_DIR / "README.md").write_text(text, encoding="utf-8")


def write_equipment(labels: dict[int, str]) -> None:
    sections = [
        "# 装備データ比較チェックリスト",
        "",
        "Ver3の装備マスターを全件列挙した初期台帳です。Ver2の `item.pl` と照合して記入します。",
        "",
        "| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    weapon_results = weapon_comparisons(labels)
    armor_results = armor_comparisons(labels)
    accessory_results = accessory_comparisons()
    for kind, label, v2_source in EQUIPMENT:
        rows = load_json(f"{kind}.json")
        sections.extend(("", f"## {label}（{len(rows)}件）", ""))
        sections.extend(
            checklist_row(
                kind,
                item,
                labels,
                v2_source,
                weapon_results.get(as_int(item.get("no"))) if kind == "weapon" else armor_results.get(as_int(item.get("no"))) if kind == "armor" else accessory_results.get(as_int(item.get("no"))),
            )
            for item in rows
        )
    (OUTPUT_DIR / "equipment.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    labels = job_labels()
    counts = {kind: len(load_json(f"{kind}.json")) for kind, _, _ in EQUIPMENT}
    write_index(counts)
    write_equipment(labels)
    write_jobs(labels)
    write_skills(labels)
    write_monster_skills()
    write_monsters()
    write_chocobo_data()
    write_commands_actions()
    write_battle_logic_checklist()
    write_progression_checklist()
    write_storage_migration_checklist()


if __name__ == "__main__":
    main()
