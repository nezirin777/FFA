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
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 戦闘ライブラリの読み込み
require 'battle.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}
#機種判定
$agent = $ENV{'HTTP_USER_AGENT'};
($browser,$version,$model) = split(/\//,$agent);
if ($browser eq "DoCoMo") {$turn = $iturn;}
	if($in{'level'}=="low"){}

if($mode eq 'monster0') {$monster_file=$low_monster; &monster; }
elsif($mode eq 'monster1') {$monster_file=$normal_monster; &monster; }
elsif($mode eq 'monster2') {$monster_file=$high_monster; &monster; }
elsif($mode eq 'monster3') {$monster_file=$sp_monster; &monster; }
elsif($mode eq 'boss0') {$bmonster=$boss_monster0;$suzi=0;$ranks=1; &boss; }
elsif($mode eq 'boss1') {$bmonster=$boss_monster1;$suzi=1;$ranks=2; &boss; }
elsif($mode eq 'boss2') {$bmonster=$boss_monster2;$suzi=2;$ranks=3; &boss; }
elsif($mode eq 'boss3') {$bmonster=$boss_monster3;$suzi=3;$ranks=4; &boss; }
elsif($mode eq 'genei') { &genei; }
elsif($mode eq 'isekiai') { &isekiai; }
exit;

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃   オートローダー
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sub AUTOLOAD {
	my $name = ($AUTOLOAD =~ /^main::(.+)$/)[0];
	($FLAG{'autoload'}++ > 50) && die $AUTOLOAD; # 念のため無限ループ防止
	defined %SUB or &SUBS;
	if (!defined $SUB{$name}) {
		&error("定義されていない関数($AUTOLOAD)が呼ばれました。"); exit;
	}
	eval $SUB{$name}; length($@) && &error("EVAL ERROR: $@ ($AUTOLOAD)");
	delete $SUB{$name}; goto &{'main::' . $name};
}

sub SUBS {
%SUB = (
	monster => <<'__SUB__',
#----------------------#
#  モンスターとの戦闘  #
#----------------------#
sub monster {
	if($battle_flag) { &error("現在戦闘中です。少しお待ちになってから戦闘してください。"); }
	
	$battle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { last; }
	}

	if(!$kmons) { &error("一度キャラクターと闘ってください"); }

	if($kitem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($ci_no,$ci_name,$ci_dmg,$ci_gold,$ci_plus) = split(/<>/);
			if($kitem eq $ci_no) { last; }
		}
	}

	if($kdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($cd_no,$cd_name,$cd_dmg,$cd_gold,$cd_plus) = split(/<>/);
			if($kdef eq $cd_no) { last; }
		}
	}

	if($kacsno){
		open(IN,"$acs_file");
		@log_acs = <IN>;
		close(IN);

		foreach(@log_acs){
			($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
			if($kacsno eq "$a_no"){last; }
		}
	}

	&acs_add;

	open(IN,"$monster_file");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = int(rand($r_no));

	($mname,$mex,$mrand,$msp,$mdmg,$mkahi,$monstac,$mons_ritu) = split(/<>/,$MONSTER[$r_no]);

	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$khp_flg = $khp;
	$mhp = int(rand($mrand)) + $msp;
	$mhp_flg = $mhp;
	$m_sp = int(rand(11));

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$dmg1 = $klv * (int(rand(5)) + 1);
		$dmg2 = $mdmg + int(rand($mrand));
		$clit1 = "";
		$clit2 = "";
		$sake1 = 0;
		$sake2 = 0;
		$com1 = "";
		$com2 = "$mnameが襲いかかった！！";
		$kawasi1 = "";
		$kawasi2 = "";
		$hpplus1 = 0;
		$hpplus2 = 0;
		$kaihuku1 = "";
		$kaihuku2 = "";

	&tyousensya;
	&tyosenwaza;
	if($monstac > 0){if($mons_ritu > int(rand(100))){&mons_waza;}}
	&acs_waza;

	&mons_clt;
	&mons_kaihi;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&imonsbattle_sts;}
	else{&monsbattle_sts;}

		$khp_flg = $khp_flg - $dmg2 - $dmgme1 + $hpplus1;
		if($khp_flg > $kmaxhp){$khp_flg = $kmaxhp;}
		$mhp = $mhp - $dmg1 + $hpplus2;
		if($mhp > $mhp_flg){$mhp = $mhp_flg;}

		if($mhp <= 0) { $win = 1; last; }
		elsif($khp_flg <= 0) { $win = 0; last; }
		else{ $win = 2;}

		$i++;
		$j++;
	}

	if($win==1) {
		$ktotal += 1;
		$kkati += 1;
		$kex = $kex + $mex;
		$kmons -= 1;
		$kmori = $boss;
		$gold = $gold + int(rand(10)+1) * int($mhp_flg);
		$kgold += $gold;
		if($kgold < 0){$kgold = 0;}
		if($kgold > $gold_max){$kgold = $gold_max;}
		$comment = "<b><font size=5>$knameは、戦闘に勝利した！！</font></b><P/>";
	}elsif($win==2) {
		$ktotal += 1;
		$kex = $kex + $mex;
		$kmons -= 1;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、逃げ出した・・・♪</font></b><P/>";
	}else{
		$ktotal += 1;
		$mex = 1;
		$kex = $kex + $mex;
		$kmons -= 1;
		$kmori = $boss;
		$kgold = int(($kgold / 2));
		$comment = "<b><font size=5>$knameは、戦闘に負けた・・・。</font></b><P/>";
	}

	&acs_sub;

	&levelup;

	$khp = $khp_flg + int(rand($kn_3));
	if($khp > $kmaxhp) { $khp = $kmaxhp; }
	if($khp <= 0) { $khp = $kmaxhp; }

	&regist;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&iheader;}
	else{&header;}

	print "<h1>$knameは、$mnameに戦いを挑んだ！！</h1><hr size=0><p>\n";
	print "<embed src=\"$mons1_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if($win) { print "$comment<p>$knameは、$mexの経験値を手に入れた。<b>$gold</b>G手に入れた。</p>\n"; }
	else { print "$comment<p>$knameは、$mexの経験値を手に入れた。お金が半分になった・・・(涙)</p>\n"; }

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ifooter;}
	else{&footer;}

	$battle_flag=0;

	exit;
}
__SUB__

	boss => <<'__SUB__',
