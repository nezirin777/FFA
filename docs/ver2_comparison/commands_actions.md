# コマンド・行動比較チェックリスト

画面遷移だけのルートと、各ルート内の実行操作を分けて管理します。比較前に状態変更か表示かを確認し、Ver2との差分を具体的に記録します。

対象: ルート 38件、実行操作 121件。
## ルート一覧（login.py）

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| ルート `mode=main`: 街のメイン画面 | `旧版_ver2/ffadventure.cgi` | `login.py` → `cgi_py.ffadventure` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=sts`: 自分のステータス | `旧版_ver2/sts.cgi` | `login.py` → `cgi_py.sts` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=tac_change`: 戦術選択 | `旧版_ver2/tac_change.cgi` | `login.py` → `cgi_py.tac_change` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=passchange`: 合言葉・パスワード変更 | `旧版_ver2/passchange.cgi` | `login.py` → `cgi_py.passchange` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=tensyoku`: 転職 | `旧版_ver2/tensyoku.cgi` | `login.py` → `cgi_py.tensyoku` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop`: 宿屋 | `旧版_ver2/shop.cgi` | `login.py` → `cgi_py.shop` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=yado`: 宿泊（shopへの互換ルート） | `旧版_ver2/shop.cgi` | `login.py` → `cgi_py.shop` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop_weapon`: 武器店 | `旧版_ver2/shop_item.cgi` | `login.py` → `cgi_py.shop_weapon` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop_armor`: 防具店 | `旧版_ver2/shop_def.cgi` | `login.py` → `cgi_py.shop_armor` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop_accessory`: 装飾品店 | `旧版_ver2/shop_acs.cgi` | `login.py` → `cgi_py.shop_accessory` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop_item`: 武器店（旧URL互換） | `旧版_ver2/shop_item.cgi` | `login.py` → `cgi_py.shop_weapon` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop_def`: 防具店（旧URL互換） | `旧版_ver2/shop_def.cgi` | `login.py` → `cgi_py.shop_armor` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=shop_acs`: 装飾品店（旧URL互換） | `旧版_ver2/shop_acs.cgi` | `login.py` → `cgi_py.shop_accessory` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=bank`: 銀行 | `旧版_ver2/bank.cgi` | `login.py` → `cgi_py.bank` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=souko`: 倉庫 | `旧版_ver2/souko.cgi` | `login.py` → `cgi_py.souko` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=battle`: 人間チャンピオン戦 | `旧版_ver2/battle.cgi` | `login.py` → `cgi_py.battle` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=select_battle`: 対人戦の相手選択 | `旧版_ver2/select_battle.cgi` | `login.py` → `cgi_py.select_battle` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=sentaku`: 対人戦の相手選択（互換ルート） | `旧版_ver2/select_battle.cgi` | `login.py` → `cgi_py.select_battle` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=monster`: 通常モンスター修行 | `旧版_ver2/monster.cgi` | `login.py` → `cgi_py.monster` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=genei`: 幻影の城（モンスター互換ルート） | `旧版_ver2/monster.cgi` | `login.py` → `cgi_py.monster` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=isekiai`: 異世界（モンスター互換ルート） | `旧版_ver2/monster.cgi` | `login.py` → `cgi_py.monster` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=legend`: レジェンドプレイス | `旧版_ver2/legend.cgi` | `login.py` → `cgi_py.legend` / 表示・状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=boss`: レジェンド戦（互換ルート） | `旧版_ver2/legend.cgi` | `login.py` → `cgi_py.legend` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=bbs`: 掲示板投稿 | `旧版_ver2/post_message.cgi` | `login.py` → `cgi_py.bbs` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=chocofarm`: チョコボ牧場 | `旧版_ver2/chocofarm.cgi` | `login.py` → `cgi_py.chocofarm` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=morifarm`: チョコボの森 | `旧版_ver2/morifarm.cgi` | `login.py` → `cgi_py.morifarm` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=choco`: チョコボの森（互換ルート） | `旧版_ver2/morifarm.cgi` | `login.py` → `cgi_py.morifarm` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=crace`: チョコボレース | `旧版_ver2/crace.cgi` | `login.py` → `cgi_py.crace` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=ctrain`: チョコボ訓練 | `旧版_ver2/ctrain.cgi` | `login.py` → `cgi_py.ctrain` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=dendo`: チョコボ殿堂 | `旧版_ver2/dendo.cgi` | `login.py` → `cgi_py.dendo` / 表示・更新 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=farmrace`: チョコボ王者戦 | `旧版_ver2/farmrace.cgi` | `login.py` → `cgi_py.farmrace` / 状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=system`: 登録者一覧・画像一覧・他者詳細 | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=chara_sts`: 他者詳細（system互換ルート） | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=img_list`: 画像一覧（system互換ルート） | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=ranking`: 登録者一覧（system互換ルート） | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=tenka`: 天下一武道会 | `旧版_ver2/tenka.cgi` | `login.py` → `cgi_py.tenka` / 表示・状態変更 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=rank`: 英雄ランキング | `旧版_ver2/rank.cgi` | `login.py` → `cgi_py.rank` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |
| ルート `mode=chocorank`: チョコボランキング | `旧版_ver2/chocorank.cgi` | `login.py` → `cgi_py.chocorank` / 表示 | 未確認 | 未判定 | 未確認 | ルート名、公開範囲、HTTPメソッド、互換エイリアスを照合後に根拠を記入 |

