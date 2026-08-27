# 所有・進行要素比較チェックリスト

プレイヤー固有・共有の状態が、どこで作成・更新・消去・参照されるかを比較する台帳です。マスターデータの値比較とは分離します。

## キャラクター・戦闘進行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| キャラクター作成時の初期状態 | `旧版_ver2/chara_make.cgi` | `chara_make.py` | 未確認 | 未判定 | 未確認 | 初期能力、職業、装備、所持金、戦術、battle_limit、boss_flag、チョコボ空値 |
| 職業熟練度とマスター職 | `旧版_ver2/syoku.cgi / tensyoku.cgi` | `cgi_py/tensyoku.py / cgi_py/sts.py / sub_def/common.py` | 未確認 | 未判定 | 未確認 | 職業別熟練度、Lv60、転職時の退避・復帰、表示 |
| 装備中の武器・防具・アクセサリー | `旧版_ver2/item/<ID>.cgi` | `user_all.json:equipment / cgi_py/shop_*.py / cgi_py/souko.py` | 未確認 | 未判定 | 未確認 | ID・性能スナップショット、職業制限、初期装備、削除時 |
| 倉庫の武器 | `旧版_ver2/souko/item/<ID>.cgi` | `user_all.json:souko_weapon / sub_def/common.py:souko_*` | 未確認 | 未判定 | 未確認 | 保存形式、件数、装備交換、削除、重複 |
| 倉庫の防具 | `旧版_ver2/souko/def/<ID>.cgi` | `user_all.json:souko_armor / sub_def/common.py:souko_*` | 未確認 | 未判定 | 未確認 | 保存形式、件数、装備交換、削除、重複 |
| 倉庫のアクセサリー | `旧版_ver2/souko/acs/<ID>.cgi` | `user_all.json:souko_accessory / sub_def/common.py:souko_*` | 未確認 | 未判定 | 未確認 | effect_id・能力補正・説明、装備交換、削除、重複 |
| 戦績・戦闘回数・勝利数 | `旧版_ver2/charalog/<ID>.cgi` | `user_all.json:chara / cgi_py/monster.py / battle.py / tenka.py` | 未確認 | 未判定 | 未確認 | battle_count、win_countの更新対象、練習戦除外、ランキング利用 |
| 修行回数・待機時刻 | `旧版_ver2/charalog/<ID>.cgi / mbattle.pl:time_check` | `user_all.json:chara.battle_limit,last_time / 各戦闘CGI` | 未確認 | 未判定 | 未確認 | 初期値、減算・回復契機、コンテンツ別待機時間 |
| レジェンドの進行フラグ・称号 | `旧版_ver2/legend.cgi / charalog` | `user_all.json:chara.boss_flag,title_id / cgi_py/legend.py` | 未確認 | 未判定 | 未確認 | 開始・勝利・敗北・中断時の値、タイトル解放条件 |
| 人間チャンピオン | `旧版_ver2/datalog/winner.cgi / battle.cgi` | `save_data/champion.json / cgi_py/battle.py` | 未確認 | 未判定 | 未確認 | 挑戦者の装備・戦術の保存、勝者交代、防衛戦績、初期王者 |
| 天下一武道会の参加者・対戦履歴 | `旧版_ver2/all_tenka.cgi / tenka_log.cgi` | `save_data/all_tenka.json,tenka_log.json / cgi_py/tenka.py` | 未確認 | 未判定 | 未確認 | 参加者抽出、順序、ログ保持数、制覇履歴 |

## チョコボ所有・レース進行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| チョコボ所持判定と未所持値 | `旧版_ver2/chocolog/<ID>.cgi` | `user_all.json:choco / sub_def/common.py:is_choco_owned` | 未確認 | 未判定 | 未確認 | 空辞書・欠損・実体データの判定、旧データ互換 |
| 飼育中チョコボの基本状態 | `旧版_ver2/chocolog/<ID>.cgi` | `user_all.json:choco / cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 名前、性別、血統、画像、能力c0〜c6、寿命、体力、戦績 |
| 野生チョコボの候補・購入 | `旧版_ver2/morifarm.cgi / chocobofile.cgi` | `cgi_py/morifarm.py / data/chocobo/chocobofile.json` | 未確認 | 未判定 | 未確認 | 候補抽選、価格、候補消費、所持制限、初期値 |
| 引退・お見合い候補リスト | `旧版_ver2/chocoboms.cgi / chocoboos.cgi` | `save_data/chocoboms.json,chocoboos.json / cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 性別別保存、候補上限、引退時移動、配合後の削除 |
| 配合後の子チョコボ | `旧版_ver2/morifarm.cgi` | `cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 父母・血統、能力上限、性別、初期能力、親の扱い |
| 訓練・休養による状態変化 | `旧版_ver2/ctrain.cgi / morifarm.cgi` | `cgi_py/ctrain.py / cgi_py/morifarm.py` | 未確認 | 未判定 | 未確認 | 各能力、寿命・体力、失敗、副作用、費用・待機時間 |
| 通常レースの戦績・クラス進行 | `旧版_ver2/crace.cgi` | `cgi_py/crace.py / user_all.json:choco` | 未確認 | 未判定 | 未確認 | run、win、gold、class条件、寿命、敗北時の変化 |
| G1/G2の個人トロフィー履歴 | `旧版_ver2/chocog1/<ID>.cgi` | `user_all.json:choco_g1 / cgi_py/crace.py` | 未確認 | 未判定 | 未確認 | r1〜r22、開催日・性別条件、重複勝利、殿堂条件 |
| チョコボ殿堂の共有リスト | `旧版_ver2/denchoco.cgi / dendo.cgi` | `save_data/denchoco.json / cgi_py/dendo.py` | 未確認 | 未判定 | 未確認 | 3重賞条件、同一チョコボの上書き、保存項目、一覧 |
| チョコボ王者 | `旧版_ver2/chocowinner.cgi / farmrace.cgi` | `save_data/chocobo_champion.json / cgi_py/farmrace.py` | 未確認 | 未判定 | 未確認 | 挑戦条件、勝者更新、連勝・前王者、初期値 |

## 記録・共有状態

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| ログイン履歴 | `旧版_ver2/loginlog/<ID>.cgi` | `user_all.json:login_log / login.py` | 未確認 | 未判定 | 未確認 | 保存件数、日時・IP等の項目、ログイン時更新 |
| 受信・送信メッセージ | `旧版_ver2/message / sousin` | `user_all.json:message / save_data/<ID>/message_sent.json` | 未確認 | 未判定 | 未確認 | 保存先分離、件数、既読・削除、変換時の扱い |
| 全体メッセージ・掲示板 | `旧版_ver2/datalog/message.cgi / post_message.cgi` | `save_data/all_message.json / cgi_py/bbs.py / admin.py` | 未確認 | 未判定 | 未確認 | 投稿者、保存件数、表示順、管理投稿 |
| 登録者・ランキング用キャッシュ | `旧版_ver2/alldata.cgi / rank.cgi` | `save_data/system_rank_cache.json / cgi_py/system.py / rank.py` | 未確認 | 未判定 | 未確認 | 対象プレイヤー、更新時刻、キャッシュ無効化、公開項目 |