#----------------------------#
#  レジェンドプレイスでの戦闘#
#----------------------------#
sub boss {
	if($battle_flag) { &error("現在戦闘中です。少しお待ちになってから戦闘してください。"); }

	$battle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { last; }
	}

$ztime = time();
$ztime = $ztime - $kdate;
$k_time = $m_time - $ztime;
if($k_time > 0) { &error("疲れています、$k_time秒まってください・・<BR><form action=$script method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=log_in><input type=submit class=btn value=引き返す></form><form action=$scriptm method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=boss$suzi><input type=submit class=btn value=先に進む></form>\n"); }


	if(!$kmori) { &error("一度キャラクターと闘ってください"); }
	if($in{'id'} ne "$kid" || $in{'pass'} ne "$kpass") {&error("オープンエラー、ID・パスワードが正しくありません。");}

	if($kitem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($ci_no,$ci_name,$ci_dmg,$ci_gold,$ci_plus) = split(/<>/);
			if($kitem eq $ci_no) { last; }
		}
	}

	if($kdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($cd_no,$cd_name,$cd_dmg,$cd_gold,$cd_plus) = split(/<>/);
			if($kdef eq $cd_no) { last; }
		}
	}

	if($kacsno){
		open(IN,"$acs_file");
		@log_acs = <IN>;
		close(IN);

		foreach(@log_acs){
			($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
			if($kacsno eq "$a_no"){last; }
		}
	}

	&acs_add;

	open(IN,"$bmonster");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = $kmori;

	($mname,$mex,$mrand,$msp,$mdmg,$mkahi,$monstac,$mons_ritu) = split(/<>/,$MONSTER[$r_no]);

	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$khp_flg = $khp;
	$mhp = int(rand($mrand)) + $msp;
	$mhp_flg = $mhp;

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$dmg1 = $klv * (int(rand(5)) + 1);
		$dmg2 = $mdmg + int(rand($mrand));
		$clit1 = "";
		$clit2 = "";
		$sake1 = 0;
		$sake2 = 0;
		$com1 = "";
		$com2 = "$mnameが襲いかかった！！";
		$kawasi1 = "";
		$kawasi2 = "";
		$hpplus1 = 0;
		$hpplus2 = 0;
		$kaihuku1 = "";
		$kaihuku2 = "";

	&tyousensya;
	&tyosenwaza;

	if($monstac > 0){if($mons_ritu > int(rand(100))){&mons_waza;}}
	&acs_waza;

	&mons_clt;
	&mons_kaihi;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&imonsbattle_sts;}
	else{&monsbattle_sts;}

		$khp_flg = $khp_flg - $dmg2 - $dmgme1 + $hpplus1;
		if($khp_flg > $kmaxhp){$khp_flg = $kmaxhp;}
		$mhp = $mhp - $dmg1 + $hpplus2;
		if($mhp > $mhp_flg){$mhp = $mhp_flg;}

		if($mhp <= 0) { $win = 1; last; }
		elsif($khp_flg <= 0) { $win = 0; last; }
		else{ $win = 2;}

		$i++;
		$j++;
	}

	$kmori_w = $kmori;
	if($win==1) {
		$ktotal += 1;
		$kkati += 1;
		$khp_flg += int(rand($kmaxhp /10));
		$kex = $kex + $mex;
		$kmori -= 1;
		if($kmori == 0 and $ranks == 1){$kmoriturn=$ranks;}
                if($kmori == 0 and $ranks == 2){$kmoriturn=$ranks;}
                if($kmori == 0 and $ranks == 3){$kmoriturn=$ranks;}
                if($kmori == 0 and $ranks == 4){$kmoriturn=$ranks;}
		$gold = $gold + int(rand(10)+1) * int($mhp_flg);
		$kgold += $gold;
		if($kgold < 0){$kgold = 0;}
		if($kgold > $gold_max){$kgold = $gold_max;}
		if($kmori == 0) {
			$comment = "<b><font color=yellow size=5>$knameは、レジェンドプレイスを攻略した！！攻略者ランキングに登録されます！！</font></b><P/>";
		}else{
			$comment = "<b><font size=5>$knameは、戦闘に勝利した！！ＨＰが少し回復した♪</font></b><P/>";
		}
	}elsif($win==2) {
		$ktotal += 1;
		$kex = $kex + $mex;
		$kmons -= 1;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、逃げ出した・・・♪</font></b><P/>";
	}else{
		$ktotal += 1;
		$mex = 1;
		$kex = $kex + $mex;
		$kmori = $boss;
		$kgold = int(($kgold / 10));
		$comment = "<b><font size=5>$knameは、戦闘に負けた・・・。</font></b><P/>";
	}

	&acs_sub;

	&levelup;

	$khp = $khp_flg + int(rand($kn_3));
	if($khp > $kmaxhp) { $khp = $kmaxhp; }
	if($khp <= 0) { $khp = $kmaxhp; }

	&regist;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&iheader;}
	else{&header;}

	$boss_h = int($boss /2);	
	if($kmori == 0){print "<embed src=\"$last_boss_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";}
	else{
		if($kmori >= $boss_h){
			print "<embed src=\"$boss_midi1\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";}
		else{
			print "<embed src=\"$boss_midi2\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";}
	}
	print <<"_BATTLE_";
