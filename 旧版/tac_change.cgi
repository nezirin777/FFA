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
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した #
#    いかなる損害に対して作者は一切の責任を負いません。     	#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。   	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $sts_back;
$midi = $sts_midi;

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;

	$back_form = << "EOM";
<br>
<form action="$scripts" method="post">
<input type=hidden name=id value="$in{'id'}">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type=hidden name=mode value="log_in">
<input type=submit class=btn value="戻る">
</form>
EOM

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

if($mode) { &$mode; }

&senjutu;

exit;

#----------------#
#  戦術表示      #
#----------------#
sub senjutu {

	&chara_load;

	&chara_check;

	$hit=0;
	@log_senjutu = "0<>普通に戦う<>戦術を使用せずに戦います<>0<>\n";

	# 現在の職業の戦術のみ
	open(IN,"$tac_folder/tac$chara[14].ini");
	@gettac = <IN>;
	close(IN);
	foreach (@gettac){
		($ks_no,$ks_name,$ks_plus,$ks_ms) = split(/<>/);
		if (!$ks_ms || ($ks_ms && $chara[33] >= 60)) {
			push(@log_senjutu,"$_");
			if($chara[30] eq "$ks_no"){
				$hit = 1;
				$now_tac = $ks_name;
				$now_tac_ex = $ks_plus;
			}
		}
	}

	#マスターした戦術のインクルード
	if ($master_tac) {
		&syoku_load;
		$i = 0;
		foreach (@syoku_master) {
			if ($_ >= 60 && $i != $chara[14]) {
				open(IN,"$tac_folder/tac$i.ini");
				@gettac = <IN>;
				close(IN);
				push(@log_senjutu,@gettac);
				foreach (@gettac){
					($ks_no,$ks_name,$ks_plus,$ks_ms) = split(/<>/);
					if($chara[30] eq "$ks_no"){
						$hit = 1;
						$now_tac = $ks_name;
						$now_tac_ex = $ks_plus;
					}
				}
			}
			$i++;
		}
	}

	if(!$hit) {
		$now_tac = "普通に戦う";
		$now_tac_ex = "戦術を使用せずに戦います";
	}

	&header;

	print <<"EOM";
<h1>作戦会議室</h1>
<hr size=0>
<BR>
<form action="$scripts" method="post">
<table>
<tr>
<th colspan=2>戦術</th>
<tr><td class=b1>現在の戦術</td><td class=b1>$now_tac</td><td class=b1>$now_tac_ex</td>
</tr>
EOM

	foreach(@log_senjutu){
		($s_no,$s_name,$s_ex,$s_mas) = split(/<>/);
		print "<tr>\n";
		print "<td class=b1><input type=radio name=senjutu_no value=\"$s_no\"></td><td class=b1>$s_name</td><td class=b1>$s_ex</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=senjutu_henkou>
<input type=submit class=btn value="変更する">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#----------------#
#  戦術変更      #
#----------------#
sub senjutu_henkou {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	@log_senjutu = "0<>普通に戦う<>0<>0<>\n";

	open(IN,"$tac_folder/tac$chara[14].ini");
	@gettac = <IN>;
	close(IN);
	foreach (@gettac){
		($ks_no,$ks_name,$ks_plus,$ks_ms) = split(/<>/);
		# 2004年7月7日修正
		if(!$ks_ms || ($ks_ms && $chara[33] >= 60)){
			push(@log_senjutu,"$_");
		}
	}

	#マスターした戦術のインクルード
	if ($master_tac) {
		&syoku_load;
		$i = 0;
		foreach (@syoku_master) {
			if ($_ >= 60 && $i != $chara[14]) {
				open(IN,"$tac_folder/tac$i.ini");
				@gettac = <IN>;
				close(IN);
				push(@log_senjutu,@gettac);
				foreach (@gettac){
					($ks_no,$ks_name,$ks_plus,$ks_ms) = split(/<>/);
					if($chara[30] eq "$ks_no"){
						$hit = 1;
						$now_tac = $ks_name;
					}
				}
			}
			$i++;
		}
	}

	$hit=0;
	foreach(@log_senjutu){
		($s_no,$s_name) = split(/<>/);
		if($in{'senjutu_no'} eq "$s_no") { $hit=1;last; }
	}

	if(!$hit) { &error("そんな戦術はありません"); }

	&get_host;

	$chara[30] = $in{'senjutu_no'};

	&chara_regist;
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<h1>戦術を$s_nameに変更しました</h1>
<hr size=0>
<form action="$script" method="post">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$new_chara">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

