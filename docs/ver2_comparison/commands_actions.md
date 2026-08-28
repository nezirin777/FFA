# コマンド・行動比較チェックリスト

画面遷移だけのルートと、各ルート内の実行操作を分けて管理します。比較前に状態変更か表示かを確認し、Ver2との差分を具体的に記録します。

対象: ルート 38件、実行操作 121件。
## ルート一覧（login.py）

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| ルート `mode=main`: 街のメイン画面 | `旧版_ver2/ffadventure.cgi` | `login.py` → `cgi_py.ffadventure` / 表示 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.ffadventureを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=sts`: 自分のステータス | `旧版_ver2/sts.cgi` | `login.py` → `cgi_py.sts` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.stsを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=tac_change`: 戦術選択 | `旧版_ver2/tac_change.cgi` | `login.py` → `cgi_py.tac_change` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.tac_changeを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=passchange`: 合言葉・パスワード変更 | `旧版_ver2/passchange.cgi` | `login.py` → `cgi_py.passchange` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.passchangeを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=tensyoku`: 転職 | `旧版_ver2/tensyoku.cgi` | `login.py` → `cgi_py.tensyoku` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.tensyokuを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=shop`: 宿屋 | `旧版_ver2/shop.cgi` | `login.py` → `cgi_py.shop` / 状態変更 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.shopを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=yado`: 宿泊（shopへの互換ルート） | `旧版_ver2/shop.cgi` | `login.py` → `cgi_py.shop` / 状態変更 | Ver3で`shop`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.shopへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=shop_weapon`: 武器店 | `旧版_ver2/shop_item.cgi` | `login.py` → `cgi_py.shop_weapon` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.shop_weaponを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=shop_armor`: 防具店 | `旧版_ver2/shop_def.cgi` | `login.py` → `cgi_py.shop_armor` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.shop_armorを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=shop_accessory`: 装飾品店 | `旧版_ver2/shop_acs.cgi` | `login.py` → `cgi_py.shop_accessory` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.shop_accessoryを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=shop_item`: 武器店（旧URL互換） | `旧版_ver2/shop_item.cgi` | `login.py` → `cgi_py.shop_weapon` / 表示・更新 | Ver3で`shop_weapon`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.shop_weaponへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=shop_def`: 防具店（旧URL互換） | `旧版_ver2/shop_def.cgi` | `login.py` → `cgi_py.shop_armor` / 表示・更新 | Ver3で`shop_armor`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.shop_armorへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=shop_acs`: 装飾品店（旧URL互換） | `旧版_ver2/shop_acs.cgi` | `login.py` → `cgi_py.shop_accessory` / 表示・更新 | Ver3で`shop_accessory`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.shop_accessoryへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=bank`: 銀行 | `旧版_ver2/bank.cgi` | `login.py` → `cgi_py.bank` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.bankを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=souko`: 倉庫 | `旧版_ver2/souko.cgi` | `login.py` → `cgi_py.souko` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.soukoを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=battle`: 人間チャンピオン戦 | `旧版_ver2/battle.cgi` | `login.py` → `cgi_py.battle` / 状態変更 | 状態変更ルートをPOST専用＋共通CSRF検証へ変更 | 意図的 | 差異あり | GET直打ちはlogin.pyで拒否し、ログイン済みセッションを確認してからモジュールを遅延ロードする。 |
| ルート `mode=select_battle`: 対人戦の相手選択 | `旧版_ver2/select_battle.cgi` | `login.py` → `cgi_py.select_battle` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.select_battleを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=sentaku`: 対人戦の相手選択（互換ルート） | `旧版_ver2/select_battle.cgi` | `login.py` → `cgi_py.select_battle` / 表示・更新 | Ver3で`select_battle`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.select_battleへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=monster`: 通常モンスター修行 | `旧版_ver2/monster.cgi` | `login.py` → `cgi_py.monster` / 状態変更 | 状態変更ルートをPOST専用＋共通CSRF検証へ変更 | 意図的 | 差異あり | GET直打ちはlogin.pyで拒否し、ログイン済みセッションを確認してからモジュールを遅延ロードする。 |
| ルート `mode=genei`: 幻影の城（モンスター互換ルート） | `旧版_ver2/monster.cgi` | `login.py` → `cgi_py.monster` / 状態変更 | Ver3で`monster`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.monsterへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=isekiai`: 異世界（モンスター互換ルート） | `旧版_ver2/monster.cgi` | `login.py` → `cgi_py.monster` / 状態変更 | Ver3で`monster`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.monsterへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=legend`: レジェンドプレイス | `旧版_ver2/legend.cgi` | `login.py` → `cgi_py.legend` / 表示・状態変更 | 攻略者一覧だけ公開閲覧として分離 | 意図的 | 差異あり | view=rankingのGETだけ未ログイン閲覧可。攻略実行はPOST専用・ログイン必須でboss互換ルートにも対応する。 |
| ルート `mode=boss`: レジェンド戦（互換ルート） | `旧版_ver2/legend.cgi` | `login.py` → `cgi_py.legend` / 状態変更 | Ver3で`legend`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.legendへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=bbs`: 掲示板投稿 | `旧版_ver2/post_message.cgi` | `login.py` → `cgi_py.bbs` / 状態変更 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.bbsを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=chocofarm`: チョコボ牧場 | `旧版_ver2/chocofarm.cgi` | `login.py` → `cgi_py.chocofarm` / 表示 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.chocofarmを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=morifarm`: チョコボの森 | `旧版_ver2/morifarm.cgi` | `login.py` → `cgi_py.morifarm` / 表示・更新 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.morifarmを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=choco`: チョコボの森（互換ルート） | `旧版_ver2/morifarm.cgi` | `login.py` → `cgi_py.morifarm` / 表示 | Ver3で`morifarm`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.morifarmへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=crace`: チョコボレース | `旧版_ver2/crace.cgi` | `login.py` → `cgi_py.crace` / 状態変更 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.craceを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=ctrain`: チョコボ訓練 | `旧版_ver2/ctrain.cgi` | `login.py` → `cgi_py.ctrain` / 状態変更 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.ctrainを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=dendo`: チョコボ殿堂 | `旧版_ver2/dendo.cgi` | `login.py` → `cgi_py.dendo` / 表示・更新 | 状態変更ルートをPOST専用＋共通CSRF検証へ変更 | 意図的 | 差異あり | GET直打ちはlogin.pyで拒否し、ログイン済みセッションを確認してからモジュールを遅延ロードする。 |
| ルート `mode=farmrace`: チョコボ王者戦 | `旧版_ver2/farmrace.cgi` | `login.py` → `cgi_py.farmrace` / 状態変更 | 状態変更ルートをPOST専用＋共通CSRF検証へ変更 | 意図的 | 差異あり | GET直打ちはlogin.pyで拒否し、ログイン済みセッションを確認してからモジュールを遅延ロードする。 |
| ルート `mode=system`: 登録者一覧・画像一覧・他者詳細 | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | 公開閲覧をlogin.pyの許可リストで明示 | 意図的 | 差異あり | 未ログインでも閲覧可。状態更新POSTは該当モジュール側の本人確認・共通CSRF検証を必要とする。 |
| ルート `mode=chara_sts`: 他者詳細（system互換ルート） | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | Ver3で`system`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.systemへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=img_list`: 画像一覧（system互換ルート） | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | Ver3で`system`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.systemへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=ranking`: 登録者一覧（system互換ルート） | `旧版_ver2/system.cgi` | `login.py` → `cgi_py.system` / 表示 | Ver3で`system`への互換別名を明示 | 意図的 | 差異あり | login.pyのFUNCTION_MAPでcgi_py.systemへ集約。旧URL・既存フォームを維持しつつ、POST時は共通CSRF検証を通す。 |
| ルート `mode=tenka`: 天下一武道会 | `旧版_ver2/tenka.cgi` | `login.py` → `cgi_py.tenka` / 表示・状態変更 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.tenkaを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
| ルート `mode=rank`: 英雄ランキング | `旧版_ver2/rank.cgi` | `login.py` → `cgi_py.rank` / 表示 | 公開閲覧をlogin.pyの許可リストで明示 | 意図的 | 差異あり | 未ログインでも閲覧可。状態更新POSTは該当モジュール側の本人確認・共通CSRF検証を必要とする。 |
| ルート `mode=chocorank`: チョコボランキング | `旧版_ver2/chocorank.cgi` | `login.py` → `cgi_py.chocorank` / 表示 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.chocorankを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |

