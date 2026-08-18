#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
winner_to_json.py

旧形式 winner.cgi（<> 区切りテキスト、Shift-JIS）を
新形式 winner.json（JSON、UTF-8）に変換します。

使い方:
    python3 winner_to_json.py ./winner.cgi ./winner.json
    python3 winner_to_json.py ./winner.cgi          # 標準出力に書く

---------------------------------------------------------------
★重要★ フィールド対応表の信頼度について

  [確定] … others.cgi / regist.pl 内で実際に $winner[N] として
           参照されているコードから特定できた項目
  [推定] … 前後の項目の並び（他の項目との相対位置）から
           位置的に推測しただけで、参照コードでは未確認の項目
  [不明] … 対応する旧フィールドが特定できず、0 / 空文字 で
           埋めている項目（実データでは別の場所にある可能性あり）

  [推定][不明] は必ず実データ（複数キャラ分）で検証してください。

  ---------------------------------------------------------------
  system.cgi (chara_sts / ranking) を突き合わせた際の追記:

  system.cgi は $winner[N] を一切参照していない（$chara / $item を
  使う別系統）ため直接の裏取りにはならないが、chara_sts サブが
  $item[N] の並びをかなり具体的に使っており、装備ボーナス周りの
  "設計図" として非常に参考になった。

    武器: item[0]=名前, item[1]=攻撃力, item[2]=(命中への寄与)
    防具: item[3]=名前, item[4]=防御力, item[5]=(回避への寄与)
    飾り: item[6]=名前, item[8..15]=str/int/mnd/vit/dex/agi/cha/karma
          ボーナス(8個, chaも含む!), item[16]=命中, item[17]=必殺,
          item[18]=回避
    $i_plus = $item[2] + $item[16];  # 武器由来+飾り由来を合算して命中率へ
    $d_plus = $item[5] + $item[18];  # 防具由来+飾り由来を合算して回避率へ

  これにより:
    - weapon.dmg(winner[22]) / armor.def(winner[25]) は name→dmg/def
      という並びが item[1]/item[4] と一致するため [推定]→確度アップ。
    - 魅力(cha)ボーナスは item[14] として実在する。ただし others.cgi の
      飾りボーナス表示コードには魅力の行だけ加算表示が無く
      (winner[28]〜[34]はstr,int,mnd,vit,dex,agi,karmaの7個で埋まる)、
      チャンプ記録に固める際にcha分だけ構造的に欠落している可能性が
      高いと判断した（単なる表示漏れではなさそう）。
    - weapon.effect / armor.effect (item[2]/item[5]相当) は、winner側
      では武器分・防具分に分かれておらず、命中/回避の合算値
      (winner[23]/[26]) として一本化されている可能性が高い。このため
      本スクリプトでは weapon.effect/armor.effect は 0 固定のままとし、
      合算値は accessory.hit_rate/evasion_rate 側に寄せている
      （モデリング上の判断であり、確証ではない）。
    - effect_id / unused30 / host (winner[36..38]) は system.cgi でも
      直接の裏付けは得られなかったが、上記の対応付けで飾りボーナスの
      必要スロット数を数え切った結果、ちょうど残り3つに一致するため
      矛盾はない（＝確定はできないが不自然でもない、という程度）。
  ---------------------------------------------------------------
"""

import sys
import html
import json
from collections import OrderedDict

EXPECTED_FIELDS = 71


def num(s):
    """数値化。ゴミ/非数値データが混ざっていても 0 にフォールバックする。"""
    if s is None or s == "":
        return 0
    try:
        return int(s)
    except ValueError:
        try:
            return int(float(s))
        except ValueError:
            return 0


def text(s):
    """regist.pl の decode() が < > " をエスケープしているので元に戻す。"""
    if s is None:
        return ""
    return html.unescape(s)


def load_fields(path):
    with open(path, "rb") as f:
        raw = f.readline()
    raw = raw.rstrip(b"\r\n")
    # 元データは Shift-JIS(cp932) 前提
    line = raw.decode("cp932")

    fields = line.split("<>")
    if len(fields) > EXPECTED_FIELDS:
        print(
            f"warning: expected {EXPECTED_FIELDS} fields, got {len(fields)} "
            "-- old-format assumptions may not hold for this record",
            file=sys.stderr,
        )
    # 足りない分はゼロ埋め
    fields += [""] * (EXPECTED_FIELDS - len(fields))
    return fields


