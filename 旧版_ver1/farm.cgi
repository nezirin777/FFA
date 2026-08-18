#!/usr/local/bin/perl

#------------------------------------------------------#
#　FF ADVENTURE v0.21
#　programed by CUMRO
#　http://cgi.members.interq.or.jp/sun/cumro/mm/
#　cumro@sun.interq.or.jp
#
#  FF ADVENTURE(改) v1.101
#  remodeling by GUN
#  http://www.gun-online.com/
#  webmaster@gun-online.com
#
#  FF ADVENTURE(改) + v1.040
#  EDIT by Laldar
#  http://www8.big.or.jp/~k-kiku/ff/index.html
#
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#  このＣＧＩについての質問は下記サポートＢＢＳまで
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した #
#    いかなる損害に対して作者は一切の責任を負いません。     	#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。   	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require './jacode.pl';

# レジストライブラリの読み込み
require './regist.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';


# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
if($mode eq 'choco_eqq0') { $choco_file = $choco_file; &choco_shop; }
elsif($mode eq 'choco_shop') { &choco_shop; }
elsif($mode eq 'choco_buy') { &choco_buy; }
elsif($mode eq 'choco_sell') { &choco_sell; }
exit;

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃   オートローダー
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sub AUTOLOAD {
	my $name = ($AUTOLOAD =~ /^main::(.+)$/)[0];
	($FLAG{'autoload'}++ > 50) && die $AUTOLOAD; # 念のため無限ループ防止
	unless (%SUB) {&SUBS};
	if (!$SUB{$name}) {
		&error("定義されていない関数($AUTOLOAD)が呼ばれました。"); exit;
	}
	eval $SUB{$name}; length($@) && &error("EVAL ERROR: $@ ($AUTOLOAD)");
	delete $SUB{$name}; goto &{'main::' . $name};
}