## 実行操作一覧

### 認証・登録

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| トップ／ログイン前画面（`（others.py）` / GET / 表示） | `旧版_ver2/others.cgi` | `others.py / templates/others.html` | UTF-8テンプレート画面へ移行 | 意図的 | 差異あり | 公開のログイン・登録導線をothers.pyで表示。認証済み状態を前提にしない。 |
| 新規登録入力（`mode=chara_make` / POST / 表示） | `旧版_ver2/others.cgi / chara_make.cgi` | `others.py / templates/chara_make.html` | 入力画面をJinja化しCSRFを追加 | 意図的 | 差異あり | 職業・画像・ID等の入力を表示し、POST確認画面へ渡す。 |
| 新規登録確認（`mode=make_pre` / POST / 表示） | `旧版_ver2/chara_make.cgi` | `chara_make.py / templates/chara_make_pre.html` | サーバー側検証と確認トークンを追加 | 意図的 | 差異あり | 入力形式・重複ID/名前/ホストを確認し、確定処理へ必要な値だけを渡す。 |
| 新規登録確定（`mode=make_end` / POST / 状態変更） | `旧版_ver2/chara_make.cgi` | `chara_make.py` | 統合JSON・PBKDF2保存へ移行 | 意図的 | 差異あり | 初期能力・装備・職歴・倉庫を原子的に生成する。初期ゲーム値の対応は所有・進行台帳で確認済み。 |
| ログイン（`mode=log_in` / POST / 状態変更） | `旧版_ver2/login.cgi` | `login.py` | 平文照合Cookieからハッシュ照合・暗号化セッションへ移行 | 意図的 | 差異あり | POST+CSRFで認証し、旧形式は成功時だけ再ハッシュ、日次バックアップ後に街へ遷移する。 |
| ログアウト（`mode=log_out` / POST/GET / 状態変更） | `旧版_ver2/login.cgi` | `login.py` | 暗号化セッション破棄へ移行 | 意図的 | 差異あり | destroy_sessionで認証Cookieを破棄しothers.pyへ遷移する。 |
| 合言葉を設定（`mode=passset` / POST / 状態変更） | `旧版_ver2/passchange.cgi` | `cgi_py/passchange.py` | 本人確認をセッション・CSRF前提へ変更 | 意図的 | 差異あり | 新規登録時に未作成だった合言葉だけを設定する。現在のパスワードと未設定状態を確認し、合言葉・保存時刻・接続元ホストを保存する。 |
| パスワード変更確定（`mode=passchan` / POST / 状態変更） | `旧版_ver2/passchange.cgi` | `cgi_py/passchange.py` | PBKDF2更新・セッション再発行へ変更 | 意図的 | 差異あり | 旧パスワード/合言葉と新値を検証する。新パスワードはVer2と同じ4〜8文字で、現行は画面の案内どおり半角英数字・記号だけを受け付ける。保存済みハッシュ・接続元ホスト・認証状態を更新する。 |

