# 戦闘計算・結果処理比較チェックリスト

戦闘入口の一覧ではなく、共通シミュレータと各結果処理を比較単位にした台帳です。必殺技の個別効果は skills.md、モンスター特殊技は monster_skills.md と併用します。

## 戦闘状態の初期化と攻撃値

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 戦闘モード別の状態初期化 | `旧版_ver2/battle.pl:shokika / mbattle.pl:shokika / wbattle.pl:shokika` | `sub_def/battle_logic.py:BattleState.__init__` | BattleStateへ状態を集約 | 意図的 | 差異あり | monster/genei/isekiai/boss/battleの一時値、最大ターン、金銭変動を状態オブジェクトへ集約。対人は相手HP・装備、モンスターはマスター値とHP乱数を設定する。 |
| 装備・アクセサリーの戦闘用補正コピー | `旧版_ver2/battle.pl:acs_add / wbattle.pl:wacs_add` | `sub_def/battle_logic.py:_with_accessory_bonus` | 保存配列の直接加算からdeep copyへ変更 | 意図的 | 差異あり | Ver2のacs_add/wacs_addと同じ8能力補正を戦闘コピーだけに加算する。戦闘後に元データを戻す必要がない。 |
| モンスターHP・初期HPの乱数 | `旧版_ver2/mbattle.pl:mons_read / shokika` | `sub_def/battle_logic.py:BattleState.__init__` | 名前付きmonster値を使用 | 意図的 | 差異あり | 双方ともhp_base + rand(random_range)で決定し、その値を表示用最大HPにも使う。random_range 0は現行で安全に0幅相当へ正規化する。 |
| 職業別の基礎ダメージ（全31職） | `旧版_ver2/battle.pl:syokuzero〜syokuthirty` | `sub_def/battle_logic.py:get_job_dmg` | 職18〜30で魅力・カルマも乱数化 | 要判断 | 差異あり | 職0〜17と職22〜27の能力組合せは対応する。一方Ver2の職18〜30は魅力・カルマを固定加算するが、現行all_statsは両方をrand値にしており、期待ダメージが低下する。 |
| モンスター・対人相手の基礎ダメージ | `旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 計算をget_job_dmgと名前付きモンスター値へ統合 | 意図的 | 差異あり | モンスターはbase_damage + rand(random_range)、対人は相手の職業式＋武器ATK。幻影ではVer2同様にプレイヤー防具DEFを敵基礎ダメージへ加算する。 |
| 最大ターンと時間切れ | `旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose` | `sub_def/battle_logic.py:BattleState.turn / BattleSimulator.simulate` | 時間切れ結果コードを現行は引分2へ統一 | 要判断 | 差異あり | Ver2は未決着時win=3、現行は初期値win=2を返す。結果画面・報酬は現行で引分として処理するため、Ver2の時間切れ専用分岐との差を採用するか確認が必要。 |

## 必殺技・固有効果の発動順

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 選択戦術IDの取得 | `旧版_ver2/battle.pl:chara[30] / wbattle.pl:winner[37]` | `sub_def/battle_logic.py:get_tactic_id` | 列番号からtactic_idへ名称化 | 意図的 | 差異あり | プレイヤー・対人相手とも選択戦術IDを使用し、不正値・欠損値は0へ正規化する。現職ではないマスター戦術も選択済みなら実行する仕様を維持する。 |
| 戦術マスター由来の発動率分母 | `旧版_ver2/tac.ini / battle.pl:tyosenwaza` | `sub_def/battle_logic.py:_load_tactic_activation_denominators / skills.py:skill_check` | tac.jsonのactivation_denominatorを優先 | 意図的 | 差異あり | 説明文ラベルを乱数分母へ対応付ける後方互換を残し、明示値があればそれを優先する。個々の分母はskills.mdでVer2照合済み。 |
| プレイヤー必殺率・上限・特殊モード減衰 | `旧版_ver2/battle.pl:tyosenwaza` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 名前付き値・設定値へ移行 | 意図的 | 差異あり | カルマ/15 + 10 + 職業Lv、75上限、アクセ補正後95上限、幻影・異世界1/3、ボス1/2を共通ループで計算する。 |
| リミットブレイク | `旧版_ver2/battle.pl:tyosenwaza / wbattle.pl:winwaza` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 表示HTMLのみ更新 | 意図的 | 差異あり | 双方ともHP10%未満かつrand(4)>1で必殺率へ999を加算する。対人相手側も同条件で判定する。 |
| プレイヤー戦術の必殺技実行 | `旧版_ver2/tech/*.pl` | `sub_def/skills.py:tech_* .hissatu / run_skill` | 動的requireからrun_skillディスパッチへ移行 | 意図的 | 差異あり | 選択戦術IDのhissatuを通常行動後に呼び、未定義IDは安全に0相当へ解決する。各必殺技の差異はskills.mdで確認済み。 |
| 対人相手戦術の必殺技実行 | `旧版_ver2/wtech/*.pl` | `sub_def/skills.py:wtech_* .whissatu / run_skill` | 動的requireからrun_skillディスパッチへ移行 | 意図的 | 差異あり | 相手の選択戦術IDをwtech/whissatuへ渡し、相手アクセの必殺率補正も加える。 |
| モンスター特殊技の実行 | `旧版_ver2/mons/*.pl` | `sub_def/skills.py:mons_* .mons_waza / run_skill` | special_skill_idを名前付き値で参照 | 意図的 | 差異あり | モンスターの技ID・発動率をBattleStateへ渡してmons_wazaを呼ぶ。個別22技の値はmonster_skills.mdで照合済み。 |
| 戦術の後発効果 | `旧版_ver2/tech/*.pl:atowaza / wtech/*.pl:watowaza` | `sub_def/skills.py:tech_* .atowaza / wtech_* .watowaza` | 呼出先を明示ディスパッチ化 | 意図的 | 差異あり | 必殺判定後にプレイヤーatowaza、アクセ効果、対人なら相手watowaza・相手アクセ、モンスターならmons_atowazaの順で処理する。 |
| アクセサリー固有効果 | `旧版_ver2/acstech/*.pl / wacstech/*.pl` | `sub_def/skills.py:acstech_* / wacstech_*` | effect_idを辞書から参照 | 意図的 | 差異あり | 命中・回避・必殺率補正は先に取り込み、固有効果は後発効果の位置で実行する。個別effect_idはskills.mdで照合済み。 |
| 対人1ターン目の逆転必殺 | `旧版_ver2/wbattle.pl:battle_clt` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 設定値化と明示的な一時装備変更 | 意図的 | 差異あり | レベル差/装備比較による初手倍率、回避不能化、相手武器無効化を維持する。現行はcounterattack_level_gap等を設定値で読む。 |

## ダメージ確定・HP・勝敗

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| クリティカル判定（プレイヤー攻撃） | `旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 回復・0ダメージを判定対象外に変更 | 意図的 | 差異あり | HP割合から確率を出し、モンスター戦3倍、対人戦2倍＋相手武器ATKを適用する。現行はdmg1>0のときだけ判定して回復技を攻撃扱いしない。 |
| クリティカル判定（敵攻撃） | `旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 回復・0ダメージを判定対象外に変更 | 意図的 | 差異あり | 対人はHP割合・100幅で2倍＋自防具DEF、モンスターは200幅で防具DEF加算。現行はdmg2>0だけに限定する。 |
| 防具DEFによるダメージ減算と最小値 | `旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 防御不能ログを追加 | 意図的 | 差異あり | モンスター戦はDEF未満を0、対人戦は1にし、負ダメージは保持する。上級職軽減後に0になった攻撃を現行はログで明示する。 |
| 上級職の被ダメージ軽減 | `旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 職IDを名前付きjobで参照 | 意図的 | 差異あり | 職8〜17は1/2、18以上は1/4を被ダメージへ適用し、対人では双方に適用する。 |
| 命中・回避判定 | `旧版_ver2/mbattle.pl:mons_kaihi / wbattle.pl:battle_kaihi` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 表示用と戦闘用の計算を共通化 | 意図的 | 差異あり | DEX・AGI・武器命中・防具回避・アクセ補正と、モンスター300幅/対人100幅の回避判定を対応させる。 |
| 先行攻撃による敵行動停止 | `旧版_ver2の行動・勝敗処理` | `sub_def/battle_logic.py:BattleSimulator.simulate` | Ver2の同時精算にない敵行動停止を追加 | 要判断 | 差異あり | Ver2は双方の行動後にhp_sumする。現行は敵HPがこのターンに0以下になる見込みならdmg2を0にして『すでに倒れていた』とするため、プレイヤー先行の仕様変更になっている。 |
| ドレイン回復の基準 | `旧版_ver2/tech/43.pl ほか` | `sub_def/battle_logic.py:BattleSimulator.simulate / skills.py` | Ver2の設定ダメージ基準から実ダメージ基準へ変更 | 意図的 | 差異あり | 防御・回避後のdmg×割合で回復する現行仕様を維持する。ドレイン43の全量回復など個別割合はskills.mdで調整済み。 |
| HP・回復・自傷の精算順 | `旧版_ver2/mbattle.pl:hp_sum / wbattle.pl:hp_sum` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 同時精算を維持。ただし敵行動停止の例外あり | 要判断 | 差異あり | Ver2 hp_sumと同様に双方のダメージ・回復を同一ターンで精算し最大HPで上限化する。ただし先行撃破時だけ現行は敵dmgを消すため、完全な同時精算ではない。 |
| ターンログの記録値 | `旧版_ver2/mbattle.pl:mons_footer / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.battle_logs / templates/monster_result.html` | HTML断片から構造化ログ＋テンプレート表示へ移行 | 意図的 | 差異あり | ターン番号、双方HP、行動、ダメージ、回復を辞書へ保存し、HPは表示時に0下限へ丸める。コメントはhtml.escapeして表示する。 |
| 勝利・敗北・引き分けの判定 | `旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 結果コードの時間切れ統合 | 要判断 | 差異あり | 同時撃破は引分、敵HP0は勝利、プレイヤーHP0は敗北の順。最大ターン未決着が現行では引分2になる点はVer2 win=3との差異。 |

## 戦闘後の報酬・成長・進行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 通常・幻影・異世界の報酬処理 | `旧版_ver2/monster.cgi / mbattle.pl:sentoukeka` | `cgi_py/monster.py` | 結果処理をmonster.pyへ分離 | 意図的 | 差異あり | 勝敗別EXP/G、盗み差分、修行回数、幻影宝箱を入口側で処理する。時間切れを引分として扱う現行差は上記結果コード行と連動する。 |
| レジェンドの報酬・階層進行 | `旧版_ver2/legend.cgi / mbattle.pl:legend_sentoukeka` | `cgi_py/legend.py` | 結果処理をlegend.pyへ分離 | 意図的 | 差異あり | boss_flag/title_id、勝利時進行、敗北・引分時初期化、盗み差分を処理する。EXP表示追加は所有・進行台帳に記録済み。 |
| チャンピオン戦の報酬・王者更新 | `旧版_ver2/battle.cgi / wbattle.pl:sentoukeka` | `cgi_py/battle.py` | 結果処理をbattle.pyへ分離 | 意図的 | 差異あり | 勝利・引分の王者交代、敗北時の王者連勝、修行回数回復を処理する。敗北EXPの自分Lv×10上限は意図的な調整。 |
| 天下一武道会の報酬・ラウンド進行 | `旧版_ver2/tenka.cgi / wbattle.pl:sentoukeka` | `cgi_py/tenka.py` | 結果処理をtenka.pyへ分離 | 要判断 | 差異あり | 相手順、boss_flag、制覇履歴、修行回数回復を処理する。時間切れが引分2へ統合されるため、Ver2のwin=3時処理との差を確認対象に残す。 |
| 対人練習戦の保存有無 | `旧版_ver2/select_battle.cgi` | `cgi_py/select_battle.py` | 戦闘専用入口をPython化 | 意図的 | 差異あり | select_battle.pyはBattleSimulatorのログを表示するだけで、経験値・所持金・戦績・待機時刻・王者状態を保存しない。 |
| 経験値加算とレベルアップ | `旧版_ver2/battle.pl:levelup` | `sub_def/battle_logic.py:process_levelup` | 名前付き値とwhileループへ移行 | 意図的 | 差異あり | 必要EXP=現Lv×係数、複数Lv上昇、HP=rand(vit)×3+vit、能力上限・最大Lvを処理する。 |
| 職業熟練度の正規化とマスター | `旧版_ver2/battle.pl:syoku_regist` | `sub_def/battle_logic.py:process_levelup / cgi_py/tensyoku.py` | 61以上の旧値を60へ正規化 | 意図的 | 差異あり | Ver2のマスター上限60に合わせ、戦闘後にjob_levelを0〜60へ正規化する。初到達時だけ職歴へ60を保存する。 |