sub SUBS {
%SUB = (
	choco_shop => <<'__SUB__',
#-------------------#
#  チョコボファーム #
#-------------------#
sub choco_shop {


	open(IN,"./charalog/$in{'id'}.cgi");
	@choco = <IN>;
	close(IN);

	$hit=0;
	foreach(@choco){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$chocolog_file");
	@log_choco = <IN>;
	close(IN);

	foreach(@log_choco){
	($cy_id,$cy_pass,$cy_kname,$cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
			if($in{'id'} eq "$cy_id" and $in{'pass'} eq "$cy_pass"){ $hit=1;last; }
	}

	if(!$hit) { $cy_name="－"; }

	if(!$hit) { $ui_gold="0"; }
	else { $ui_gold = int($cy_gold / 3) * 2 + int($cy_rank * 10) + int($cy_kati * 2);}

	open(IN,"$chocobo_file");
	@choco_array = <IN>;
	close(IN);

	&header;

	print <<"EOM";
<h1>チョコボファーム</h1>
<hr size=0>
<p>
<form action="$scriptcho" method="post">
<FONT SIZE=3>
<B>ファームのおじさん</B><BR>
「あんれま！お客さんだべか。こんなへんぴな牧場まで、よくきたのう<BR>
　しかも、<B>$kname</B>でねえか。びっくりだ。
<BR>こんな所に$chara_syoku[$ksyoku]さんが何の用だべ？
<BR>なに？おらっちのチョコボさ目当てか？それならはよ言うてくれんと。
<BR>チョコボを買い替える時は一度売ってくれな。<BR>ほれ、こっちだべ。」
</FONT><BR><BR>
<table border=0>
<td id="td2" class="b2"><b>名前</b></td><td class="b2"><b>$kname　　　　</b></td>
<tr>
<td id="td2" class="b2"><b>職業</b></td><td class="b2"><b>$chara_syoku[$ksyoku]</b></td>
<tr>
<td id="td2" class="b2"><b>持ってるチョコボ</b></td><td class="b2"><b>$cy_name</b></td>
<tr>
<td id="td2" class="b2"><b>売値</b></td><td class="b2"><b>$ui_goldギル　　　</b></td>
<tr>
<td id="td2" class="b2"><b>所持金</b></td><td class="b2"><b>$kgoldギル　　　</b></td>

<tr>
<td colspan=2><input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=choco_sell>
<input type=submit class=btn  value="今のチョコボを売ってしまう">
</td></table></form>
<table border=0>
<tr>
<th class=\"b2\"></th><th class=\"b2\">No.</th><th class=\"b2\"></th><th class=\"b2\">なまえ</th><th class=\"b2\">価格</th><th class=\"b2\">おじさんからのコメント</th></tr>
<tr><form action="$scriptcho" method="post">
EOM

	foreach(@choco_array){
		($cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money,$cy_komen) = split(/<>/);

		print "<tr>\n";
		print "<td  class=\"b2\"><input type=radio name=item_no value=\"$cy_no\"></td><td align=right  class=\"b2\">$cy_no</td><td class=\"b2\"><img src=\"$img_path/$choco_img[$cy_no]\"></td><td  class=\"b2\">$cy_name</td><td align=right  class=\"b2\">$cy_gold</td><td class=\"b2\">$cy_komen</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<p><td class="b2"><input type=text name=st_name value="ボコちゃん♪">※チョコボに好きな名前が付けられます。</td>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=choco_buy>
<input type=submit class=btn  value="チョコボを買う">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	choco_buy => <<'__SUB__',
#------------------#
#  チョコボを買う  #
#------------------#
sub choco_buy {

   	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi");
	@choco = <IN>;
	close(IN);

	foreach(@choco){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$chocobo_file");
	@choco_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@choco_array){
		($cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money,$cy_komen) = split(/<>/);
		if($in{'item_no'} eq "$cy_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなチョコボは存在しません"); }
         $s_name=$in{'st_name'};
	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi");
	@cyoco_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@cyoco_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			if($igold < $cy_gold) { &error("お金が足りません"); }
			else { $igold = $igold - $cy_gold; }
			unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;last;
		}else{
			push(@item_new,"$_");
		}
	}

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @item_new;
	close(OUT);

	open(IN,"$chocolog_file");
	@choco_chara = <IN>;
	close(IN);

	$hit=0;@choco_new=();
	foreach(@choco_chara){
	($c_id,$c_pass,$c_kname,$c_no,$c_name,$c_gold,$c_rank,$c_sp,$c_sta,$c_maxsta,$c_ex,$c_total,$c_kati,$c_0,$c_1,$c_2,$c_3,$c_4,$c_5,$c_6,$c_life,$c_kon,$c_waza,$c_money,$c_komen) = split(/<>/);
		if($c_id eq "$kid") {
		$n_no = $c_no;
		$n_name = $s_name;
		$n_gold = $c_gold;
		$n_rank = $c_rank;
		$n_sp = $c_sp;
		$n_sta = $c_sta;
		$n_maxsta = $c_maxsta;
		$n_ex = $y_ex;
		$n_total = $c_total;
		$n_kati = $c_kati;
		$n_0 = $c_0;
		$n_1 = $c_1;
		$n_2 = $c_2;
		$n_3 = $c_3;
		$n_4 = $c_4;
		$n_5 = $c_5;
		$n_6 = $c_6;
		$n_life = $c_life;
                $n_kon = $c_kon;
                $n_waza = $c_waza;
                $n_money = $c_money;

	unshift(@choco_new,"$c_id<>$c_pass<>$c_kname<>$n_no<>$n_name<>$n_gold<>$n_rank<>$n_sp<>$n_sta<>$n_maxsta<>$n_ex<>$n_total<>$n_kati<>$n_0<>$n_1<>$n_2<>$n_3<>$n_4<>$n_5<>$n_6<>$n_life<>$n_kon<>$n_waza<>$n_money<>\n");
	$hit=1;
	}else{
	push(@choco_new,"$_");
	}
	}

	if(!$hit){
	unshift(@choco_new,"$kid<>$kpass<>$kname<>$cy_no<>$s_name<>$cy_gold<>$cy_rank<>$cy_sp<>$cy_sta<>$cy_maxsta<>$cy_ex<>$cy_total<>$cy_kati<>$cy_0<>$cy_1<>$cy_2<>$cy_3<>$cy_4<>$cy_5<>$cy_6<>$cy_life<>$cy_kon<>$cy_waza<>$cy_money<>\n");
	}

	open(OUT,">$chocolog_file");
	print OUT @choco_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>チョコボを買いました</h1>
<hr size=0>
<p>

EOM

	&footer;

	exit;
}
__SUB__

	choco_sell => <<'__SUB__',
#------------------#
#  チョコボを売る  #
#------------------#
sub choco_sell {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@choco = <IN>;
	close(IN);

	foreach(@choco){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$chocolog_file");
	@choco_chara = <IN>;
	close(IN);

	$hit=0;@choco_new=();
	foreach(@choco_chara){
	($c_id,$c_pass,$c_kname,$c_no,$c_name,$c_gold,$c_rank,$c_sp,$c_sta,$c_maxsta,$c_ex,$c_total,$c_kati,$c_0,$c_1,$c_2,$c_3,$c_4,$c_5,$c_6,$c_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($c_id eq "$kid") {
		$ui_gold = int($c_gold / 3) * 2 + int($c_rank * 10) + int($c_kati * 2);
	unshift(@choco_new,"");
	$hit=1;
	}else{
	push(@choco_new,"$_");
	}
	}

	open(OUT,">$chocolog_file");
	print OUT @choco_new;
	close(OUT);


	open(IN,"$chocobo_file");
	@choco_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@choco_array){
		($cy_no,$cy_name,$cy_kname,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($cy_no eq "$c_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなチョコボは存在しません"); }
	if(!$cy_no) { &error("チョコボを持ってません"); }

	&get_host;

	$date = time();


	@item_chara = ();
	open(IN,"./charalog/$in{'id'}.cgi");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			$igold = $igold + $ui_gold;
			unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;last;
		}else{
			push(@item_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @item_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>チョコボを売りました</h1>
<hr size=0>
<p>
EOM

	&footer;

	exit;
}
__SUB__

	footer => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {

	print "<form action=\"$script\" method=\"post\">\n";
	print "<A HREF=\"$scripto\">ＴＯＰページへ</A>\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$in{'pass'}>\n";
	print "<input type=hidden name=mode value=log_in>\n";
	print "<input type=submit class=btn  value=\"ステータス画面へ\">\n";
	print "</form>\n";

	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 edit by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";

	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	header => <<'__SUB__',
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
EOM

	if($access_flg) {
	print <<"EOM";
<SCRIPT language="JavaScript">
<!--
if(parent.location == location) location = "$top_url";
if(document.referrer =="") location = "$top_url";
//-->
</SCRIPT>
EOM
	}
	print <<"EOM";
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
-->
</STYLE>
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	print "<embed src=\"$farm_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__
);
}
