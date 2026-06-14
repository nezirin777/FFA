#!/usr/local/bin/perl

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#								#
#　　アイテム（武器＆防具の装着交換）ＣＧＩ　簡易版		#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# キャラクタデータの配列添字の定義 $chara_d[]
$kid=0;$kpass=1;$ksite=2;$kurl=3;$kname=4;$ksex=5;$kchara=6;$kn_0=7;$kn_1=8;$kn_2=9;$kn_3=10;$kn_4=11;$kn_5=12;$kn_6=13;$ksyoku=14;$khp=15;$kmaxhp=16;$kex=17;$klv=18;$kgold=19;$klp=20;$ktotal=21;$kkati=22;$kwaza=23;$kitem=24;$kmons=25;$khost=26;$kdate=27;$kmori=28;$kdef=29;$ktac=30;$kacsno=31;$kmoriturn=32;$kcllv=33;$ks0=34;$ks1=35;$ks2=36;$ks3=37;$ks4=38;$ks5=39;$ks6=40;$ks7=41;$ks8=42;$ks9=43;$ks10=44;$ks11=45;$ks12=46;$ks13=47;$ks14=48;$ks15=49;$ks16=50;$ks17=51;$ks18=52;$ks19=53;$ks20=54;$ks21=55;$ks22=56;$ks23=57;$ks24=58;$ks25=59;$ks26=60;$ks27=61;$ks28=62;$ks29=63;$ks30=64;$krec=65;

# キャラクタデータファイル
$chara1 = "./charalog/";

# 追加キャラクタデータディレクトリ
$chara2 = "./charalog2/";

# 武器保有最大数 ffadventure.iniで定義
# $item_max[0] = 10; 
# 武器データの配列 $weapon_d[]
# 添え字　0：保有数（装着分を除く）1～$item_max[0]：武器ナンバーを記録

# 防具保有最大数 ffadventure.iniで定義
# $item_max[1] = 10;
# 防具データの配列 $protector_d[]
# 添え字　0：保有数（装着分を除く）1～$item_max[1]：防具ナンバーを記録

# 防具保有最大数 ffadventure.iniで定義
# $item_max[2] = 10;
# アクセサリーデータの配列 $acs_d[]
# 添え字　0：保有数（装着分を除く）1～$item_max[2]：防具ナンバーを記録

# 表示切り替え用サフィックス
@suf = ("_wd","_pd","_ad","_wc","_pc","_ac");#(武器削除,防具削除,アクセサリー削除,武器交換,防具交換,アクセサリー交換)

# 表示ループ切り替え用データ
@koumoku = ("","");#(武器,防具)

# アイテムデータの配列添字の定義$item_d[]
$k_num=0;$k_name=1;$k_dmg=2;$k_gold=3;

@d_sex = ("男","女");

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
if($mode eq 'c_house') { &c_house; }
if($mode eq 'c_house_exec') { &c_house_exec; }
#&error("このＣＧＩを動作させるのに必要な情報が不足しています。");
exit;

#------------------#
#  カプセルハウス  #
#------------------#
sub c_house {
	&disp;
	exit;
}

