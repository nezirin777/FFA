#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#------------------------------------------------------#
#  FFA改 Vips Ver 3.00
#  作成者: ねじりん
#------------------------------------------------------#
#------------------------------------------------------#
#　本スクリプトの著作権は下記の4人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE 改i v2.1
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE v0.21
#　programed by CUMRO
#　http://cgi.members.interq.or.jp/sun/cumro/mm/
#　cumro@sun.interq.or.jp
#------------------------------------------------------#
#  FF ADVENTURE(改) v1.021
#  remodeling by GUN
#  http://www2.to/meeting/
#  gun24@j-club.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#
#　本スクリプトの著作権は下記の4人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE 改i v2.1
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#
#　FF ADVENTURE v0.21
#　programed by CUMRO
#　http://cgi.members.interq.or.jp/sun/cumro/mm/
#　cumro@sun.interq.or.jp
#------------------------------------------------------#
#  FF ADVENTURE(改) v1.021
#  remodeling by GUN
#  http://www2.to/meeting/
#  gun24@j-club.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#

"""
FFA Python/CGI - スキル・特殊効果定義モジュール (skills.py)
Perl版の *.pl ファイル群を Python クラス/メソッド構造に変換・集約したものです。
"""
import random

# ==========================================
# === FOLDER: TECH ===
# ==========================================

class tech_0:
    def hissatu(s):
        pass
    def atowaza(s):
        pass

class tech_1:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg1 += (s.chara['str'] + s.chara['job_level']) * random.randrange(int(50))
            s.com1 += "<font class='red' size='5'>必殺技凶斬り！！！</font><br>"

    def atowaza(s):
        pass

class tech_2:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dhit = random.randrange(int(7)) + 1
            s.dmg1 += (s.chara['str'] + s.chara['job_level']) * random.randrange(int(10))
            s.dmg1 = s.dmg1 * s.dhit
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>必殺技！！！超究武神覇斬！！！</font><font class=small>s.dhit連続ヒット！！</font><br>"

    def atowaza(s):
        pass

class tech_3:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(50))
            s.com1 += "<font class='red' size='5'>黒魔法ファイガ！！！</font><br>"

    def atowaza(s):
        pass

class tech_4:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(100))
            s.com1 += "<font class='red' size='5'>黒魔法フレア！！！</font><br>"

    def atowaza(s):
        pass

class tech_5:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dhit = random.randrange(int(15))+1
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(10))
            s.dmg1 = s.dmg1 * s.dhit
            s.sake2 -= 999999
            s.com1 += "<font class='yellow' size='5'>黒魔法メテオ！！！</font><font class=small>s.dhit連続ヒット！！</font><br>"

    def atowaza(s):
        pass

class tech_6:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg2 = int(s.dmg2 * 0.1)
            s.com1 += "<font class='white'>白魔法シェル！！！</font><br>"


class tech_7:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = 0
            s.hpplus1 = (s.chara['dex'] + s.chara['job_level']) + random.randrange(int(s.chara['lp']))
            s.com1 += "<font class='white' size='5'>白魔法ケアルガ！！！</font><br>"
            s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"

    def atowaza(s):
        pass

class tech_8:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['dex'] + s.chara['job_level']) * random.randrange(int(80))
            s.com1 += "<font class='white' size='5'>白魔法ホーリー！！！</font><br>"

    def atowaza(s):
        pass

class tech_9:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(80))):
            if (s.mode == 'isekai' or s.mode == 'boss' and random.randrange(int(4)) == 1):
                s.com1 += "s.chara['name']が叫んだ！<font size='5'>「あ！あれはなんだ！？？？？」</font>s.winner['url'] s.mnameには効かなかった！！<br>"
            else:
                s.sake2 -= 999999
                s.dmg2 = 0
                s.com1 += "s.chara['name']が叫んだ！<font size='5'>「あ！あれはなんだ！？？？？」</font>s.winner['url'] s.mnameに隙ができた！<br>"


class tech_10:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.temp_gold =  random.randrange(int(s.gold)) + 1
            s.com1 += "<font class='yellow'>お金を盗んだ♪合計s.temp_goldＧゲット♪</font><br>"
            s.gold += s.temp_gold

    def atowaza(s):
        pass

class tech_11:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1+= ((s.chara['agi']+s.chara['job_level']) * random.randrange(int(50)))
            s.com1 += "<font class='yellow' size='5'>必殺技ライフ・デジョン！！！</font><br>"
            s.hpplus1 = int(s.dmg1 / 5)
            s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪<br>"

    def atowaza(s):
        pass

class tech_12:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg1 = 0
            s.sake1 += 999
            s.com1 += "<font class='yellow' size='5'>時空魔法ヘイスト！！！（回避率激増）</font><br>"

    def atowaza(s):
        pass

class tech_13:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (s.mode == 'isekai' or s.mode == 'boss'):
                s.com1 += "<font class='yellow' size='5'>時空魔法ストップ！！！</FONT>s.mnameには効かなかった！！<br>"
            else:
                s.sake2 -= 999999
                s.dmg2 = 0
                s.com1 += "<font class='yellow' size='5'>時空魔法ストップ！！！</font>s.winner['url'] s.mnameの動きを止めた！<br>"


class tech_14:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.i = s.turn
            s.j = s.turn
            s.dmg1 = 0
            s.com1 += "<font class='yellow' size='5'>時空魔法テレポ！！！</font><br>"

    def atowaza(s):
        pass

class tech_15:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(80))
            s.com1 += "<font class='white' size='5'>赤魔法トルネド！！！</font><br>"

    def atowaza(s):
        pass

class tech_16:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.winner['battle_limit'] = 0
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(40))
            s.com1 += "<font class='red' size='5'>赤魔法メルトン！！！（防御力無効）</font><br>"

    def atowaza(s):
        pass

class tech_17:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (s.mode == 'isekai' or s.mode == 'boss'):
                s.com2 += "<font class='red' size='5'>赤魔法ウオール！！！</FONT>s.mnameには効かなかった！！<br>"
            else:
                s.sake1 += 999
                s.dmg2 = 0
                s.com1 += "<font class='white' size='5'>赤魔法ウオール！！！（全ての攻撃を無効）</font><br>"


class tech_18:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.hpplus1 = (s.chara['lck'] + s.chara['job_level']) + random.randrange(int(s.chara['lp']))
            s.dmg1 = 0
            s.com1 += "<font class='white' size='5'>s.chara['name']は回復の歌を歌った♪</font><br>"
            s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"

    def atowaza(s):
        pass

class tech_19:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake1 += 999
            s.dmg1 += s.dmg1
            s.com1 += "<font class='white' size='5'>s.chara['name']は勇奮の歌を歌った♪（攻撃力、回避率上昇）</font><br>"

    def atowaza(s):
        pass

class tech_20:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80 + s.syukuhuku * 40))):
            s.item['weapon']['dmg'] += s.item['weapon']['dmg']
            s.item['armor']['def'] += s.item['armor']['def']
            s.syukuhuku += 1
            s.com1 += "<font class='white' size='5'>s.chara['name']は祝福の歌を歌った♪（攻撃力、防御力増大、効果持続）</font><br>"

    def atowaza(s):
        pass

class tech_21:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(100))
            s.com1 += "<font class='red' size='4'>幻獣イフリートを召還！！地獄の火炎！！</font><br>"

    def atowaza(s):
        pass

class tech_22:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (random.randrange(int(3)) == 0):
                s.dmg1 = int(s.mhp / 3) + int(s.khp / 3)
                s.com1 += "<font class='blue' size='4'>幻獣ディアボロスを召還！！グラビガ！！</font><br>"

    def atowaza(s):
        pass

class tech_23:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (s.mode == 'isekai' or s.mode == 'boss'):
                s.com1 += "<font class='yellow' size='4'>幻獣カーバンクルを召還！！リフレク！！</FONT>s.mnameには効かなかった！！<br>"
            else:
                s.dmg1 += s.dmg2
                s.dmg2 = 0
                s.com1 += "<font class='yellow' size='4'>幻獣カーバンクルを召還！！リフレク！！（攻撃を反射）</font><br>"


class tech_24:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake1 += 999
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>ジャンプ！！</font><br>"

    def atowaza(s):
        pass

class tech_25:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake1 += 999
            s.sake2 -= 999999
            s.dmg1+= ((s.chara['str'] + s.chara['job_level']) * random.randrange(int(60)))
            s.com1 += "<font class='white' size='5'>ハイウインド！！</font><br>"

    def atowaza(s):
        pass

class tech_26:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake1 += 999
            s.sake2 -= 999999
            s.dmg1+= ((s.chara['str'] + s.chara['agi'] + s.chara['job_level']) * random.randrange(int(160)))
            s.com1 += "<font class='white' size='5'>旋空飛竜滅殺槍！！</font><br>"


class tech_27:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(160))
            s.com1 += "<font class='yellow' size='5'>黒魔法コメット！！！</font><br>"

    def atowaza(s):
        pass

class tech_28:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(300))
            s.com1 += "<font class='white' size='5'>神聖魔法ジハード！！！</font><br>"

    def atowaza(s):
        pass

class tech_29:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(150))):
            s.hpplus1 = s.chara['max_hp']
            s.dmg1 = 0
            s.com1 += "<font class='yellow' size='4'>大いなる福音♪s.chara['name']の傷が完全に回復した！！</font><br>"

    def atowaza(s):
        pass

class tech_30:
    def hissatu(s):
        pass
    def atowaza(s):
        s.dmg2 = int(s.dmg2 * 0.1)
        s.com1 += "s.chara['name']は防御している。。。<br>"


