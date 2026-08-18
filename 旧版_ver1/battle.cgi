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
#     http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi 		#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require './jacode.pl';

# レジストライブラリの読み込み
require './regist.pl';

# 戦闘ライブラリの読み込み
require './battle.pl';
# チャンプ戦用ライブラリ読み込み
require './wbattle.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

#-----------------------------------------------------------------------------#
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

if($mode eq 'battle') { &battle; }
elsif($mode eq 'tatakai' or $mode eq 'katinuki') { &tatakai; }
exit;

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃   オートローダー
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sub AUTOLOAD {
	my $name = ($AUTOLOAD =~ /^main::(.+)$/)[0];
	($FLAG{'autoload'}++ > 50) && die $AUTOLOAD; # 念のため無限ループ防止
	unless (%SUB) {&SUBS};
	if (!$SUB{$name}) {
		&error("定義されていない関数($AUTOLOAD)が呼ばれました。"); exit;
	}
	eval $SUB{$name}; length($@) && &error("EVAL ERROR: $@ ($AUTOLOAD)");
	delete $SUB{$name}; goto &{'main::' . $name};
}

sub SUBS {
%SUB = (
	battle => <<'__SUB__',
#------------#
#  戦闘画面  #
#------------#
sub battle {
	if($battle_flag) { &error("現在戦闘中です。少しお待ちになってから戦闘してください。"); }

	$battle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@battle = <IN>;
	close(IN);
$hit=0;
	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq $kpass) {$hit=1;last; }
	}

	&read_winner;

	$ltime = time();
	$ltime = $ltime - $kdate;
	$vtime = $b_time - $ltime;
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	if($wid eq $kid) { &error("現在チャンプなので闘えません。"); }

	if($vtime > 0){
	if($ltime < $b_time or !$ktotal) { &error("あと$vtime秒間闘えません。"); }
			}
	&item_read;

	&acs_add;
	&wacs_add;

	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$khp_flg = $khp;
	$whp_flg = $whp;

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$dmg1 = $klv * (int(rand(3)) + 1);
		$dmg2 = $wlv * (int(rand(3)) + 1);
		$clit1 = "";
		$clit2 = "";
		$com1 = "";
		$com2 = "";
		$kawasi1 = "";
		$kawasi2 = "";
		$sake1 = 0;
		$sake2 = 0;
		$kclit = $khp_flg / 10;
		$wclit = $whp_flg / 10;
		$kmclit = $kmaxhp / 10;
		$wmclit = $wmaxhp / 10;
		$hpplus1 = 0;
		$hpplus2 = 0;
		$kaihuku1 = "";
		$kaihuku2 = "";

	&tyousensya;
	&winner;

	&tyosenwaza;
	&winwaza;

	&acs_waza;
	&wacs_waza;

	&battle_clt;
	&battle_kaihi;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ibattle_sts;}
	else{&battle_sts;}

		$khp_flg = $khp_flg - $dmg2 + $hpplus1;
		if($khp_flg > $kmaxhp){$khp_flg = $kmaxhp;}
		$whp_flg = $whp_flg - $dmg1 + $hpplus2;
		if($whp_flg > $wmaxhp){$whp_flg = $wmaxhp;}

		if($whp_flg <= 0 and $khp_flg > 0) { $win = 1; last; }
		elsif($khp_flg <= 0 and $whp_flg > 0) { $win = 0; last; }
		elsif($khp_flg <= 0 and $whp_flg <= 0) { $win = 2; last; }
		else{ $win = 3;}

		$i++;
		$j++;
	}

	&sentoukeka;

	&acs_sub;
	&wacs_sub;

	&levelup;

	$khp = $khp_flg + int(rand($kn_3));
	if($khp > $kmaxhp) { $khp = $kmaxhp; }
	$whp = $whp_flg + int(rand($wn_3));
	if($whp > $wmaxhp) { $whp = $wmaxhp; }
	if($khp <= 0) { $khp = 1; }
	if($whp <= 0) { $whp = 1; }
	$kgold += $gold;
	if($kgold < 0){$kgold = 0;}
	if($kgold > $gold_max){$kgold = $gold_max;}

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	if($win==1 or $win==2){
		@new=();
		open(IN,">$winner_file");
		@winnew = <IN>;
		unshift(@new,"$kid<>$kpass<>$ksite<>$kurl<>$kname<>$ksex<>$kchara<>$kn_0<>$kn_1<>$kn_2<>$kn_3<>$kn_4<>$kn_5<>$kn_6<>$ksyoku<>$khp<>$kmaxhp<>$kex<>$klv<>$wgold<>$klp<>$ktotal<>$kkati<>$kwaza<>$kitem<>$kmons<>$host<>$date<>$win<>$wsite<>$wurl<>$wname<>$kmori<>$kdef<>$ktac<>$kacsno<>$kmoriturn<>$kcllv<>$ks0<>$ks1<>$ks2<>$ks3<>$ks4<>$ks5<>$ks6<>$ks7<>$ks8<>$ks9<>$ks10<>$ks11<>$ks12<>$ks13<>$ks14<>$ks15<>$ks16<>$ks17<>$ks18<>$ks19<>$ks20<>$ks21<>$ks22<>$ks23<>$ks24<>$ks25<>$ks26<>$ks27<>$ks28<>$ks29<>$ks30<>$krec<>\n");
		print IN @new;
		close(IN);

	}elsif($win==0){
		$wcount += 1;
		$whp += int($wmaxhp / 10);
		if($whp > $wmaxhp){$whp = $wmaxhp;}
		@new=();
		open(IN,">$winner_file");
		@winnew = <IN>;
		unshift(@new,"$wid<>$wpass<>$wsite<>$wurl<>$wname<>$wsex<>$wchara<>$wn_0<>$wn_1<>$wn_2<>$wn_3<>$wn_4<>$wn_5<>$wn_6<>$wsyoku<>$whp<>$wmaxhp<>$wex<>$wlv<>$wgold<>$wlp<>$wtotal<>$wkati<>$wwaza<>$witem<>$wmons<>$host<>$date<>$wcount<>$ksite<>$kurl<>$kname<>$wmori<>$wdef<>$wtac<>$wacsno<>$wmoriturn<>$wcllv<>$ws0<>$ws1<>$ws2<>$ws3<>$ws4<>$ws5<>$ws6<>$ws7<>$ws8<>$ws9<>$ws10<>$ws11<>$ws12<>$ws13<>$ws14<>$ws15<>$ws16<>$ws17<>$ws18<>$ws19<>$ws20<>$ws21<>$ws22<>$ws23<>$ws24<>$ws25<>$ws26<>$ws27<>$ws28<>$ws29<>$ws30<>$wrec<>\n");
		print IN @new;
		close(IN);

		open(IN,"$recode_file");
		@recode = <IN>;
		close(IN);

		($count,$name) = split(/<>/,$recode[0]);

		if($wcount > $count) {
			open(OUT,">$recode_file");
			print OUT "$wcount<>$wname<>$wsite<>$wurl<>\n";
			close(IN);
		}
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }


	if($khp == 1) { $khp = $kmaxhp; }

	&regist;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {if($refresh and !$win) { &iheader2; } else { &iheader; }}
	else{if($refresh and !$win) { &header2; } else { &header; }}

	print "<h1>$knameは、$wnameに戦いを挑んだ！！</h1><hr size=0><p>\n";
	print "<embed src=\"$battle_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}

	if($win) { print "$comment<p>$knameは、<b>$exp</b>の経験値を手に入れた。$wnameの賞金<b>$gold</b>G手に入れた。</p>\n"; }
	else { print "$comment<p>$knameは、<b>$exp</b>の経験値を手に入れた。お金が半分になった・・・(涙)</p>\n"; }

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ifooter;}
	else{&footer;}

	$battle_flag=0;

	exit;
}
__SUB__

	tatakai => <<'__SUB__',
