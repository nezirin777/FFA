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

# アイテムライブラリの読み込み
require 'item.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $shop_back;
$midi = $shop_midi;

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) {
	&error("現在バージョンアップ中です。しばらくお待ちください。");
}

&decode;

	$back_form = << "EOM";
<br>
<form action="$def_shop" method="post">
<input type=hidden name=id value=$in{'id'}>
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type=submit class=btn value="戻る">
</form>
EOM

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}
if($mode) { &$mode; }

&item_view;

exit;

#----------------#
#  アイテム表示  #
#----------------#
sub item_view {

	&chara_load;

	&chara_check;

	open(IN,"$def_file");
	@log_item = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_item){
		($si_no,$si_name,$si_dmg,$si_gold) = split(/<>/);
		if($chara[29] eq "$si_no"){ $hit=1;last; }
	}

	if(!$hit) {
		$si_name="普段着";
		$si_dmg="0";
		$si_gold="0";
	}

	$ui_gold = int($si_gold / 3) * 2;


	open(IN,"$def_folder/def$chara[14].ini");
	@item_array = <IN>;
	close(IN);

	&header;

	print <<"EOM";
<h1>防具屋</h1>
<hr size=0>

<FONT SIZE=3>
<B>防具屋のマスター</B><BR>
「いらっしゃい！いい防具揃ってるよ～。この大陸の中じゃ、うちが一番の品揃えだよ！<BR>
　あ、なんだい、<B>$chara[4]</B>じゃないか。元気にしてたかい？
<BR>今は$chara_syoku[$chara[14]]をやってるのか。
<BR>昨日$chara_syoku[$chara[14]]用の防具を入荷したんだよ！
<BR>
　まあ、ゆっくり見ていってくれ。
<BR><BR>そうそう！最近装備品の下取りもはじめたんだ。」
</FONT>
<br><hr>現在の所持金：$chara[19] Ｇ<br>
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>威力</th><th>価格</th></tr>
<tr>
<form action="$def_shop" method="post">
<th><input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value=item_sell>
EOM
if ($hit) { print "<input type=submit class=btn value=\"売る\">"; }
	print <<"EOM";
</th></form><th>現在の装備品</th><th>$si_name</th><th>$si_dmg</th><th>$ui_gold</th></tr></table>
<form action="$def_shop" method="post">
<table>
EOM

	foreach (@item_array) {
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print "<tr><td class=b1 align=\"center\">\n";
		if ($chara[19] >= $igold) {
			print "<input type=radio name=item_no value=\"$ino\">";
		} else {
			print "×";
		}
		print "</td><td align=right class=b1>$ino</td><td class=b1>$iname</td><td align=right class=b1>$idmg</td><td align=right class=b1>$igold</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</table>
<input type=hidden name=id value=$in{'id'}>
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value=item_buy>
<input type=submit class=btn value="防具を買う">
</form>
EOM

	$new_chara = $chara_log;
	&shopfooter;

	&footer;

	exit;
}

#----------------#
#  アイテム買う  #
#----------------#
sub item_buy {
	

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	open(IN,"$def_folder/def$chara[14].ini");
	@item_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@item_array){
		($d_no,$d_name,$d_dmg,$d_gold,$d_hit) = split(/<>/);
		if($in{'item_no'} eq "$d_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	if($chara[19] < $d_gold) { &error("お金が足りません$back_form"); }
	else { $chara[19] = $chara[19] - $d_gold; }

	$chara[26] = $host;

	$lock_file = "$lockfolder/sdefe$in{'id'}.lock";
	&lock($lock_file,'SD');
	open(IN,"$souko_folder/def/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item_num = @souko_item;

	if ($souko_item_num >= $def_max) {
		&error("防具倉庫がいっぱいです！$back_form");
	}

	push(@souko_item,"$d_no<>$d_name<>$d_dmg<>$d_gold<>$d_hit<>\n");

	open(OUT,">$souko_folder/def/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SD');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE=3>
<B>防具屋のマスター</B><BR>
「毎度あり～！<br>
買った防具はあんたの防具倉庫に送っておいたよ！
」</font>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#----------------#
#  アイテム売る  #
#----------------#
sub item_sell {
	

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$chara[26] = $host;

	open(IN,"$def_file");
	@item_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@item_array){
		($i_no,$i_name,$i_dmg,$i_gold) = split(/<>/);
		if($chara[29] eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }
	if(!$chara[29]) { &error("そんなアイテムは存在しません"); }
	$ui_gold = int($i_gold / 3) * 2;

	$chara[19] = $chara[19] + $ui_gold;
	if($chara[19] > $gold_max){$chara[19] = $gold_max;}

	$chara[29] = 0;

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&lock($lock_file,'IM');
	&item_load;

	&def_lose;

	&item_regist;
	&unlock($lock_file,'IM');

	&header;

	print <<"EOM";
<h1>$i_nameを売りました</h1>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}
