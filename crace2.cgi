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
#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

if($mente) {
	&error("現在バージョンアップ中です。しばらくお待ちください。");
}
&decode;
$ribal = "./denchoco.cgi";
$racename = "殿堂入りチョコボ戦";
&chocobattle;
exit;

#--------------#
#  レース画面  #
#--------------#
sub chocobattle {

	&read_cwinner;

	@type = ('逃げ','先行','普通','差し','追込','自在');
	$waza = $type[$ctype];

	for($i=1;$i<=4;$i++){
		$wwaza[$i] = $type[$wctype[$i]];
		$wdedasi[$i] = 0;
		$whp_flg[$i] = $wc1[$i];
		$wnokori[$i] = 2400;
		$wnear[$i] = 0;
	}

	$wdedasi[0] = 0;
	$khp_flg = $wc1[0];
	$heri = ($wc2[0] + $wc2[1] + $wc2[2] + $wc2[3] + $wc2[4] )/10000;
	$nebari = int(($wc2[0] + $wc2[1] + $wc2[2] + $wc2[3] + $wc2[4])/5);
	$kisyou = int(($wc3[0] + $wc3[1] + $wc3[2] + $wc3[3] + $wc3[4])/5);
	$seriai = int(($wc4[0] + $wc4[1] + $wc4[2] + $wc4[3] + $wc4[4])/5);
	$tiryoku = int(($wc5[0] + $wc5[1] + $wc5[2] + $wc5[3] + $wc5[4])/5);
	$tyousei = 5000 / ($wc0[0] + $wc0[1] + $wc0[2] + $wc0[3] + $wc0[4]);
	$kinryoku = int(($wc0[0] + $wc0[1] + $wc0[2] + $wc0[3] + $wc0[4])/5);
	$wnokori[0] = 2400;
	$lastspart = int((($wc0[0] + $wc0[1] + $wc0[2] + $wc0[3] + $wc0[4])/3 + ($wc6[0] + $wc6[1] + $wc6[2] + $wc6[3] + $wc6[4]))/150);
	$syasin = 0;
	$comment = "";
	$gold = 0;
	$nuki = 0;
	$near = 0;
	$hikihanasi = 0;
	$member = 5;

	@t_status = ('倒れる寸前','バテバテ','バテ気味','普通','元気モリモリ');

	$i=1;$j=0;@battle_date=();$java_com = "";
	foreach(1..$turn) {

		$kdmg[0] = 0;
		$com1 = "";
		$joutai = "";
		$com = "";
		$dmg[0]="";
		$sinkou = "";
		$after = "";
		@junni = ();
		@tmp=();
		@level = ();


		for($n=1;$n<=4;$n++){
			$wdmg[$n] = 0;
			$com2[$n] = "";
			$dmg[$n]="";
		}

		if($i == 1){
			if(rand($kisyou) <= rand($wc3[0]*2/3)){
				$wdedasi[0] = int(rand($wc0[0]/($tyousei*4))+$wc0[0]/($tyousei*4));
				$com1 .= "<font size = 3 color = red>$wcname[0]は出遅れてしまった！</font>";
				$ksyoumou = $heri * $wdedasi[0] * 3 * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari);
			} elsif (rand($tiryoku) <= rand($wc5[0]*2/3)) {
				$wdedasi[0] = int(rand($wc0[0]*1.5/$tyousei));
				$com1 .= "<font size = 3 color = red>$wcname[0]は絶好のスタートを切った！</font>";
				$ksyoumou = $heri * ($wdedasi[0] / 2) * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari);
			} else {
				$wdedasi[0] = int(rand($wc0[0]/($tyousei*2)) + $wc0[0]/($tyousei*2));
				$com1 .= "<font size = 3 color = red>$wcname[0]はスタートを切った！</font>";
				$ksyoumou = $heri * $wdedasi[0] * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari);
			}

			for($n=1;$n<=4;$n++){
				if(rand($kisyou) <= rand($wc3[$n]*2/3)){
				$wdedasi[$n] = int(rand($wc0[$n]/($tyousei*4)) + $wc0[$n]/($tyousei*4));
				$com2[$n] .= "<font size = 3 color = red>$wcname[$n]は出遅れてしまった！</font>";
				$wsyoumou[$n] = $heri * $wdedasi[$n] * 3 * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari);
				} elsif (rand($tiryoku) <= rand($wc5[$n]*2/3)) {
				$wdedasi[$n] = int(rand($wc0[$n]*1.5/$tyousei));
				$com2[$n] .= "<font size = 3 color = red>$wcname[$n]は絶好のスタートを切った！</font>";
				$wsyoumou[$n] = $heri * $wdedasi[$n] / 2 * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari);
				} else {
				$wdedasi[$n] = int(rand($wc0[$n]/($tyousei*2)) + $wc0[$n]/($tyousei*2));
				$com2[$n] .= "<font size = 3 color = red>$wcname[$n]はスタートを切った！</font>";
				$wsyoumou[$n] = $heri * $wdedasi[$n] * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari);
				}
				$dmg[$n] .= $wdedasi[$n];
				$wsyoumou[$n] = $wsyoumou[$n] / 2;
				$wnokori[$n] = 2400 - $wdedasi[$n];
			}

			$dmg[0] .= $wdedasi[0];
			$ksyoumou = $ksyoumou / 2;
			$wnokori[0] = 2400 - $wdedasi[0];
			$sinkou = "チョコ進んだ！";

			for($n=0;$n<=4;$n++){
				$wnoko[$n] = 2400 - $dmg[$n];
				unshift(@level,"$wcname[$n]<>$wnoko[$n]<>$n<>\n");
			}

			@tmp = map {(split /<>/)[1]} @level;
			@junni = @level[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

			$n=0;
			foreach(@junni){
				($jname[$n],$jnokori[$n],$iti)=split(/<>/);
				if ($n == 0) {$itii = $iti;}
				elsif ($n == 1) {$niii = $iti;}
				elsif ($n == 2) {$sanii = $iti;}
				elsif ($n == 3) {$yonii = $iti;}
				elsif ($n == 4) {$goii = $iti;last;}
				$n+=1;
			}

			$after = << "EOM";
スタートしました！<BR>
<font color=#FFFF33 size=4><b>$jname[0]</b></font>がいいスタートを切ったようだ！次に続くのは<font color=#FF0099 size=4><b>$jname[1]</b></font>その後ろに<font color=#339999 size=4><b>$jname[2]</b></font><br>さらに<font color=#6600FF size=4><b>$jname[3]</b></font>そして、最後に<font color=#FFFFFF size=4><b>$jname[4]</b></font>と続きます。<br>
さぁ、このレースの最後には何が待ち受けているのでしょうか？<BR>
EOM

			$after =~ s/\n//gi;
			$after =~ s/\r//gi;

			$java_com = << "EOM";
function move$i() {
	xPos1 = 2400;
	xPos2 = 2400;
	xPos3 = 2400;
	xPos4 = 2400;
	xPos5 = 2400;
	setTimeout("moveb$i()", 1500);
	document.all.comment3.innerHTML = '<font color=#FFFF33 size=6>さぁ、スタートしました！</font>';
}
function moveb$i() {
	xPos1 = parseInt(Layer1.style.left);
	xPos2 = parseInt(Layer2.style.left);
	xPos3 = parseInt(Layer3.style.left);
	xPos4 = parseInt(Layer4.style.left);
	xPos5 = parseInt(Layer5.style.left);
	xPos1 = xPos1 - ($wdedasi[0] * 9 / 360);
	xPos2 = xPos2 - ($wdedasi[1] * 9 / 360);
	xPos3 = xPos3 - ($wdedasi[2] * 9 / 360);
	xPos4 = xPos4 - ($wdedasi[3] * 9 / 360);
	xPos5 = xPos5 - ($wdedasi[4] * 9 / 360);
	Layer1.style.left = xPos1;
	Layer2.style.left = xPos2;
	Layer3.style.left = xPos3;
	Layer4.style.left = xPos4;
	Layer5.style.left = xPos5;
	turn++;
	if (turn == 14) {
		turn = 0;
		setTimeout("move2()", 150);
	} else {
	setTimeout("moveb$i()", 150);
	}
}
EOM

		} elsif ($i == 2) {
			$wkeii[0] = int(rand($wc0[0]/4)) + int($wc0[0]*3/4) - $kinryoku + $wdedasi[0];
			$wnokori[0] = 1000 - $wkeii[0];
			if($wnokori[0] < 400){ $wnokori[0] = 400; }
			for($n=1;$n<=4;$n++){
				$wkeii[$n] = int(rand($wc0[$n]/4)) + int($wc0[$n]*3/4) - $kinryoku + $wdedasi[$n];
				$wnokori[$n] = 1000 - $wkeii[$n];
				if($wnokori[$n] < 400){ $wnokori[$n] = 400; }
			}

			if (rand($kisyou) <= rand($wc3[0]*1/4)) {
				$ksyoumou = $heri * (1400 + $wkeii[0] - $wdedasi[0]) * 3 * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari);
				$com1 = "<font size = 3 color = yellow>$wcname[0]は息をあらたげて走ってきた！</font>";
				$wnokori[0] = int($wnokori[0] * 9/10);
			} elsif (rand($tiryoku) <= rand($wc5[0]*1/3)) {
				$ksyoumou = ($heri * (1400 + $wkeii[0] - $wdedasi[0]) * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari) )/ 2;
				$com1 = "<font size = 3 color = yellow>$wcname[0]は足場が楽なコースを走ってきた！</font>";
			} else {
				$ksyoumou = $heri * (1400 + $wkeii[0] - $wdedasi[0]) * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari);
				$com1 = "<font size = 3 color = yellow>$wcname[0]はいつも通りに走った！</font>";
			}

			for($n=1;$n<=4;$n++){
				if (rand($kisyou) <= rand($wc3[$n]*1/4)) {
				$wsyoumou[$n] = $heri * (1400 + $wkeii[$n] - $wdedasi[$n]) * 3 * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari);
				$com2[$n] = "<font size = 3 color = yellow>$wcname[$n]は息をあらたげて走ってきた！</font>";$wnokori[$n] = int($wnokori[$n] * 9/10);
				} elsif (rand($tiryoku) <= rand($wc5[$n]*1/3)) {
				$wsyoumou[$n] = ($heri * (1400 + $wkeii[$n] - $wdedasi[$n]) * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari) )/ 2;
				$com2[$n] = "<font size = 3 color = yellow>$wcname[$n]は足場が楽なコースを走ってきた！</font>";
				} else {
				$wsyoumou[$n] = $heri * (1400 + $wkeii[$n] - $wdedasi[$n]) * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari);
				$com2[$n] = "<font size = 3 color = yellow>$wcname[$n]はいつも通りに走った！</font>";
				}
				$dmg[$n] .= "残り$wnokori[$n]チョコ！";
				$wsyoumou[$n] = $wsyoumou[$n] * 3 / 4;
			}

			$dmg[0] .= "残り$wnokori[0]チョコ！";
			$ksyoumou = $ksyoumou * 3 / 4;

			for ($n=0;$n<=4;$n++) {
				$wnoko[$n] = $wnokori[$n] - $dmg[$n];
				unshift(@level,"$wcname[$n]<>$wnoko[$n]<>$n<>\n");
			}

			@tmp = map {(split /<>/)[1]} @level;
			@junni = @level[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

			$n=0;
			foreach(@junni){
				($jname[$n],$jnokori[$n],$iti)=split(/<>/);
				if($n == 0){$itii = $iti;}
				elsif($n == 1){$niii = $iti;}
				elsif($n == 2){$sanii = $iti;}
				elsif($n == 3){$yonii = $iti;}
				else{$goii = $iti;last;}
				$n+=1;
			}

			if($jnokori[4] < $jnokori[0] + 200){
				$after = "大混戦！！団子状態のまま各チョコボ一斉にコーナーを回ります。<br>いったいどのチョコボが勝利を手にするのでしょうか？！";
				$dango=1;
			} elsif ($jnokori[3] < $jnokori[0] + 200 && $jnokori[4] > $jnokori[3] + 200) {
				$after = "$jname[4]が大きく後方に残されている！<br>前４羽は揃って直線に向かった！$jname[4]は直線でレースに加わってこれるだろうか？！";
				$dango=1;
			} elsif (!$dango) {
				if ($jnokori[1] > $jnokori[0] + 500) {
				$after = "<font color = #ff00cc>$jname[0]</font>の一人旅！！このまま最後まで逃げ切ってしまうのか！？<br>大きく後方離したまま、<font color = #ff00cc>$jname[0]</font>が最後の直線に向かいます！";
				$hitoributai=1;
				} elsif($jnokori[1] > $jnokori[0] + 300) {
				$after = "<font color = #ff00cc>$jname[0]</font>はかなり前方に進んでいる！このまま逃げ切ってしまうのか！？<br><font color = #ff00cc>$jname[0]</font>が最後の直線に向かいます！";
				$hitoributai=1;
				} elsif ($jnokori[1] > $jnokori[0] + 150) {
				$after = "<font color = #ff00cc>$jname[0]</font>が相当進んでいるぞ！<br><font color = #ff00cc>$jname[0]</font>を先頭に集団は最後の直線に向かいます！";
				$hitoributai=1;
				} elsif (!$hitoritabi) {
				if ($jnokori[2] > $jnokori[1] + 300) {
					if ($jnokori[1] > $jnokori[0] + 100) {
						$after .= "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>の差はほとんどない！<br>最後の直線に勝負がかけられます！<br>両者が一緒になって最終コーナーを回ります！<br>この２羽だけの戦いになるのか！";
					} elsif ($jnokori[1] > $jnokori[0] + 20) {
						$after .= "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>はほぼ同時に最終コーナーを回ります！<br>名勝負が目の前で繰り広げられています！<br>誰がこんな展開を予\想したでしょうか？！<br>はたまた、後方集団から誰かが抜け出してくるのでしょうか？！";
					} else {
						$after .= "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>の激しいデッドヒート！！<br>この勝負の行方はいったいどうなるのでしょうか？！<br>さぁ、両者が最終コーナーを回って最後の直線に向かいます！！<br>後方集団はこの二羽の戦いに加われるでしょうか？！";
					}
				} elsif($jnokori[2] > $jnokori[1] + 150) {
					if ($jnokori[1] > $jnokori[0] + 100) {
						$after = "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>の差はほとんどない！<br>最後の直線に勝負がかけられます！<br>両者が一緒になって最終コーナーを回ります！<br>後方集団はこの２羽に追いつくことができるのだろうか？！";
					} elsif ($jnokori[1] > $jnokori[0] + 20) {
						$after = "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>はほぼ同時に最終コーナーを回ります！<br>名勝負が目の前で繰り広げられています！<br>誰がこんな展開を予\想したでしょうか？！<br>はたまた、後方集団から誰かが抜け出してくるのでしょうか？！";
					} else {
						$after = "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>の激しいデッドヒート！！<br>この勝負の行方はいったいどうなるのでしょうか？！<br>さぁ、両者が最終コーナーを回って最後の直線に向かいます！！<br>後方集団はこの二羽の戦いに加われるでしょうか？！";
					}
				} else {
					if ($jnokori[1] > $jnokori[0] + 100) {
						$after = "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>と<font color = #ff00cc>$jname[2]</font>の差はほとんどない！<br>最後の直線に勝負がかけられます！<br>３羽が一緒になって最終コーナーを回ります！<br>後方集団はこの３羽に追いつくことができるのだろうか？！";
					} elsif ($jnokori[1] > $jnokori[0] + 50) {
						$after = "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>と<font color = #ff00cc>$jname[2]</font>はほぼ同時に最終コーナーを回ります！<br>名勝負が目の前で繰り広げられています！<br>誰がこんな展開を予\想したでしょうか？！<br>はたまた、後方集団から誰かが抜け出してくるのでしょうか？！<br>勝負の最後の直線に入ります！！！";
					} else {
						$after = "<font color = #ff00cc>$jname[0]</font>と<font color = #ff00cc>$jname[1]</font>と<font color = #ff00cc>$jname[2]</font>の激しいデッドヒート！！<br>この勝負の行方はいったいどうなるのでしょうか？！<br>まれに見る大激戦！！！<br>さぁ、両者が最終コーナーを回って最後の直線に向かいます！！<br>後方集団はこの３羽の戦いに加われるでしょうか？！";
					}
				}
				}
			}

			$after .="<br><font color=#FFFF33 size=4><b>$jname[0]、</b><font color=#FF0099 size=4><b></font></b></font><font color=#339999 size=4><b>$jname[1]、</b></font><font color=#FF0099 size=4><b>$jname[2]、</b></font><font color=#6600FF size=4><b>$jname[3]、</b></font><font color=#FFFFFF size=4><b>$jname[4]</b></font>の順でコーナーを抜けたぁぁ！";

			$java_com .= << "EOM";
function move2() {
	Layer1.style.left = $iti[0];
	Layer2.style.left = $iti[1];
	Layer3.style.left = $iti[2];
	Layer4.style.left = $iti[3];
	Layer5.style.left = $iti[4];
	document.all.comment3.innerHTML = "$next_com";
	document.all.joutai0.innerHTML = '<b>$wjoutai[0]</b>';
	document.all.joutai1.innerHTML = '<b>$wjoutai[1]</b>';
	document.all.joutai2.innerHTML = '<b>$wjoutai[2]</b>';
	document.all.joutai3.innerHTML = '<b>$wjoutai[3]</b>';
	document.all.joutai4.innerHTML = '<b>$wjoutai[4]</b>';
	setTimeout("moveb2()", 1500);
}
function moveb2() {
	xPos1 = parseInt(Layer1.style.left) - ((2400 - $wnokori[0] - $wdedasi[0]) * 9 / 600);
	xPos2 = parseInt(Layer2.style.left) - ((2400 - $wnokori[1] - $wdedasi[1]) * 9 / 600);
	xPos3 = parseInt(Layer3.style.left) - ((2400 - $wnokori[2] - $wdedasi[2]) * 9 / 600);
	xPos4 = parseInt(Layer4.style.left) - ((2400 - $wnokori[3] - $wdedasi[3]) * 9 / 600);
	xPos5 = parseInt(Layer5.style.left) - ((2400 - $wnokori[4] - $wdedasi[4]) * 9 / 600);
	Layer1.style.left = xPos1;
	Layer2.style.left = xPos2;
	Layer3.style.left = xPos3;
	Layer4.style.left = xPos4;
	Layer5.style.left = xPos5;
	turn++;
	if (turn == 24) {
		turn = 0;
		setTimeout("move3()", 150);
	} else {
	setTimeout("moveb2()", 150);
	}
}
EOM
		} else {
			for($n=1;$n<=4;$n++){
				$wdmg[$n] = (rand($wc0[$n]) + rand($wc6[$n]) + rand($wc6[$n]) + rand($wc6[$n]))/$lastspart;
				$wsyoumou[$n] = $heri * $wdmg[$n] * ($kisyou / $wc3[$n]) * ($wc2[$n] / $nebari);
			}
			$kdmg[0] = (rand($wc0[0]) + rand($wc6[0]) + rand($wc6[0]) + rand($wc6[0]))/$lastspart;
			$ksyoumou = $heri * $kdmg[0] * ($kisyou / $wc3[0]) * ($wc2[0] / $nebari);

			if($khp_flg <= 0){
				if(rand($nebari) < rand($wc2[0])){
				$kdmg[0] = $kdmg[0] * 1.5;
				$com1 .= "<font size = 3 color = red>$wcname[0]が底力を見せる！！</font>";
				} else {
				$kdmg[0] = $kdmg[0] / 3;$com1 .= "<font size = 3 color = red>$wcname[0]はもうバテてきている！</font>";
				}
			} elsif (rand($seriai) < rand($wc4[0]) || ($khp_flg/$wc1[0] >= 0.4)) {
				$ksyoumou = $ksyoumou * 2;$kdmg[0] = $kdmg[0] * 2.5;$com1 .= "<font size = 3 color = red>$wcname[0]がラストスパート！！</font>";
			}
			$kdmg[0] = int($kdmg[0]);
			$dmg[0] = $kdmg[0];

			for($n=1;$n<=4;$n++){
				if ($whp_flg[$n] <= 0) {
				if (rand($nebari) < rand($wc2[$n])) {
					$wdmg[$n] = $wdmg[$n] * 1.5;
					$com2[$n] .= "<font size = 3 color = red>$wcname[$n]が底力を見せる！！</font>";
				} else {
					$wdmg[$n] = $wdmg[$n] / 3;$com2[$n] .= "<font size = 3 color = red>$wcname[$n]はもうバテてきている！</font>";
				}
				} elsif (rand($seriai) < rand($wc4[$n]) || ($whp_flg[$n]/$wc1[$n] > 0.5)) {
				$wsyoumou[$n] = $wsyoumou[$n] * 2;$wdmg[$n] = $wdmg[$n] * 2.5;$com2[$n] .= "<font size = 3 color = red>$wcname[$n]がラストスパート！！</font>";
				}
				$wdmg[$n] = int($wdmg[$n]);
				$dmg[$n] = $wdmg[$n];
			}

			$sinkou = "チョコ進んだ！";
			for($n=0;$n<=4;$n++){
				$wnoko[$n] = $wnokori[$n] - $dmg[$n];
				unshift(@level,"$wcname[$n]<>$wnoko[$n]<>$n<>\n");
			}

			@tmp = map {(split /<>/)[1]} @level;
			@junni = @level[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

			$n=0;
			foreach(@junni){
				($jname[$n],$jnokori[$n],$iti)=split(/<>/);
				if($n == 0){$itii = $iti;}
				elsif($n == 1){$niii = $iti;}
				elsif($n == 2){$sanii = $iti;}
				elsif($n == 3){$yonii = $iti;}
				else {$goii = $iti;last;}
				$n+=1;
			}


			if ($wnokori[$niii] < $wnokori[$itii] || $wnokori[$goii] < $wnokori[$itii] || $wnokori[$sanii] < $wnokori[$itii] || $wnokori[$yonii] < $wnokori[$itii]) {
				if ($nuki) {
				$after = "<font color = #ff00cc>$jname[0]</font>が<font color = #ff00cc>$jname[1]</font>をさらに抜いてトップに立った！";
				$nuki += 1;
				} else {
				$after = "<font color = #ff00cc>$jname[0]</font>が<font color = #ff00cc>$jname[1]</font>を抜いてトップに立った！";$nuki = 1;
				}
			} elsif (!$nuki && !$near) {
				if ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 600) {
				$after = "<font color = #ff00cc>$jname[0]</font>！強い強い！ぶっちぎりだぁぁ！！";
				} elsif ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 400) {
				$after = "<font color = #ff00cc>$jname[0]</font>！逃げる逃げる！このまま逃げ切りか？！";
				} elsif ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 200) {
				$after ="<font color = #ff00cc>$jname[0]</font>が一歩抜け出している感じだ！";
				} elsif ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 100) {
				$after ="<font color = #ff00cc>$jname[1]</font>が先頭の<font color = #ff00cc>$jname[0]</font>に近づいてきている！";
				$near = 1;
				} else {
				$after = "先頭<font color = #ff00cc>$jname[0]</font>との差がなくなった！！";
				$near = 1;
				}
			} elsif($near) {
				if ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 500 && $hikihanasi) {
				$after = "<font color = #ff00cc>$jname[0]</font>が完全にぶっちぎる！！強すぎる！！！格の違いを見せつけた！";
				} elsif ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 250 && $hikihanasi) {
				$after = "<font color = #ff00cc>$jname[0]</font>が後続をどんどん引き離していく！！<br>このままゴールか！？";
				} elsif ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 100 && $hikihanasi) {
				$after = "<font color = #ff00cc>$jname[0]</font>がそのままいってしまうのか？！";
				} elsif ($hikihanasi) {
				$after = "<font color = #ff00cc>$jname[0]</font>との差が段々と詰まってきた！";
				} elsif ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 100 && !$hikihanasi) {
				$after = "<font color = #ff00cc>$jname[0]</font>が後続を引き離す！！";
				$hikihanasi = 1;
				} else {
				$after = "<font color = #ff00cc>$jname[0]</font>が粘っている！";
				}
			} else {
				if ($jnokori[1] - $jnokori[0] - $dmg[$niii] + $dmg[$itii] > 100) {
				$after = "<font color = #ff00cc>$jname[0]</font>が一気に引き離した！！";
				$near=1;
				} else {
				$after = "<font color = #ff00cc>$jname[0]</font>が粘る！！";
				$near=1;
				}
			}
			$after .= "先頭は$jname[0]！！！<br>続いて$jname[1]、$jname[2]、$jname[3]、最後方に$jname[4]。";
			if($jnokori[0] < 0){ $after = ""; }
		}

		if ($i == 1) {
		$com = "<font size = 5 color = blue><b>$racename、今、スタートしました！</b></font>";
		} elsif ($i == 2) {
			$com = "<font size = 5 color = blue><b>各チョコボ、道中、どんな展開が待ち受けているのか？！</b></font>";
			if ($khp_flg > 0 && 0 > $khp_flg - $ksyoumou) {
				$com .= "<br><font color = white size =3>$wcname[0]のスタミナが切れた！あとは気力で進むのみ！</font>";
			}
			for($n=1;$n<=4;$n++){
				if ($whp_flg[$n] > 0 && 0 > $whp_flg[$n] - $wsyoumou[$n]) {
					$com .= "<br><font color = white size =3>$wcname[$n]のスタミナが切れた！あとは気力で進むのみ！</font>";
				}
			}
		} elsif ($i==3) {
			$com = "<font size = 5 color = blue><b>各チョコボが一斉にラストスパートに向かいます！</b></font>";
			if ($khp_flg > 0 && 0 > $khp_flg - $ksyoumou) {
				$com .= "<br><font color = white size =3>$wcname[0]のスタミナが切れた！あとは気力で進むのみ！</font>";
			}
			for($n=1;$n<=4;$n++){
				if ($whp_flg[$n] > 0 && 0 > $whp_flg[$n] - $wsyoumou[$n]) {
					$com .= "<br><font color = white size =3>$wcname[$n]のスタミナが切れた！あとは気力で進むのみ！</font>";
				}
			}
		$java_com .= << "EOM";
function move$i() {
	Layer1.style.left = $iti[0];
	Layer2.style.left = $iti[1];
	Layer3.style.left = $iti[2];
	Layer4.style.left = $iti[3];
	Layer5.style.left = $iti[4];
	document.all.comment3.innerHTML = "$next_com";
	document.all.joutai0.innerHTML = '<b>$wjoutai[0]</b>';
	document.all.joutai1.innerHTML = '<b>$wjoutai[1]</b>';
	document.all.joutai2.innerHTML = '<b>$wjoutai[2]</b>';
	document.all.joutai3.innerHTML = '<b>$wjoutai[3]</b>';
	document.all.joutai4.innerHTML = '<b>$wjoutai[4]</b>';
	setTimeout("moveb$i()", 1500);
}
function moveb$i() {
	xPos1 = parseInt(Layer1.style.left) - ($kdmg[0] * 9 / 120);
	xPos2 = parseInt(Layer2.style.left) - ($wdmg[1] * 9 / 120);
	xPos3 = parseInt(Layer3.style.left) - ($wdmg[2] * 9 / 120);
	xPos4 = parseInt(Layer4.style.left) - ($wdmg[3] * 9 / 120);
	xPos5 = parseInt(Layer5.style.left) - ($wdmg[4] * 9 / 120);
	Layer1.style.left = xPos1;
	Layer2.style.left = xPos2;
	Layer3.style.left = xPos3;
	Layer4.style.left = xPos4;
	Layer5.style.left = xPos5;
	turn++;
EOM
		} else {
			$com = "<font size = 5 color = blue><b>最後の直線！！一番にゴールをするのはどのチョコボか？！</b></font>";
			if ($khp_flg > 0 && 0 > $khp_flg - $ksyoumou) {
				$com .= "<br><font color = white size =3>$wcname[0]のスタミナが切れた！あとは気力で進むのみ！</font>";
			}
			for($n=1;$n<=4;$n++){
				if ($whp_flg[$n] > 0 && 0 > $whp_flg[$n] - $wsyoumou[$n]) {
					$com .= "<br><font color = white size =3>$wcname[$n]のスタミナが切れた！あとは気力で進むのみ！</font>";
				}
			}
		$java_com .= << "EOM";
function move$i() {
	Layer1.style.left = $iti[0];
	Layer2.style.left = $iti[1];
	Layer3.style.left = $iti[2];
	Layer4.style.left = $iti[3];
	Layer5.style.left = $iti[4];
	document.all.joutai0.innerHTML = '<b>$wjoutai[0]</b>';
	document.all.joutai1.innerHTML = '<b>$wjoutai[1]</b>';
	document.all.joutai2.innerHTML = '<b>$wjoutai[2]</b>';
	document.all.joutai3.innerHTML = '<b>$wjoutai[3]</b>';
	document.all.joutai4.innerHTML = '<b>$wjoutai[4]</b>';
	document.all.comment3.innerHTML = "$next_com";
	setTimeout("moveb$i()", 1500);
}
function moveb$i() {
	xPos1 = parseInt(Layer1.style.left) - ($kdmg[0] * 9 / 120);
	xPos2 = parseInt(Layer2.style.left) - ($wdmg[1] * 9 / 120);
	xPos3 = parseInt(Layer3.style.left) - ($wdmg[2] * 9 / 120);
	xPos4 = parseInt(Layer4.style.left) - ($wdmg[3] * 9 / 120);
	xPos5 = parseInt(Layer5.style.left) - ($wdmg[4] * 9 / 120);
	document.all.joutai0.innerHTML = '<b>$wjoutai[0]</b>';
	document.all.joutai1.innerHTML = '<b>$wjoutai[1]</b>';
	document.all.joutai2.innerHTML = '<b>$wjoutai[2]</b>';
	document.all.joutai3.innerHTML = '<b>$wjoutai[3]</b>';
	document.all.joutai4.innerHTML = '<b>$wjoutai[4]</b>';
	Layer1.style.left = xPos1;
	Layer2.style.left = xPos2;
	Layer3.style.left = xPos3;
	Layer4.style.left = xPos4;
	Layer5.style.left = xPos5;
	turn++;
EOM
		}

		if ($khp_flg >= 0) {
		$hp_t = $khp_flg/$wc1[0];
		$wjoutai[0] = $t_status[$hp_t];
		} else { $wjoutai[0] = "残るは気力のみ"; }

		for($n=1;$n<=4;$n++){
			if ($whp_flg[$n] >= 0) {
				$hp_t = $whp_flg[$n] / $wc1[$n];
				$wjoutai[$n] = $t_status[$hp_t];
			} else { $wjoutai[$n] = "残るは気力のみ"; }
		}
		$khp_flg -= $ksyoumou;
		for($n=1;$n<=4;$n++){
			$whp_flg[$n] -= $wsyoumou[$n];
		}

		$iti[0] = 900*$wnoko[0]/2400;
		$iti[1] = 900*($wnoko[1])/2400;
		$iti[2] = 900*($wnoko[2])/2400;
		$iti[3] = 900*($wnoko[3])/2400;
		$iti[4] = 900*($wnoko[4])/2400;

			$next_com = "<font size=3 color=#FFFFFF>$com<br>$com1 $wcname[0]は<font class=dmg><b>$dmg[0]</b></font>$sinkou<br>$com2[1] $wcname[1]は<font class=dmg><b>$dmg[1]</b></font>$sinkou<br>$com2[2] $wcname[2]は<font class=dmg><b>$dmg[2]</b></font>$sinkou<br>$com2[3] $wcname[3]は<font class=dmg><b>$dmg[3]</b></font>$sinkou<br>$com2[4] $wcname[4]は<font class=dmg><b>$dmg[4]</b></font>$sinkou</font><br><font color = pink size = 4><b>$after</b></font><br>";

		for($n=1;$n<=4;$n++){
			$wnokori[$n] -= $wdmg[$n];
		}
		$wnokori[0] -= $kdmg[0];

		if($wnokori[0] < 0 || $wnokori[1] < 0 || $wnokori[2] < 0 || $wnokori[3] < 0 || $wnokori[4] < 0){
		$java_com .= << "EOM";
	if (turn < 5) {
		setTimeout("moveb$i()", 150);
	} else {
		setTimeout("finish()", 100);
	}
}
EOM
			last;
		}

		$ii = $i+1;

		if ($i > 2) {
		$java_com .= << "EOM";
	if (turn == 4) {
		turn = 0;
		setTimeout("move$ii()", 150);
	} else {
	setTimeout("moveb$i()", 150);
	}
}
EOM
		}

		$i++;
		$j++;
	}
	$n=0;
	for ($i=0;$i<=4;$i++) {
		$goal[$i]=0;
		if ($wnokori[$i] < 0) {
			$goal[$i]=1;$goalcho.="$wcname[$i]と";
			$n++;
		}
	}

	$seri=0;
	if($n >=2){
		for($n=0;$n<=4;$n++){
			$goalseri[$n]=0;
			if ($goal[$n]) {
				$goalseri[$n]=int(rand($wc4[$n]));
			}
			unshift(@level,"$wcname[$n]<>$goalseri[$n]<>$n<>\n");
		}

		@tmp = map {(split /<>/)[1]} @level;
		@junni = @level[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

		$n=0;
		foreach(@junni){
			($jname[$n],$seri[$n],$iti)=split(/<>/);
			$n+=1;
		}

		$comment = "<b><font size=6>$goalchoが同時にゴール！！！結果は写真判定にゆだねられます！<br>審議の結果は・・・・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br></font></b>";
	}

	$comment .= "<b><font size=8 color=blue>勝ったのは$jname[0]！！<br>トップでゴールを通過し、激戦を制しました！</font></b><b>";

	&race_header;

		print <<"EOM";
<h1><center>サラブレッドチョコボ$racename！！！</h1><font color = black size = 5><b>チョコボたちの激しいレースが今日も開催されます。<br>$racename、今、発走です！</b></font></center>
<DIV style="left : 250 px;
position:relative;
  z-index : 1;">
<TABLE border="1" width = "600">
  <TBODY>
    <TR>
      <TD align="center"><IMG src="$img_farm/$choco_img[$wcno[0]]" width="32" height="32" border="0" alt="$wcname[0]"></TD>
      <TD align="center"><IMG src="$img_farm/$choco_img[$wcno[1]]" width="32" height="32" border="0" alt="$wcname[1]"></TD>
      <TD align="center"><IMG src="$img_farm/$choco_img[$wcno[2]]" width="32" height="32" border="0" alt="$wcname[2]"></TD>
      <TD align="center"><IMG src="$img_farm/$choco_img[$wcno[3]]" width="32" height="32" border="0" alt="$wcname[3]"></TD>
      <TD align="center"><IMG src="$img_farm/$choco_img[$wcno[4]]" width="32" height="32" border="0" alt="$wcname[4]"></TD>
</tr><tr>
      <TD><b>１：$wcname[0]</b></TD>
      <TD><b>２：$wcname[1]</b></TD>
      <TD><b>３：$wcname[2]</b></TD>
      <TD><b>４：$wcname[3]</b></TD>
      <TD><b>５：$wcname[4]</b></TD>
</tr><tr>
      <TD><DIV id ="joutai0">元気モリモリ</DIV></TD>
      <TD><DIV id ="joutai1">元気モリモリ</DIV></TD>
      <TD><DIV id ="joutai2">元気モリモリ</DIV></TD>
      <TD><DIV id ="joutai3">元気モリモリ</DIV></TD>
      <TD><DIV id ="joutai4">元気モリモリ</DIV></TD>
</tr><tr>
      <TD><b>$waza</b></TD>
      <TD><b>$wwaza[1]</b></TD>
      <TD><b>$wwaza[2]</b></TD>
      <TD><b>$wwaza[3]</b></TD>
      <TD><b>$wwaza[4]</b></TD>
    </TR>
<tr>
      <TD><b>$wcbreader[0]</b></TD>
      <TD><b>$wcbreader[1]</b></TD>
      <TD><b>$wcbreader[2]</b></TD>
      <TD><b>$wcbreader[3]</b></TD>
      <TD><b>$wcbreader[4]</b></TD>
    </TR>
  </TBODY>
</TABLE>
</DIV>
<table background="$img_farm/race.gif" width="900" height="60" border="0">
    <TR><font color = black>
      <TD>１００</TD>
      <TD>３００</TD>
      <TD>５００</TD>
      <TD>７００</TD>
      <TD>９００</TD>
      <TD>１１００</TD>
      <TD>１３００</TD>
      <TD>１５００</TD>
      <TD>１７００</TD>
      <TD>１９００</TD>
      <TD>２１００</TD>
      <TD>２３００</TD>
</font>
    </TR>
<tr>
<DIV style="left : 900 px; position:absolute;  z-index : 1;" id="Layer1"><IMG src="$img_farm/$choco_img[$wcno[0]]" width="32" height="32" border="0" alt="$wcname[0]"><br><b><font color=red size = 3>１<br></font></b>
</DIV>
<DIV style="left : 900 px;
position:absolute;
  z-index : 1;
" id="Layer2"><IMG src="$img_farm/$choco_img[$wcno[1]]" width="32" height="32" border="0" alt="$wcname[1]"><br><b><font color=red size = 3>２<br></font></b>
</DIV>
<DIV style="left : 900 px;
position:absolute;
  z-index : 1;
" id="Layer3"><IMG src="$img_farm/$choco_img[$wcno[2]]" width="32" height="32" border="0" alt="$wcname[2]"><br><b><font color=red size = 3>３<br></font></b>
</DIV>
<DIV style="left : 900 px;
position:absolute;
  z-index : 1;
" id="Layer4"><IMG src="$img_farm/$choco_img[$wcno[3]]" width="32" height="32" border="0" alt="$wcname[3]"><br><b><font color=red size = 3>４<br></font></b>
</DIV>
<DIV style="left : 900 px;
position:absolute;
  z-index : 1;
" id="Layer5"><IMG src="$img_farm/$choco_img[$wcno[4]]" width="32" height="32" border="0" alt="$wcname[4]"><br><b><font color=red size = 3>５<br></font></b>
</DIV>
</td></tr></table>
<DIV>
<br><br>
<TABLE width=100% bgcolor=0000FF><TBODY><TR><TD width=10 bgcolor=#99CCFF><img src=\"$img_farm/ana.gif\"></TD><TD width=100% bgcolor=#000000>
<DIV id="comment3">
<font size="5" color="#FF00FF">$racenameが間もなく発走です</font>
</DIV>
<DIV id="comment2">
</DIV>
</TD></TR></TBODY></TABLE>
</DIV>
EOM

	&choco_footer;

	exit;
}

