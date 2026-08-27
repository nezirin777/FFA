# モンスター特殊技比較チェックリスト

モンスターが使う特殊技と、その使用モンスターを分けて確認します。発動率は各モンスターの `special_rate > random.randrange(100)` です。

## 特殊技一覧

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| モンスター特殊技 1: マイティガード | `旧版_ver2/mons/1.pl`、`旧版_ver2/mbattle.pl` | 使用 19体 / special_rate 10〜99 / 使用マスター: legend_boss_lv1.json, mons_isekai.json, mons_lv1.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_1.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 2: ケアルガ | `旧版_ver2/mons/2.pl`、`旧版_ver2/mbattle.pl` | 使用 25体 / special_rate 10〜90 / 使用マスター: legend_boss_lv2.json, legend_boss_lv3.json, mons_isekai.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_2.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 3: ファイガ | `旧版_ver2/mons/3.pl`、`旧版_ver2/mbattle.pl` | 使用 14体 / special_rate 10〜150 / 使用マスター: legend_boss_lv1.json, legend_boss_lv2.json, mons_isekai.json, mons_lv1.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_3.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 4: ブリザガ | `旧版_ver2/mons/4.pl`、`旧版_ver2/mbattle.pl` | 使用 5体 / special_rate 30〜90 / 使用マスター: legend_boss_lv2.json, mons_isekai.json, mons_lv2.json / `sub_def/skills.py`: mons_4.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 5: サンダガ | `旧版_ver2/mons/5.pl`、`旧版_ver2/mbattle.pl` | 使用 12体 / special_rate 10〜99 / 使用マスター: legend_boss_lv1.json, mons_isekai.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_5.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 6: メテオ | `旧版_ver2/mons/6.pl`、`旧版_ver2/mbattle.pl` | 使用 13体 / special_rate 10〜99 / 使用マスター: legend_boss_lv1.json, legend_boss_lv2.json, legend_boss_lv4.json, mons_isekai.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_6.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 7: グラビガ | `旧版_ver2/mons/7.pl`、`旧版_ver2/mbattle.pl` | 使用 5体 / special_rate 30〜70 / 使用マスター: legend_boss_lv2.json, legend_boss_lv4.json, mons_isekai.json, mons_lv3.json / `sub_def/skills.py`: mons_7.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 8: クエイク | `旧版_ver2/mons/8.pl`、`旧版_ver2/mbattle.pl` | 使用 12体 / special_rate 30〜99 / 使用マスター: mons_isekai.json, mons_lv2.json / `sub_def/skills.py`: mons_8.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 9: アルテマ | `旧版_ver2/mons/9.pl`、`旧版_ver2/mbattle.pl` | 使用 13体 / special_rate 20〜80 / 使用マスター: legend_boss_lv3.json, legend_boss_lv4.json, mons_isekai.json, mons_lv3.json / `sub_def/skills.py`: mons_9.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 10: ショック・ウェーブ・パルサー | `旧版_ver2/mons/10.pl`、`旧版_ver2/mbattle.pl` | 使用 5体 / special_rate 40〜99 / 使用マスター: legend_boss_lv3.json, mons_isekai.json / `sub_def/skills.py`: mons_10.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 11: デジョン | `旧版_ver2/mons/11.pl`、`旧版_ver2/mbattle.pl` | 使用 17体 / special_rate 10〜99 / 使用マスター: legend_boss_lv1.json, legend_boss_lv2.json, legend_boss_lv3.json, mons_isekai.json, mons_lv1.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_11.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 12: ファイア・ブレス | `旧版_ver2/mons/12.pl`、`旧版_ver2/mbattle.pl` | 使用 11体 / special_rate 0〜70 / 使用マスター: legend_boss_lv1.json, legend_boss_lv4.json, mons_isekai.json, mons_lv1.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_12.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 13: ケアルガ / アルテマ | `旧版_ver2/mons/13.pl`、`旧版_ver2/mbattle.pl` | 使用 20体 / special_rate 30〜99 / 使用マスター: legend_boss_lv3.json, mons_isekai.json, mons_lv3.json / `sub_def/skills.py`: mons_13.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 14: お金を盗む | `旧版_ver2/mons/14.pl`、`旧版_ver2/mbattle.pl` | 使用 7体 / special_rate 40〜99 / 使用マスター: legend_boss_lv3.json, legend_boss_lv4.json, mons_lv1.json, mons_lv4.json / `sub_def/skills.py`: mons_14.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 15: ドレイン | `旧版_ver2/mons/15.pl`、`旧版_ver2/mbattle.pl` | 使用 25体 / special_rate 10〜99 / 使用マスター: legend_boss_lv1.json, mons_isekai.json, mons_lv1.json, mons_lv2.json, mons_lv3.json, mons_lv4.json / `sub_def/skills.py`: mons_15.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 16: アポガリプス | `旧版_ver2/mons/16.pl`、`旧版_ver2/mbattle.pl` | 使用 5体 / special_rate 20〜99 / 使用マスター: legend_boss_lv2.json, mons_isekai.json, mons_lv4.json / `sub_def/skills.py`: mons_16.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 17: えりりんの甘いささやき / 祝福のキス | `旧版_ver2/mons/17.pl`、`旧版_ver2/mbattle.pl` | 使用 3体 / special_rate 999〜999 / 使用マスター: mons_lv1.json, mons_lv2.json, mons_lv4.json / `sub_def/skills.py`: mons_17.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 18: メガ・フレア | `旧版_ver2/mons/18.pl`、`旧版_ver2/mbattle.pl` | 使用 2体 / special_rate 90〜99 / 使用マスター: legend_boss_lv2.json, legend_boss_lv4.json / `sub_def/skills.py`: mons_18.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 19: ハァハァ。。。 | `旧版_ver2/mons/19.pl`、`旧版_ver2/mbattle.pl` | 使用 3体 / special_rate 90〜99 / 使用マスター: legend_boss_lv4.json, mons_lv4.json / `sub_def/skills.py`: mons_19.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 20: 斬・鉄・剣 | `旧版_ver2/mons/20.pl`、`旧版_ver2/mbattle.pl` | 使用 2体 / special_rate 50〜70 / 使用マスター: legend_boss_lv2.json, legend_boss_lv4.json / `sub_def/skills.py`: mons_20.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 21: 性転換 | `旧版_ver2/mons/21.pl`、`旧版_ver2/mbattle.pl` | 使用 1体 / special_rate 999〜999 / 使用マスター: mons_lv4.json / `sub_def/skills.py`: mons_21.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |
| モンスター特殊技 22: 臭い息 | `旧版_ver2/mons/22.pl`、`旧版_ver2/mbattle.pl` | 使用 1体 / special_rate 20〜20 / 使用マスター: mons_lv4.json / `sub_def/skills.py`: mons_22.mons_waza / mons_atowaza | 未確認 | 未判定 | 未確認 | 発動条件・通常攻撃との加算/置換・命中/回避・回復・状態変化を照合後に根拠を記入 |

