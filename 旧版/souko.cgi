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

	$back_form = << "EOM";
<br>
<form action="$script_souko" method="post">
<input type=hidden name=id value="$in{'id'}">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type=submit class=btn value="戻る">
</form>
EOM

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) {
	&error("現在バージョンアップ中です。しばらくお待ちください。");
}

&decode;

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

	&item_load;

	open(IN,"$souko_folder/item/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	open(IN,"$souko_folder/def/$chara[0].cgi");
	@souko_def = <IN>;
	close(IN);

	open(IN,"$souko_folder/acs/$chara[0].cgi");
	@souko_acs = <IN>;
	close(IN);

	&header;

	print <<"EOM";
<h1>アイテム倉庫</h1>
<hr size=0>

<FONT SIZE=3>
<B>倉庫管理人</B><BR>
「
$chara[4]様に預かっている道具は下のようになっております
」
</FONT>
<br><hr>現在の装備<br>
<table>
<tr>
<td id="td2" class="b2">武器</td><td align="right" class="b2">$item[0]</td>
<td id="td2" class="b2">攻撃力</td><td align="right" class="b2">$item[1]</td>
EOM
	if ($chara[24]) {
	print <<"EOM";
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value="item_hazusi">
<input type=submit class=btn value="外す">
</td>
</form>
EOM
	}
	print <<"EOM";
</tr>
<tr>
<td id="td2" class="b2">防具</td><td align="right" class="b2">$item[3]</td>
<td id="td2" class="b2">防御力</td><td align="right" class="b2">$item[4]</td>
EOM
	if ($chara[29]) {
	print <<"EOM";
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value="def_hazusi">
<input type=submit class=btn value="外す">
</td>
</form>
EOM
	}
	print <<"EOM";
</tr>
<tr>
<td id="td2" class="b2">装飾品</td><td align="right" class="b2">$item[6]</td>
<td id="td2" class="b2">説明</td><td align="right" class="b2">$item[19]</td>
EOM
	if ($chara[31]) {
	print <<"EOM";
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value="acs_hazusi">
<input type=submit class=btn value="外す">
</td>
</form>
EOM
	}
	print <<"EOM";
</tr>
</table>
<table width = "100%">
<tr>
<td width = "30%" align = "center" valign = "top">
武器倉庫
<table width = "98%">
<tr><th></th><th></th><th nowrap>なまえ</th><th nowrap>攻撃力</th><th nowrap>価格</th></tr>
EOM
	$i = 0;
	foreach (@souko_item) {
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print << "EOM";
<tr>
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$i">
<input type=hidden name=mode value="item_soubi">
<input type=submit class=btn value="装備する">
</td>
</form>
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$i">
<input type=hidden name=mode value="item_delete">
<input type=submit class=btn value="捨てる">
</td>
</form>
<td class=b1 nowrap>$iname</td>
<td align=right class=b1>$idmg</td>
<td align=right class=b1>$igold</td>
</tr>
EOM
	$i++;
	}
		print << "EOM";
</table>
</td>
<td width = "30%" align = "center" valign = "top">
防具倉庫
<table width = "98%">
<tr><th></th><th></th><th nowrap>なまえ</th><th nowrap>防御力</th><th nowrap>価格</th></tr>
EOM
	$i = 0;
	foreach (@souko_def) {
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print << "EOM";
<tr>
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$i">
<input type=hidden name=mode value="def_soubi">
<input type=submit class=btn value="装備する">
</td>
</form>
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$i">
<input type=hidden name=mode value="def_delete">
<input type=submit class=btn value="捨てる">
</td>
</form>
<td class=b1 nowrap>$iname</td>
<td align=right class=b1>$idmg</td>
<td align=right class=b1>$igold</td>
</tr>
EOM
	$i++;
	}
		print << "EOM";
</table>
</td>
<td width = "40%" align = "center" valign = "top">
装飾品倉庫
<table width = "98%">
<tr><th></th><th></th><th>なまえ</th><th>説明</th><th>価格</th></tr>
EOM

	$i = 0;
	foreach (@souko_acs) {
		($ai_no,$ai_name,$ai_gold,$ai_kouka,$ai_0up,$ai_1up,$ai_2up,$ai_3up,$ai_4up,$ai_5up,$ai_6up,$ai_lpup,$ai_hitup,$ai_kaihiup,$ai_wazaup,$ai_msg) = split(/<>/);
		print << "EOM";
<tr>
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$i">
<input type=hidden name=mode value="acs_soubi">
<input type=submit class=btn value="装備する">
</td>
</form>
<form action="$script_souko" method="post">
<td class=b1 align="center">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$i">
<input type=hidden name=mode value="acs_delete">
<input type=submit class=btn value="捨てる">
</td>
</form>
<td class=b1 nowrap>$ai_name</td>
<td align=right class=b1>$ai_msg</td>
<td align=right class=b1>$ai_gold</td>
</tr>
EOM
	$i++;
	}
		print << "EOM";
</table>
</td></table>
EOM

	$new_chara = $chara_log;
	&shopfooter;

	&footer;

	exit;
}

