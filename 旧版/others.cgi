#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はT.CUMROさんにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FFA Emilia Ver1.01
#  edit by Emilia
#  http://www5d.biglobe.ne.jp/~sprite/
#  y-kamata@jcom.home.ne.jp
#------------------------------------------------------#
#
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
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイルの初期設定
$midi = $title_midi;
$backgif = $backgif;

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

if($link_flg){
	&link_chack;
}

&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {
		&error("アクセスできません！！");
	}
}

&html_top;

#-----------------#
#  TOPページ表示  #
#-----------------#
sub html_top {

	# チャンプデータ読込
	&read_winner;

	# クッキー取得
	&get_cookie;

	# チャンプクラス表示
	$class_flg = int($winner[39]/10);

	@class_mark = (
		'■□□□□□　　<i><b>(Beginner)</b></i>'
		,'■■□□□□　　<i><b>(Charanger)</b></i>'
		,'■■■□□□　　<i><b>(Low Class)</b></i>'
		,'■■■■□□　　<i><b>(Normal Class)</b></i>'
		,'■■■■■□　　<i><b>(High Class)</b></i>'
		,'■■■■■■　　<i><b>(Top Class)</b></i>'
		,'★★★★★★　　<i><b>(Master)</b></i>'
	);

	$class = $class_mark[$class_flg];


	# 勝率計算
	if($winner[18]) {
		$ritu = int(($winner[19] / $winner[18]) * 100);
	}
	else {
		$ritu = 0;
	}

	# チャンプ性別取得
	if($winner[4]) {
		$esex = "男";
	} else {
		$esex = "女";
	}

	# チャンプ基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int(($winner[10] / 10)+51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($winner[11] / 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($winner[13] / 15)) + 10 + $winner[39];
	if($waza_ritu > 75){$waza_ritu = 75;}

	# 能力値バーの詳しい幅設定
	$bw0     = int(1 * ($winner[6] / $divpm));
	$bw1     = int(1 * ($winner[7] / $divpm));
	$bw2     = int(1 * ($winner[8] / $divpm));
	$bw3     = int(1 * ($winner[9] / $divpm));
	$bw4     = int(1 * ($winner[10] / $divpm));
	$bw5     = int(1 * ($winner[11] / $divpm));
	$bw6     = int(1 * ($winner[12] / $divpm));
	$bwlp    = int(1 * ($winner[13] / $divpm));
	$winner[23] += $a_hitup;
	$winner[26] += $a_kaihiup;
	$bwhit   = int(0.5 * ($hit_ritu + $winner[23]));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $winner[26]));
	$bwwaza  = int(1 * ($waza_ritu + $winner[35]));
	if($bwhit > 100){$bwhit = 100;}
	if($bwkaihi > 100){$bwkaihi = 100;}
	if($bwwaza > 100){$bwwaza = 100;}

	$date = time();

	# ヘッダー表示
	&header;

	# HTMLの表示
	print <<"EOM";
<table border=0>
<tr>
<td valign="top">
<table border=1>
<tr><td id="td2" align=center colspan=5 class=b2>
<font class="$white">前回の続き</font></td></tr>
<tr><td class=b1>I D</td>
<form action="$loginscript" method="POST">
<input type="hidden" name="mode" value="log_in">
<td><input type="text" size="10" name="id" value="$c_id"></td>
<td class=b1>パスワード</td>
<td><input type="password" size="10" name="pass" value="$c_pass"></td>
<td><input type="submit" class="btn" value="ログイン"></td>
</form>
</tr>
</table>
</td><td>
EOM
	open(IN,"./charalog/test.cgi");
	@testdata = <IN>;
	close(IN);
if ($testdata[27] + 600 < $date) {
	print <<"EOM";
<table border=1>
<tr><td id="td2" align=center colspan=5 class=b2>
<font class="$white">テストプレイ</font></td></tr>
<tr>
<form action="$loginscript" method="POST">
<td>
<input type="hidden" name="mode" value="log_in">
<input type=hidden name="id" value=test>
<input type=hidden name="pass" value=test>
<input type="submit" class="btn" value="テストプレイ"></td>
</form>
</tr></table>
EOM
} else {
print "現在使用中です<br>お待ち下さい";
}
	print <<"EOM";
