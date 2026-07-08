#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#　いかなる理由があってもこの表記を削除することはできません
#　違反を発見した場合、スクリプトの利用を停止していただく
#　だけでなく、然るべき処置をさせていただきます。
#  チョコボ牧場 edit by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#     http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi 		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 牧場ライブラリの読み込み
require 'choco-farm.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $farm_back;
$midi = $farm_midi;
$style_sheet = $chococss;

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

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}

if($in{'mode'} eq 'ranking'){&ranking;}
else{&rank;}
exit;

#------------------#
#  ランキング表示  #
#------------------#
sub ranking {

	@level=();

	# キャラデータ読み込み
	opendir(DIR,'./chocolog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./chocolog/$entry");
		@WORK=<IN>;
		if($WORK[0] ne ""){
		push(@level,"@WORK");
		}close(IN);
		}

	}
	closedir(DIR);

	$sousu = @level;

	# 配列20番目でソート
	@tmp = map {(split /<>/)[19]} @level;
	@win = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列18番目でソート
	@tmp = map {(split /<>/)[17]} @level;
	@train = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列22番目でソート
	@tmp = map {(split /<>/)[21]} @level;
	@tikara = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列23番目でソート
	@tmp = map {(split /<>/)[22]} @level;
	@stamina = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列24番目でソート
	@tmp = map {(split /<>/)[23]} @level;
	@nebari = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列25番目でソート
	@tmp = map {(split /<>/)[24]} @level;
	@otituki = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列26番目でソート
	@tmp = map {(split /<>/)[25]} @level;
	@tousou = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列27番目でソート
	@tmp = map {(split /<>/)[26]} @level;
	@tiryoku = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列28番目でソート
	@tmp = map {(split /<>/)[27]} @level;
	@kire = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# 配列29番目でソート
	@tmp = map {(split /<>/)[28]} @level;
	@lyen = @level[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	&header;

	print <<"EOM";
<center><H3>サラブレッドチョコボたちの記録</H3>
<FONT SIZE="3">それぞれのステータスのTOP10を表\示しています。
<P>全登録サラブレッドチョコボ数は、<B>$sousu</B>人です。
</FONT>
<P>
| <A HREF="$scripto">戻る</A> |
<HR SIZE=0>
EOM
	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "レベル</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">名前</TD><TD ALIGN=\"center\" CLASS=\"b1\">勝利数</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@win){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);

		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cwin勝\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}

	print "</TABLE>\n";

	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "練習量</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">練習量</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@train){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);

		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$ctrain\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";


	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "筋力</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">筋力</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@tikara){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);
		if($c1 > 1000){$ctikara = "<img src =$img_farm/ss.gif>";}
		elsif($c1 > 800){$ctikara = "<img src =$img_farm/s.gif>";}
		elsif($c1 > 600){$ctikara = "<img src =$img_farm/a.gif>";}
		elsif($c1 > 400){$ctikara = "<img src =$img_farm/b.gif>";}
		elsif($c1 > 200){$ctikara = "<img src =$img_farm/c.gif>";}
		elsif($c1 > 100){$ctikara = "<img src =$img_farm/d.gif>";}
		else{$ctikara = "<img src =$img_farm/e.gif>";}



		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$ctikara\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";


	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "スタミナ</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">スタミナ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@stamina){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);
		if($c2 > 1000){$tairyoku = "<img src =$img_farm/ss.gif>";}
		elsif($c2 > 800){$tairyoku = "<img src =$img_farm/s.gif>";}		elsif($c2 > 600){$tairyoku = "<img src =$img_farm/a.gif>";}		elsif($c2 > 400){$tairyoku = "<img src =$img_farm/b.gif>";}		elsif($c2 > 200){$tairyoku = "<img src =$img_farm/c.gif>";}		elsif($c2 > 100){$tairyoku = "<img src =$img_farm/d.gif>";}		else{$tairyoku = "<img src =$img_farm/e.gif>";}


		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$tairyoku\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "粘り</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">粘り</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@nebari){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);

		if($c3 > 1000){$cnebari = "<img src =$img_farm/ss.gif>";}
		elsif($c3 > 800){$cnebari = "<img src =$img_farm/s.gif>";}
		elsif($c3 > 600){$cnebari = "<img src =$img_farm/a.gif>";}
		elsif($c3 > 400){$cnebari = "<img src =$img_farm/b.gif>";}
		elsif($c3 > 200){$cnebari = "<img src =$img_farm/c.gif>";}
		elsif($c3 > 100){$cnebari = "<img src =$img_farm/d.gif>";}
		else{$cnebari = "<img src =$img_farm/e.gif>";}


		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cnebari\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "落ち着き</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">落ち着き</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@otituki){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);

		if($c4 > 1000){$cotituki = "<img src =$img_farm/ss.gif>";}
		elsif($c4 > 800){$cotituki = "<img src =$img_farm/s.gif>";}
		elsif($c4 > 600){$cotituki = "<img src =$img_farm/a.gif>";}
		elsif($c4 > 400){$cotituki = "<img src =$img_farm/b.gif>";}
		elsif($c4 > 200){$cotituki = "<img src =$img_farm/c.gif>";}
		elsif($c4 > 100){$cotituki = "<img src =$img_farm/d.gif>";}
		else{$cotituki = "<img src =$img_farm/e.gif>";}


		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cotituki\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "闘争心</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">闘争心</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@tousou){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);
		if($c5 > 1000){$ctousou = "<img src =$img_farm/ss.gif>";}
		elsif($c5 > 800){$ctousou = "<img src =$img_farm/s.gif>";}
		elsif($c5 > 600){$ctousou = "<img src =$img_farm/a.gif>";}
		elsif($c5 > 400){$ctousou = "<img src =$img_farm/b.gif>";}
		elsif($c5 > 200){$ctousou = "<img src =$img_farm/c.gif>";}
		elsif($c5 > 100){$ctousou = "<img src =$img_farm/d.gif>";}
		else{$ctousou = "<img src =$img_farm/e.gif>";}


		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$ctousou\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";



	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "賢さ</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">賢さ</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@tiryoku){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);

		if($c6 > 1000){$ctiryoku = "<img src =$img_farm/ss.gif>";}
		elsif($c6 > 800){$ctiryoku = "<img src =$img_farm/s.gif>";}
		elsif($c6 > 600){$ctiryoku = "<img src =$img_farm/a.gif>";}
		elsif($c6 > 400){$ctiryoku = "<img src =$img_farm/b.gif>";}
		elsif($c6 > 200){$ctiryoku = "<img src =$img_farm/c.gif>";}
		elsif($c6 > 100){$ctiryoku = "<img src =$img_farm/d.gif>";}
		else{$ctiryoku = "<img src =$img_farm/e.gif>";}

		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$ctiryoku\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "反射神経</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">反射神経</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@kire){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);

		if($c7 > 1000){$ckire = "<img src =$img_farm/ss.gif>";}
		elsif($c7 > 800){$ckire = "<img src =$img_farm/s.gif>";}
		elsif($c7 > 600){$ckire = "<img src =$img_farm/a.gif>";}
		elsif($c7 > 400){$ckire = "<img src =$img_farm/b.gif>";}
		elsif($c7 > 200){$ckire = "<img src =$img_farm/c.gif>";}
		elsif($c7 > 100){$ckire = "<img src =$img_farm/d.gif>";}
		else{$ckire = "<img src =$img_farm/e.gif>";}

		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$ckire\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "<TABLE BORDER=1>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b2\" COLSPAN=\"5\">\n";
	print "獲得賞金</TD></TR>\n";
	print "<TR><TD ALIGN=\"center\" CLASS=\"b1\"></TD><TD ALIGN=\"center\" CLASS=\"b1\">なまえ</TD><TD ALIGN=\"center\" CLASS=\"b1\">獲得賞金</TD><TD ALIGN=\"center\" CLASS=\"b1\">ブリーダー</TD>\n";

	$i=1;
	foreach(@lyen){
		($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$cmax7,$clife,$ctrain,$crun,$cwin,$cmax,$c1,$c2,$c3,$c4,$c5,$c6,$c7,$cgold,$cfather,$cfblood,$cmother,$cmblood)=split(/<>/);
		$gold = $cgold*100;
		print "<TR><TD  ALIGN=\"center\">\n";
		print "<B>$i</B></TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cname\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$gold\n";
		print "</TD>\n";
		print "<TD  ALIGN=\"center\">\n";
		print "$cbreader\n";
		print "</TD>\n";
		print "</TR>\n";
		$i++;
		if($i >10){last;}
	}
	print "</TABLE>\n";

	print "</center><P><HR SIZE=0>\n";
	print "| <A HREF=\"$scripto\">戻る</A> |\n";

	&choco_footer;

	exit;
}