### 街・プロフィール

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 街のメイン画面（`mode=main` / GET/POST / 表示） | `旧版_ver2/ffadventure.cgi` | `cgi_py/ffadventure.py` | テンプレート表示と共有ニュース/BBS分離 | 意図的 | 差異あり | 能力・王者・待機時間・現職クラスを計算し、all_messageとbbsを別データとして表示する。チャンピオン戦以外の戦闘導線はbattle_count>0を確認して表示する。 |
| レジェンド挑戦を中断して街へ戻る（`mode=main, legend_cancel=1` / POST / 状態変更） | `旧版_ver2/ffadventure.cgi` | `cgi_py/ffadventure.py` | POST+CSRFで進行値をリセット | 意図的 | 差異あり | legend_cancel時だけboss_flagを設定初期値へ戻す。 |
| 自分のステータスを表示（`mode=sts` / POST / 表示） | `旧版_ver2/sts.cgi` | `cgi_py/sts.py` | 名前付き状態・テンプレート表示へ移行 | 意図的 | 差異あり | 能力、アクセサリー補正、現職クラス、職業熟練度を現行データから組み立てる。ホームページ名・URLは現行スキーマから意図的に除外する。 |
| 画像・発動コメントを変更（`mode=st_buy` / POST / 状態変更） | `旧版_ver2/sts.cgi` | `cgi_py/sts.py` | 入力値検証を追加 | 意図的 | 差異あり | 画像IDとコメント長・禁止語を検査する。Ver2と同じくロック後に最新charaを読み込み、画像・コメント・接続元ホストを保存する。 |
| 戦術一覧を表示（`mode=tac_change` / POST / 表示） | `旧版_ver2/tac_change.cgi` | `cgi_py/tac_change.py` | 利用可否をJSON職歴から算出 | 意図的 | 差異あり | 現職の戦術と、master_tactics_enabled=1のときのLv60以上の他職戦術を表示する。これはVer2のmaster_tacと同じ独立設定で、転職時の選択戦術リセットとは分けている。 |
| 戦術を変更（`mode=senjutu_henkou` / POST / 状態変更） | `旧版_ver2/tac_change.cgi` | `cgi_py/tac_change.py` | POST時の戦術ID・利用条件検証を追加 | 意図的 | 差異あり | 未選択・不正・未習得の戦術を拒否する。Ver2と同じくロック後に最新のchara/syokuから候補を再構築し、tactic_idと接続元ホストを保存する。 |
| 転職画面を表示（`mode=tensyoku` / POST / 表示） | `旧版_ver2/tensyoku.cgi` | `cgi_py/tensyoku.py` | 職業マスターをJSONから参照 | 意図的 | 差異あり | 能力・職歴前提を満たす候補と未マスター候補を分けて表示する。 |
| 転職を実行（`mode=tensyoku_change` / POST / 状態変更） | `旧版_ver2/tensyoku.cgi` | `cgi_py/tensyoku.py` | 実行POSTでも前提職を再検証 | 意図的 | 差異あり | 現職Lvを退避、転職先Lvを復帰し、必要なら戦術を初期化する。成功時はVer2と同じく接続元ホストを更新し、chara/syokuを同時保存する。能力減少値は一致し、カルマの下限だけはVer2の0許容に対して現行は1へ戻す意図的仕様。 |
| 掲示板へ投稿（`mode=post` / POST / 状態変更） | `旧版_ver2/post_message.cgi` | `cgi_py/bbs.py` | 私信一体型からBBS専用JSONへ分離 | 意図的 | 差異あり | 本人ID・200文字・禁止語を検査し、新着順と保存上限を守って書込む。 |