class tech_31:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80 + 40 * s.ora))):
            s.item['weapon']['dmg'] = s.item['weapon']['dmg'] * 2
            s.ora += 1
            s.com1 += "<font class='yellow' size='5'>古代魔法オーラ！！！（武器攻撃力２倍効果持続）</font><br>"

    def atowaza(s):
        pass

class tech_32:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['str'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(180))
            s.com1 += "<font class='white'>必殺技！！ホーリースラッシュ！！</font><br>"

    def atowaza(s):
        pass

class tech_33:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (s.mode != 'isekai' and s.mode != 'boss'):
                s.dmg2 = 0
                s.com1 += "<font class='white'>真剣白刃取り！！</font><br>"


class tech_34:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg1 += (s.chara['str'] + s.chara['agi'] + s.chara['mnd'] + s.chara['job_level']) * random.randrange(int(80))
            s.com1 += "<font class='white'>必殺技！！燕返し！！</font><br>"

    def atowaza(s):
        pass

class tech_35:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (random.randrange(int(5)) == 0):
                s.dmg1 = s.mhp + s.khp
                s.com1 += "<font class='white' size='6'><i>斬・鉄・剣！！</i></font><br>"
            else:
                s.com1 += "<font class='white'><i>斬・鉄・剣！！失敗！！</i></font><br>"

    def atowaza(s):
        pass

class tech_36:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg1 += (s.chara['str'] + s.chara['agi'] + s.chara['mnd'] + s.chara['job_level']) * random.randrange(int(80))
            s.com1 += "<font class='yellow' size='6'>s.chara['name']は大きな気の塊をs.mname s.winner['url']に放った！！</font><br>"

    def atowaza(s):
        pass

class tech_37:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dhit = random.randrange(int(7)) + 1
            s.dmg1 = s.dmg1 * s.dhit
            s.com1 += "<font class='yellow' size='4'>必殺技！！！無限乱武！！！</font><font class=small>s.dhit連続ヒット！！</font><br>"

    def atowaza(s):
        pass

class tech_38:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(80))
            s.com1 += "<font class='yellow' size='4'>必殺技！！！ファイナルヘヴン！！！</font><br>"

    def atowaza(s):
        pass

class tech_39:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake1 += 999
            s.sake2 -= 999999
            s.com1 += "<font class='green' size='4'>影縫いの術！！（姿を消してs.mname s.winner['url']に忍び寄る！！）</font><br>"

    def atowaza(s):
        pass

class tech_40:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dhit = random.randrange(int(7)) + 1
            s.dmg1 = s.dmg1 * s.dhit
            s.com1 += "<font class='yellow' size='4'>分身の術！！</font><font color=red>s.dhit体の分身が一斉に攻撃！！</font><br>"

    def atowaza(s):
        pass

class tech_41:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(20))
            s.sake2 -= 999999
            s.com1 += "<font class='yellow' size='4'>森羅万象！！（全てのエネルギーを解放！！）</font><br>"

    def atowaza(s):
        pass

class tech_42:
    def hissatu(s):
        s.dmg1 += s.chara['str'] * random.randrange(int(100))
        s.hpplus1 = int(0) - int(s.dmg1 * (random.random() * 0.1))
        s.com1 += "<font class='dark' size='5'>暗黒剣！！（自分にもs.hpplus1ダメージ）</font><br>"

    def atowaza(s):
        pass

class tech_43:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(20))
            s.hpplus1 = s.dmg1
            s.sake2 -= 999999
            s.com1 += "<font class='dark' size='4'>暗黒魔法ドレイン！！！</font><br>";s.kaihuku1 += "s.kname のＨＰが s.hpplus1 回復した！♪"

    def atowaza(s):
        pass

class tech_44:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['int'] + s.chara['job_level']) * random.randrange(int(360))
            s.hpplus1 = int(s.dmg1 / 10)
            s.com1 += "<font class='dark' size='4'>必殺技！！ダーク・イリュージョン！！！</font><br>"
            s.kaihuku1 += "s.kname のＨＰが s.hpplus1 回復した！♪"

    def atowaza(s):
        pass

class tech_45:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg1 += (s.chara['str'] + s.chara['int'] + s.chara['job_level']) * random.randrange(int(50))
            s.com1 += "<font class='red' size='5'>ファイガ剣！！！</font><br>"

    def atowaza(s):
        pass

class tech_46:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['str'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(80))
            s.com1 += "<font class='white' size='5'>ホーリー剣！！！</font><br>"

    def atowaza(s):
        pass

class tech_47:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(160))
            s.com1 += "<font class='yellow' size='5'>アルテマ剣！！！</font><br>"

    def atowaza(s):
        pass

class tech_48:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake2 -= 999999
            s.dmg1 += s.dmg1
            s.com1 += "狙いを定めた！！<br>"

    def atowaza(s):
        pass

class tech_49:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dhit = random.randrange(int(7))+1
            s.dmg1 = s.dmg1 * s.dhit
            s.com1 += "乱れ撃ち！！<font class=small>s.dhit連続ヒット！！</font><br>"

    def atowaza(s):
        pass

class tech_50:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (random.randrange(int(3)) == 0):
                s.dmg1 = s.mhp + s.khp
                s.sake2 -= 999999
                s.com1 += "<font class=red>急所に狙いを定めた！！</font><br>"

    def atowaza(s):
        pass

class tech_51:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(200))
            s.com1 += "<font class='blue' size='4'>幻獣リヴァイアサンを召還！！大海嘯！！</font><br>"

    def atowaza(s):
        pass

class tech_52:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(200))
            s.com1 += "<font class='red' size='4'>幻獣バハムートを召還！！メガフレア！！</font><br>"

    def atowaza(s):
        pass

class tech_53:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dhit = random.randrange(int(11))+1
            s.sake2 -= 999999
            s.dmg1 = (s.chara['int'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(100))
            s.dmg1 = s.dmg1 * s.dhit
            s.com1 += "<font class='yellow' size='4'>幻獣ナイツ・オブ・ラウンドを召還！！</font><font color=red>s.dhit人の騎士が力を貸した！！</font><br>"

    def atowaza(s):
        pass

class tech_54:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.sake2 -= 999999
            s.dmg1 =(s.chara['int'] + s.chara['dex'] + s.chara['job_level']) * random.randrange(int(160))
            s.com1 += "<font class='white' size='5'>禁断魔法アルテマ！！！</font><br>"

    def atowaza(s):
        pass

class tech_55:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            if (random.randrange(int(3)) == 0):
                s.sake2 -= 999999
                s.dmg1 = s.winner['max_hp'] + s.mhp_flg
                s.com1 += "<font class='yellow' size='5'>時空魔法デジョン！！！</font><br>"
            else:
                s.com1 += "<font class='red' size='5'>時空魔法デジョン！！！失敗した。。</font><br>"

    def atowaza(s):
        pass

class tech_56:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.sake2 -= 999999
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(360))
            s.com1 += "<font class='white' size='5'>青魔法ショック・ウェーブ・パルサー！！！</font><br>"

    def atowaza(s):
        pass

class tech_57:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dmg1 += (s.chara['str'] + s.chara['job_level']) * random.randrange(int(160))
            s.com1 += "<font class='yellow' size='5'>必殺技！！ラブディバイド！！</font><br>"

    def atowaza(s):
        pass

class tech_58:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 += (s.chara['str'] + s.chara['job_level']) * random.randrange(int(320))
            s.com1 += "<font class='yellow' size='5'>必殺技！！ブラスティングゾーン！！</font><br>"

    def atowaza(s):
        pass

class tech_59:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dhit = random.randrange(int(15)) + 1
            s.dmg1 += (s.chara['str'] + s.chara['mnd']) * random.randrange(int(80))
            s.dmg1 = s.dmg1 * s.dhit
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>必殺技！！！エンド・オブ・ハート！！！</font><font class=small>s.dhit連続ヒット！！</font><br>"

    def atowaza(s):
        pass

class tech_60:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(100))):
            s.com1 += "<font color='white'>s.chara['name']は、タロットカードを一枚捲った！！ 生か死か？ 全てはこの運命のカード一枚に委ねられたッ！！</font><br>"
            s.ura = random.randrange(int(22))
            if (0 == s.ura):
                s.com1 += "THE MAGICIAN！！！！\n"
                s.dmg1 += (s.chara['int'] + s.chara['dex']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (1 == s.ura):
                s.com1 += "THE CHARIOT！！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['agi']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (2 == s.ura):
                s.com1 += "STRENGTH！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['vit']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (3 == s.ura):
                s.com1 += "THE HIGH PRIESTESS！！！\n"
                s.dmg1 = 0
                s.hpplus1 = (s.chara['int'] + s.chara['dex']) * random.randrange(int(180))
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (4 == s.ura):
                s.com1 += "THE HIEROPHANT！！！！\n"
                s.dmg1 += (s.chara['str'] +s.chara['int'] + s.chara['dex']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (5 == s.ura):
                s.com1 += "THE EMPRESS！！！！\n"
                s.dmg1 += (s.chara['str'] +s.chara['int'] + s.chara['dex']) * random.randrange(int(120))
                s.sake2 -= 999999
            elif (6 == s.ura):
                s.com1 += "THE EMPEROR！！！！！\n"
                s.dmg1 += (s.chara['str'] +s.chara['int'] + s.chara['dex']) * random.randrange(int(180))
                s.sake2 -= 999999
            elif (7 == s.ura):
                s.com1 += "THE LOVERS！！！！\n"
                s.hpplus1 = s.chara['vit'] * random.randrange(int(80))
                s.dmg1 = 0
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (8 == s.ura):
                s.com1 += "THE HERMIT！！！！\n"
                s.dmg1 += s.chara['lck'] * random.randrange(int(80))
                s.sake2 -= 999999
            elif (9 == s.ura):
                s.com1 += "WHEEL of FORTUNE！！！！\n"
                s.dmg1 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (10 == s.ura):
                s.com1 += "JUSTICE！！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['dex'] ) * random.randrange(int(180))
                s.sake2 -= 999999
            elif (11 == s.ura):
                s.com1 += "THE HANGEDMAN！！！！\n"
                s.dmg1 = int(0)
            elif (12 == s.ura):
                s.com1 += "DEATH！！！！\n"
                s.dmg1 = s.khp + s.mhp + s.wd_dmg
                s.sake2 -= 999999
            elif (13 == s.ura):
                s.com1 += "TEMPERANCE！！！！\n"
                s.dmg1 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (14 == s.ura):
                s.com1 += "THE DEVIL！！！！\n"
                s.dmg1 = 0
                s.dmg2 = s.khp
                s.sake1 -= 999999
            elif (15 == s.ura):
                s.com1 += "THE TOWER！！！！\n"
                s.hpplus2 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(180))
                s.dmg1 = 0
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (16 == s.ura):
                s.com1 += "THE STAR！！！！\n"
                s.dmg1 += (s.chara['dex'] + s.chara['lck']) * random.randrange(int(80))
            elif (17 == s.ura):
                s.com1 += "THE MOON！！！！\n"
                s.hpplus1 = (s.chara['int'] + s.chara['dex']) * random.randrange(int(80))
                s.dmg1 = 0
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (18 == s.ura):
                s.com1 += "THE SUN！！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['agi']) * random.randrange(int(999))
                s.sake2 -= 999999
            elif (19 == s.ura):
                s.com1 += "THE JUDGEMENT！！！！\n"
                s.dmg1 += (s.chara['int'] + s.chara['dex']) * random.randrange(int(999))
                s.sake2 -= 999999
            elif (20 == s.ura):
                s.com1 += "THE WORLD！！！！\n"
                s.dmg1 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(80))
                s.sake2 -= 999999
            else:
                s.com1 += "THE FOOL\n"
                s.dmg1 = int(1)

    def atowaza(s):
        pass