#--------------#
# 　実行する　 #
#--------------#
sub c_house_exec {
	$read_file = "$chara2$in{'id'}.cgi";
	&s_data_read;		#追加キャラクタデータ読み込み
	@have_item = @read_data;

	($item_num,$kind) = split(/_/,$in{'item_no'});
	if($kind =~ /w/) { $n=0;}
	if($kind =~ /p/) { $n=1;}
	if($kind =~ /a/) { $n=2;}

	if(!( $have_item[$n] =~ /$item_num/ )) { &error("そんなアイテムは存在しません"); }

	$read_file = "$chara1$in{'id'}.cgi";
	&chara_data_read;	#キャラクタデータ読み込み
	if ($chara_d[$kitem] eq "0" || $chara_d[$kitem] eq "" ) { $chara_d[$kitem] = "0000"; }
	if ($chara_d[$kdef] eq "0" || $chara_d[$kdef] eq "" ) { $chara_d[$kdef] = "0000"; }
	if ($chara_d[$kacsno] eq "0" || $chara_d[$kacsno] eq "" ) { $chara_d[$kacsno] = "0000"; }

	if($kind eq 'wd') {
		$have_item[0] =~ s/$item_num/0000/;
		@item_d = split(/,/,$have_item[0]);
		$item_d[0]--;
		if($item_d[0]<0) {$item_d[0]=0;}
		$have_item[0] = join(",",@item_d);
	}

	if($kind eq 'pd') {
		$have_item[1] =~ s/$item_num/0000/;
		@item_d = split(/,/,$have_item[1]);
		$item_d[0]--;
		if($item_d[0]<0) {$item_d[0]=0;}
		$have_item[1] = join(",",@item_d);
	}

	if($kind eq 'ad') {
		$have_item[2] =~ s/$item_num/0000/;
		@item_d = split(/,/,$have_item[2]);
		$item_d[0]--;
		if($item_d[0]<0) {$item_d[0]=0;}
		$have_item[2] = join(",",@item_d);
	}

	if($kind eq 'wc') {
		$have_item[0] =~ s/$item_num/$chara_d[$kitem]/;
		@item_d = split(/,/,$have_item[0]);
		if($chara_d[$kitem] eq "0000") {$item_d[0]--;}
		if($item_num eq "0000") {$item_d[0]++;}
		if($item_d[0]<0) {$item_d[0]=0;}
		$have_item[0] = join(",",@item_d);
		$chara_d[$kitem] = $item_num;
		if($chara_d[$kitem] eq "0000") {$chara_d[$kitem] = "";}
	}

	if($kind eq 'pc') {
		$have_item[1] =~ s/$item_num/$chara_d[$kdef]/;
		@item_d = split(/,/,$have_item[1]);
		if($chara_d[$kdef] eq "0000") {$item_d[0]--;}
		if($item_num eq "0000") {$item_d[0]++;}
		if($item_d[0]<0) {$item_d[0]=0;}
		$have_item[1] = join(",",@item_d);
		$chara_d[$kdef] = $item_num;
		if($chara_d[$kdef] eq "0000") {$chara_d[$kdef] = "";}
	}

	if($kind eq 'ac') {
		$have_item[2] =~ s/$item_num/$chara_d[$kacsno]/;
		@item_d = split(/,/,$have_item[2]);
		if($chara_d[$kacsno] eq "0000") {$item_d[0]--;}
		if($item_num eq "0000") {$item_d[0]++;}
		if($item_d[0]<0) {$item_d[0]=0;}
		$have_item[2] = join(",",@item_d);
		$chara_d[$kacsno] = $item_num;
		if($chara_d[$kacsno] eq "0000") {$chara_d[$kacsno] = "";}
	}

	@new_data = @have_item;
	$write_file = "$chara2$in{'id'}.cgi";
	&data_write;

	$write_file = "$chara1$in{'id'}.cgi";
	&chara_data_write;	#キャラクタデータ書き込み

	&disp;
	exit;
}