</td><td>
<table border=1>
<tr><td id="td2" align=center colspan=5 class=b2>
<font class="$white">新規キャラ作成</font></td></tr>
<tr>
<FORM ACTION="$chara_make" METHOD="POST">
<INPUT TYPE="hidden" NAME="mode" VALUE="chara_make">
<td><input type="submit" class="btn" value="新規キャラクタ作成"></td>
</form>
</tr></table>
</td></tr></table>
<table border=0 width='90%'>
<tr><td align="center" talign="center" class="b1">
<MARQUEE>$telop_message</MARQUEE></td>
</tr></table>
EOM

	# 冒険者数表示
	open(GUEST,"$guestfile");
	@member=<GUEST>;
	close(GUEST);

	$num = 0;
	$blist = '';
	foreach (@member) {
		($ntimer,$nname,$nid) = split(/<>/);
		if($date - $ntimer < $sanka_time){
			$blist .= "<a href=\"$scripta?mode=chara_sts&id=$nid\">$nname</a><font size=1 color=#ffff00>★</font>";
			$num++;
		}
	}


	print "<font size=2 color=#aaaaff>現在の冒険者(<B>$num人</B>)：</font>\n";

	if ($blist) {
		print $blist;
	}
	else {
		print '誰もいません';
	}

	print <<"EOM";
<br>現在の連勝記録は、$winner[47]さんの「<A HREF=\"$winner[49]\" TARGET=\"_blank\"><FONT SIZE=\"3\" COLOR=\"#6666BB\">$winner[48]</FONT></A>」、$winner[45]連勝です。新記録を出したサイト名の横には、<IMG SRC="$mark">マークがつきます。
<table border=0 width='100%'>
<tr>
<td width="500" valign="top">
	<table border=1 width="100%">
	<tr>
	<td id="td1" colspan=5 align="center" class="b2">現在のチャンプ<font class="white">$winner[44]連勝中</font><br><font class = "yellow">(<a href=$scripta?mode=chara_sts&id=$winner[40]>$winner[41]</a><font class = "yellow">に勝利！！\[サイト\]</font><A HREF=\"$winner[43]" TARGET="_blank">$winner[42]</A> )</font></td>
	</tr>
	<tr>
	<td id="td2" align="center" class="b1">ホームページ</td>
	<td colspan="4"><a href="$winner[2]"><b>$winner[1]</b></a>
EOM
	if($winner[49] eq $winner[2]) {
		print "<IMG SRC=\"$mark\" border=0>\n";
	}

	$kyouyuu="";
	$index=0;
	foreach (@site_url) {
		$kyouyuu.="<a href=\"$_\">$site_title[$index]</a>/";
		$index++;
		}

	print <<"EOM";
