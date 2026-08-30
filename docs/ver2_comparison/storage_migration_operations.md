# 保存・認証・移行・運用比較チェックリスト

Ver2の保存形式・認証・管理CGIと、Ver3の実装を28項目で照合した台帳です。保存形式の差異と、安全対策・運用手順として残すべき差異を分けて記録します。

## 入力・表示・認証

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| CGIパラメータの復号・文字列処理 | `旧版_ver2/regist.pl / login.cgi` | `sub_def/common.py:decode_params` | Ver2はGET/POSTの一方だけを手動分解し、POSTは50KiB上限・SJIS変換・入力時HTMLエスケープ。Ver3はGETとPOSTをparse_qsで解析しPOST優先、UTF-8前提・出力時エスケープへ変更。現行に本文サイズ上限はない。 | 要判断 | 差異あり | Ver3のGET/POST優先はcommon.pyの明示仕様。Ver2の50KiB上限を廃止した理由は履歴に記録が見当たらないため、上限の要否を運用判断する。 |
| CGI入口のUTF-8標準入出力 | `旧版Ver2 CGIの出力設定` | `others.py,login.py,chara_make.py,admin.py:reconfigure` | Ver2はShift_JIS出力。Ver3はothers.py・login.py・chara_make.py・admin.pyの4入口でstdin/stdoutをUTF-8へ再構成する。 | 意図的 | 差異あり | Windows ApacheのCP932標準出力でUTF-8文字を出すための互換設定。4入口以外へ一律追加・削除はしない。 |
| HTML出力・リダイレクトのヘッダー | `旧版_ver2/regist.pl:header / footer` | `sub_def/utils.py:render_template,redirect` | Ver2はShift_JISのContent-typeとHTML直書き。Ver3はUTF-8ヘッダー、no-cache、Jinja自動エスケープ、302 Locationと開発サーバー用meta refreshを出力する。 | 意図的 | 差異あり | utils.pyはテンプレート例外の詳細をstderrだけへ出し、HTTP応答には汎用エラーだけを返す。 |
| セッションCookieの暗号化・改ざん検証 | `旧版_ver2/login.cgi:set_cookie` | `sub_def/crypto.py:encrypt_data,decrypt_data,get_session,save_session` | Ver2はIDと保存済みパスワードを60日Cookieへ平文で保存。Ver3は署名付き暗号化FFAPY_SESSION（既定30分・HttpOnly）へ移行し、30日CookieはID記憶だけに分離。Secure属性は未設定。 | 意図的 | 差異あり | 旧cookie_name APIは暗号化セッションへ橋渡しする互換層を残す。HTTPS化時のSecure属性は別途運用設定が必要。 |
| ログイン・ログアウト | `旧版_ver2/login.cgi:log_in` | `login.py` | Ver2は成功・失敗ともloginlogへ最大15件を書き、入力パスワードも記録する。Ver3は検証・セッション発行・日次バックアップを行うが、login.pyからlogin_log_registを呼ばず履歴を更新しない。 | 意図的 | 差異あり | 平文パスワードを含むVer2のログイン履歴機能は廃止で確定する。移行済みの過去ログは互換データとして残すが、login.pyから新規の成功・失敗履歴は追加しない。 |
| パスワード形式とログイン時移行 | `旧版Ver2の保存パスワード` | `sub_def/crypto.py:hash_password,verify_password,needs_rehash / login.py` | Ver2はcharalogの平文比較。Ver3はPBKDF2-SHA256（ユーザー別salt）を新形式とし、旧固定salt・平文も成功時だけ検証してPBKDF2へ再ハッシュする。 | 意図的 | 差異あり | verify_passwordは旧形式を読み取り互換に限定し、needs_rehashが真のときだけ保存値を更新する。 |
| CSRFトークンの生成・検証・再生成 | `旧版Ver2のフォーム送信` | `sub_def/crypto.py:token_generate,token_regenerate,token_check` | Ver2にCSRF照合はない。Ver3はセッション内ランダムトークンを主要POSTで定数時間比較する。token_regenerateは定義のみで、画面再表示は既存トークンを維持する。 | 意図的 | 差異あり | 別タブ・戻る操作で直ちに失効させない方針はutils.pyコメントで確認。セッション期限でのみ失効する。 |
| 本人操作の認可（IDOR対策） | `旧版Ver2のID・パスワード照合` | `sub_def/common.py:require_owner / 各状態変更CGI` | Ver2はリクエストid/passを各CGIで直接照合。Ver3は暗号化セッションを旧cookie互換値へ変換し、require_ownerまたは同等照合で対象ID・保存済みhashを確認する。 | 意図的 | 差異あり | shop・souko・チョコボ系等はrequire_owner、battle・monster・legend・bank・passchangeは同条件を個別実装。閲覧系には適用しない。 |