## 実行操作一覧

### 認証・登録

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| トップ／ログイン前画面（`（others.py）` / GET / 表示） | `旧版_ver2/others.cgi` | `others.py / templates/others.html` | 未確認 | 未判定 | 未確認 | 公開範囲、ログイン入力、登録導線 |
| 新規登録入力（`mode=chara_make` / POST / 表示） | `旧版_ver2/others.cgi / chara_make.cgi` | `others.py / templates/chara_make.html` | 未確認 | 未判定 | 未確認 | 入力項目、初期職、画像選択、CSRF |
| 新規登録確認（`mode=make_pre` / POST / 表示） | `旧版_ver2/chara_make.cgi` | `chara_make.py / templates/chara_make_pre.html` | 未確認 | 未判定 | 未確認 | 入力検証、同一IP制限、確認画面 |
| 新規登録確定（`mode=make_end` / POST / 状態変更） | `旧版_ver2/chara_make.cgi` | `chara_make.py` | 未確認 | 未判定 | 未確認 | 初期能力・初期装備・保存形式・パスワード |
| ログイン（`mode=log_in` / POST / 状態変更） | `旧版_ver2/login.cgi` | `login.py` | 未確認 | 未判定 | 未確認 | 認証方式、セッション、旧ハッシュ移行、日次バックアップ |
| ログアウト（`mode=log_out` / POST/GET / 状態変更） | `旧版_ver2/login.cgi` | `login.py` | 未確認 | 未判定 | 未確認 | セッション破棄、遷移先 |
| 合言葉確認（`mode=passset` / POST / 表示） | `旧版_ver2/passchange.cgi` | `cgi_py/passchange.py` | 未確認 | 未判定 | 未確認 | 本人確認条件、画面遷移 |
| パスワード変更確定（`mode=passchan` / POST / 状態変更） | `旧版_ver2/passchange.cgi` | `cgi_py/passchange.py` | 未確認 | 未判定 | 未確認 | 旧/新パスワード検証、ハッシュ、セッション更新 |

