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
#     http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 牧場用ライブラリの読み込み
require 'choco-farm.pl';


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
if($mente) { &error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m"); }
&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}

if($mode eq 'dendo') {&dendo;}
&rank;

#----------------#
#  　　登録 　   #
#----------------#
sub dendo{

	&chara_load;

	&chara_check;

	if($in{'id'} eq "test"){&error("テストキャラは登録できません！！");}

	&farm_choco_read;

	$lock_file = "$lockfolder/dnd.lock";
	&lock($lock_file,'DND');
	open(IN,"./denchoco.cgi");
	@dencho = <IN>;
	close(IN);

	@newdendo=();$hit=0;
	foreach(@dencho){
	($dcid,$dcpass,$dcbreader,$dcname,$dcsex,$dcblood,$dcno,$dcmaxmax,$dctype,$dcmax1,$dcmax2,$dcmax3,$dcmax4,$dcmax5,$dcmax6,$dcmax7,$dclife,$dctrain,$dcrun,$dcwin,$dcmax,$dc1,$dc2,$dc3,$dc4,$dc5,$dc6,$dc7,$dcgold,$dcfather,$dcfblood,$dcmother,$dcmblood) = split(/<>/);
if($dcid eq "$kid" && $dcname eq "$cname"){$hit=1;unshift(@newdendo,"$cid<>$cpass<>$cbreader<>$cname<>$csex<>$cblood<>$cno<>$cmaxmax<>$ctype<>$cmax0<>$cmax1<>$cmax2<>$cmax3<>$cmax4<>$cmax5<>$cmax6<>$clife<>$ctrain<>$crun<>$cwin<>$cmax<>$c0<>$c1<>$c2<>$c3<>$c4<>$c5<>$c6<>$cgold<>$cfather<>$cfblood<>$cmother<>$cmblood<>\n");
}else{push(@newdendo,"$_"); }
}

if(!$hit){unshift(@newdendo,"$cid<>$cpass<>$cbreader<>$cname<>$csex<>$cblood<>$cno<>$cmaxmax<>$ctype<>$cmax0<>$cmax1<>$cmax2<>$cmax3<>$cmax4<>$cmax5<>$cmax6<>$clife<>$ctrain<>$crun<>$cwin<>$cmax<>$c0<>$c1<>$c2<>$c3<>$c4<>$c5<>$c6<>$cgold<>$cfather<>$cfblood<>$cmother<>$cmblood<>\n");}

	open(OUT,">./denchoco.cgi");
	print OUT @newdendo;
	close(OUT);
	$lock_file = "$lockfolder/dnd.lock";
	&unlock($lock_file,'DND');

	&header;

		print <<"EOM";
<h1>殿堂登録が完了しました。</h1>
<hr size=0>
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value='$chara_log'>
<input type=hidden name=mode value=log_in>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場へ">
</form>
EOM
	&choco_footer;

	exit;
}