class tech_61:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(100))):
            s.com1 += "<font color='white'>s.chara['name']は、タロットカードを一枚捲った！！ 生か死か？ 全てはこの運命のカード一枚に委ねられたッ！！</font><br>"
            s.ura = random.randrange(int(22))
            if (0 == s.ura):
                s.com1 += "THE MAGICIAN！！！！\n"
                s.dmg1 += (s.chara['int'] + s.chara['dex']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (1 == s.ura):
                s.com1 += "THE CHARIOT！！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['agi']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (2 == s.ura):
                s.com1 += "STRENGTH！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['vit']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (3 == s.ura):
                s.com1 += "THE HIGH PRIESTESS！！！\n"
                s.dmg1 = 0
                s.hpplus1 = (s.chara['int'] + s.chara['dex']) * random.randrange(int(180))
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (4 == s.ura):
                s.com1 += "THE HIEROPHANT！！！！\n"
                s.dmg1 += (s.chara['str'] +s.chara['int'] + s.chara['dex']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (5 == s.ura):
                s.com1 += "THE EMPRESS！！！！\n"
                s.dmg1 += (s.chara['str'] +s.chara['int'] + s.chara['dex']) * random.randrange(int(120))
                s.sake2 -= 999999
            elif (6 == s.ura):
                s.com1 += "THE EMPEROR！！！！！\n"
                s.dmg1 += (s.chara['str'] +s.chara['int'] + s.chara['dex']) * random.randrange(int(180))
                s.sake2 -= 999999
            elif (7 == s.ura):
                s.com1 += "THE LOVERS！！！！\n"
                s.hpplus1 = s.chara['vit'] * random.randrange(int(80))
                s.dmg1 = 0
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (8 == s.ura):
                s.com1 += "THE HERMIT！！！！\n"
                s.dmg1 += s.chara['lck'] * random.randrange(int(80))
                s.sake2 -= 999999
            elif (9 == s.ura):
                s.com1 += "WHEEL of FORTUNE！！！！\n"
                s.dmg1 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (10 == s.ura):
                s.com1 += "JUSTICE！！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['dex'] ) * random.randrange(int(180))
                s.sake2 -= 999999
            elif (11 == s.ura):
                s.com1 += "THE HANGEDMAN！！！！\n"
                s.dmg1 = int(0)
            elif (12 == s.ura):
                s.com1 += "DEATH！！！！\n"
                s.dmg1 = s.khp + s.mhp + s.wd_dmg
                s.sake2 -= 999999
            elif (13 == s.ura):
                s.com1 += "TEMPERANCE！！！！\n"
                s.dmg1 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(80))
                s.sake2 -= 999999
            elif (14 == s.ura):
                s.com1 += "THE DEVIL！！！！\n"
                s.dmg1 = 0
                s.dmg2 = s.khp
                s.sake1 -= 999999
            elif (15 == s.ura):
                s.com1 += "THE TOWER！！！！\n"
                s.hpplus2 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(180))
                s.dmg1 = 0
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (16 == s.ura):
                s.com1 += "THE STAR！！！！\n"
                s.dmg1 += (s.chara['dex'] + s.chara['lck']) * random.randrange(int(80))
            elif (17 == s.ura):
                s.com1 += "THE MOON！！！！\n"
                s.hpplus1 = (s.chara['int'] + s.chara['dex']) * random.randrange(int(80))
                s.dmg1 = 0
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (18 == s.ura):
                s.com1 += "THE SUN！！！！\n"
                s.dmg1 += (s.chara['str'] + s.chara['agi']) * random.randrange(int(999))
                s.sake2 -= 999999
            elif (19 == s.ura):
                s.com1 += "THE JUDGEMENT！！！！\n"
                s.dmg1 += (s.chara['int'] + s.chara['dex']) * random.randrange(int(999))
                s.sake2 -= 999999
            elif (20 == s.ura):
                s.com1 += "THE WORLD！！！！\n"
                s.dmg1 = (s.chara['str'] +s.chara['int'] + s.chara['dex'] + s.chara['vit'] +s.chara['agi'] + s.chara['mnd'] + s.chara['lck']) * random.randrange(int(80))
                s.sake2 -= 999999
            else:
                s.com1 += "THE FOOL\n"
                s.dmg1 = int(1)
            s.dmg1 += s.dmg1
            s.dmg2 += s.dmg2
            s.hpplus1 += s.hpplus1
            s.hpplus2 += s.hpplus2
            s.com1 += "<font color=s.red>効果倍増</font><br>"

    def atowaza(s):
        pass

class tech_62:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(400))
            s.sake2 -= 999999
            s.com1 += "<font class='yellow' size='4'>スター・ダスト・フォーチューン（全ての運命を砕く。。。）</font><br>"

    def atowaza(s):
        pass

class tech_63:
    def hissatu(s):
        pass
    def atowaza(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = s.dmg2
            s.sake1 = s.sake2
            s.hpplus1 = s.hpplus2
            s.clit1 = s.clit2
            if (s.hpplus1):
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            s.com1 += "<font class='red'>s.mname s.winner['url']のものまね〜♪</font><br>"


class tech_64:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(80))):
            s.dhit = random.randrange(int(15))+1 * 2
            s.dmg1 = (s.chara['int'] + s.chara['job_level']) * random.randrange(int(20))
            s.dmg1 = s.dmg1 * s.dhit
            s.sake2 -= 999999
            s.com1 += "<font class='yellow' size='5'>古代魔法Ｗメテオ！！！</font><font class=small>s.dhit連続ヒット！！</font><br>"

    def atowaza(s):
        pass

class tech_65:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['int'] + s.chara['dex']) * random.randrange(int(100))
            s.com1 += "<font class='yellow' size='5'>禁断魔法アルテマ！！</font>"
            if (s.waza_ritu > random.randrange(int(80))):
                s.dmg1 += (s.chara['dex']) * random.randrange(int(80))
                s.com1 += "<font class='white' size='5'>ホーリー！！</font>"
            if (s.waza_ritu > random.randrange(int(80))):
                s.dmg1 += (s.chara['int']) * random.randrange(int(80))
                s.com1 += "<font class='red' size='5'>フレア！！</font>"
            if (s.waza_ritu > random.randrange(int(80))):
                s.dmg1 += (s.chara['int']) * random.randrange(int(100))
                s.com1 += "<font class='red' size='5'>メテオ！！</font>"
            s.com1 += "<br>\n"
            s.sake2 -= 999999

    def atowaza(s):
        pass

class tech_66:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 =(s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(800))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>最強魔法アポガリプス！！！</font><br>"

    def atowaza(s):
        pass

class tech_67:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(400))
            s.sake2 -= 999
            s.com1 += "<font class='white' size='5'>闇にまぎれて敵に襲い掛かった！！！</font><br>"

    def atowaza(s):
        pass

class tech_68:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(1000))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>辺りが暗闇に包まれた！秘儀　真・獄刹！！</font><br>"

    def atowaza(s):
        pass

class tech_69:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.hpplus1 = (s.chara['dex'] + s.chara['vit'] + s.chara['job_level']) + random.randrange(int(s.chara['lp']))
            s.dmg1 = 0
            s.com1 += "<font class='white' size='5'>光・あれ！！！</font><br>"
            s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"

    def atowaza(s):
        pass

class tech_70:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(1000))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>極大聖魔法・オメガホーリー！！</font><br>"

    def atowaza(s):
        pass

class tech_73:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(500))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>秘儀　神極剣！！</font><br>"

    def atowaza(s):
        pass

class tech_74:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(1500))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>神極剣奥義・羅刹！！！</font><br>"

    def atowaza(s):
        pass

class tech_75:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(500))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>聖・エンドオブハート！！！</font><br>"

    def atowaza(s):
        pass

class tech_76:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(1200))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>ライトニングダスト！！！</font><br>"

    def atowaza(s):
        pass

