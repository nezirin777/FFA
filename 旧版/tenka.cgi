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
$backgif = $tennka_back;
$midi = $tennka_midi;

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

	$lock_file = "$lockfolder/tim.lock";
	&lock($lock_file,'TM');
	open(IN,"$all_data_time");
	@all_time = <IN>;
	close(IN);

	$hit=0;
	foreach(@all_time){
		($rankmode,$ranktime) = split(/<>/);
		if ($rankmode eq "tenka") { $hit=1;last; }
	}

	$ltime = time();
	$btime = $ltime - $ranktime;
	$ztime = int($btime/3600);

	if ($btime > 3600*24 || !$hit) {

		$hit=0;
		@item_new=();
		foreach (@all_time) {
			($rankmode,$ranktime) = split(/<>/);
			if ($rankmode eq "tenka") {
				unshift(@item_new,"tenka<>$ltime<>\n");
				$hit=1;
			} else {
				push(@item_new,"$_");
			}
		}

		if (!$hit) { unshift(@item_new,"tenka<>$ltime<>\n"); }

		open(OUT,">$all_data_time");
		print OUT @item_new;
		close(OUT);
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');

		opendir (DIR,'./charalog') or die "$!";
		foreach $entry (readdir(DIR)){

			if ($entry =~ /\.cgi/) {
				open(IN,"./charalog/$entry");
				$WORK=<IN>;
				$WORK =~ s/\n//gi;
				$WORK =~ s/\r//gi;
				push(@temp_member,"$WORK\n");
				close(IN);		
			}
		}
		closedir(DIR);

		$tenka_hit = 0;
		$tenka_ninzu = @temp_member;
		if ($tenka_su > $tenka_ninzu) {
			$tenka_su = $tenka_ninzu;
			$tenka_hit = 1;
		}
		# 配列19番目でソート
		@tmp = map {(split /<>/)[18]} @temp_member;
		@RANKING = @temp_member[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

		for ($si=0;$si<$tenka_su;$si++) {
			push(@tenka_member,"$RANKING[$si]");
		}

		open(OUT,">$all_tenka");
		print OUT @tenka_member;
		close(OUT);

	} else {
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');

		open(IN,"$all_tenka");
		@tenka_member = <IN>;
		close(IN);

		$tenka_hit = 0;
		$tenka_ninzu = @tenka_member;
		if ($tenka_su > $tenka_ninzu) {
			$tenka_hit = 1;
		}
	}

	open(IN,"$tenka_log");
	@tenka_log = <IN>;
	close(IN);

	&header;

	print << "EOM";
<h1>天下一武道会</h1>
<hr size=0>
<FONT SIZE=3>
<B>司会者</B><BR>
「
ようこそ！天下一武道会へ！<br>
ここはこの$main_titleでの最強のプレイヤーたちを勝ち抜いていく舞台となっています！<br>
あなたは$chara[4]さんですね！<br>
挑戦してみますか？
」
<table width = "80%">
<tr>
<td width = "50%" align = "left" valign = "top">
<table width = "95%">
<tr>
<td align="center" id="td2" class="b2" colspan = "2">
天下一武道会メンバーリスト($ztime時間前更新)
</td>
</tr>
<tr>
<td align="right" class="b2">
名前
</td>
<td align="right" class="b2">
レベル
</td>
</tr>
EOM

	foreach (@tenka_member) {
		s/\n//gi;
		s/\r//gi;
		@tenka = split(/<>/);
		print << "EOM";
<tr>
<td align="right" class="b2">
$tenka[4]
</td>
<td align="right" class="b2">
$tenka[18]
</td>
</tr>
EOM
	}

	print << "EOM";
</table>
</td>
<td width = "50%" align = "left" valign = "top">
<table width = "95%">
<tr>
<td align="center" id="td2" class="b2" colspan = "3">
ここ最近の制覇者
</td>
</tr>
<tr>
<td align="right" class="b2">
名前
</td>
<td align="right" class="b2">
レベル
</td>
<td align="right" class="b2">
日時
</td>
</tr>
EOM

	if (@tenka_log) {
		foreach (@tenka_log) {
			s/\n//gi;
			s/\r//gi;
			@tenka = split(/<>/);
			print << "EOM";
<tr>
<td align="right" class="b2">
<a href="$scripta?mode=chara_sts&id=$tenka[0]">$tenka[1]</a>
</td>
<td align="right" class="b2">
$tenka[2]
</td>
<td align="right" class="b2">
$tenka[3]
</td>
</tr>
EOM
		}
	} else {
			print << "EOM";
<tr>
<td align="center" class="b2" colspan ="2">
そのような猛者はまだいません
</td>
</tr>
EOM
	}
	print << "EOM";
</table>
</td></tr></table>
EOM
	if ($chara[28] != $boss) {
		print '一度、チャンプに挑戦して下さい';
	} elsif (!$tenka_hit) {
		print << "EOM";
<form action="$script_tenka" method="POST">
<input type="hidden" name="mode" value="battle">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="hidden" name="no" value="1">
<input type="submit" class="btn" value="天下一武道会に挑戦する">
</form>
EOM
	} else {
		print "人数が足りません";
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

#------------#
#  戦闘画面  #
#------------#
sub battle {

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$ltime = time();
	$ltime = $ltime - $chara[27];
	$ztime = $b_time - $ltime;

	if ($ztime > 0) {
		&tenka_error;
	}

	open(IN,"$all_tenka");
	@tenka_member = <IN>;
	close(IN);

	$aite = $tenka_su + $chara[28] - $boss - 1;

	if ($in{'no'} != $tenka_su - $aite) {
		&error("キャラデータ不整合");
	}

	@winner_data = split(/<>/,$tenka_member[$aite]);

	&winner_data;

	# 賞金の決定
	$gold = int(rand($syoukin)+1) * int($winner[17]);

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
	$chara[28]--;

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

	if($chara[15] == 1) { $chara[15] = $chara[16]; }

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$next_winner = $chara[28] + $tenka_su - $boss;

	# 武道会制覇
	if ($win == 1 && $next_winner == 0) {
		&get_time($chara[27]);

		&all_message("$chara[4]さんが天下一武道会を制覇されました！");

		$lock_file = "$lockfolder/tnk.lock";
		&lock($lock_file,'TENKA');
		open(IN,"$tenka_log");
		@tenka_log = <IN>;
		close(IN);
		$log_num =@tenka_log;
		if ($tenaka_su < $log_num) {
			pop(@tenka_log);
		}

		unshift(@tenka_log,"$chara[0]<>$chara[4]<>$chara[18]<>$gettime<>\n");
		open(OUT,">$tenka_log");
		print OUT @tenka_log;
		close(OUT);
		&unlock($lock_file,'TENKA');
	}

	&header;

	$juni = $tenka_su - $in{'no'} + 1;

		print << "EOM";
<font class=yellow size=5>天下一武道会　第<font class=red>$in{'no'}</font>回戦！！</font><br>
※レベル上位$tenka_su人のうち第$juni位のキャラクターとの戦闘<br>
<h1>$chara[4]は、$winner[3]に戦いを挑んだ！！</h1>
<hr size=0><br>
EOM
	$in{'no'}++;
	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	if ($win) {
		if ($next_winner != 0) {
			print << "EOM";
$comment<br>$chara[4]は、<b>$exp</b>の経験値を手に入れた。$winner[3]の賞金<b>$gold</b>G手に入れた。<br>
<form action="$script_tenka" method="POST">
<input type="hidden" name="mode" value="battle">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type="hidden" name="no" value="$in{'no'}">
<input type="submit" class="btn" value="次の戦いへ">
</form>
EOM
		} else {
		print "<font class=yellow>$comment<br>$chara[4]は、天下一武道会で優勝した！！</font><b>$exp</b>の経験値を手に入れた。優勝賞金<b>$gold</b>G手に入れた。<br>\n";
		}
	} else {
		print "$comment<br>$chara[4]は、<b>$exp</b>の経験値を手に入れた。お金が半分になった・・・(涙)<br>\n";
	}

	$new_chara =~ s/</&lt;/g;
	$new_chara =~ s/>/&gt;/g;

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

#----------------#
#  待ち時間表示  #
#----------------#
sub tenka_error {

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
<FORM NAME="form1">
あと<INPUT TYPE="text" NAME="clock" SIZE="3">秒待って下さい
</FORM>
<form action="$script_tenka" method="POST">
<input type="hidden" name="mode" value="battle">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type="hidden" name="no" value="$in{'no'}">
<input type="submit" class="btn" value="次の戦いへ">
</form>
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
<hr width=400>
</center>
EOM

	&footer;

	exit;

}
