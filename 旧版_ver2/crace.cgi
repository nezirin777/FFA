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

$chococss = 'choco.css';

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

$backform = << "EOM";
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$in{'id'}">
<input type="hidden" name=mydata value="$in{'mydata'}">
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場に戻る">
</form>
EOM

if($mode eq 'race0') { $win_min = 0;$win_limit = 1;$ribal = "./ribal0.cgi"; $racename = "新羽戦"; &chocobattle; }
elsif($mode eq 'race1') { $win_min = 1;$win_limit = 5;$ribal = "./ribal1.cgi"; $racename = "５００万下"; &chocobattle; }
elsif($mode eq 'race2') { $win_min = 5;$win_limit = 15;$ribal = "./ribal2.cgi"; $racename = "９００万下"; &chocobattle; }
elsif($mode eq 'race3') { $win_min = 15;$win_limit = 30;$ribal = "./ribal3.cgi"; $racename = "１６００万下"; &chocobattle; }
elsif($mode eq 'race4') { $win_min = 30;$win_limit = 80;$ribal = "./ribal4.cgi"; $racename = "オープン"; &chocobattle; }
elsif($mode eq 'race5') { $win_min = 50;$win_limit = 100;$ribal = "./ribal5.cgi"; $racename = "グレードⅢ"; &chocobattle; }
elsif($mode eq 'race6') { $win_min = 75;$win_limit = 130;$ribal = "./ribal6.cgi"; $racename = "グレードⅡ"; &chocobattle; }
elsif($mode eq 'race7') {
	$win_min = 30;
	$win_limit = 10000;
	$ribal = "./ribal7.cgi"; 
	if($in{'race'} == 1){$racename = "チョコボダービー";}
	elsif($in{'race'} == 2){$racename = "チョコボスタリオン";}
	elsif($in{'race'} == 3){$racename = "チョコボカップ";}
	elsif($in{'race'} == 4){$racename = "レジェンドカップ";}
	elsif($in{'race'} == 5){$racename = "ＣＣＢ賞";}
	elsif($in{'race'} == 6){$racename = "チョコボ桜花賞";}
	elsif($in{'race'} == 7){$racename = "チョコボ皐月賞";}
	elsif($in{'race'} == 8){$racename = "チョコボ記念";}
	elsif($in{'race'} == 9){$racename = "チョコボステークス";}
	elsif($in{'race'} == 10){$racename = "キングスカップ";}
	elsif($in{'race'} == 11){$racename = "クイーンカップ";}
	&chocobattle;
} elsif($mode eq 'race8') {
	$win_min = 30;
	$win_limit = 10000;
	$ribal = "./ribal8.cgi";
	if($in{'race'} == 12){$racename = "シルバーカップ";}
	elsif($in{'race'} == 13){
		$racename = "キングイクアンドクイーンエリリン";
	}
	elsif($in{'race'} == 14){$racename = "チョコリスダービー";}
	elsif($in{'race'} == 15){$racename = "チョコボワールドカップ";}
	elsif($in{'race'} == 16){$racename = "チョコボエンプレス杯";}
	elsif($in{'race'} == 17){$racename = "チョコボウル";}
	elsif($in{'race'} == 18){$racename = "ブリーダーズカップ";}
	elsif($in{'race'} == 19){$racename = "ゴールドカップ";}
	elsif($in{'race'} == 20){$racename = "プラチナカップ";}
	elsif($in{'race'} == 21){$racename = "チョコボオークス";}
	elsif($in{'race'} == 22){$racename = "チョコボキングス";}
	&chocobattle;
}
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

	($wcid[0],$wcpass[0],$wcbreader[0],$wcname[0],$wcsex[0]) = split(/<>/,$choco_chara[0]);

	if ($cwin < $win_min || $cwin >= $win_limit) { &error('出れません！'); }
	if (!$wcname[0]) { &error('チョコボがいません。'); }
	if(!($wcname[0]) || ($wcname[0] eq "ここに名前を入力")){&error("チョコボに名前がついていません！$backform");}
	if($mode eq 'race7' && ($crun + $ctrain) % 40 != 0) {
		&error('出れません！');
	} elsif($mode eq 'race8' && ($crun + $ctrain) % 60 != 0) {
		&error('出れません！');
	}

	&read_cwinner;

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$chara[27] = time();
	$vtime = $m_time - $ltime;
	$success = 0;
	$lose = 0;

	if($clife < 400) { &error("チョコボが弱っています。レースはできません。$backform");}

	if($vtime > 0){
		if($ltime < $b_time) { &error("あと$vtime秒レースはできません。"); }
	}

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
	$khp_flg = $c1;
	$heri = ($c2 + $wc2[1] + $wc2[2] + $wc2[3] + $wc2[4] )/10000;
	$nebari = int(($c2 + $wc2[1] + $wc2[2] + $wc2[3] + $wc2[4])/5);
	$kisyou = int(($c3 + $wc3[1] + $wc3[2] + $wc3[3] + $wc3[4])/5);
	$seriai = int(($c4 + $wc4[1] + $wc4[2] + $wc4[3] + $wc4[4])/5);
	$tiryoku = int(($c5 + $wc5[1] + $wc5[2] + $wc5[3] + $wc5[4])/5);
	$tyousei = 5000 / ($c0 + $wc0[1] + $wc0[2] + $wc0[3] + $wc0[4]);
	$kinryoku = int(($c0 + $wc0[1] + $wc0[2] + $wc0[3] + $wc0[4])/5);
	$wnokori[0] = 2400;
	$lastspart = int((($c0 + $wc0[1] + $wc0[2] + $wc0[3] + $wc0[4])/3 + ($c6 + $wc6[1] + $wc6[2] + $wc6[3] + $wc6[4]))/150);
	$syasin = 0;
	$comment = "";
	$gold = 0;
	$nuki = 0;
	$near = 0;
	$hikihanasi = 0;
	$member = 5;
	@t_status = ('倒れる寸前','バテバテ','バテ気味','普通','元気モリモリ');


	$i=1;$j=0;@battle_date=();
	foreach(1..5000) {


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
			if(rand($kisyou) <= rand($c3*2/3)){
				$wdedasi[0] = int(rand($c0/($tyousei*4))+$c0/($tyousei*4));
				$com1 .= "<font size = 3 color = red>$wcname[0]は出遅れてしまった！</font>";
				$ksyoumou = $heri * $wdedasi[0] * 3 * ($kisyou / $c3) * ($c2 / $nebari);
			} elsif (rand($tiryoku) <= rand($c5*2/3)) {
				$wdedasi[0] = int(rand($c0*1.5/$tyousei));
				$com1 .= "<font size = 3 color = red>$wcname[0]は絶好のスタートを切った！</font>";
				$ksyoumou = $heri * ($wdedasi[0] / 2) * ($kisyou / $c3) * ($c2 / $nebari);
			} else {
				$wdedasi[0] = int(rand($c0/($tyousei*2)) + $c0/($tyousei*2));
				$com1 .= "<font size = 3 color = red>$wcname[0]はスタートを切った！</font>";
				$ksyoumou = $heri * $wdedasi[0] * ($kisyou / $c3) * ($c2 / $nebari);
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
	document.all.comment3.innerHTML = "<font color=#FFFF33 size=6>さぁ、スタートしました！</font>";
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
			$wkeii[0] = int(rand($c0/4)) + int($c0*3/4) - $kinryoku + $wdedasi[0];
			$wnokori[0] = 1000 - $wkeii[0];
			if($wnokori[0] < 400){ $wnokori[0] = 400; }
			for($n=1;$n<=4;$n++){
				$wkeii[$n] = int(rand($wc0[$n]/4)) + int($wc0[$n]*3/4) - $kinryoku + $wdedasi[$n];
				$wnokori[$n] = 1000 - $wkeii[$n];
				if($wnokori[$n] < 400){ $wnokori[$n] = 400; }
			}

			if (rand($kisyou) <= rand($c3*1/4)) {
				$ksyoumou = $heri * (1400 + $wkeii[0] - $wdedasi[0]) * 3 * ($kisyou / $c3) * ($c2 / $nebari);
				$com1 = "<font size = 3 color = yellow>$wcname[0]は息をあらたげて走ってきた！</font>";
				$wnokori[0] = int($wnokori[0] * 9/10);
			} elsif (rand($tiryoku) <= rand($c5*1/3)) {
				$ksyoumou = ($heri * (1400 + $wkeii[0] - $wdedasi[0]) * ($kisyou / $c3) * ($c2 / $nebari) )/ 2;
				$com1 = "<font size = 3 color = yellow>$wcname[0]は足場が楽なコースを走ってきた！</font>";
			} else {
				$ksyoumou = $heri * (1400 + $wkeii[0] - $wdedasi[0]) * ($kisyou / $c3) * ($c2 / $nebari);
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
	document.all.joutai0.innerHTML = "<b>$wjoutai[0]</b>";
	document.all.joutai1.innerHTML = "<b>$wjoutai[1]</b>";
	document.all.joutai2.innerHTML = "<b>$wjoutai[2]</b>";
	document.all.joutai3.innerHTML = "<b>$wjoutai[3]</b>";
	document.all.joutai4.innerHTML = "<b>$wjoutai[4]</b>";
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
			$kdmg[0] = (rand($c0) + rand($c6) + rand($c6) + rand($c6))/$lastspart;
			$ksyoumou = $heri * $kdmg[0] * ($kisyou / $c3) * ($c2 / $nebari);

			if($khp_flg <= 0){
				if(rand($nebari) < rand($c2)){
				$kdmg[0] = $kdmg[0] * 1.5;
				$com1 .= "<font size = 3 color = red>$wcname[0]が底力を見せる！！</font>";
				} else {
				$kdmg[0] = $kdmg[0] / 3;$com1 .= "<font size = 3 color = red>$wcname[0]はもうバテてきている！</font>";
				}
			} elsif (rand($seriai) < rand($c4) || ($khp_flg/$c1 >= 0.4)) {
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
	document.all.joutai0.innerHTML = "<b>$wjoutai[0]</b>";
	document.all.joutai1.innerHTML = "<b>$wjoutai[1]</b>";
	document.all.joutai2.innerHTML = "<b>$wjoutai[2]</b>";
	document.all.joutai3.innerHTML = "<b>$wjoutai[3]</b>";
	document.all.joutai4.innerHTML = "<b>$wjoutai[4]</b>";
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
	document.all.joutai0.innerHTML = "<b>$wjoutai[0]</b>";
	document.all.joutai1.innerHTML = "<b>$wjoutai[1]</b>";
	document.all.joutai2.innerHTML = "<b>$wjoutai[2]</b>";
	document.all.joutai3.innerHTML = "<b>$wjoutai[3]</b>";
	document.all.joutai4.innerHTML = "<b>$wjoutai[4]</b>";
	document.all.comment3.innerHTML = "$next_com";
	setTimeout("moveb$i()", 1500);
}
function moveb$i() {
	xPos1 = parseInt(Layer1.style.left) - ($kdmg[0] * 9 / 120);
	xPos2 = parseInt(Layer2.style.left) - ($wdmg[1] * 9 / 120);
	xPos3 = parseInt(Layer3.style.left) - ($wdmg[2] * 9 / 120);
	xPos4 = parseInt(Layer4.style.left) - ($wdmg[3] * 9 / 120);
	xPos5 = parseInt(Layer5.style.left) - ($wdmg[4] * 9 / 120);
	document.all.joutai0.innerHTML = "<b>$wjoutai[0]</b>";
	document.all.joutai1.innerHTML = "<b>$wjoutai[1]</b>";
	document.all.joutai2.innerHTML = "<b>$wjoutai[2]</b>";
	document.all.joutai3.innerHTML = "<b>$wjoutai[3]</b>";
	document.all.joutai4.innerHTML = "<b>$wjoutai[4]</b>";
	Layer1.style.left = xPos1;
	Layer2.style.left = xPos2;
	Layer3.style.left = xPos3;
	Layer4.style.left = xPos4;
	Layer5.style.left = xPos5;
	turn++;
EOM
		}

		if ($khp_flg >= 0) {
		$hp_t = $khp_flg/$c1;
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
		}

if($wnokori[0] < 0 && $wnokori[1] < 0){$seri = 1;$syasin = 1;last;}
elsif($wnokori[0] < 0 && $wnokori[2] < 0){$seri = 2;$syasin = 1;last;}
elsif($wnokori[0] < 0 && $wnokori[3] < 0){$seri = 3;$syasin = 1;last;}
elsif($wnokori[0] < 0 && $wnokori[4] < 0){$seri = 4;$syasin = 1;last;}
elsif($wnokori[0] < 0){$win = 1;last;}
elsif($wnokori[1] < 0 || $wnokori[2] < 0 || $wnokori[3] < 0 || $wnokori[4] < 0){$win = 0;last;}

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

	if($syasin){
		$comment = "<b><font size=6>同時にゴール！！！結果は写真判定にゆだねられます！<br>審議の結果は・・・・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br>・<br></font></b>"; 
		if(rand($c4) > rand($wc4[$seri])){$win = 1;}
		else{$win = 0;$jname[0]=$wcname[$seri];}
		}

	if($win) {
		$crun += 1;
		$cwin += 1;
		$cmax += 80;
		$c0 += int(rand(6))+1;
		$c1 += int(rand(6))+1;
		$c2 += int(rand(6))+1;
		$c3 += int(rand(6))+1;
		$c4 += int(rand(6))+1;
		$c5 += int(rand(6))+1;
		$c6 += int(rand(6))+1;
		$gold = (int($wcmax[1]/1000) + 1) ** 13;
		$comment .= "<b><font size=5>勝ったのは$wcname[0]！！</font></b><p><b><font size=5 color=\'#ff0000\'>$chara[4]「よくやった$wcname[0]！」</font></b><p><b><font size=5 color=\'#0000ff\'>$wcname[0]「クエ～♪」<br>$wcname[0]は一段と成長した！！！</font></b><p>";


		if($in{'race'}){$comment .= "<br><font color = gold size = 7><b>$racename</font><font size=5>を制した！ＧⅠウィナーとして名前が残ります。</b></font>";

	&all_message("$wcbreader[0]さんの$wcname[0]が$racenameを制しました！！");

	$lock_file = "$lockfolder/rir.lock";
	&lock($lock_file,'RIR');
	open(IN,"./g1/$chara[0].cgi");
	@rireki = <IN>;
	close(IN);

for($i=1;$i<=20;$i++){$rire[$i]=0;}
$hit=0;@rireki_new=();
	foreach(@rireki){
			($rid,$rpass,$rname,$rfather,$rmother,$rire[1],$rire[2],$rire[3],$rire[4],$rire[5],$rire[6],$rire[7],$rire[8],$rire[9],$rire[10],$rire[11],$rire[12],$rire[13],$rire[14],$rire[15],$rire[16],$rire[17],$rire[18],$rire[19],$rire[20],$rire[21],$rire[22],$rbreader) = split(/<>/);
if($rid eq "$wcid[0]" && $rname eq "$wcname[0]"){$hit = 1;
			$rire[$in{'race'}] = 1;
			unshift(@g_new,"$wcid[0]<>$wcpass[0]<>$wcname[0]<>$cfather<>$cmother<>$rire[1]<>$rire[2]<>$rire[3]<>$rire[4]<>$rire[5]<>$rire[6]<>$rire[7]<>$rire[8]<>$rire[9]<>$rire[10]<>$rire[11]<>$rire[12]<>$rire[13]<>$rire[14]<>$rire[15]<>$rire[16]<>$rire[17]<>$rire[18]<>$rire[19]<>$rire[20]<>$rire[21]<>$rire[22]<>$rbreader<>\n");
}
else{push(@g_new,"$_");}
			}
	open(IN,"./rireki.cgi");
	@rireki = <IN>;
	close(IN);

for($i=1;$i<=20;$i++){$rire[$i]=0;}
$hit=0;@rireki_new=();
	foreach(@rireki){
			($rid,$rpass,$rname,$rfather,$rmother,$rire[1],$rire[2],$rire[3],$rire[4],$rire[5],$rire[6],$rire[7],$rire[8],$rire[9],$rire[10],$rire[11],$rire[12],$rire[13],$rire[14],$rire[15],$rire[16],$rire[17],$rire[18],$rire[19],$rire[20],$rire[21],$rire[22],$rbreader) = split(/<>/);
if($rid eq "$wcid[0]" && $rname eq "$wcname[0]"){$hit = 1;
			$rire[$in{'race'}] = 1;
			unshift(@rireki_new,"$wcid[0]<>$wcpass[0]<>$wcname[0]<>$cfather<>$cmother<>$rire[1]<>$rire[2]<>$rire[3]<>$rire[4]<>$rire[5]<>$rire[6]<>$rire[7]<>$rire[8]<>$rire[9]<>$rire[10]<>$rire[11]<>$rire[12]<>$rire[13]<>$rire[14]<>$rire[15]<>$rire[16]<>$rire[17]<>$rire[18]<>$rire[19]<>$rire[20]<>$rire[21]<>$rire[22]<>$rbreader<>\n");
}
else{push(@rireki_new,"$_");}
			}

for($i=1;$i<=20;$i++){$rire[$i]=0;}
	if(!$hit){
			$rire[$in{'race'}] = 1;
	unshift(@g_new,"$wcid[0]<>$wcpass[0]<>$wcname[0]<>$cfather<>$cmother<>$rire[1]<>$rire[2]<>$rire[3]<>$rire[4]<>$rire[5]<>$rire[6]<>$rire[7]<>$rire[8]<>$rire[9]<>$rire[10]<>$rire[11]<>$rire[12]<>$rire[13]<>$rire[14]<>$rire[15]<>$rire[16]<>$rire[17]<>$rire[18]<>$rire[19]<>$rire[20]<>$rire[21]<>$rire[22]<>$wcbreader[0]<>\n");
	unshift(@rireki_new,"$wcid[0]<>$wcpass[0]<>$wcname[0]<>$cfather<>$cmother<>$rire[1]<>$rire[2]<>$rire[3]<>$rire[4]<>$rire[5]<>$rire[6]<>$rire[7]<>$rire[8]<>$rire[9]<>$rire[10]<>$rire[11]<>$rire[12]<>$rire[13]<>$rire[14]<>$rire[15]<>$rire[16]<>$rire[17]<>$rire[18]<>$rire[19]<>$rire[20]<>$rire[21]<>$rire[22]<>$wcbreader[0]<>\n");
		}

	open(OUT,">./g1/$chara[0].cgi");
	print OUT @g_new;
	close(OUT);

	open(OUT,">./rireki.cgi");
	print OUT @rireki_new;
	close(OUT);
	$lock_file = "$lockfolder/rir.lock";
	&unlock($lock_file,'RIR');

	$gold *= 1000;
			}#G１読込

	} else {

		$crun += 1;
		$cmax += 20;
		$c0 += int(rand(1))+1;
		$c1 += int(rand(1))+1;
		$c2 += int(rand(1))+1;
		$c3 += int(rand(1))+1;
		$c4 += int(rand(1))+1;
		$c5 += int(rand(1))+1;
		$c6 += int(rand(1))+1;
		$gold = int($wcmax[1] / 1000);
		$comment .= "<b><font size=5>勝ったのは$jname[0]！！</font></b><b><font size=5>$wcname[0]は負けてしまった･･･</font></b><p><b><font size=5 color='#0000ff'>$chara[4]「$wcname[0]～～（T_T）」</font></b><p><b><font size=5 color=\'#ff0000\'>$wcname[0]「クエエエ・・・」<br></font></b><br>$wcname[0]はほんのちょっぴり成長した<p>";
	}

if($ctrain + $crun > 1000){$cmaxmax = int($cmaxmax * 0.99);$rousui = "もう、これ以上$wcname[0]を酷使するのは可哀想な気がする･･･。これまですごくよくしてくれたと思うよ。そろそろ引退の時期なんじゃないかな･･･？";}

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
if($c0+$c1+$c2+$c3+$c4+$c5+$c6 > $cmax){$senzai = "もう$wcname[0]の能\力の限界に達してしまったように見える･･･。これ以上の成長は見込めなさそうだ･･･。<br>";
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
$senzai = "今の$wcname[0]の能\力の限界になってきているのかも･･･。潜在能\力を引き出さないといけなさそうだ･･･。<br>";}

	$chara[19] = $chara[19] + $gold;
	$cgold = $cgold + $gold/100;

	&farm_choco_regist;
	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&unlock($lock_file,'CHC');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$comment .= "<br>$chara[4]は、<b>$gold</b>G手に入れた。<br>$senzai $genkai $rousui";

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

#--------------------------#
#  ライバルチョコボ読み込み  #
#--------------------------#
sub read_cwinner {

$n=0;
	open(IN,"$ribal");
	@winner = <IN>;
	close(IN);

	foreach(@winner){
			($bcbreader,$bcname,$bcno,$bctype,$bcmax,$bc0,$bc1,$bc2,$bc3,$bc4,$bc5,$bc6) = split(/<>/);
$n += 1;
}

	open(IN,"$ribal");
	@winnera = <IN>;
	close(IN);

for($i=1;$i<=4;$i++){
$rib=int(rand($n));
	($wcbreader[$i],$wcname[$i],$wcno[$i],$wctype[$i],$wcmax[$i],$wc0[$i],$wc1[$i],$wc2[$i],$wc3[$i],$wc4[$i],$wc5[$i],$wc6[$i]) = split(/<>/,$winnera[$rib]);

}



}