class tech_77:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(800))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>食らえ！！アバン・ストラッシュ！！！</font><br>"

    def atowaza(s):
        pass

class tech_78:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(180))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(1800))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>ギガ・ブレイク！！！</font><br>"

    def atowaza(s):
        pass

class tech_79:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(120))):
            s.dmg1 = (s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(1200))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>グローリアス！！！</font><br>"

    def atowaza(s):
        pass

class tech_80:
    def hissatu(s):
        if (s.waza_ritu > random.randrange(int(150))):
            s.dmg1 =(s.chara['str'] + s.chara['int'] + s.chara['dex'] + s.chara['vit'] + s.chara['agi'] + s.chara['mnd'] + s.chara['lck'] + s.chara['lp'] + s.chara['job_level']) * random.randrange(int(2400))
            s.sake2 -= 999999
            s.com1 += "<font class='white' size='5'>神魔法ファイナル・ブレイカー！！！</font><br>"

    def atowaza(s):
        pass

# ==========================================
# === FOLDER: WTECH ===
# ==========================================

class wtech_0:
    def whissatu(s):
        pass
    def watowaza(s):
        pass

class wtech_1:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg2 += (s.winner['img'] + s.winner['attr_39']) * random.randrange(int(50))
            s.com2 += "<font class='red' size='5'>必殺技凶斬り！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_2:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(150))):
            s.dwhit = random.randrange(int(7))+1;	s.dmg2 +=(s.winner['img'] + s.winner['attr_39'])* random.randrange(int(10))
            s.dmg2 =s.dmg2 *s.dwhit
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>必殺技！！！超究武神覇斬！！！</font><font class=small>s.dwhit連続ヒット！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_3:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake1 -= 999999
            s.dmg2 =(s.winner['str'] + s.winner['attr_39'])* random.randrange(int(50))
            s.com2 += "<font class='red' size='5'>黒魔法ファイガ！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_4:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(100))
            s.com2 += "<font class='red' size='5'>黒魔法フレア！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_5:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dwhit = random.randrange(int(15))+1
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(10))
            s.dmg2 = s.dmg2 * s.dwhit
            s.sake1 -= 999999
            s.com2 += "<font class='yellow' size='5'>黒魔法メテオ！！！</font><font class=small>s.dwhit連続ヒット！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_6:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg1 = int(s.dmg1 * 0.1)
            s.com2 += "<font class='white'>白魔法シェル！！！</FONT><br>"


class wtech_7:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = 0
            s.hpplus2 = (s.winner['int'] + s.winner['attr_39']) * random.randrange(int(s.winner['lck']))
            if (s.hpplus2 > s.winner['max_hp']/10):
                s.hpplus2 = s.winner['max_hp']/10
            s.com2 += "<br><font class='yellow' size='3'>白魔法ケアルガ！！！</FONT><br>"
            s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"

    def watowaza(s):
        pass

class wtech_8:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['int'] + s.winner['attr_39']) * random.randrange(int(80))
            s.com2 += "<font class='white' size='5'>白魔法ホーリー！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_9:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            if (random.randrange(int(4)) == 0):
                s.com2 += "s.winner['url']が叫んだ！<font size='5'>「あ！あれはなんだ！？？？？」</font>s.chara['name']には効かなかった！！<br>"
            else:
                s.sake1 -= 999999
                s.dmg1 = 0
                s.com2 += "s.winner['url']が叫んだ！<font size='5'>「あ！あれはなんだ！？？？？」</font>s.chara['name']に隙ができた！<br>"

class wtech_10:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.gold -= int(s.kgold /25)
            s.com2 += "<font class='red'>お金を盗まれた！！合計s.goldＧマイナス！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_11:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = s.dmg2 + ((s.winner['vit'] + s.winner['attr_39']) * random.randrange(int(50)))
            s.com2 += "<font class='yellow' size='5'>必殺技ライフ・デジョン！！！</FONT><br>"
            s.hpplus2 = int(s.dmg2 /5)
            s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"

    def watowaza(s):
        pass

class wtech_12:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg2 = 0
            s.sake2 += 999;	s.com2 += "<font class='yellow' size='5'>時空魔法ヘイスト！！！（回避率激増）</FONT><br>"

    def watowaza(s):
        pass

class wtech_13:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (random.randrange(int(4)) == 0):
                s.com2 += "<font class='yellow' size='5'>時空魔法ストップ！！！</FONT>s.chara['name']には効かなかった！！<br>"
            else:
                s.sake1 -= 999999
                s.dmg1 = 0
                s.com2 += "<font class='yellow' size='5'>時空魔法ストップ！！！</FONT>s.chara['name']の動きを止めた！<br>"

class wtech_14:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = 0
            s.i = s.turn
            s.com2 += "<font class='yellow' size='5'>時空魔法テレポ！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_15:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(80))
            s.com2 += "<font class='white' size='5'>赤魔法トルネド！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_16:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.item['armor']['def'] = 0
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(40))
            s.com2 += "<font class='red' size='5'>赤魔法メルトン！！！（防御力無効）</FONT><br>"

    def watowaza(s):
        pass

class wtech_17:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (random.randrange(int(4)) == 0):
                s.com2 += "<font class='red' size='5'>赤魔法ウオール！！！</FONT>s.chara['name']には効かなかった！！<br>"
            else:
                s.sake2 += 999
                s.dmg1 = 0
                s.com2 += "<font class='red' size='5'>赤魔法ウオール！！！（全ての攻撃を無効）</FONT><br>"

class wtech_18:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(200))):
            s.dmg2 = 0
            s.hpplus2 = ((s.winner['mnd'] + s.winner['attr_39']) + random.randrange(int(s.winner['lck'])))/10
            s.com2 += "<font class='yellow' size='3'>s.winner['url']は回復の歌を歌った♪</FONT><br>"
            s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"

    def watowaza(s):
        pass

class wtech_19:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake2 += 999
            s.dmg2 += s.dmg2
            s.com2 += "<font class='yellow' size='3'>s.winner['url']は勇奮の歌を歌った♪（攻撃力、回避率上昇）</FONT><br>"

    def watowaza(s):
        pass

class wtech_20:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.winner['attr_22'] += s.winner['attr_22']
            s.winner['battle_limit'] += s.winner['battle_limit']
            s.com2 += "<font class='yellow' size='3'>s.winner['url']は祝福の歌を歌った♪（攻撃力、防御力増大、効果持続）</FONT><br>"

    def watowaza(s):
        pass

class wtech_21:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(100))
            s.com2 += "<font class='red' size='4'>幻獣イフリートを召還！！地獄の火炎！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_22:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = int(s.khp / 3)
            s.com2 += "<font color='#000055' size='4'>幻獣ディアボロスを召還！！グラビガ！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_23:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (random.randrange(int(4)) == 0):
                s.com2 += "<font class='yellow' size='4'>幻獣カーバンクルを召還！！リフレク！！</FONT>s.chara['name']には効かなかった！！<br>"
            else:
                s.dmg2 += s.dmg1
                s.dmg1 = 0
                s.com2 += "<font class='yellow' size='4'>幻獣カーバンクルを召還！！リフレク！！（攻撃を反射）</FONT><br>"

class wtech_24:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake2 += 999
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>ジャンプ！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_25:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake2 += 999
            s.sake1 -= 999999
            s.dmg2 = s.dmg2 + ((s.winner['img'] + s.winner['attr_39']) * random.randrange(int(60)))
            s.com2 += "<font class='white' size='5'>ハイウインド！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_26:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake2 += 999
            s.sake1 -= 999999
            s.dmg2 = s.dmg2 + ((s.winner['img'] + s.winner['vit'] + s.winner['attr_39']) * random.randrange(int(160)))
            s.com2 += "<font class='white' size='5'>旋空飛竜滅殺槍！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_27:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(160))
            s.com2 += "<font class='yellow' size='5'>黒魔法コメット！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_28:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(300))
            s.com2 += "<font class='white' size='5'>神聖魔法ジハード！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_29:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(150))):
            s.hpplus2 = int(s.chara['max_hp'] * 1 / 100)
            s.dmg2 = 0
            s.com2 += "<font class='yellow' size='4'>大いなる福音により、s.winner['url']の傷の一部が回復</FONT><br>"

    def watowaza(s):
        pass

class wtech_30:
    def whissatu(s):
        pass
    def watowaza(s):
        s.dmg2 = int(s.dmg2 * 0.5)
        s.com2 += "s.winner['url']は防御している。。。<br>"


class wtech_31:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.winner['attr_22'] = s.winner['attr_22'] * 2
            s.com2 += "<font class='yellow' size='5'>古代魔法オーラ！！！（武器攻撃力２倍効果持続）</FONT><br>"

    def watowaza(s):
        pass

