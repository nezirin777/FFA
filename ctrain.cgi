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

# 牧場用ライブラリの読み込み
require 'choco-farm.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

# このファイル用設定
$backgif = $farm_back;
$midi = $farm_midi;
$style_sheet = $chococss;

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
$backform = << "EOM";
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$in{'id'}">
<input type="hidden" name=mydata value="$in{'mydata'}">
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場に戻る">
</form>
EOM

if($mode eq 'race0') { $syurui = 0; $subject = "バーベル上げ"; }
elsif($mode eq 'race1') {$syurui = 1; $subject = "長距離走"; }
elsif($mode eq 'race2') {$syurui = 2; $subject = "スイミング"; }
elsif($mode eq 'race3') {$syurui = 3; $subject = "精神統一"; }
elsif($mode eq 'race4') {$syurui = 4; $subject = "鬼ごっこ"; }
elsif($mode eq 'race5') {$syurui = 5; $subject = "勉強"; }
elsif($mode eq 'race6') {$syurui = 6; $subject = "障害物競走"; }

&training;

exit;

#--------------#
#   練習画面   #
#--------------#
sub training {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&lock($lock_file,'CHC');
	&farm_choco_read;

	if (!$cname) {&error('チョコボがいません。');}
	if($clife < 200){&error("疲れすぎています！$backform");}

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$chara[27] = time();
	$vtime = $b_time - $ltime;
	$success = 0;
	$lose = 0;
	$turn=20;

	@pre_com = ('<font size = 4 color = blue>持ち上げられなかった･･･。</font>','<font size = 4 color = blue>寄り道して遊んじゃった･･･。</font>','<font size = 4 color = blue>溺れちゃった･･･。</font>','<font size = 4 color = blue>目の前の蝶々が気になって集中できない･･･。</font>','<font size = 4 color = blue>鬼に捕まっちゃった･･･。</font>','<font size = 4 color = blue>居眠りしてしまった･･･。</font>','<font size = 4 color = blue>障害物にひっかかってしまった･･･。</font>');
	$mae = int(rand(1000));
	$usiro = int(rand(1000));
	$kotae = $mae*$usiro;
	@pre_s_com = ('<font size = 4 color = red>持ち上げ成功！</font>','<font size = 4 color = red>必死に走ったぞ！</font>','<font size = 4 color = red>グングン泳いだ！</font>','<font size = 4 color = red>静かなること山の如し！</font>','<font size = 4 color = red>鬼で捕まえまくった♪</font>',"<font size = 4 color = red>$mae×$usiro＝$kotae！完璧！</font>",'<font size = 4 color = red>すいすい障害物を避けた！</font>');

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$com = "";


		if(int(rand(4)) == 1){
			$com = $pre_com[$syurui];
			$lose = $lose + 1;
		}
			else{
			$com = $pre_s_com[$syurui];
			$success = $success + 1;
		}

		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0 WIDTH=100%>
<TR>
	<TD ALIGN="center">
	<font size = 3 color = black>$i回目の挑戦</font>
	</TD>
</TR>
<TR>
<TD ALIGN="center">
<TABLE BORDER=0>
	<TD CLASS="b1"id="td2">
	ブリーダー
	</TD>
	<TD CLASS="b1"id="td2">
	なまえ
	</TD>
	<TD CLASS="b1"id="td2" align="center">
	成功回数/失敗回数
	</TD>
	<TD align="center"></TD>
</TR>
<TR>
	<TD CLASS="b2">
	$chara[4]
	</TD>
	<TD CLASS="b2">
	$cname
	</TD>
	<TD CLASS="b2">
	$success/$lose
	</TD>
	<TD ALIGN="center">
	<IMG SRC="$img_farm/$choco_img[$cno]" >
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>
<center>$com</center>
<p>
EOM

		$i++;
		$j++;

	}

	$agari = "";
	$senzai = "";
	$rousui = "";
	$genkai = "";