#------------#
#  武器装備  #
#------------#
sub item_soubi {
	

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&lock($lock_file,'IM');
	&item_load;

	$chara[26] = $host;

	$lock_file = "$lockfolder/sitem$in{'id'}.lock";
	&lock($lock_file,'SI');
	open(IN,"$souko_folder/item/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item[$in{'item_no'}] =~ s/\n//g;
	$souko_item[$in{'item_no'}] =~ s/\r//g;

	($ino,$iname,$idmg,$igold,$ihit) = split(/<>/,$souko_item[$in{'item_no'}]);

	if ($chara[24]) {
		&item_read($chara[24]);
		$souko_item[$in{'item_no'}] = "$ci_no<>$item[0]<>$item[1]<>$ci_gold<>$item[2]<>\n";
	} else {
		$souko_item[$in{'item_no'}] = ();
	}

	open(OUT,">$souko_folder/item/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SI');

	$chara[24] = $ino;
	$item[0] = $iname;
	$item[1] = $idmg;
	$item[2] = $ihit;

	&item_regist;
	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&unlock($lock_file,'IM');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE=3>
<B>$inameを装備しました</B><BR>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#------------#
#  武器解除  #
#------------#
sub item_hazusi {

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$chara[26] = $host;

	open(IN,"$item_file");
	@item_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@item_array){
		($i_no,$i_name,$i_dmg,$i_gold,$ihit) = split(/<>/);
		if($chara[24] eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	$lock_file = "$lockfolder/sitem$in{'id'}.lock";
	&lock($lock_file,'SI');
	open(IN,"$souko_folder/item/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item_num = @souko_item;

	if ($souko_item_num >= $item_max) {
		&error("武器倉庫がいっぱいです！$back_form");
	}

	push(@souko_item,"$i_no<>$i_name<>$i_dmg<>$i_gold<>$ihit<>\n");

	open(OUT,">$souko_folder/item/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);

	&unlock($lock_file,'SI');

	$chara[24] = 0;

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&lock($lock_file,'IM');
	&item_load;

	&item_lose;

	&item_regist;
	&unlock($lock_file,'IM');

	&header;

	print <<"EOM";
<FONT SIZE=3>
<B>$i_nameを外しました</B><BR>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#----------------#
#  武器を捨てる  #
#----------------#
sub item_delete {
	

	&get_host;

	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/sitem$in{'id'}.lock";
	&lock($lock_file,'SI');
	open(IN,"$souko_folder/item/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item[$in{'item_no'}] =~ s/\n//g;
	$souko_item[$in{'item_no'}] =~ s/\r//g;

	($ino,$iname,$idmg,$igold,$ihit) = split(/<>/,$souko_item[$in{'item_no'}]);

	if (!$in{'kakunin'}){

		&unlock($lock_file,'SI');

		&header;

		print << "EOM";
<center>
<h2>本当に$inameを捨てますか？</h2>
<form action="$script_souko" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$in{'item_no'}">
<input type=hidden name=kakunin value="1">
<input type=hidden name=mode value="item_delete">
<input type=submit class=btn value="捨てる">
</form>
</center>
EOM

		$new_chara = $chara_log;

		&shopfooter;

		&footer;

		exit;

	}

	$souko_item[$in{'item_no'}] = ();

	open(OUT,">$souko_folder/item/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SI');

	&header;

	print <<"EOM";
<h1>$inameを捨てました</h1>
<hr size=0>
EOM

	$new_chara = $chara_log;

	&shopfooter;

	&footer;

	exit;
}

#------------#
#  防具装備  #
#------------#
sub def_soubi {
	

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&lock($lock_file,'IM');
	&item_load;

	$chara[26] = $host;

	$lock_file = "$lockfolder/sdefe$in{'id'}.lock";
	&lock($lock_file,'SD');
	open(IN,"$souko_folder/def/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item[$in{'item_no'}] =~ s/\n//g;
	$souko_item[$in{'item_no'}] =~ s/\r//g;

	($ino,$iname,$idmg,$igold,$ihit) = split(/<>/,$souko_item[$in{'item_no'}]);

	if ($chara[29]) {
		&def_read($chara[29]);
		$souko_item[$in{'item_no'}] = "$cd_no<>$item[3]<>$item[4]<>$cd_gold<>$item[5]<>\n";
	} else {
		$souko_item[$in{'item_no'}] = ();
	}

	open(OUT,">$souko_folder/def/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SD');

	$chara[29] = $ino;
	$item[3] = $iname;
	$item[4] = $idmg;
	$item[5] = $ihit;

	&item_regist;
	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&unlock($lock_file,'IM');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE=3>
<B>$inameを装備しました</B><BR>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#------------#
#  防具解除  #
#------------#
sub def_hazusi {

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
		($i_no,$i_name,$i_dmg,$i_gold,$ihit) = split(/<>/);
		if($chara[29] eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	$lock_file = "$lockfolder/sdefe$in{'id'}.lock";
	&lock($lock_file,'SD');
	open(IN,"$souko_folder/def/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item_num = @souko_item;

	if ($souko_item_num >= $def_max) {
		&error("防具倉庫がいっぱいです！$back_form");
	}

	push(@souko_item,"$i_no<>$i_name<>$i_dmg<>$i_gold<>$ihit<>\n");

	open(OUT,">$souko_folder/def/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);

	&unlock($lock_file,'SD');

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
<FONT SIZE=3>
<B>$i_nameを外しました</B><BR>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#----------------#
#  武器を捨てる  #
#----------------#
sub def_delete {
	

	&get_host;

	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/sdefe$in{'id'}.lock";
	&lock($lock_file,'SD');
	open(IN,"$souko_folder/def/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item[$in{'item_no'}] =~ s/\n//g;
	$souko_item[$in{'item_no'}] =~ s/\r//g;

	($ino,$iname,$idmg,$igold,$ihit) = split(/<>/,$souko_item[$in{'item_no'}]);

	if (!$in{'kakunin'}){

		&unlock($lock_file,'SD');

		&header;

		print << "EOM";
<center>
<h2>本当に$inameを捨てますか？</h2>
<form action="$script_souko" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$in{'item_no'}">
<input type=hidden name=kakunin value="1">
<input type=hidden name=mode value="def_delete">
<input type=submit class=btn value="捨てる">
</form>
</center>
EOM

		$new_chara = $chara_log;

		&shopfooter;

		&footer;

		exit;

	}

	$souko_item[$in{'item_no'}] = ();

	open(OUT,">$souko_folder/def/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SD');

	&header;

	print <<"EOM";
<h1>$inameを捨てました</h1>
<hr size=0>
EOM

	$new_chara = $chara_log;

	&shopfooter;

	&footer;

	exit;
}

#------------#
#  装飾装備  #
#------------#
sub acs_soubi {
	

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&lock($lock_file,'IM');
	&item_load;

	$chara[26] = $host;

	$lock_file = "$lockfolder/acsesa$in{'id'}.lock";
	&lock($lock_file,'SA');
	open(IN,"$souko_folder/acs/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item[$in{'item_no'}] =~ s/\n//g;
	$souko_item[$in{'item_no'}] =~ s/\r//g;

	@acs_data = split(/<>/,$souko_item[$in{'item_no'}]);

	if ($chara[31]) {
		&acs_read($chara[31]);
		$souko_item[$in{'item_no'}] = "$a_no<>$item[6]<>$a_gold<>$item[7]<>$item[8]<>$item[9]<>$item[10]<>$item[11]<>$item[12]<>$item[13]<>$item[14]<>$item[15]<>$item[16]<>$item[17]<>$item[18]<>$item[19]<>\n";
	} else {
		$souko_item[$in{'item_no'}] = ();
	}

	open(OUT,">$souko_folder/acs/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SA');

	$chara[31] = $acs_data[0];
	$item[6] = $acs_data[1];
	for ($i=3;$i<=15;$i++) {
		$s = $i + 4;
		$item[$s] = $acs_data[$i];
	}

	&item_regist;
	$lock_file = "$lockfolder/item$in{'id'}.lock";
	&unlock($lock_file,'IM');

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<FONT SIZE=3>
<B>$acs_data[1]を装備しました</B><BR>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#------------#
#  防具解除  #
#------------#
sub acs_hazusi {

	&get_host;

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	$chara[26] = $host;

	open(IN,"$acs_file");
	@item_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@item_array){
		$acs_array = $_;
		@acs_data = split(/<>/);
		if($chara[31] eq "$acs_data[0]") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	$lock_file = "$lockfolder/acsesa$in{'id'}.lock";
	&lock($lock_file,'SA');
	open(IN,"$souko_folder/acs/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item_num = @souko_item;

	if ($souko_item_num >= $def_max) {
		&error("防具倉庫がいっぱいです！$back_form");
	}

	push(@souko_item,"$acs_array");

	open(OUT,">$souko_folder/acs/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SA');

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
<FONT SIZE=3>
<B>$acs_data[1]を外しました</B><BR>
<hr size=0>
EOM

	&shopfooter;

	&footer;

	exit;
}

#----------------#
#  武器を捨てる  #
#----------------#
sub acs_delete {
	

	&get_host;

	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/acsesa$in{'id'}.lock";
	&lock($lock_file,'SA');
	open(IN,"$souko_folder/acs/$chara[0].cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item[$in{'item_no'}] =~ s/\n//g;
	$souko_item[$in{'item_no'}] =~ s/\r//g;

	($ino,$iname) = split(/<>/,$souko_item[$in{'item_no'}]);

	if (!$in{'kakunin'}){

		&unlock($lock_file,'SA');

		&header;

		print << "EOM";
<center>
<h2>本当に$inameを捨てますか？</h2>
<form action="$script_souko" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=item_no value="$in{'item_no'}">
<input type=hidden name=kakunin value="1">
<input type=hidden name=mode value="acs_delete">
<input type=submit class=btn value="捨てる">
</form>
</center>
EOM

		$new_chara = $chara_log;
		&shopfooter;

		&footer;

		exit;

	}

	$souko_item[$in{'item_no'}] = ();

	open(OUT,">$souko_folder/acs/$chara[0].cgi");
	print OUT @souko_item;
	close(OUT);
	&unlock($lock_file,'SA');


	&header;

	print <<"EOM";
<h1>$inameを捨てました</h1>
<hr size=0>
EOM

	$new_chara = $chara_log;

	&shopfooter;

	&footer;

	exit;
}
