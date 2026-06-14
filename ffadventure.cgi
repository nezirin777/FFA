#!/usr/local/bin/perl

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

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# レジストライブラリの読み込み
require 'sankasya.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $sts_back;
$midi = $sts_midi;
#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
if ($mente) {
	&error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m"); 
}
&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {
		&error("アクセスできません！！");
	}
}

&log_in;

#----------------#
#  ログイン画面  #
#----------------#
sub log_in {

	&chara_load;

	&chara_check;

	&item_load;

	&read_winner;

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$vtime = $b_time - $ltime;
	$xtime = $vtime + 1;
	$ztime = $vtime + 1;
	$mtime = $m_time - $ltime + 1;

	if($chara[28] < $boss) {
		$chara[28] = 0;
	}

	&class;

	if($chara[5]) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $chara[18] * $lv_up;

        if(!$chara[32]){$chara[32] = 0;}
	$syou = @shogo[$chara[32]];

        #宿代計算
        $yado_daix=int($yado_dai*$chara[18]);

	&header;

	&guest_list;

	&guest_view;

       print <<"EOM";
	<hr size=0>
	<font class=white>メニュー/</font><a href="$scripta?mode=ranking">登録者一覧</a> / <a href="$ranking">能\力別ランキングへ</a> / <a href="$syoku_html" target="_blank">各職業に必要な特性値</a> /<a href="$img_all_list" target="_blank">$vote_gazou</a> /<a href="$bbs" target="_blank">$bbs_title</a> /<a href="$helptext" target="_blank">$helptext_url</a><br>
<font class=white>町の外れ/</font><a href="$sbbs" target="_blank">$sbbs_title</a> / <a href="$vote" target="_blank">$vote_title</a> /<br>
<table align="center"width="100%">
<TR><td rowspan="2"  align="center" class="b2" width=70 height=60><img src="$img_path/$chara_img[$winner[5]]">
<TD id="td1" align="center" colspan=2 class="b2">現在のチャンプ<a href="$scripta?id=$winner[0]"><B>$winner[3]</B></a>さん($winner[44]連勝中)</TD></TR>
	<TR><td id="td2"align="center" class="b2">現在のHP</td><TD class="b2"align="center"><B>$winner[15]\/$winner[16]</B></TD></TR></table>
<hr size=0>

<table border=0 align="center" width='100%'>
<tr>
<td valign=top width='50%'>
EOM
if ($ztime > 0) {
       print <<"EOM";
<table><tr>
<FORM NAME="form1">
<td>
戦闘開始可能\まで残り<INPUT TYPE="text" NAME="clock" SIZE="3">秒です。(更新の目安に使って下さい)
</td>
</FORM>
</tr></table>
EOM
}
       print <<"EOM";
<table width="100%">
<tr><td id="td1" colspan="5" class="b2" align="center">キャラクターデータ</td></tr>
<td rowspan="4" align="center" valign=bottom class="b2"><img src="$img_path/$chara_img[$chara[6]]">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$item[0]</td>
<td id="td2" class="b1">攻撃力</td><td align="right" class="b2">$item[1]</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$item[3]</td>
<td id="td2" class="b1">防御力</td><td align="right" class="b2">$item[4]</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$item[6]</td>
	
<td id="td2" class="b2">称号</td><td align="center" class="b2"><font color=yellow>$syou</font></td></tr>
</table>

<table width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr><td class="b1" id="td2">ジョブ</td><td class="b2">$chara_syoku[$chara[14]]</td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$chara[33]</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$chara[18]</td>
<td class="b1" id="td2">経験値</td><td class="b2">$chara[17]/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$chara[15]\/$chara[16]</td>
<td class="b1" id="td2">お金</td><td class="b2">$chara[19]\/$gold_max</td></tr>
<tr>
<td class="b1" id="td2">チャンピオンを目指す</td>
<form action="$scriptb" method="post">
<td colspan="3" align="center" class="b2">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
EOM
	if ($winner[0] eq $chara[0]) {
		print "現在チャンプなので闘えません\n";
	} elsif ($winner[40] eq $chara[0] and $chanp_milit == 1) {
		print "チャンプと戦った直後なので疲れて闘えません\n";
	}elsif($ltime > $b_time) {
		print "<input type=\"submit\" class=btn value=\"チャンプに挑戦\">\n";
	}else{
		print "$ztime秒後闘えるようになります。\n";
	}
	print <<"EOM";
<br>※賞金：$winner[50] G
</td></form>
</tr>
<tr>
<td class="b1" id="td2" class="b2">好きなキャラと対戦</td>
<form action="$script_select" method="post">
<td align="center" colspan="3" class="b2">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
EOM
	if(!$chara[21]) {
		print "１度チャンプに挑戦してください\n";
	} elsif($ltime > $b_time or !$chara[21]) {
		print "<input type=submit class=btn value=\"好きなキャラに挑戦\">\n";
	} else{
		print "$ztime秒後闘えるようになります。\n";
	}

	print <<"EOM";
</td></form></tr>
<tr>
<td class="b1" id="td2" class="b2">天下一武道会</td>
<form action="$script_tenka" method="post">
<td align="center" colspan="3" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
EOM
	if(!$chara[21]) {
		print "１度チャンプに挑戦してください\n";
	} elsif($ltime > $b_time or !$chara[21]) {
		print "<input type=submit class=btn value=\"天下一武道会\">\n";
	} else{
		print "$ztime秒後闘えるようになります。\n";
	}

	print <<"EOM";
</td></form></tr>
<tr>
<td class="b1" id="td2">作戦会議室</td>
<form action="$scripts" method="post">
<td colspan="3" align="center" class="b2">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=submit class=btn value="戦術の変更">
</td></form>
</tr>
</table>
</td>
EOM

# ここから右半分のテーブル
	print <<"EOM";
<td valign="top">
<table width="100%">
<tr><td id="td1" colspan="4" class="b2" align="center">街の施設</td></tr>
<tr>
<td bgcolor="#cbfffe" align="center">【旅の宿】(<b>$yado_daix</b>G)</td>
<td bgcolor="#cbfffe" align="center">【武器屋】</td>
<td bgcolor="#cbfffe" align="center">【防具屋】</td>
<td bgcolor="#cbfffe" align="center">【装飾品店】</td>
</tr>
<tr>
<form action="$scripty" method="post">
<td align="center" class="b2">
<input type=hidden name=mode value="yado">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="体力を回復"></td>
</form>
<form action="$item_shop" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="武器屋"></td>
</form>
<form action="$def_shop" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="防具屋"></td>
</form>
<form action="$acs_shop" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="装飾品店"></td>
</form>
</tr>
<tr>
<td bgcolor="#cbfffe" align="center">【ステータスの変更】</td>
<td bgcolor="#cbfffe" align="center">【銀　行】</td>
<td bgcolor="#cbfffe" align="center">【アイテム倉庫】</td>
<td bgcolor="#cbfffe" align="center">【郵便局】</td>
</tr><tr>
<td align="center" class="b2">
<form action="$scriptst" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータスの変更">
</td>
</form>
<form action="$script_bank" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="　銀行　"></td>
</form>
<form action="$script_souko" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="アイテム倉庫"></td>
</form>
<form action="$script_post" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局">
</td>
</form>
</tr>
<tr>
<td bgcolor="#cbfffe" align="center">【転職の神殿】</td>
<td bgcolor="#cbfffe" align="center">【更地】</td>
<td bgcolor="#cbfffe" align="center">【更地】</td>
<td bgcolor="#cbfffe" align="center">【更新所】</td>
</tr><tr>
<form action="$script_tensyoku" method="post">
<td align="center" class="b2">
<input type=hidden name=mode value=tensyoku>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="submit" class="btn" value="転職の神殿">
</td>
</form>
<td align="center" class="b2">
更地
</td>
<td align="center" class="b2">
更地
</td>
<form action="$script" method="post">
<td align="center" class="b2">
<input type=hidden name=mode value=log_in>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="画面更新">
</td>
</form>
</tr>
</table>
<table width="100%">
<tr>
<td id="td1" colspan="2" class="b2" align="center">冒険に出かける</td>
</tr>
<tr><td class="b1" id="td2">
周辺の探索</td>
<form action="$scriptm" method="post">
<td align="center" class="b2">
<input type=hidden name=mode value=monster>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
EOM

	if(!$chara[21]) {
		print "１度チャンプに挑戦してください\n";
	} elsif($ltime >= $m_time or !$chara[21]) {
	print <<"EOM";
<select name="mons_file">
<option value="monster0">その辺に出かける（弱い敵が出現！）
<option value="monster1">近くの洞窟（強い敵が出現！）
<option value="monster2">ダークダンジョン（かなり強い敵が出現！）
<option value="monster3">ミシディアの塔（鬼のような敵が出現！）
</select>
<input type=submit class=btn value="モンスターと闘う">
EOM
	}else{
		print "$mtime秒後闘えるようになります。<br>\n";
	}

	print <<"EOM";
</td>
</form>
</tr><tr><td colspan=2>※修行の旅にいけます。</td></tr>
EOM

	if($chara[27]%5 == 0){
	print <<"EOM";
<tr><td class="b1" id="td2">突然の出現</td>
<form action=\"$scriptm\" method=\"post\">
<td align=\"center\" class=\"b2\">
<input type=hidden name=mode value=genei>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
EOM
	if (!$chara[21]) {
		print "１度チャンプに挑戦してください\n";
	} elsif($ltime >= $m_time or !$chara[21]) {
	print "<input type=submit class=btn value=\"幻影の城へ\">\n";
	} else {
		print "$mtime秒後行けるようになります。<br>\n";
	}

	print <<"EOM";
</td>
</form>
</tr><tr><td colspan=2>
※財宝が眠ると言われる「幻影の城」にいけます。
</td></tr>
EOM
}

	print <<"EOM";
<tr>
<td class="b1" id="td2">
レジェンドプレイス</td>
<form action="$script_legend" method="post">
<td align="center" class="b2">
<input type=hidden name=mode value=boss>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
EOM
	if (!$chara[21] || $chara[28] != $boss) {
		print "１度チャンプに挑戦してください\n";
	} elsif ($ltime >= $m_time or !$chara[21]) {
		print <<"EOM";
<select name="boss_file">
<option value="0">うわさのほこら（初心者を口を開けて・・）
EOM
		if ($chara[32] > 0) {
			print "<option value=\"1\">古の神殿（熟練者も命を落とすという・・）\n";
		}
		if ($chara[32] > 1) {
			print "<option value=\"2\">勇者の洞窟（伝説の勇者が訪れたという・・）\n";
		}
		if ($chara[32] > 2) {
			print "<option value=\"3\">ガイアフォース（神のみが入ることを許されている・・）\n";
		}
print <<"EOM";
</select>
<input type=submit class=btn value="伝説に挑む">
EOM
	}else{
		print "$mtime秒後闘えるようになります。<br>\n";
	}

	print <<"EOM";
</td>
</form>
</tr><tr><td colspan=2>
※でんせつの場所へ訪れることができます。</td></tr>
<tr>
<td class="b1" id="td2">異世界</td>
<form action="$scriptm" method="post">
<td align="center" class="b2">
<input type=hidden name=mode value=isekiai>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
EOM
	if (!$chara[21]) {
		print "１度チャンプに挑戦してください\n";
	} elsif ($ltime >= $m_time or !$chara[21]) {
		if ($chara[18] < $isekai_lvl) {
			print "レベルが$isekai_lvlを超えるまで行けません。<br>\n";
		} else {
			print "<input type=submit class=btn value=\"異世界へ行く\"><br>\n";
		}
	} else {
			print "$mtime秒後闘えるようになります。<br>\n";
	}

	print <<"EOM";
</td></form></tr>
<tr><td colspan=2>※神々の領域と言われるこの世界に足をふみいれて、無事に帰ったものは誰一人いない・・・</td></tr>
</table></td></tr></table>
EOM

	&message_load;

	&footer;

	exit;
}