### 店・資産

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 宿泊（`mode=yado` / POST / 状態変更） | `旧版_ver2/shop.cgi` | `cgi_py/shop.py` | 状態更新をshop.pyへ集約 | 意図的 | 差異あり | 料金確認後にHPを回復し、王者表示用状態とレジェンド進行の宿屋処理を更新する。 |
| 銀行を表示（`mode=bank` / POST / 表示） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 統合JSONのgold/bankを表示 | 意図的 | 差異あり | 本人の所持金・預金と上限を表示し、変更はしない。 |
| 銀行へ預け入れ（`mode=bank_sell` / POST / 状態変更） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 入力検証と原子的保存を追加 | 意図的 | 差異あり | 1,000G単位・所持金/預金上限を検査してgoldからbankへ移す。 |
| 銀行から引き出し（`mode=bank_buy` / POST / 状態変更） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 入力検証と原子的保存を追加 | 意図的 | 差異あり | 1,000G単位・預金残高・所持金上限を検査してbankからgoldへ移す。 |
| 倉庫を表示（`mode=souko` / POST / 表示） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 3種別配列を統合表示 | 意図的 | 差異あり | 装備中とsouko_weapon/armor/accessoryを分け、変更操作は本人確認下だけで受け付ける。 |
| 武器店を表示（`mode=shop_weapon` / POST / 表示） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 個別店CGIを種別モジュールへ分離 | 意図的 | 差異あり | 武器マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。 |
| 武器を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 購入POSTの入力・職業・所持金検証を追加 | 意図的 | 差異あり | 武器IDをマスター参照し、職業制限・価格・倉庫上限を確認して倉庫へ追加する。 |
| 武器を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 売却対象を倉庫要素へ限定 | 意図的 | 差異あり | 武器の保管番号を検証し、売値をgold上限内で加算して対象要素を削除する。 |
| 防具店を表示（`mode=shop_armor` / POST / 表示） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 個別店CGIを種別モジュールへ分離 | 意図的 | 差異あり | 防具マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。 |
| 防具を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 購入POSTの入力・職業・所持金検証を追加 | 意図的 | 差異あり | 防具IDをマスター参照し、職業制限・価格・倉庫上限を確認して倉庫へ追加する。 |
| 防具を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 売却対象を倉庫要素へ限定 | 意図的 | 差異あり | 防具の保管番号を検証し、売値をgold上限内で加算して対象要素を削除する。 |
| 装飾品店を表示（`mode=shop_accessory` / POST / 表示） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 個別店CGIを種別モジュールへ分離 | 意図的 | 差異あり | 装飾品マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。 |
| 装飾品を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 購入POSTの入力・職業・所持金検証を追加 | 意図的 | 差異あり | 装飾品IDをマスター参照し、職業制限・価格・倉庫上限を確認して倉庫へ追加する。 |
| 装飾品を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 売却対象を倉庫要素へ限定 | 意図的 | 差異あり | 装飾品の保管番号を検証し、売値をgold上限内で加算して対象要素を削除する。 |
| 装備中の武器を倉庫へ外す（`mode=weapon_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 装備と倉庫を統合JSONで同時更新 | 意図的 | 差異あり | 装備中の武器を倉庫へ退避し、初期武器へ戻す。倉庫上限と二重登録を検査する。 |
| 倉庫の武器を装備（`mode=weapon_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 倉庫番号を配列添字として検証 | 意図的 | 差異あり | 選択武器を装備し、既存装備を倉庫へ退避する。武器/防具では職業制限も再検証する。 |
| 倉庫の武器を削除（`mode=weapon_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 個別店CGIを種別モジュールへ分離 | 意図的 | 差異あり | 武器マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。 |
| 装備中の防具を倉庫へ外す（`mode=armor_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 装備と倉庫を統合JSONで同時更新 | 意図的 | 差異あり | 装備中の防具を倉庫へ退避し、初期防具へ戻す。倉庫上限と二重登録を検査する。 |
| 倉庫の防具を装備（`mode=armor_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 倉庫番号を配列添字として検証 | 意図的 | 差異あり | 選択防具を装備し、既存装備を倉庫へ退避する。武器/防具では職業制限も再検証する。 |
| 倉庫の防具を削除（`mode=armor_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 個別店CGIを種別モジュールへ分離 | 意図的 | 差異あり | 防具マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。 |
| 装備中の装飾品を倉庫へ外す（`mode=accessory_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 装備と倉庫を統合JSONで同時更新 | 意図的 | 差異あり | 装備中の装飾品を倉庫へ退避し、初期装飾品へ戻す。倉庫上限と二重登録を検査する。 |
| 倉庫の装飾品を装備（`mode=accessory_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 倉庫番号を配列添字として検証 | 意図的 | 差異あり | 選択装飾品を装備し、既存装備を倉庫へ退避する。武器/防具では職業制限も再検証する。 |
| 倉庫の装飾品を削除（`mode=accessory_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 個別店CGIを種別モジュールへ分離 | 意図的 | 差異あり | 装飾品マスター、価格、職業制限、所持品を読み取り表示し、状態は変更しない。 |

### 戦闘・対戦

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| チャンピオンに挑戦（`mode=battle` / POST / 状態変更） | `旧版_ver2/battle.cgi / wbattle.pl` | `cgi_py/battle.py / sub_def/battle_logic.py` | POST専用・結果表示mode明示 | 意図的 | 差異あり | 待機後に王者状態で戦い、結果・王者更新・経験値上限は戦闘/所有台帳の確認結果に従う。 |
| 道場の入口を表示（`mode=log_in` / POST / 表示） | `旧版_ver2/select_battle.cgi` | `cgi_py/select_battle.py` | テンプレート入口とPOST+CSRFへ移行 | 意図的 | 差異あり | battle_count>0を表示・実行の双方で検査する。名前の完全一致検索または一覧選択へ進むだけで、保存状態は変更しない。 |
| 対人相手を選択（`mode=sentaku` / POST / 表示） | `旧版_ver2/select_battle.cgi` | `cgi_py/select_battle.py` | 相手IDをサーバー側で再検証・本人選択を拒否 | 意図的 | 差異あり | battle_count>0を検査する。存在しない相手と本人を拒否して選択画面だけを表示する。Ver2の候補一覧は24時間キャッシュ済みレベル降順だが、現行は全ユーザーを直接列挙するため表示順を保証しない。 |
| 選択相手と対戦（`mode=battle` / POST / 状態変更） | `旧版_ver2/select_battle.cgi / wbattle.pl` | `cgi_py/select_battle.py / sub_def/battle_logic.py` | 模擬戦を保存しないシミュレーションへ明示 | 意図的 | 差異あり | battle_count>0を検査する。相手の現在のキャラクター・装備で戦い、経験値・所持金・戦績・待機時刻を更新しない。時間切れwin=3は相打ちと別表示にする。 |
| 通常モンスター修行（`mode=monster` / POST / 状態変更） | `旧版_ver2/monster.cgi / mbattle.pl` | `cgi_py/monster.py / sub_def/battle_logic.py` | POST+CSRF・統合保存へ移行 | 意図的 | 差異あり | battle_count>0と出現表・修行回数を検査し、勝敗別報酬・戦績・職歴を保存する。戦闘後HPはレベルアップ後のvit/max_hpで回復する。 |
| 幻影の城へ挑戦（`mode=genei` / POST / 状態変更） | `旧版_ver2/monster.cgi / mbattle.pl` | `cgi_py/monster.py / sub_def/battle_logic.py` | monster.pyのgenei分岐へ統合 | 意図的 | 差異あり | battle_count>0、出現条件、修行回数、敵攻撃への防具補正、幻影報酬を通常修行と区別して処理する。戦闘後HPはレベルアップ後のvit/max_hpで回復する。 |
| 異世界へ挑戦（`mode=isekiai` / POST / 状態変更） | `旧版_ver2/monster.cgi / mbattle.pl` | `cgi_py/monster.py / sub_def/battle_logic.py` | monster.pyのisekiai分岐へ統合 | 意図的 | 差異あり | battle_count>0、レベル/進行条件と修行回数を検査し、異世界出現表と報酬を用いる。戦闘後HPはレベルアップ後のvit/max_hpで回復する。 |
| レジェンド攻略者一覧を閲覧（`mode=legend, view=ranking` / GET / 表示） | `旧版_ver2/legend.cgi` | `cgi_py/legend.py` | 公開GET閲覧を明示 | 意図的 | 差異あり | ログイン不要で攻略者を称号・戦績から並べ、状態変更は行わない。 |
| レジェンドの階層へ挑戦（`mode=boss, boss_file=0〜3` / POST / 状態変更） | `旧版_ver2/legend.cgi / mbattle.pl` | `cgi_py/legend.py / sub_def/battle_logic.py` | POST専用・階層値を検証、クリア後の再挑戦を許可 | 意図的 | 差異あり | battle_count>0、title_id、boss_flag、修行回数、待機時間を検査して階層別モンスターと戦う。クリア後は進行値を開始値へ戻し、現行は同じ階層を再挑戦できる。戦闘後HPはレベルアップ後のvit/max_hpで回復する。 |
| 天下一武道会ロビーを表示（`mode=tenka` / POST / 表示） | `旧版_ver2/tenka.cgi` | `cgi_py/tenka.py` | 24時間メンバーキャッシュへ移行 | 意図的 | 差異あり | battle_count>0を検査し、レベル上位者、参加可能boss_flag、進行ラウンド、制覇履歴を表示する。 |
| 天下一武道会で対戦（`mode=battle, no=1〜3` / POST / 状態変更） | `旧版_ver2/tenka.cgi / wbattle.pl` | `cgi_py/tenka.py / sub_def/battle_logic.py` | ラウンド番号をサーバー側照合、戦闘全体をユーザーロックで直列化 | 意図的 | 差異あり | battle_count>0と期待ラウンドを検査する。勝敗・進行のwin分岐は現行方針を維持し、戦闘前から保存までロックする。レベルアップ後のvit/max_hpで戦闘後HPを回復し、boss_flagが開始値を超える場合は開始値へ正規化する。 |

### 閲覧

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 英雄ランキングを表示（`mode=rank` / GET / 表示） | `旧版_ver2/rank.cgi` | `cgi_py/rank.py` | HTMLキャッシュからJSONキャッシュへ移行 | 意図的 | 差異あり | 部門別上位と勝率を24時間キャッシュから公開表示する。 |
| 登録者一覧を表示（`mode=ranking, shtm` / GET / 表示） | `旧版_ver2/system.cgi` | `cgi_py/system.py` | JSONキャッシュ・ページングへ移行 | 意図的 | 差異あり | 公開プレイヤーをレベル順にページ表示し、個人状態は更新しない。 |
| 他者の詳細ステータスを表示（`mode=chara_sts, id` / GET / 表示） | `旧版_ver2/system.cgi` | `cgi_py/system.py` | 公開GETの名前付き状態表示へ移行 | 意図的 | 差異あり | 対象IDの能力・装備・称号・マスター職を読み取り専用で表示する。 |
| キャラクター画像一覧を表示（`mode=img_list` / GET / 表示） | `旧版_ver2/system.cgi` | `cgi_py/system.py` | 設定の画像マスターを表示 | 意図的 | 差異あり | 公開画像IDとファイル対応を読み取り専用で出力する。 |

### チョコボ

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| チョコボ訓練: バーベルあげ（`mode=race0` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | バーベルあげ用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ訓練: 砂浜走り（`mode=race1` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | 砂浜走り用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ訓練: スイミング（`mode=race2` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | スイミング用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ訓練: 瞑想（`mode=race3` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | 瞑想用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ訓練: 猛特訓（`mode=race4` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | 猛特訓用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ訓練: お勉強（`mode=race5` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | お勉強用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ訓練: 坂道ダッシュ（`mode=race6` / POST / 状態変更） | `旧版_ver2/ctrain.cgi` | `cgi_py/ctrain.py` | 訓練modeを検証して統合chocoへ保存 | 意図的 | 差異あり | 坂道ダッシュ用modeのみを受け付け、待機・体力・20回試行・失敗副作用・寿命を処理して保存する。 |
| チョコボ牧場を表示（`mode=chocofarm` / POST / 表示） | `旧版_ver2/chocofarm.cgi` | `cgi_py/chocofarm.py` | チョコボ保存を統合JSON・共有JSONへ移行 | 意図的 | 差異あり | 所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。 |
| チョコボの森を表示（`mode=choco / morifarm` / POST / 表示） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | チョコボ保存を統合JSON・共有JSONへ移行 | 意図的 | 差異あり | 所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。 |
| 野生チョコボ候補を表示（`mode=choco_shop` / POST / 表示） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | チョコボ保存を統合JSON・共有JSONへ移行 | 意図的 | 差異あり | 所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。 |
| 野生チョコボを購入（`mode=choco_buy, item_no` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 所持中の直接POST上書きを拒否 | 意図的 | 差異あり | 候補ID・価格・未所持を再検証し、初期能力の個体と空の重賞履歴を同時保存する。 |
| お見合い相手を表示（`mode=choco_shopb` / POST / 表示） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | チョコボ保存を統合JSON・共有JSONへ移行 | 意図的 | 差異あり | 所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。 |
| お見合い・配合を実行（`mode=choco_buyb, item_no` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 親候補・所持状態を再検証 | 意図的 | 差異あり | 相手候補、所持個体、価格を検査して血統・能力上限・初期状態を計算し現役個体を置換する。 |
| チョコボに名前を付ける（`mode=choco_name` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 名称・禁止語・殿堂履歴の検証を追加 | 意図的 | 差異あり | 未所持/無名を検査し、既存殿堂名との重複を拒否してchoco.nameだけを更新する。 |
| チョコボを休ませる（`mode=yadoya` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 統合choco/charaの同時保存へ移行 | 意図的 | 差異あり | G5000・体力最大・所持を検査し、回復量、train、maxを更新する。 |
| チョコボを手放す（`mode=choco_sell` / POST / 状態変更） | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未所持値を明示消去し候補リストをJSON化 | 要判断 | 差異あり | 名前付き個体だけを性別別お見合い候補へ移し、chocoを空辞書へ戻す。候補固定枠廃止は要判断。 |
| チョコボ殿堂を表示（`mode=list` / POST / 表示） | `旧版_ver2/dendo.cgi` | `cgi_py/dendo.py / templates/chocofarm.html` | チョコボ保存を統合JSON・共有JSONへ移行 | 意図的 | 差異あり | 所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。 |
| チョコボを殿堂登録（`mode=dendo` / POST / 状態変更） | `旧版_ver2/dendo.cgi` | `cgi_py/dendo.py` | 重賞3個条件を追加 | 要判断 | 差異あり | Ver2にないG1/G2タイトル3個を検査し、同ID・同名は上書き、他は先頭追加する。 |
| チョコボランキングを表示（`mode=ranking` / POST / 表示） | `旧版_ver2/chocorank.cgi` | `cgi_py/chocorank.py` | チョコボ保存を統合JSON・共有JSONへ移行 | 意図的 | 差異あり | 所持判定、候補/ランキング/殿堂表示は読み取り専用で、空辞書を未所持として扱う。 |
| チョコボ王者戦（`mode=farmrace` / POST / 状態変更） | `旧版_ver2/farmrace.cgi` | `cgi_py/farmrace.py` | 王者状態を専用JSON・ロックで更新 | 意図的 | 差異あり | 所持・待機・同一王者を検査し、勝者/連勝/前王者と通知を更新する。 |
| チョコボレース: 新馬戦（`mode=race0` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race0をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| チョコボレース: 500万以下（`mode=race1` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race1をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| チョコボレース: 900万以下（`mode=race2` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race2をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| チョコボレース: 1600万以下（`mode=race3` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race3をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| チョコボレース: オープン特別（`mode=race4` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race4をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| チョコボレース: グレードIII（`mode=race5` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race5をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| チョコボレース: グレードII（`mode=race6` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race6をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボダービー（`mode=race7, race=1` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=1をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボスタリオン（`mode=race7, race=2` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=2をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボカップ（`mode=race7, race=3` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=3をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: ジェイドカップ（`mode=race7, race=4` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=4をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: BBA賞（`mode=race7, race=5` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=5をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボ春賞（`mode=race7, race=6` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=6をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボ秋賞（`mode=race7, race=7` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=7をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボキング（`mode=race7, race=8` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=8をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: チョコボステークス（`mode=race7, race=9` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=9をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: キングスカップ（`mode=race7, race=10` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=10をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G1レース: クイーンカップ（`mode=race7, race=11` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race7, race=11をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: シルバーカップ（`mode=race8, race=12` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=12をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: 新潟アドバンス（`mode=race8, race=13` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=13をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: チコスダービー（`mode=race8, race=14` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=14をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: チョコボードカップ（`mode=race8, race=15` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=15をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: チョコボエプソム（`mode=race8, race=16` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=16をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: チョコボ王（`mode=race8, race=17` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=17をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: ブリーダーズカップ（`mode=race8, race=18` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=18をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: ゴールドカップ（`mode=race8, race=19` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=19をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: プラチナカップ（`mode=race8, race=20` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=20をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: チョコボオークス（`mode=race8, race=21` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=21をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| G2レース: チョコボキングス（`mode=race8, race=22` / POST / 状態変更） | `旧版_ver2/crace.cgi` | `cgi_py/crace.py` | レースID・開催条件をサーバー側で検証 | 意図的 | 差異あり | mode=race8, race=22をcrace.pyで解決し、勝利数・性別・開催日・ライバル・寿命・賞金・run/win・トロフィーを処理する。 |
| 殿堂レジェンドレース（`mode=race_dendo` / POST / 状態変更） | `旧版_ver2/crace.cgi / denchoco.cgi` | `cgi_py/crace.py` | 殿堂JSONをライバル表へ利用 | 意図的 | 差異あり | race_dendoだけdenchoco.jsonを参照し、出走資格・寿命・結果報酬を通常レースと分けて処理する。 |

### 管理

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 管理画面を表示（`mode=kanri_top` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| 管理画面からログアウト（`mode=admin_log_out` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| 全体メッセージを投稿（`mode=post_all_message` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・型/範囲検証を追加 | 意図的 | 差異あり | 入力を検証して原子的に保存し、マスター更新時はID一意性・下限・参照可能性を確認する。 |
| マスター一覧を表示（`mode=master_list` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| マスターを編集表示（`mode=master_edit` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| マスターを保存（`mode=master_save` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・型/範囲検証を追加 | 意図的 | 差異あり | 入力を検証して原子的に保存し、マスター更新時はID一意性・下限・参照可能性を確認する。 |
| マスターを削除（`mode=master_delete` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・保護対象検査を追加 | 意図的 | 差異あり | 対象と削除可否を検証し、関連JSONを安全に処理する。未プレイ削除は保護IDを除外する。 |
| プレイヤー所持品を表示（`mode=player_item` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| プレイヤー所持品を追加（`mode=player_item_add` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・型/範囲検証を追加 | 意図的 | 差異あり | 入力を検証して原子的に保存し、マスター更新時はID一意性・下限・参照可能性を確認する。 |
| バックアップから復元（`mode=backup_restore` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | Ver2にない復元操作を追加 | 意図的 | 差異あり | 暗号化管理セッション・CSRF・maintenance_modeを要求し、入力名/固定復元元を検証して安全に復元する。 |
| 保護ユーザーを復元（`mode=restore_protected` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | Ver2にない復元操作を追加 | 意図的 | 差異あり | 暗号化管理セッション・CSRF・maintenance_modeを要求し、入力名/固定復元元を検証して安全に復元する。 |
| 全キャラクターデータを表示（`mode=kanri_all` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| 個別キャラクターデータを表示（`mode=data` / POST / 表示） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | hidden平文管理パスワードから暗号化管理セッションへ移行 | 意図的 | 差異あり | 表示操作も管理認証を確認し、一覧・編集対象を読み取り表示する。 |
| 個別キャラクターデータを保存（`mode=save` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・型/範囲検証を追加 | 意図的 | 差異あり | 入力を検証して原子的に保存し、マスター更新時はID一意性・下限・参照可能性を確認する。 |
| 個別キャラクターを削除（`mode=del_chara` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・保護対象検査を追加 | 意図的 | 差異あり | 対象と削除可否を検証し、関連JSONを安全に処理する。未プレイ削除は保護IDを除外する。 |
| 未プレイキャラクターを削除（`mode=del_noplay` / POST / 状態変更） | `旧版_ver2/admin.cgi / alldata.cgi` | `admin.py / templates/admin.html` | 管理セッション・CSRF・保護対象検査を追加 | 意図的 | 差異あり | 対象と削除可否を検証し、関連JSONを安全に処理する。未プレイ削除は保護IDを除外する。 |

