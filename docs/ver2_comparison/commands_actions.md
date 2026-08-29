# コマンド・行動比較チェックリスト

画面遷移だけのルートと、各ルート内の実行操作を分けて管理します。比較前に状態変更か表示かを確認し、Ver2との差分を具体的に記録します。

対象: ルート 38件、実行操作 122件、二次精査 24ファイル。
## ファイル単位の精査記録

ここには一次台帳作成後に、Ver2実装と現行実装を分岐・保存値・表示まで再確認したファイルだけを記録します。未記載のファイルは未精査であり、一次比較完了を根拠に一致と扱いません。

| Ver3対象ファイル | Ver2確認箇所 | 確認範囲 | Ver2との差異 | 意図的な仕様か否か | 備考・根拠 |
| --- | --- | --- | --- | --- | --- |
| `cgi_py/tac_change.py` | `旧版_ver2/tac_change.cgi / data/ffadventure.ini:master_tac` | 表示・変更の候補条件、マスター職、ロック後再検証、接続元ホスト | master_tacを転職時の戦術リセット設定と誤って共用していた | 不具合を修正済み | master_tactics_enabledを独立設定として追加し、Ver2と同じくLv60以上の他職戦術を候補にする。POST時は最新chara/syokuで再検証する。 |
| `cgi_py/tensyoku.py` | `旧版_ver2/tensyoku.cgi` | 転職条件、職業Lv退避・復帰、能力減少、戦術、接続元ホスト | 転職成功時の接続元ホスト保存が欠けていた。カルマ下限はVer2と異なる | ホストは不具合を修正済み／カルマ下限1は意図的 | 成功時にREMOTE_ADDRを保存する。能力減少値と職業Lv遷移は一致。Ver2のカルマ0許容に対し、現行は0も1へ戻す既決仕様を維持する。 |
| `cgi_py/passchange.py / chara_make.py` | `旧版_ver2/passchange.cgi / chara_make.cgi` | 合言葉設定、パスワード変更、新規登録時の入力規則、接続元ホスト | 新パスワードの許可文字と変更成功時の接続元ホスト保存が不一致 | 不具合を修正済み | 4〜8文字の半角英数字・記号を許可し、全角・空白・制御文字を拒否する。passchan成功時はREMOTE_ADDRを保存し、PBKDF2とセッション再発行は現行の意図的な安全化として維持する。 |
| `cgi_py/shop.py` | `旧版_ver2/shop.cgi` | 宿代、HP回復、王者HP、boss_flag、接続元ホスト | 宿泊成功時の接続元ホスト保存が欠けていた | 不具合を修正済み | 宿代Lv×10、HP全快、王者HP全快、boss_flagの10への復帰は一致。成功時にREMOTE_ADDRも保存する。 |
| `cgi_py/bank.py` | `旧版_ver2/bank.cgi / data/ffadventure.ini` | 預入・引出、半角数値、1,000G単位、所持金・預金上限、接続元ホスト | 全角数字を受理し、預金上限超過時は画面案内と異なり拒否していた | 不具合を修正済み | ASCII数字だけを受理する。預金上限超過分は画面案内どおり国への寄付として所持金から差し引き、預金へは上限までだけ加算する。 |
| `cgi_py/souko.py` | `旧版_ver2/souko.cgi / data/ffadventure.ini:item_max,def_max,acs_max` | 武器・防具・装飾品の表示、着脱、交換、破棄、上限、接続元ホスト | 交換時の保管順、着脱時の接続元保存、破棄確認がVer2と異なる | 要判断 | 3種別の上限は8で一致。現行は選択品を配列から取り出し、旧装備を末尾へ追加する。Ver2は選択位置を旧装備で置換する。現行は着脱でREMOTE_ADDRを保存せず、破棄は二段階確認を挟まない。どちらを採るかは現行の操作性を含めて判断する。 |
| `cgi_py/shop_weapon.py / templates/shop_trade.html` | `旧版_ver2/shop_item.cgi / data/item/item<N>.ini` | 職別品揃え、購入・売却額、倉庫上限、接続元ホスト、画面遷移 | JSON・CSRF・入力再検証・トースト遷移へ移行。武器1181の販売対象だけ未判断 | 処理移行は意図的／武器1181は要判断 | 購入・売却額は両版とも価格の2/3、購入時のREMOTE_ADDR保存と武器倉庫上限8は一致する。職別品揃えは、台帳記載のシーフ武器1032〜1038価格調整を除き一致。皇帝用1181はVer2の職別リストにないが現行では販売するため、維持可否はequipment.mdの要判断項目として残す。 |
| `cgi_py/shop_armor.py / templates/shop_trade.html` | `旧版_ver2/shop_def.cgi / data/def/def<N>.ini` | 職別品揃え、購入・売却額、倉庫上限、接続元ホスト、画面遷移 | JSON・CSRF・入力再検証・トースト遷移へ移行。売却時の接続元保存と防具2181の販売対象が異なる | 処理移行は意図的／接続元・防具2181は要判断 | 購入・売却額は両版とも価格の2/3、購入時のREMOTE_ADDR保存と防具倉庫上限8は一致する。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しない。皇帝用2181はVer2の職別リストにないが現行では販売する。2165・2183の名称記号差はequipment.mdに記録済み。 |
| `cgi_py/shop_accessory.py / templates/shop_trade.html` | `旧版_ver2/shop_acs.cgi / data/acs/acs<N>.ini` | 職別品揃え、能力補正の保管、購入・売却額、倉庫上限、接続元ホスト、画面遷移 | JSON・CSRF・入力再検証・トースト遷移へ移行。売却時の接続元保存はVer2と異なる | 処理移行は意図的／売却時の接続元は要判断 | 購入・売却額は両版とも価格の2/3、購入時のREMOTE_ADDR保存と装飾品倉庫上限8は一致する。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しない。職別品揃えと補正は一致し、85・87の率補正だけはd7105f6で記録済みのVer1準拠調整を維持する。 |
| `cgi_py/bbs.py / templates/ffadventure.html` | `旧版_ver2に一般掲示板はなし（post_message.cgiは私信）` | 投稿者・本文・禁止語・保存上限・表示順・接続元・遷移 | 全員が書き込む掲示板をVer3で新設。Ver2の私信とは別機能 | 一般掲示板は意図的な追加／私信の未実装は要判断 | ログイン本人だけが200文字以内・禁止語なしで投稿でき、最新100件を新着順に共有JSONへ保持する。投稿後のPRGリダイレクト、CSRF、共有ロックは現行の安全化。Ver2の私信・送信箱・受信拒否・友人登録は置き換えられておらず、別の未実装項目として記録する。 |
| `cgi_py/ffadventure.py / templates/ffadventure.html` | `旧版_ver2/ffadventure.cgi` | 本人認証、王者・待機時間、戦闘導線、レジェンド進行、クラス、施設、共有表示 | テンプレート・CSRF・共有ニュース・一般掲示板へ移行。レジェンド進行中の入口挙動が異なる | 画面・安全化は意図的／レジェンド進行継続は要判断 | 戦闘回数0ではモンスター・幻影・異世界・道場・武道会・レジェンドを表示段階で止め、20秒待機、クラス、宿代Lv×10、称号段階は一致する。Ver2はboss_flagが10以外ならレジェンド入口から挑戦させない。現行は進行状態を保ち、legend_cancelの明示POSTでのみ10へ戻すため、継続可能な現行挙動を維持するか要判断。 |
| `cgi_py/sts.py / templates/sts.html` | `旧版_ver2/sts.cgi` | 本人の詳細表示、能力・率計算、現職クラス、職業熟練度、アイコン・発動コメント更新、接続元ホスト | テンプレート・CSRF・本人確認・入力検証へ移行。ホームページ名・URLは現行スキーマで扱わない | 画面・安全化・プロフィール項目の整理は意図的 | 命中=dex/10+51（上限150）、回避=agi/20（上限50）、必殺=karma/15+10+job_level（上限75）、装備補正、現在職のクラス表示、100文字・禁止語制限、更新時のREMOTE_ADDR保存は確認した。Ver2のsite/urlだけは現行スキーマから除外し、現行はアイコン番号を設定済み画像へ制限する。能力名の括弧内説明は実装との対応が曖昧だったため、既決方針で非表示にしている。 |
| `cgi_py/battle.py` | `旧版_ver2/battle.cgi / wbattle.pl:sentoukeka` | 王者挑戦、待機・ロック、戦績、経験値・賞金、王者交代、防衛、HP回復、レジェンド・修行回数、保存順 | 時間切れの王者側更新と敗北経験値上限がVer2と異なる。JSON・本人認証・原子的保存へ移行 | 時間切れ・敗北経験値は既決仕様／移行・安全化は意図的 | 対人時間切れwin=3は経験値だけを得て、王者交代・賞金・防衛連勝・次回賞金を発生させない。Ver2は時間切れ時に王者の防衛側更新を行う。敗北EXPはVer2の相手Lvそのままではなくmin(相手Lv, 自分Lv×10)に制限する。通常勝利・相打ちwin=2の王者交代、敗北時の半額、boss_flagと修行回数の復帰、レベルアップ後に新王者と戦闘後HPを確定する順は確認した。 |
| `cgi_py/select_battle.py / templates/select_battle.html` | `旧版_ver2/select_battle.cgi / regist.pl:all_name_search / wbattle.pl` | 道場入口、名前・一覧による相手選択、待機、模擬戦、保存有無、初回解放 | 全ユーザーの直接列挙、POST・CSRF・本人照合へ移行。初回チャンピオン戦前の直接実行も拒否する | 安全化・解放条件の入口側強制は意図的 | 名前の完全一致検索、本人との対戦拒否、待機20秒、対人BattleSimulator、経験値・所持金・戦績・待機時刻を保存しない点は確認した。Ver2の候補一覧はキャッシュ済みRANKINGを使う一方、現行は保存済み全ユーザーを直接列挙する。Ver2は街画面で初回解放を隠すだけだが、現行はbattle_count>0を入口・直接POSTの双方で検査する。 |
| `cgi_py/monster.py` | `旧版_ver2/monster.cgi / mbattle.pl:sentoukeka,hp_after` | 通常修行・幻影の城・異世界、入口条件、出現抽選、待機・回数、勝敗報酬、盗み、戦績、回復、保存順 | 直接実行時の解放・異世界Lv制限、20秒待機、敗北EXP0、JSON重み抽選へ移行。幻影・異世界の後続モンスター技呼出しが異なる | 入口検証・待機・敗北EXP0・抽選移行は既決仕様／後続技呼出しは要判断 | Ver2の重複行数と現行weight合計は初級193・中級169・上級45・最上級121・異世界95で全て一致する。通常・幻影・異世界の回数消費、勝敗時の所持金、戦績、boss_flag復帰、レベルアップ後のHP回復、接続元保存は確認した。現行はbattle_count>0と異世界Lv300を実行側でも検査し、待機は設定値20秒、敗北EXPは0とする。Ver2は幻影・異世界でmons_atowazaを呼ばないが、現行の全モンスターIDの同フックは空実装のため、現時点で実効差はない。将来効果を追加する前に呼出し範囲を判断する。 |
| `cgi_py/legend.py / templates/monster_result.html / templates/legend_error.html` | `旧版_ver2/legend.cgi / mbattle.pl:legend_sentoukeka,hp_after / data/bossmons0〜3.ini` | 公開ランキング、階層選択、入口条件、ボス進行、勝敗報酬、称号、連戦、待機、回復、保存順 | 公開ランキング・CSRF/POSTルーティング・連戦導線を追加。クリア後の進行値、レジェンド入口のboss_flag検証、階層値検証がVer2と異なる | 階層値検証は不具合を修正済み／連戦・クリア後再挑戦は意図的 | 各階層は両版とも11体で、boss_flag 10から1へ減らして0で階層クリアする。Ver2の通常画面はboss_flagが10以外なら入口を隠すが、legend.cgi自体は進行値を検証しないため、直接POSTでは0番目の行を参照する不整合な再入場が可能だった。現行は7754ecaで開始値10へ戻し、同階層を正しく最初から再挑戦できる。勝利・引分・敗北の経験値、所持金、battle_count、battle_limit、title_id、レベルアップ後HP回復、接続元保存を照合した。実行はlogin.pyがPOST・CSRFを検証する。範囲外・数値外のboss_fileは第1階層へフォールバックしていたため拒否へ修正した。 |
| `cgi_py/tenka.py / templates/tenka.html / templates/tenka_result.html / templates/tenka_error.html` | `旧版_ver2/tenka.cgi / wbattle.pl:sentoukeka / battle.pl:winner_data` | 24時間参加者キャッシュ、入口・ラウンド照合、対戦相手・装備、勝敗報酬、進行、制覇履歴、待機、回復、保存順 | JSON/CSRF/ロック・履歴上限・全体通知へ移行。引分・時間切れ・敗北の進行はVer2と異なる | 進行分岐は既決の現行仕様／ロビーの途中再開表示と説明文は不具合を修正済み | 参加者は両版とも24時間ごとにレベル上位3人を固定し、対戦時はその能力スナップショットと最新装備を組み合わせる。相手順は3位→2位→1位で一致し、ラウンド番号を現行はサーバー側でも照合する。Ver2は全勝敗でboss_flagを減らし、相打ちは勝利、時間切れは次戦へ進行、敗北後は9となる。現行は勝利だけ進行し、相打ち・時間切れは進めず、敗北も開始状態を保つ既決方針を維持する。battle_limit補充、経験値、所持金、レベルアップ後HP回復、接続元保存を確認した。Ver2の制覇履歴は変数名誤記で実質1件、現行は設定値20件を保持する。途中進行時に第1回戦を再送するロビー導線と、実装と異なる5名・順位交換の説明を修正した。 |
| `cgi_py/rank.py / templates/rank.html` | `旧版_ver2/rank.cgi / regist.pl:all_data_read` | 公開表示、24時間キャッシュ、全登録者数、11部門の集計・上位10件、勝率対象・端数処理、プロフィール導線 | 静的HTMLキャッシュからJSONキャッシュとテンプレート表示へ移行。外部ホームページ欄を廃止 | JSON・表示刷新・URL除外は意図的／勝率条件コメントは実装どおりに整理済み | レベル、最大HP、力・知能・信仰心・生命力・器用さ・速さ・魅力・カルマ、勝率の11部門は全て対応し、各上位10件の値も一致する。勝率は両版ともbattle_countが1,000超だけを対象にし、win_count×10000÷battle_countを小数第2位まで切り捨てる。24時間更新・登録者数・個人詳細への公開リンクは維持する。現行は画像を追加し、Ver2の外部ホームページ列はプロフィールURLを扱わない現行スキーマに合わせて表示しない。 |
| `cgi_py/system.py / templates/system_ranking.html / templates/system_chara_sts.html / templates/system_img_list.html` | `旧版_ver2/system.cgi:ranking_no_html,chara_sts,img_list / regist.pl:all_data_read` | 公開ルート、24時間登録者キャッシュ、レベル順・20件ページング、他者詳細の能力・装備・率・称号・職業、画像一覧 | 静的HTMLからJSONキャッシュ・テンプレート・公開GETへ移行。他者詳細の公開項目とバー上限が異なる | クラス欠落・範囲外ページ番号・性別/所持金の非公開は不具合を修正済み | レベル降順、20件単位、削除期限、勝率、能力値・装備補正・命中/回避/必殺・称号・マスター職、画像ID一覧を照合した。現行はキャッシュの必須キーを検証し、負数は0・過大なshtmは最終ページへ正規化する。Ver2と同じ7段階の職業クラス、性別、所持金を他者詳細へ復元した。外部ホームページURLだけは現行スキーマから除外する。バーはCSS幅100%へ正規化する表示差で、計算値自体は一致する。 |
| `sub_def/battle_logic.py` | `旧版_ver2/battle.pl / mbattle.pl / wbattle.pl` | 戦闘状態、Lv・職業基礎ダメージ、装備補正、必殺・後続効果、クリティカル、命中・回避、HP精算、勝敗、レベルアップ | 初期Python移植時から欠けていたターンLv基礎ダメージを復元。状態オブジェクト・構造化ログへ移行 | Lv基礎ダメージは不具合を修正済み／同時精算と部分先行停止の混在は既知の保留 | 通常・幻影・異世界・レジェンドはLv×(rand(5)+1)、対人は双方Lv×(rand(3)+1)を職業式と武器ATKへ加算する。全31職の能力参照を再確認し、上級職のカルマはall_stats・職24・職25で固定加算とする。必殺技・モンスター技の個別効果はskills.md・monster_skills.mdで別途照合済み。Ver2は同時精算だが、現行は撃破見込みの敵通常ダメージだけを止めるため、速度・死亡中断を含む一貫した行動順を決めるまで変更しない。 |
| `cgi_py/chocorank.py / templates/chocorank.html` | `旧版_ver2/chocorank.cgi:ranking,rank / chocolog/*.cgi / rireki.cgi` | 飼育中チョコボ抽出、24時間キャッシュ、勝数・訓練数・7能力・獲得賞金の各Top 10、能力ランク、重賞制覇履歴、牧場への復帰 | JSON・ロック・テンプレートへ移行。現行テンプレートが別形式のranksを参照し、集計済みのrankings/rirekiを表示していなかった | テンプレート契約と能力ランク境界は不具合を修正済み／JSON保存・24時間キャッシュ・数値併記は意図的 | Ver2の10部門（勝数、訓練数、筋力、スタミナ、粘り、落ち着き、闘争心、賢さ、反射神経、獲得賞金）を各10件・同じ並びで表示する。退役済みの空データはcommon.choco_loadで対象外とし、賞金は両版とも保存値の100倍を表示する。能力画像はVer2の厳密な>100、>200、>400、>600、>800、>1000境界に戻す。キャッシュ版を上げて旧ランク番号を即時再構築する。現行は画像だけだったVer2に実数値も併記し、キャッシュの最終更新時刻も表示する。重賞履歴はr1〜r22を全レース名と○/−で表示する。 |
| `cgi_py/chocofarm.py / cgi_py/crace.py / templates/chocofarm.html` | `旧版_ver2/chocofarm.cgi / crace.cgi / choco-farm.pl` | 本人用牧場、チョコボ・王者表示、能力ランク、クラス・体調、訓練・一般レース・G1/G2開催導線、重賞タイトル、海外重賞解放、復帰フォーム | JSON・CSRF・セッション本人確認・テンプレートへ移行。本人以外の牧場表示と海外重賞直接POSTの条件検証が欠け、重賞のG1/G2色情報をテンプレートへ渡す前に破棄していた | 本人確認・直接POST検証・重賞色分け・自己チョコボ詳細の表示量は不具合を修正済み | クラス境界、体調、一般レースの勝数範囲、G1の40回・G2の60回周期、性別限定最終枠は一致する。牧場の能力画像はVer2もint(能力/100)であり、ランキング画面の厳密な閾値判定とは別仕様のため変更しない。海外重賞の解放はVer2のrenzと同じr1〜r22合計3個以上をcrace.pyでも検証する。現行は待機終了をちょうど設定秒で許可し、Ver2の1秒後判定より操作性を優先する。自己チョコボの画像・性別・血統・訓練数・7能力ランクと実数値を表示へ復元し、ステータスカードを2カラム全幅、訓練・お世話・アドバイス・関連施設を後続の2カラムへ再配置した。 |
| `cgi_py/morifarm.py / templates/morifarm.html` | `旧版_ver2/morifarm.cgi / choco-farm.pl / chocobofile.cgi / chocoboos.cgi / chocoboms.cgi` | 野生チョコボ探索・購入、お見合い候補・配合、血統/能力/性別/タイプ乱数、命名、休養、引退と候補リスト、重賞履歴、本人認証・CSRF | JSON・テンプレート・本人認証へ移行。状態変更フォームはCSRFトークンを出力していたが、処理側の検証が欠けていた。配合のprebirth乱数はVer2の合算後切捨てを個別切捨てへ誤移植していた | CSRF検証、空名の直接配合拒否、prebirth乱数、配合時の乱数分布、引退金と誤認させる表示は不具合を修正済み／候補枠は現行仕様を維持 | 野生購入時の初期値、候補数1〜5、血統表、能力上限・初期能力、休養の5,000G・200〜499回復・max加算は一致する。Ver2のprebirthはint(rand(相手祖先合計)+rand(自分祖先合計))であり、合算してから切り捨てる。配合時の性別と突然変異画像・タイプは、Ver2のint(rand(1.9))・int(rand(7.999))・int(rand(5.1))へ修正し、端数を含む分布を再現する。候補は現行の性別別・設定上限100件のJSONリストを維持する。Ver2の性別ごとの固定99枠、および同じ育て親の引退個体を25%で追加表示する挙動は採用しない。メス親時のVer2は相手決定前の父名を使う不具合があり、現行の選択相手名を使う実装を維持する。引退でキャラクター所持金は増えず、候補としての想定引取額だけを記録する。重賞履歴はVer2が世代をまたいで残すのに対し、現行は野生購入・配合時に新世代用へ空にする意図的仕様。 |
| `cgi_py/dendo.py / templates/dendo.html` | `旧版_ver2/dendo.cgi / crace2.cgi / rireki.cgi / denchoco.cgi` | 殿堂登録・同名更新、登録対象、重賞履歴、公開一覧、能力ランク、血統・戦績・トロフィー表示、本人認証・CSRF | JSON・テンプレート・本人認証へ移行。現行は一覧を認証済み利用者に限る。テンプレートは所有者の未定義参照、能力等の表示欠落、maxmaxの年齢誤表示、登録完了メッセージ未表示があった | CSRF検証と殿堂詳細表示の不備を修正済み／登録条件はVer2、一覧の公開範囲は現行仕様を維持 | Ver2と同じくIDとチョコボ名が一致する登録は先頭へ更新し、新規は先頭へ追加する。登録時はVer2どおり重賞数を問わず、名前付きの現役チョコボを対象とする。一覧はVer2ではログイン不要だが、現行の本人認証済み利用者限定を維持する。Ver2の殿堂一覧は画像・性別・タイプ・父母・戦績・訓練・能力ランク・重賞を表示しており、現行でも復元した。引退年齢として表示していたmaxmaxは年齢ではないため廃止し、想定引取額を表示する。現行は登録時点のトロフィーを殿堂データにスナップショットするため、世代交代後も記録が混ざらない。 |

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
| ルート `mode=bbs`: 掲示板投稿 | `旧版_ver2に一般掲示板はなし（post_message.cgiは私信）` | `login.py` → `cgi_py.bbs` / 状態変更 | 個別CGI入口からlogin.pyの集中ルーティングへ移行 | 意図的 | 差異あり | FUNCTION_MAPでcgi_py.bbsを選択し、ログイン済みならPOSTのCSRFを共通検証して実行する。 |
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
| 掲示板へ投稿（`mode=post` / POST / 状態変更） | `旧版_ver2に一般掲示板はなし（post_message.cgiは私信）` | `cgi_py/bbs.py` | Ver2にない一般掲示板を追加 | 意図的 | 差異あり | 本人ID・200文字・禁止語を検査し、新着順で最大100件を共有JSONへ書込む。私信を置換した機能ではなく、投稿後はPRGリダイレクトとCSRFを用いる独立機能である。 |
| 私信・受信拒否・友人登録（Ver2のみ）（`Ver2専用（message / all_list / limit / ban / friend）` / POST / Ver3未実装） | `旧版_ver2/post_message.cgi` | `該当なし` | Ver3に実行経路がない | 要判断 | 差異あり | Ver2のpost_message.cgiは私信送受信、送受信箱、全受信拒否、個別拒否、友人登録を扱う。現行スキーマには移行値が残るがCGIの読書き経路はないため、復元するか機能廃止とするか要判断。 |

