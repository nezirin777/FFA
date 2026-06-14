#!/usr/bin/perl --

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　edit by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# syoku_regist呼び出し
require 'battle.pl';

# shopfooter呼び出し
require 'item.pl';

# このファイル用設定
$backgif = $shop_back;
$midi = $shop_midi;

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
if ($mente) {
	&error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m");
}

&decode;

	$back_form = << "EOM";
<br>
<form action="$script_tensyoku" method="post">
<input type=hidden name=id value="$in{'id'}">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type=submit class=btn value="戻る">
</form>
EOM

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

if ($mode) { &$mode; }
&tensyoku;

exit;

#------------#
# 転職の神殿 #
#------------#
sub tensyoku {

	&chara_load;

	&chara_check;

	&syoku_load;

	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

$mitensyoku.="現在転職できるまだマスターしていない職業は<br><table><tr>";
$tensyokuok.= "現在転職できる職業は<br><table><tr>";

	$i=0;$hit=0;$mhit=0;
	foreach (@syoku) {
		s/\n//i;
		s/\r//i;
		($a,$b,$c,$d,$e,$f,$g,$h) = split(/<>/);
		@pre = split(/<>/,$_,17);
		@syoku_require = split(/<>/,$pre[16]);
		if($chara[7] >= $a and $chara[8] >= $b and $chara[9] >= $c and $chara[10] >= $d and $chara[11] >= $e and $chara[12] >= $f and $chara[13] >= $g and $chara[20] >= $h and $chara[14] != $i) {
			$is=0;
			$shit=0;
			foreach (@syoku_require) {
				if ($_ > $syoku_master[$is]) {$shit = 1;}
				$is++;
			}
			if (!$shit) {
				$tensyokuok.="<td><font color=white size=3>\[$chara_syoku[$i]\]</font></td>";
				$selection.="<option value=\"$i\">$chara_syoku[$i]</option>\n";
				$hit+=1;
				if($hit % 5 == 0){$tensyokuok.="</tr><tr>";}
				if ($syoku_master[$i] < 60) {
					$mitensyoku.="<td><font color=white size=3>\[$chara_syoku[$i]\]</font></td>";
					$mhit+=1;
					if($mhit % 5 == 0){$mitensyoku.="</tr><tr>";}

				}
			}
		}
		$i++;
	}
	if(!$hit) { $tensyokuok.= "<td>ありません</td>"; }
	if(!$mhit) { $mitensyoku.="<td>ありません</td>"; }

	&header;

	print <<"EOM";
<h1>転職の神殿</h1><hr>
ここでは他の職業に転職できます。<br>
※ 転職すると、現在の能\力値がランダムで下がります。ただし、転職する職業の職業レベルが20以上の場合は下がりません。<br><br>
$tensyokuok</tr></table><br>
$mitensyoku</tr></table><br>
<form action="$script_tensyoku" method="post">
<select name=syoku>
<option value="no">選択してください
$selection
</select>
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value="tensyoku_change">
<input type=submit class="btn" value="転職する">
</form>
<form action="$script" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#--------#
#  転職  #
#--------#
sub tensyoku_change {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	if($in{'syoku'} eq 'no') {
		&error("職業を選択してください。$back_form");
	}

	$lock_file = "$lockfolder/syoku$in{'id'}.lock";
	&lock($lock_file,'SK');
	&syoku_load;

	$syoku_master[$chara[14]] = $chara[33];

	&syoku_regist;
	&unlock($lock_file,'SK');

	&get_host;

	open(IN,"$syoku_file");
	@syokudate = <IN>;
	close(IN);

	($a,$b,$c,$d,$e,$f,$g,$h) = split(/<>/,$syokudate[$in{'syoku'}]);
	$syokudate[$in{'syoku'}] =~ s/\n//gi;
	$syokudate[$in{'syoku'}] =~ s/\r//gi;

	if (!($chara[7] >= $a and $chara[8] >= $b and $chara[9] >= $c and $chara[10] >= $d and $chara[11] >= $e and $chara[12] >= $f and $chara[13] >= $g and $chara[20] >= $h) || !$syokudate[$in{'syoku'}]) {&error("まだ転職できません");}

	$chara[14] = $in{'syoku'};
	if ($master_tac) { $chara[30] = 0; }	# 転職後の戦術クリア
	$chara[33] = $syoku_master[$chara[14]];

	if (!$chara[33]) { $chara[33] = 1; }

	if ($chara[33] < 20) {
		$chara[7] = int($chara[7]) - int($chara[7] / 10);
		$chara[8] = int($chara[8]) - int($chara[8] / 10);
		$chara[9] = int($chara[9]) - int($chara[9] / 10);
		$chara[10] = int($chara[10]) - int($chara[10] / 10);
		$chara[11] = int($chara[11]) - int($chara[11] / 10);
		$chara[12] = int($chara[12]) - int($chara[12] / 10);
		$chara[13] = int($chara[13]) - int($chara[13] / 10);
		$chara[20] = int($chara[20]) - int($chara[7] / 5);
		if($chara[7] < 9) { $chara[7] = 9; }
		if($chara[8] < 8) { $chara[8] = 8; }
		if($chara[9] < 8) { $chara[9] = 8; }
		if($chara[10] < 9) { $chara[10] = 9; }
		if($chara[11] < 9) { $chara[11] = 9; }
		if($chara[12] < 8) { $chara[12] = 8; }
		if($chara[13] < 8) { $chara[13] = 8; }
		if($chara[20]  < 0) { $chara[20] = 1; }
	}

	&chara_regist;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<h1>$chara_syoku[$chara[14]]に転職しました</h1><hr size=0>
<form action="$script" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

	&shopfooter;

	&footer;

	exit;
}