## JSON保存・ロック

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 統合ユーザー保存形式 | `旧版_ver2/charalog,item,syoku,souko等の分割ファイル` | `save_data/<ID>/user_all.json / sub_def/file_ops.py` | Ver2はcharalog/item/syoku/souko/loginlog/message等を別ファイル保存。Ver3は大半をuser_all.jsonのセクションへ統合し、送信箱だけmessage_sent.jsonに分離する。 | 意図的 | 差異あり | 変換器は各分割ファイルをchara・equipment・syoku・ログ・倉庫へ明示対応させる。 |
| ユーザーデータのキー順・旧キー正規化 | `旧版Ver2の配列列番号` | `sub_def/data_schema.py:order_user_data` | Ver2の列番号保存を、Ver3は名前付きJSONと固定キー順へ変更。title→title_id、unused30→tactic_idを移し、site/urlを除去し、未知キーは末尾に保持する。 | 意図的 | 差異あり | order_user_dataは既知の旧キーだけを変換し、任意の追加キーを破棄しない。 |
| 装備・アクセサリー保存値の正規化 | `旧版_ver2/item/<ID>.cgi` | `sub_def/data_schema.py:_order_equipment / sub_def/common.py` | Ver2の<>列を、Ver3はweapon/armor/accessory辞書とbonus8能力・3率へ正規化し、説明欠損はマスターから補完する。 | 意図的 | 差異あり | 変換器は武器・防具・アクセの列順を固定し、アクセ説明が空なら現行/旧マスターから補う。 |
| HTMLエンティティの読込正規化 | `旧版のHTML保存文字列` | `sub_def/file_ops.py:_normalize_loaded_data / sub_def/common.py:decode_html_entities` | Ver2は入力時にHTMLエンティティ化して保存。Ver3はJSON読込時に再帰的html.unescapeし、表示はテンプレートの自動エスケープへ委ねる。 | 意図的 | 差異あり | 互換データを読めるようにする処理。保存済みの多重エンティティを何段階まで復元するかは値に依存するため、移行検証で表示確認が必要。 |
| 単一JSONの原子的書込み | `旧版_ver2/regist.pl:chara_regist ほか` | `sub_def/file_ops.py:_write_json_atomically,save_data_atomically` | Ver2は対象ファイルを直接開いて上書き。Ver3は同一ディレクトリの一時JSONへflush/fsync後、os.replaceで置換する。 | 意図的 | 差異あり | 例外時は一時ファイルを削除して再送出するため、途中JSONを本体として公開しない。 |
| read-modify-writeの原子更新 | `旧版_ver2/regist.pl:lock / unlock` | `sub_def/file_ops.py:update_data_atomically` | Ver2は呼出側がlock/unlockと個別読書きを組み合わせる。Ver3は共有データ向けupdate_data_atomicallyが読込・更新・置換を同一ロックで実行する。 | 意図的 | 差異あり | user_all.jsonのsave_user_sectionsは呼出側がユーザーロックを保持する契約。全呼出元がこの契約を守ることが前提になる。 |
| ユーザー・共有データのロック | `旧版_ver2/regist.pl:lock / unlock` | `sub_def/common.py:get_lock,release_lock / sub_def/lock_state.py` | Ver2はsymlink/空ファイル/flockを設定で切替え、再試行・古いロック削除を行う。Ver3はos.mkdirディレクトリロック、同一スレッド再入管理、10/15秒タイムアウトと設定式の残存ロック自動回復を使う。 | 意図的 | 差異あり | finallyでrelease_lock/unlockする設計。Ver3はlock_stale_seconds（既定300秒）を超えた空ディレクトリだけを再取得時に削除し、0以下なら自動回復を無効化できる。 |
| バックアップ中のスナップショット排他 | `旧版には相当処理なし` | `sub_def/file_ops.py:backup_snapshot.lock / sub_def/backup.py` | Ver2に保存と全体コピーを直列化する仕組みはない。Ver3は通常保存・日次作成・復元がbackup_snapshotロックを共有する。 | 意図的 | 差異あり | 通常保存はsnapshot→個別、復元はrestore→snapshotの順で取得する。 |
| 部分更新API | `旧版の複数ファイル個別保存` | `sub_def/common.py:save_user_sections,souko_regist,choco_regist` | Ver2は関連ファイルを個別上書き。Ver3はsave_user_sectionsが統合データを読んで指定セクションだけ更新し、souko/chocoも同経路を使う。 | 意図的 | 差異あり | 指定しないセクションを消さないが、呼出側のユーザーロックなしでは読込後更新の競合を防げない。 |

