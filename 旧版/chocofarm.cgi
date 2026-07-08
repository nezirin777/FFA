#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#　いかなる理由があってもこの表記を削除することはできません
#　違反を発見した場合、スクリプトの利用を停止していただく
#　だけでなく、然るべき処置をさせていただきます。
#  チョコボ牧場 edit by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#     http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi 		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 牧場ライブラリの読み込み
require 'choco-farm.pl';

# レジストライブラリの読み込み
require 'sankasya.pl';


# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $farm_back;
$midi = $farm_midi;
$style_sheet = $chococss;

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

exit;

#----------------#
#  ログイン画面  #
#----------------#
sub log_in {

	&chara_load;

	&chara_check;

	&item_load;

	&read_farm_winner;

	&farm_choco_read;

	@measure = ('Ｅ','Ｄ','Ｃ','Ｃ','Ｂ','Ｂ','Ａ','Ａ','Ｓ','Ｓ','ＳＳ','ＳＳ','ＳＳ','ＳＳ');

	$wc0_t = int($wc0/100);
	$wc1_t = int($wc1/100);
	$wc2_t = int($wc2/100);
	$wc3_t = int($wc3/100);
	$wc4_t = int($wc4/100);
	$wc5_t = int($wc5/100);
	$wc6_t = int($wc6/100);

	$wkin = $measure[$wc0_t];
	$wtai = $measure[$wc1_t];
	$wneb = $measure[$wc2_t];
	$woti = $measure[$wc3_t];
	$wtou = $measure[$wc4_t];
	$wkasi = $measure[$wc5_t];
	$whan = $measure[$wc6_t];

	open(IN,"./hint.cgi");
	@hint = <IN>;
	close(IN);

	$jun = int(rand(@hint));

	$com = $hint[$jun];

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$vtime = $b_time - $ltime;
	$xtime = $vtime + 1;
	$ztime = $vtime + 1;
	$mtime = $m_time - $ltime + 1;

	if ($chara[28] < $boss) {
		$chara[28] = 0;
	}

	&class;

	if ($chara[5]) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $chara[18] * $lv_up;

        if (!$chara[32]) {$chara[32] = 0;}
	$syou = @shogo[$chara[32]];

	&header;

	&guest_list;

	&guest_view;


       print <<"EOM";
	<hr size=0>
	<font class=white>メニュー/</font><a href="$scripta?mode=ranking">登録者一覧</a> / <a href="$ranking">能\力別ランキングへ</a> / <a href="$syoku_html" target="_blank">各職業に必要な特性値</a> /<a href="$img_all_list" target="_blank">$vote_gazou</a> /<a href="$bbs" target="_blank">$bbs_title</a> /<a href="$helptext" target="_blank">$helptext_url</a><br>
<font class=white>町の外れ/</font><a href="$sbbs" target="_blank">$sbbs_title</a> / <a href="$vote" target="_blank">$vote_title</a> / <font color = black><a href = "./chocorank.cgi?mode=ranking"><b>サラブレッドチョコボランキング</b></a></font><br>
<TABLE align="center">
<TR><TD align=center rowspan="4" class="b2" width=70 height=60><img src=\"$img_farm/$choco_img[$wcno]\"></TD>
<TD id="td1" align="center" colspan=2 class="b2" width=360><font color=yellow>トップオブサラブレッド</FONT></TD>
<TD rowspan="4" align="center" class="b2"><font color="#ff0000" size = 5><b>$wcren</b></FONT><br><font color="blue">連勝中<br></TD></font></TR>
<tr><TD align=center colspan=2 class="b2"><font size=1><B>筋力:<font color = red>$wkin</font>･体力:<font color = red>$wtai</font>･粘り:<font color = red>$wneb</font>･落ち着き:<font color = red>$woti</font>･闘争心:<font color = red>$wtou</font>･賢さ:<font color = red>$wkasi</font>･反射:<font color = red>$whan</font></B></font></TD></tr>
<TR><TD align=center class="b2"><FONT color="#f23e66"><B>$wcbreader</B>さんの</font><font size=3 color="blue"><B>$wcname</B></font>です</a></TD>
<TD class="b2" align="right"><B>$wcrun 戦 $wcwin 勝</B></TD></TR>
<TR><TD colspan="2" class="b2" align="center">最後に<font color="#22ae22">$wclbreader</font></a>さんの<font color="#f23e66"><B>$wclname</B></font>に勝利しています。
</TD></TR></TABLE>
<br>
<hr size=0>

<table border=0 align="center" width='100%'>
<tr>
<td valign=top width='50%'>
EOM


	if ($cmaxmax) {

		if ($ztime > 0) {
		       print <<"EOM";
<table><tr>
<FORM NAME="form1">
<td>
レース開始可能\まで残り<INPUT TYPE="text" NAME="clock" SIZE="3">秒です。(更新の目安に使って下さい)
</td>
</FORM>
</tr></table>
EOM
		}

		open(IN,"./g1/$chara[0].cgi");
		@rireki = <IN>;
		close(IN);

		$hit=0;
		foreach(@rireki) {
			($rid,$rpass,$rname,$rfather,$rmother,$rire[1],$rire[2],$rire[3],$rire[4],$rire[5],$rire[6],$rire[7],$rire[8],$rire[9],$rire[10],$rire[11],$rire[12],$rire[13],$rire[14],$rire[15],$rire[16],$rire[17],$rire[18],$rire[19],$rire[20],$rire[21],$rire[22],$rbreader) = split(/<>/);
			if ($rid eq "$cid" && $rname eq "$cname") {
				$hit = 1;
				last;
			}
		}

		if (!$hit) {for($i=1;$i<=20;$i++) {$rire[$i]=0;}}
		$renz=0;

		if ($rire[1]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボダービー</font></td>";
			$renz+=1;
		}

		if ($rire[2]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボスタリオン</td>";
			$renz+=1;
		}

		if ($rire[3]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボカップ</td>";
			$renz+=1;
		}

		if ($rire[4]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>レジェンドカップ</font></td>";
			$renz+=1;
		}

		if ($rire[5]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>ＣＣＢ賞</font></td>";
			$renz+=1;
			if ($renz==5) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[6]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボ桜花賞</font></td>";
			$renz+=1;

			if ($renz==5) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[7]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボ皐月賞</font></td>";
			$renz+=1;
			if ($renz==5) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[8]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボ記念</font></td>";
			$renz+=1;
			if ($renz==5) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[9]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>チョコボステークス</font></td>";
			$renz+=1;
			if ($renz==5) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[10]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>キングスカップ</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[11]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = red>クイーンカップ</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[12]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>シルバーカップ</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[13]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>ＫイクアンドＱエリリン</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[14]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>チョコリスダービー</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[15]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>チョコボワールドカップ</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[16]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>チョコボエンプレス杯</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[17]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>チョコボウル</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[18]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>ブリーダーズカップ</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[19]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>ゴールドカップ</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[20]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>プラチナカップ</td></font>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[21]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>チョコボオークス</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($rire[22]) {
			$racename .= "<td class=\"b2\" align=\"center\"><font color = blue>チョコボキングス</font></td>";
			$renz+=1;
			if ($renz%5 == 0) {
				$racename .= "</tr><tr>";
			}
		}

		if ($cwin == 0) {
			$cls = "新羽";
		} elsif ($cwin < 5) {
			$cls = "５００万下";
		} elsif ($cwin < 15) {
			$cls = "９００万下";
		} elsif ($cwin < 30) {
			$cls = "１６００万下";
		} elsif ($cwin < 50) {
			$cls = "オープン";
		} elsif ($cwin < 75) {
			$cls = "グレードⅢ";
		} elsif ($cwin < 105) {
			$cls = "グレードⅡ";
		} elsif ($cwin < 140) {
			$cls = "グレードⅠ";
		} elsif ($cwin >= 140) {
			$cls = "伝説級";
		}

		@nimg = ("<img src =$img_farm/e.gif>",
			"<img src =$img_farm/d.gif>",
			"<img src =$img_farm/c.gif>",
			"<img src =$img_farm/c.gif>",
			"<img src =$img_farm/b.gif>",
			"<img src =$img_farm/b.gif>",
			"<img src =$img_farm/a.gif>",
			"<img src =$img_farm/a.gif>",
			"<img src =$img_farm/s.gif>",
			"<img src =$img_farm/s.gif>",
			"<img src =$img_farm/ss.gif>",
			"<img src =$img_farm/ss.gif>",
			"<img src =$img_farm/ss.gif>",
			"<img src =$img_farm/ss.gif>",
			"<img src =$img_farm/ss.gif>");

		$c0_t = int($c0 / 100);
		$c1_t = int($c1 / 100);
		$c2_t = int($c2 / 100);
		$c3_t = int($c3 / 100);
		$c4_t = int($c4 / 100);
		$c5_t = int($c5 / 100);
		$c6_t = int($c6 / 100);

		$tikara = $nimg[$c0_t];
		$tairyoku = $nimg[$c1_t];
		$nebari = $nimg[$c2_t];
		$otituki = $nimg[$c3_t];
		$tousou = $nimg[$c4_t];
		$tiryoku = $nimg[$c5_t];
		$kire = $nimg[$c6_t];

		if ($csex) {$sei = "♂";}
		else {$sei = "♀";}

		$money = $cgold * 100;

		@type = ('逃げ','先行','普通','差し','追込','自在');
		$waza = $type[$ctype];

		@status = ('動けない','疲労困憊','疲れ気味','普通','元気');

		if ($clife >= 990) {
			$csta = "元気いっぱい";
		} else {
			$life_t = int($clife / 200);
			$csta = $status[$life_t];
		}

		print << "EOM";
<table width="100%">
<tr>
<td class="b2"id="td1"  colspan=8 align=center>
サラブレッドチョコボ情報
</td>
</tr>
<tr>
<td align="center" class="b2"rowspan=4 colspan=2 height=100>
<img src="$img_farm/$choco_img[$cno]" >
</td>
<td class="b1"id="td2">なまえ</td>
<td class="b2">$cname</td>
<td class="b1"id="td2">試合数</td>
<td class="b2">$crun</td>
<td class="b1"id="td2">勝利数</td>
<td class="b2">$cwin勝</td>
</tr>
<tr>
<td class="b1"id="td2">タイプ</td>
<td class="b2">$waza</td>
<td class="b1"id="td2">クラス</td>
<td class="b2">$cls</td>
<td class="b1"id="td2">練習数</td>
<td class="b2">$ctrain</td>
</tr>
<tr>
<td class="b1"id="td2">性別</td>
<td class="b2">$sei</td>
<td class="b1"id="td2">父</td>
<td class="b2">$cfather</td>
<td class="b1"id="td2">母</td>
<td class="b2">$cmother</td>
</tr>
<tr>
<td class="b1"id="td2"colspan=2 align="center">獲得本賞金</td>
<td class="b2" colspan=4 align="center">$moneyギルを獲得</td>
</tr>
<tr>
<td class="b1"id="td2" align="center">筋力</td>
<td class="b2" align="center">$tikara</td>
<td class="b1"id="td2" align="center">体力</td>
<td class="b2" align="center">$tairyoku</td>
<td class="b1"id="td2" align="center">粘り強さ</td>
<td class="b2" align="center">$nebari</td>
<td class="b1"id="td2" align="center">落ち着き</td>
<td class="b2" align="center">$otituki</td>
</tr>
<tr>
<td class="b1"id="td2" align="center">闘争心</td>
<td class="b2" align="center">$tousou</td>
<td class="b1"id="td2" align="center">賢さ</td>
<td class="b2" align="center">$tiryoku</td>
<td class="b1"id="td2" align="center">反射神経</td>
<td class="b2" align="center">$kire</td>
<td class="b1"id="td2" align="center">じょうたい</td>
<td class="b2" align="center">$csta</td>
</tr>
</table>
EOM

		if ($renz) {
			print "<table width=100%><TR><TD width=100% class=\"b1\"id=\"td2\" colspan=5 align=center>勝利ＧⅠ</TD></TR><tr>$racename</tr></table>\n";
		}

		print << "EOM";
<table width=100%>
<TR>
<TD width=100% class="b2"id="td1" colspan=3 align=center>
トレーニング
</TD>
</TR>
<tr>
<td class="b1"id="td2" align=center>
練習
</td>
<form action="./ctrain.cgi" method="post">
<td class="b2"align="center">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
EOM

		if ($ltime > $m_time) {

			print << "EOM";
<select name="mode">
<option value="race0">筋トレ</option>
<option value="race1">長距離走</option>
<option value="race2">水泳</option>
<option value="race3">座禅</option>
<option value="race4">鬼ごっこ</option>
<option value="race5">勉強</option>
<option value="race6">障害物競走</option>
</select>
</td>
<td class="b2"align="center">
<input type="submit" style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="トレーニング">
</td>
EOM

		} else {
		print "</td><td class=\"b2\"align=\"center\">$mtime秒後練習できます。</td>\n";
		}

		print << "EOM";
</form></tr><TR>
<TD width=100% class="b2"id="td1" colspan=3 align=center>
キングに挑戦
</TD>
</TR>
<tr>
<form action="./farmrace.cgi" method="post">
<td class="b1"id="td2" align=center>
キングに挑戦</td>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type="hidden" name="mode" value="chocobattle">
EOM

		if ($wcid eq $chara[0] && $wcname eq "$cname") {
			print "<td class=\"b2\" align=\"center\" colspan=2>現在チョコボキングです</td>\n";
		} elsif ($ltime > $b_time) {
			print "<td class=\"b2\"align=\"center\" colspan=2><input type=\"submit\"style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\"  value=\"チョコボキングに挑戦\"></td>\n";
		} else {
		print "<td class=\"b2\"align=\"center\" colspan=2>$ztime秒後レースできます。</td>\n";
		}

	print <<"EOM";
</form></tr></tr>
</table>
<table width="100%">
          <TR>
            <TD width=100% class="b2"id="td1"  colspan=2 align=center>レース場</TD>
          </TR>
<tr>
<form action="./crace.cgi" method="post">
<td class="b2"align="center">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
EOM

		if ($ltime > $m_time) {
			$limit=0;
			print "<select name=mode>\n";

			if ($cwin >= 75 && $cwin <= 130) {
				print"<option value=\"race6\">グレードⅡ\n";
				$limit=1;
			}

			if ($cwin >= 50 && $cwin <= 100) {
				print"<option value=\"race5\">グレードⅢ\n";
				$limit=1;
			}

			if ($cwin >= 30 && $cwin <= 80) {
				print"<option value=\"race4\">オープン\n";
				$limit=1;
			}

			elsif ($cwin >= 15 && $cwin <30) {
				print"<option value=\"race3\">１６００万下\n";
				$limit=1;
			}

			elsif ($cwin >= 5 && $cwin <15) {
				print"<option value=\"race2\">９００万下\n";
				$limit=1;
			}
			elsif ($cwin >= 1 && $cwin <5) {
				print"<option value=\"race1\">５００万下\n";
				$limit=1;
			}

			elsif ($cwin == 0) {
				print"<option value=\"race0\">新羽戦\n";
				$limit=1;
			}

			print"</select>\n";

			if (!$limit) {
				print"一般戦に出るには強すぎます</td>";
			}
			else{
				print "</td><td class=\"b2\"align=\"center\"><input type=\"submit\" style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value=\"レースに出場\"></td>\n";
			}
		} else {
			print "$mtime秒後レースできます。</td>\n";
		}

		print <<"EOM";
</form></tr></TABLE>
<table width="100%">
          <TR>
            <TD width=100% class=\"b2\"id=\"td1\"  colspan=2 align=center>ＧⅠレース</TD>
          </TR>
<tr>
<form action="./crace.cgi" method="post">
<td class="b2"align="center">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value="race7">
EOM

		if ($cwin >= 30) {
			if ($ltime > $m_time) {
				$sikaku = ($crun + $ctrain)/200;
				$nokori = 40 - ($crun + $ctrain)%40;
				$hit = 0;
				print"<select name=race>\n";
				if (($crun + $ctrain) % 400 == 0) {
					print"<option value=\"1\">チョコボダービー\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 360) % 400 == 0) {
					print"<option value=\"2\">チョコボスタリオン\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 320) % 400 == 0) {
					print"<option value=\"3\">チョコボカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 280) % 400 == 0) {
					print"<option value=\"4\">レジェンドカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 240) % 400 == 0) {
					print"<option value=\"5\">ＣＣＢ賞\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 200) % 400 == 0) {
					print"<option value=\"6\">チョコボ桜花賞\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 160) % 400 == 0) {
					print"<option value=\"7\">チョコボ皐月賞\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 120) % 400 == 0) {
					print"<option value=\"8\">チョコボ記念\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 80) % 400 == 0) {
					print"<option value=\"9\">チョコボステークス\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 40) % 400 == 0) {
					if ($csex) {
						print"<option value=\"10\">キングスカップ\n";
					} else {
						print"<option value=\"11\">クイーンカップ\n";
					}
					$hit=1;
				}

				print"</select>\n";

				if ($hit) {
					print "</td><td class=\"b2\"align=\"center\"><input type=\"submit\" style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value=\"レースに出場\"></td>\n";
				} else {
					print"現在開催レースはありません。<br>次のレースまで練習・試合$nokori回後です。</td>";
				}

			} else {
				print "$mtime秒後レースできます。</td>\n";
			}
		}
		else {
			print"オープン以上のみです。</td>";
		}

		if ($renz >= 3) {

			print <<"EOM";
</form></tr>
<tr>
<TR>
<TD width=100% class="b2"id="td1"  colspan=2 align=center>海外ＧⅠレース</TD>
</TR>
<tr>
<form action="./crace.cgi" method="post">
<td class="b2"align="center">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value="race8">
EOM

			if ($ltime > $m_time) {
				$ksikaku = ($crun + $ctrain)/300;
				$knokori = 60 - ($crun + $ctrain)%60;
				$hit=0;
				print"<select name=race>\n";

				if (($crun + $ctrain) % 600 == 0) {
					print"<option value=\"12\">シルバーカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 540) % 600 == 0) {
					print"<option value=\"13\">ＫイクアンドＱエリリン\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 480) % 600 == 0) {
					print"<option value=\"14\">チョコリスダービー\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 420) % 600 == 0) {
					print"<option value=\"15\">チョコボワールドカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 360) % 600 == 0) {
					print"<option value=\"16\">チョコボエンプレス杯\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 300) % 600 == 0) {
					print"<option value=\"17\">チョコボウル\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 240) % 600 == 0) {
					print"<option value=\"18\">ブリーダーズカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 180) % 600 == 0) {
					print"<option value=\"19\">ゴールドカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 120) % 600 == 0) {
					print"<option value=\"20\">プラチナカップ\n";
					$hit=1;
				}

				elsif (($crun + $ctrain + 60) % 600 == 0) {
					if ($csex) {
						print"<option value=\"22\">チョコボキングス\n";
						$hit=1;
					} else {
						print"<option value=\"21\">チョコボオークス\n";
						$hit=1;
					}
				}
				print"</select>\n";

				if ($hit) {
					print "</td><td class=\"b2\"align=\"center\"><input type=\"submit\" style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value=\"レースに出場\"></td>\n";
				} else {
					print"現在開催レースはありません。<br>次のレースまで練習・試合$knokori回後です。</td>";
				}
			} else {
				print "$mtime秒後レースできます。</td>\n";
			}

			print <<"EOM";
</form></tr><tr>
<form action="./dendo.cgi" method="post">
<td class="b2"align="center" colspan=2>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=dendo>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="殿堂登録する">
</td>
EOM
		}
		print "</form></tr>";
	}

	print <<"EOM";
</TABLE></td>
<td valign="top">
<table width="100%">
<tr><td id="td1" colspan="4" class="b2" align="center">チョコ牧場</td></tr>
<tr><td bgcolor="#cbfffe" align="center">【放牧】(5000 G)</td>
<td bgcolor="#cbfffe" align="center">【チョコボの森】</td>
<td bgcolor="#cbfffe" align="center">【更新所】</td>
<td bgcolor="#cbfffe" align="center">【街に戻る】</td></tr>
<tr>
<form action="./morifarm.cgi" method="post">
<td align="center" class="b2">
EOM
		if ($cname ne "") {
			print <<"EOM";
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=yadoya>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="チョコボの体力回復"><br>練習回数に入ります
EOM
		} else {
			print "チョコボがいません";
		}

	print <<"EOM";
</td>
</form>
<form action="./morifarm.cgi" method="post">
<td align=center class=b2>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="チョコボの森"></td></form>
<form action="./chocofarm.cgi" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=log_in>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="画面更新">
</td>
</form>
<form action="$script" method="post">
<td align="center" class="b2">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=log_in>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="街へ"></td>
</form>
</tr>
</table>
<TABLE width=100% bgcolor=0000FF><TBODY>
<tr>
<td id="td1" colspan="2" class="b2" align="center">
モーグリからのアドバイス
</td>
</tr>
<TR>
<TD width=10 bgcolor=#99CCFF>
<img src=\"$img_farm/mog.gif\">
</TD>
<TD width=100% bgcolor=#ff66cc>
<font size="3" color="#FFFFFF">
$com
</font></TD></TR></TBODY></TABLE>
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
</TABLE></td></tr></table>
EOM

	&message_load;

	&choco_footer;

	$chara_flag=0;

	exit;
}
