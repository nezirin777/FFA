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
#  http://www8.big.or.jp/~k-kiku/cbbs/wforum.cgi
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
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　           #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
if($mente) { &error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m"); }
&decode;
if($mode eq 'cyado') { &cyado; }
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
	cyado => <<'__SUB__',
#------------#
#  体力回復  #
#------------#
sub cyado {
	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi") or &error('ファイルを開けませんでした。');
	@YADO = <IN>;
	close(IN);

	foreach(@YADO){
		($yid,$ypass,$ysite,$yurl,$yname,$ysex,$ychara,$yn_0,$yn_1,$yn_2,$yn_3,$yn_4,$yn_5,$yn_6,$ysyoku,$yhp,$ymaxhp,$yex,$ylv,$ygold,$ylp,$ytotal,$ykati,$ywaza,$yitem,$ymons,$yhost,$ydate,$ymori,$ydef,$ytac,$yacsno,$ymoriturn,$ycllv,$ys0,$ys1,$ys2,$ys3,$ys4,$ys5,$ys6,$ys7,$ys8,$ys9,$ys10,$ys11,$ys12,$ys13,$ys14,$ys15,$ys16,$ys17,$ys18,$ys19,$ys20,$ys21,$ys22,$ys23,$ys24,$ys25,$ys26,$ys27,$ys28,$ys29,$ys30,$yrec) = split(/<>/);

	}

	open(IN,"$chocolog_file") or &error('ファイルを開けませんでした。');
	@CYADO = <IN>;
	close(IN);

	foreach(@CYADO){
		($c_id,$c_pass,$c_kname,$c_no,$c_name,$c_gold,$c_rank,$c_sp,$c_sta,$c_maxsta,$c_ex,$c_total,$c_kati,$c_0,$c_1,$c_2,$c_3,$c_4,$c_5,$c_6,$c_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($in{'id'} eq "$c_id" and $in{'pass'} eq "$c_pass") {last;}
	}

	if($c_sta eq $c_maxsta) { &error("チョコボはまだまだ元気です。"); }

	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi") or &error('ファイルを開けませんでした。');
	@yado_chara = <IN>;
	close(IN);

	$hit=0;@yado_new=();
	foreach(@yado_chara){
		($yid,$ypass,$ysite,$yurl,$yname,$ysex,$ychara,$yn_0,$yn_1,$yn_2,$yn_3,$yn_4,$yn_5,$yn_6,$ysyoku,$yhp,$ymaxhp,$yex,$ylv,$ygold,$ylp,$ytotal,$ykati,$ywaza,$yitem,$ymons,$yhost,$ydate,$ymori,$ydef,$ytac,$yacsno,$ymoriturn,$ycllv,$ys0,$ys1,$ys2,$ys3,$ys4,$ys5,$ys6,$ys7,$ys8,$ys9,$ys10,$ys11,$ys12,$ys13,$ys14,$ys15,$ys16,$ys17,$ys18,$ys19,$ys20,$ys21,$ys22,$ys23,$ys24,$ys25,$ys26,$ys27,$ys28,$ys29,$ys30,$yrec) = split(/<>/);
	$cyado_daix = int($c_rank * $yado_dai);
		if($in{'id'} eq "$yid" and $in{'pass'} eq "$ypass") {
			if($in{'id'} ne "$yid" or $in{'pass'} ne "$ypass"){&error("オープンエラー、ID・パスワードが正しくありません。");}
			if($ygold < $cyado_daix) { &error("お金が足りません"); }
			else { $ygold = $ygold - $cyado_daix; }
			unshift(@yado_new,"$yid<>$ypass<>$ysite<>$yurl<>$yname<>$ysex<>$ychara<>$yn_0<>$yn_1<>$yn_2<>$yn_3<>$yn_4<>$yn_5<>$yn_6<>$ysyoku<>$yhp<>$ymaxhp<>$yex<>$ylv<>$ygold<>$ylp<>$ytotal<>$ykati<>$ywaza<>$yitem<>$ymons<>$host<>$ydate<>$ymori<>$ydef<>$ytac<>$yacsno<>$ymoriturn<>$ycllv<>$ys0<>$ys1<>$ys2<>$ys3<>$ys4<>$ys5<>$ys6<>$ys7<>$ys8<>$ys9<>$ys10<>$ys11<>$ys12<>$ys13<>$ys14<>$ys15<>$ys16<>$ys17<>$ys18<>$ys19<>$ys20<>$ys21<>$ys22<>$ys23<>$ys24<>$ys25<>$ys26<>$ys27<>$ys28<>$ys29<>$ys30<>$yrec<>\n");
		}else{
			push(@yado_new,"$_");
		}
	}

	open(IN,"$chocolog_file") or &error('ファイルを開けませんでした。');
	@cyado_chara = <IN>;
	close(IN);

	$hit=0;@cyado_new=();
	foreach(@cyado_chara){
		($c_id,$c_pass,$c_kname,$c_no,$c_name,$c_gold,$c_rank,$c_sp,$c_sta,$c_maxsta,$c_ex,$c_total,$c_kati,$c_0,$c_1,$c_2,$c_3,$c_4,$c_5,$c_6,$c_life,$c_kon,$c_waza,$c_money) = split(/<>/);
		if($in{'id'} eq "$c_id" and $in{'pass'} eq "$c_pass") {
			$c_life += int(rand(9) + 3);
	unshift(@cyado_new,"$c_id<>$c_pass<>$c_kname<>$c_no<>$c_name<>$c_gold<>$c_rank<>$c_sp<>$c_maxsta<>$c_maxsta<>$c_ex<>$c_total<>$c_kati<>$c_0<>$c_1<>$c_2<>$c_3<>$c_4<>$c_5<>$c_6<>$c_life<>$c_kon<>$c_waza<>$c_money<>\n");
	}else{
		push(@cyado_new,"$_");
		}
	}

	open(OUT,">$chocolog_file");
	print OUT @cyado_new;
	close(OUT);

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @yado_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>チョコボを休ませました。</h1>
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
	print "<input type=hidden name=id value=$in{'id'}>\n";
	print "<input type=hidden name=pass value=$in{'pass'}>\n";
	print "<input type=hidden name=mode value=log_in>\n";
	print "<input type=submit class=btn value=\"ステータス画面へ\">\n";
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
	print "<embed src=\"$sts_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__
);
}