</td></tr><tr>
<td align="center" rowspan="11" valign=bottom><img src="$img_path/$chara_img[$winner[5]]"><font color=$white>$winner[18]</font>戦<font color=$white>$winner[19]</font>勝中<br>勝率：$ritu\%<br>
<table width="100%" border=1>
<tr><td id="td2" class="b2">武器</td><td align="center" class="b2">$winner[21]</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="center" class="b2">$winner[24]</td></tr>
<tr><td id="td2" class="b2">飾り</td><td align="center" class="b2">$winner[27]</td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $winner[23] %</b></td></tr>
<tr><td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu + $winner[26] %</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $winner[35]%</b></td><td></td></tr>
</table></td><tr>
<td id="td2" align="center" class="b1">なまえ</td><td class="b2"><b>$winner[3]</b></td>
<td id="td2" align="center" class="b1">性別</td><td class="b2"><b>$esex</b></td></tr>
<tr><td id="td2" align="center" class="b1">ジョブ</td><td class="b2"><b>$chara_syoku[$winner[14]]</b></td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$winner[39]</b></td></tr>
<tr><td id="td2" align="center" class="b1">クラス</td><td colspan=3 class="b2"><b>$class</b></td></tr>
<tr><td id="td2" align="center" class="b1">レベル</td><td class="b2"><b>$winner[17]</b></td>
<td id="td2" align="left" class="b1">-</td><td class="b2">-</td></tr>
<tr><td id="td2" align="left" class="b1">HP</td><td class="b2"><b>$winner[15]\/$winner[16]</b></td>
<td id="td2" align="left" class="b1">賞金</td><td class="b2"><b>$winner[50]</b></td></tr>
<tr><td id="td2" align="left" class="b1">力</td><td class="b2"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$winner[6] + $winner[28]</b></td>
<td id="td2" align="left" class="b1">魔力</td><td class="b2"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$winner[7] + $winner[29]</b></td></tr>
<tr><td id="td2" align="left" class="b1">信仰心</td><td class="b2"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$winner[8] + $winner[30]</b></td>
<td id="td2" align="left" class="b1">生命力</td><td class="b2"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$winner[9] + $winner[31]</b></td>	</tr>
<tr><td id="td2" align="left" class="b1">器用さ</td><td class="b2"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$winner[10] + $winner[32]</b></td>
<td id="td2" align="left" class="b1">速さ</td><td class="b2"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$winner[11] + $winner[33]</b></td></tr>
<tr><td id="td2" align="left" class="b1">魅力</td><td class="b2"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$winner[12]</b></td>
<td id="td2" align="left" class="b1">カルマ</td><td class="b2"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$winner[13] + $winner[34]</b></td></tr>
</table>
</td>
<td valign="top">
<td valign="top" align="left">
[<B><FONT COLOR=$yellow>$main_title の遊び方</FONT></B>]
<OL>
<LI>まず、「新規キャラクター登録」ボタンを押して、キャラクターを作成します。
<LI>キャラクターの作成が完了したら、このページの左上にあるところからログインして、あなた専用のステータス画面に入ります。
<LI>そこであなたの行動を選択することができます。
<LI>一度キャラクターを作成したら、右上のところからログインして遊びます。新規にキャラクターを作れるのは、一人に一つのキャラクターのみです。
<LI>これは、HPバトラーではなく、キャラバトラーです。キャラクターを育てていくゲームです。
<LI>能\力を振り分けることができキャラクターの能\力をご自分で決めることができます。(ここで決めた能\力はごくまれにしか上昇しないので、慎重に)
<LI><b>$limit日</b>以上闘わなければ、キャラクターのデータが削除されます。
<LI>一度戦闘すると<b>$b_time</b>秒経過しないと再び戦闘できません。
</OL>
</td>
</tr>
</table>
<hr size=0>
<font color=$white>共有設置者/<a href="$homepage" TARGET="_top">$home_title</a> / $kyouyuu<br>
<font color=$white>メニュー/</font><a href="$scripta?mode=ranking">登録者一覧</a> / <a href="$ranking">\能\力別ランキングへ</a> / <a href="$syoku_html" target="_blank">各職業に必要な特性値</a> /<a href="$img_all_list" target="_blank">$vote_gazou</a> /<a href="$bbs">$bbs_title</a> /<a href="$helptext" target="_blank">$helptext_url</a><br>
<font color=$white>町の外れ/</font><a href="$sbbs">$sbbs_title</a> / <a href="$vote">$vote_title</a> /<br>
<table border=0 width="100%">
<TR><TD class="b1" bgcolor="#000000" align="center"><B>連絡事項</B></font></TD></TR>
<TR><TD class="b2">$kanri_message</TD></TR></table>

<form action="$scriptk" method="POST">
<table><td><input type="password" size="10" name="pass"></td>
<td><input type="submit" class="btn" value="管理者"></td>
</tr></table></form>
EOM

	# フッター表示
	&footer;

	exit;
}
#------------------#
#  クッキーを取得  #
#------------------#
sub get_cookie {
	@pairs = split(/;/, $ENV{'HTTP_COOKIE'});
	foreach (@pairs) {
		local($key,$val) = split(/=/);
		$key =~ s/\s//g;
		$GET{$key} = $val;
	}
	@pairs = split(/,/, $GET{$ffcookie});
	foreach (@pairs) {
		local($key,$val) = split(/<>/);
		$COOK{$key} = $val;
	}
	$c_id  = $COOK{'id'};
	$c_pass = $COOK{'pass'};
}

#------------------#
#直リンクチェック  #
#------------------#
sub link_chack {
	#直リンク防止処理
	$geturl = $ENV{'HTTP_REFERER'};
	#直リンク抑止機能使用に案内するＵＲＬ
	$guid ="<H1>呼び出し元が正しくありません！！</H1>";
	if ($top_url) {
		$guid.="<a href=\"$top_url\">$top_url</a>から入りなおしてください。";
	}
	else{
		$guid.="<font color=$yellow size=4>共有サイト一覧</font>";
		$index=0;
		foreach (@site_url) {
			$guid.="<a href=\"$_\">$site_title[$index]</a>/";
			$index++;
		}
	}
	if($geturl eq ""){
		&header;
		print "<center><hr width=400><h3>ERROR !</h3>\n";
		print "<font color=$red><B>$guid</B></font>\n";
		print "<hr width=400></center>\n";
		print "</body></html>\n";
		exit;
	} 
}