<FONT SIZE="5" COLOR="#7777DD"><B>レジェンドプレイス</B></FONT><br>
<P>
<B><CENTER><FONT SIZE="6">$mname</B>が現れた！</FONT></CENTER>
<BR>
<BR>
_BATTLE_

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if($win) { print "$comment<p>$knameは、$mexの経験値を手に入れた。<b>$gold</b>G手に入れた。</p>\n"; }
	else { print "$comment<p>$knameは、$mexの経験値を手に入れた。お金が１０分の１になった・・・(涙)</p>\n"; }

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ibossfooter;}
	else{&bossfooter;}

	$battle_flag=0;

	exit;
}
__SUB__

	genei => <<'__SUB__',
#----------------------#
#  幻影の城の戦闘      #
#----------------------#
sub genei {
	if($battle_flag) { &error("現在戦闘中です。少しお待ちになってから戦闘してください。"); }

	$battle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { last; }
	}

	if($klv < $genei_low) {$monster_file=$low_monster;}
	elsif($klv < $genei_high) {$monster_file=$normal_monster;}
	else{$monster_file=$high_monster;}

	if(!$kmons) { &error("一度キャラクターと闘ってください"); }
	if($klv%3 != 0){ &error("もう消えてしまって行けませんでした"); }
	if($in{'id'} ne "$kid" || $in{'pass'} ne "$kpass") {&error("オープンエラー、ID・パスワードが正しくありません。");}

	if($kitem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($ci_no,$ci_name,$ci_dmg,$ci_gold,$ci_plus) = split(/<>/);
			if($kitem eq $ci_no) { last; }
		}
	}

	if($kdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($cd_no,$cd_name,$cd_dmg,$cd_gold,$cd_plus) = split(/<>/);
			if($kdef eq $cd_no) { last; }
		}
	}

	if($kacsno){
		open(IN,"$acs_file");
		@log_acs = <IN>;
		close(IN);

		foreach(@log_acs){
			($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
			if($kacsno eq "$a_no"){last; }
		}
	}

	&acs_add;

	open(IN,"$monster_file");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = int(rand($r_no));

	($mname,$mex,$mrand,$msp,$mdmg,$mkahi,$monstac,$mons_ritu) = split(/<>/,$MONSTER[$r_no]);

	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$khp_flg = $khp;
	$mhp = int(rand($mhp)) + $msp + $msp;
	$mhp_flg = $mhp;

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$dmg1 = $klv * (int(rand(5)) + 1);
		$dmg2 = $mdmg + int(rand($msp)) + $cd_dmg;
		$clit1 = "";
		$clit2 = "";
		$sake1 = 0;
		$sake2 = 0;
		$com1 = "";
		$com2 = "$mnameが襲いかかった！！";
		$kawasi1 = "";
		$kawasi2 = "";
		$hpplus1 = 0;
		$hpplus2 = 0;
		$kaihuku1 = "";
		$kaihuku2 = "";

	&tyousensya;
	&tyosenwaza;

	if($monstac > 0){if($mons_ritu > int(rand(100))){&mons_waza;}}
	&acs_waza;

	&mons_clt;
	&mons_kaihi;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&imonsbattle_sts;}
	else{&monsbattle_sts;}

		$khp_flg = $khp_flg - $dmg2 - $dmgme1 + $hpplus1;
		if($khp_flg > $kmaxhp){$khp_flg = $kmaxhp;}
		$mhp = $mhp - $dmg1 + $hpplus2;
		if($mhp > $mhp_flg){$mhp = $mhp_flg;}

		if($mhp <= 0) { $win = 1; last; }
		elsif($khp_flg <= 0) { $win = 0; last; }
		else{ $win = 2;}

		$i++;
		$j++;
	}

	if($win==1) {
		$ktotal += 1;
		$kkati += 1;
		$mex +=$mex; 
		$kex +=$mex;
		$kmons -= 1;
		$comment = "<b><font size=5>$knameは、戦闘に勝利した！！</font></b><P/>";
		if(int(rand(3)) == 0){
			$gold = $gold + int(rand(1000)+1) * int($mhp_flg);
			$comment .= "<b><font size=5 color=red>財宝を発見した！！！！</font></b>";
		}else{
			$gold = $gold + int(rand(10)+1) * int($mhp_flg);
			$comment .= "<b><font size=5>辺りに財宝は見つからなかった・・・。</font></b>";
			}
		$kmori = $boss;
		$kgold += $gold;
		if($kgold < 0){$kgold = 0;}
		if($kgold > $gold_max){$kgold = $gold_max;}
	}elsif($win==2) {
		$ktotal += 1;
		$kex = $kex + $mex;
		$kmons -= 1;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、逃げ出した・・・♪</font></b><P/>";
	}else{
		$ktotal += 1;
		$mex = 1;
		$kex = $kex + $mex;
		$kmons -= 1;
		$kmori = $boss;
		$kgold = int(($kgold / 2));
		$comment = "<b><font size=5>$knameは、戦闘に負けた・・・。</font></b><P/>";
	}

	&acs_sub;

	&levelup;

	$khp = $khp_flg + int(rand($kn_3));
	if($khp > $kmaxhp) { $khp = $kmaxhp; }
	if($khp <= 0) { $khp = $kmaxhp; }

	&regist;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&iheader;}
	else{&header;}

	print "<embed src=\"$mons2_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	print <<"_BATTLE_";
