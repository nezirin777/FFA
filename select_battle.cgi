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

if ($mode) { &$mode; }

&log_in;

exit;

#------------#
#  受付画面  #
#------------#
sub log_in{

	&chara_load;

	&chara_check;

	&header;

	print << "EOM";
<h1>好きなキャラに挑戦</h1>
<hr size=0>
<FONT SIZE=3>
<B>案内人</B><BR>
「
ようこそいらっしゃいました！<br>
ここではこの$main_titleの好きなプレイヤーに腕試し挑戦をすることができます！<br>
ただし、経験値・お金は入手できません。あくまでも腕試しだけです。<br>
あなたは$chara[4]さんですね！挑戦してみますか？
」
<form action="$script_select" method="post">
<input type="hidden" name="mode" value="battle">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
名前指定
<input type="text" name="aitename" value="" size="20"><br>
<input type="submit" class="btn" value="挑戦する">
</form>
<form action="$script_select" method="post">
<input type="hidden" name="mode" value="sentaku">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="submit" class="btn" value="名前を一覧から選択する">
</form>
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;

}

#------------#
#  選択画面  #
#------------#
sub sentaku{

	&chara_load;

	&chara_check;

	&all_data_read;

	&header;

	print << "EOM";
<h1>一覧から選択</h1>
<hr size=0>
<FONT SIZE=3>
<B>案内人</B><BR>
「
どの方と戦われますか？
」
<form action="$script_select" method="post">
<input type="hidden" name="mode" value="battle">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<table width = "80%"><tr>
EOM
	foreach (@RANKING) {
		s/\n//gi;
		s/\r//gi;
		@aite_data = split(/<>/);
		print << "EOM";
<td align="left" class="b2" width = "20%">
<input type = "radio" name = "aiteid" value = "$aite_data[0]">
$aite_data[4](Lv.$aite_data[18])
</td>
EOM
		$a++;
		if ($a % 5 == 0) {
			print "</tr><tr>";
		}
	}
	print << "EOM";
</tr></table>
<input type="submit" class="btn" value="挑戦する">
</form>
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;

}

#------------#
#  戦闘画面  #
#------------#
sub battle {

	&get_host;

	&chara_load;

	&chara_check;

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$vtime = $b_time - $ltime;

	if ($vtime > 0) {
		if ($ltime < $b_time) {
			&error("あと$vtime秒間闘えません。");
		}
	}

	if (!$in{'aiteid'}) {
		$form = << "EOM";
<form action="$script_select" method="post">
<input type="hidden" name="mode" value="battle">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
もう一度名前指定
<input type="text" name="aitename" value="" size="20"><br>
<input type="submit" class="btn" value="挑戦する">
</form>
EOM
		&all_name_search($in{'aitename'},$form);
	} else {
		$aiteid = $in{'aiteid'};
	}

	open(IN,"./charalog/$aiteid.cgi");
	$aite_data = <IN>;
	close(IN);

	@winner_data = split(/<>/,$aite_data);

	&winner_data;

	# 賞金の決定
	$gold = 0;

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

	&header;

	print "<h1>$chara[4]は、$winner[3]に戦いを挑んだ！！</h1>\n<hr size=0><br>\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if ($win) {
		print "$comment<br>\n";
	} else {
		print "$comment<br>\n";
	}

	print << "EOM";
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