class wtech_32:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 +=(s.winner['img'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(180))
            s.com2 += "<font class='white'>必殺技！！ホーリースラッシュ！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_33:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (s.ksyoku <= 16):
                s.dmg1 = 0
                s.com2 += "<font class='white'>真剣白刃取り！！</FONT><br>"

class wtech_34:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg2 +=(s.winner['img'] + s.winner['vit'] + s.winner['agi'] + s.winner['attr_39']) * random.randrange(int(80))
            s.com2 += "<font color='#FFaaaa'>必殺技！！燕返し！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_35:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (random.randrange(int(3)) == 0):
                s.dmg2 = s.khp
                s.com2 += "<font class='white' size='6'><i>斬・鉄・剣！！</i></FONT><br>"
            else:
                s.com2 += "<font class='white'><i>斬・鉄・剣！！失敗！！</i></font><br>"
    def watowaza(s):
        pass

class wtech_36:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg2 +=(s.winner['img'] + s.winner['vit'] + s.winner['agi'] + s.winner['attr_39']) * random.randrange(int(80))
            s.com2 += "<font class='yellow' size='6'>s.winner['url']は大きな気の塊をs.chara['name']に放った！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_37:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dwhit = random.randrange(int(7))+1
            s.dmg2 = s.dmg2 * s.dwhit
            s.com2 += "<font class='yellow' size='4'>必殺技！！！無限乱武！！！</font><font class=small>s.dwhit連続ヒット！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_38:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 +=(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(80))
            s.com2 += "<font class='yellow' size='4'>必殺技！！！ファイナルヘヴン！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_39:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake2 += 999
            s.sake1 -= 999999
            s.com2 += "<font color='#006600' size='4'>影縫いの術！！（姿を消してs.chara['name']に忍び寄る！！）</FONT><br>"

    def watowaza(s):
        pass

class wtech_40:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dwhit = random.randrange(int(7))+1
            s.dmg2 = s.dmg2 * s.dwhit
            s.com2 += "<font class='yellow' size='4'>分身の術！！</font><font class=small>s.dwhit体の分身が一斉に攻撃！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_41:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 +=(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(20))
            s.sake1 -= 999999
            s.com2 += "<font class='yellow' size='4'>森羅万象！！（全てのエネルギーを解放！！）</FONT><br>"

    def watowaza(s):
        pass

class wtech_42:
    def whissatu(s):
        s.dmg2 += s.winner['img'] * random.randrange(int(10))
        s.hpplus2 = int(0)-int(s.dmg2 /10)
        s.com2 += "<font color='#005555' size='5'>暗黒剣！！（自分にもダメージ）</FONT><br>"

    def watowaza(s):
        pass

class wtech_43:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(20))
            s.hpplus2 = s.dmg2
            s.sake1 -= 999999
            s.com2 += "<font color='#009999' size='4'>暗黒魔法ドレイン！！！</FONT><br>"
            s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"

    def watowaza(s):
        pass

class wtech_44:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 += (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(360))
            s.hpplus2 = int(s.dmg2 / 10)
            s.com2 += "<font color='#009999' size='4'>必殺技！！ダーク・イリュージョン！！！</FONT><br>"
            s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"

    def watowaza(s):
        pass

class wtech_45:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['attr_39']) * random.randrange(int(50))
            s.com2 += "<font class='red' size='5'>ファイガ剣！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_46:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 += (s.winner['img'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(80))
            s.com2 += "<font class='white' size='5'>ホーリー剣！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_47:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(160))
            s.com2 += "<font class='yellow' size='5'>アルテマ剣！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_48:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake1 -= 999999
            s.dmg2 += s.dmg2
            s.com2 += "狙いを定めた！！<br>"

    def watowaza(s):
        pass

class wtech_49:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dwhit = random.randrange(int(7))+1
            s.dmg2 = s.dmg2 * s.dwhit
            s.com2 += "乱れ撃ち！！<font class=small>s.dwhit連続ヒット！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_50:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (random.randrange(int(3)) == 0):
                s.dmg2 = s.khp
                s.sake1 -= 999999
                s.com2 += "<font color=red>急所に狙いを定めた！！</FONT><br>"
    def watowaza(s):
        pass

class wtech_51:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(200))
            s.com2 += "<font class='blue' size='4'>幻獣リヴァイアサンを召還！！大海嘯！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_52:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(200))
            s.com2 += "<font class='red' size='4'>幻獣バハムートを召還！！メガフレア！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_53:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dwhit = random.randrange(int(11))+1
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(100))
            s.dmg2 = s.dmg2 * s.dwhit
            s.com2 += "<font class='yellow' size='4'>幻獣ナイツ・オブ・ラウンドを召還！！</font><font class=small>s.dwhit人の騎士が力を貸した！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_54:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.sake1 -= 999999
            s.dmg2 =(s.winner['str'] + s.winner['int'] + s.winner['attr_39']) * random.randrange(int(160))
            s.com2 += "<font class='white' size='5'>禁断魔法アルテマ！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_55:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            if (random.randrange(int(3)) == 0):
                s.sake1 -= 999999
                s.dmg2 = s.chara['max_hp']
                s.com2 += "<font class='yellow' size='5'>時空魔法デジョン！！！</FONT><br>"
            else:
                s.com2 += "<font class='red' size='5'>時空魔法デジョン！！！失敗した。。</FONT><br>"
    def watowaza(s):
        pass

class wtech_56:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.sake1 -= 999999
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(360))
            s.com2 += "<font class='white' size='5'>青魔法ショック・ウェーブ・パルサー！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_57:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dmg2 += (s.winner['img'] + s.winner['attr_39']) * random.randrange(int(160))
            s.com2 += "<font class='yellow' size='5'>必殺技！！ラブディバイド！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_58:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 += (s.winner['img'] + s.winner['attr_39']) * random.randrange(int(320))
            s.com2 += "<font class='yellow' size='5'>必殺技！！ブラスティングゾーン！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_59:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dwhit = random.randrange(int(15))+1
            s.dmg2 += (s.winner['img'] + s.winner['agi']) * random.randrange(int(80))
            s.dmg2 = s.dmg2 * s.dwhit
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>必殺技！！！エンド・オブ・ハート！！！</font><font class=small>s.dwhit連続ヒット！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_60:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(100))):
            s.com2 += "<font color='white'>s.winner['url']は、タロットカードを一枚捲った！！ 生か死か？ 全てはこの運命のカード一枚に委ねられたッ！！</font><br>"
            s.ura = random.randrange(int(22))
            if (0 == s.ura):
                s.com2 += "THE MAGICIAN！！！！\n"
                s.dmg2 += (s.winner['str'] + s.winner['int']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (1 == s.ura):
                s.com2 += "THE CHARIOT！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['vit']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (2 == s.ura):
                s.com2 += "STRENGTH！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['dex']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (3 == s.ura):
                s.com2 += "THE HIGH PRIESTESS！！！\n"
                s.dmg2 = 0
                s.hpplus2 = (s.winner['str'] + s.winner['int']) * random.randrange(int(180))
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (4 == s.ura):
                s.com2 += "THE HIEROPHANT！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (5 == s.ura):
                s.com2 += "THE EMPRESS！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int']) * random.randrange(int(120))
                s.sake1 -= 999999
            elif (6 == s.ura):
                s.com2 += "THE EMPEROR！！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int']) * random.randrange(int(180))
                s.sake1 -= 999999
            elif (7 == s.ura):
                s.com2 += "THE LOVERS！！！！\n"
                s.dmg2 = 0
                s.hpplus2 = s.winner['dex'] * random.randrange(int(80))
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (8 == s.ura):
                s.com2 += "THE HERMIT！！！！\n"
                s.dmg2 += s.winner['mnd'] * random.randrange(int(80))
                s.sake1 -= 999999
            elif (9 == s.ura):
                s.com2 += "WHEEL of FORTUNE！！！！\n"
                s.dmg2 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (10 == s.ura):
                s.com2 += "JUSTICE！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['int'] ) * random.randrange(int(180))
                s.sake1 -= 999999
            elif (11 == s.ura):
                s.com2 += "THE HANGEDMAN！！！！\n"
                s.dmg2 = int(0)
            elif (12 == s.ura):
                s.com2 += "DEATH！！！！\n"
                s.dmg2 = s.khp + s.item['armor']['def']
                s.sake1 -= 999999
            elif (13 == s.ura):
                s.com2 += "TEMPERANCE！！！！\n"
                s.dmg2 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(80));	s.sake1 -= 999999
            elif (14 == s.ura):
                s.com2 += "THE DEVIL！！！！\n"
                s.dmg2 = 0
                s.dmg1 = s.khp
                s.sake2 -= 999999
            elif (15 == s.ura):
                s.com2 += "THE TOWER！！！！\n"
                s.dmg2 = 0
                s.hpplus1 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(180))
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (16 == s.ura):
                s.com2 += "THE STAR！！！！\n"
                s.dmg2 += (s.winner['int'] + s.winner['mnd']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (17 == s.ura):
                s.com2 += "THE MOON！！！！\n"
                s.dmg2 = 0
                s.hpplus2 = (s.winner['str'] + s.winner['int']) * random.randrange(int(80))
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (18 == s.ura):
                s.com2 += "THE SUN！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['vit']) * random.randrange(int(999))
                s.sake1 -= 999999
            elif (19 == s.ura):
                s.com2 += "THE JUDGEMENT！！！！\n"
                s.dmg2 += (s.winner['str'] + s.winner['int']) * random.randrange(int(999))
                s.sake1 -= 999999
            elif (20 == s.ura):
                s.com2 += "THE WORLD！！！！\n"
                s.dmg2 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(80))
                s.sake1 -= 999999
            else:
                s.com2 += "THE FOOL\n"
                s.dmg2 = int(1)

    def watowaza(s):
        pass