if($success && $lose){
if($syurui == 0){$c0 += int($success*2/3 + 1);$c6 -= int($lose/2 + 1);
if($cmax0 > $c0){$agari = "力強くなった！少し反射が鈍くなった！";}
else{$cmax0 += 3;$c0 = $cmax0;$agari = "$cnameの筋力は限界のようだが、ほんの少しだけ成長が見える<br>少し反射が鈍くなった！";}
}
elsif($syurui == 1){$c1 += int($success*2/3 + 1);$c5 -= int($lose/2 + 1);
if($cmax1 > $c1){$agari = "体力がついた！少し勉強のことを忘れてしまった！";}
else{$cmax1 += 3;$c1 = $cmax1;$agari = "$cnameの体力は限界のようだが、ほんの少しだけ成長が見える<br>少し勉強のことを忘れてしまった！";}
}
elsif($syurui == 2){$c2 += int($success/2);
if($cmax2 > $c2){$agari = "我慢強くなった！";}
else{$cmax2 += 3;$c2 = $cmax2;$agari = "$cnameの我慢強さは限界のようだが、ほんの少しだけ成長が見える";}
}
elsif($syurui == 3){$c3 += int($success*2/3 + 1);$c4 -= int($lose/2 + 1);
if($cmax3 > $c3){$agari = "落ち着きの心を会得した！少し闘争心をなくしてしまった！";}
else{$cmax3 += 3;$c3 = $cmax3;$agari = "$cnameの落ち着きは限界のようだが、ほんの少しだけ成長が見える<br>少し闘争心をなくしてしまった！";}
}
elsif($syurui == 4){$c4 += int($success*2/3 + 1);$c3 -= int($lose/2 + 1);
if($cmax4 > $c4){$agari = "闘争心に火がついた！少し気性が荒くなった！";}
else{$cmax4 += 3;$c4 = $cmax4;$agari = "$cnameの闘争心は限界のようだが、ほんの少しだけ成長が見える<br>少し気性が荒くなった！";}
}
elsif($syurui == 5){$c5 += int($success*2/3 + 1);$c1 -= int($lose/2 + 1);
if($cmax5 > $c5){$agari = "賢くなった！少し体力が落ちた！";}
else{$cmax5 += 3;$c5 = $cmax5;$agari = "$cnameの賢さは限界のようだが、ほんの少しだけ成長が見える<br>少し体力が落ちた！";}
}
elsif($syurui == 6){$c6 += int($success*2/3 + 1);$c0 -= int($lose/2 + 1);
if($cmax6 > $c6){$agari = "反射神経が良くなった！筋力が少し落ちた！";}
else{$cmax6 += 3;$c6 = $cmax6;$agari = "$cnameの反射神経は限界のようだが、ほんの少しだけ成長が見える<br>筋力が少し落ちた！";}
}
}
elsif($success){
if($syurui == 0){$c0 += int($success*2/3 + 1);
if($cmax0 > $c0){$agari = "かなり力強くなった！";}
else{$cmax0 += 5;$c0 = $cmax0;$agari = "$cnameの筋力は限界のようだが、少しだけ成長が見える";}
}
elsif($syurui == 1){$c1 += int($success*2/3 + 1);
if($cmax1 > $c1){$agari = "かなり体力がついた！";}
else{$cmax1 += 5;$c1 = $cmax1;$agari = "$cnameの体力は限界のようだが、少しだけ成長が見える";}
}
elsif($syurui == 2){$c2 += int($success/2);
if($cmax2 > $c2){$agari = "かなり我慢強くなった！";}
else{$cmax2 += 5;$c2 = $cmax2;$agari = "$cnameの我慢強さは限界のようだが、少しだけ成長が見える";}
}
elsif($syurui == 3){$c3 += int($success*2/3 + 1);
if($cmax3 > $c3){$agari = "かなり落ち着きの心を会得した！";}
else{$cmax3 += 5;$c3 = $cmax3;$agari = "$cnameの落ち着きは限界のようだが、少しだけ成長が見える";}
}
elsif($syurui == 4){$c4 += int($success*2/3 + 1);
if($cmax4 > $c4){$agari = "かなり闘争心に火がついた！";}
else{$cmax4 += 5;$c4 = $cmax4;$agari = "$cnameの闘争心は限界のようだが、少しだけ成長が見える";}
}
elsif($syurui == 5){$c5 += int($success*2/3 + 1);
if($cmax5 > $c5){$agari = "かなり賢くなった！";}
else{$cmax5 += 5;$c5 = $cmax5;$agari = "$cnameの賢さは限界のようだが、少しだけ成長が見える";}
}
elsif($syurui == 6){$c6 += int($success*2/3 + 1);
if($cmax6 > $c6){$agari = "かなり反射神経が良くなった！";}
else{$cmax6 += 5;$c6 = $cmax6;$agari = "$cnameの反射神経は限界のようだが、少しだけ成長が見える";}
}
}
else{
if($syurui == 0){$c6 -= int($lose/2 + 1);$agari = "反射が鈍くなった！";}
elsif($syurui == 1){$c5 -= int($lose/2 + 1);$agari = "勉強のことを忘れてしまった！";}
elsif($syurui == 2){$agari = "何も効果がなかった・・・。";}
elsif($syurui == 3){$c4 -= int($lose/2 + 1);$agari = "闘争心をなくしてしまった！";}
elsif($syurui == 4){$c3 -= int($lose/2 + 1);$agari = "気性が荒くなった！";}
elsif($syurui == 5){$c1 -= int($lose/2 + 1);$agari = "体力が落ちた！";}
elsif($syurui == 6){$c0 -= int($lose/2 + 1);$agari = "筋力が落ちた！";}
}