### 街・プロフィール

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 街のメイン画面（`mode=main` / GET/POST / 表示） | `旧版_ver2/ffadventure.cgi` | `cgi_py/ffadventure.py` | 未確認 | 未判定 | 未確認 | 能力表示、王者情報、待機時間、掲示板表示 |
| レジェンド挑戦を中断して街へ戻る（`mode=main, legend_cancel=1` / POST / 状態変更） | `旧版_ver2/ffadventure.cgi` | `cgi_py/ffadventure.py` | 未確認 | 未判定 | 未確認 | boss_flagのリセット値、CSRF、途中進行の扱い |
| 自分のステータスを表示（`mode=sts` / POST / 表示） | `旧版_ver2/sts.cgi` | `cgi_py/sts.py` | 未確認 | 未判定 | 未確認 | 能力・装備補正・職業熟練度・表示値 |
| 画像・発動コメントを変更（`mode=st_buy` / POST / 状態変更） | `旧版_ver2/sts.cgi` | `cgi_py/sts.py` | 未確認 | 未判定 | 未確認 | 画像ID、コメント長・禁止語、保存 |
| 戦術一覧を表示（`mode=tac_change` / POST / 表示） | `旧版_ver2/tac_change.cgi` | `cgi_py/tac_change.py` | 未確認 | 未判定 | 未確認 | 使用可能条件、マスター判定、現在戦術 |
| 戦術を変更（`mode=senjutu_henkou` / POST / 状態変更） | `旧版_ver2/tac_change.cgi` | `cgi_py/tac_change.py` | 未確認 | 未判定 | 未確認 | 戦術ID、職業・熟練度条件、保存 |
| 転職画面を表示（`mode=tensyoku` / POST / 表示） | `旧版_ver2/tensyoku.cgi` | `cgi_py/tensyoku.py` | 未確認 | 未判定 | 未確認 | 候補職、能力条件、マスター条件 |
| 転職を実行（`mode=tensyoku_change` / POST / 状態変更） | `旧版_ver2/tensyoku.cgi` | `cgi_py/tensyoku.py` | 未確認 | 未判定 | 未確認 | 転職条件、現職熟練度、能力上限、戦術 |
| 掲示板へ投稿（`mode=post` / POST / 状態変更） | `旧版_ver2/post_message.cgi` | `cgi_py/bbs.py` | 未確認 | 未判定 | 未確認 | 文字数、保存上限、投稿者、CSRF |