class wtech_61:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(100))):
            s.com2 += "<font color='white'>s.winner['url']は、タロットカードを一枚捲った！！ 生か死か？ 全てはこの運命のカード一枚に委ねられたッ！！</font><br>"
            s.ura = random.randrange(int(22))
            if (0 == s.ura):
                s.com2 += "THE MAGICIAN！！！！\n"
                s.dmg2 += (s.winner['str'] + s.winner['int']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (1 == s.ura):
                s.com2 += "THE CHARIOT！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['vit']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (2 == s.ura):
                s.com2 += "STRENGTH！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['dex']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (3 == s.ura):
                s.com2 += "THE HIGH PRIESTESS！！！\n"
                s.dmg2 = 0
                s.hpplus2 = (s.winner['str'] + s.winner['int']) * random.randrange(int(180))
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (4 == s.ura):
                s.com2 += "THE HIEROPHANT！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (5 == s.ura):
                s.com2 += "THE EMPRESS！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int']) * random.randrange(int(120))
                s.sake1 -= 999999
            elif (6 == s.ura):
                s.com2 += "THE EMPEROR！！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['str'] + s.winner['int']) * random.randrange(int(180))
                s.sake1 -= 999999
            elif (7 == s.ura):
                s.com2 += "THE LOVERS！！！！\n"
                s.dmg2 = 0
                s.hpplus2 = s.winner['dex'] * random.randrange(int(80))
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (8 == s.ura):
                s.com2 += "THE HERMIT！！！！\n"
                s.dmg2 += s.winner['mnd'] * random.randrange(int(80))
                s.sake1 -= 999999
            elif (9 == s.ura):
                s.com2 += "WHEEL of FORTUNE！！！！\n"
                s.dmg2 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (10 == s.ura):
                s.com2 += "JUSTICE！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['int'] ) * random.randrange(int(180))
                s.sake1 -= 999999
            elif (11 == s.ura):
                s.com2 += "THE HANGEDMAN！！！！\n"
                s.dmg2 = int(0)
            elif (12 == s.ura):
                s.com2 += "DEATH！！！！\n"
                s.dmg2 = s.khp + s.item['armor']['def']
                s.sake1 -= 999999
            elif (13 == s.ura):
                s.com2 += "TEMPERANCE！！！！\n"
                s.dmg2 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(80));	s.sake1 -= 999999
            elif (14 == s.ura):
                s.com2 += "THE DEVIL！！！！\n"
                s.dmg2 = 0
                s.dmg1 = s.khp
                s.sake2 -= 999999
            elif (15 == s.ura):
                s.com2 += "THE TOWER！！！！\n"
                s.dmg2 = 0
                s.hpplus1 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(180))
                s.kaihuku1 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
            elif (16 == s.ura):
                s.com2 += "THE STAR！！！！\n"
                s.dmg2 += (s.winner['int'] + s.winner['mnd']) * random.randrange(int(80))
                s.sake1 -= 999999
            elif (17 == s.ura):
                s.com2 += "THE MOON！！！！\n"
                s.dmg2 = 0
                s.hpplus2 = (s.winner['str'] + s.winner['int']) * random.randrange(int(80))
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            elif (18 == s.ura):
                s.com2 += "THE SUN！！！！\n"
                s.dmg2 += (s.winner['img'] + s.winner['vit']) * random.randrange(int(999))
                s.sake1 -= 999999
            elif (19 == s.ura):
                s.com2 += "THE JUDGEMENT！！！！\n"
                s.dmg2 += (s.winner['str'] + s.winner['int']) * random.randrange(int(999))
                s.sake1 -= 999999
            elif (20 == s.ura):
                s.com2 += "THE WORLD！！！！\n"
                s.dmg2 = (s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd']) * random.randrange(int(80))
                s.sake1 -= 999999
            else:
                s.com2 += "THE FOOL\n"
                s.dmg2 = int(1)
            s.dmg1 += s.dmg1
            s.dmg2 += s.dmg2
            s.hpplus1 += s.hpplus1
            s.hpplus2 += s.hpplus2
            s.com2 += "<font color=s.red>効果倍増</font><br>"

    def watowaza(s):
        pass

class wtech_62:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(400))
            s.sake1 -= 999999
            s.com2 += "<font class='yellow' size='4'>スター・ダスト・フォーチューン（全ての運命を砕く。。。）</FONT><br>"

    def watowaza(s):
        pass

class wtech_63:
    def whissatu(s):
        pass
    def watowaza(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = s.dmg1
            s.sake2 = s.sake1
            s.hpplus2 = s.hpplus1
            s.clit2 = s.clit1
            if (s.hpplus2):
                s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"
            s.com2 += "<font class='red'>s.chara['name']のものまね〜♪</FONT><br>"


class wtech_64:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(80))):
            s.dwhit = random.randrange(int(15))+1 * 2
            s.dmg2 = (s.winner['str'] + s.winner['attr_39']) * random.randrange(int(20))
            s.dmg2 = s.dmg2 * s.dwhit
            s.sake1 -= 999999
            s.com2 += "<font class='yellow' size='5'>古代魔法Ｗメテオ！！！</font><font class=small>s.dwhit連続ヒット！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_65:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 = (s.winner['str'] + s.winner['int']) * random.randrange(int(100))
            s.com2 += "<font class='yellow' size='5'>禁断魔法アルテマ！！</font>"
            if (s.wwaza_ritu > random.randrange(int(80))):
                s.dmg2 += (s.winner['int']) * random.randrange(int(80))
                s.com2 += "<font class='white' size='5'>ホーリー！！</font>"
            if (s.wwaza_ritu > random.randrange(int(80))):
                s.dmg2 += (s.winner['str']) * random.randrange(int(80))
                s.com2 += "<font class='red' size='5'>フレア！！</font>"
            if (s.wwaza_ritu > random.randrange(int(80))):
                s.dmg2 += (s.winner['str']) * random.randrange(int(100))
                s.com2 += "<font class='red' size='5'>メテオ！！</font>"
            s.sake1 -= 999999

    def watowaza(s):
        pass

class wtech_66:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(800))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>最強魔法アポガリプス！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_67:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(400))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>闇にまぎれて敵に襲い掛かった！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_68:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(1000))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>辺りが暗闇に包まれた！秘儀　真・獄刹！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_69:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.hpplus2 = (s.winner['int'] + s.winner['dex'] + s.winner['attr_39']) + random.randrange(int(s.winner['lck']))
            s.dmg2 = 0
            s.com2 += "<font class='white' size='5'>光・あれ！！！</font><br>"
            s.kaihuku2 += "s.winner['url'] のＨＰが s.hpplus2 回復した！♪"

    def watowaza(s):
        pass

class wtech_70:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(1000))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>極大聖魔法・オメガホーリー！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_71:
    def whissatu(s):
        pass
    def watowaza(s):
        pass

class wtech_72:
    def whissatu(s):
        pass
    def watowaza(s):
        pass

class wtech_73:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(500))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>秘儀　神極剣！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_74:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(1500))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>神極剣奥義・羅刹！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_75:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(500))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>聖・エンドオブハート！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_76:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(1200))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>ライトニングダスト！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_77:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(800))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>食らえ！！アバン・ストラッシュ！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_78:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(180))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(1800))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>食らえ！！ギガ・ブレイク！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_79:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(120))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(1200))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>グローリアス！！！</FONT><br>"

    def watowaza(s):
        pass

class wtech_80:
    def whissatu(s):
        if (s.wwaza_ritu > random.randrange(int(150))):
            s.dmg2 =(s.winner['img'] + s.winner['str'] + s.winner['int'] + s.winner['dex'] + s.winner['vit'] + s.winner['agi'] + s.winner['mnd'] + s.winner['lck'] + s.winner['attr_39']) * random.randrange(int(2400))
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>神魔法ファイナル・ブレイカー！！！</FONT><br>"

    def watowaza(s):
        pass

# ==========================================
# === FOLDER: MONS ===
# ==========================================

class mons_0:
    def mons_waza(s):
        pass
    def mons_atowaza(s):
        pass

class mons_1:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmg1 = int(s.dmg1 * 0.1)
            s.com2 += "<font class='yellow'>防御魔法マイティガード！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_2:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.hpplus2 = random.randrange(int(s.mhp)) * 2
            s.kaihuku2 += "s.mname のＨＰが s.hpplus2 回復した！♪"
            s.dmg2 = 0
            s.com2 = "<font class='yellow' size='5'>白魔法ケアルガ！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_3:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmg2 += random.randrange(int(s.mrand))
            s.dmg2 += s.item['armor']['def']
            s.sake1 -= 999999
            s.com2 += "<font class='red' size='5'>黒魔法ファイガ！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_4:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmg2 += random.randrange(int(s.mrand))
            s.dmg2 += s.item['armor']['def']
            s.sake1 -= 999999
            s.com2 += "<font class='blue' size='5'>黒魔法ブリザガ！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_5:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmg2 += random.randrange(int(s.mrand))
            s.dmg2 += s.item['armor']['def']
            s.sake1 -= 999999
            s.com2 += "<font class='yellow' size='5'>黒魔法サンダガ！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_6:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmhit = random.randrange(int(7))+1
            s.sake1 -= 999999
            s.dmg2 = random.randrange(int(s.mrand)) * s.dmhit
            s.dmg2 += s.item['armor']['def']
            s.com2 += "<font class='red' size='5'>古代魔法メテオ！！！</font><font color=red>s.dmhitヒット！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_7:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.dmg2 += int(s.khp / 5)
            s.com2 += "<font class='red' size='5'>重力魔法グラビガを発動！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_8:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.dmg2 += random.randrange(int(s.mrand)) * 2
            s.dmg2 += s.item['armor']['def']
            s.com2 += "<font class='red' size='5'>黒魔法クエイクを発動！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_9:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.dmg2 += random.randrange(int(s.mrand)) * 3
            s.dmg2 += s.item['armor']['def']
            s.com2 += "<font class='white' size='5'>禁断の魔法アルテマを発動！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_10:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.dmg2 += random.randrange(int(s.mrand)) * 5
            s.dmg2 += s.item['armor']['def']
            s.com2 += "<font class='blue' size='5'>青魔法ショック・ウェーブ・パルサーを発動！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_11:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            if (random.randrange(int(3))==0):
                s.sake1 -= 999999
                s.dmg2 = s.khp
                s.dmg2 += s.item['armor']['def']
                s.com2 += "<font class='red' size='5'>時空魔法デジョンを発動！！！</font><br>"
            else:
                s.com2 += "<font class='red' size='5'>時空魔法デジョンを発動！！！失敗！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_12:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.dmg2 += random.randrange(int(s.mrand))
            s.dmg2 += s.item['armor']['def']
            s.com2 += "<font class='red' size='5'>ファイア・ブレス！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_13:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            if (random.randrange(int(1))==0):
                s.hpplus2 = random.randrange(int(s.mrand)) * 2
                s.kaihuku2 += "s.mname のＨＰが s.hpplus2 回復した！♪"
                s.com2 = "<font class='yellow' size='5'>白魔法ケアルガ！！！</font><br>"
            else:
                s.sake1 -= 999999
                s.dmg2 += random.randrange(int(s.mrand)) * 3
                s.dmg2 += s.item['armor']['def']
                s.com2 += "<font class='white' size='5'>禁断の魔法アルテマを発動！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_14:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.tgold = random.randrange(int(s.chara['gold'] /7))
            s.gold -= s.tgold
            s.com2 += "<font class='red'>お金を盗まれた！！s.tgoldＧマイナス！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_15:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmg2 += random.randrange(int(s.mrand))
            s.dmg2 += s.item['armor']['def']
            s.hpplus2 = s.dmg2
            s.sake1 -= 999999
            s.com2 += "<font class='dark' size='4'>暗黒魔法ドレイン！！！</font><br>"
            s.kaihuku2 += "s.mname のＨＰが s.hpplus2 回復した！♪"

    def mons_atowaza(s):
        pass

