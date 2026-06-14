#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はT.CUMROさんにあります。
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
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi     #
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

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

if ($mode) { &$mode; }
&error();
exit;

#------------------#
#  ランキング出力  #
#------------------#
sub ranking {

	if (!$no_html) { &ranking_no_html; }

	$lock_file = "$lockfolder/tim.lock";
	&lock($lock_file,'TM');
	open(IN,"$all_data_time");
	@all_time = <IN>;
	close(IN);

	$hit=0;
	foreach(@all_time){
		($rankmode,$ranktime) = split(/<>/);
		if ($rankmode eq "rankinghtml") { $hit=1;last; }
	}

	$lrtime = time();
	$btime = $lrtime - $ranktime;
	$ztime = int($btime/3600);
	$ranking_make = 0;

	if ($btime > 3600*24 || !$hit) {

		$hit=0;
		@item_new=();
		foreach (@all_time) {
			($rankmode,$ranktime) = split(/<>/);
			if ($rankmode eq "rankinghtml") {
				unshift(@item_new,"rankinghtml<>$lrtime<>\n");
				$hit=1;
			} else {
				push(@item_new,"$_");
			}
		}

		if (!$hit) { unshift(@item_new,"rankinghtml<>$lrtime<>\n"); }

		open(OUT,">$all_data_time");
		print OUT @item_new;
		close(OUT);
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');

		$ranking_make = 1;

	} else {
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');
	}

	if ($ranking_make) {

		&all_data_read;

		local(@mody)=localtime($ltime);
		$mody[4]++;
		$ima = $ltime;
		$sousu = @RANKING;
		$pagenum = int($sousu/20);

		for($shtm=0;$shtm<=$pagenum;$shtm++){

			$ifr = $shtm*20;
			$ito = $shtm*20+19;
			if($ito > $sousu){ $ito=$sousu; }

			$buffer = <<"EOM";
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Pragma" content="no-cache">
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<SCRIPT Language="JavaScript" src="$html_path$java_script" type="text/javascript">
</SCRIPT>
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
  background-image : url($html_path$backgif);
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:8px;$font_name;color:$red;}
//-->
</STYLE>
<link rel="stylesheet" href="$html_path$style_sheet" type="text/css">
<title>$main_title</title></head>
<body background="$html_path$backgif" bgcolor="$bgcolor" text="$text" link="$link" vlink="$vlink" alink="$alink">
EOM
			if($midi_set){
				$buffer .= "<embed src=\"$html_path$midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
			}

			$buffer .= <<"EOM";
<h1>登録者一覧</h1><hr size=0>
<br>現在の登録者数<b>$sousu</b>人<br>
現在登録されているキャラクターの中で、レベル上位<b>$ifr</b>人目から<b>$ito</b>人目を表\示しています。<br>
<font size =3 color =red><b>ただし、更新は１日に１回しか行われません。</b></font>前回は$mody[4]月$mody[3]日$mody[2]時$mody[1]分に更新されました。<br>
※名前をクリックすると詳細情報がご覧になれます♪<br>
EOM


			for ($i=$ifr;$i<=$ito;$i++) {
				@chara = split(/<>/,$RANKING[$i]);
				if (!@chara) { next; }

				$rdate = $chara[27] + (60*60*24*$limit);
				$niti = $rdate - $ima;
				$niti = int($niti / (60*60*24));
				if ($chara[21] >= 1) {
					$rritu = int(($chara[22] / $chara[21]) * 100);
				} else {
					$chara[21] = 0;
					$rritu = 0;
				}
   
				# 基本値算出
				$divpm = int($charamaxpm / 100);
				$hit_ritu = int(($chara[11] / 10)+51);
				if($hit_ritu > 150){$hit_ritu = 150;}
				$kaihi_ritu = int(($chara[12] / 20));
				if($kaihi_ritu > 50){$kaihi_ritu = 50;}
				$waza_ritu = int(($chara[20] / 15)) + 10 + $chara[33];
				if($waza_ritu > 75){$waza_ritu = 75;}

				# 能力値バーの詳しい幅設定
				$bw0 = int(0.5 * ($chara[7] / $divpm));
				$bw1 = int(0.5 * ($chara[8] / $divpm));
				$bw2 = int(0.5 * ($chara[9] / $divpm));
				$bw3 = int(0.5 * ($chara[10] / $divpm));
				$bw4 = int(0.5 * ($chara[11] / $divpm));
				$bw5 = int(0.5 * ($chara[12] / $divpm));
				$bw6 = int(0.5 * ($chara[13] / $divpm));
				$bwlp = int(0.5 * ($chara[20] / $divpm));
				$bwhit = int(0.5 * $hit_ritu);
				$bwkaihi = int(0.5 * $kaihi_ritu);
				$bwwaza = int(1 * $waza_ritu);
				if($bwhit > 100){ $bwhit = 100; }
				if($bwkaihi > 100){ $bwkaihi = 100; }
				if($bwwaza > 100){ $bwwaza = 100; }
				$juni=$i+1;

				$rankhtml = <<"EOM";
<table><tr><td id="td1" align="center">$juni</td>
<td><table border="1"><tr>
<td rowspan="2" width="50" align=center><img src="$img_path/$chara_img[$chara[6]]"></td>
<td id="td2" align="center" width="50">サイト</td>
<td align="center" width="100"><a href=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</a></td>
<td id="td2" align="center" width="50">力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$chara[7]</b></td>
<td id="td2" align="center" width="50">魔力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$chara[8]</b></td>
<td id="td2" align="center" width="50">信仰心</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$chara[9]</b></td>
<td id="td2" align="center" width="50">生命力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$chara[10]</b></td>
<td id="td2" align="center">レベル</td>
<td align="center">$chara[18]</td>
</tr><tr>
<td id="td2" align="center" width="50">HP</td>
<td align="center" width="100">$chara[16]</td>
<td id="td2" align="center" width="50">器用さ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$chara[11]</b></td>
<td id="td2" align="center" width="50">速さ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$chara[12]</b></td>
<td id="td2" align="center" width="50">魅力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$chara[13]</b></td>
<td id="td2" align="center" width="50">カルマ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$chara[20]</b></td>
<td id="td2" align="center">勝率</td>
<td align="center">$rritu%</td>
</tr><tr>
<td width="50" align=center><a href="../$scripta?mode=chara_sts&id=$chara[0]">$chara[4]</a></td>
<td id="td2" align="center" width="50">職業</td>
<td align="center" width="100">$chara_syoku[$chara[14]]</td>
<td id="td2" align="center" width="50">命中率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu%</b></td>
<td id="td2" class="b2" width="80">回避率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu%</b></td>
<td id="td2" align="center" width="50">必殺率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu%</b></td>
<td id="td2" align="center" width="50">戦闘回数</td>
<td align="center" width="100">$chara[21]回</td>
<td id="td2" align="center">削除まで</td>
<td align="center">残$niti日</td>
</tr></table></td></tr></table>
EOM
				$buffer.="$rankhtml";
			}

			$prevfr = $ito-39;
			$prevto = $ito-20;
			$ifr += 20;
			$ito += 20;
			$pagenum = int($sousu/20)+1;

			if($ito > $sousu){
				$ito = $sousu;
				$lhit = 1;
			}

			$mae = $shtm - 1;
			$tugi = $shtm + 1;

			if ($prevfr >= 0){
				$buffer.="<br><a href=\"$mae.html\">前の 20 件</a> ／";
			}
			if (!$lhit){
				$buffer.="<a href=\"$tugi.html\">次の 20 件</a>\n";
			}

			$buffer.="<br><br><table border=0 width=100%><tr>";
			for($i=0;$i<=$pagenum-1;$i++){
				$mae = 20 * $i + 1;
				$ato = 20 * $i + 20;
				if($ato > $sousu){$ato = $sousu;}
				$buffer.="<td align=center width=10%>\[<a href=\"$i.html\">$mae位～$ato位</a>\]</td>";
				if($i%10==9){$buffer.="</tr><tr>";}
			}
			$buffer.="</tr></table>";
			$buffer.= <<"EOM";
<a href = "$html_path$scripto">$main_titleのTOPへ</a>
<HR SIZE=0 WIDTH="100%"><DIV align=right>
FFA いく改ver2.00 edit by <a href="http://www.eriicu.com" target="_top">いく</a><br>
FFA Emilia Ver1.01 remodeled by Classic(閉鎖)<br>
FF Battle De I v3.06 remodeling by <a href="http://www.mj-world.jp/" target="_blank">jun-k</a>(更新停止中)<br>
FF ADVENTURE(改) v1.040 remodeled by <a href="http://www.gun-online.com" target="_blank">ＧＵＮ</a><br>
FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) <a href="http://www5c.biglobe.ne.jp/~ma-ti/" target="_blank">現配布元(管理者ma-ti)</a><br>
</DIV></body></html>
EOM
			$buffer.="</body></html>\n";

			open(LOG,">$no_html/$shtm.html");
			print LOG $buffer;
			close(LOG);

		}
	}

        print "Location: $no_html/0.html\n\n";

	exit;
}