#----------------#
#  制覇Ｇ１画面  #
#----------------#
sub rank {

&header;

       print <<"EOM";
一番最近にＧⅠに勝利したチョコボ順です。
<hr size=0>
<table width = 100%>
<tr>
<td class=\"b2\" align=\"center\">チョコボ名</td>
<td class=\"b2\" align=\"center\">父</td>
<td class=\"b2\" align=\"center\">母</td>
<td class=\"b2\" align=\"center\">ブリーダー</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボダ｜ビ｜</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボスタリオン</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>レジェンドカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>ＣＣＢ賞</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボ桜花賞</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボ皐月賞</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボ記念</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>チョコボステ｜クス</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>キングスカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = red>クイ｜ンカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>シルバ｜カップ</font>
</td><td class=\"b2\" align=\"center\" width="5">
<font color = blue>Ｋイク＆Ｑエリリン</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>チョコリスダ｜ビ｜</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>チョコボワ｜ルドカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>チョコボエンプレス杯</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>チョコボウル</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>ブリ｜ダ｜ズカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>ゴ｜ルドカップ</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>プラチナカップ</font></td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>チョコボオ｜クス</font>
</td>
<td class=\"b2\" align=\"center\" width="5">
<font color = blue>チョコボキングス</font>
</td>
</tr>
EOM


	open(IN,"./rireki.cgi");
	@rireki = <IN>;
	close(IN);

$hit=0;
	foreach(@rireki){
			($rid,$rpass,$rname,$rfather,$rmother,$rire[1],$rire[2],$rire[3],$rire[4],$rire[5],$rire[6],$rire[7],$rire[8],$rire[9],$rire[10],$rire[11],$rire[12],$rire[13],$rire[14],$rire[15],$rire[16],$rire[17],$rire[18],$rire[19],$rire[20],$rire[21],$rire[22],$rbreader) = split(/<>/);

print"<tr><td align=center class=b2>$rname</td><td align=center>$rfather</td><td align=center>$rmother</td><td align=center>$rbreader</td>";
if($rire[1]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[2]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[3]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[4]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[5]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[6]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[7]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[8]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[9]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[10]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[11]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[12]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[13]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[14]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[15]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[16]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[17]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[18]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[19]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[20]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[21]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
if($rire[22]){print"<td  align=\"center\">○</td>";}
else{print"<td  align=\"center\">－</td>";}
print"</tr>";
}
	print"</table>";

	&choco_footer;

	exit;
}