class mons_16:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.dmg2 += random.randrange(int(s.mrand)) * 7
            s.dmg2 += s.item['armor']['def']
            s.sake1 -= 999999
            s.com2 += "<font class='white' size='5'>最強魔法アポガリプス！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_17:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            if (random.randrange(int(1199)) == 0):
                s.sake1 -=999999
                s.dmg1 = 0
                s.dmg2 += random.randrange(int(s.mrand)) ** 8
                s.com2 = "<font class='red' size =6>えりりんの甘いささやき！</font><br>"
            else:
                s.hpplus1 = random.randrange(int(s.msp)) * 8
                s.kaihuku2 += "s.chara['name'] のＨＰが s.hpplus1 回復した！♪"
                s.dmg1 = 0
                s.dmg2 = 0
                s.com2 = "<font class='yellow' size='5'>祝福のキス♪♪</font><br>"

    def mons_atowaza(s):
        pass

class mons_18:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.dmg2 += random.randrange(int(s.mrand))*3
            s.dmg2 += s.item['armor']['def']*3
            s.com2 += "<font class='red' size='5'>メガ・フレア！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_19:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            if (random.randrange(int(5))==0):
                s.hpplus2 = random.randrange(int(s.mrand)) * 4
                s.kaihuku2 += "s.mname のＨＰが s.hpplus2 回復した！♪"
                s.com2 = "<font class='yellow' size='5'>ハァハァ。。。</font><br>"
            else:
                s.dmg2 += random.randrange(int(s.mrand)) * 5
                s.dmg2 += s.item['armor']['def']
                s.sake1 -= 999999
                s.com2 += "<font class='white' size='5'>ハァハァ。。。</font><br>"

    def mons_atowaza(s):
        pass

class mons_20:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            if (random.randrange(int(2))==0):
                s.sake1 -= 999999
                s.dmg2 = s.khp + s.chara['max_hp']
                s.com2 += "<font class='red' size='5'>斬・鉄・剣！！！</font><font color =#cc6633 size = 5><br>「私に斬れぬものなどない」</font><br>"
            else:
                s.dmg2 += random.randrange(int(s.mrand)) * 10
                s.dmg2 += s.item['armor']['def']
                s.com2 += "<font class='red' size='5'>斬・鉄・剣！！！</font><br>"

    def mons_atowaza(s):
        pass

class mons_21:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            s.sake1 -= 999999
            s.ksex = random.randrange(int(2))
            if (s.ksex == 1):
                s.seibetu = "男"
            elif (s.ksex == 0):
                s.seibetu = "女"
            s.com2 += "<font class='red' size='5'>性転換！！！</font><font color =#cc6633 size = 2><br>性別がランダムに変化する！s.seibetuになった！</font><br>"

    def mons_atowaza(s):
        pass

class mons_22:
    def mons_waza(s):
        if (s.mons_ritu > random.randrange(int(100))):
            if (random.randrange(int(2))==0):
                s.charadown[7] = random.randrange(int(3))
                s.charadown[8] = random.randrange(int(3))
                s.charadown[9] = random.randrange(int(3))
                s.charadown[10] = random.randrange(int(3))
                s.charadown[11] = random.randrange(int(3))
                s.charadown[12] = random.randrange(int(3))
                s.charadown[13] = random.randrange(int(3))
                s.charadown[20] = random.randrange(int(3))
                s.chara['str'] -= s.charadown[7]
                s.chara['int'] -= s.charadown[8]
                s.chara['dex'] -= s.charadown[9]
                s.chara['vit'] -= s.charadown[10]
                s.chara['agi'] -= s.charadown[11]
                s.chara['mnd'] -= s.charadown[12]
                s.chara['lck'] -= s.charadown[13]
                s.chara['lp'] -= s.charadown[20]
                s.sake1 -= 999999
                s.dmg2 += random.randrange(int(s.mrand)) * 2
                s.com2 += f"""<font class='red' size='5'>臭い息！！！</font><br>
<font class ="white" size = 2>
力が<font class ="yellow">{s.charadown[7]}</font>下がった。<br>
魔力が<font class ="yellow">{s.charadown[8]}</font>下がった。<br>
信仰心が<font class ="yellow">{s.charadown[9]}</font>下がった。<br>
生命力が<font class ="yellow">{s.charadown[10]}</font>下がった。<br>
器用さが<font class ="yellow">{s.charadown[11]}</font>下がった。<br>
速さが<font class ="yellow">{s.charadown[12]}</font>下がった。<br>
魅力が<font class ="yellow">{s.charadown[13]}</font>下がった。<br>
カルマが<font class ="yellow">{s.charadown[20]}</font>下がった。
</font><br>"""
            else:
                s.dmg2 += random.randrange(int(s.mrand)) * 10
                s.dmg2 += s.item['armor']['def']
                s.com2 += "<font class='red' size='5'>臭い息！！！</font><br>"

    def mons_atowaza(s):
        pass

# ==========================================
# === FOLDER: ACSTECH ===
# ==========================================

class acstech_0:
    def acskouka(s):
        pass

class acstech_1:
    def acskouka(s):
        s.hpplus1 += int(s.chara['lp'] * (random.random() * 10))
        s.com1 += "<font class='white' size='5'>s.item['accessory']['name']が光を放つ！！s.chara['name'] のＨＰが s.hpplus1 回復♪</font><br>"


class acstech_2:
    def acskouka(s):
        s.hpplus1 += int(s.chara['lp'] * (random.random() * 50))
        s.com1 += "<font class='white' size='5'>s.item['accessory']['name']が光を放つ！！s.chara['name'] のＨＰが s.hpplus1 回復♪</font><br>"


class acstech_3:
    def acskouka(s):
        s.hpplus1 += int(s.chara['lp'] * (random.random() * 200))
        s.com1 += "<font class='white' size='5'>s.item['accessory']['name']が光を放つ！！s.chara['name'] のＨＰが s.hpplus1 回復♪</font><br>"


class acstech_4:
    def acskouka(s):
        s.dmg2 = s.dmg2 - int(dmg2 / 8)


class acstech_5:
    def acskouka(s):
        s.dmg2 = s.dmg2 - int(dmg2 / 4)


class acstech_6:
    def acskouka(s):
        s.dmg2 = s.dmg2 - int(dmg2 / 2)


class acstech_7:
    def acskouka(s):
        s.dmg1 += int(s.dmg1 / 2)


class acstech_8:
    def acskouka(s):
        s.dmg1 += s.dmg1


class acstech_9:
    def acskouka(s):
        s.dmg1 += s.dmg1 * 2


class acstech_10:
    def acskouka(s):
        if (random.randrange(int(5))==0):
            s.item['weapon']['dmg'] = s.item['weapon']['dmg'] * 2
            s.com1 += "<font class='white' size='5'>s.item['accessory']['name']が光を放つ！！オーラの効果！！！（武器攻撃力２倍効果持続）</font><br>"


class acstech_11:
    def acskouka(s):
        if (random.randrange(int(5))==0):
            s.hpplus1 = s.chara['dex'] * random.randrange(int(s.chara['lp']))
            s.com1 += "<font class='white' size='5'>s.item['accessory']['name']が光を放つ！！ケアルガの効果！！s.chara['name'] のＨＰが s.hpplus1 回復した！♪</font><br>"


class acstech_12:
    def acskouka(s):
        if (random.randrange(int(5))==0):
            s.sake2 -= 999999
            s.dmg1 += s.chara['dex'] * random.randrange(int(80))
            s.com1 += "<font class='white' size='3'>s.item['accessory']['name']が光を放つ！！ホーリーの効果！！</font><br>"


class acstech_13:
    def acskouka(s):
        if (random.randrange(int(5))==0):
            s.sake2 -= 999999
            s.dmg1 += s.chara['int'] * random.randrange(int(80))
            s.com1 += "<font class='red' size='3'>s.item['accessory']['name']が光を放つ！！メテオの効果！！</font><br>"


class acstech_14:
    def acskouka(s):
        if (random.randrange(int(5))==0):
            s.sake2 -= 999999
            s.dmg1 += (s.chara['int'] + s.chara['dex']) * random.randrange(int(100))
            s.com1 += "<font class='white' size='3'>s.item['accessory']['name']が光を放つ！！アルテマの効果！！</font><br>"


