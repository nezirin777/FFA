#!/usr/local/bin/perl

#------------------------------------------------------#
#　FF ADVENTURE v0.21
#　programed by CUMRO
#　http://cgi.members.interq.or.jp/sun/cumro/mm/
#　cumro@sun.interq.or.jp
#
#  FF ADVENTURE(改) v1.040
#  remodeling by GUN
#  http://www2.to/meeting/
#  gun24@j-club.ne.jp
#
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#-----------------------------------------------------#
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

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
$method="POST";          
#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}
&rank;
exit;

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#┃   オートローダー
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sub AUTOLOAD {
	my $name = ($AUTOLOAD =~ /^main::(.+)$/)[0];
	($FLAG{'autoload'}++ > 50) && die $AUTOLOAD; # 念のため無限ループ防止
	defined %SUB or &SUBS;
	if (!defined $SUB{$name}) {
		&error("定義されていない関数($AUTOLOAD)が呼ばれました。"); exit;
	}
	eval $SUB{$name}; length($@) && &error("EVAL ERROR: $@ ($AUTOLOAD)");
	delete $SUB{$name}; goto &{'main::' . $name};
}

sub SUBS {
%SUB = (
	rank => <<'__SUB__',
#------------------#
#  ランキング表示  #
#------------------#
sub rank {
	# キャラデータ読み込み
	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		@WORK=<IN>;
		if($WORK[0] ne ""){
		push(@level,"@WORK[0]");
		}close(IN);
		}

	}
	closedir(DIR);

	$sousu = @level;

	# 配列19番目でソート
	@tmp = map {(split /<>/)[18]} @level;
	@level = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列17番目でソート
	@tmp = map {(split /<>/)[16]} @level;
	@hitp = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列8番目でソート
	@tmp = map {(split /<>/)[7]} @level;
	@atack = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列9番目でソート
	@tmp = map {(split /<>/)[8]} @level;
	@def = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列10番目でソート
	@tmp = map {(split /<>/)[9]} @level;
	@rp = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列11番目でソート
	@tmp = map {(split /<>/)[10]} @level;
	@gp = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列12番目でソート
	@tmp = map {(split /<>/)[11]} @level;
	@sp = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列13番目でソート
	@tmp = map {(split /<>/)[12]} @level;
	@bp = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列14番目でソート
	@tmp = map {(split /<>/)[13]} @level;
	@lp = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列21番目でソート
	@tmp = map {(split /<>/)[20]} @level;
	@yen = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列20番目でソート
	@tmp = map {(split /<>/)[19]} @level;
	@lyen = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	&header;

	print <<"EOM";
<H3>英雄たちの記録</H3>
<FONT SIZE="3">それぞれのステータスのTOP10を表\示しています。
<P>全登録キャラクター数は、<B>$sousu</B>人です。
</FONT>
<P>
| <A HREF="$scripto">戻る</A> |
<HR SIZE=0>
EOM
	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "レベル</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">LV</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@level){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$klv\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}

	print "</TABLE>\n";

	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "HP</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">HP</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@hitp){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kmaxhp\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "ちから</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ちから</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@atack){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_0\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "知\能\</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">知\能\</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@def){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_1\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";


	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "信仰心</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">信仰心</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@rp){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_2\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "生命力</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">生命力</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@gp){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_3\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "器用さ</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">器用さ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@sp){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_4\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "速さ</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">速さ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@bp){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_5\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "魅力</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">魅力</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@lp){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kn_6\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "カルマ</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">カルマ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@yen){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$klp\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<TABLE BORDER=0>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "お金</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">お金</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@lyen){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		print "<TR><TD ALIGN=\"right\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD>\n";
		print "$kname\n";
		print "</TD>\n";
		print "<TD ALIGN=\"right\">\n";
		print "$kgold\n";
		print "</TD>\n";
		print "<TD>\n";
		print "$url\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<P><HR SIZE=0>\n";
	print "| <A HREF=\"$scripto\">戻る</A> |\n";

	&footer;

	exit;
}
__SUB__

	header => <<'__SUB__',
#------------#
#  ヘッダー  #
#------------#
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<SCRIPT Language="JavaScript" src="$java_script"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
<!---新しいウィンドウを開く
function wopen(){
window.open("rommode.html","hpmff","toolbar=0,menubar=0,scrollbars=0,width=370,height=400")
}
//end --->
</SCRIPT>
<link rel="stylesheet" href=$style_sheet type"text.css"><TITLE>$main_title</TITLE>
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
</head>
$body
EOM
}
__SUB__

	footer => <<'__SUB__',
#------------#
#　フッター　#
#------------#
sub footer {
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
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
);
}