#------------------------------------------#
#  ランキング画面(HTML生成不可サーバー用)  #
#------------------------------------------#
sub ranking_no_html {

	&all_data_read;

	local(@mody)=localtime($ltime);
	$mody[4]++;
	$ima = $ltime;
	$sousu = @RANKING;
	$pagenum = int($sousu/20);

	$ifr = $in{'shtm'} * 20;
	$ito = $in{'shtm'}*20+19;
	if($ito > $sousu){ $ito=$sousu; }

	&header;

	print << "EOM";
<h1>登録者一覧</h1><hr size=0>
<br>現在の登録者数<b>$sousu</b>人<br>
現在登録されているキャラクターの中で、レベル上位<b>$ifr</b>人目から<b>$ito</b>人目を表\示しています。<br>
<font size =3 color =red><b>ただし、更新は１日に１回しか行われません。</b></font>前回は$mody[4]月$mody[3]日$mody[2]時$mody[1]分に更新されました。<br>
※名前をクリックすると詳細情報がご覧になれます♪<br>
EOM

	for ($i=$ifr;$i<=$ito;$i++) {
		@chara = split(/<>/,$RANKING[$i]);

		$rdate = $chara[27] + (60*60*24*$limit);
		$niti = $rdate - $ima;
		$niti = int($niti / (60*60*24));
		if ($chara[21] >= 1) {
			$rritu = int(($chara[22] / $chara[21]) * 100);
		} else {
			$chara[21] = 0;
			$rritu = 0;
		}

		# 基本値算出
		$divpm = int($charamaxpm / 100);
		$hit_ritu = int(($chara[11] / 10)+51);
		if($hit_ritu > 150){$hit_ritu = 150;}
		$kaihi_ritu = int(($chara[12] / 20));
		if($kaihi_ritu > 50){$kaihi_ritu = 50;}
		$waza_ritu = int(($chara[20] / 15)) + 10 + $chara[33];
		if($waza_ritu > 75){$waza_ritu = 75;}

		# 能力値バーの詳しい幅設定
		$bw0 = int(0.5 * ($chara[7] / $divpm));
		$bw1 = int(0.5 * ($chara[8] / $divpm));
		$bw2 = int(0.5 * ($chara[9] / $divpm));
		$bw3 = int(0.5 * ($chara[10] / $divpm));
		$bw4 = int(0.5 * ($chara[11] / $divpm));
		$bw5 = int(0.5 * ($chara[12] / $divpm));
		$bw6 = int(0.5 * ($chara[13] / $divpm));
		$bwlp = int(0.5 * ($chara[20] / $divpm));
		$bwhit = int(0.5 * $hit_ritu);
		$bwkaihi = int(0.5 * $kaihi_ritu);
		$bwwaza = int(1 * $waza_ritu);
		if($bwhit > 100){ $bwhit = 100; }
		if($bwkaihi > 100){ $bwkaihi = 100; }
		if($bwwaza > 100){ $bwwaza = 100; }
		$juni=$i+1;

		print << "EOM";
<table><tr><td id="td1" align="center">$juni</td>
<td><table border="1"><tr>
<td rowspan="2" width="50" align=center><img src="$img_path/$chara_img[$chara[6]]"></td>
<td id="td2" align="center" width="50">サイト</td>
<td align="center" width="100"><a href=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</a></td>
<td id="td2" align="center" width="50">力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$chara[7]</b></td>
<td id="td2" align="center" width="50">魔力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$chara[8]</b></td>
<td id="td2" align="center" width="50">信仰心</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$chara[9]</b></td>
<td id="td2" align="center" width="50">生命力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$chara[10]</b></td>
<td id="td2" align="center">レベル</td>
<td align="center">$chara[18]</td>
</tr><tr>
<td id="td2" align="center" width="50">HP</td>
<td align="center" width="100">$chara[16]</td>
<td id="td2" align="center" width="50">器用さ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$chara[11]</b></td>
<td id="td2" align="center" width="50">速さ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$chara[12]</b></td>
<td id="td2" align="center" width="50">魅力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$chara[13]</b></td>
<td id="td2" align="center" width="50">カルマ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$chara[20]</b></td>
<td id="td2" align="center">勝率</td>
<td align="center">$rritu%</td>
</tr><tr>
<td width="50" align=center><a href="$scripta?mode=chara_sts&id=$chara[0]">$chara[4]</a></td>
<td id="td2" align="center" width="50">職業</td>
<td align="center" width="100">$chara_syoku[$chara[14]]</td>
<td id="td2" align="center" width="50">命中率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu%</b></td>
<td id="td2" class="b2" width="80">回避率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu%</b></td>
<td id="td2" align="center" width="50">必殺率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu%</b></td>
<td id="td2" align="center" width="50">戦闘回数</td>
<td align="center" width="100">$chara[21]回</td>
<td id="td2" align="center">削除まで</td>
<td align="center">残$niti日</td>
</tr></table></td></tr></table>
EOM
	}

	$prevfr = $ito-39;
	$prevto = $ito-20;
	$ifr += 20;
	$ito += 20;
	$pagenum = int($sousu/20)+1;

	if($ito > $sousu){
		$ito = $sousu;
		$lhit = 1;
	}

	$mae = $in{'shtm'} - 1;
	$tugi = $in{'shtm'} + 1;

	if ($prevfr >= 0){
		print "<br><a href=\"$scripta?mode=ranking_no_html&shtm=$mae\">前の 20 件</a> ／";
	}
	if (!$lhit){
		print "<a href=\"$scripta?mode=ranking_no_html&shtm=$tugi\">次の 20 件</a>\n";
	}

	print "<br><br><table border=0 width=100%><tr>";
	for($i=0;$i<=$pagenum-1;$i++){
		$mae = 20 * $i + 1;
		$ato = 20 * $i + 20;
		if($ato > $sousu){$ato = $sousu;}
		print "<td align=center width=10%>\[<a href=\"$scripta?mode=ranking_no_html&shtm=$i\">$mae位～$ato位</a>\]</td>";
		if($i%10==9){print "</tr><tr>";}
	}
	print "</tr></table>";

	&footer;

	exit;
}