<FONT SIZE="5" COLOR="#7777DD"><B>幻影の城</B></FONT>
<BR>
<P>
<B><CENTER><FONT SIZE="6">$mname</B>が現れた！</FONT></CENTER>
<BR>
<BR>
_BATTLE_

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if($win) { print "$comment<p>$knameは、$mexの経験値を手に入れた。<b>$gold</b>G手に入れた。</p>\n"; }
	else { print "$comment<p>$knameは、$mexの経験値を手に入れた。お金が半分になった・・・(涙)</p>\n"; }

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ifooter;}
	else{&footer;}

	$battle_flag=0;

	exit;
}
__SUB__

	isekiai => <<'__SUB__',
#----------------------#
#  異世界での戦闘      #
#----------------------#
sub isekiai {
	if($battle_flag) { &error("現在戦闘中です。少しお待ちになってから戦闘してください。"); }

	$battle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { last; }
	}

	if(!$kmons) { &error("一度キャラクターと闘ってください"); }
	if($in{'id'} ne "$kid" || $in{'pass'} ne "$kpass") {&error("オープンエラー、ID・パスワードが正しくありません。");}

	if($kitem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($ci_no,$ci_name,$ci_dmg,$ci_gold,$ci_plus) = split(/<>/);
			if($kitem eq $ci_no) { last; }
		}
	}

	if($kdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($cd_no,$cd_name,$cd_dmg,$cd_gold,$cd_plus) = split(/<>/);
			if($kdef eq $cd_no) { last; }
		}
	}

	if($kacsno){
		open(IN,"$acs_file");
		@log_acs = <IN>;
		close(IN);

		foreach(@log_acs){
			($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
			if($kacsno eq "$a_no"){last; }
		}
	}

	&acs_add;

	open(IN,"$isekai_monster");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = int(rand($r_no));

	($mname,$mex,$mrand,$msp,$mdmg,$mkahi,$monstac,$mons_ritu) = split(/<>/,$MONSTER[$r_no]);

	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$khp_flg = $khp;
	$mhp = int(rand($mrand)) + $msp;
	$mhp_flg = $mhp;

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$dmg1 = $klv * (int(rand(5)) + 1);
		$dmg2 = $mdmg + int(rand($mrand));
		$sake1 = 0;
		$sake2 = 0;
		$clit1 = "";
		$clit2 = "";
		$com1 = "";
		$com2 = "$mnameが襲いかかった！！";
		$kawasi1 = "";
		$kawasi2 = "";
		$hpplus1 = 0;
		$hpplus2 = 0;
		$kaihuku1 = "";
		$kaihuku2 = "";

	&tyousensya;
	&tyosenwaza;

	if($monstac > 0){if($mons_ritu > int(rand(100))){&mons_waza;}}
	&acs_waza;

	&mons_clt;
	&mons_kaihi;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&imonsbattle_sts;}
	else{&monsbattle_sts;}

		$khp_flg = $khp_flg - $dmg2 - $dmgme1 + $hpplus1;
		if($khp_flg > $kmaxhp){$khp_flg = $kmaxhp;}
		$mhp = $mhp - $dmg1 + $hpplus2;
		if($mhp > $mhp_flg){$mhp = $mhp_flg;}

		if($mhp <= 0) { $win = 1; last; }
		elsif($khp_flg <= 0) { $win = 0; last; }
		else{ $win = 2;}

		$i++;
		$j++;
	}

	if($win==1) {
		$ktotal += 1;
		$kkati += 1;
		$kex = $kex + $mex;
		$kmori = $boss;
		$gold = $gold + int(rand(100)+1) * int($mhp_flg);
		$kgold += $gold;
		if($kgold > $gold_max){$kgold = $gold_max;}
		if($kgold < 0){$kgold = 0;}
 		$comment = "<b><font size=5>$knameは、戦闘に勝利した！！</font></b><P/>";
	}elsif($win==2) {
		$ktotal += 1;
		$kmons -= 1;
		$kex = $kex + $mex;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、逃げ出した・・・♪</font></b><P/>";
	}else{
		$ktotal += 1;
		$mex = 1;
		$kex = $kex + $mex;
		$kmori = $boss;
		$kgold = int(($kgold / 100));
		$comment = "<b><font size=5>$knameは、戦闘に負けた・・・。</font></b><P/>";
	}

	&acs_sub;

	&levelup;

	$khp = $khp_flg + int(rand($kn_3));
	if($khp > $kmaxhp) { $khp = $kmaxhp; }
	if($khp <= 0) { $khp = $kmaxhp; }

	&regist;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&iheader;}
	else{&header;}

	print "<embed src=\"$mons3_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	print <<"_BATTLE_";
