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
<form action="$acs_shop" method="post">
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
if($mode) { &$mode; }

&item_view;

exit;

#----------------#
#  アイテム表示  #
#----------------#
sub item_view {

	&chara_load;

	&chara_check;

	open(IN,"$acs_file");
	@log_acs = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup,$a_ex) = split(/<>/);
		if($chara[31] eq "$a_no"){ $hit=1;last; }
	}

	if(!$hit) {
		$a_name="なし";
		$a_gold="0";
		$a_ex = "-";
	}

	$ui_gold = int($a_gold / 3) * 2;


	open(IN,"$acs_folder/acs$chara[14].ini");
	@acs_array = <IN>;
	close(IN);

	&header;

	print <<"EOM";
<h1>アクセサリーショップ</h1>
<hr size=0>

<FONT SIZE=3>
<B>装飾品屋のマスター</B><BR>
「ふっ。。冷やかしならさっさと帰りな。。。<BR>
　ん？、おまえ<B>$chara[4]</B>じゃないか。
<BR>おまえ柄にもなく$chara_syoku[$chara[14]]をやってるらしいじゃないか。。。
<BR>
この店の品物をおまえごときが使えこなせると思っているのか？
<BR><BR>で、どれを買うんだ？」
</FONT>
<br><hr>現在の所持金：$chara[19] Ｇ<br>
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>説明</th><th>価格</th></tr>
<tr>
<form action="$acs_shop" method="post">
<th><input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value=item_sell>
EOM
if ($hit) { print "<input type=submit class=btn value=\"売る\">"; }
	print <<"EOM";
</th></form><th>現在の装備品</th><th>$a_name</th><th>$a_ex</th><th>$ui_gold</th></tr></table>
<form action="$acs_shop" method="post">
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>説明</th><th>価格</th></tr>
EOM

	foreach (@acs_array) {
		($ai_no,$ai_name,$ai_gold,$ai_kouka,$ai_0up,$ai_1up,$ai_2up,$ai_3up,$ai_4up,$ai_5up,$ai_6up,$ai_lpup,$ai_hitup,$ai_kaihiup,$ai_wazaup,$ai_msg) = split(/<>/);
		print "<tr><td class=b1 align=\"center\">\n";
		if ($chara[19] >= $ai_gold) {
			print "<input type=radio name=item_no value=\"$ai_no\">";
		} else {
			print "×";
		}
		print "</td><td align=right class=b1>$ai_no</td><td class=b1>$ai_name</td><td align=right class=b1>$ai_msg</td><td align=right class=b1>$ai_gold</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</table>
<input type=hidden name=id value=$in{'id'}>
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value=item_buy>
<input type=submit class=btn value="装飾品を買う">
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

	open(IN,"$acs_folder/acs$chara[14].ini");
	@acs_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@acs_array){
		($ai_no,$ai_name,$ai_gold,$ai_kouka,$ai_0up,$ai_1up,$ai_2up,$ai_3up,$ai_4up,$ai_5up,$ai_6up,$ai_lpup,$ai_hitup,$ai_kaihiup,$ai_wazaup,$ai_msg) = split(/<>/);
		if($in{'item_no'} eq "$ai_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	if($chara[19] < $ai_gold) { &error("お金が足りません$back_form"); }
	else { $chara[19] = $chara[19] - $ai_gold; }

	$chara[26] = $host;

	$lock_file = "$lockfolder/acsesa$in{'id'}.lock";
	&lock($lock_file,'SA');
	open(IN,"$souko_folder/acs/$chara[0].cgi");
	@souko_acs = <IN>;
	close(IN);

	$souko_acs_num = @souko_acs;

	if ($souko_acs_num >= $acs_max) {
		&error("装飾品倉庫がいっぱいです！$back_form");
	}

	push(@souko_acs,"$ai_no<>$ai_name<>$ai_gold<>$ai_kouka<>$ai_0up<>$ai_1up<>$ai_2up<>$ai_3up<>$ai_4up<>$ai_5up<>$ai_6up<>$ai_lpup<>$ai_hitup<>$ai_kaihiup<>$ai_wazaup<>$ai_msg<>\n");

	open(OUT,">$souko_folder/acs/$chara[0].cgi");
	print OUT @souko_acs;
	close(OUT);
	&unlock($lock_file,'SA');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE=3>
<B>装飾品屋のマスター</B><BR>
「毎度あり～！<br>
買った装飾品はあんたの装飾品倉庫に送っておいたよ！
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

	open(IN,"$acs_file");
	@acs_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@acs_array){
		($i_no,$i_name,$i_gold) = split(/<>/);
		if($chara[31] eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }
	if(!$chara[31]) { &error("そんなアイテムは存在しません"); }
	$ui_gold = int($i_gold / 3) * 2;

	$chara[19] = $chara[19] + $ui_gold;
	if($chara[19] > $gold_max){$chara[19] = $gold_max;}

	$chara[31] = 0;

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&lock($lock_file,'IM');
	&item_load;

	&acs_lose;

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