#----------------#
#ステータス画面  #
#----------------#
sub chara_sts {

	&chara_load;

	&class;

	&item_load;

	if ($chara[5]) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $chara[18] * $lv_up;

	# 基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int(($chara[11] / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($chara[12]/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($chara[20] / 15)) + 10 + $chara[33];
	if($waza_ritu > 75){$waza_ritu = 75;}

	# 能力値バーの詳しい幅設定
	$bw0 = int(1 * ($chara[7] / $divpm));
	$bw1 = int(1 * ($chara[8] / $divpm));
	$bw2 = int(1 * ($chara[9] / $divpm));
	$bw3 = int(1 * ($chara[10] / $divpm));
	$bw4 = int(1 * ($chara[11] / $divpm));
	$bw5 = int(1 * ($chara[12] / $divpm));
	$bw6 = int(1 * ($chara[13] / $divpm));
	$bwlp    = int(1 * ($chara[20] / $divpm));
	$i_plus = $item[2] + $item[16];
	$d_plus = $item[5] + $item[18];
	$bwhit   = int(0.5 * ($hit_ritu + $i_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $d_plus));
	$bwwaza  = int(1 * ($waza_ritu + $item[17]));
	if($bwhit > 200){$bwhit = 200;}
	if($bwkaihi > 200){$bwkaihi = 200;}
	if($bwwaza > 200){$bwwaza = 200;}

	&syoku_load;

	$i = 0;
	$kmaster = "";
	foreach (@syoku_master) {
		if ($syoku_master[$i] >= 60){
			$kmaster .="<td nowrap align=center width=25% class=b1>$chara_syoku[$i]</td>";
		}
		$i++;
		if ($i % 5 == 0) { $kmaster .= "</tr>\n<tr>"; }
	}

	&header;

	print <<"EOM";
<table align="center"><TR><TD><font size=5>$chara[4]さんのステータス画面</font></TD><TD>
</TD></table>
<hr size=0>
<table border=0 align="center" width='50%'>
<tr>
<td valign=top width='100%'>
<table width="100%"><tr>
<tr><td id="td1" colspan="5" class="b2" align="center">キャラクターデータ</td></tr>
<td rowspan="4" align="center" valign=bottom class="b2"><img src="$img_path/$chara_img[$chara[6]]">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$item[0]</td>
<td id="td2" class="b1">攻撃力</td><td align="right" class="b2">$item[1]</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$item[3]</td>
<td id="td2" class="b1">防御力</td><td align="right" class="b2">$item[4]</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$item[6]</td></tr>
</table>
<table width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr>
<td class="b1" id="td2">なまえ</td><td class="b2">$chara[4]</td>
<td class="b1" id="td2">性別</td><td class="b2">$esex</td></tr>
<tr><td class="b1" id="td2">ジョブ</td><td class="b2">$chara_syoku[$chara[14]]</td>
<td id="td2" class="b1">ジョブLV</td><td class="b2"><b>$chara[33]</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$chara[18]</td>
<td class="b1" id="td2">経験値</td><td class="b2">$chara[17]/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$chara[15]\/$chara[16]</td>
<td class="b1" id="td2">お金</td><td class="b2">$chara[19]</td></tr>
<tr><td class="b1" id="td2">力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$chara[7] + $item[8]</b></td>
<td class="b1" id="td2">魔力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$chara[8] + $item[9]</b></td></tr>
<tr><td class="b1" id="td2">信仰心</td><td align="left" class="b2"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$chara[9] + $item[10]</b></td>
<td class="b1" id="td2">生命力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$chara[10] + $item[11]</b></td></tr>
<tr><td class="b1" id="td2">器用さ</td><td align="left" class="b2"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$chara[11] + $item[12]</b></td>
<td class="b1" id="td2">速さ</td><td align="left" class="b2"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$chara[12] + $item[13]</b></td></tr>
<tr><td class="b1" id="td2">魅力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$chara[13] + $item[14]</b></td>
<td class="b1" id="td2">カルマ</td><td align="left" class="b2"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$chara[20] + $item[15]</b></td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $i_plus%</b></td>
<td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu + $d_plus%</b></td></tr>
<tr>
<td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $item[17]%</b></td>
<td id="td2" class="b2">称号</td><td align="left" class="b2"><font color="$yellow">$shogo[$chara[32]]</font></td>
</tr>
</table>
<table width="100%"><tr><td id="td2" align="center" class="b1">極めたジョブ</td></tr>
<tr>$kmaster</tr></table>
</table>
EOM

	&footer;

	exit;
}

#----------------#
#キャラ画像参照  #
#----------------#
sub img_list {

	&header;

	print <<"EOM";
<TABLE ALIGN="center" BORDER="1" CELLSPACING="3" CELLPADDING="3">
<CAPTION>キャラ一覧</CAPTION>
<tr>
EOM

	$i=0;
	foreach(@chara_img){
		print "<td><img src=\"$img_path/$chara_img[$i]\"><br>$i</td>\n";
		$i++;
		if ($i % 10 == 0) { print "</tr>\n<tr>\n"; }
	}

	print <<"EOM";
</tr></table><br>
EOM

&footer;

exit;

}