$ctrain += 1;
if($ctrain + $crun > 1000){$cmaxmax = int($cmaxmax * 0.99);$rousui = "もう、これ以上$cnameを酷使するのは可哀想な気がする･･･。<br>これまですごくよくしてくれたと思うよ。<br>そろそろ引退の時期なんじゃないかな･･･？<br>";}

if($c0 > $cmax0){$genkai .= "筋力の限界に達したようだ<br>";$c0 = $cmax0;}
if($c1 > $cmax1){$genkai .= "体力の限界に達したようだ<br>";$c1 = $cmax1;}
if($c2 > $cmax2){$genkai .= "我慢強さの限界に達したようだ<br>";$c2 = $cmax2;}
if($c3 > $cmax3){$genkai .= "落ち着きの限界に達したようだ<br>";$c3 = $cmax3;}
if($c4 > $cmax4){$genkai .= "闘争心の限界に達したようだ<br>";$c4 = $cmax4;}
if($c5 > $cmax5){$genkai .= "賢さの限界に達したようだ<br>";$c5 = $cmax5;}
if($c6 > $cmax6){$genkai .= "反射神経の限界に達したようだ<br>";$c6 = $cmax6;}

if($c0 < 0){$genkai .= "筋力が下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>";$c0 = 1;$cmaxmax -= 5;}
if($c1 < 0){$genkai .= "体力が下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>>";$c1 = 1;$cmaxmax -= 5;}
if($c2 < 0){$genkai .= "我慢強さが下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>";$c2 = 1;$cmaxmax -= 5;}
if($c3 < 0){$genkai .= "筋力が下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>";$c3 = 1;$cmaxmax -= 5;}
if($c4 < 0){$genkai .= "落ち着きが下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>";$c4 = 1;$cmaxmax -= 5;}
if($c5 < 0){$genkai .= "賢さが下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>";$c5 = 1;$cmaxmax -= 5;}
if($c6 < 0){$genkai .= "反射神経が下がりすぎたため、チョコボが弱ってしまったようだ･･･<br>";$c6 = 1;$cmaxmax -= 5;}


$clife -= 50;
$cmax += 5;
if($cmax > $cmaxmax){
$cmax = $cmaxmax;
if($c0+$c1+$c2+$c3+$c4+$c5+$c6 > $cmax){$senzai = "もう$cnameの能\力の限界に達してしまったように見える･･･。<br>これ以上の成長はあまり見込めなさそうだ･･･。<br>";
if(int(rand(3)) > 1){$cmaxmax += 2;$senzai.="だけど、がんばったおかげで少し能\力が上昇したようだ･･･。<br>";}
$wariai=$cmax/($c0+$c1+$c2+$c3+$c4+$c5+$c6);
$c0=int($c0*$wariai)+1;
$c1=int($c1*$wariai)+1;
$c2=int($c2*$wariai)+1;
$c3=int($c3*$wariai)+1;
$c4=int($c4*$wariai)+1;
$c5=int($c5*$wariai)+1;
$c6=int($c6*$wariai)+1;
}
else{$senzai = "今が一番の成長期なのかも。<br>";}}
elsif($c0+$c1+$c2+$c3+$c4+$c5+$c6 > $cmax){
$wariai=$cmax/($c0+$c1+$c2+$c3+$c4+$c5+$c6);
$c0=int($c0*$wariai)+1;
$c1=int($c1*$wariai)+1;
$c2=int($c2*$wariai)+1;
$c3=int($c3*$wariai)+1;
$c4=int($c4*$wariai)+1;
$c5=int($c5*$wariai)+1;
$c6=int($c6*$wariai)+1;
$senzai = "訓練だけでは今の$cnameの能\力の限界になってきているのかも･･･。<br>レースで潜在能\力を引き出さないと････。<br>";}

	&farm_choco_regist;
	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&unlock($lock_file,'CHC');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print "<h1><center><font  color=\"blue\">★☆　（$subject)　☆★</font><br>
特訓開始！</center></h1><hr size=0><p>\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}

	print "<font size =3><center><b>$cnameは、$success回成功した。<br>$agari<br> $senzai $genkai $rousui</b></center></font><hr size=0>\n";

	print <<"EOM";
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value='$new_chara'>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場に戻る">
</form>
EOM

	&choco_footer;

	exit;
}