#----------------#
#  　画面表示　  #
#----------------#
sub disp {
	$read_file = "$chara1$in{'id'}.cgi";
	&chara_data_read;	#キャラクタデータ読み込み

	$chara_flag=1;
	$kcllv = $chara_d[$klv];
	&class;
	$klv=18;
	$next_ex = $chara_d[$klv] * $lv_up;

	$read_file = "$chara2$in{'id'}.cgi";
	$valign = 0;
	&s_data_read;		#追加キャラクタデータ読み込み
	@have_item = @read_data;
	($dummy_w1,$dummy_w2) = split(/,/,$have_item[0]);
	($dummy_p1,$dummy_p2) = split(/,/,$have_item[1]);
	($dummy_a1,$dummy_a2) = split(/,/,$have_item[2]);

	$read_file = $item_file;
	&c_data_read;		#武器データファイル読み込み
	$n = 0;$wp=$kitem;
	&item_pick_up;
	$i_name = $item_name; $i_dmg = $item_dmg;
	@weapon_list = @item_list;

	$read_file = $def_file;
	&c_data_read;		#防具データファイル読み込み
	$n=1;$wp=$kdef;
	&item_pick_up;
	$d_name = $item_name; $d_dmg = $item_dmg;
	@protector_list = @item_list;

	$read_file = $acs_file;
	&c_data_read;		#アクセサリーデータファイル読み込み
	$n=2;$wp=$kacsno;
	&item_pick_up;
	$a_name = $item_name; $a_dmg = $item_dmg;
	@acs_list = @item_list;

	$chara_d[$khp]=$chara_d[$kmaxhp];	#ＨＰの自動回復

	&header;

	print <<"EOM";
<CENTER>
<TABLE>
<TBODY>
<TD colspan="2" align="center"><B><FONT size="4">飛空艇</FONT></B></TD>
</TR><TR>
<td><img src="$img_path/mog.gif" BORDER=0 ></A></TD>
<td class="b3">
<FONT color="#aaaaff">「</FONT><FONT color="#ffff00"><b>$chara_d[$kname]</b></FONT><FONT color="#aaaaff">、お帰りなさい♪毎日の戦闘で疲れたでしょ。<BR>食事と風呂の仕度ができてるよ。ＨＰはボクの魔法で回復させておくからね！<BR>
EOM

	if (($dummy_w1 eq '0' && $dummy_p1 eq '0') || ( $valign eq '1')) {
		print "それから、装備品を置いていくなら預かるよ。シドがさっき直してくれたんだ♪\n";
	}
	else {
		print "それから、預かってる装備品は大切にしまってあるよ、交換する？<BR>\n";
	}

	print <<"EOM";
それじゃ、ゆっくりしてってね。」</FONT>
</TD></TR>
</TBODY>
</TABLE>
</CENTER>
<hr size=0>
<CENTER>
<TABLE border="0">
<TBODY>
<TR><TD>
      <B><FONT color="#ff0000">シド</FONT></B><FONT color="#00ffff">「町まで行くのなら脱出ポットを使うと便利だよ。」</FONT><BR>
<table><tr><td align="center" class="b2">
<form action="$scripts" method="post">
<input type=hidden name=id value=$chara_d[$kid]>
<input type=hidden name=pass value=$chara_d[$kpass]>
<input type=hidden name=mode value=bank_shop>
<input type=submit class=btn value="銀行へ"></td>
<td align="center" class="b2"></form>
<form action="$scripts" method="post">
<input type=hidden name=id value=$chara_d[$kid]>
<input type=hidden name=pass value=$chara_d[$kpass]>
<input type=hidden name=mode value=kunren>
<input type=submit class=btn value="訓練所"></td>
</tr></table></form>
【<a href=\"$scripto\">TOPページへ</a>】
【<a href=\"$script?mode=log_in&id=$chara_d[$kid]&pass=$chara_d[$kpass]\">ステータス画面へ</a>】
</td>
<td valign=top width='65%'>
<table border=1 width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">$chara_d[$kname]さんのステータス</td></tr>
<tr><td rowspan="8" align="center" valign=bottom><img src="$img_path/$chara_img[$chara_d[$kchara]]">
<br>
<table width="100%" border=1>
<tr><td class="b2">武器</td><td align="right">$i_name</td></tr>
<tr><td class="b1">攻撃力</td><td align="right">$i_dmg</td></tr>
<tr><td class="b2">防具</td><td align="right">$d_name</td></tr>
<tr><td class="b1">防御力</td><td align="right">$d_dmg</td></tr>
<tr><td class="b2">アクセサリー</td><td align="right">$a_name</td></tr>
</table></td>
<td class="b1">なまえ</td><td>$chara_d[$kname]</td><td class="b1">職業</td><td>$chara_syoku[$chara_d[$ksyoku]]</td></tr>
<tr><td class="b1">レベル</td><td>$chara_d[$klv]</td><td class="b1">経験値</td><td>$chara_d[$kex]/$next_ex</td></tr>
<tr><td class="b1">お金</td><td>$chara_d[$kgold]</td><td class="b1">HP</td><td>$chara_d[$khp]\/$chara_d[$kmaxhp]</td></tr>
<tr><td class="b1">力</td><td>$chara_d[$kn_0]</td><td class="b1">知能\</td><td>$chara_d[$kn_1]</td></tr>
<tr><td class="b1">信仰心</td><td>$chara_d[$kn_2]</td><td class="b1">生命力</td><td>$chara_d[$kn_3]</td></tr>
<tr><td class="b1">器用さ</td><td>$chara_d[$kn_4]</td><td class="b1">速さ</td><td>$chara_d[$kn_5]</td></tr>
<tr><td class="b1">魅力</td><td>$chara_d[$kn_6]</td><td class="b1">カルマ</td><td>$chara_d[$klp]</td></tr>
</table></td></tr>
</table>

<table border=0 align="center" width='90%'>
<tr><td valign=top width='90%'>
<table border=1 align="center" width='90%'>
<form action="./c_house.cgi" method="post">
<tr><td id="td1" class="b2" align="center">【武器】</td><td id="td1" class="b2" align="center">【防具】</td><td id="td1" class="b2" align="center">【アクセサリー】</td></tr>
<tr>
EOM

	$n=0;
	@item_list = @weapon_list;
	&disp_item_list;

	$n=1;
	@item_list = @protector_list;
	&disp_item_list;

	$n=2;
	@item_list = @acs_list;
	&disp_item_list;

	print <<"EOM";
</tr></table>
</td></tr></table>
</td></tr></table>
<p><CENTER>
<input type=hidden name=id value=$in{'id'}>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=c_house_exec>
<input type=submit class=btn value="実行する/更新">
</form></CENTER>
EOM

	$write_file = "$chara1$in{'id'}.cgi";
	&chara_data_write;	#キャラクタデータ書き込み

	&footer;

}