#--------------------#
#  キャラ選択バトル  #
#--------------------#
sub tatakai {

	if($battle_flag) { &error("現在戦闘中です。少しお待ちになってから戦闘してください。"); }

	$battle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@battle = <IN>;
	close(IN);

$hit=0;
	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq $kpass) { $hit=1;last; }
	}

	if($mode eq 'tatakai') {&read_select;}
	elsif($mode eq 'katinuki') {&read_nuki;}

	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

$ztime = time();
$ztime = $ztime - $kdate;
$k_time = $b_time - $ztime;
if($k_time > 0) { &error("あと$k_time秒お待ちください。<form action=$script method=post><input type=hidden name=id value=$in{'id'}><input type=hidden name=pass value=$in{'pass'}><input type=hidden name=mode value=log_in><input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value=街に戻る></form><br> <form action=$scriptb method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=no value=$in{'no'}><input type=hidden name=mode value=katinuki><input type=submit class=btn value=第$in{'no'}回戦に出場></form>\n"); }

	if($chanp_milit) {
		if($kurl eq $lurl) { &error("チャンプと戦った直後なので疲れて闘えません"); }
	}

	&item_read;

	&acs_add;
	&wacs_add;

	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$khp_flg = $khp;
	$whp_flg = $wmaxhp;

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
		$dmg1 = $klv * (int(rand(3)) + 1);
		$dmg2 = $wlv * (int(rand(3)) + 1);
		$clit1 = "";
		$clit2 = "";
		$com1 = "";
		$com2 = "";
		$kawasi1 = "";
		$kawasi2 = "";
		$sake1 = 0;
		$sake2 = 0;
		$hpplus1 = 0;
		$hpplus2 = 0;
		$kaihuku1 = "";
		$kaihuku2 = "";

	&tyousensya;
	&winner;

	&tyosenwaza;
	&winwaza;

	&acs_waza;
	&wacs_waza;

	&battle_clt;
	&battle_kaihi;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ibattle_sts;}
	else{&battle_sts;}

		$khp_flg = $khp_flg - $dmg2 + $hpplus1;
		if($khp_flg > $kmaxhp){$khp_flg = $kmaxhp;}
		$whp_flg = $whp_flg - $dmg1 + $hpplus2;
		if($whp_flg > $wmaxhp){$whp_flg = $wmaxhp;}

		if($whp_flg <= 0 and $khp_flg > 0) { $win = 1; last; }
		elsif($khp_flg <= 0 and $whp_flg > 0) { $win = 0; last; }
		elsif($khp_flg <= 0 and $whp_flg <= 0) { $win = 2; last; }
		else{ $win = 3;}

		$i++;
		$j++;
	}

	&sentoukeka;

	&acs_sub;
	&wacs_sub;

	&levelup;

	$khp = $khp_flg + int(rand($kn_3));
	if($khp > $kmaxhp) { $khp = $kmaxhp; }
	$whp = $whp_flg + int(rand($wn_3));
	if($whp > $wmaxhp) { $whp = $wmaxhp; }
	if($khp <= 0) { $khp = $kmaxhp; }
	if($whp <= 0) { $whp = 1; }
	$kgold += $gold;
	if($kgold < 0){$kgold = 0;}
	if($kgold > $gold_max){$kgold = $gold_max;}

	&regist;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {if($refresh and !$win) { &iheader2; } else { &iheader; }}
	else{if($refresh and !$win) { &header2; } else { &header; }}

	if($mode eq 'katinuki'){
		$juni = $sousu - $in{'no'} + 1;
		print "<p><font class=yellow size=5>天下一武道会　第<font class=red>$in{'no'}</font>回戦！！</font></p>\n";
		print "<p>※レベル上位$tenka_su人のうち第$juni位のキャラクターとの戦闘</p>\n";
		print "<h1>$knameは、$wnameに戦いを挑んだ！！</h1><hr size=0><p>\n";
		print "<embed src=\"$tennka_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	}else{
		print "<h1>$knameは、$wnameに戦いを挑んだ！！</h1><hr size=0><p>\n";
		print "<embed src=\"$sentou_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	}

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}

	if($win) {
		if($mode eq 'katinuki' and $in{'no'} == $sousu){
			print "<font class=yellow>$comment<p>$knameは、天下一武道会で優勝した！！</font><b>$exp</b>の経験値を手に入れた。優勝賞金<b>$gold</b>G手に入れた。</p>\n";
		}else{print "$comment<p>$knameは、<b>$exp</b>の経験値を手に入れた。<b>$gold</b>G手に入れた。</p>\n";}
	}else { print "$comment<p>$knameは、<b>$exp</b>の経験値を手に入れた。お金が半分になった・・・(涙)</p>\n"; }

	if($mode eq 'katinuki') {
	&nukifooter;
	}else{
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ifooter;}
	else{&footer;}
	}

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
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
	 print "FFA Emilia・いく改ver1.00 remodeling by <a href=\"http://www3.big.or.jp/~icu/\" target=\"_top\">いく</a><br>\n";
	 print "画像提供 by <a href=\"http://www.wisnet.ne.jp/~jnkw/index.html\" target=\"_top\">Jinkun</a><br>\n";
	 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 edit by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";

	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	nukifooter => <<'__SUB__',