#--------------------------#
#  ライバルチョコボ読み込み  #
#--------------------------#
sub read_cwinner {

	open(IN,"$ribal");
	@winnera = <IN>;
	close(IN);

	$enter_sum = @winnera;

	if ($in{'enter1'} > $enter_sum) { $in{'enter1'} = int(rand($enter_sum)); }
	if ($in{'enter2'} > $enter_sum) { $in{'enter2'} = int(rand($enter_sum)); }
	if ($in{'enter3'} > $enter_sum) { $in{'enter3'} = int(rand($enter_sum)); }
	if ($in{'enter4'} > $enter_sum) { $in{'enter4'} = int(rand($enter_sum)); }
	if ($in{'enter5'} > $enter_sum) { $in{'enter5'} = int(rand($enter_sum)); }

	($wcid[0],$wcpass[0],$wcbreader[0],$wcname[0],$wcsex[0],$cblood,$wcno[0],$cmaxmax,$ctype,$cmax0,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$clife,$ctrain,$crun,$cwin,$cmax,$wc0[0],$wc1[0],$wc2[0],$wc3[0],$wc4[0],$wc5[0],$wc6[0],$cgold,$cfather,$cfblood,$cmother,$cmblood) = split(/<>/,$winnera[$in{'enter1'}]);

	($bcid,$bcpass,$wcbreader[1],$wcname[1],$bcsexb,$bblood,$wcno[1],$bmaxmax,$wctype[1],$bmax0,$bmax1,$bmax2,$bmax3,$bmax4,$bmax5,$bmax6,$blife,$btrain,$brun,$bwin,$wcmax[1],$wc0[1],$wc1[1],$wc2[1],$wc3[1],$wc4[1],$wc5[1],$wc6[1],$bgold,$bfather,$bfblood,$bmother,$bmblood) = split(/<>/,$winnera[$in{'enter2'}]);

	($bcid,$bcpass,$wcbreader[2],$wcname[2],$bcsexb,$bblood,$wcno[2],$bmaxmax,$wctype[2],$bmax0,$bmax1,$bmax2,$bmax3,$bmax4,$bmax5,$bmax6,$blife,$btrain,$brun,$bwin,$wcmax[2],$wc0[2],$wc1[2],$wc2[2],$wc3[2],$wc4[2],$wc5[2],$wc6[2],$bgold,$bfather,$bfblood,$bmother,$bmblood) = split(/<>/,$winnera[$in{'enter3'}]);

	($bcid,$bcpass,$wcbreader[3],$wcname[3],$bcsexb,$bblood,$wcno[3],$bmaxmax,$wctype[3],$bmax0,$bmax1,$bmax2,$bmax3,$bmax4,$bmax5,$bmax6,$blife,$btrain,$brun,$bwin,$wcmax[3],$wc0[3],$wc1[3],$wc2[3],$wc3[3],$wc4[3],$wc5[3],$wc6[3],$bgold,$bfather,$bfblood,$bmother,$bmblood) = split(/<>/,$winnera[$in{'enter4'}]);

	($bcid,$bcpass,$wcbreader[4],$wcname[4],$bcsexb,$bblood,$wcno[4],$bmaxmax,$wctype[4],$bmax0,$bmax1,$bmax2,$bmax3,$bmax4,$bmax5,$bmax6,$blife,$btrain,$brun,$bwin,$wcmax[4],$wc0[4],$wc1[4],$wc2[4],$wc3[4],$wc4[4],$wc5[4],$wc6[4],$bgold,$bfather,$bfblood,$bmother,$bmblood) = split(/<>/,$winnera[$in{'enter5'}]);
}
