#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権は下記の4人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
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

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

# このファイル用設定
$backgif = $sts_back;
$midi = $sts_midi;
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

#------------------#
#  ランキング表示  #
#------------------#
sub rank {

	if (!$no_html) { &error("負荷が大きいのでHTML生成できないサーバーでは使用できません"); }

	$lock_file = "$lockfolder/tim.lock";
	&lock($lock_file,'TM');
	open(IN,"$all_data_time");
	@all_time = <IN>;
	close(IN);

	$hit=0;
	foreach(@all_time){
		($rankmode,$ranktime) = split(/<>/);
		if ($rankmode eq "sranking") { $hit=1;last; }
	}

	$lrtime = time();
	$btime = $lrtime - $ranktime;
	$ztime = int($btime/3600);
	$ranking_make = 0;

	if ($btime > 3600*24 || !$hit) {

		$hit=0;
		@item_new=();
		foreach (@all_time) {
			($rankmode,$ranktime) = split(/<>/);
			if ($rankmode eq "sranking") {
				unshift(@item_new,"sranking<>$lrtime<>\n");
				$hit=1;
			} else {
				push(@item_new,"$_");
			}
		}

		if (!$hit) { unshift(@item_new,"sranking<>$lrtime<>\n"); }

		open(OUT,">$all_data_time");
		print OUT @item_new;
		close(OUT);
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');

		$ranking_make = 1;

	} else {
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');
	}

	if ($ranking_make) {

	&all_data_read;

	$sousu = @RANKING;

	# 配列19番目でソート
	@tmp = map {(split /<>/)[18]} @RANKING;
	@levela = @RANKING[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列17番目でソート
	@tmp = map {(split /<>/)[16]} @levela;
	@hitp = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列8番目でソート
	@tmp = map {(split /<>/)[7]} @levela;
	@atack = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列9番目でソート
	@tmp = map {(split /<>/)[8]} @levela;
	@def = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列10番目でソート
	@tmp = map {(split /<>/)[9]} @levela;
	@rp = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列11番目でソート
	@tmp = map {(split /<>/)[10]} @levela;
	@gp = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列12番目でソート
	@tmp = map {(split /<>/)[11]} @levela;
	@sp = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列13番目でソート
	@tmp = map {(split /<>/)[12]} @levela;
	@bp = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列14番目でソート
	@tmp = map {(split /<>/)[13]} @levela;
	@lp = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列21番目でソート
	@tmp = map {(split /<>/)[20]} @levela;
	@yen = @levela[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	foreach(@levela){
		@chara = split(/<>/);

		if ($chara[21] > 1000) {
			$kati_ritu = int($chara[22]*10000/$chara[21])/100;
			unshift(@win_new,"$chara[4]<>$chara[3]<>$chara[2]<>$kati_ritu<>$chara[21]<>$chara[18]<>$chara[0]<>\n");
		}
	}

	# 配列3番目でソート
	@tmp = map {(split /<>/)[3]} @win_new;
	@win_new = @win_new[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];


	$buffer = <<"EOM";
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Pragma" content="no-cache">
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<SCRIPT Language="JavaScript" src="$java_script" type="text/javascript">
</SCRIPT>
<STYLE type="text/css">
<!--
BODY{
  font-family : $font_name;
  font-size:12px;
  color:$text;
  background-image : url($html_path$backgif);
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
<link rel="stylesheet" href="$html_path$style_sheet" type="text/css">
<title>$main_title</title></head>
<body background="$html_path$backgif" bgcolor="$bgcolor" text="$text" link="$link" vlink="$vlink" alink="$alink">
EOM
		if ($midi_set) {
			$buffer .= "<embed src=\"$html_path$midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
		}
	local(@mody)=localtime($ltime);
	$mody[4]++;

		$buffer .= <<"EOM";
<H3>英雄たちの記録</H3>
<FONT SIZE="3">それぞれのステータスのTOP10を表\示しています。<br>
<font size =3 color =red><b>ただし、更新は１日に１回しか行われません。</b></font>前回は$mody[4]月$mody[3]日$mody[2]時$mody[1]分に更新されました。<br>

全登録キャラクター数は、<B>$sousu</B>人です。
</FONT>
<HR SIZE=0>
EOM
	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="レベル</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">LV</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@levela){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[18]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}

	$buffer.="</TABLE>\n";

	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="HP</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">HP</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@hitp){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[16]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";

	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="ちから</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ちから</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@atack){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[7]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";

	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="知\能\</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">知\能\</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@def){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[8]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";


	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="信仰心</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">信仰心</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@rp){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[9]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";



	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="生命力</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">生命力</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@gp){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[10]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";



	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="器用さ</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">器用さ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@sp){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[11]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";



	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="速さ</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">速さ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@bp){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[12]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";



	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="魅力</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">魅力</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@lp){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[13]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";

	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="カルマ</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">カルマ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@yen){
		@chara = split(/<>/);
		$url="<A HREF=\"$chara[3]\" TARGET=\"_blank\">$chara[2]</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="$chara[20]\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";

	$buffer.="<TABLE BORDER=0>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	$buffer.="勝率</TD></TR>\n";
	$buffer.="<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">勝率</TD><TD ALIGN=\"center\" CLASS=\"b1\">ホームページ</TD>\n";

	$i=1;
	foreach(@win_new){
		($kname,$kurl,$ksite,$kati_ritu,$ktotal,$klv,$kid)=split(/<>/);
		$url="<A HREF=\"http\:\/\/$kurl\" TARGET=\"_blank\">$ksite</A>";
		$buffer.="<TR><TD ALIGN=\"right\">\n";
		$buffer.="<B>$i</B></TD>\n";
		$buffer.="<TD>\n";
		$buffer.="<a href=\"../$scripta?mode=chara_sts&id=$kid\">$kname</a>\n";
		$buffer.="</TD>\n";
		$buffer.="<TD ALIGN=\"right\">\n";
		$buffer.="<b>$kati_ritu</b>％($ktotal戦)\n";
		$buffer.="</TD>\n";
		$buffer.="<TD>\n";
		$buffer.="$url\n";
		$buffer.="</TD>\n";
		$buffer.="</TR>\n";
		$i++;
		if($i >10){last;}
	}
	$buffer.="</TABLE>\n";

	$buffer.= <<"EOM";
<HR SIZE=0 WIDTH="100%">
<a href = "$html_path$scripto">$main_titleのTOPへ</a>
<HR SIZE=0 WIDTH="100%"><DIV align=right>
FFA いく改ver2.00 edit by <a href="http://www.eriicu.com" target="_top">いく</a><br>
FFA Emilia Ver1.01 remodeled by Classic(閉鎖)<br>
FF Battle De I v3.06 remodeling by <a href="http://www.mj-world.jp/" target="_blank">jun-k</a>(更新停止中)<br>
FF ADVENTURE(改) v1.040 remodeled by <a href="http://www.gun-online.com" target="_blank">ＧＵＮ</a><br>
FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) <a href="http://www5c.biglobe.ne.jp/~ma-ti/" target="_blank">現配布元(管理者ma-ti)</a><br>
</DIV></body></html>
EOM

		open(LOG,">./rankhtml/sougorank.html");
		print LOG $buffer;
		close(LOG);

	}

        print "Location: $no_html/sougorank.html\n\n";

	exit;

}
