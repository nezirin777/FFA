#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権は下記の3人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
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
#　http://www3.big.or.jp/~icu/
#　icus2@hotmail.com
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#     http://www3.big.or.jp/~icu/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

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

	$back_form = << "EOM";
<br>
<form action="$scriptst" method="post">
<input type=hidden name=id value="$in{'id'}">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type=submit class=btn value="戻る">
</form>
EOM

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {
		&error("アクセスできません！！");
	}
}

if ($mode) { &$mode; }
&chara_st;
exit;

#----------------#
#  ログイン画面  #
#----------------#
sub chara_st {

	&chara_load;

	&chara_check;

	&item_load;

	# 能力値バーの詳しい幅設定
	$hit_ritu = int(($chara[11] / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($chara[12]/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($chara[20] / 15)) + 10 + $chara[33];
	if($waza_ritu > 75){$waza_ritu = 75;}
	$ci_plus = $item[2] + $item[16];
	$cd_plus = $item[5] + $item[18];

	open(IN,"$tac_file");
	@gettac = <IN>;
	close(IN);

	$thit = 0;
	foreach (@gettac) {
		($tacno,$tacname) = split(/<>/);
		if ($chara[30] == $tacno) {
			$ktac_name = $tacname;
			$thit = 1;
			last;
		}
	}

	if (!$thit) { $ktac_name = "普通に戦う"; }

	&class;

	if($chara[5]) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $chara[18] * $lv_up;

        if(!$chara[32]){$chara[32] = 0;}
	$syou = @shogo[$chara[32]];

	&syoku_load;

	&header;

       print <<"EOM";
<table align="center">
<TR>
<TD><font size=5>$chara[4]さん用ステータス変更画面</font></TD>
</TR>
</table>
<hr size=0>
<font class=white>メニュー/</font>
<a href="$scripta?mode=ranking">登録者一覧</a> / 
<a href="$ranking">\能\力別ランキングへ</a> / 
<a href="$syoku_html" target="_blank">各職業に必要な特性値</a> / 
<a href="$img_all_list" target="_blank">$vote_gazou</a> / 
<a href="$bbs" target="_blank">$bbs_title</a> / 
<a href="$helptext" target="_blank">$helptext_url</a>
<br>
<font class=white>町の外れ/</font>
<a href="$sbbs" target="_blank">$sbbs_title</a> / 
<a href="$vote" target="_blank">$vote_title</a> / 
<br>
<form action="$scripts" method="post">
<table border=0 align="center" width='100%'>
<tr>
<td valign=top width='50%'>
<table width="100%"><tr>
<tr><td id="td1" colspan="5" class="b2" align="center">キャラクターデータ</td></tr>
<td rowspan="4" align="center" valign=bottom class="b2"><img src="$img_path/$chara_img[$chara[6]]">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$item[0]</td>
<td id="td2" class="b1">攻撃力</td><td align="right" class="b2">$item[1]</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$item[3]</td>
<td id="td2" class="b1">防御力</td><td align="right" class="b2">$item[4]</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$item[6]</td>
	
<td id="td2" class="b2">称号</td><td align="center" class="b2"><font color=yellow>$syou</font></td></tr>
</table>
<table width="100%">
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr><td class="b1" id="td2">ジョブ</td>
<td class="b2">
$chara_syoku[$chara[14]]
</td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$chara[33]</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$chara[18]</td>
<td class="b1" id="td2">経験値</td><td class="b2">$chara[17]/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$chara[15]\/$chara[16]</td>
<td class="b1" id="td2">お金</td><td class="b2">$chara[19]\/$gold_max</td></tr>
</table>

<table width="100%"><tr><td id="td2" align="center" class="b1">今までのジョブ</td></tr>
<tr><td colspan=3 align="center" class="b1">
<table width="100%">
<tr>
EOM
	$s = 0;
	foreach (@syoku_master){
		if ($_) {
			$class_flg = int($syoku_master[$s]/10);
			$class[$s] = $class_mark[$class_flg];
			print "<td class=\"b2\" width=\"20%\" align=\"center\">$chara_syoku[$s]<br>$class[$s]</td>";
		}
		$s++;
		if ($s % 5 == 0) {
			print '</tr><tr>';
		}
	}

	if (!$s) {
		print "<td class=\"b2\" width=\"100%\" align = \"center\">なし</td>";
	}

       print <<"EOM";
</tr></table></td></tr></table>
<table width="100%"></form>
<tr><td id="td1" colspan="5" class="b2" align="center">その他のコマンド</td></tr><tr><td id="td2"align="center" class="b2">【戦術変更】</td>
<form action="$scripts" method="post">
<td align="center"colspan="4" class="b2">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=submit class=btn value="戦術を変更"></td>
</form>
</tr>
<tr><td id="td2"align="center" class="b2">【ステータス画面へ】</td>
<form action="$script" method="post">
<td align="center"colspan="4" class="b2">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=submit class=btn value="ステータス画面へ"></td>
</form>
</tr>
<tr><td id="td2"align="center" class="b2">【パスワード変更】</td>
<form action="$script_pass" method="post">
<td align="center"colspan="4" class="b2">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=submit class=btn value="パスワード変更"></td>
</form>
</tr></table>
<td valign="top">
<table width='100%'>
<form action="$scriptst" method="post">
<tr><td id="td1" colspan="5" class="b2" align="center">ホームページデータ</td></tr>
<tr><td id="td2" class="b1">ホームページ名</td></tr><tr><td colspan="4"><input type="text" name=site value="$chara[2]" size=50></td></tr>
<tr><td id="td2" class="b1">ホームページのURL</td></tr><tr><td colspan="4"><input type="text" name=url value="$chara[3]" size=60></td></tr>
</table>
<table width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr>
<td class="b1" id="td2">画像設定</td>
<td class="b2"colspan="4">
<input type="text" name="chara" value="$chara[6]" size=5>
<a href="$img_all_list" target="_blank">
$vote_gazou</a>
</td>
</tr></td>
<tr>
<td class="b1" id="td2">なまえ</td><td class="b2">$chara[4]</td>
<td class="b1" id="td2">性別</td><td class="b2">$esex</td></tr>
<tr><td class="b1" id="td2">ジョブ</td><td class="b2">$chara_syoku[$chara[14]]</td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$chara[33]</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$chara[18]</td>
<td class="b1" id="td2">経験値</td><td class="b2">$chara[17]/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$chara[15]\/$chara[16]</td>
<td class="b1" id="td2">お金</td><td class="b2">$chara[19]\/$gold_max</td></tr>
<tr><td class="b1" id="td2">力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$chara[7] + $item[8]</b></td>
<td class="b1" id="td2">魔力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$chara[8] + $item[9]</b></td></tr>
<tr><td class="b1" id="td2">信仰心</td><td align="left" class="b2"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$chara[9] + $item[10]</b></td>
<td class="b1" id="td2">生命力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$chara[10] + $item[11]</b></td></tr>
<tr><td class="b1" id="td2">器用さ</td><td align="left" class="b2"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$chara[11] + $item[12]</b></td>
<td class="b1" id="td2">速さ</td><td align="left" class="b2"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$chara[12] + $item[13]</b></td></tr>
<tr><td class="b1" id="td2">魅力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$chara[13] + $item[14]</b></td>
<td class="b1" id="td2">カルマ</td><td align="left" class="b2"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$chara[20] + $item[15]</b></td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $ci_plus%</b></td>
<td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu + $cd_plus%</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $item[17]%</b></td><td id="td2" class="b2">技名</td><td align="center" class="b2"><B>$ktac_name</B></td></tr>
<tr><td class="b1" id="td2">技発動時コメント</td><td colspan="3" align="center" class="b2"><input type="text" name=waza value="$chara[23]" size=50></td></tr>
<tr><td id="td2" class="b1">

変更したステータスを登録><td align="center" colspan=3 class="b2">
<input type=hidden name=mode value=st_buy>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=submit class=btn value="ステータスを登録する">
</td></tr>
</form>
</table>
</table></td></tr></table>
EOM

	&message_load;

	&footer;

	exit;
}

#----------------#
#  変更登録画面  #
#----------------#
sub st_buy {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	&get_host;

	if($in{'id'} eq test){
		&error("テストキャラはステータス変更はできません$back_form");
	}

	if($in{'site'} eq "") {
		$in{'site'} = 'いくのＣＧＩのＨＰ';
	}
	if($in{'url'} eq "") {
		$in{'url'} = 'http://www.eriicu.com';
	}

	if (length($in{'waza'}) > 100) {
		&error("クリティカルコメントが長すぎます！$back_form");
	}

	foreach (@ban_word) {
		if(index($in{'waza'},$_) >= 0) {
			$in{'mesname'} = $aite_data[4];
			&error("禁止語「$_」が含まれています$back_form");
		}
	}

	$chara[2] = $in{'site'};
	$chara[3] = $in{'url'};
	$chara[6] = $in{'chara'};
	$chara[23] = $in{'waza'};

	&chara_regist;
	&unlock($lock_file,'CR');

	&header;

 print <<"EOM";
<h1>$chara[4]さんのステータスを変更しました</h1><br>
<form action="$scriptst" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="ステータス変更画面へ">
</form>
EOM

	&footer;

	exit;
}
