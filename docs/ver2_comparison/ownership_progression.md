# 所有・進行要素比較チェックリスト

プレイヤー固有・共有の状態が、どこで作成・更新・消去・参照されるかを比較する台帳です。マスターデータの値比較とは分離します。

## キャラクター・戦闘進行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| キャラクター作成時の初期状態 | `旧版_ver2/chara_make.cgi` | `chara_make.py` | JSON統合保存・PBKDF2認証へ移行（初期ゲーム値は同値） | 意図的 | 確認済み | Ver2/Ver3とも職業別初期8能力・Lv1・HP500・G5000・初期装備0・戦術0・修行回数・レジェンド進行初期値を設定。Ver3は職歴31件、倉庫・チョコボ空値を統合JSONで明示し、Ver2のsite/url・平文パスワードは保持しない。 |
| 職業熟練度とマスター職 | `旧版_ver2/syoku.cgi / tensyoku.cgi` | `cgi_py/tensyoku.py / cgi_py/sts.py / sub_def/common.py` | JSONの職ID→熟練度へ移行し、転職実行時にも前提職を再検証 | 意図的 | 確認済み | 両版とも現職Lvを退避して転職先Lvを復帰、Lv60をマスター表示に用いる。Ver3は表示だけでなくPOST時もjob_reqsを検証し、Lv60超の既存値を成長処理で正規化する。 |
| 装備中の武器・防具・アクセサリー | `旧版_ver2/item/<ID>.cgi` | `user_all.json:equipment / cgi_py/shop_*.py / cgi_py/souko.py` | 個別itemレコードからequipmentオブジェクトへ統合 | 意図的 | 確認済み | 装備IDと性能スナップショットを保持し、ショップ・倉庫交換時にキャラクター状態と同時保存する。初期値は武器0・防具0・アクセ0で一致し、現行は名前付き項目と原子的保存に変更。 |
| 倉庫の武器 | `旧版_ver2/souko/item/<ID>.cgi` | `user_all.json:souko_weapon / sub_def/common.py:souko_*` | 1行1品の専用ファイルからsouko_weapon配列へ統合 | 意図的 | 確認済み | 購入・装備交換・廃棄は現行souko.pyで件数上限を確認して配列を更新する。重複品を配列要素として保持する点はVer2の行単位保存と同じ。 |
| 倉庫の防具 | `旧版_ver2/souko/def/<ID>.cgi` | `user_all.json:souko_armor / sub_def/common.py:souko_*` | 1行1品の専用ファイルからsouko_armor配列へ統合 | 意図的 | 確認済み | 購入・装備交換・廃棄の件数制限と、個別スナップショットを保持する構造を確認。Ver3はキャラクター・倉庫を一括保存する。 |
| 倉庫のアクセサリー | `旧版_ver2/souko/acs/<ID>.cgi` | `user_all.json:souko_accessory / sub_def/common.py:souko_*` | 1行1品の専用ファイルからsouko_accessory配列へ統合 | 意図的 | 確認済み | effect_idを含むアクセサリー定義を倉庫要素として保持し、装備交換・廃棄時に上限を検査する。保存形式以外の所有数・重複品の扱いは同じ。 |
| 戦績・戦闘回数・勝利数 | `旧版_ver2/charalog/<ID>.cgi` | `user_all.json:chara / cgi_py/monster.py / battle.py / tenka.py` | charalog列からbattle_count/win_countへ名称化 | 意図的 | 確認済み | 通常モンスター、チャンピオン、レジェンド、天下一で戦闘回数を加算し、勝利時のみ勝利数を加算する。対人練習戦は保存更新しない。ランキング表示は両値から勝率を算出する。 |
| 修行回数・待機時刻 | `旧版_ver2/charalog/<ID>.cgi / mbattle.pl:time_check` | `user_all.json:chara.battle_limit,last_time / 各戦闘CGI` | charalog列からbattle_limit/last_timeへ名称化 | 意図的 | 確認済み | 通常・レジェンドは修行回数を消費し、チャンピオン・天下一は結果にかかわらず上限まで補充する。各戦闘CGIは完了時にlast_timeを更新し、設定値の待機時間で検査する。 |
| レジェンドの進行フラグ・称号 | `旧版_ver2/legend.cgi / charalog` | `user_all.json:chara.boss_flag,title_id / cgi_py/legend.py` | 進行列・称号列をboss_flag/title_idへ名称化し、クリア後は開始値へ戻して再挑戦可能化 | 要判断 | 確認済み | 階層選択は称号値で制限し、勝利でboss_flagを減算、敗北・引分では開始値へ戻す。Ver2は階層クリア時にboss_flag=0を保持し、結果画面から続行できない。現行はtitle_idを上げた後にboss_flagを開始値へ戻して再挑戦可能にする意図的な継続仕様であり、実際に加算するEXPも結果へ表示する。 |
| 人間チャンピオン | `旧版_ver2/datalog/winner.cgi / battle.cgi` | `save_data/champion.json / cgi_py/battle.py` | winner.cgiの連番レコードからchampion.jsonの名前付き状態へ移行。時間切れと新王者保存順を修正 | 不具合修正 | 確認済み | 通常の勝利・相打ち引分は挑戦者を王者へ交代し、敗北では王者の連勝・最高連勝を更新する。新王者は戦闘EXPのレベルアップ後に保存するため、本人とchampion.jsonの能力値・最大HP・現在HPが一致する。時間切れwin=3は引分表示として、王者交代・賞金・連勝を発生させず通常EXPのみを得る。勝利・相打ち引分EXPは相手Lv×基準値、敗北EXPだけmin(相手Lv, 自分Lv×10)へ調整済み。 |
| 天下一武道会の参加者・対戦履歴 | `旧版_ver2/all_tenka.cgi / tenka_log.cgi` | `save_data/all_tenka.json,tenka_log.json / cgi_py/tenka.py` | all_tenka/tenka_logをJSONキャッシュ化し、履歴上限を設定値で明示 | 要判断 | 確認済み | 両版ともレベル上位者の状態スナップショットと対戦時点の装備を組み合わせ、制覇時に履歴先頭へ追加する。Ver3は24時間キャッシュとtenka_log_limitで履歴を切り詰める一方、Ver2の履歴件数判定は変数名の不整合を含む。対戦時はキャラクターロックを取得してからロード・戦闘・保存まで保持し、重複送信による待機/進行更新の競合を防ぐ。 |