#------------------#
#勝ちぬきのフッター#
#------------------#
sub nukifooter {

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		push(@winner, <IN>);
		close(IN);
		}

	}
	closedir(DIR);

	$nuki_no=$in{'no'}+1;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
		print "<a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>\n";
		if($nuki_no <= $sousu and $win==1){
			print " / <form action=$scriptb method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=no value=$nuki_no><input type=hidden name=mode value=katinuki><input type=hidden name=total value=$ktotal><input type=submit class=btn value=第$nuki_no回戦に出場></form>\n";
			}
		print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
		print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
	}else{
		print "<form action=$script method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=mode value=log_in><input type=submit class=btn value=ステータス画面へ></form>\n";
		if($nuki_no <= $sousu and $win==1){
			print " / <form action=$scriptb method=post><input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass><input type=hidden name=no value=$nuki_no><input type=hidden name=mode value=katinuki><input type=hidden name=total value=$ktotal><input type=submit class=btn value=第$nuki_no回戦に出場></form>\n";
			}
		print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
                print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 edit by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";

	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
	}
	print "</DIV></body></html>\n";
}
__SUB__

	header => <<'__SUB__',
#------------------#
#  HTMLのヘッダー  #
#------------------#
sub header {
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
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
	if($mode eq 'battle') {print "background-image : url($battle_back);\n";}
	elsif($mode eq 'katinuki'){print "background-image : url($tennka_back);\n";}
	else{print "background-image : url($chara_back);\n";}
	print <<"EOM";
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:10px;$font_name;color:$red;}
//-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	if($mode eq 'battle') {print "<body background=\"$battle_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";}
	elsif($mode eq 'katinuki'){print "<body background=\"$tennka_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";}
	else{print "<body background=\"$chara_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";}
}
__SUB__

	header2 => <<'__SUB__',