<FONT SIZE="5" COLOR="#7777DD"><B>異世界</B></FONT>
<BR>
<P>
<B><CENTER><FONT SIZE="6">$mname</B>が現れた！</FONT></CENTER>
<BR>
<BR>
_BATTLE_

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if($win) { print "$comment<p>$knameは、$mexの経験値を手に入れた。<b>$gold</b>G手に入れた。</p>\n"; }
	else { print "$comment<p>$knameは、$mexの経験値を手に入れた。お金が１００分の１になった・・・(涙)</p>\n"; }

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ifooter;}
	else{&footer;}

	$battle_flag=0;

	exit;
}
__SUB__

	footer => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {
	if($refresh and !$win and $mode eq 'battle') {
		print "【<b><a href=\"http\:\/\/$wurl\">チャンプのホームページへ</a></b>】\n";
	}else{
		if($mode ne ""){
			print "<a href=\"$scripto\">TOPページへ</a>\n";
		}
		if($kid and $mode ne 'log_in' and $mode ne 'tensyoku' and $mode ne 'yado') { 
			print " / <a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">ステータス画面へ</a>\n";
		}
		if($mode eq 'kunren') { 
			print " / <a href=\"$script?mode=log_in&id=$pid&pass=$ppass\">ステータス画面へ</a>\n";
		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	 print "FFA Emilia・いく改ver1.00 remodeling by <a href=\"http://www3.big.or.jp/~icu/\" target=\"_top\">いく</a><br>\n";
	 print "画像提供 by <a href=\"http://www.wisnet.ne.jp/~jnkw/index.html\" target=\"_top\">Jinkun</a><br>\n";
	print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
	print "壁紙供給 by <a href=\"http://cg-i.bird.to/\" target=\"_top\">Loop</a><br>\n";
	print "$verg edit by <a href=\"http://www.gun-online.com/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	bossfooter => <<'__SUB__',
#----------------------#
#　BossHTMLのフッター　#
#----------------------#
sub bossfooter {
	if($refresh and !$win and $ranks) {
		print "<form action=$script method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=log_in><input type=submit class=btn value=ステータス画面へ></form>\n";
	}else{
		if($ranks and $kmori > 0 and $win==1){
			print "<form action=$script method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=log_in><input type=submit class=btn value=ステータス画面へ></form>\n";
			print "<form action=$scriptm method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=boss$suzi><input type=submit class=btn value=先に進む></form>\n";
		}
		if($kmori <= 0 or $win!=1) { 
			print " / <form action=$script method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=log_in><input type=submit class=btn value=ステータス画面へ></form>\n";		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
#        
	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	header => <<'__SUB__',
#------------------#
#  HTMLのヘッダー  #
#------------------#
sub header {
	print "Content-type: text/html\n\n";
	if($ranks) {
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<SCRIPT Language="JavaScript" src="$java_script"></SCRIPT>
EOM

	if($access_flg) {
	print <<"EOM";
<SCRIPT language="JavaScript">
<!--
if(parent.location == location) location = "$top_url";
if(document.referrer =="") location = "$top_url";
//-->
</SCRIPT>
EOM
	}
	print <<"EOM";
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
EOM
	$boss_h = int($boss /2);	
	if($kmori == 0){print "background-image : url($last_back);\n";}
	else{
		if($kmori_w >= $boss_h){
			print "background-image : url($boss_back);\n";}
		else{
			print "background-image : url($boss2_back);\n";}
	}
	print <<"EOM";
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:8px;$font_name;color:$red;}
-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	$boss_h = int($boss /2);	
	if($kmori == 0){print "<body background=\"$last_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";}
	else{
		if($kmori_w >= $boss_h){
			print "<body background=\"$boss_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";}
		else{
			print "<body background=\"$boss2_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";}
	}
	}elsif($mode eq 'genei') {
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<SCRIPT Language="JavaScript" src="$java_script"></SCRIPT>
EOM

	if($access_flg) {
	print <<"EOM";
<SCRIPT language="JavaScript">
<!--
if(parent.location == location) location = "$top_url";
if(document.referrer =="") location = "$top_url";
//-->
</SCRIPT>
EOM
	}
	print <<"EOM";
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
  background-image : url($siro_back);
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:8px;$font_name;color:$red;}
-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$siro_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	}elsif($mode eq 'isekiai') {
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<SCRIPT Language="JavaScript" src="$java_script"></SCRIPT>
EOM

	if($access_flg) {
	print <<"EOM";
<SCRIPT language="JavaScript">
<!--
if(parent.location == location) location = "$top_url";
if(document.referrer =="") location = "$top_url";
//-->
</SCRIPT>
EOM
	}
	print <<"EOM";
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
  background-image : url($isekai_back);
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:8px;$font_name;color:$red;}
-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$isekai_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	}else{
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<SCRIPT Language="JavaScript" src="$java_script"></SCRIPT>
EOM

	if($access_flg) {
	print <<"EOM";
<SCRIPT language="JavaScript">
<!--
if(parent.location == location) location = "$top_url";
if(document.referrer =="") location = "$top_url";
//-->
</SCRIPT>
EOM
	}
	print <<"EOM";
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
  background-image : url($mons_back);
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:8px;$font_name;color:$red;}
-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$mons_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	}
}
__SUB__

	set_cookie => <<'__SUB__',
#------------------#
#  クッキーの発行  #
#------------------#
sub set_cookie {
	# クッキーは60日間有効
	local($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+60*24*60*60);

	@month=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);
	$cook="id<>$cookie_id\,pass<>$cookie_pass";
	print "Set-Cookie: FFADV=$cook; expires=$gmt\n";
}
__SUB__

	ifooter => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub ifooter {
	if($refresh and !$win and $mode eq 'ibattle') {
		print "【<b><a href=\"http\:\/\/$wurl\">&#63904;</a></b>】\n";
	}else{
		if($mode ne ""){
			print "<a href=\"$scripto\">TOP</a>\n";
		}
		if($kid and $mode ne 'ilog_in' and $mode ne 'itensyoku' and $mode ne 'iyado') { 
			print " / <a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>\n";
		}
		if($mode eq 'kunren') { 
			print " / <a href=\"$script?mode=log_in&id=$pid&pass=$ppass\">&#63873;</a>\n";
		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	ibossfooter => <<'__SUB__',
#----------------------#
#　BossHTMLのフッター　#
#----------------------#
sub ibossfooter {
	if($refresh and !$win and $mode eq 'boss') {
		print "【<b><a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a></b>】\n";
	}else{
		if($mode eq 'boss' and $kmori > 0 and $win==1){
			print "<form action=$script method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=log_in><input type=submit class=btn value=ステータス画面へ></form>\n";
			print " / <form action=$scriptm method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=boss$suzi><input type=submit class=btn value=先に進む></form>\n";
		}
		if($kmori <= 0 or $win!=1) { 
			print " / <a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>\n";
		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	iheader => <<'__SUB__',
#------------------#
#  HTMLのヘッダー  #
#------------------#
sub iheader {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$mons_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
}
__SUB__

	monsbattle_sts => <<'__SUB__',
#------------------#
#　戦闘状況      　#
#------------------#
sub monsbattle_sts {

	# 能力値バーの詳しい幅設定
	$hit_ritu = int(($kn_4 / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($kn_5/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($klp / 15)) + 10 + $kcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}
	$ci_plus += $a_hitup;
	$cd_plus += $a_kaihiup;
	$bwhit   = int(0.5 * ($hit_ritu + $ci_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $cd_plus));
	$bwwaza  = int(1 * ($waza_ritu + $a_wazaup));
	if($bwhit > 200){$bwhit = 200;}
	if($bwkaihi > 200){$bwkaihi = 200;}
	if($bwwaza > 200){$bwwaza = 200;}

	if($i == 1){
		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0>
<TR>
	<TD COLSPAN="3" ALIGN="center">
	$iターン
	</TD>
</TR>
<TR>
	<TD ALIGN="center">
	<IMG SRC="$img_path/$chara_img[$kchara]"><table width="100%">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$ci_name</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$cd_name</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$a_name</td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $ci_plus%</b></td></tr>
<tr><td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><br><b>$kaihi_ritu + $cd_plus%</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $a_wazaup%</b></td></tr>
</table>
	</TD>
	</TR>
<TR>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
	<TD CLASS="b1" id="td2">
	職業
	</TD>
	<TD CLASS="b1" id="td2">
	LV
	</TD>
</TR>
<TR>
	<TD class="b2">
	$kname
	</TD>
	<TD class="b2">
	$khp_flg\/$kmaxhp
	</TD>
	<TD class="b2">
	$chara_syoku[$ksyoku]
	</TD>
	<TD class="b2">
	$klv
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT SIZE=5 COLOR="#9999DD">VS</FONT>
</TD>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
</TR>
<TR>
	<TD class="b2">
	$mname
	</TD>
	<TD class="b2">
	$mhp/$mhp_flg
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>$com1 $clit1 $kawasi2 $mname に <font class="yellow">$dmg1</font> のダメージを与えた。<font class="yellow">$kaihuku1</font></p>
<p>$com2 $clit2 $kawasi1 $kname に <font class="red">$dmg2</font> のダメージを与えた。<font class="yellow">$kaihuku2</font></p>
EOM
	}else{
		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0>
<TR>
	<TD COLSPAN="3" ALIGN="center">
	$iターン
	</TD>
</TR>
<TR>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
</TR>
<TR>
	<TD class="b2">
	$kname
	</TD>
	<TD class="b2">
	$khp_flg\/$kmaxhp
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT SIZE=5 COLOR="#9999DD">VS</FONT>
</TD>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
</TR>
<TR>
	<TD class="b2">
	$mname
	</TD>
	<TD class="b2">
	$mhp/$mhp_flg
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>$com1 $clit1 $kawasi2 $mname に <font class="yellow">$dmg1</font> のダメージを与えた。<font class="yellow">$kaihuku1</font></p>
<p>$com2 $clit2 $kawasi1 $kname に <font class="red">$dmg2</font> のダメージを与えた。<font class="yellow">$kaihuku2</font></p>
EOM
}
}
__SUB__

	imonsbattle_sts => <<'__SUB__',
#------------------#
#　戦闘状況      　#
#------------------#
sub imonsbattle_sts {

	if($i == 1){
$battle_date[$j] = <<"EOM";
$iターン<br>
$kname：<br>
<IMG SRC="$img_pathi/$chara_img[$kchara]"><br>
&#63889;:$khp_flg<br>
$mname：<br>
&#63814;:$mhp<br>
$com1 <font color=$yellow>$dmg1</font>ダメージ>$mname<font color=$yellow>$kaihuku1</font><br>
$com2 <font color=$red>$dmg2</font>ダメージ>$kname<font color=$yellow>$kaihuku2</font><br>
EOM
	}else{
if($dmg1 ==0 and $dmg2 ==0){
$battle_date[$j] = <<"EOM";
$iターン<br><hr>
EOM
}else{
$battle_date[$j] = <<"EOM";
$iターン<br>
$kname：<br>
&#63889;:$khp_flg<br>
$mname：<br>
&#63814;:$mhp<br>
$com1 <font color=$yellow>$dmg1</font>ダメージ>$mname<font color=$yellow>$kaihuku1</font><br>
$com2 <font color=$red>$dmg2</font>ダメージ>$kname<font color=$yellow>$kaihuku2</font><br>
EOM
}
}
}
__SUB__

	mons_clt => <<'__SUB__',
#------------------#
#魔物クリィティカル#
#------------------#
sub mons_clt{
	#クリティカル率算出
	$kclt_ritu = 100-int($khp_flg / $kmaxhp * 100);
	$mclt_ritu = 100-int($mhp / $mhp_flg * 100);

	# 封印球の効果
	if($a_kouka == 19){
		if($mode eq 'boss' or $mode eq 'isekiai'){$com1 .="<P><font class=\"red\" size=3>$a_nameが光を放つ！！$mnameには効かなかった！！</font><P/>";}
		else{if(int(rand(2))==0){$monstac =0;$com1 .="<P><font class=\"yellow\" size=3>$a_nameが光を放つ！！$mnameの必殺技を封じ込めた！！</font><P/>";}}
		}
	if($kclt_ritu > int(rand(100))) {
		$com1 .= "<font color=\"$red\" size=5>クリティカル！！「$kwaza」</font><P/>";
		$dmg1 = $dmg1 * 3;
		}
	if($mclt_ritu > int(rand(200))) {
		$com2 .= "<font color=\"$red\">クリティカル！！</font><P/>";
		$dmg2 = $dmg2 + $cd_dmg;
		}
}
__SUB__

	mons_kaihi => <<'__SUB__',
#------------------#
#魔物回避          #
#------------------#
sub mons_kaihi{

		#回避率計算
		$ci_plus += $a_hitup;
		$cd_plus += $a_kaihiup;
		$hit_ritu = int(($kn_4 / 10)+51) + $ci_plus;	

		$sake1 += int(($kn_5 / 20)) + $cd_plus;
		$sake2 += $mkahi - $hit_ritu;

		if($dmg2 < 0){$dmg2 = $dmg2;}
			elsif($dmg2 < $cd_dmg){$dmg2 = 0;}
			else{$dmg2 = $dmg2 - $cd_dmg;}
		#職業別防御ボーナス
		if($ksyoku > 17){$dmg2=int($dmg2/4);}
		elsif($ksyoku > 7){$dmg2=int($dmg2/2);}

		if(int($sake1) > int(rand(300))) {
			$dmg2 = 0;
			$kawasi1 = "<P><FONT SIZE=4 COLOR=\"$red\">$knameは身をかわした！</FONT>";
		}
		if(int($sake2) > int(rand(100))) {
			$dmg1 = 0;
			$kawasi2 = "<P><FONT SIZE=4 COLOR=\"$red\">$mnameは身をかわした！</FONT>";
		}

}
__SUB__

	mons_waza => <<'__SUB__',
#------------------#
#　魔物の技      　#
#------------------#
sub mons_waza {

	if($monstac == 1){
		$dmg1 = int($dmg1 * 0.1);
		$com2 .="<P><font class=\"yellow\">防御魔法マイティガード！！！</font><P/>";
		}
	if($monstac == 2){
		$hpplus2 = int(rand($mhp)) * 2;
		$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
		$dmg2 = 0;
		$com2 ="<P><font class=\"yellow\" size=5>白魔法ケアルガ！！！</font><P/>";
		}
	if($monstac == 3){
		$dmg2 += int(rand($mrand));
		$dmg2 += $cd_dmg;
		$sake1 -= 999999;
		$com2 .="<P><font class=\"red\" size=5>黒魔法ファイガ！！！</font><P/>";
		}
	if($monstac == 4){
		$dmg2 += int(rand($mrand));
		$dmg2 += $cd_dmg;
		$sake1 -= 999999;
		$com2 .="<P><font class=\"blue\" size=5>黒魔法ブリザガ！！！</font><P/>";
		}
	if($monstac == 5){
		$dmg2 += int(rand($mrand));
		$dmg2 += $cd_dmg;
		$sake1 -= 999999;
		$com2 .="<P><font class=\"yellow\" size=5>黒魔法サンダガ！！！</font><P/>";
		}
	if($monstac == 6){
		$dmhit = int(rand(7))+1;
		$sake1 -= 999999;
		$dmg2 = int(rand($mrand)) * $dmhit;
		$dmg2 += $cd_dmg;
		$com2 .="<P><font class=\"red\" size=5>古代魔法メテオ！！！</font><font color=red>$dmhitヒット！！</font><P/>";
		}
	if($monstac == 7){
		$sake1 -= 999999;
		$dmg2 += int($khp_flg / 5);
		$com2 .="<P><font class=\"red\" size=5>重力魔法グラビガを発動！！！</font><P/>";
		}
	if($monstac == 8){
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand)) * 2;
		$dmg2 += $cd_dmg;
		$com2 .="<P><font class=\"red\" size=5>黒魔法クエイクを発動！！！</font><P/>";
		}
	if($monstac == 9){
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand)) * 3;
		$dmg2 += $cd_dmg;
		$com2 .="<P><font class=\"white\" size=5>禁断の魔法アルテマを発動！！！</font><P/>";
		}
	if($monstac == 10){
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand)) * 5;
		$dmg2 += $cd_dmg;
		$com2 .="<P><font class=\"blue\" size=5>青魔法ショック・ウェーブ・パルサーを発動！！！</font><P/>";
		}
	if($monstac == 11){
		if(int(rand(3))==0){
			$sake1 -= 999999;
			$dmg2 = $khp_flg;
			$dmg2 += $cd_dmg;
			$com2 .="<P><font class=\"red\" size=5>時空魔法デジョンを発動！！！</font><P/>";
		}else{
			$com2 .="<P><font class=\"red\" size=5>時空魔法デジョンを発動！！！失敗！！</font><P/>";
			}
		}
	if($monstac == 12){
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand));
		$dmg2 += $cd_dmg;
		$com2 .="<P><font class=\"red\" size=5>ファイア・ブレス！！！</font><P/>";
		}
	if($monstac == 13){
		if(int(rand(1))==0){
			$hpplus2 = int(rand($mrand)) * 2;
			$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
			$com2 ="<P><font class=\"yellow\" size=5>白魔法ケアルガ！！！</font><P/>";
		}else{
			$sake1 -= 999999;
			$dmg2 += int(rand($mrand)) * 3;
			$dmg2 += $cd_dmg;
			$com2 .="<P><font class=\"white\" size=5>禁断の魔法アルテマを発動！！！</font><P/>";
			}
		}
	if($monstac == 14){
		$tgold = int(rand($kgold /7));
		$gold -= $tgold;
		$com2 .="<P><font class=\"red\">お金を盗まれた！！$tgoldＧマイナス！！</font><P/>";
		}
	if($monstac == 15){
		$dmg2 += int(rand($mrand));
		$dmg2 += $cd_dmg;
		$hpplus2 = $dmg2;
		$sake1 -= 999999;
		$com2 .="<P><font classr=\"dark\" size=4>暗黒魔法ドレイン！！！</font><P/>";
		$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
		}
	if($monstac == 16){
		$dmg2 += int(rand($mrand)) * 7;
		$dmg2 += $cd_dmg;
		$sake1 -= 999999;
		$com2 .="<P><font class=\"white\" size=5>最強魔法アポガリプス！！！</font><P/>";
		}
	if($monstac == 17){
		if(int(rand(1199)) == 0){
		$sake1 -=999999;
		$dmg1 = 0;
		$dmg2 += int(rand($mrand)) ** 8; 
		$com2 ="<p><font class=\"red\" size =6>えりりんの甘いささやき！</font><p/>";}
		else{$hpplus1 = int(rand($msp)) * 8;
		$kaihuku2 .= "$kname のＨＰが $hpplus1 回復した！♪";
		$dmg1 = 0;
		$dmg2 = 0;
		$com2 ="<P><font class=\"yellow\" size=5>祝福のキス♪♪</font><P/>";}
		}
	if($monstac == 18){
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand))*3;
		$dmg2 += $cd_dmg*3;
		$com2 .="<P><font class=\"red\" size=5>メガ・フレア！！！</font><P/>";
		}
	if($monstac == 19){
		if(int(rand(5))==0){
			$hpplus2 = int(rand($mrand)) * 4;
			$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
			$com2 ="<P><font class=\"yellow\" size=5>ハァハァ。。。</font><P/>";
}
		else{
		$dmg2 += int(rand($mrand)) * 5;
		$dmg2 += $cd_dmg;
		$sake1 -= 999999;
		$com2 .="<P><font class=\"white\" size=5>ハァハァ。。。</font><P/>";}
		

		}
	if($monstac == 20){
		if(int(rand(2))==0){
			$sake1 -= 999999;
			$dmg2 = $khp_flg + $kmaxhp;
			$com2 .="<P><font class=\"red\" size=5>斬・鉄・剣！！！</font><font color =#cc6633 size = 5><br>「私に斬れぬものなどない」</font><P/>";
		}else{
		$dmg2 += int(rand($mrand)) * 10;
		$dmg2 += $cd_dmg;
			$com2 .="<P><font class=\"red\" size=5>斬・鉄・剣！！！</font><P/>";
			}
		}

	if($monstac == 21){
			$sake1 -= 999999;
			$ksex = int(rand(1.999));
		if($ksex == 1){$seibetu ="男";}
		elsif($ksex == 0){$seibetu ="女";}
			$com2 .="<P><font class=\"red\" size=5>性転換！！！</font><font color =#cc6633 size = 2><br>性別がランダムに変化する！$seibetuになった！</font><P/>";
		}

	if($monstac == 22){
			if(int(rand(2))==0){
			$kn_0a = int(rand(3));
			$kn_1a = int(rand(3));
			$kn_2a = int(rand(3));
			$kn_3a = int(rand(3));
			$kn_4a = int(rand(3));
			$kn_5a = int(rand(3));
			$kn_6a = int(rand(3));
			$klpa = int(rand(3));
			$kn_0 -= $kn_0a;
			$kn_1 -= $kn_1a;
			$kn_2 -= $kn_2a;
			$kn_3 -= $kn_3a;
			$kn_4 -= $kn_4a;
			$kn_5 -= $kn_5a;
			$kn_6 -= $kn_6a;
			$klp -= $klpa;
			$sake1 -= 499;
			$dmg2 += int(rand($mrand)) * 2;
			$com2 .="<P><font class=\"red\" size=5>臭い息！！！</font><font class =\"white\" size = 2><br>力が<font class =\"yellow\">$kn_0a</font>下がった。<br>魔力が<font class =\"yellow\">$kn_1a</font>下がった。<br>信仰心が<font class =\"yellow\">$kn_2a</font>下がった。<br>生命力が<font class =\"yellow\">$kn_3a</font>下がった。<br>器用さが<font class =\"yellow\">$kn_4a</font>下がった。<br>速さが<font class =\"yellow\">$kn_5a</font>下がった。<br>魅力が<font class =\"yellow\">$kn_6a</font>下がった。<br>カルマが<font class =\"yellow\">$klpa</font>下がった。</font><P/>";
}
			else{$dmg2 += int(rand($mrand)) * 10;
			$dmg2 += $cd_dmg;
			$com2 .="<P><font class=\"red\" size=5>臭い息！！！</font><P/>";
}}
}
__SUB__
);
}
