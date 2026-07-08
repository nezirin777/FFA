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

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");
	}
}

&boss;

exit;
#----------------------------#
#  レジェンドプレイスでの戦闘#
#----------------------------#
sub boss {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	if (!$chara[25]) {
		&error("一度キャラクターと闘ってください");
	}

	if ($chara[32] < $in{'boss_file'}) {
		&error("まだ挑戦できません！");
	}

	$ntime = time();
	$b_time = $m_time;
	$ztime = $ntime - $chara[27];
	$ztime = $b_time - $ztime;

	if ($ztime > 0) { &legend_error; }

	&get_host;

	&item_load;

	&acs_add;

	$bmonster = "boss$in{'boss_file'}\_monster";

	open(IN,"$$bmonster");
	@MONSTER = <IN>;
	close(IN);

	$r_no = @MONSTER;

	$r_no = $chara[28];

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
		&mons_atowaza;

		&mons_clt;
		&mons_kaihi;

		&monsbattle_sts;

		&hp_sum;

		&winlose;

		$i++;
		$j++;
	}

	$kmori_w = $chara[28];

	&legend_sentoukeka;

	&acs_sub;

	&levelup;

	&hp_after;

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$boss_h = int($boss /2);	
	if ($kmori_w == 1) {
		$backgif = $last_back;
		$midi = $last_boss_midi;
	} elsif ($kmori_w >= $boss_h) {
		$backgif = $boss_back;
		$midi = $boss_midi1;
	} else {
		$backgif = $boss2_back;
		$midi = $boss_midi2;
	}

	&header;

	print <<"EOM";
<FONT SIZE= "5" COLOR= "#7777DD"><B>レジェンドプレイス</B></FONT><br>

<B><CENTER><FONT SIZE= "6">$mname</B>が現れた！</FONT></CENTER>
<BR>
<BR>
EOM

	$i=0;
	foreach(@battle_date) {
		print "$battle_date[$i]";
		$i++;
	}

	&bossfooter;

	&footer;

	exit;
}

#--------------------------------#
#  レジェンドプレイス用フッター  #
#--------------------------------#
sub bossfooter {
	if ($win) { print "$comment$chara[4]は、$mexの経験値を手に入れた。<b>$gold</b>G手に入れた。<br>\n"; }
	else { print "$comment$chara[4]は、$mexの経験値を手に入れた。お金が100分の１になった・・・(涙)<br>\n"; }

	if ($chara[28] != 0 && $win == 1) {
		print <<"EOM";
<form action="$script_legend" method="post">
<input type=hidden name="mode" value="boss">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type="hidden" name="boss_file" value="$in{'boss_file'}">
<input type=submit class=btn value="さらに奥に進む">
</form>
EOM
	}
	print <<"EOM";
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM
}

#----------------#
#  待ち時間表示  #
#----------------#
sub legend_error {

	foreach (keys %lock_flg) {
		if ($lock_flg{$_}) {
			if ($lockkey == 3) {
				foreach (@flock) {
					($flock_pre,$flock_file) = split(/,/);
					if ($flock_file eq $_) {
						last;
					}
				}
			}
			&unlock($_,$flock_pre);
		}
	}

	&header;

	&time_view;

       print <<"EOM";
<center><hr width=400>
<font color=red><B>まだ戦闘できません！</B></font><br>
<FORM NAME= "form1">
あと<INPUT TYPE= "text" NAME= "clock" SIZE= "3">秒待って下さい
</FORM>
<form action= "$script_legend" method= "POST">
<input type= "hidden" name= "mode" value= "boss">
<input type= "hidden" name= "id" value= "$chara[0]">
<input type= "hidden" name= "mydata" value= "$in{'mydata'}">
<input type="hidden" name="boss_file" value="$in{'boss_file'}">
<input type= "submit" class= "btn" value= "次の戦いへ">
</form>
<form action= "$script" method= "POST">
<input type= "hidden" name= "mode" value= "log_in">
<input type= "hidden" name= "id" value= "$chara[0]">
<input type= "hidden" name= "mydata" value= "$in{'mydata'}">
<input type= "submit" class= "btn" value= "ステータス画面へ">
</form>
<hr width=400>
</center>
EOM

	&footer;

	exit;

}