## チョコボ所有・レース進行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| チョコボ所持判定と未所持値 | `旧版_ver2/chocolog/<ID>.cgi` | `user_all.json:choco / sub_def/common.py:is_choco_owned` | ファイル有無判定から必須キーを持つ辞書の実体判定へ変更 | 意図的 | 確認済み | Ver2はchocologファイルが存在すれば所持扱い。Ver3は空辞書・欠損辞書を未所持とし、引退時にchocoを明示消去するため、空データを所持扱いする不整合を防ぐ。 |
| 飼育中チョコボの基本状態 | `旧版_ver2/chocolog/<ID>.cgi` | `user_all.json:choco / cgi_py/morifarm.py` | 33列のchocologレコードから名前付きchoco辞書へ移行 | 意図的 | 確認済み | 名前・性別・血統・画像番号・type・maxmax・能力上限c0〜c6・寿命life・train/run/win・max・gold・父母を保持する。Ver3はチョコボ内に平文パスワードを複製しない。 |
| 野生チョコボの候補・購入 | `旧版_ver2/morifarm.cgi / chocobofile.cgi` | `cgi_py/morifarm.py / data/chocobo/chocobofile.json` | 候補データをJSON化し、購入POSTでも未所持を検証 | 意図的 | 確認済み | 両版とも野生候補を1〜5件抽選し、価格を支払って初期life=100・能力/上限=10・run/win/train=0の個体を作る。候補自体は消費せず、現行は直接POSTによる所持チョコボ上書きを拒否する。 |
| 引退・お見合い候補リスト | `旧版_ver2/chocoboms.cgi / chocoboos.cgi` | `save_data/chocoboms.json,chocoboos.json / cgi_py/morifarm.py` | 固定99枠の行ファイルからJSONリスト＋設定上限へ変更 | 要判断 | 確認済み | 性別別リストへ引退個体の戦績・血統・価格を移し、配合相手の候補にする基本設計は同じ。Ver3は実リスト長を基準に置換し、空リストも許容してchocobo_partner_list_limitで切詰めるため、Ver2の固定ID枠とは候補選出が異なり得る。 |
| 配合後の子チョコボ | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 保存形式と排他制御のみ変更（配合計算をPythonへ移植） | 意図的 | 確認済み | 異性のお見合い候補を選び、父母・血統・性別・画像・type・能力上限・初期能力・life=1000・戦績0を生成して現役個体を置換する。現行は親候補の存在と所持状態をサーバー側で再検証し、統合JSONへ保存する。 |
| 訓練・休養による状態変化 | `旧版_ver2/ctrain.cgi / morifarm.cgi` | `cgi_py/ctrain.py / cgi_py/morifarm.py` | 保存形式をJSON化し、不正mode・未所持を明示検証 | 意図的 | 確認済み | 訓練は20回試行、train+1・life-50・max+5、能力上限・潜在力・寿命処理を引き継ぐ。休養はG5000、lifeに200〜499加算（1000超過時max追加）、train+1・max+10で、計算式はVer2と対応する。 |
| 通常レースの戦績・クラス進行 | `旧版_ver2/crace.cgi` | `cgi_py/crace.py / user_all.json:choco` | レース状態・相手をJSON化し、入力modeを明示検証 | 意図的 | 確認済み | run/win/gold・寿命・クラス到達条件を個体状態へ反映し、通常レース・重賞・殿堂レースを同じ個体データで進行する。現行は候補読み込みと結果保存を原子的に行い、無効なレース種別を受け付けない。 |
| G1/G2の個人トロフィー履歴 | `旧版_ver2/chocog1/<ID>.cgi` | `user_all.json:choco_g1 / cgi_py/crace.py` | chocog1の22列レコードからchoco_g1のr1〜r22辞書へ移行 | 意図的 | 確認済み | 重賞勝利時だけ対象レースIDを1として保存し、同一レースの再勝利は同じ個人フラグを維持する。開催日・性別・レース進行の条件はcraceの分岐で処理し、保存は個体と分離されたまま引退後も残す。 |
| チョコボ殿堂の共有リスト | `旧版_ver2/denchoco.cgi / dendo.cgi` | `save_data/denchoco.json / cgi_py/dendo.py` | denchoco行レコードからJSON＋トロフィー名の埋込へ移行。重賞3個を登録条件に追加 | 要判断 | 確認済み | 同一ID・同名は上書き、異なる個体は先頭追加する。Ver2のdendo.cgiはテストID以外に重賞数を検査しないが、Ver3はG1/G2 3個未満を拒否するため、この追加制限の採否を確認する必要がある。 |
| チョコボ王者 | `旧版_ver2/chocowinner.cgi / farmrace.cgi` | `save_data/chocobo_champion.json / cgi_py/farmrace.py` | farmwinner行レコードからchocobo_champion.jsonへ移行 | 意図的 | 確認済み | 現王者への挑戦、勝者の個体・ブリーダー情報への交代、敗北時の連勝・前王者情報の更新を維持する。現行は欠損した旧キーを正規化し、王者共有データを専用ロックで保存する。 |

