# 戦闘計算・結果処理比較チェックリスト

戦闘入口の一覧ではなく、共通シミュレータと各結果処理を比較単位にした台帳です。必殺技の個別効果は skills.md、モンスター特殊技は monster_skills.md と併用します。

## 戦闘状態の初期化と攻撃値

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 戦闘モード別の状態初期化 | `旧版_ver2/battle.pl:shokika / mbattle.pl:shokika / wbattle.pl:shokika` | `sub_def/battle_logic.py:BattleState.__init__` | 未確認 | 未判定 | 未確認 | mode別の初期値、対人・モンスターの状態キー、ターン上限 |
| 装備・アクセサリーの戦闘用補正コピー | `旧版_ver2/battle.pl:acs_add / wbattle.pl:wacs_add` | `sub_def/battle_logic.py:_with_accessory_bonus` | 未確認 | 未判定 | 未確認 | 恒久保存値を変更しないこと、8能力値補正、対人側補正 |
| モンスターHP・初期HPの乱数 | `旧版_ver2/mbattle.pl:mons_read / shokika` | `sub_def/battle_logic.py:BattleState.__init__` | 未確認 | 未判定 | 未確認 | hp_base、random_range、最小値、表示用最大HP |
| 職業別の基礎ダメージ（全31職） | `旧版_ver2/battle.pl:syokuzero〜syokuthirty` | `sub_def/battle_logic.py:get_job_dmg` | 未確認 | 未判定 | 未確認 | 各職IDの参照能力値、乱数範囲、武器ATK、カルマの扱い |
| モンスター・対人相手の基礎ダメージ | `旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | base_damage、random_range、相手職業・装備、幻影の城補正 |
| 最大ターンと時間切れ | `旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose` | `sub_def/battle_logic.py:BattleState.turn / BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | 最大ターン数、未決着時の引き分け、ログ最終ターン |

## 必殺技・固有効果の発動順

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 選択戦術IDの取得 | `旧版_ver2/battle.pl:chara[30] / wbattle.pl:winner[37]` | `sub_def/battle_logic.py:get_tactic_id` | 未確認 | 未判定 | 未確認 | 未設定値、不正値、現職以外のマスター戦術の使用可否 |
| 戦術マスター由来の発動率分母 | `旧版_ver2/tac.ini / battle.pl:tyosenwaza` | `sub_def/battle_logic.py:_load_tactic_activation_denominators / skills.py:skill_check` | 未確認 | 未判定 | 未確認 | 説明文の確率と乱数分母、未定義戦術、Ver2との差異 |
| プレイヤー必殺率・上限・特殊モード減衰 | `旧版_ver2/battle.pl:tyosenwaza` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | カルマ・職業熟練度・アクセ補正、75/95上限、genei・isekiai・boss補正 |
| リミットブレイク | `旧版_ver2/battle.pl:tyosenwaza / wbattle.pl:winwaza` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | HP10%未満の条件、乱数、プレイヤー・対人相手の双方 |
| プレイヤー戦術の必殺技実行 | `旧版_ver2/tech/*.pl` | `sub_def/skills.py:tech_* .hissatu / run_skill` | 未確認 | 未判定 | 未確認 | 全戦術IDの呼出先、発動失敗時、副作用とログ |
| 対人相手戦術の必殺技実行 | `旧版_ver2/wtech/*.pl` | `sub_def/skills.py:wtech_* .whissatu / run_skill` | 未確認 | 未判定 | 未確認 | 相手側tactic_id、発動率、プレイヤー側との対称性 |
| モンスター特殊技の実行 | `旧版_ver2/mons/*.pl` | `sub_def/skills.py:mons_* .mons_waza / run_skill` | 未確認 | 未判定 | 未確認 | special_skill_id・special_rate、通常行動との排他、各技効果 |
| 戦術の後発効果 | `旧版_ver2/tech/*.pl:atowaza / wtech/*.pl:watowaza` | `sub_def/skills.py:tech_* .atowaza / wtech_* .watowaza` | 未確認 | 未判定 | 未確認 | 必殺技後の実行順、対象、累積・上限 |
| アクセサリー固有効果 | `旧版_ver2/acstech/*.pl / wacstech/*.pl` | `sub_def/skills.py:acstech_* / wacstech_*` | 未確認 | 未判定 | 未確認 | effect_id、発動順、対人双方、装備能力補正との重複 |
| 対人1ターン目の逆転必殺 | `旧版_ver2/wbattle.pl:battle_clt` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | レベル差・装備比較条件、倍率、武器無効化、双方の判定順 |

