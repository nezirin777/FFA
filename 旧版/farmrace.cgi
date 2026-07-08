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
$backgif = $crace_back;
$midi = $crace_midi;
$style_sheet = $chococss;
#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
&chocobattle;
exit;

#--------------#
#  レース画面  #
#--------------#
sub chocobattle {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&lock($lock_file,'CHC');
	&farm_choco_read;

	if (!$cname) {&error('チョコボがいません。');}
	if($clife < 400) { &error("チョコボが弱っています。レースはできません。");}

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$chara[27] = time();
	$vtime = $b_time - $ltime;
	$success = 0;
	$lose = 0;
	$turn=20;

	$lock_file = "$lockfolder/fwm.lock";
	&unlock($lock_file,'FWM');
	&read_farm_winner;

	if($wcid eq $chara[0] && $wcname eq "$cname") { &error("現在チョコボキングなのでレースはできません。"); }

	if(!($cname) || ($cname eq "ここに名前を入力")){&error('チョコボに名前がついていません！');}

	if($vtime > 0){
		if($ltime < $b_time) { &error("あと$vtime秒レースはできません。"); }
	}

	@type = ('逃げ','先行','普通','差し','追込','自在');
	$waza = $type[$ctype];
	$wwaza = $type[$wctype];

	$kdedasi = 0;
	$wdedasi = 0;
	$khp_flg = $c1;
	$whp_flg = $wc1;
	$heri = ($c2 + $wc2)/4000;
	$nebari = int(($c2 + $wc2)/2);
	$kisyou = int(($c3 + $wc3)/2);
	$seriai = int(($c4 + $wc4)/2);
	$tiryoku = int(($c5 + $wc5)/2);
	$tyousei = 2000 / ($c0 + $wc0);
	$kinryoku = int(($c0 + $wc0)/2);
	$knokori = 2400;
	$wnokori = 2400;
	$lastspart = int((($c0 + $wc0)/3 + ($c6 + $wc6))/60);
	$syasin = 0;
	$comment = "";
	$gold = 0;
	$nuki = 0;
	$knear = 0;
	$wnear = 0;
	$hikihanasi = 0;


	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {

			$kdmg = 0;
			$wdmg = 0;
			$com1 = "";
			$com2 = "";
			$mybar = int(($knokori /2400 ) * 100);
			$myb2 = 100 - $mybar + 1;
			$enbar = int(($wnokori /2400 ) * 100);
			$enb2 = 100 - $enbar + 1;
			$joutai = "";
			$wjoutai = "";
			$com = "";
			$dmg1="";
			$dmg2="";
			$sinkou = "";
			$after = "";


if($khp_flg/$c1 >= 0.8){$joutai = "元気モリモリ";}
elsif($khp_flg/$c1 >= 0.6){$joutai = "普通";}
elsif($khp_flg/$c1 >= 0.4){$joutai = "バテ気味";}
elsif($khp_flg/$c1 >= 0.2){$joutai = "バテバテ";}
elsif($khp_flg/$c1 >= 0){$joutai = "倒れる寸前";}
elsif($khp_flg/$c1 < 0){$joutai = "残るは気力のみ";}
if($whp_flg/$wc1 >= 0.8){$wjoutai = "元気モリモリ";}
elsif($whp_flg/$wc1 >= 0.6){$wjoutai = "普通";}
elsif($whp_flg/$wc1 >= 0.4){$wjoutai = "バテ気味";}
elsif($whp_flg/$wc1 >= 0.2){$wjoutai = "バテバテ";}
elsif($whp_flg/$wc1 >= 0){$wjoutai = "倒れる寸前";}
elsif($whp_flg/$wc1 < 0){$wjoutai = "残るは気力のみ";}



		if($i == 1){
if(rand($kisyou) <= rand($c3*2/3)){
$kdedasi = int(rand($c0/($tyousei*4))+$c0/($tyousei*4));
$com1 .= "<font size = 3 color = red>$cnameは出遅れてしまった！</font>";
$ksyoumou = $heri * $kdedasi * 3 * ($kisyou / $c3) * ($c2 / $nebari);}
elsif(rand($tiryoku) <= rand($c5*2/3)){
$kdedasi = int(rand($c0*0.75/$tyousei) + $c0*0.75/$tyousei);
$com1 .= "<font size = 3 color = red>$cnameは絶好のスタートを切った！</font>";
$ksyoumou = $heri * ($kdedasi / 2) * ($kisyou / $c3) * ($c2 / $nebari);}
else{$kdedasi = int(rand($c0/($tyousei*2)) + $c0/($tyousei*2));
$com1 .= "<font size = 3 color = red>$cnameはスタートを切った！</font>";
$ksyoumou = $heri * $kdedasi * ($kisyou / $c3) * ($c2 / $nebari);}
if(rand($kisyou) <= rand($wc3*2/3)){
$wdedasi = int(rand($wc0/($tyousei*4)) + $wc0/($tyousei*4));
$com2 .= "<font size = 3 color = red>$wcnameは出遅れてしまった！</font>";
$wsyoumou = $heri * $wdedasi * 3 * ($kisyou / $wc3) * ($wc2 / $nebari);}
elsif(rand($tiryoku) <= rand($wc5*2/3)){
$wdedasi = int(rand($wc0*0.75/$tyousei) + $wc0*0.75/$tyousei);
$com2 .= "<font size = 3 color = red>$wcnameは絶好のスタートを切った！</font>";
$wsyoumou = $heri * $wdedasi / 2 * ($kisyou / $wc3) * ($wc2 / $nebari);}
else{$wdedasi = int(rand($wc0/($tyousei*2)) + $wc0/($tyousei*2));
$com2 .= "<font size = 3 color = red>$wcnameはスタートを切った！</font>";
$wsyoumou = $heri * $wdedasi * ($kisyou / $wc3) * ($wc2 / $nebari);}
$dmg1 .= $kdedasi;
$dmg2 .= $wdedasi;
$ksyoumou = $ksyoumou / 2;
$wsyoumou = $wsyoumou / 2;
$knokori = 2400 - $kdedasi;
$wnokori = 2400 - $wdedasi;
$sinkou = "チョコ進んだ！";
if($kdedasi > $wdedasi){$after = "挑戦者<font color = #ff00cc>$cname</font>がいいスタートを切った！このままつっきるのか？！";}
elsif($kdedasi == $wdedasi){$after = "同時スタート！！波乱の幕開けか？！";}
else{$after = "王者<font color = #ff00cc>$wcname</font>がいいスタートを切った！このままつっきるのか？！";}}

elsif($i == 2){
$keii = int(rand($c0/4)) + int($c0*3/4) - $kinryoku + $kdedasi;
$knokori = 1000 - $keii;
if($knokori < 400){$knokori = 400;}
$wkeii = int(rand($wc0/4)) + int($wc0*3/4) - $kinryoku + $wdedasi;
$wnokori = 1000 - $wkeii;
if($wnokori < 400){$wnokori = 400;}

if(rand($kisyou) <= rand($c3*1/4)){
$ksyoumou = $heri * (1400 + $keii - $kdedasi) * 3 * ($kisyou / $c3) * ($c2 / $nebari);
$com1 = "<font size = 3 color = yellow>$cnameは息をあらたげて走ってきた！</font>";$knokori = int($knokori * 9/10);}
elsif(rand($tiryoku) <= rand($c5*1/3)){
$ksyoumou = ($heri * (1400 + $keii - $kdedasi) * ($kisyou / $c3) * ($c2 / $nebari) )/ 2;
$com1 = "<font size = 3 color = yellow>$cnameは足場が楽なコースを走ってきた！</font>";}
else{$ksyoumou = $heri * (1400 + $keii - $kdedasi) * ($kisyou / $c3) * ($c2 / $nebari);
$com1 = "<font size = 3 color = yellow>$cnameはいつも通りに走った！</font>";}
if(rand($kisyou) <= rand($wc3*1/4)){
$wsyoumou = $heri * (1400 + $wkeii - $wdedasi) * 3 * ($kisyou / $wc3) * ($wc2 / $nebari);
$com2 = "<font size = 3 color = yellow>$wcnameは息をあらたげて走ってきた！</font>";$wnokori = int($wnokori * 9/10);}
elsif(rand($tiryoku) <= rand($wc5*1/3)){
$wsyoumou = ($heri * (1400 + $wkeii - $wdedasi) * ($kisyou / $wc3) * ($wc2 / $nebari) )/ 2;
$com2 = "<font size = 3 color = yellow>$wcnameは足場が楽なコースを走ってきた！</font>";}
else{$wsyoumou = $heri * (1400 + $wkeii - $wdedasi) * ($kisyou / $wc3) * ($wc2 / $nebari);
$com2 = "<font size = 3 color = yellow>$wcnameはいつも通りに走った！</font>";}
$dmg1 .= "残り$knokoriチョコ！";
$dmg2 .= "残り$wnokoriチョコ！";
$ksyoumou = $ksyoumou * 3 / 4;
$wsyoumou = $wsyoumou * 3 / 4;
if($wnokori > $knokori*2){$after = "挑戦者<font color = #ff00cc>$cname</font>は大きく<font color = #ff00cc>$wcname</font>を引き離した！！このまま最後まで逃げ切ってしまうのか！？<br>大きく離れたまま、挑戦者<font color = #ff00cc>$cname</font>が最後の直線に向かいます！<br>王者<font color = #ff00cc>$wcname</font>は追いきれるだろうか！！";}
elsif($knokori > $wnokori*2){$after = "王者<font color = #ff00cc>$wcname</font>は大きく<font color = #ff00cc>$cname</font>を引き離した！！このまま最後まで逃げ切ってしまうのか！？<br>大きく離れたまま、王者<font color = #ff00cc>$wcname</font>が最後の直線に向かいます！<br>挑戦者<font color = #ff00cc>$cname</font>は追いきれるだろうか！！";}
elsif($wnokori > $knokori*1.5){$after = "挑戦者<font color = #ff00cc>$cname</font>はかなり前に進んでいるぞ！このまま逃げ切ってしまうのか！？<br>挑戦者<font color = #ff00cc>$cname</font>が先に最後の直線に向かいます！<br>王者<font color = #ff00cc>$wcname</font>はこれを差しきれるか！？";}
elsif($knokori > $wnokori*1.5){$after = "王者<font color = #ff00cc>$wcname</font>はかなり前に進んでいるぞ！このまま逃げ切ってしまうのか！？<br>王者<font color = #ff00cc>$wcname</font>が先に最後の直線に向かいます！<br>挑戦者<font color = #ff00cc>$cname</font>はこれを差しきれるか！？";}
elsif($wnokori > $knokori*1.2){$after = "挑戦者<font color = #ff00cc>$cname</font>は相当進んでいるぞ！<br>王者<font color = #ff00cc>$wcname</font>は差しきれるか！？<br>挑戦者<font color = #ff00cc>$cname</font>が先に最後の直線に向かいます！";}
elsif($knokori > $wnokori*1.2){$after = "王者<font color = #ff00cc>$wcname</font>は相当進んでいるぞ！<br>挑戦者<font color = #ff00cc>$cname</font>は差しきれるか！？<br>王者<font color = #ff00cc>$wcname</font>が先に最後の直線に向かいます！";}
elsif($wnokori > $knokori){$after = "挑戦者<font color = #ff00cc>$cname</font>と王者<font color = #ff00cc>$wcname</font>の差はほとんどない！<br>最後の直線に勝負がかけられます！<br>両者が一緒になって最終コーナーを回った！";}
elsif($knokori > $wnokori){$after = "王者<font color = #ff00cc>$wcname</font>と挑戦者<font color = #ff00cc>$cname</font>の差はほとんどない！<br>最後の直線に勝負がかけられます！<br>両者が一緒になって最終コーナーを回ります！";}
elsif($knokori == $wnokori){$after = "王者<font color = #ff00cc>$wcname</font>と挑戦者<font color = #ff00cc>$cname</font>は同時に最終コーナーを回った！<br>名勝負が目の前で繰り広げられています！<br>誰がこんな展開を予\想したでしょうか？！";}
}
else{
$kdmg = (rand($c0) + rand($c6) + rand($c6) + rand($c6))/$lastspart;
$wdmg = (rand($wc0) + rand($wc6) + rand($wc6) + rand($wc6))/$lastspart;
$kdmg2 = $kdmg;
$wdmg2 = $wdmg;
if($khp_flg <= 0){
if(rand($nebari) < rand($c2)){$kdmg = $kdmg * 1.5;
$com1 .= "<font size = 3 color = red>$cnameが底力を見せる！！</font>";}
else{$kdmg = $kdmg / 3;$com1 .= "<font size = 3 color = red>$cnameはもうバテてきている！</font>";}}
elsif(rand($seriai) < rand($c4*1.5) || ($khp_flg/$c1 >= 0.4)){$ksyoumou = $ksyoumou * 2;$kdmg = $kdmg * 2.5;$com1 .= "<font size = 3 color = red>$cnameがラストスパート！！</font>";}

if($whp_flg <= 0){
if(rand($nebari) < rand($wc2)){$wdmg = $wdmg * 1.5;
$com2 .= "<font size = 3 color = red>$wcnameが底力を見せる！！</font>";}
else{$wdmg = $wdmg / 3;$com2 .= "<font size = 3 color = red>$wcnameはもうバテてきている！</font>";}}
elsif(rand($seriai) < rand($wc4*1.5) || ($whp_flg/$wc1 > 0.5)){$wsyoumou = $wsyoumou * 2;$wdmg = $wdmg * 2.5;$com2 .= "<font size = 3 color = red>$wcnameがラストスパート！！</font>";}

$kdmg = int($kdmg);
$wdmg = int($wdmg);
$ksyoumou = $heri * $kdmg2 * ($kisyou / $c3) * ($c2 / $nebari);
$wsyoumou = $heri * $wdmg2 * ($kisyou / $wc3) * ($wc2 / $nebari);
$dmg1 .= $kdmg;
$dmg2 .= $wdmg;
$sinkou = "チョコ進んだ！";
$after = "";


if($knokori < $wnokori){
if($knokori - $kdmg > $wnokori - $wdmg){if($nuki){$after = "<font color = #ff00cc>$wcname</font>が<font color = #ff00cc>$cname</font>を抜き返した！";$nuki += 1;}else{$after = "<font color = #ff00cc>$wcname</font>が<font color = #ff00cc>$cname</font>を抜いたぁ！";$nuki = 1;}}
elsif(!$nuki && !$knear){
if($wnokori - $knokori - $wdmg + $kdmg > 600){$after ="<font color = #ff00cc>$cname</font>！強い強い！ぶっちぎりだぁぁ！！";}
elsif($wnokori - $knokori - $wdmg + $kdmg > 400){$after ="<font color = #ff00cc>$cname</font>！逃げる逃げる！このまま逃げ切りか？！";}
elsif($wnokori - $knokori - $wdmg + $kdmg > 200){$after ="<font color = #ff00cc>$wcname</font>が少しずつ近づいてきている！";}
elsif($wnokori - $knokori - $wdmg + $kdmg > 100){$after ="<font color = #ff00cc>$wcname</font>が近づいてきている！";$knear = 1;}
else{$after = "<font color = #ff00cc>$wcname</font>がじりじり近づいてきた！！";$knear = 1;}
}#抜く前～近づく
elsif($knear){
if($wnokori - $knokori - $wdmg + $kdmg > 500 && $hikihanasi){$after = "<font color = #ff00cc>$cname</font>が完全にぶっちぎる！！強すぎる！！！各の違いを見せつけた！";}
elsif($wnokori - $knokori - $wdmg + $kdmg > 250 && $hikihanasi){$after = "<font color = #ff00cc>$cname</font>が<font color = #ff00cc>$wcname</font>をどんどん引き離していく！！";}
elsif($wnokori - $knokori - $wdmg + $kdmg > 100 && $hikihanasi){$after = "<font color = #ff00cc>$cname</font>がそのままいってしまうのか？！";}
elsif($hikihanasi){$after = "<font color = #ff00cc>$wcname</font>がもう一度差を詰める！";}
elsif($wnokori - $knokori - $wdmg + $kdmg > 100 && !$hikihanasi){$after = "<font color = #ff00cc>$cname</font>が<font color = #ff00cc>$wcname</font>を引き離す！！";$hikihanasi = 1;}
else{$after = "<font color = #ff00cc>$cname</font>が粘っている！";}
}#近づく～引き離し
else{
if($wnokori - $knokori - $wdmg + $kdmg > 100){$after = "<font color = #ff00cc>$cname</font>が一気に引き離した！！";$knear=1;}
else{$after = "<font color = #ff00cc>$cname</font>が粘る！！";$knear=1;}
}#抜いて、距離が近い
}#挑戦者が前

elsif($wnokori < $knokori){
if($wnokori - $wdmg > $knokori - $kdmg){if($nuki){$after = "<font color = #ff00cc>$cname</font>が<font color = #ff00cc>$wcname</font>を抜き返した！";$nuki += 1;}else{$after = "<font color = #ff00cc>$cname</font>が<font color = #ff00cc>$wcname</font>を抜いたぁ！";$nuki = 1;}}
elsif(!$nuki && !$wnear){
if($knokori - $wnokori - $kdmg + $wdmg > 600){$after ="<font color = #ff00cc>$wcname</font>！強い強い！ぶっちぎりだぁぁ！！";}
elsif($knokori - $wnokori - $kdmg + $wdmg > 400){$after ="<font color = #ff00cc>$wcname</font>！逃げる逃げる！このまま逃げ切りか？！";}
elsif($knokori - $wnokori - $kdmg + $wdmg > 200){$after ="<font color = #ff00cc>$cname</font>が少しずつ近づいてきている！";}
elsif($knokori - $wnokori - $kdmg + $wdmg > 100){$after ="<font color = #ff00cc>$cname</font>が近づいてきている！";$wnear = 1;}
else{$after = "<font color = #ff00cc>$cname</font>がじりじり近づいてきた！！";$wnear = 1;}
}#抜く前～近づく
elsif($wnear){
if($knokori - $wnokori - $kdmg + $wdmg > 500 && $hikihanasi){$after = "<font color = #ff00cc>$wcname</font>が完全にぶっちぎる！！強すぎる！！！各の違いを見せつけた！";}
elsif($knokori - $wnokori - $kdmg + $wdmg > 250 && $hikihanasi){$after = "<font color = #ff00cc>$wcname</font>が<font color = #ff00cc>$cname</font>をどんどん引き離していく！！";}
elsif($knokori - $wnokori - $kdmg + $wdmg > 100 && $hikihanasi){$after = "<font color = #ff00cc>$wcname</font>がそのままいってしまうのか？！";}
elsif($hikihanasi){$after = "<font color = #ff00cc>$cname</font>がもう一度差を詰める！";}
elsif($knokori - $wnokori - $kdmg + $wdmg > 100 && !$hikihanasi){$after = "<font color = #ff00cc>$wcname</font>が<font color = #ff00cc>$cname</font>を引き離す！！";$hikihanasi = 1;}
else{$after = "<font color = #ff00cc>$wcname</font>が粘っている！";}
}#近づく～引き離し
else{
if($knokori - $wnokori - $kdmg + $wdmg > 100){$after = "<font color = #ff00cc>$wcname</font>が一気に引き離した！！";$wnear=1;}
else{$after = "<font color = #ff00cc>$wcname</font>が粘る！！";$wnear=1;}
}#抜いて、距離が近い
}#王者が前
else{$after = "これはすごいレースだ！！両者並んだぁぁぁ！！！";}
if($nuki >= 5){$after .="<br>激しいデッドヒートだ！勝つのはいったいどっちだ？！";}
}


if($i == 1){$com = "<font size = 5 color = blue><b>チョコボキングを決定するキングレース、今、スタートしました！</b></font>";}
elsif($i == 2){$com = "<font size = 5 color = blue><b>各チョコボ、道中、どんな展開が待ち受けているのか？！</b></font>";}
elsif($i==3){$com = "<font size = 5 color = blue><b>各チョコボが一斉にラストスパートに向かいます！</b></font>";}
else{$com = "<font size = 5 color = blue><b>最後の直線！！一番にゴールをするのはどのチョコボか？！</b></font>";
if($khp_flg > 0 && 0 > $khp_flg - $ksyoumou){$com .= "<br><font color = white size =3>$cnameのスタミナが切れた！あとは気力で進むのみ！</font>";}
if($whp_flg > 0 && 0 > $whp_flg - $wsyoumou){$com .= "<br><font color = white size =3>$wcnameのスタミナが切れた！あとは気力で進むのみ！</font>";}
}

$khp_flg -= $ksyoumou;
$whp_flg -= $wsyoumou;


		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0 align = "center">
<TR>
	<TD ALIGN="center">
	<IMG SRC="$img_farm/$choco_img[$cno]" width=60 height=60><table width="100%" border=1>
</table>
	</TD>
	<TD>
	</TD>
	<TD ALIGN="center">
	<IMG SRC="$img_farm/$choco_img[$wcno]" width=60 height=60><table width="100%" border=1>
</table></TD>
	</TR>
<TR>
<TD>
<TABLE BORDER=0 align = "center">
<TR>
	<TD CLASS="b1"id="td2">
	ブリーダー
	</TD>
	<TD CLASS="b1"id="td2">
	なまえ
	</TD>
	<TD CLASS="b1"id="td2">
	状態
	</TD>
	<TD CLASS="b1"id="td2">
	タイプ
	</TD>
	<TD CLASS="b1"id="td2" align="center">
	残りチョコ
	</TD>
</TR>
<TR>
	<TD CLASS="b2">
	$chara[4]
	</TD>
	<TD CLASS="b2">
	$cname
	</TD>
	<TD CLASS="b2">
	$joutai
	</TD>
	<TD CLASS="b2">
	$waza
	</TD>
	<TD CLASS="b2">
	$knokori/2400<BR>
	<IMG SRC="$img_farm/mrk.gif" WIDTH=$mybar HEIGHT=5 ALIGN=top><IMG SRC="$img_farm/mrk_r.gif" WIDTH=$myb2 HEIGHT=5 ALIGN=top>
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT SIZE=5 COLOR="$red">VS</FONT>
</TD>
<TD>
<TABLE BORDER=0 align = "center">
<TR>
	<TD CLASS="b1"id="td2">
	ブリーダー
	</TD>
	<TD CLASS="b1"id="td2">
	なまえ
	</TD>
	<TD CLASS="b1"id="td2">
	状態
	</TD>
	<TD CLASS="b1"id="td2">
	タイプ
	</TD>
	<TD CLASS="b1"id="td2" align="center">
	残りチョコ
	</TD>
</TR>
<TR>
	<TD CLASS="b2">
	$wcbreader
	</TD>
	<TD CLASS="b2">
	$wcname
	</TD>
	<TD CLASS="b2">
	$wjoutai
	</TD>
	<TD CLASS="b2">
	$wwaza
	</TD>
	<TD CLASS="b2">
	$wnokori/2400<BR>
        <IMG SRC="$img_farm/mrk.gif" WIDTH=$enbar HEIGHT=5 ALIGN=top><IMG SRC="$img_farm/mrk_r.gif" WIDTH=$enb2 HEIGHT=5 ALIGN=top>
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>
<TABLE width=100% bgcolor=0000FF><TBODY><TR><TD width=10 bgcolor=#99CCFF><img src=\"$img_farm/ana.gif\"></TD><TD width=100% bgcolor=#000000>
<font size="3" color="#FFFFFF">
$com<br>
$com1 $cnameは<font class="dmg"><b>$dmg1</b></font>$sinkou<br>
$com2 $wcnameは<font class="dmg"><b>$dmg2</b></font>$sinkou</font><br>
<font color = pink size = 4><b>$after</b></font><br></TD></TR></TBODY></TABLE><P>
EOM

$knokori -= $kdmg;
$wnokori -= $wdmg;


if($knokori < 0 && $wnokori < 0){$syasin = 1;last;}
elsif($knokori < 0){$win = 1;$comment = "<font size=7>$cnameが先にゴール！！！！<br><br></font>";last;}
elsif($wnokori < 0){$win = 0;$comment = "<font size=7>$wcnameが先にゴール！！！！<br><br></font>";last;}

		$i++;
		$j++;

	}

	if($syasin){
		$comment = "<b><font size=6>同時にゴール！！！結果は写真判定にゆだねられます！<br>審議の結果は・・・・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br></font></b>";
		if(rand($c0) > rand($wc0)){$win = 1;}
		else{$win = 0;}
		}

	if($win) {
		$crun += 1;
		$cwin += 1;

		@new_winner=();
		unshift(@new_winner,"$cid<>$cpass<>$cbreader<>$chara[2]<>$chara[3]<>$cname<>$cno<>$ctype<>$crun<>$cwin<>$cmax<>$c0<>$c1<>$c2<>$c3<>$c4<>$c5<>$c6<>1<>$wcname<>$wcsite<>$wcurl<>$wcbreader<>$cfather<>$cmother<>\n");

		$cmax += 80;
		$c0 += int(rand(6))+1;
		$c1 += int(rand(6))+1;
		$c2 += int(rand(6))+1;
		$c3 += int(rand(6))+1;
		$c4 += int(rand(6))+1;
		$c5 += int(rand(6))+1;
		$c6 += int(rand(6))+1;
		$gold = $wcmax * $wcren * 10000;
		$comment .= "<b><font size=5>勝ったのは$cname！！</font></b><p><b><font size=5 color=\"#ff0000\">$chara[4]「よくやった$cname！」</font></b><p><b><font size=5 color=\"#0000ff\">$cname「クエ～♪」<br>$cnameは一段と成長した！！！</font></b><p>";


	}else{

		$wcren += 1;

		@new_winner=();
		unshift(@new_winner,"$wcid<>$wcpass<>$wcbreader<>$wcsite<>$wcurl<>$wcname<>$wcno<>$wctype<>$wcrun<>$wcwin<>$wcmax<>$wc0<>$wc1<>$wc2<>$wc3<>$wc4<>$wc5<>$wc6<>$wcren<>$cname<>$chara[2]<>$chara[3]<>$chara[4]<>$wcfather<>$wcmother<>\n");

		$crun += 1;
		$cmax += 20;
		$c0 += int(rand(1))+1;
		$c1 += int(rand(1))+1;
		$c2 += int(rand(1))+1;
		$c3 += int(rand(1))+1;
		$c4 += int(rand(1))+1;
		$c5 += int(rand(1))+1;
		$c6 += int(rand(1))+1;
		$gold = int($wcmax * $wcren / 1000);
		$comment .= "<b><font size=5>勝ったのは$wcname！！</font></b><p><b><font size=5 color=\"#0000ff\">$chara[4]「$cname～～（T_T）」</font></b><p><b><font size=5 color=\"#ff0000\">$cname「クエエエ・・・」<br>$wcbreaderの$wcnameは$wcren連勝！</font></b><br>$cnameはほんのちょっぴり成長した<p>";
	}

if($ctrain + $crun > 1000){$cmaxmax = int($cmaxmax * 0.99);$rousui = "もう、これ以上$cnameを酷使するのは可哀想な気がする･･･。これまですごくよくしてくれたと思うよ。そろそろ引退の時期なんじゃないかな･･･？";}

if($c0 > $cmax0){$genkai = "筋力の限界に達したようだ<br>";$c0 = $cmax0;}
if($c1 > $cmax1){$genkai .= "体力の限界に達したようだ<br>";$c1 = $cmax1;}
if($c2 > $cmax2){$genkai .= "我慢強さの限界に達したようだ<br>";$c2 = $cmax2;}
if($c3 > $cmax3){$genkai .= "落ち着きの限界に達したようだ<br>";$c3 = $cmax3;}
if($c4 > $cmax4){$genkai .= "闘争心の限界に達したようだ<br>";$c4 = $cmax4;}
if($c5 > $cmax5){$genkai .= "賢さの限界に達したようだ<br>";$c5 = $cmax5;}
if($c6 > $cmax6){$genkai .= "反射神経の限界に達したようだ<br>";$c6 = $cmax6;}


$clife -= 200;

if($cmax > $cmaxmax){
$cmax = $cmaxmax;
if($c0+$c1+$c2+$c3+$c4+$c5+$c6 > $cmax){$senzai = "もう$cnameの能\力の限界に達してしまったように見える･･･。これ以上の成長は見込めなさそうだ･･･。<br>";
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
$senzai = "今の$cnameの能\力の限界になってきているのかも･･･。潜在能\力を引き出さないといけなさそうだ･･･。<br>";}

       $chara[19] = $chara[19] + $gold;
       $cgold = $cgold + $gold/100;

	&farm_choco_regist;
	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&unlock($lock_file,'CHC');

	open(OUT,">./farmwinner.cgi");
	print OUT @new_winner;
	close(OUT);
	$lock_file = "$lockfolder/fwm.lock";
	&unlock($lock_file,'FWM');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print "<h1><center>サラブレッドチョコボキング決定戦！！！</h1><hr size=0><font color = black size = 5><b>サラブレッドチョコボの頂点を極めるチョコボたちの激しいレースが今日も開催されます。<br>どちらのチョコボが勝利するのでしょう？<br>やはりキングの$wcnameが王者の座を死守するのでしょうか？<br>もしくは、挑戦者の$cnameが王者の座をもぎ取るのか？！<br>注目のレース、今、発走です！</b></font></center><p>\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}

	print "<p>$comment<p>$chara[4]は、<b>$gold</b>G手に入れた。<p>$senzai $genkai $rousui\n";

	print <<"EOM";
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value='$new_chara'>
<input type=hidden name=mode value=log_in>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場に戻る">
</form>
EOM

	&choco_footer;

	exit;
}