## 記録・共有状態

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| ログイン履歴 | `旧版_ver2/loginlog/<ID>.cgi` | `user_all.json:login_log / login.py` | 移行先login_logは残るが、現行ログイン処理から更新呼出しがない | 要判断 | 確認済み | Ver2 login.cgiはloginlog/<ID>.cgiを読んで日時・IP等を追加し上限処理する。Ver3にはlogin_log_load/login_log_registと移行項目があるが、login.pyからlogin_log_registを呼ばないため、新規ログイン履歴が蓄積されない。 |
| 受信・送信メッセージ | `旧版_ver2/message / sousin` | `user_all.json:message / save_data/<ID>/message_sent.json` | 変換先のmessage/message_sentは残るが、現行の送受信・既読・削除CGIが見当たらない | 要判断 | 確認済み | Ver2はmessage/sousinとpost_message.cgiで私信・送信箱・件数制限を扱う。Ver3のスキーマには受信messageとmessage_sentがあるものの、現行CGIから読み書きする経路を確認できず、機能廃止か未移植かを決める必要がある。 |
| 全体メッセージ・掲示板 | `旧版_ver2/datalog/message.cgi / post_message.cgi` | `save_data/all_message.json / cgi_py/bbs.py / admin.py` | 全体ニュース(all_message)とプレイヤー掲示板(bbs)を別JSONへ分離 | 意図的 | 確認済み | Ver3は管理者・登録・イベント通知をall_messageへ、一般投稿をbbsへ保存し、双方を新着順・設定件数で切詰める。Ver2のpost_message.cgiは私信・制限操作を含む一体型であり、表示経路は再編されている。 |
| 登録者・ランキング用キャッシュ | `旧版_ver2/alldata.cgi / rank.cgi` | `save_data/system_rank_cache.json / cgi_py/system.py / rank.py` | HTML出力キャッシュからJSONデータキャッシュへ移行 | 意図的 | 確認済み | 両版とも全登録者をレベル順に集計し、約24時間単位で再生成する。Ver3はsystem_rank_cacheとrank_cacheを分け、キャッシュ欠損・必要項目欠損時も再構築し、テンプレートで安全に表示する。 |