## ダメージ確定・HP・勝敗

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| クリティカル判定（プレイヤー攻撃） | `旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | HP比率、乱数幅、モンスター戦3倍・対人戦2倍+武器ATK |
| クリティカル判定（敵攻撃） | `旧版_ver2/mbattle.pl:mons_clt / wbattle.pl:battle_clt` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | モンスター・対人での確率、ダメージ補正、回復技の除外 |
| 防具DEFによるダメージ減算と最小値 | `旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | モンスター戦0・対人戦1の最小ダメージ、負値・防御不能ログ |
| 上級職の被ダメージ軽減 | `旧版_ver2/mbattle.pl:monsbattle_sts / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | 職業ID 8〜17の半減、18以上の1/4、双方への適用 |
| 命中・回避判定 | `旧版_ver2/mbattle.pl:mons_kaihi / wbattle.pl:battle_kaihi` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | dex・agi、武器命中・防具回避・アクセ補正、乱数幅、対人双方 |
| 先行攻撃による敵行動停止 | `旧版_ver2の行動・勝敗処理` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | 敵がこのターンに倒れる場合の敵ダメージ・ログ、対人・モンスター双方 |
| ドレイン回復の基準 | `旧版_ver2/tech/43.pl ほか` | `sub_def/battle_logic.py:BattleSimulator.simulate / skills.py` | 未確認 | 未判定 | 未確認 | 防御・回避後の実ダメージ基準、回復比率、0ダメージ時 |
| HP・回復・自傷の精算順 | `旧版_ver2/mbattle.pl:hp_sum / wbattle.pl:hp_sum` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | 同時精算、最大HP上限、過剰回復、死亡と回復の組合せ |
| ターンログの記録値 | `旧版_ver2/mbattle.pl:mons_footer / wbattle.pl:battle_sts` | `sub_def/battle_logic.py:BattleSimulator.battle_logs / templates/monster_result.html` | 未確認 | 未判定 | 未確認 | 表示HP、ダメージ、回復、勝敗文、HTMLエスケープ |
| 勝利・敗北・引き分けの判定 | `旧版_ver2/mbattle.pl:winlose / wbattle.pl:winlose` | `sub_def/battle_logic.py:BattleSimulator.simulate` | 未確認 | 未判定 | 未確認 | 相打ち、判定優先順位、時間切れ、結果コード |

## 戦闘後の報酬・成長・進行

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| 通常・幻影・異世界の報酬処理 | `旧版_ver2/monster.cgi / mbattle.pl:sentoukeka` | `cgi_py/monster.py` | 未確認 | 未判定 | 未確認 | 勝利・引き分け・敗北EXP/G、盗み差分、battle_limit、幻影宝箱 |
| レジェンドの報酬・階層進行 | `旧版_ver2/legend.cgi / mbattle.pl:legend_sentoukeka` | `cgi_py/legend.py` | 未確認 | 未判定 | 未確認 | boss_flag、title_id、階層解放、称号、敗北・中断時 |
| チャンピオン戦の報酬・王者更新 | `旧版_ver2/battle.cgi / wbattle.pl:sentoukeka` | `cgi_py/battle.py` | 未確認 | 未判定 | 未確認 | 敗北EXP上限、勝利・引き分けEXP、賞金、王者保存、制限回復 |
| 天下一武道会の報酬・ラウンド進行 | `旧版_ver2/tenka.cgi / wbattle.pl:sentoukeka` | `cgi_py/tenka.py` | 未確認 | 未判定 | 未確認 | 相手順、勝敗・引分、ログ、boss_flag、制限回復 |
| 対人練習戦の保存有無 | `旧版_ver2/select_battle.cgi` | `cgi_py/select_battle.py` | 未確認 | 未判定 | 未確認 | 戦闘ログのみか、経験値・所持金・戦績・待機時間を更新しないこと |
| 経験値加算とレベルアップ | `旧版_ver2/battle.pl:levelup` | `sub_def/battle_logic.py:process_levelup` | 未確認 | 未判定 | 未確認 | 必要EXP、複数Lv上昇、最大Lv、能力・HP成長、職業上限 |
| 職業熟練度の正規化とマスター | `旧版_ver2/battle.pl:syoku_regist` | `sub_def/battle_logic.py:process_levelup / cgi_py/tensyoku.py` | 未確認 | 未判定 | 未確認 | Lv60上限、既存61以上の正規化、転職時の保存 |