### 店・資産

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 宿泊（`mode=yado` / POST / 状態変更） | `旧版_ver2/shop.cgi` | `cgi_py/shop.py` | 未確認 | 未判定 | 未確認 | 宿代、HP全快、王者HP、boss_flagリセット |
| 銀行を表示（`mode=bank` / POST / 表示） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 未確認 | 未判定 | 未確認 | 所持金・預金上限、表示単位 |
| 銀行へ預け入れ（`mode=bank_sell` / POST / 状態変更） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 未確認 | 未判定 | 未確認 | 1,000G単位、所持金・預金上限 |
| 銀行から引き出し（`mode=bank_buy` / POST / 状態変更） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 未確認 | 未判定 | 未確認 | 1,000G単位、所持金上限 |
| 倉庫を表示（`mode=souko` / POST / 表示） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | 装備中・保管中の区分、表示順 |
| 武器店を表示（`mode=shop_weapon` / POST / 表示） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 未確認 | 未判定 | 未確認 | 品揃え、職業制限、価格、所持品表示 |
| 武器を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 未確認 | 未判定 | 未確認 | item_no、価格、職業制限、所持金、保管先 |
| 武器を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 未確認 | 未判定 | 未確認 | 売値、装備中の扱い、保管品削除、所持金上限 |
| 防具店を表示（`mode=shop_armor` / POST / 表示） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 未確認 | 未判定 | 未確認 | 品揃え、職業制限、価格、所持品表示 |
| 防具を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 未確認 | 未判定 | 未確認 | item_no、価格、職業制限、所持金、保管先 |
| 防具を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 未確認 | 未判定 | 未確認 | 売値、装備中の扱い、保管品削除、所持金上限 |
| 装飾品店を表示（`mode=shop_accessory` / POST / 表示） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 未確認 | 未判定 | 未確認 | 品揃え、職業制限、価格、所持品表示 |
| 装飾品を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 未確認 | 未判定 | 未確認 | item_no、価格、職業制限、所持金、保管先 |
| 装飾品を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 未確認 | 未判定 | 未確認 | 売値、装備中の扱い、保管品削除、所持金上限 |
| 装備中の武器を倉庫へ外す（`mode=weapon_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | 初期装備化、保管先、二重登録 |
| 倉庫の武器を装備（`mode=weapon_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | item_no、職業制限、既存装備の退避 |
| 倉庫の武器を削除（`mode=weapon_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | item_no、削除対象、復元不能な削除の確認 |
| 装備中の防具を倉庫へ外す（`mode=armor_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | 初期装備化、保管先、二重登録 |
| 倉庫の防具を装備（`mode=armor_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | item_no、職業制限、既存装備の退避 |
| 倉庫の防具を削除（`mode=armor_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | item_no、削除対象、復元不能な削除の確認 |
| 装備中の装飾品を倉庫へ外す（`mode=accessory_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | 初期装備化、保管先、二重登録 |
| 倉庫の装飾品を装備（`mode=accessory_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | item_no、職業制限、既存装備の退避 |
| 倉庫の装飾品を削除（`mode=accessory_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | item_no、削除対象、復元不能な削除の確認 |

### 戦闘・対戦

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| チャンピオンに挑戦（`mode=battle` / POST / 状態変更） | `旧版_ver2/battle.cgi / wbattle.pl` | `cgi_py/battle.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | 待機時間、勝敗・引分、経験値・賞金、王者交代 |
| 対人相手一覧を表示（`mode=log_in` / POST / 表示） | `旧版_ver2/select_battle.cgi` | `cgi_py/select_battle.py` | 未確認 | 未判定 | 未確認 | 対象者抽出、公開範囲、待機時間 |
| 対人相手を選択（`mode=sentaku` / POST / 表示） | `旧版_ver2/select_battle.cgi` | `cgi_py/select_battle.py` | 未確認 | 未判定 | 未確認 | 相手ID、本人・無効対象の除外 |
| 選択相手と対戦（`mode=battle` / POST / 状態変更） | `旧版_ver2/select_battle.cgi / wbattle.pl` | `cgi_py/select_battle.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | 相手認証、勝敗、経験値・賞金、戦績 |
| 通常モンスター修行（`mode=monster` / POST / 状態変更） | `旧版_ver2/monster.cgi / mbattle.pl` | `cgi_py/monster.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | 出現テーブル、回数制限、勝敗・引分報酬、経験値 |
| 幻影の城へ挑戦（`mode=genei` / POST / 状態変更） | `旧版_ver2/monster.cgi / mbattle.pl` | `cgi_py/monster.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | 出現条件、HP/防御補正、報酬 |
| 異世界へ挑戦（`mode=isekiai` / POST / 状態変更） | `旧版_ver2/monster.cgi / mbattle.pl` | `cgi_py/monster.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | レベル条件、出現テーブル、特殊報酬 |
| レジェンド攻略者一覧を閲覧（`mode=legend, view=ranking` / GET / 表示） | `旧版_ver2/legend.cgi` | `cgi_py/legend.py` | 未確認 | 未判定 | 未確認 | 公開範囲、順位、称号 |
| レジェンドの階層へ挑戦（`mode=boss, boss_file=0〜3` / POST / 状態変更） | `旧版_ver2/legend.cgi / mbattle.pl` | `cgi_py/legend.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | 進行フラグ、階層順、勝敗・称号・報酬 |
| 天下一武道会ロビーを表示（`mode=tenka` / POST / 表示） | `旧版_ver2/tenka.cgi` | `cgi_py/tenka.py` | 未確認 | 未判定 | 未確認 | 参加条件、進行状態、対戦相手 |
| 天下一武道会で対戦（`mode=battle, no=1〜3` / POST / 状態変更） | `旧版_ver2/tenka.cgi / wbattle.pl` | `cgi_py/tenka.py / sub_def/battle_logic.py` | 未確認 | 未判定 | 未確認 | ラウンド順、引分・敗北、賞金・経験値・制覇履歴 |

### 閲覧

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 英雄ランキングを表示（`mode=rank` / GET / 表示） | `旧版_ver2/rank.cgi` | `cgi_py/rank.py` | 未確認 | 未判定 | 未確認 | 部門、勝率の対象条件、キャッシュ |
| 登録者一覧を表示（`mode=ranking, shtm` / GET / 表示） | `旧版_ver2/system.cgi` | `cgi_py/system.py` | 未確認 | 未判定 | 未確認 | ページング、公開項目、キャッシュ |
| 他者の詳細ステータスを表示（`mode=chara_sts, id` / GET / 表示） | `旧版_ver2/system.cgi` | `cgi_py/system.py` | 未確認 | 未判定 | 未確認 | 公開項目、装備・マスター職、ID指定 |
| キャラクター画像一覧を表示（`mode=img_list` / GET / 表示） | `旧版_ver2/system.cgi` | `cgi_py/system.py` | 未確認 | 未判定 | 未確認 | 画像ID・ファイル対応 |

### チョコボ

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| チョコボ訓練: バーベルあげ（`mode=race0` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | 速度の増減、寿命、失敗時の副作用、待機時間 |
| チョコボ訓練: 砂浜走り（`mode=race1` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | スタミナの増減、寿命、失敗時の副作用、待機時間 |
| チョコボ訓練: スイミング（`mode=race2` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | 粘りの増減、寿命、失敗時の副作用、待機時間 |
| チョコボ訓練: 瞑想（`mode=race3` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | 落ち着きの増減、寿命、失敗時の副作用、待機時間 |
| チョコボ訓練: 猛特訓（`mode=race4` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | 闘争心の増減、寿命、失敗時の副作用、待機時間 |
| チョコボ訓練: お勉強（`mode=race5` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | 賢さの増減、寿命、失敗時の副作用、待機時間 |
| チョコボ訓練: 坂道ダッシュ（`mode=race6` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 未確認 | 未判定 | 未確認 | 反射神経の増減、寿命、失敗時の副作用、待機時間 |
| チョコボ牧場を表示（`mode=chocofarm` / POST / 表示） | `旧版_ver2/chocofarm.cgi` | `cgi_py/chocofarm.py` | 未確認 | 未判定 | 未確認 | 所持判定、レース条件、重賞開催条件 |
| チョコボの森を表示（`mode=choco / morifarm` / POST / 表示） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 所持判定、候補表示、互換ルート |
| 野生チョコボ候補を表示（`mode=choco_shop` / POST / 表示） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 候補抽選、候補数、マスター参照 |
| 野生チョコボを購入（`mode=choco_buy, item_no` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 候補検証、価格、初期能力、所持制限 |
| お見合い相手を表示（`mode=choco_shopb` / POST / 表示） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 性別、引退候補、候補上限 |
| お見合い・配合を実行（`mode=choco_buyb, item_no` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 親の引退、血統、能力上限、子の初期値 |
| チョコボに名前を付ける（`mode=choco_name` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 名前入力、禁止語、保存 |
| チョコボを休ませる（`mode=yadoya` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 寿命・体力の回復、費用、待機時間 |
| チョコボを手放す（`mode=choco_sell` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 引退先、売却額、取り消し不可 |
| チョコボ殿堂を表示（`mode=list` / POST / 表示） | `旧版_ver2/dendo.cgi` | `cgi_py/dendo.py / templates/chocofarm.html` | 未確認 | 未判定 | 未確認 | 登録済み一覧、トロフィー表示、表示用modeと登録用modeの分離 |
| チョコボを殿堂登録（`mode=dendo` / POST / 状態変更） | `旧版_ver2/dendo.cgi` | `cgi_py/dendo.py` | 未確認 | 未判定 | 未確認 | 重賞3勝条件、重複登録、保存値 |
| チョコボランキングを表示（`mode=ranking` / POST / 表示） | `旧版_ver2/chocorank.cgi` | `cgi_py/chocorank.py` | 未確認 | 未判定 | 未確認 | 部門、ランキング対象、表示値 |
| チョコボ王者戦（`mode=farmrace` / POST / 状態変更） | `旧版_ver2/farmrace.cgi` | `cgi_py/farmrace.py` | 未確認 | 未判定 | 未確認 | 挑戦条件、勝敗、王者更新、待機時間 |
| チョコボレース: 新馬戦（`mode=race0` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| チョコボレース: 500万以下（`mode=race1` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| チョコボレース: 900万以下（`mode=race2` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| チョコボレース: 1600万以下（`mode=race3` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| チョコボレース: オープン特別（`mode=race4` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| チョコボレース: グレードIII（`mode=race5` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| チョコボレース: グレードII（`mode=race6` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 勝利数条件、ライバルファイル、寿命、賞金・戦績 |
| G1レース: チョコボダービー（`mode=race7, race=1` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: チョコボスタリオン（`mode=race7, race=2` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: チョコボカップ（`mode=race7, race=3` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: ジェイドカップ（`mode=race7, race=4` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: BBA賞（`mode=race7, race=5` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: チョコボ春賞（`mode=race7, race=6` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: チョコボ秋賞（`mode=race7, race=7` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: チョコボキング（`mode=race7, race=8` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: チョコボステークス（`mode=race7, race=9` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: キングスカップ（`mode=race7, race=10` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G1レース: クイーンカップ（`mode=race7, race=11` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: シルバーカップ（`mode=race8, race=12` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: 新潟アドバンス（`mode=race8, race=13` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: チコスダービー（`mode=race8, race=14` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: チョコボードカップ（`mode=race8, race=15` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: チョコボエプソム（`mode=race8, race=16` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: チョコボ王（`mode=race8, race=17` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: ブリーダーズカップ（`mode=race8, race=18` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: ゴールドカップ（`mode=race8, race=19` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: プラチナカップ（`mode=race8, race=20` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: チョコボオークス（`mode=race8, race=21` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| G2レース: チョコボキングス（`mode=race8, race=22` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 開催周期・性別、勝利数条件、トロフィー、ライバル |
| 殿堂レジェンドレース（`mode=race_dendo` / POST / 状態変更） | `旧版_ver2/crace.cgi / denchoco.cgi` | `cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | 出走条件、殿堂データ、勝敗・報酬 |

