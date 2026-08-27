# 保存・認証・移行・運用比較チェックリスト

現行の安全対策・JSON保存形式はVer2と意図的に異なる可能性があります。差異を見つけた時点で、互換性・安全性・運用上の必要性を分けて判断します。

## 入力・表示・認証

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| CGIパラメータの復号・文字列処理 | `旧版_ver2/regist.pl / login.cgi` | `sub_def/common.py:decode_params` | 未確認 | 未判定 | 未確認 | GET/POSTの優先順位、複数値、文字コード、空値・不正値 |
| CGI入口のUTF-8標準入出力 | `旧版Ver2 CGIの出力設定` | `others.py,login.py,chara_make.py,admin.py:reconfigure` | 未確認 | 未判定 | 未確認 | Windows Apache CP932環境、4入口の維持、UTF-8ヘッダーとの整合 |
| HTML出力・リダイレクトのヘッダー | `旧版_ver2/regist.pl:header / footer` | `sub_def/utils.py:render_template,redirect` | 未確認 | 未判定 | 未確認 | Content-Type、UTF-8、キャッシュ制御、Location、例外時出力 |
| セッションCookieの暗号化・改ざん検証 | `旧版_ver2/login.cgi:set_cookie` | `sub_def/crypto.py:encrypt_data,decrypt_data,get_session,save_session` | 未確認 | 未判定 | 未確認 | Cookie内容、署名、期限、HttpOnly、旧Cookieとの関係 |
| ログイン・ログアウト | `旧版_ver2/login.cgi:log_in` | `login.py` | 未確認 | 未判定 | 未確認 | ID・パスワード検証、セッション更新、記憶Cookie、日次バックアップの起点 |
| パスワード形式とログイン時移行 | `旧版Ver2の保存パスワード` | `sub_def/crypto.py:hash_password,verify_password,needs_rehash / login.py` | 未確認 | 未判定 | 未確認 | 平文・旧ハッシュ・PBKDF2の受入範囲、成功時再ハッシュ |
| CSRFトークンの生成・検証・再生成 | `旧版Ver2のフォーム送信` | `sub_def/crypto.py:token_generate,token_regenerate,token_check` | 未確認 | 未判定 | 未確認 | 対象POST、トークン寿命、再表示時、エラー時 |
| 本人操作の認可（IDOR対策） | `旧版Ver2のID・パスワード照合` | `sub_def/common.py:require_owner / 各状態変更CGI` | 未確認 | 未判定 | 未確認 | 対象操作、Cookieとの照合、ロック前検証、閲覧操作との区別 |

## JSON保存・ロック

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 統合ユーザー保存形式 | `旧版_ver2/charalog,item,syoku,souko等の分割ファイル` | `save_data/<ID>/user_all.json / sub_def/file_ops.py` | 未確認 | 未判定 | 未確認 | セクション構成、必須・任意キー、旧分割データとの対応 |
| ユーザーデータのキー順・旧キー正規化 | `旧版Ver2の配列列番号` | `sub_def/data_schema.py:order_user_data` | 未確認 | 未判定 | 未確認 | title→title_id、unused30→tactic_id、site/url削除、未知キー保持 |
| 装備・アクセサリー保存値の正規化 | `旧版_ver2/item/<ID>.cgi` | `sub_def/data_schema.py:_order_equipment / sub_def/common.py` | 未確認 | 未判定 | 未確認 | 武器・防具・アクセ順、bonus8能力、旧アクセキー、説明補完 |
| HTMLエンティティの読込正規化 | `旧版のHTML保存文字列` | `sub_def/file_ops.py:_normalize_loaded_data / sub_def/common.py:decode_html_entities` | 未確認 | 未判定 | 未確認 | 再帰対象、二重復号、名前・コメント・ログへの影響 |
| 単一JSONの原子的書込み | `旧版_ver2/regist.pl:chara_regist ほか` | `sub_def/file_ops.py:_write_json_atomically,save_data_atomically` | 未確認 | 未判定 | 未確認 | 一時ファイル、fsync、os.replace、例外時の残存一時ファイル |
| read-modify-writeの原子更新 | `旧版_ver2/regist.pl:lock / unlock` | `sub_def/file_ops.py:update_data_atomically` | 未確認 | 未判定 | 未確認 | 読込から保存までの同一ロック、default値、更新関数の例外 |
| ユーザー・共有データのロック | `旧版_ver2/regist.pl:lock / unlock` | `sub_def/common.py:get_lock,release_lock / sub_def/lock_state.py` | 未確認 | 未判定 | 未確認 | ロック名、再入、タイムアウト、ディレクトリロック、必ず解放すること |
| バックアップ中のスナップショット排他 | `旧版には相当処理なし` | `sub_def/file_ops.py:backup_snapshot.lock / sub_def/backup.py` | 未確認 | 未判定 | 未確認 | 通常保存とバックアップの順序、デッドロック、保存待機 |
| 部分更新API | `旧版の複数ファイル個別保存` | `sub_def/common.py:save_user_sections,souko_regist,choco_regist` | 未確認 | 未判定 | 未確認 | 他セクションを消さないこと、読込失敗時、呼出元のロック |