## バックアップ・管理復元

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 日次バックアップ作成 | `旧版_ver2/admin.cgi:save_chara / save_log.cgi（保護一覧。日次バックアップなし）` | `sub_def/backup.py:create_daily_backup,ensure_daily_backup` | Ver2のsave_log.cgiは保護ユーザー一覧であり、日次バックアップ処理は確認できない。Ver3は当日初回ログイン時にsave_data全体を日付別コピーする。 | 意図的 | 差異あり | バックアップ失敗はstderr記録のみでログインを継続し、同日のmanifestがあれば再作成しない。 |
| バックアップのマニフェスト・世代削除 | `旧版Ver2には相当処理なし` | `sub_def/backup.py:_write_manifest,_prune_daily_backups,list_daily_backups` | Ver2にはバックアップ世代・検証情報がない。Ver3は件数・容量・作成時刻をmanifest.jsonへ記録し、既定40日を超える日付世代を削除する。 | 意図的 | 差異あり | 一覧は日付形式・manifest形式を検証し、壊れた世代を表示しない。 |
| 管理画面からのバックアップ復元 | `旧版_ver2/login.cgi:70（hukugen.cgiを参照するが同梱なし）` | `sub_def/backup.py:restore_daily_backup / admin.py:backup_restore` | Ver2 login.cgiはhukugen.cgiを参照するが同梱実装がなく、復元手順をコードで確認できない。Ver3は管理画面から日付バックアップを復元できる。 | 意図的 | 差異あり | Ver3は日付名検証、maintenance_mode必須、復元前全体退避、temp置換、snapshot/restoreロックを実装する。 |
| 保護ユーザーの復元 | `旧版_ver2/admin.cgi:save_chara / save_del` | `admin.py:protected_backup_path,restore_protected_users` | Ver2はsave_log.cgiで削除保護対象を列挙するだけ。Ver3はprotected_user_idsを削除対象外にし、固定user_all.jsonを優先して欠落・破損時だけ復元する。固定バックアップが無いtestは初期状態で再作成する。 | 意図的 | 差異あり | restore_protected_usersはchara.idを検証して個別ロック下で復元する。protected_user_backup_dirへの自動書込みは行わず、固定バックアップが無い場合の初期化対象は公開ゲストID test に限定する。 |
| 管理画面によるマスター保存・削除 | `旧版_ver2/admin.cgi` | `admin.py:validate_master_record,save_master_records` | Ver2管理画面はhidden平文管理パスワードを引き回し、テキストを直接上書き。Ver3は暗号化管理セッション・CSRF・JSON解析・ID/型/下限/職業ID検証・原子保存を行う。 | 意図的 | 差異あり | 職業は配列ID順を守るため削除不可。アクセサリー保存後は説明文キャッシュも無効化する。 |

## 旧版からの移行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| Ver1→Ver2変換 | `旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py` | `docs/migration_specs.html（履歴資料）` | Ver1→Ver2は過去世代間の変換であり、Ver3通常処理・Ver2→Ver3変換器の比較対象ではない。 | 該当なし | 対象外 | 履歴資料として入力列・dry-run・原本保持を残す。Ver3へ移す場合はVer2形式を経由してconvert_all.pyを使う。 |
| Ver2→Ver3ユーザー本体変換 | `旧版_ver2/charalog/<ID>.cgi` | `旧版_ver2/change_data/convert_all.py / sub_def/data_schema.py` | Ver2 charalogの固定35列をCHARA_COLUMNSで名前付きcharaへ写し、site/urlを除外、bankは34列目（残るbanklogがあればそちら優先）にする。 | 意図的 | 差異あり | 能力8値、job・HP・EXP・戦績・戦術・称号・職業Lvの列番号を明示し、validate_userで必須能力と旧キー残存を検証する。 |
| Ver2→Ver3装備・職業・倉庫変換 | `旧版_ver2/item,syoku,souko` | `旧版_ver2/change_data/convert_all.py` | Ver2のitem/syoku/soukoを、装備辞書・職業ID文字列辞書・種別倉庫配列へ変換する。旧charalog2形式の倉庫もマスター参照で受け付ける。 | 意図的 | 差異あり | アクセ8能力・3率・説明を正規化し、存在しない倉庫マスターはwarningを出して除外する。 |
| Ver2→Ver3ログ・共有データ変換 | `旧版_ver2/loginlog,message,sousin,datalog` | `旧版_ver2/change_data/convert_all.py` | Ver2 loginlog/message/sousin/datalogをJSON化し、送信箱はuser_all.json外のmessage_sent.json、winnerはchampion.json、全体文はall_message.jsonにする。 | 意図的 | 差異あり | 欠損ファイルは空値扱い。送信箱が空ならmessage_sent.jsonを作らず、winnerが無ければchampion.jsonを出力しない。 |
| Ver2チョコボの移行時初期化 | `旧版_ver2のチョコボ保存データ` | `旧版_ver2/change_data/convert_all.py / docs/migration_specs.html` | Ver2の現役チョコボ・個人G1履歴は変換せず、全ユーザーのchoco/choco_g1を空辞書で初期化する。 | 意図的 | 差異あり | convert_userの固定出力。旧チョコボを引き継がない仕様を明文化済みであり、既存Ver3データへ混在出力しない。 |
| 変換の文字コード・検証用出力 | `旧版Ver2のCP932テキスト` | `旧版_ver2/change_data/convert_all.py` | Ver2のCP932テキストをerrors=replaceで読み、<>分解後にHTMLエンティティを復元する。Ver3 JSONはUTF-8で、既定出力先はchange_data/users・shared、--dry-runは書込なし。 | 意図的 | 差異あり | --output等で現行save_dataを指定できるため、実運用はdry-run→検証用出力→バックアップ後配置の順を守る。 |