## 使用モンスター一覧

| 項目名 | Ver2確認箇所 | Ver3現行値・確認箇所 | Ver2との差異 | 意図的な仕様か否か | 照合状態 | 備考・根拠 |
| --- | --- | --- | --- | --- | --- | --- |
| legend_boss_lv1.json: 魔界の騎士ベルフェゴール | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 30 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 魔界の騎士ベルフェゴール | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 30 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 冥府の管理人ラダマンティス | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 40 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 地獄の番犬ケルベロス | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 70 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 闇の幻獣ベヒーモス | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 10 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 稲妻の幻獣ケツアルカトル | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 60 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 煉獄の幻獣イフリート | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 60 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 悪魔アークデーモン | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 30 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv1.json: 悪魔ガーゴイル | `旧版_ver2/data/bossmons0.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 50 / `data/monsters/legend_boss_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 偉大なる魔女アルティミシア | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 16: アポガリプス / special_rate 20 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 偉大なる魔女アルティミシア | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 16: アポガリプス / special_rate 20 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 忘れ去られし騎士ガーランド | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 10 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 最強の竜神バハムート | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 18: メガ・フレア / special_rate 90 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 最強の水竜リヴァイアサン | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 4: ブリザガ / special_rate 90 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 最強の機械神アレクサンダー | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 30 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 孤高の戦士セフイロス | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 50 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 炎の魔神アポロン | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 150 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 氷河の魔神オーディン | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 20: 斬・鉄・剣 / special_rate 50 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 魔女イデア | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 7: グラビガ / special_rate 40 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv2.json: 冥府の王ハーデス | `旧版_ver2/data/bossmons1.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 10 / `data/monsters/legend_boss_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 伝説の機械神オメガ・ウエポン | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 10: ショック・ウェーブ・パルサー / special_rate 75 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 伝説の機械神オメガ・ウエポン | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 10: ショック・ウェーブ・パルサー / special_rate 75 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 大天使ミカエル | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 99 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 堕天使ルシファー | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 大魔王サタン | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 70 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 破壊神シヴァ | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 30 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 偉大なる神アフラマズダ | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 40 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 古代兵器アルテマ・ウエポン | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 暗黒の忍者シャドウ・ジタン | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 90 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 暗黒の騎士シャドウ・スコール | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 70 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv3.json: 暗黒の戦士シャドウ・クラウド | `旧版_ver2/data/bossmons2.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 70 / `data/monsters/legend_boss_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 全能神いく | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 19: ハァハァ。。。 / special_rate 99 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 全能神いく | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 19: ハァハァ。。。 / special_rate 99 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: バハムート改 | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 18: メガ・フレア / special_rate 99 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 目覚めたオーディン | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 20: 斬・鉄・剣 / special_rate 70 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 初代覇者！雄翼の踊り子FEENA | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 70 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 大いなる力シン | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 70 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 闇よりの悪商人セラ | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 40 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 邪竜の化身ヒュドラ | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 7: グラビガ / special_rate 40 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 古の破壊神くらやみの雲 | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 99 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 廃退した邪神ケフカ | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 80 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| legend_boss_lv4.json: 神竜 | `旧版_ver2/data/bossmons3.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 60 / `data/monsters/legend_boss_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神アメノトリフネ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神オモイカネ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 10: ショック・ウェーブ・パルサー / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神ヒノカクヅチ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神タケミカヅチ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神ツクヨミ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神アマテラス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神イザナミ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 天津神イザナギ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 国津神オオヤマツミ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 国津神スクナヒコナ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 国津神サルタヒコ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 国津神オオナムチ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 国津神タケミナカタ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 国津神ヤシャテンテイ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神ゾウチョウテン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神タモンテン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 4: ブリザガ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神コウモクテン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神ジコクテン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神ティール | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神ショウキ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神ビシャモンテン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 7: グラビガ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 鬼神マリシテン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神サルガナタス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神ミシャクジ様 | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 44 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神エキドナ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 20 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神テスカポリトカ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神サトゥルヌス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神パレス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神セト | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 邪神アシュラ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 20 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神フレイア | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神フレイ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神ゼウス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神ツァバト | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神シャダイ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神エロヒム | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 愚神Y･H･V･H | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王ロキ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 4: ブリザガ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王スルト | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王ディルムヴォンド | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王ミトラ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王ベリアル | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 12 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王バエル | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王アスタロート | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王アスモダイ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王ベルゼブブ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 堕天使アザゼル | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 16: アポガリプス / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔王ディアボロス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 7: グラビガ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神インドラ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神ルーグ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神ブラフマー | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神オシリス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神サジタリウス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神バアル | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神アルダー | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神ヴィシュヌ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 魔神クリシュナ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 70 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神アリアンロッド | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神スカアハ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神サラスヴァティ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神パラスアテナ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神ラクシュミ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神ノルン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神アナト | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 女神ルミネ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神タウエレト | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神ハリティー | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神ダイアナ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神ドゥルガー | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神イシュタル | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 90 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神カーリー | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 30 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神セイオウボ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 地母神ファルナ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 破壊神チェルノボグ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 破壊神セイテンタイセイ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 破壊神ザオウゴンゲン | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 破壊神カルティケーヤ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 10: ショック・ウェーブ・パルサー / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 破壊神カオス | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 40 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 破壊神アンドロメダ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 10: ショック・ウェーブ・パルサー / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 伝説の武神ギルガ・メッシュ | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 10 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_isekai.json: 伝説のメタルキング | `旧版_ver2/data/isekaimons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_isekai.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 吸血こうもり | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 40 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 悪魔のこうもり | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 40 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 海賊 | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 40 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: どろぼう | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 40 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 盗賊 | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 40 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: ギル・ゴースト | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 99 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: メタルスライム | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: はぐれメタル | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: メタルキング | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 悪魔の使い | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 30 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: ランプの精 | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 30 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 魔獣オルトロス | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 30 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 無人くん | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 20 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: 死神アンクウ | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 30 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv1.json: えりりん | `旧版_ver2/data/normalmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 17: えりりんの甘いささやき / 祝福のキス / special_rate 999 / `data/monsters/mons_lv1.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 狂人バナナ７協会長 | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 精霊シルフ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 精霊ノーム | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 精霊ウンディーネ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 4: ブリザガ / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 精霊サラマンダー | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 聖獣スザク | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 聖獣ビャッコ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 4: ブリザガ / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 聖獣ゲンブ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 8: クエイク / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 聖獣セイリュウ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 12 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 幻魔アルラウネ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 幻魔バフォメット | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 幻魔タム・リン | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 幻魔クー・フーリン | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 幻魔クルーニスク | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 幻魔ハヌマーン | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔モコイ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔リリス | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔インキュバス | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔サキュバス | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 30 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔ニュクス | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 20 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔ヘカーテ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 40 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 夜魔リリス | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 将軍エドアルム | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 20 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: 英雄ロアッド | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: ブラットソウル | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: ガルバディア兵 | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 20 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: グレンデル | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 20 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: コカトリス | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 10 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: メタルスライム | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: はぐれメタル | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: メタルキング | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv2.json: えりりん♪ | `旧版_ver2/data/lowmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 17: えりりんの甘いささやき / 祝福のキス / special_rate 999 / `data/monsters/mons_lv2.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: キマイラブレイン | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 40 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: クアール | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 40 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ベヒーモス | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 10 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ベルヘルメルヘル | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 40 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ボム | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 99 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: メルトドラゴン | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 30 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ライフフォビドン | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 99 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ルブルムドラゴン | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 40 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: オチュー | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 99 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ガルキマセラ | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 30 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: アダマンタイマイ | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 70 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: インビンシブル | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 7: グラビガ / special_rate 40 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: エリート兵 | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: ドラゴンイゾルテ | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 30 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: 猛将カールマルテル | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: 猛将ロンギヌス | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: 猛将ヨシツネ | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 9: アルテマ / special_rate 20 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: 猛将信長 | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 10 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: 猛将マサカド | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 20 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: 英雄ジャンヌダルク | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 13: ケアルガ / アルテマ / special_rate 90 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: はぐれメタル | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv3.json: メタルキング | `旧版_ver2/data/highmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv3.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: アヌビス | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 40 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ギリガメラ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 40 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: カトブレパス | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 50 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ペリ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 10 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: カナロア | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 5: サンダガ / special_rate 40 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ゲーデ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 99 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: スレイプニル | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 30 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: イルルヤンカシュ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 99 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ファファニール | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 6: メテオ / special_rate 40 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: バルバドス | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 99 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: アラハバキ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 30 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ヤマタノオロチ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 12: ファイア・ブレス / special_rate 0 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: オベロン | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 70 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ランダ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 16: アポガリプス / special_rate 99 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ヘカーナ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ヴァルキリー | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 16: アポガリプス / special_rate 20 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ガルーダ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 11: デジョン / special_rate 60 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ケルンヌス | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 30 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ウロボロス | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 14: お金を盗む / special_rate 60 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ケルプ | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 15: ドレイン / special_rate 50 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: バロン | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 3: ファイガ / special_rate 60 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: アスタロト | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 2: ケアルガ / special_rate 20 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: モルボル | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 22: 臭い息 / special_rate 20 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: 狂気のあなきん | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 19: ハァハァ。。。 / special_rate 90 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: ブラックジャック | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 21: 性転換 / special_rate 999 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: メタルキングPowerUPVer! | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: プラチナキング | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 1: マイティガード / special_rate 99 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
| mons_lv4.json: 愛しのえりりん | `旧版_ver2/data/spmons.ini` の対応モンスター・特殊技ID・特殊率 | 特殊技 17: えりりんの甘いささやき / 祝福のキス / special_rate 999 / `data/monsters/mons_lv4.json` | 未確認 | 未判定 | 未確認 | モンスター名、特殊技ID、特殊率を照合後に根拠を記入 |