## バックアップ・管理復元

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 日次バックアップ作成 | `旧版_ver2/save_log.cgi` | `sub_def/backup.py:create_daily_backup,ensure_daily_backup` | 未確認 | 未判定 | 未確認 | 実行契機、対象範囲、同日再実行、失敗時のログイン継続 |
| バックアップのマニフェスト・世代削除 | `旧版_ver2/save_log.cgi` | `sub_def/backup.py:_write_manifest,_prune_daily_backups,list_daily_backups` | 未確認 | 未判定 | 未確認 | 件数・容量、形式検証、保持日数、壊れた世代の表示除外 |
| 管理画面からのバックアップ復元 | `旧版Ver2の手動復元運用` | `sub_def/backup.py:restore_daily_backup / admin.py:backup_restore` | 未確認 | 未判定 | 未確認 | maintenance_mode必須、パス検証、復元前退避、現在save_dataの置換 |
| 保護ユーザーの復元 | `旧版Ver2の保護データ運用` | `admin.py:protected_backup_path,restore_protected_users` | 未確認 | 未判定 | 未確認 | 対象ID、JSON妥当性、個別ロック、上書き範囲 |
| 管理画面によるマスター保存・削除 | `旧版_ver2/admin.cgi` | `admin.py:validate_master_record,save_master_records` | 未確認 | 未判定 | 未確認 | ID一意性、型・下限、JSON妥当性、アクセサリーキャッシュ無効化 |

## 旧版からの移行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| Ver1→Ver2変換 | `旧版_ver1/セーブデータ移行用ファイル/convert_to_ver2.py` | `docs/migration_specs.html（履歴資料）` | 未確認 | 未判定 | 未確認 | 入力・出力の列対応、原本保持、dry-run、Ver3比較対象外であること |
| Ver2→Ver3ユーザー本体変換 | `旧版_ver2/charalog/<ID>.cgi` | `旧版_ver2/change_data/convert_all.py / sub_def/data_schema.py` | 未確認 | 未判定 | 未確認 | 列番号→charaキー、能力値順、パスワード、戦績、戦術・称号 |
| Ver2→Ver3装備・職業・倉庫変換 | `旧版_ver2/item,syoku,souko` | `旧版_ver2/change_data/convert_all.py` | 未確認 | 未判定 | 未確認 | マスター参照、装備性能、職業熟練度、倉庫件数、旧形式の残存 |
| Ver2→Ver3ログ・共有データ変換 | `旧版_ver2/loginlog,message,sousin,datalog` | `旧版_ver2/change_data/convert_all.py` | 未確認 | 未判定 | 未確認 | message_sentの別保存、champion.json、all_message.json、欠損時 |
| Ver2チョコボの移行時初期化 | `旧版_ver2のチョコボ保存データ` | `旧版_ver2/change_data/convert_all.py / docs/migration_specs.html` | 未確認 | 未判定 | 未確認 | 現役チョコボを移さずchoco/choco_g1を空辞書にする意図、既存データとの衝突 |
| 変換の文字コード・検証用出力 | `旧版Ver2のCP932テキスト` | `旧版_ver2/change_data/convert_all.py` | 未確認 | 未判定 | 未確認 | CP932読込、文字化け置換、dry-run、検証先出力、現行save_dataを直接上書きしないこと |