### 店・資産

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 宿泊（`mode=yado` / POST / 状態変更） | `旧版_ver2/shop.cgi` | `cgi_py/shop.py` | 状態更新をshop.pyへ集約 | 意図的 | 差異あり | 料金確認後にHPを回復し、王者表示用状態とレジェンド進行の宿屋処理を更新する。Ver2と同じく接続元ホストも保存する。 |
| 銀行を表示（`mode=bank` / POST / 表示） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 統合JSONのgold/bankを表示 | 意図的 | 差異あり | 本人の所持金・預金と上限を表示し、変更はしない。 |
| 銀行へ預け入れ（`mode=bank_sell` / POST / 状態変更） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 入力検証と原子的保存を追加 | 意図的 | 差異あり | 半角数字の1,000G単位で、所持金を確認してgoldからbankへ移す。預金上限を超える分はVer2の画面案内どおり国への寄付としてgoldから差し引き、bankには上限までだけ加算する。成功時は接続元ホストも保存する。 |
| 銀行から引き出し（`mode=bank_buy` / POST / 状態変更） | `旧版_ver2/bank.cgi` | `cgi_py/bank.py` | 入力検証と原子的保存を追加 | 意図的 | 差異あり | 半角数字の1,000G単位で、預金残高・所持金上限を検査してbankからgoldへ移す。成功時は接続元ホストも保存する。 |
| 倉庫を表示（`mode=souko` / POST / 表示） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 3種別の保管ファイルを統合JSON配列・テンプレート表示へ移行 | 意図的 | 差異あり | 装備中とsouko_weapon/armor/accessoryを分けて表示する。Ver2の削除済み空行はJSON配列へ保持せず、現行では詰めて表示する。 |
| 武器店を表示（`mode=shop_weapon` / POST / 表示） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 職別販売ファイルをJSON抽出・共通テンプレートへ移行 | 意図的 | 差異あり | 装備中武器の価格は両版ともマスター価格の2/3で表示する。現行はCSRF付きフォーム、未選択を防ぐrequired、倉庫・街への導線を追加する。 |
| 武器を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 販売候補をJSONから再取得し、統合倉庫へ原子的に保存 | 意図的 | 差異あり | 職業別商品・所持金・武器倉庫8件・商品番号をサーバー側で確認し、価格を差し引いてREMOTE_ADDRと倉庫を保存する。商品1032〜1038の価格調整と1181の皇帝販売は装備台帳の判断に従う。 |
| 武器を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_item.cgi` | `cgi_py/shop_weapon.py` | 装備・所持金を統合JSONで同時保存し、結果をトースト表示 | 意図的 | 差異あり | 装備中だけをマスター価格の2/3で下取りし、gold上限で打ち止めにして素手へ戻す。売却時に接続元を保存しない点はVer2と同じ。 |
| 防具店を表示（`mode=shop_armor` / POST / 表示） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 職別販売ファイルをJSON抽出・共通テンプレートへ移行 | 意図的 | 差異あり | 装備中防具の価格は両版ともマスター価格の2/3で表示する。現行はCSRF付きフォーム、未選択を防ぐrequired、倉庫・街への導線を追加する。 |
| 防具を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 販売候補をJSONから再取得し、統合倉庫へ原子的に保存 | 意図的 | 差異あり | 職業別商品・所持金・防具倉庫8件・商品番号をサーバー側で確認し、価格を差し引いてREMOTE_ADDRと倉庫を保存する。商品2181の皇帝販売は装備台帳の判断に従う。 |
| 防具を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_def.cgi` | `cgi_py/shop_armor.py` | 装備・所持金を統合JSONで同時保存し、結果をトースト表示 | 要判断 | 差異あり | 装備中だけをマスター価格の2/3で下取りし、gold上限で打ち止めにして衣服へ戻す。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しないため維持可否は要判断。 |
| 装飾品店を表示（`mode=shop_accessory` / POST / 表示） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 職別販売ファイルをJSON抽出・共通テンプレートへ移行 | 意図的 | 差異あり | 装備中装飾品の価格は両版ともマスター価格の2/3で表示する。現行は説明をdescriptionまたは能力補正から組み立て、CSRF付きフォーム・倉庫・街への導線を追加する。 |
| 装飾品を購入（`mode=buy` / POST / 状態変更） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 販売候補をJSONから再取得し、統合倉庫へ原子的に保存 | 意図的 | 差異あり | 職業別商品・所持金・装飾品倉庫8件・商品番号をサーバー側で確認し、価格を差し引いてREMOTE_ADDRと能力補正を含む倉庫要素を保存する。85・87の率補正は意図的なVer1準拠調整を維持する。 |
| 装飾品を売却（`mode=sell` / POST / 状態変更） | `旧版_ver2/shop_acs.cgi` | `cgi_py/shop_accessory.py` | 装備・所持金を統合JSONで同時保存し、結果をトースト表示 | 要判断 | 差異あり | 装備中だけをマスター価格の2/3で下取りし、gold上限で打ち止めにして補正なしへ戻す。Ver2は売却時にもREMOTE_ADDRを保存するが、現行は保存しないため維持可否は要判断。 |
| 装備中の武器を倉庫へ外す（`mode=weapon_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 着脱時の接続元保存を現行は省略 | 要判断 | 差異あり | 武器倉庫8件を確認してマスター値を退避し、素手へ戻す。Ver2はREMOTE_ADDRを保存するが、現行は装備・倉庫だけを更新する。 |
| 倉庫の武器を装備（`mode=weapon_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 現行は選択品を除去し、旧装備を末尾へ追加 | 要判断 | 差異あり | Ver2は選択した保管位置を旧装備で置換する。現行の並び替えを伴う方式を維持するかは要判断。職業制限はVer2・現行とも倉庫交換時に再検証しない。 |
| 倉庫の武器を削除（`mode=weapon_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | Ver2の二段階確認を現行は省略 | 要判断 | 差異あり | Ver2は確認画面を挟んでから削除するが、現行はCSRF付きの1回のPOSTで削除する。復元不能な操作のため確認を復元するか要判断。 |
| 装備中の防具を倉庫へ外す（`mode=armor_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 着脱時の接続元保存を現行は省略 | 要判断 | 差異あり | 防具倉庫8件を確認してマスター値を退避し、衣服へ戻す。Ver2はREMOTE_ADDRを保存するが、現行は装備・倉庫だけを更新する。 |
| 倉庫の防具を装備（`mode=armor_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 現行は選択品を除去し、旧装備を末尾へ追加 | 要判断 | 差異あり | Ver2は選択した保管位置を旧装備で置換する。現行の並び替えを伴う方式を維持するかは要判断。職業制限はVer2・現行とも倉庫交換時に再検証しない。 |
| 倉庫の防具を削除（`mode=armor_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | Ver2の二段階確認を現行は省略 | 要判断 | 差異あり | Ver2は確認画面を挟んでから削除するが、現行はCSRF付きの1回のPOSTで削除する。復元不能な操作のため確認を復元するか要判断。 |
| 装備中の装飾品を倉庫へ外す（`mode=accessory_remove` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 着脱時の接続元保存を現行は省略 | 要判断 | 差異あり | 装飾品倉庫8件を確認してマスター値を退避し、補正なしへ戻す。Ver2はREMOTE_ADDRを保存するが、現行は装備・倉庫だけを更新する。 |
| 倉庫の装飾品を装備（`mode=accessory_equip` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | 現行は選択品を除去し、旧装備を末尾へ追加 | 要判断 | 差異あり | Ver2は選択した保管位置を旧装備で置換する。現行の並び替えを伴う方式を維持するかは要判断。 |
| 倉庫の装飾品を削除（`mode=accessory_delete` / POST / 状態変更） | `旧版_ver2/souko.cgi` | `cgi_py/souko.py` | Ver2の二段階確認を現行は省略 | 要判断 | 差異あり | Ver2は確認画面を挟んでから削除するが、現行はCSRF付きの1回のPOSTで削除する。復元不能な操作のため確認を復元するか要判断。 |

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
| チョコボを殿堂登録（`mode=dendo` / POST / 状態変更） | `旧版_ver2/dendo.cgi` | `cgi_py/dendo.py` | JSON・CSRF・本人認証へ移行 | 意図的 | 差異あり | Ver2と同じく名前付きの現役チョコボを登録し、同ID・同名は上書き、他は先頭追加する。 |
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