def convert(fields):
    f = fields

    # ---- [確定] 基本情報 ----
    id_ = f[0]  # regist.pl 全体で $chara[0] がファイルキーとして
    # 使われている慣習と一致
    password = f[1]  # 未使用
    site = f[2]
    url = f[3]
    name = f[4]
    sex = f[5]  # others.cgi: if($winner[4]){男}else{女}
    img = f[6]  # others.cgi: $chara_img[$winner[5]]

    # ---- [確定] 能力値（並びは acs.ini / item.pl の並びとも一致） ----
    str_ = f[7]  # 力
    int_ = f[8]  # 魔力 表示だが新形式では int
    mnd = f[9]  # 信仰心
    vit = f[10]  # 生命力
    dex = f[11]  # 器用さ
    agi = f[12]  # 速さ
    cha = f[13]  # 魅力（ボーナス加算なしで表示 = そのままの値）
    karma = f[20]  # カルマ

    job = f[14]  # $chara_syoku[$winner[14]]
    hp = f[15]
    max_hp = f[16]
    exp = f[17]  # 経験値
    level = f[18]

    # ---- [確定] 賞金 ----
    gold = f[19]

    # ---- [確定] 戦績（連勝記録とは別の通算値） ----
    battle_count = f[21]
    battle_win_count = f[22]

    # ---- [推定] コメント ----
    # level/戦績の直後、equipped_item ブロックの直前という
    # JSON側の並び順から推測。others.cgi 内に直接の参照は見つからず。
    comment = ""

    # ---- 装備品 ----
    # [確定] 名称は others.cgi の「武器/防具/飾り」表示から特定
    weapon_name = f[24]
    armor_name = f[33]
    accessory_name = f[35]

    # [推定・裏付けあり] system.cgi の chara_sts では item[0]=武器名,
    # item[1]=攻撃力 という並びで、winner側も name(21)→dmg(22) と同じ
    # オフセットで一致する。armor も同様(name=24→def=25)。
    # effect は system.cgi 上では item[2]/item[5]として武器/防具ごとに
    # 個別に存在するが、winner側では命中/回避の合算値(23/26)に一本化
    # されている可能性が高く、単独の値を復元できないため0固定。
    weapon_dmg = 0
    weapon_effect = 0  # [不明] item[2]相当は23に合算されている可能性
    armor_def = 0
    armor_effect = 0  # [不明] item[5]相当は26に合算されている可能性

    # [確定] 命中率・回避率ボーナスは hit_ritu / kaihi_ritu の計算式
    # ($a_hitup / $a_kaihiup を加算している箇所)から特定。
    # system.cgi の $i_plus=$item[2]+$item[16] / $d_plus=$item[5]+$item[18]
    # と見比べると、winner[23]/[26]は「武器(or防具)由来 + 飾り由来」の
    # 合算値である可能性が高い（＝厳密には accessory 単体の値ではない）。
    accessory_hit_rate = 0
    accessory_evasion_rate = 0

    # [確定] ボーナス値は「$winner[stat] + $winner[N]」という表示コードから
    # 特定。魅力(cha)だけ元コードでボーナス加算の表示が一切なく0固定に
    # しているが、system.cgi の item[8..15]（str/int/mnd/vit/dex/agi/
    # cha/karmaの8個、chaも実在）と比べると、winnerの飾りボーナス欄は
    # str/int/mnd/vit/dex/agi/karmaの7個しか埋まっておらず、cha分だけ
    # チャンプ記録に固める際に構造的に欠落している可能性が高い
    # （単なる表示漏れではなさそう）。
    bonus_str = 0
    bonus_int = 0
    bonus_mnd = 0
    bonus_vit = 0
    bonus_dex = 0
    bonus_agi = 0
    bonus_cha = 0  # [不明] 元コードに加算表示なし
    bonus_karma = 0

    # [確定] 必殺率ボーナスは bwwaza の計算式から特定
    accessory_special_rate = 0

    # [推定] effect_id / unused30 / host はどれも直接の参照コードが
    # 見つからなかったため、残り3フィールド(36,37,38)に仮で割り当てている。
    # この並びの妥当性は要検証。
    accessory_effect_id = 0  # [不明]
    unused30 = 0  # [推定]
    host = f[26]  # [推定] 旧データに無ければ空文字でも可

    # ---- [確定] ジョブレベル ----
    job_level = f[37]  # class_flg = int($winner[39]/10) 、
    # 「ジョブLV」表示欄と一致

    # ---- [確定] 直近の対戦相手（連勝記録の説明文から特定） ----
    lc_id = ""  # Ver1データに記録者IDなし
    lc_name = f[31]
    lc_site = f[29]
    lc_url = f[30]

    # ---- [確定] 連勝数 ----
    win_count = f[28]  # 現在の連勝数
    max_win_count = 0  # 最高連勝記録

    # ---- [確定/推定] 連勝記録保持者 ----
    # name/site/url は「現在の連勝記録は、$winner[47]さんの...」の記述から
    # 特定。id($winner[46])は直近対戦相手ブロック(40-43: id,name,site,url)と
    # 同じ並びのはずという類推で[推定]扱い。
    max_win_id = ""  # [推定]
    max_win_name = ""
    max_win_site = ""
    max_win_url = ""

    # ---- フィールド 51-69 ----
    # 新JSONスキーマに対応する項目が見当たらないため、このスクリプトでは
    # 変換対象外（切り捨て）としている。旧データの参照が必要な場合は
    # legacy_unmapped を利用すること。
    legacy_unmapped = f[50:70]  # noqa: F841 (参照用に残すだけ)

    data = OrderedDict()
    data["id"] = text(id_)
    data["site"] = text(site)
    data["url"] = text(url)
    data["name"] = text(name)
    data["sex"] = num(sex)
    data["img"] = num(img)
    data["str"] = num(str_)
    data["int"] = num(int_)
    data["dex"] = num(dex)
    data["vit"] = num(vit)
    data["agi"] = num(agi)
    data["mnd"] = num(mnd)
    data["job"] = num(job)
    data["hp"] = num(hp)
    data["max_hp"] = num(max_hp)
    data["level"] = num(level)
    data["battle_count"] = num(battle_count)
    data["battle_win_count"] = num(battle_win_count)
    data["comment"] = text(comment)
    data["equipped_item"] = OrderedDict(
        [
            (
                "weapon",
                OrderedDict(
                    [
                        ("name", text(weapon_name)),
                        ("dmg", num(weapon_dmg)),
                        ("effect", num(weapon_effect)),
                    ]
                ),
            ),
            (
                "armor",
                OrderedDict(
                    [
                        ("name", text(armor_name)),
                        ("def", num(armor_def)),
                        ("effect", num(armor_effect)),
                    ]
                ),
            ),
            (
                "accessory",
                OrderedDict(
                    [
                        ("name", text(accessory_name)),
                        ("effect_id", num(accessory_effect_id)),
                        (
                            "bonus",
                            OrderedDict(
                                [
                                    ("str", num(bonus_str)),
                                    ("int", num(bonus_int)),
                                    ("mnd", num(bonus_mnd)),
                                    ("vit", num(bonus_vit)),
                                    ("dex", num(bonus_dex)),
                                    ("agi", num(bonus_agi)),
                                    ("cha", num(bonus_cha)),
                                    ("karma", num(bonus_karma)),
                                ]
                            ),
                        ),
                        ("hit_rate", num(accessory_hit_rate)),
                        ("evasion_rate", num(accessory_evasion_rate)),
                        ("special_rate", num(accessory_special_rate)),
                    ]
                ),
            ),
        ]
    )
    data["unused30"] = num(unused30)
    data["host"] = text(host)
    data["job_level"] = num(job_level)
    data["last_challenger"] = OrderedDict(
        [
            ("id", text(lc_id)),
            ("name", text(lc_name)),
            ("site", text(lc_site)),
            ("url", text(lc_url)),
        ]
    )
    data["win_count"] = num(win_count)
    data["max_win_count"] = num(max_win_count)
    data["max_win_id"] = text(max_win_id)
    data["max_win_name"] = text(max_win_name)
    data["max_win_site"] = text(max_win_site)
    data["max_win_url"] = text(max_win_url)
    data["gold"] = num(gold)
    data["cha"] = num(cha)
    data["karma"] = num(karma)

    return data


def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} winner.cgi [winner.json]", file=sys.stderr)
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    fields = load_fields(in_file)
    data = convert(fields)
    text_out = json.dumps(data, ensure_ascii=False, indent=2)

    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text_out + "\n")
        print(f"wrote {out_file}")
    else:
        print(text_out)


if __name__ == "__main__":
    main()
