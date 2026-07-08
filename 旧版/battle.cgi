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
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 戦闘ライブラリの読み込み
require 'battle.pl';
# チャンプ戦用ライブラリ読み込み
require 'wbattle.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $battle_back;
$midi = $battle_midi;


#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
if($mente) {
	&error("現在バージョンアップ中です。しばらくお待ちください。");
}

&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

&battle;

exit;

#------------#
#  戦闘画面  #
#------------#
sub battle {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	&get_host;

	$lock_file = "$lockfolder/cmp.lock";
	&lock($lock_file,'BT');
	&read_winner;

	# 賞金の決定
	$gold = $winner[50];

	if ($winner[0] eq $chara[0]) {
		&error("現在チャンプなので闘えません。");
	}

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$vtime = $b_time - $ltime;

	if ($vtime > 0) {
		&error("あと$vtime秒間闘えません。");
	}

	&item_load;

	&acs_add;

	&wacs_add;

	$khp_flg = $chara[15];
	$whp_flg = $winner[15];

	$i=1;$j=0;@battle_date=();
	foreach (1..$turn) {

		&shokika;

		&tyousensya;
		&winner_atack;

		&tyosenwaza;
		&winwaza;

		&acs_waza;
		&wacs_waza;

		&battle_clt;
		&battle_kaihi;

		&battle_sts;

		&hp_sum;

		&winlose;

		$i++;
		$j++;
	}

	&sentoukeka;
	$chara[25] = $sentou_limit;
	$chara[28] = $boss;

	&acs_sub;
	&wacs_sub;

	&levelup;

	$chara[15] = $khp_flg + int(rand($chara[10]));
	if($chara[15] > $chara[16]) { $chara[15] = $chara[16]; }
	$winner[15] = $whp_flg + int(rand($winner[9]));
	if($winner[15] > $winner[16]) { $winner[15] = $winner[16]; }
	if($chara[15] <= 0) { $chara[15] = 1; }
	if($winner[15] <= 0) { $winner[15] = 1; }
	$chara[19] += $gold;
	if($chara[19] < 0){$chara[19] = 0;}
	if($chara[19] > $gold_max){$chara[19] = $gold_max;}

	if ($win == 1 or $win == 2) {
		$new_winner = "$chara[0]<>$chara[2]<>$chara[3]<>$chara[4]<>$chara[5]<>$chara[6]<>$chara[7]<>$chara[8]<>$chara[9]<>$chara[10]<>$chara[11]<>$chara[12]<>$chara[13]<>$chara[20]<>$chara[14]<>$chara[15]<>$chara[16]<>$chara[18]<>$chara[21]<>$chara[22]<>$chara[23]<>$item[0]<>$item[1]<>$item[2]<>$item[3]<>$item[4]<>$item[5]<>$item[6]<>$item[8]<>$item[9]<>$item[10]<>$item[11]<>$item[12]<>$item[13]<>$item[15]<>$item[17]<>$item[18]<>$chara[30]<>$host<>$chara[33]<>$winner[0]<>$winner[3]<>$winner[1]<>$winner[2]<>1<>$winner[45]<>$winner[46]<>$winner[47]<>$winner[48]<>$winner[49]<>$winner[50]<>$item[7]<>$item[16]<>$item[14]<>";

	} else {
		$winner[44] += 1;

		if ($winner[44] > $winner[45]) {
			$winner[45] = $winner[44];
			$winner[46] = $winner[0];
			$winner[47] = $winner[3];
			$winner[48] = $winner[1];
			$winner[49] = $winner[2];
		}

		$winner[15] += int($winner[16] / 10);
		if($winner[15] > $winner[16]){$winner[15] = $winner[16];}
		$winner[40] = $chara[0];
		$winner[41] = $chara[4];
		$winner[42] = $chara[2];
		$winner[43] = $chara[3];

		$new_winner = '';
		$new_winner = join('<>',@winner);
		$new_winner .= '<>';
	}

	open(OUT,">$winner_file");
	print OUT $new_winner;
	close(OUT);

	$lock_file = "$lockfolder/cmp.lock";
	&unlock($lock_file,'BT');

	if($chara[15] == 1) { $chara[15] = $chara[16]; }

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print "<h1>$chara[4]は、$winner[3]に戦いを挑んだ！！</h1>\n<hr size=0><br>\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if ($win) {
		print "$comment<br>$chara[4]は、<b>$exp</b>の経験値を手に入れた。$winner[3]の賞金<b>$gold</b>G手に入れた。<br>\n";
	} else {
		print "$comment<br>$chara[4]は、<b>$exp</b>の経験値を手に入れた。お金が半分になった・・・(涙)<br>\n";
	}

	print << "EOM";
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