#----------------#
#  　　殿堂 　   #
#----------------#
sub rank{

	&header;

print"<center><h1>殿堂入りしたチョコボたちの一覧</h1><hr></center>";

	open(IN,"./denchoco.cgi");
	@dencho = <IN>;
	close(IN);
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
	@type = ('逃げ','先行','普通','差し','追込','自在');

	$n=0;
	foreach (@dencho) {
	($dcid,$dcpass,$dcbreader,$dcname,$dcsex,$dcblood,$dcno,$dcmaxmax,$dctype,$dcmax1,$dcmax2,$dcmax3,$dcmax4,$dcmax5,$dcmax6,$dcmax7,$dclife,$dctrain,$dcrun,$dcwin,$dcmax,$dc1,$dc2,$dc3,$dc4,$dc5,$dc6,$dc7,$dcgold,$dcfather,$dcfblood,$dcmother,$dcmblood) = split(/<>/);

	open(IN,"./rireki.cgi");
	@rireki = <IN>;
	close(IN);

$hit=0;
	foreach(@rireki){
			($rid,$rpass,$rname,$rfather,$rmother,$rire[1],$rire[2],$rire[3],$rire[4],$rire[5],$rire[6],$rire[7],$rire[8],$rire[9],$rire[10],$rire[11],$rire[12],$rire[13],$rire[14],$rire[15],$rire[16],$rire[17],$rire[18],$rire[19],$rire[20],$rire[21],$rire[22],$rbreader) = split(/<>/);
if($rid eq "$dcid" && $rpass eq "$dcpass" && $rname eq "$dcname"){last;}}
$racename="";
if($rire[1]){$racename .= "<font color = red>・チョコボダービー</font>";}
if($rire[2]){$racename .= "<font color = red>・チョコボスタリオン";}
if($rire[3]){$racename .= "<font color = red>・チョコボカップ";}
if($rire[4]){$racename .= "<font color = red>・レジェンドカップ</font>";}
if($rire[5]){$racename .= "<font color = red>・ＣＣＢ賞</font>";}
if($rire[6]){$racename .= "<font color = red>・チョコボ桜花賞</font>";}
if($rire[7]){$racename .= "<font color = red>・チョコボ皐月賞</font>";}
if($rire[8]){$racename .= "<font color = red>・チョコボ記念</font>";}
if($rire[9]){$racename .= "<font color = red>・チョコボステークス</font>";}
if($rire[10]){$racename .= "<font color = red>・キングスカップ</font>";}
if($rire[11]){$racename .= "<font color = red>・クイーンカップ</font>";}
$racename .="<br>";
if($rire[12]){$racename .= "<font color = blue>・シルバーカップ</font>";}
if($rire[13]){$racename .= "<font color = blue>・ＫイクアンドＱエリリン</font>";}
if($rire[14]){$racename .= "<font color = blue>・チョコリスダービー</font>";}
if($rire[15]){$racename .= "<font color = blue>・チョコボワールドカップ</font>";}
if($rire[16]){$racename .= "<font color = blue>・チョコボエンプレス杯</font>";}
if($rire[17]){$racename .= "<font color = blue>・チョコボウル</font>";}
if($rire[18]){$racename .= "<font color = blue>・ブリーダーズカップ</font>";}
if($rire[19]){$racename .= "<font color = blue>・ゴールドカップ</font>";}
if($rire[20]){$racename .= "<font color = blue>・プラチナカップ</font>"}
if($rire[21]){$racename .= "<font color = blue>・チョコボオークス</font>";}
if($rire[22]){$racename .= "<font color = blue>・チョコボキングス</font>";}

	$c1_t = int($dc1 / 100);
	$c2_t = int($dc2 / 100);
	$c3_t = int($dc3 / 100);
	$c4_t = int($dc4 / 100);
	$c5_t = int($dc5 / 100);
	$c6_t = int($dc6 / 100);
	$c7_t = int($dc7 / 100);
	$tikara = $nimg[$c1_t];
	$tairyoku = $nimg[$c2_t];
	$nebari = $nimg[$c3_t];
	$otituki = $nimg[$c4_t];
	$tousou = $nimg[$c5_t];
	$tiryoku = $nimg[$c6_t];
	$kire = $nimg[$c7_t];
	if($dcsex){$sei = "♂";}
	else{$sei = "♀";}

	$money=$dcgold*100;

	$waza = $type[$dctype];

		print <<"EOM";
<form action="./crace2.cgi" method="post">
<TABLE border=10 width=100%  bordercolorlight=#ccdd00 bordercolordark=#cccc33><TBODY>    <TR>
      <TD><input type="radio" name="enter1" value="$n">1</TD>
      <TD rowspan="5" align="center"><img src=\"$img_farm/$choco_img[$dcno]\" ></TD>
      <TD align="center" class="b1" id="td2">なまえ</TD>
      <TD align="center" class="b2">$dcname</TD>
      <TD align="center" class="b1" id="td2">父</TD>
      <TD align="center" class="b2">$dcfather</TD>
      <TD align="center" width="80" class="b1" id="td2">筋力</TD>
      <TD align="center" width="80" class="b1" id="td2">体力</TD>
      <TD align="center" width="80" class="b1" id="td2">粘り強さ</TD>
      <TD align="center" width="80" class="b1" id="td2">落ち着き</TD>
      <TD align="center" width="80" class="b1" id="td2">闘争心</TD>
      <TD align="center" width="80" class="b1" id="td2">賢さ</TD>
      <TD align="center" width="80" class="b1" id="td2">反射神経</TD>
    </TR>
    <TR>
      <TD><input type="radio" name="enter2" value="$n">2</TD>
      <TD align="center" class="b1" id="td2">タイプ</TD>
      <TD align="center" class="b2">$waza</TD>
      <TD align="center" class="b1" id="td2">母</TD>
      <TD align="center" class="b2">$dcmother</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$tikara</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$tairyoku</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$nebari</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$otituki</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$tousou</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$tiryoku</TD>
      <TD align="center" width="80" class="b2" rowspan="2">$kire</TD>
    </TR>
    <TR>
      <TD><input type="radio" name="enter3" value="$n">3</TD>
      <TD align="center" class="b1" id="td2">性別</TD>
      <TD align="center" class="b2">$sei</TD>
      <TD align="center" class="b1" id="td2">試合数</TD>
      <TD align="center" class="b2">$dcrun</TD>
    </TR>
    <TR>
      <TD><input type="radio" name="enter4" value="$n">4</TD>
      <TD align="center" class="b1" id="td2">ブリーダー</TD>
      <TD align="center" class="b2">$dcbreader</TD>
      <TD align="center" class="b1" id="td2">勝数</TD>
      <TD align="center" class="b2">$dcwin</TD>
      <TD align="center" colspan="7" class="b1" id="td2">獲得したＧⅠ</TD>
    </TR>
    <TR>
      <TD><input type="radio" name="enter5" value="$n">5</TD>
      <TD align="center" class="b1" id="td2">総賞金</TD>
      <TD align="center" class="b2">$money</TD>
      <TD align="center" class="b1" id="td2">練習</TD>
      <TD align="center" class="b2">$dctrain</TD>
      <TD align="center" colspan="7" class="b2">$racename</TD>
    </TR>
</TBODY></TABLE><br>
EOM
		$n++;
	}

		$n++;

if($n >= 5){
       print <<"EOM";
出場チョコボランダム用<br>
<input type="radio" name="enter1" value="$n" checked>1
<input type="radio" name="enter2" value="$n" checked>2
<input type="radio" name="enter3" value="$n" checked>3
<input type="radio" name="enter4" value="$n" checked>4
<input type="radio" name="enter5" value="$n" checked>5<br>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="殿堂チョコボの展示レース">
</form>
EOM
}
	&choco_footer;

	exit;
}
