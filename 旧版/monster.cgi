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
# モンスター戦用ライブラリ
require 'mbattle.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

if ($mente) {
	&error("現在バージョンアップ中です。しばらくお待ちください。");
}

&decode;

# このファイル用設定
$temp_back = "$mode\_back";
$temp_midi = "$mode\_midi";
$backgif = $$temp_back;
$midi = $$temp_midi;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");
	}
}

&$mode;

exit;

#----------------------#
#  モンスターとの戦闘  #
#----------------------#
sub monster {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	&get_host;

	if (!$chara[25]) {
		&error("一度キャラクターと闘ってください");
	}

	&time_check;

	&item_load;

	&acs_add;

	$monster_file = "$in{'mons_file'}\_monster";

	open(IN,"$$monster_file");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = int(rand($r_no));

	&mons_read;

	$khp_flg = $chara[15];
	$mhp = int(rand($mrand)) + $msp;
	$mhp_flg = $mhp;
	$m_sp = int(rand(11));

	$i=1;
	$j=0;
	@battle_date=();
	foreach(1..$turn) {

		&shokika;

		&tyousensya;

		&tyosenwaza;
		&mons_waza;

		&acs_waza;
		&mons_atowaza;

		&mons_clt;
		&mons_kaihi;

		&monsbattle_sts;

		&hp_sum;

		&winlose;

		$i++;
		$j++;
	}

	&sentoukeka;

	&acs_sub;

	&levelup;

	&hp_after;

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print "<h1>$chara[4]は、$mnameに戦いを挑んだ！！</h1><hr size=0>\n";

	$i=0;
	foreach(@battle_date) {
		print "$battle_date[$i]";
		$i++;
	}

	&mons_footer;

	&footer;

	exit;
}

#----------------------#
#  幻影の城の戦闘      #
#----------------------#
sub genei {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	&get_host;

	if (!$chara[25]) {
		&error("一度キャラクターと闘ってください");
	}

	&time_check;

	if ($chara[27]%5 != 0) {
		&error("もう消えてしまって行けませんでした");
	}

	&item_load;

	&acs_add;


	if ($chara[18] < $genei_low) {
		$monster_file=$monster0_monster;
	}
	elsif ($chara[18] < $genei_high) {
		$monster_file=$monster1_monster;
	}
	elsif ($chara[18] < $genei_max) {
		$monster_file=$monster2_monster;
	}
	else {
		$monster_file=$monster3_monster;
	}

	open(IN,"$monster_file");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = int(rand($r_no));

	&mons_read;

	$khp_flg = $chara[15];
	$mhp = int(rand($mrand)) + $msp * 2;
	$mhp_flg = $mhp;

	$i=1;
	$j=0;@battle_date=();
	foreach(1..$turn) {

		&shokika;

		$dmg2 += $item[4];

		&tyousensya;
		&tyosenwaza;

		&mons_waza;

		&acs_waza;

		&mons_clt;
		&mons_kaihi;

		&monsbattle_sts;

		&hp_sum;

		&winlose;

		$i++;
		$j++;
	}

	&sentoukeka;

	if ($win == 1) {
		if (int(rand(3)) == 0) {
			$otakara = int(rand(1000)+1) * int($mgold);
			$chara[19] += $otakara;
			$comment .= "<b><font size=5 color=red>財宝($otakaraＧ)を発見した！！！！</font></b>";
		} else {
			$comment .= "<b><font size=5>辺りに財宝は見つからなかった・・・。</font></b>";
		}
	}

	&acs_sub;

	&levelup;

	&hp_after;

	&chara_regist;
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE= "5" COLOR= "#7777DD"><B>幻影の城</B></FONT>
<BR>

<B><CENTER><FONT SIZE= "6">$mname</B>が現れた！</FONT></CENTER>
<BR>
<BR>
EOM

	$i=0;
	foreach(@battle_date) {
		print "$battle_date[$i]";
		$i++;
	}
	
	&mons_footer;

	&footer;

	exit;
}

#----------------------#
#  異世界での戦闘      #
#----------------------#
sub isekiai {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	&get_host;

	if (!$chara[25]) {
		&error("一度キャラクターと闘ってください");
	}

	&time_check;

	&item_load;

	&acs_add;

	open(IN,"$isekai_monster");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = int(rand($r_no));

	&mons_read;

	$khp_flg = $chara[15];
	$mhp = int(rand($mrand)) + $msp;
	$mhp_flg = $mhp;

	$i=1;
	$j=0;@battle_date=();
	foreach(1..$turn) {
		&shokika;

		&tyousensya;
		&tyosenwaza;

		&mons_waza;

		&acs_waza;

		&mons_clt;
		&mons_kaihi;

		&monsbattle_sts;

		&hp_sum;

		&winlose;

		$i++;
		$j++;
	}

	&sentoukeka;

	&acs_sub;

	&levelup;

	&hp_after;

	&chara_regist;
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE= "5" COLOR= "#7777DD"><B>異世界</B></FONT>
<BR>

<B><CENTER><FONT SIZE= "6">$mname</B>が現れた！</FONT></CENTER>
<BR>
<BR>
EOM

	$i=0;
	foreach(@battle_date) {
		print "$battle_date[$i]";
		$i++;
	}

	&mons_footer;

	&footer;

	exit;
}