#----------------------#
# アイテムピックアップ #
#----------------------#
sub item_pick_up {
	$i=1;
	$item_name="－"; $item_dmg="－";
	chop($have_item[$n]);
	@items1 = split(/,/,$have_item[$n]);
	shift @items1;
	foreach (@read_data){
		@item_d = split(/<>/);
		if( $chara_d[$wp] eq $item_d[$k_num] ) {	#現在装備中のアイテムピックアップ
			$item_name=$item_d[$k_name]; $item_dmg=$item_d[$k_dmg];
		}
		if( $have_item[$n] =~ /$item_d[$k_num]/ ) {	#現在保有中のアイテムピックアップ
			foreach $item1 (@items1) {
				if ( $item1 eq $item_d[$k_num] ) { 
					$item_list[$i] = $_;
					$i++;
				}
			}
		}
	}
	$item_list[0] = $i;
}

#--------------------#
# アイテムリスト表示 #
#--------------------#
sub disp_item_list {
	print "<td valign=\"top\"><table border=1 width=\"100%\">\n";
	print "<tr><th>捨てる</th><th>交換</th><th>No.</th><th>なまえ</th></tr>\n";
	for ($i=1; $i<$item_list[0]; $i++) {
		@item_d = split(/<>/,$item_list[$i]);
			print "<tr>\n";
			print "<td align=center><input type=radio name=item_no value=\"$item_d[$k_num]$suf[$n]\"></td>\n";
			print "<td align=center><input type=radio name=item_no value=\"$item_d[$k_num]$suf[$n+3]\"></td>\n";
			print "<td align=center>$item_d[$k_num]</td><td class=\"b2\">$item_d[$k_name]</td>\n";
			#print "<td align=right>$item_d[$k_dmg]</td>\n";
			print "</tr>\n";
	}
	for ($i=$item_list[0]; $i<=$item_max[$n]; $i++) {
			print "<tr>\n";
			print "<td align=center><input type=radio name=item_no value=\"0000$suf[$n]\"></td>\n";
			print "<td align=center><input type=radio name=item_no value=\"0000$suf[$n+3]\"></td>\n";
			print "<td align=center>－－</td><td class=\"b2\">－－－－</td>\n";
			
			print "</tr>\n";
	}
	print "</table></td>\n";
}