### 管理

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 管理画面を表示（`mode=kanri_top` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 管理画面認証、一覧範囲 |
| 管理画面からログアウト（`mode=admin_log_out` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 管理セッションの破棄 |
| 全体メッセージを投稿（`mode=post_all_message` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 文字数、保存上限、投稿者 |
| マスター一覧を表示（`mode=master_list` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 対象マスター、ID順 |
| マスターを編集表示（`mode=master_edit` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | master_type、master_id、新規判定 |
| マスターを保存（`mode=master_save` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | JSON検証、ID重複、バックアップ |
| マスターを削除（`mode=master_delete` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 削除対象、参照整合性、バックアップ |
| プレイヤー所持品を表示（`mode=player_item` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 対象ID、装備・保管品 |
| プレイヤー所持品を追加（`mode=player_item_add` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 対象ID、アイテム参照、重複 |
| バックアップから復元（`mode=backup_restore` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | バックアップ名、現在状態退避、復元範囲 |
| 保護ユーザーを復元（`mode=restore_protected` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 保護対象、復元元、上書き |
| 全キャラクターデータを表示（`mode=kanri_all` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 一覧範囲、公開情報 |
| 個別キャラクターデータを表示（`mode=data` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 対象ID、編集項目 |
| 個別キャラクターデータを保存（`mode=save` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 能力値境界、職業・HP・所持金、保存 |
| 個別キャラクターを削除（`mode=del_chara` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 対象ID、関連保存データ、復元可能性 |
| 未プレイキャラクターを削除（`mode=del_noplay` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 未確認 | 未判定 | 未確認 | 対象条件、保護ユーザー、削除範囲 |