#--------------#
#  強制送還用  #
#--------------#
sub header2 {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="refresh" content="$refresh;URL=http\:\/\/$wurl" target="_new">
<link rel="stylesheet" href="http://www5b.biglobe.ne.jp/~jun-kei/cgi-bin/cgi.css" type"text.css">
EOM
	print "<title>$main_title</title></head>\n";
	print "<body>\n";
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


	read_select => <<'__SUB__',
#--------------------#
#  対戦相手読み込み  #
#--------------------#
sub read_select {

	if($in{'sentou'} eq "") { &error("相手が指定されていません"); }
	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		push(@TATAKAI, <IN>);
		close(IN);
		}
	}
	closedir(DIR);

	foreach(@TATAKAI) {
		($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec) = split(/<>/);
		if($in{'sentou'} eq "$wid") { last; }
	}

}
__SUB__

	read_winner => <<'__SUB__',
#--------------------#
#  チャンプ読み込み  #
#--------------------#
sub read_winner {
	open(IN,"$winner_file");
	@winner = <IN>;
	close(IN);

	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec) = split(/<>/,$winner[0]);

}
__SUB__

	read_nuki => <<'__SUB__',
#--------------------#
#  勝ち抜き読み込み  #
#--------------------#
sub read_nuki {

	if($in{'no'} eq "") { &error("相手が指定されていません"); }
	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		@WORKA=<IN>;
		if($WORKA[0] ne ""){
		push(@winner,"@WORKA");
		$i++;}
		close(IN);
		}
	}
	closedir(DIR);

	@tmp1 = @tmp2 = ();
	foreach (@winner) {
 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
		if($first){
			if($aa ne $kid){
		 		push(@WORK, $_);
		 		push(@tmp1, $first);
				}
			}
		}
	$sousu = @WORK;
	@WORK = @WORK[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];
	$i=0;
	foreach (@WORK) {
 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
		if($i==31 or $i == $sousu){last;}
 		push(@RANK_NEW, $_);
 		push(@tmp2, $first);
		$i++;
		}
	@RANK_NEW = @RANK_NEW[sort {$tmp2[$a] <=> $tmp2[$b]} 0 .. $#tmp2];

	$sousu = @RANK_NEW -1;

	if($sousu < $tenka_su){&error("現在武道会の参加者が足りないためエントリーできませんでした。");}

	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec) = split(/<>/,$RANK_NEW[$in{'no'}]);

}
__SUB__

	ifooter => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub ifooter {
	if($refresh and !$win and $mode eq 'battle') {
		print "【<b><a href=\"http\:\/\/$wurl\">&#63904;</a></b>】\n";
	}else{
		if($mode ne ""){
			print "<a href=\"$scripto\">TOP</a>\n";
		}
		if($kid and $mode ne 'ilog_in' and $mode ne 'itensyoku' and $mode ne 'yado') {
			print " / <a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>\n";
		}
		if($mode eq 'kunren') {
			print " / <a href=\"$script?mode=log_in&id=$pid&pass=$ppass\">&#63873;</a>\n";
		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	iheader => <<'__SUB__',
#------------------#
#  HTMLのヘッダー  #
#------------------#
sub iheader {
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
EOM
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$battle_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
}
__SUB__

	iheader2 => <<'__SUB__',
#--------------#
#  強制送還用  #
#--------------#
sub iheader2 {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="refresh" content="$refresh;URL=http\:\/\/$wurl" target="_new">
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body>\n";
}
__SUB__

	battle_sts => <<'__SUB__',
#------------------#
#　戦闘状況        #
#------------------#
sub battle_sts {

	# 能力値バーの詳しい幅設定
	$hit_ritu = int(($kn_4 / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($kn_5/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($klp / 15))+10+$kcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}
	$ci_plus += $a_hitup;
	$cd_plus += $a_kaihiup;
	$bwhit   = int(0.5 * ($hit_ritu + $ci_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $cd_plus));
	$bwwaza  = int(1 * ($waza_ritu + $a_wazaup));
	if($bwhit > 200){$bwhit = 200;}
	if($bwkaihi > 200){$bwkaihi = 200;}
	if($bwwaza > 200){$bwwaza = 200;}

	# 能力値バーの詳しい幅設定
	$whit_ritu = int(($wn_4 / 10) + 51);
	if($whit_ritu > 150){$whit_ritu = 150;}
	$wkaihi_ritu = int(($wn_5/ 20));
	if($wkaihi_ritu > 50){$wkaihi_ritu = 50;}
	$wwaza_ritu = int(($wlp / 15))+10+$wcllv;
	if($wwaza_ritu > 75){$wwaza_ritu = 75;}
	$wi_plus += $wa_hitup;
	$wd_plus += $wa_kaihiup;
	$bwwhit   = int(0.5 * ($whit_ritu + $wi_plus));
	$bwwkaihi = int(0.5 * ($wkaihi_ritu + $wd_plus));
	$bwwwaza  = int(1 * ($wwaza_ritu + $wa_wazaup));
	if($bwwhit > 200){$bwwhit = 200;}
	if($bwwkaihi > 200){$bwwkaihi = 200;}
	if($bwwwaza > 200){$bwwwaza = 200;}

	if($i == 1){
		$battle_date[$j] = <<"EOM";
<TABLE>
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
	<TD>
	</TD>
	<TD ALIGN="center">
	<IMG SRC="$img_path/$chara_img[$wchara]"><table width="100%">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$wi_name</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$wd_name</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$wa_name</td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwhit height=$bh><br><b>$whit_ritu + $wi_plus%</b></td></tr>
<tr><td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwkaihi height=$bh><br><b>$wkaihi_ritu + $wd_plus%</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwwaza height=$bh><br><b>$wwaza_ritu + $wa_wazaup%</b></td></tr>
</table></TD>
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
<FONT class=red size=5>VS</FONT>
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
	<TD CLASS="b1" id="td2">
	職業
	</TD>
	<TD CLASS="b1" id="td2">
	LV
	</TD>
</TR>
<TR>
	<TD class="b2">
	$wname
	</TD>
	<TD class="b2">
	$whp_flg\/$wmaxhp
	</TD>
	<TD class="b2">
	$chara_syoku[$wsyoku]
	</TD>
	<TD class="b2">
	$wlv
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>$com1 $clit1 $kawasi2 $wname に <font class=yellow>$dmg1</font> のダメージを与えた。<font class=yellow>$kaihuku1</FONT></P>
<p>$com2 $clit2 $kawasi1 $kname に <font class=red>$dmg2</font> のダメージを与えた。<font class=yellow>$kaihuku2</FONT></P>
EOM
	}else{

		$battle_date[$j] = <<"EOM";
<TABLE>
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
<FONT class=red size=5>VS</FONT>
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
	$wname
	</TD>
	<TD class="b2">
	$whp_flg\/$wmaxhp
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>$com1 $clit1 $kawasi2 $wname に <font class=yellow>$dmg1</font> のダメージを与えた。<font class=yellow>$kaihuku1</FONT></P>
<p>$com2 $clit2 $kawasi1 $kname に <font class=red>$dmg2</font> のダメージを与えた。<font class=yellow>$kaihuku2</FONT></P>
EOM
	}

}
__SUB__

	ibattle_sts => <<'__SUB__',
#------------------#
#　戦闘状況        #
#------------------#
sub ibattle_sts {

	if($i == 1){
$battle_date[$j] = <<"EOM";
$iターン<br>
$kname：<br>
<IMG SRC="$img_pathi/$chara_img[$kchara]"><br>
&#63889;:$khp_flg<br>
$wname：<br>
<IMG SRC="$img_pathi/$chara_img[$wchara]"><br>
&#63889;:$whp_flg<br>
$com1 <font color=$yellow>$dmg1</font>ダメージ>$wname<font color=$yellow>$kaihuku1</font><br>
$com2 <font color=$red>$dmg2</font>ダメージ>$kname<font color=$yellow>$kaihuku2</font><br>
EOM
	}else{
if($dmg1 ==0 and $dmg2 ==0){
$battle_date[$j] = <<"EOM";
$iターン<br>
EOM
}else{
$battle_date[$j] = <<"EOM";
$iターン<br>
$kname：<br>
&#63889;:$khp_flg<br>
$wname：<br>
&#63889;:$whp_flg<br>
$com1 <font color=$yellow>$dmg1</font>ダメージ>$wname<font color=$yellow>$kaihuku1</font><br>
$com2 <font color=$red>$dmg2</font>ダメージ>$kname<font color=$yellow>$kaihuku2</font><br>
EOM
}
	}
}
__SUB__

	battle_clt => <<'__SUB__',
#------------------#
#戦闘クリィティカル#
#------------------#
sub battle_clt {
	#クリティカル率算出
	$kclt_ritu = 100 - int($khp_flg / $kmaxhp * 100);
	$wclt_ritu = 100 - int($whp_flg / $wmaxhp * 100);

	if($mode eq 'battle'){
	if(($wlv - $klv >= $level_sa and $kmaxhp * 2 < $wmaxhp) or $ci_dmg < $wd_dmg){
		if($i == 1){
			$com1 .= "<p><font color=$blue size=5>逆転必殺技発動！！</font>$wnameの防具が一時的に効果無効！！<P/>";
			$dmg1 = $dmg1 * 100;
			$sake2 = int(0)-999999;
			$wd_dmg = 0;
			}
	}
	}
	if($kclt_ritu > int(rand(100))) {
		$clit1 = "<font color=$red size=5>クリティカル！！「<b>$kwaza</b>」</FONT></P>";
		$dmg1 = $dmg1 * 2;
		$dmg1 += $wd_dmg;
	}

	if($mode eq 'battle'){
	if(($klv - $wlv >= $level_sa and $wmaxhp * 2 < $kmaxhp) or $wi_dmg < $cd_dmg){
		if($i == 1){
			$com2 .= "<p><font color=$red size=5>逆転必殺技発動！！</font>$knameの防具が一時的に効果無効！！<P/>";
			$dmg2 = $dmg2 * 100;
			$sake1 -= 999999;
			$cd_dmg = 0;
		}
	}
	}
	if($wclt_ritu > int(rand(100))) {
		$clit2 = "<font color=$red size=5>クリティカル！！「<b>$wwaza</b>」</FONT></P>";
		$dmg2 = $dmg2 * 2;
		$dmg2 += $cd_dmg;
	}



}
__SUB__

	battle_kaihi => <<'__SUB__',
#------------------#
#戦闘回避          #
#------------------#
sub battle_kaihi{

	#挑戦者命中率＆回避率
	$hit_ritu = int(($kn_4 / 10)+51);
	$kaihi_ritu = int(($kn_5 / 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$hit_ritu += $a_hitup + $ci_plus;
	$kaihi_ritu += $a_kaihiup + $cd_plus;

	#相手命中率＆回避率
	$whit_ritu = int(($wn_4 / 10)+51);
	$wkaihi_ritu = int(($wn_5 / 20));
	if($wkaihi_ritu > 50){$wkaihi_ritu = 50;}
	$whit_ritu += $wa_hitup + $wi_plus;
	$wkaihi_ritu += $wa_kaihiup + $wd_plus;

	$sake1 += 100 - int($whit_ritu - $kaihi_ritu);
	$sake2 += 100 - int($hit_ritu - $wkaihi_ritu);

	if($dmg2 < 0){$dmg2 = $dmg2;}
		elsif($dmg2 < $cd_dmg){$dmg2 = 0;}
		else{$dmg2 = $dmg2 - $cd_dmg;}

	if($dmg1 < 0){$dmg1 = $dmg1;}
		elsif($dmg1 < $wd_dmg){$dmg1 = 0;}
		else{$dmg1 = $dmg1 - $wd_dmg;}

	#職業別防御ボーナス
	if($ksyoku > 17){$dmg2=int($dmg2/4);}
	elsif($ksyoku > 7){$dmg2=int($dmg2/2);}
	if($wsyoku > 17){$dmg1=int($dmg1/4);}
	elsif($wsyoku > 7){$dmg1=int($dmg1/2);}

	if($whp_flg < $wmclit){
		if($whp_flg < $kclit){
			if($i > 15){
			$dmg2 = $dmg2 * 10;
			$com2 .="<p><font color=$red size=5>残った力をふりしぼった！！</font><P/>";
				}
			}
	}elsif(int($sake1) > int(rand(100))) {
		$dmg2 = 0;
		$kawasi1 = "<P><FONT SIZE=4 class=\"red\">$knameは身をかわした！</FONT></P>";
	}
	if($khp_flg < $kmclit){
		if($khp_flg < $wclit){
			if($i > 15){
			$dmg1 = $dmg1 * 10;
			$com1 .="<p><font color=$red size=5>残った力をふりしぼった！！</font><P/>";
				}
			}
	}elsif(int($sake2) > int(rand(100))) {
		$dmg1 = 0;
		$kawasi2 = "<P><FONT SIZE=4 class=\"red\">$wnameは身をかわした！</FONT></P>";
	}

}
__SUB__

	sentoukeka => <<'__SUB__',
#------------------#
#戦闘結果判定      #
#------------------#
sub sentoukeka{

	if($win==1) {
		if($mode eq 'katinuki' and $in{'no'} eq $sousu){
			$ktotal += 1;
			$kkati += 1;
			$exp = int($wlv * $kiso_exp);
			$kex = $kex + $exp;
			$gold += ($wcllv + $wlv + $sousu + $klv) * $wmaxhp;
			$kmons = $sentou_limit;
			$kmori = $boss;
			$comment = "<b><font size=5>$knameは、最後の戦闘に勝利した！！</font></b><P/>";
		}else{
			$ktotal += 1;
			$kkati += 1;
			$exp = int($wlv * $kiso_exp);
			$kex = $kex + $exp;
			if($mode eq 'battle') {$gold += $wgold;}
			else{$gold += int(rand(100)+1) * int($wmaxhp);}
			$wgold = int($wcount * $klv * $syoukin);
			$kmons = $sentou_limit;
			$kmori = $boss;
			$comment = "<b><font size=5>$knameは、戦闘に勝利した！！</font></b><P/>";
			}
		}
	elsif($win==2) {
		$win=1;
		$ktotal += 1;
		$exp = int($wlv * $kiso_exp);
		$kex = $kex + $exp;
		$khp = 1;
		$whp = 1;
		if($mode eq 'battle') {$gold += $wgold;}
		else{$gold += int(rand(100)+1) * int($wmaxhp);}
		$wgold = int($wcount * $klv * $syoukin);
		$kmons = $sentou_limit;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、$wnameと相打ちした！！</font></b><P/>";
		}
	elsif($win==3) {
		$ktotal += 1;
		$exp = int($wlv * $kiso_exp);
		$kex = $kex + $exp;
		$gold = 0;
		$wgold += int($wcount * $klv * $syoukin);
		$kmons = $sentou_limit;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、$wnameと勝負が決まらなかった。。。</font></b><P/>";
		}
	else{
		$ktotal += 1;
		$exp = int($wlv * 1);
		$kex = $kex + $exp;
		$kgold = int(($kgold / 2));
		$wgold += int($wcount * $klv * $syoukin);
		$kmons = $sentou_limit;
		$kmori = $boss;
		$comment = "<b><font size=5>$knameは、戦闘に負けた・・・。</font></b><P/>";
	}
}
__SUB__

	wacs_add => <<'__SUB__',
#------------------#
#チアクセサリー加算#
#------------------#
sub wacs_add {
	$wn_0 += $wa_0up;
	$wn_1 += $wa_1up;
	$wn_2 += $wa_2up;
	$wn_3 += $wa_3up;
	$wn_4 += $wa_4up;
	$wn_5 += $wa_5up;
	$wn_6 += $wa_6up;
	$wlp  += $wa_lpup;
if($wtac){require "./wtech/$wtac.pl";}
}
__SUB__

	wacs_sub => <<'__SUB__',
#------------------#
#チアクセサリー減算#
#------------------#
sub wacs_sub {
	$wn_0 -= $wa_0up;
	$wn_1 -= $wa_1up;
	$wn_2 -= $wa_2up;
	$wn_3 -= $wa_3up;
	$wn_4 -= $wa_4up;
	$wn_5 -= $wa_5up;
	$wn_6 -= $wa_6up;
	$wlp  -= $wa_lpup;
}
__SUB__

	winner => <<'__SUB__',
#------------------#
#　チャンプの攻撃　#
#------------------#
sub winner {
	# チャンプダメージ計算
	if($witem){ $com2 = "<p>$wnameは、$wi_nameで攻撃！！<FONT COLOR=\"$yellow\">$battlecom[$wsyoku]</FONT></p>"; }
	else{ $com2 = "<p>$wnameは、素手で攻撃！！ </p>";}

$wattackpower="w"."$iryoku[$wsyoku]";
&$wattackpower;

}
__SUB__

	winwaza => <<'__SUB__',
#------------------#
#　チャンプの必殺技#
#------------------#
sub winwaza {

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {$com2="";}

	# クリティカル
	$wwaza_ritu = int(($wlp / 15))+10+$wcllv;
	if($wwaza_ritu > 75){$wwaza_ritu = 75;}
	$wwaza_ritu += $wa_wazaup;
	if($wwaza_ritu > 95){$wwaza_ritu = 95;}
	#ＨＰが１／１０時に必殺率＋１００％
	if(int($wmaxhp / 10) > $whp_flg && int(rand(4))>1){
		$wwaza_ritu +=999;
		$com2 .="<P><font class=\"red\" size=4>LIMIT BREAK!!</FONT></P>";
		}

	# 封印球の効果
	if($a_kouka == 19 and $wa_kouka != 24 and $wa_kouka != 19){
		if($wsyoku > 16){$com1 .="<P><font class=\"red\" size=3>$a_nameが光を放つ！！$wnameには効かなかった！！</FONT></P>";}
		elsif($wsyoku > 7){if(int(rand(5))==0){$wwaza_ritu = 0;$com1 .="<P><font class=\"yellow\" size=3>$a_nameが光を放つ！！$wnameの必殺技を封じ込めた！！</FONT></P>";}}
		else{if(int(rand(2))==0){$wa_kouka =0;$wwaza_ritu = 0;$com1 .="<P><font class=\"yellow\" size=3>$a_nameが光を放つ！！$wnameの必殺技を封じ込めた！！</FONT></P>";}}
		}

	if($wtac){&whissatu;}

}
__SUB__

	wacs_waza => <<'__SUB__',
#------------------#
#チアクセサリー効果#
#------------------#
sub wacs_waza {

	if($wtac){&watowaza;}

	if($wa_kouka){if(!$wwazawaza){require "./wacstech/$wa_kouka.pl";$wwazawaza=1;}&wacskouka;}
}
__SUB__

);
}