class acstech_15:
    def acskouka(s):
        if (random.randrange(int(10))==0):
            s.com1 += "<font class='dark' size='3'>s.item['accessory']['name']が光を放つ！！デジョンの効果！！</font><br>"
            if (random.randrange(int(3)) == 0):
                s.sake2 -= 999999
                s.dmg1 = s.winner['max_hp'] + s.mhp_flg
                s.com1 += "<font class='yellow' size='5'>時空魔法デジョン！！！</font><br>"
            else:
                s.com1 += "<font class='red' size='5'>時空魔法デジョン！！！失敗した。。</font><br>"


class acstech_16:
    def acskouka(s):
        s.dmg2 = s.dmg2 - int(dmg2 / 8)


class acstech_17:
    def acskouka(s):
        s.dmg1 += int(s.dmg1 / 2)


class acstech_18:
    def acskouka(s):
        s.dmg2 = s.dmg2 - int(dmg2 / 4)


class acstech_19:
    def acskouka(s):
        pass

class acstech_20:
    def acskouka(s):
        s.dmg2 = s.dmg2 - int(dmg2 / 2)
        s.dmg1 += s.dmg1 * 2


class acstech_21:
    def acskouka(s):
        if (random.randrange(int(2))==0):
            s.sake2 -= 999999
            s.dmg1 += (s.chara['int'] + s.chara['dex']) * random.randrange(int(500))
            s.com1 += "<font class='green' size='3'>s.item['accessory']['name']が光を放つ！！時の狭間より古の魔神を呼び寄せた！！グランドクロス！！</font><br>"


class acstech_22:
    def acskouka(s):
        if (random.randrange(int(10))==0):
            if (s.khp < s.dmg2):
                if (s.a_22lmt >= 3):
                    s.com1 += "<font class='red' size='3'>s.item['accessory']['name']は光らなかった。。。</font><br>"
                else:
                    s.a_22lmt += 1
                    s.dmg1 += s.dmg2
                    s.dmg2 = 0
                    s.com1 += "<font class='white' size='3'>s.item['accessory']['name']が光を放つ！！s.winner['url'] s.mnameの攻撃を跳ね返した！！</font><br>"


class acstech_23:
    def acskouka(s):
        if (random.randrange(int(5))==0):
            if (s.khp < s.dmg2):
                if (s.a_23lmt >= 1):
                    s.com1 += "<font class='red' size='3'>s.item['accessory']['name']は光らなかった。。。</font><br>"
                else:
                    s.a_23lmt += 1
                    s.hpplus1 = s.chara['max_hp']
                    s.dmg2 = 0
                    s.com1 += "<font class='white' size='5'>s.item['accessory']['name']が光を放つ！！s.chara['name']の傷が完全に回復した！！</font><br>"


class acstech_24:
    def acskouka(s):
        if (s.winner['attr_51'] == 19):
            if (random.randrange(int(4))==0):
                s.dmg1 = s.dmg1 * 10
                s.sake2 -= 999999
                s.com1 += "<font class='green' size='3'>s.item['accessory']['name']が光を放つ！！s.winner['last_time']に封じ込めれれた力を解放！！</font><br>"


# ==========================================
# === FOLDER: WACSTECH ===
# ==========================================

class wacstech_0:
    def wacskouka(s):
        pass

class wacstech_1:
    def wacskouka(s):
        s.hpplus2 += int(s.winner['lck'] * (random.random() * 10))
        s.com2 += "<font class='yellow' size='3'>s.winner['last_time']が光を放つ！！s.winner['url'] のＨＰが s.hpplus2 回復♪</FONT><br>"


class wacstech_2:
    def wacskouka(s):
        s.hpplus2 += int(s.winner['lck'] * (random.random() * 50))
        s.com2 += "<font class='yellow' size='3'>s.winner['last_time']が光を放つ！！s.winner['url'] のＨＰが s.hpplus2 回復♪</FONT><br>"


class wacstech_3:
    def wacskouka(s):
        s.hpplus2 += int(s.winner['lck'] * (random.random() * 200))
        s.com2 += "<font class='yellow' size='3'>s.winner['last_time']が光を放つ！！s.winner['url'] のＨＰが s.hpplus2 回復♪</FONT><br>"


class wacstech_4:
    def wacskouka(s):
        s.dmg1 = s.dmg1 - int(s.dmg1 / 8)


class wacstech_5:
    def wacskouka(s):
        s.dmg1 = s.dmg1 - int(s.dmg1 / 4)


class wacstech_6:
    def wacskouka(s):
        s.dmg1 = s.dmg1 - int(s.dmg1 / 2)


class wacstech_7:
    def wacskouka(s):
        s.dmg2 += int(s.dmg2 / 2)


class wacstech_8:
    def wacskouka(s):
        s.dmg2 += s.dmg2


class wacstech_9:
    def wacskouka(s):
        s.dmg2 += s.dmg2 * 2


class wacstech_10:
    def wacskouka(s):
        if (random.randrange(int(5))==0):
            s.winner['attr_22'] = s.winner['attr_22'] * 2
            s.com2 += "<font class='yellow' size='3'>s.winner['last_time']が光を放つ！！オーラの効果！！！（武器攻撃力２倍効果持続）</FONT><br>"


class wacstech_11:
    def wacskouka(s):
        if (random.randrange(int(15))==0):
            s.hpplus2 = s.winner['int'] * random.randrange(int(s.winner['lck']))
            s.com2 += "<font class='yellow' size='3'>s.winner['last_time']が光を放つ！！ケアルガの効果！！s.winner['url'] のＨＰが s.hpplus2 回復した！♪</FONT><br>"


class wacstech_12:
    def wacskouka(s):
        if (random.randrange(int(5))==0):
            s.sake1 -= 999999
            s.dmg2 = s.winner['int'] * random.randrange(int(80))
            s.com2 += "<font class='white' size='3'>s.winner['last_time']が光を放つ！！ホーリーの効果！！</FONT><br>"


class wacstech_13:
    def wacskouka(s):
        if (random.randrange(int(5))==0):
            s.sake1 -= 999999
            s.dmg2 = s.winner['str'] * random.randrange(int(80))
            s.com2 += "<font class='red' size='3'>s.winner['last_time']が光を放つ！！メテオの効果！！</FONT><br>"


class wacstech_14:
    def wacskouka(s):
        if (random.randrange(int(5))==0):
            s.sake1 -= 999999
            s.dmg2 = (s.winner['str'] + s.winner['int']) * random.randrange(int(100))
            s.com2 += "<font class='white' size='3'>s.winner['last_time']が光を放つ！！アルテマの効果！！</FONT><br>"


class wacstech_15:
    def wacskouka(s):
        if (random.randrange(int(10))==0):
            s.com2 += "<font class='dark' size='3'>s.winner['last_time']が光を放つ！！デジョンの効果！！</FONT><br>"
            if (random.randrange(int(3)) == 0):
                s.sake1 -= 999999
                s.dmg2 = s.chara['max_hp']
                s.com2 += "<font class='yellow' size='5'>時空魔法デジョン！！！</FONT><br>"
            else:
                s.com2 += "<font class='red' size='5'>時空魔法デジョン！！！失敗した。。</FONT><br>"


class wacstech_16:
    def wacskouka(s):
        s.dmg1 = s.dmg1 - int(s.dmg1 / 8)


class wacstech_17:
    def wacskouka(s):
        s.dmg2 += int(s.dmg2 / 2)


class wacstech_18:
    def wacskouka(s):
        s.dmg1 = s.dmg1 - int(s.dmg1 / 2)
        s.dmg2 += s.dmg2


class wacstech_19:
    def wacskouka(s):
        pass

class wacstech_20:
    def wacskouka(s):
        s.dmg1 = s.dmg1 - int(s.dmg1 / 2)
        s.dmg2 += s.dmg2 * 2


class wacstech_21:
    def wacskouka(s):
        if (random.randrange(int(2))==0):
            s.sake1 -= 999999
            s.dmg2 += (s.winner['str'] + s.winner['int']) * random.randrange(int(500))
            s.com2 += "<font class='green' size='3'>s.winner['last_time']が光を放つ！！時の狭間より古の魔神を呼び寄せた！！グランドクロス！！</FONT><br>"


class wacstech_22:
    def wacskouka(s):
        if (random.randrange(int(30))==1):
            if (s.khp < s.dmg1):
                if (s.wa_22lmt >= 3):
                    s.winner['attr_51'] == 0
                    s.com2 += "<font class='green' size='3'>s.winner['last_time']は光らなかった。。。</FONT><br>"
                else:
                    s.wa_22lmt += 1
                    s.dmg2 += s.dmg1
                    s.dmg1 = 0
                    s.com2 += "<font class='white' size='3'>s.winner['last_time']が光を放つ！！s.chara['name']の攻撃を跳ね返した！！</FONT><br>"


class wacstech_23:
    def wacskouka(s):
        if (s.khp < s.dmg1):
            s.com2 += "<font class='green' size='3'>s.winner['last_time']は光らなかった。。。</FONT><br>"


class wacstech_24:
    def wacskouka(s):
        if (s.item['accessory']['effect_id'] == 19):
            if (random.randrange(int(5))==0):
                s.dmg2 = s.dmg2 * 10
                s.sake1 -= 999999
                s.com2 += "<font class='green' size='3'>s.winner['last_time']が光を放つ！！s.item['accessory']['name']に封じ込めれれた力を解放！！</FONT><br>"



def run_skill(folder, skill_id, method, state):
    """
    指定されたフォルダ・IDのスキルメソッドを実行します。
    例: run_skill("tech", 1, "hissatu", battle_state)
    """
    class_name = f"{folder}_{skill_id}"
    cls = globals().get(class_name)
    if cls and hasattr(cls, method):
        func = getattr(cls, method)
        try:
            func(state)
        except Exception as e:
            state.com1 += f"<small class=red>[効果発動エラー: {class_name}.{method}: {e}]</small><br>"