#------------------------#
#キャラクタデータ読み込み#
#------------------------#
sub chara_data_read {
	open(IN,"$read_file") || &error("キャラクターが見つかりません"); 
	$chara_data = <IN>;
	close(IN);

	@chara_d = split(/<>/,$chara_data);
	if(!($in{'id'} eq $chara_d[$kid] and $in{'pass'} eq $chara_d[$kpass])) { &error("ＩＤかパスワードが違います$in{'id'}  $chara_d[$kid] $in{'pass'} $chara_d[$kpass]"); }
}

#------------------------#
#キャラクタデータ書き込み#
#------------------------#
sub chara_data_write {
	# ファイルロック（個人用ファイルで、一人しかアクセスしないので、たぶんロックする必要はないですね(^^;）
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	$chara_new = join("<>",@chara_d);
	open(OUT,">$write_file") || &error("キャラクターファイルが見つかりません");
	print OUT $chara_new;
	close(OUT);
	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }
}

#------------------------#
#   帳票データ読み込み   #
#------------------------#
sub c_data_read {
	open(IN,"$read_file") || &error("$read_fileファイルが見つかりません");
	@read_data = <IN>;
	close(IN);
}

#------------------------#
#   単票データ読み込み   #
#------------------------#
sub s_data_read {
	open(IN,"$read_file") || &make_new_file;
	@read_data = <IN>;
	close(IN);
}

#単票データファイルが無かった時、新規作成
sub make_new_file {
	$valign = 1;
	$weapon_d[0]=0;
	for ($i=1; $i<=$item_max[0]; $i++) {
		$weapon_d[$i]="0000";
	}
	$weapon = join(",",@weapon_d);
	$protector_d[0]=0;
	for ($i=1; $i<=$item_max[1]; $i++) {
		$protector_d[$i]="0000";
	}
	$protector = join(",",@protector_d);
	$acs_d[0]=0;
	for ($i=1; $i<=$item_max[2]; $i++) {
		$acs_d[$i]="0000";
	}
	$acs = join(",",@acs_d);
	@new_data = ("$weapon\n","$protector\n","$acs\n");
	$write_file = $read_file;
	&data_write;
}

#--------------------------------#
#   帳票単票共用データ書き込み   #
#--------------------------------#
sub data_write {
	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(OUT,">$write_file") || &error("$write_fileファイルがオープン出来ません");
	print OUT @new_data;
	close(OUT);
	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }
}

#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {
	print "<DIV align=left>\n";
	print "<a href=\"$scripto\">TOPページへ</a>\n";
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
	 print "FFA Emilia・いく改ver1.00 remodeling by <a href=\"http://www3.big.or.jp/~icu/\" target=\"_top\">いく</a><br>\n";
	 print "画像提供 by <a href=\"http://www.wisnet.ne.jp/~jnkw/index.html\" target=\"_top\">Jinkun</a><br>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 edit by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Emilia</a><br>\n";
        
	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
	print "</DIV></body></html>\n";
}

#------------------#
#  HTMLのヘッダー  #
#------------------#
sub header {
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<SCRIPT Language="JavaScript" src="$java_script"></SCRIPT>
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
  background-image : url($backgif);
  background-attachment : fixed;
}
.red{font-family : $font_name;color:$red;}
.yellow{font-family : $font_name;color:$yellow;}
.blue{font-family : $font_name;color:$blue;}
.green{font-family : $font_name;color:$green;}
.white{font-family : $font_name;color:$white;}
.dark{font-family : $font_name;color:$dark;}
.small{font-size:8px;$font_name;color:$red;}
//-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	print "<embed src=\"$hiku_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
