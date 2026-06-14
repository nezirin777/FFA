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

# 牧場用ライブラリの読み込み
require 'choco-farm.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

# このファイル用設定
$backgif = $farm_back;
$midi = $farm_midi;
$style_sheet = $chococss;

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;

$backform = << "EOM";
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$in{'id'}">
<input type="hidden" name=mydata value="$in{'mydata'}">
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場に戻る">
</form>
EOM

if($mode) { &$mode; }
&choco;
exit;

#------------#
# 森の入り口 #
#------------#
sub choco {

	&chara_load;

	&chara_check;

	&farm_choco_read;

	if ($cwin == 0) { $cls = "新羽"; }
	elsif ($cwin < 5) { $cls = "５００万下"; }
	elsif ($cwin < 15) { $cls = "９００万下"; }
	elsif ($cwin < 30) { $cls = "１６００万下"; }
	elsif ($cwin < 50) { $cls = "オープン"; }
	elsif ($cwin < 75) { $cls = "グレードⅢ"; }
	elsif ($cwin < 105) { $cls = "グレードⅡ"; }
	elsif ($cwin < 140) { $cls = "グレードⅠ"; }
	elsif ($cwin >= 140) { $cls = "伝説級"; }

	@type = ('逃げ','先行','普通','差し','追込','自在');
	$waza = $type[$ctype];

	@status = ('動けない','疲労困憊','疲れ気味','普通','元気');

	if ($clife >= 990) {
		$csta = "元気いっぱい";
	} else {
		$life_t = int($clife / 200);
		$csta = $status[$life_t];
	}

	$money = $cgold*100;

	if (!(-e "./chocolog/$chara[0].cgi")) {
		$moricom = <<"EOM";
<font color = black size = 3>
<b>ここはチョコボの森。ここではあなたの育てるサラブレッドチョコボの親を探して見つけることができるクポ。探すクポ？</b></font>
<br>
<form action= ./morifarm.cgi  method= post >
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type="hidden" name="mode" value="choco_shop">
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="チョコボを探す">
</form>
EOM
	} else {
		$moricom = <<"EOM";
<font color = black size = 3>
<b>ここはチョコボの森。あなたのチョコボをここで引退させることができるクポ。ここで野に放つことも、そのまま繁殖用としてここにいるチョコボと配合させることもできるクポ。どうするクポ？</b></font>
<br>
<table><tr>
<td align=center class=b2 rowspan=4 colspan=2>
<img src=$img_farm/$choco_img[$cno]>
</td>
<td class=b1 id=td2>なまえ</td>
<td class=b2>$cname</td>
<td class=b1 id=td2>試合数</td>
<td class=b2>$crun</td>
<td class=b1 id=td2>勝利数</td>
<td class=b2>$cwin勝</td>
</tr>
<tr>
<td class=b1 id=td2>脚質</td>
<td class=b2>$waza</td>
<td class= b1 id= td2 >クラス</td>
<td class= b2 >$cls</td>
<td class= b1 id= td2 >練習数</td>
<td class= b2 >$ctrain</td>
</tr>
<tr>
<td class= b1 id= td2 colspan=2 align= center >じょうたい</td>
<td class= b2  colspan=4 align= center >$csta</td>
</tr>
<tr>
<td class= b1 id= td2 colspan=2 align= center >獲得本賞金</td>
<td class= b2  colspan=4 align= center >$moneyギルを獲得</td>
</tr>
</table>
<br>
<form action= ./morifarm.cgi  method= post >
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="hidden" name="mode" value="choco_sell">
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value= チョコボを野に放つ >
</form>
<br>
<form action= ./morifarm.cgi  method= post >
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_shopb>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value= 配合する >
</form>
EOM

		if (!($cname) || ($cname eq "ここに名前を入力")) {
			$naduke = <<"EOM";
<font size = 5><b>名前を付け忘れられてるクポ！！！名付けてあげるクポ！</b></font><br><form action="./morifarm.cgi" method="post">
<td class="b2"><input type=text name=st_name value=""></td>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_name>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="これでよし">
</form>
EOM
		}
	}

	&header;

	print <<"EOM";
<h1><font color =red>チョコボの森</font></h1>
<hr size=0>
<br>
<img src="$img_farm/mog.gif">
$moricom
<hr size=1>
$naduke
EOM

	&mori_footer;

	exit;
}

#-------------------#
#  チョコボ探しＢ　 #
#-------------------#
sub choco_shopb {

	&chara_load;

	&chara_check;

	&farm_choco_read;

	if (!($cname) || ($cname eq "ここに名前を入力")) {
		&error('親となるチョコボに名前がついていないか、存在しません！');
	}
	$money = $cgold*100;

	$n=0;
	if($csex){
		open(IN,"./chocoboms.cgi");
		@choco_array = <IN>;
		close(IN);
		$seibetu = "<b>♂</b>";
		$aite = "<b>♀</b>";
	} else {
		open(IN,"./chocoboos.cgi");
		@choco_array = <IN>;
		close(IN);
		$seibetu = "<b>♀</b>";
		$aite = "<b>♂</b>";
	}

	foreach(@choco_array){
		($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/);
		if($cy_breader eq "$chara[4]"){
			if(!$mada){
				$mychoco=$n;
				$mada=1;
			}
		}
		$n = $n+1;
	}

	&header;

	print <<"EOM";
<h1><font color=red>繁殖用チョコボ発見</font></h1>
<hr size=0>
<br>
<FONT SIZE=3>
<B>$km_name</B><BR>
<img src="$img_farm/mog.gif">「これだけつかまえてきたクポ♪どのチョコボと配合させるクポ？」
</FONT><BR><BR>
<table border=0>
<tr><font size = 4 color = blue><b>あなたのチョコボ</b></font>
</tr>
<tr>
<th>ブリーダー</th><th></th><th>性別</th><th>なまえ</th><th>獲得賞金額</th><th>戦績</th><th>練習量</th><th>タイプ</th><th>父</th><th>父血統</th><th>母</th><th>母血統</th></tr>
<tr>
EOM

		@img_rank = ("<img src = $img_farm/g.gif>","<img src =$img_farm/e.gif>","<img src =$img_farm/d.gif>","<img src =$img_farm/c.gif>","<img src =$img_farm/b.gif>","<img src =$img_farm/a.gif>","<img src =$img_farm/s.gif>","<img src =$img_farm/ss.gif>");
		@type = ('逃げ','先行','普通','差し','追込','自在');

		$waza = "<font color = #33cc66><b>$type[$ctype]</b></font>";
		$cfkettou = $img_rank[$cfblood];
		$cmkettou = $img_rank[$cmblood];

		print "<tr><td align=right  class=\"b2\">$chara[4]</td><td class=\"b2\"><img src=\"$img_farm/$choco_img[$cno]\"></td><td align=center  class=\"b2\">$seibetu</td><td  class=\"b2\">$cname</td><td align=right class=\"b2\">$money</td><td class=\"b2\">$crun戦$cwin勝</td><td align=right class=\"b2\">$ctrain</td><td class=\"b2\" align = center>$waza</td><td class=\"b2\">$cfather</td><td class=\"b2\">$cfkettou</td><td class=\"b2\">$cmother</td><td class=\"b2\">$cmkettou</td></tr>\n";

	print <<"EOM";
</tr>
</table>
<table border=0>
<tr><font size =4 color = pink><b>見つけたチョコボ
</b></font></tr>
<tr>
<th>選択</th><th>ブリーダー</th><th></th><th>性別</th><th>なまえ</th><th>獲得賞金額</th><th>戦績</th><th>血統</th><th>タイプ</th><th>父</th><th>父血統</th><th>母</th><th>母血統</th></tr>
<tr><form action="./morifarm.cgi" method="post">
EOM
		$hakken = int(rand(5)) + 1;

		for($i=1;$i<=$hakken;$i++){
			$des=int(rand($n));
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/,$choco_array[$des]);
			$waza = "<font color = #33cc66><b>$type[$ctype]</b></font>";
			$cy_kettou = $img_rank[$cy_blood];
			$cy_kettouf = $img_rank[$cy_fatherrank];
			$cy_kettoum = $img_rank[$cy_motherrank];
			$waza = "<font color = #33cc66><b>$type[$cy_waza]</b></font>";
			print "<tr><td  class=\"b2\"><input type=radio name=item_no value=\"$cy_no\"></td><td align=right  class=\"b2\">$cy_breader</td><td class=\"b2\" align = center><img src=\"$img_farm/$choco_img[$cy_e]\"></td><td  class=\"b2\" align = center>$aite</td><td  class=\"b2\" align = center>$cy_name</td><td align=right  class=\"b2\" align = center>$cy_plice</td><td class=\"b2\" align = center>$cy_run戦$cy_win勝</td><td class=\"b2\" align = center>$cy_kettou</td><td class=\"b2\" align = center>$waza</td><td class=\"b2\" align = center>$cy_father</td><td class=\"b2\" align = center>$cy_kettouf</td><td class=\"b2\" align = center>$cy_mother</td><td class=\"b2\" align = center>$cy_kettoum</td></tr>\n";
		}

		if(int(rand(4))==0 && $mada){
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/,$choco_array[$mychoco]);
			$cy_kettou = $img_rank[$cy_blood];
			$cy_kettouf = $img_rank[$cy_fatherrank];
			$cy_kettoum = $img_rank[$cy_motherrank];
			$waza = "<font color = #33cc66><b>$type[$cy_waza]</b></font>";
			print "<tr><td colspan=13><b>$cy_nameが$chara[4]の姿を見て、喜んで出てきたクポ！</b></td></tr><tr><td  class=\"b2\"><input type=radio name=item_no value=\"$cy_no\"></td><td align=right  class=\"b2\">$cy_breader</td><td class=\"b2\" align = center><img src=\"$img_farm/$choco_img[$cy_e]\"></td><td  class=\"b2\" align = center>$aite</td><td  class=\"b2\" align = center>$cy_name</td><td align=right  class=\"b2\" align = center>$cy_plice</td><td class=\"b2\" align = center>$cy_run戦$cy_win勝</td><td class=\"b2\" align = center>$cy_kettou</td><td class=\"b2\" align = center>$waza</td><td class=\"b2\" align = center>$cy_father</td><td class=\"b2\" align = center>$cy_kettouf</td><td class=\"b2\" align = center>$cy_mother</td><td class=\"b2\" align = center>$cy_kettoum</td></tr>\n";
		}
		print <<"EOM";
</tr>
</table>
<br>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_buyb>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="配合させる">
</form>
<form action= ./morifarm.cgi  method= post >
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_shopb>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="探しなおす">
</form>
EOM

	&mori_footer;

	exit;
}

#-------------------#
#  チョコボ探しＡ　 #
#-------------------#
sub choco_shop {

	&chara_load;

	&chara_check;

	$n=0;
	open(IN,"./chocobofile.cgi");
	@choco_array = <IN>;
	close(IN);

	&header;

	print <<"EOM";
<h1><font color=red>繁殖用チョコボ発見</font></h1>
<hr size=0>
<br>
<FONT SIZE=3>
<B>$km_name<BR>
<img src="$img_farm/mog.gif">「これだけつかまえてきたクポ♪どのチョコボを捕まえるクポ？」
</FONT></b><BR><BR>
<table border=0>
<tr><font size =4 color = pink><b>見つけたチョコボ♀
</b></font></tr>
<tr>
<th>選択</th><th>ブリーダー</th><th></th><th>なまえ</th><th>獲得賞金額</th><th>戦績</th><th>血統</th><th>タイプ</th><th>父</th><th>父血統</th><th>母</th><th>母血統</th></tr>
<tr><form action="./morifarm.cgi" method="post">
EOM

		$hakken = int(rand(5)) + 1;
		@img_rank = ("<img src = $img_farm/g.gif>","<img src =$img_farm/e.gif>","<img src =$img_farm/d.gif>","<img src =$img_farm/c.gif>","<img src =$img_farm/b.gif>","<img src =$img_farm/a.gif>","<img src =$img_farm/s.gif>","<img src =$img_farm/ss.gif>");
		@type = ('逃げ','先行','普通','差し','追込','自在');

		for($i=1;$i<=$hakken;$i++){
			$des=int(rand(35));
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/,$choco_array[$des]);
			$cy_kettou = $img_rank[$cy_blood];
			$cy_kettouf = $img_rank[$cy_fatherrank];
			$cy_kettoum = $img_rank[$cy_motherrank];
			$waza = "<font color = #33cc66><b>$type[$cy_waza]</b></font>";
			print "<tr><td  class=\"b2\"><input type=radio name=item_no value=\"$cy_no\"></td><td align=right  class=\"b2\">$cy_breader</td><td class=\"b2\" align = center><img src=\"$img_farm/$choco_img[$cy_e]\"></td><td  class=\"b2\" align = center>$cy_name</td><td align=right  class=\"b2\" align = center>$cy_plice</td><td class=\"b2\" align = center>$cy_run戦$cy_win勝</td><td class=\"b2\" align = center>$cy_kettou</td><td class=\"b2\" align = center>$waza</td><td class=\"b2\" align = center>$cy_father</td><td class=\"b2\" align = center>$cy_kettouf</td><td class=\"b2\" align = center>$cy_mother</td><td class=\"b2\" align = center>$cy_kettoum</td></tr>\n";
		}

	print <<"EOM";
</tr>
</table>
<br>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_buy>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="捕まえる">
</form>
<form action= ./morifarm.cgi  method= post >
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type="hidden" name="mode" value="choco_shop">
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value="探しなおす">
</form>
EOM

	&mori_footer;

	exit;
}

#------------------#
#  チョコボを配合  #
#------------------#
sub choco_buy {

	&chara_load;

	&chara_check;

	open(IN,"./chocobofile.cgi");
	@choco_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@choco_array){
	($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/);
		if($in{'item_no'} eq "$cy_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなチョコボは存在しません"); }

	&get_host;

	@choco_new=();

	@choco_new = "$chara[0]<>$chara[1]<>$chara[4]<>$cy_name<>0<>$cy_blood<>$cy_e<>70<>$cy_waza<>10<>10<>10<>10<>10<>10<>10<>100<>0<>0<>0<>10<>10<>10<>10<>10<>10<>10<>10<>0<>$cy_mother<>$cy_motherrank<>$cy_father<>$cy_fatherrank<>";

	open(OUT,">./chocolog/$in{'id'}.cgi");
	print OUT @choco_new;
	close(OUT);

	&header;

	print <<"EOM";
<h1>繁殖用に$cy_nameを捕まえたクポ！</h1><br>
さっそく子供を産ませるクポ！
<form action= ./morifarm.cgi  method= post >
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_shopb>
<input type=submit style="background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF" value= 配合する >
</form>
EOM

	&mori_footer;

	exit;
}

#------------------#
# チョコボを配合Ｂ #
#------------------#
sub choco_buyb {

	&chara_load;

	&chara_check;

	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&lock($lock_file,'CHC');

	open(IN,"./chocolog/$chara[0].cgi");
	@choco_chara = <IN>;
	close(IN);

	($cfid,$cfpass,$cfbreader,$cfname,$cfsex,$cfblood,$cfno,$cfmaxmax,$cftype,$cfmax1,$cfmax2,$cfmax3,$cfmax4,$cfmax5,$cfmax6,$cfmax7,$cflife,$cftrain,$cfrun,$cfwin,$cfmax,$cf1,$cf2,$cf3,$cf4,$cf5,$cf6,$cf7,$cfgold,$cffather,$cffblood,$cfmother,$cfmblood) = split(/<>/,$choco_chara[0]);

	if (!$cfname) { &error('親チョコボが見つかりません。'); }

	if($cfsex){
		open(IN,"./chocoboms.cgi");
		@choco_array = <IN>;
		close(IN);

		$hit=0;
		foreach(@choco_array){
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/);
			if($in{'item_no'} eq "$cy_no") { $hit=1;last; }
		}

		$cfather = $cfname;
		$cmother = $cy_name;
	} else {
		open(IN,"./chocoboos.cgi");
		@choco_array = <IN>;
		close(IN);
		$hit=0;
		foreach(@choco_array){
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/);
			if($in{'item_no'} eq "$cy_no") { $hit=1;last; }
			$cfather = $cy_name;
			$cmother = $cfname;
		}
	}

	if(!$hit) { &error("そんなチョコボは存在しません"); }

	&get_host;

	#計算式
	if (!$cfblood) { $cfblood = int(rand(10)); $cfranhit=1; }
	if (!$cy_blood) { $cy_blood = int(rand(10)); $cmranhit=1; }
	$birth = int(rand($cfblood + $cy_blood));
	if ($cfranhit) { $cfblood = 0; }
	if ($cmranhit) { $cy_blood = 0; }
	if($cfwin > 50){ $birth += 1; }
	if($cftrain > 1000){ $birth += 1; }
	$prebirth = int(rand($cy_fatherrank + $cy_motherrank) + rand($cffblood + $cfmblood));
	if($cfwin > 100){ $prebirth += 2; }
	if($cftrain > 500){ $prebirth += 1; }

	if($birth >= 14){
		if($prebirth >= 1){$cblood = 7;}
		else{$cblood = 0;}
	}
	elsif($birth == 13){
		if($prebirth >= 3){$cblood = 7;}
		elsif($prebirth >= 1){$cblood = 6;}
		else{$cblood = 0;}
	}
	elsif($birth >= 12){
		if($prebirth >= 7){$cblood = 7;}
		elsif($prebirth >= 5){$cblood = 6;}
		elsif($prebirth >= 3){$cblood = 5;}
		elsif($prebirth >= 1){$cblood = 4;}
		else{$cblood = 0;}
	}
	elsif($birth >= 11){
		if($prebirth >= 9){$cblood = 7;}
		elsif($prebirth >= 7){$cblood = 6;}
		elsif($prebirth >= 5){$cblood = 5;}
		elsif($prebirth >= 3){$cblood = 4;}
		elsif($prebirth >= 1){$cblood = 3;}
		else{$cblood = 0;}
	}
	elsif($birth >= 10){
		if($prebirth >= 11){$cblood = 7;}
		elsif($prebirth >= 9){$cblood = 6;}
		elsif($prebirth >= 7){$cblood = 5;}
		elsif($prebirth >= 5){$cblood = 4;}
		elsif($prebirth >= 3){$cblood = 3;}
		elsif($prebirth >= 1){$cblood = 2;}
		else{$cblood = 0;}
	}
	elsif($birth >= 9){
		if($prebirth >= 13){$cblood = 7;}
		elsif($prebirth >= 11){$cblood = 6;}
		elsif($prebirth >= 9){$cblood = 5;}
		elsif($prebirth >= 7){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 8){
		if($prebirth >= 15){$cblood = 7;}
		elsif($prebirth >= 12){$cblood = 6;}
		elsif($prebirth >= 10){$cblood = 5;}
		elsif($prebirth >= 8){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 7){
		if($prebirth >= 17){$cblood = 7;}
		elsif($prebirth >= 13){$cblood = 6;}
		elsif($prebirth >= 11){$cblood = 5;}
		elsif($prebirth >= 9){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 6){
		if($prebirth >= 19){$cblood = 7;}
		elsif($prebirth >= 15){$cblood = 6;}
		elsif($prebirth >= 12){$cblood = 5;}
		elsif($prebirth >= 9){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 5){
		if($prebirth >= 21){$cblood = 7;}
		elsif($prebirth >= 17){$cblood = 6;}
		elsif($prebirth >= 13){$cblood = 5;}
		elsif($prebirth >= 9){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 4){
		if($prebirth >= 23){$cblood = 7;}
		elsif($prebirth >= 19){$cblood = 6;}
		elsif($prebirth >= 15){$cblood = 5;}
		elsif($prebirth >= 9){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 3){
		if($prebirth >= 25){$cblood = 7;}
		elsif($prebirth >= 21){$cblood = 6;}
		elsif($prebirth >= 15){$cblood = 5;}
		elsif($prebirth >= 13){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 2){
		if($prebirth >= 27){$cblood = 7;}
		elsif($prebirth >= 23){$cblood = 6;}
		elsif($prebirth >= 19){$cblood = 5;}
		elsif($prebirth >= 14){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	elsif($birth >= 1){
		if($prebirth >= 28){$cblood = 7;}
		elsif($prebirth >= 25){$cblood = 6;}
		elsif($prebirth >= 21){$cblood = 5;}
		elsif($prebirth >= 15){$cblood = 4;}
		elsif($prebirth >= 5){$cblood = 3;}
		elsif($prebirth >= 3){$cblood = 2;}
		elsif($prebirth >= 1){$cblood = 1;}
		else{$cblood = 0;}
	}
	else{
		if($prebirth == 28){$cblood = 7;}
		elsif($prebirth >= 27){$cblood = 6;}
		elsif($prebirth >= 25){$cblood = 5;}
		elsif($prebirth >= 21){$cblood = 4;}
		elsif($prebirth >= 11){$cblood = 3;}
		elsif($prebirth >= 7){$cblood = 2;}
		elsif($prebirth >= 3){$cblood = 1;}
		else{$cblood = 0;}
	}


	if($cblood == 7){$cmaxmax = 5500 + int(rand(1500));}
	elsif($cblood == 6){$cmaxmax = 5500 + int(rand(1000));}
	elsif($cblood == 5){$cmaxmax = 4500 + int(rand(2000));}
	elsif($cblood == 4){$cmaxmax = 3500 + int(rand(2500));}
	elsif($cblood == 3){$cmaxmax = 3000 + int(rand(3000));}
	elsif($cblood == 2){$cmaxmax = 2500 + int(rand(3000));}
	elsif($cblood == 1){$cmaxmax = 2000 + int(rand(3500));}
	else{$cmaxmax = int(rand(7000));}

	$csex = int(rand(1.9));
	if($csex){$seibetu = "たくましそうな男の子";}
	else{$seibetu = "かわいらしい女の子";}

	if(int(rand(19)) == 1){
		$cno = int(rand(7.999));$ctype = int(rand(5.1));$koukei="曽祖父似";
	} elsif (int(rand(2)) == 1) {
		$cno = $cy_e;
		$ctype = $cy_waza;
		if($cfsex){ $koukei="母親似"; }
		else{ $koukei="父親似"; }
	} else {
		$cno = $cfno;
		$ctype = $cftype;
		if($cfsex){ $koukei="父親似"; }
		else{ $koukei="母親似"; }
	}

	if($ctype == 0){
		$cmax1 = 950 + int(rand(100));
		$cmax2 = 750 + int(rand(100));
		$cmax3 = 950 + int(rand(100));
		$cmax4 = 650 + int(rand(100));
		$cmax5 = 550 + int(rand(100));
		$cmax6 = 850 + int(rand(100));
		$cmax7 = 550 + int(rand(100));
		$c1 = 20 + int(rand(48) * ($cblood + 1));
		$c2 = 20 + int(rand(38) * ($cblood + 1));
		$c3 = 20 + int(rand(48) * ($cblood + 1));
		$c4 = 20 + int(rand(33) * ($cblood + 1));
		$c5 = 20 + int(rand(28) * ($cblood + 1));
		$c6 = 20 + int(rand(43) * ($cblood + 1));
		$c7 = 20 + int(rand(28) * ($cblood + 1));
		$cmax=int(($c1+$c2+$c3+$c4+$c5+$c6+$c7)*(1+rand(2)));
		if($cmax > $cmaxmax){
			$cmax = $cmaxmax;
			if($c1+$c2+$c3+$c4+$c5+$c6+$c7 > $cmaxmax){
				$wariai=$cmaxmax/($c1+$c2+$c3+$c4+$c5+$c6+$c7);
				$c1=int($c1*$wariai)+1;
				$c2=int($c2*$wariai)+1;
				$c3=int($c3*$wariai)+1;
				$c4=int($c4*$wariai)+1;
				$c5=int($c5*$wariai)+1;
				$c6=int($c6*$wariai)+1;
				$c7=int($c7*$wariai)+1;
			}
		}
	} elsif($ctype == 1) {
		$cmax1 = 850 + int(rand(100));
		$cmax2 = 750 + int(rand(100));
		$cmax3 = 850 + int(rand(100));
		$cmax4 = 650 + int(rand(100));
		$cmax5 = 650 + int(rand(100));
		$cmax6 = 850 + int(rand(100));
		$cmax7 = 650 + int(rand(100));
		$c1 = 20 + int(rand(43) * ($cblood + 1));
		$c2 = 20 + int(rand(38) * ($cblood + 1));
		$c3 = 20 + int(rand(43) * ($cblood + 1));
		$c4 = 20 + int(rand(38) * ($cblood + 1));
		$c5 = 20 + int(rand(33) * ($cblood + 1));
		$c6 = 20 + int(rand(38) * ($cblood + 1));
		$c7 = 20 + int(rand(33) * ($cblood + 1));
		$cmax=int(($c1+$c2+$c3+$c4+$c5+$c6+$c7)*(1+rand(2)));
		if($cmax > $cmaxmax){
			$cmax = $cmaxmax;
			if($c1+$c2+$c3+$c4+$c5+$c6+$c7 > $cmaxmax){
				$wariai=$cmaxmax/($c1+$c2+$c3+$c4+$c5+$c6+$c7);
				$c1=int($c1*$wariai)+1;
				$c2=int($c2*$wariai)+1;
				$c3=int($c3*$wariai)+1;
				$c4=int($c4*$wariai)+1;
				$c5=int($c5*$wariai)+1;
				$c6=int($c6*$wariai)+1;
				$c7=int($c7*$wariai)+1;
			}
		}
	} elsif($ctype == 2) {
		$cmax1 = 750 + int(rand(100));
		$cmax2 = 750 + int(rand(100));
		$cmax3 = 750 + int(rand(100));
		$cmax4 = 750 + int(rand(100));
		$cmax5 = 750 + int(rand(100));
		$cmax6 = 750 + int(rand(100));
		$cmax7 = 750 + int(rand(100));
		$c1 = 20 + int(rand(38) * ($cblood + 1));
		$c2 = 20 + int(rand(38) * ($cblood + 1));
		$c3 = 20 + int(rand(38) * ($cblood + 1));
		$c4 = 20 + int(rand(38) * ($cblood + 1));
		$c5 = 20 + int(rand(38) * ($cblood + 1));
		$c6 = 20 + int(rand(38) * ($cblood + 1));
		$c7 = 20 + int(rand(38) * ($cblood + 1));
		$cmax=int(($c1+$c2+$c3+$c4+$c5+$c6+$c7)*(1+rand(2)));
		if($cmax > $cmaxmax){
			$cmax = $cmaxmax;
			if($c1+$c2+$c3+$c4+$c5+$c6+$c7 > $cmaxmax){
				$wariai=$cmaxmax/($c1+$c2+$c3+$c4+$c5+$c6+$c7);
				$c1=int($c1*$wariai)+1;
				$c2=int($c2*$wariai)+1;
				$c3=int($c3*$wariai)+1;
				$c4=int($c4*$wariai)+1;
				$c5=int($c5*$wariai)+1;
				$c6=int($c6*$wariai)+1;
				$c7=int($c7*$wariai)+1;
			}
		}
	} elsif($ctype == 3) {
		$cmax1 = 650 + int(rand(100));
		$cmax2 = 650 + int(rand(100));
		$cmax3 = 750 + int(rand(100));
		$cmax4 = 850 + int(rand(100));
		$cmax5 = 850 + int(rand(100));
		$cmax6 = 650 + int(rand(100));
		$cmax7 = 850 + int(rand(100));
		$c1 = 20 + int(rand(33) * ($cblood + 1));
		$c2 = 20 + int(rand(33) * ($cblood + 1));
		$c3 = 20 + int(rand(38) * ($cblood + 1));
		$c4 = 20 + int(rand(38) * ($cblood + 1));
		$c5 = 20 + int(rand(43) * ($cblood + 1));
		$c6 = 20 + int(rand(38) * ($cblood + 1));
		$c7 = 20 + int(rand(43) * ($cblood + 1));
		$cmax=int(($c1+$c2+$c3+$c4+$c5+$c6+$c7)*(1+rand(2)));
		if($cmax > $cmaxmax){
			$cmax = $cmaxmax;
			if($c1+$c2+$c3+$c4+$c5+$c6+$c7 > $cmaxmax){
				$wariai=$cmaxmax/($c1+$c2+$c3+$c4+$c5+$c6+$c7);
				$c1=int($c1*$wariai)+1;
				$c2=int($c2*$wariai)+1;
				$c3=int($c3*$wariai)+1;
				$c4=int($c4*$wariai)+1;
				$c5=int($c5*$wariai)+1;
				$c6=int($c6*$wariai)+1;
				$c7=int($c7*$wariai)+1;
			}
		}
	} elsif($ctype == 4) {
		$cmax1 = 550 + int(rand(100));
		$cmax2 = 650 + int(rand(100));
		$cmax3 = 650 + int(rand(100));
		$cmax4 = 950 + int(rand(100));
		$cmax5 = 850 + int(rand(100));
		$cmax6 = 650 + int(rand(100));
		$cmax7 = 950 + int(rand(100));
		$c1 = 20 + int(rand(28) * ($cblood + 1));
		$c2 = 20 + int(rand(33) * ($cblood + 1));
		$c3 = 20 + int(rand(33) * ($cblood + 1));
		$c4 = 20 + int(rand(38) * ($cblood + 1));
		$c5 = 20 + int(rand(43) * ($cblood + 1));
		$c6 = 20 + int(rand(43) * ($cblood + 1));
		$c7 = 20 + int(rand(48) * ($cblood + 1));
		$cmax=int(($c1+$c2+$c3+$c4+$c5+$c6+$c7)*(1+rand(2)));
		if($cmax > $cmaxmax){
			$cmax = $cmaxmax;
			if($c1+$c2+$c3+$c4+$c5+$c6+$c7 > $cmaxmax){
				$wariai=$cmaxmax/($c1+$c2+$c3+$c4+$c5+$c6+$c7);
				$c1=int($c1*$wariai)+1;
				$c2=int($c2*$wariai)+1;
				$c3=int($c3*$wariai)+1;
				$c4=int($c4*$wariai)+1;
				$c5=int($c5*$wariai)+1;
				$c6=int($c6*$wariai)+1;
				$c7=int($c7*$wariai)+1;
			}
		}
	} elsif($ctype == 5) {
		$cmax1 = 750 + int(rand(100));
		$cmax2 = 650 + int(rand(100));
		$cmax3 = 650 + int(rand(100));
		$cmax4 = 950 + int(rand(100));
		$cmax5 = 650 + int(rand(100));
		$cmax6 = 950 + int(rand(100));
		$cmax7 = 650 + int(rand(100));
		$c1 = 20 + int(rand(38) * ($cblood + 1));
		$c2 = 20 + int(rand(33) * ($cblood + 1));
		$c3 = 20 + int(rand(33) * ($cblood + 1));
		$c4 = 20 + int(rand(48) * ($cblood + 1));
		$c5 = 20 + int(rand(33) * ($cblood + 1));
		$c6 = 20 + int(rand(48) * ($cblood + 1));
		$c7 = 20 + int(rand(33) * ($cblood + 1));
		$cmax=int(($c1+$c2+$c3+$c4+$c5+$c6+$c7)*(1+rand(2)));
		if($cmax > $cmaxmax){
			$cmax = $cmaxmax;
			if($c1+$c2+$c3+$c4+$c5+$c6+$c7 > $cmaxmax){
				$wariai=$cmaxmax/($c1+$c2+$c3+$c4+$c5+$c6+$c7);
				$c1=int($c1*$wariai)+1;
				$c2=int($c2*$wariai)+1;
				$c3=int($c3*$wariai)+1;
				$c4=int($c4*$wariai)+1;
				$c5=int($c5*$wariai)+1;
				$c6=int($c6*$wariai)+1;
				$c7=int($c7*$wariai)+1;
			}
		}
	}

	$crun=0;
	$cwin=0;
	$clife=1000;
	$cgold=0;
	$ctrain=0;
	#計算式終了

	@choco_new = "$chara[0]<>$chara[1]<>$chara[4]<><>$csex<>$cblood<>$cno<>$cmaxmax<>$ctype<>$cmax1<>$cmax2<>$cmax3<>$cmax4<>$cmax5<>$cmax6<>$cmax7<>$clife<>$ctrain<>$crun<>$cwin<>$cmax<>$c1<>$c2<>$c3<>$c4<>$c5<>$c6<>$c7<>$cgold<>$cfather<>$cfblood<>$cmother<>$cy_blood<>";

	open(OUT,">./chocolog/$in{'id'}.cgi");
	print OUT @choco_new;
	close(OUT);
	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&unlock($lock_file,'CHC');

	&header;

	print <<"EOM";
<h1>$koukeiの$seibetuが産まれました♪</h1>
<table border=0>
<tr>
<th></th><th>タイプ</th><th>父</th><th>父血統</th><th>母</th><th>母血統</th></tr>
<tr>
EOM

	@type = ('逃げ','先行','普通','差し','追込','自在');
	$waza = "<font color = #33cc66><b>$type[$ctype]</b></font>";

	@img_rank = ("<img src = $img_farm/g.gif>","<img src =$img_farm/e.gif>","<img src =$img_farm/d.gif>","<img src =$img_farm/c.gif>","<img src =$img_farm/b.gif>","<img src =$img_farm/a.gif>","<img src =$img_farm/s.gif>","<img src =$img_farm/ss.gif>");

	$cfkettou = $img_rank[$cfblood];
	$cy_kettou = $img_rank[$cy_blood];

	print <<"EOM";
<tr>
<td class=\"b2\" align = center>
<img src=\"$img_farm/$choco_img[$cno]\">
</td>
<td class=\"b2\" align = center>$waza</td>
<td class=\"b2\" align = center>$cfname</td>
<td class=\"b2\" align = center>$cfkettou</td>
<td class=\"b2\" align = center>$cy_name</td>
<td class=\"b2\" align = center>$cy_kettou</td>
</tr>
</tr>
</table>
さっそく名前をつけてあげましょう♪
<form action="./morifarm.cgi" method="post">
<td class="b2"><input type=text name=st_name value="ここに名前を入力"></td>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=choco_name>
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="これでよし">
</form>
<hr size=0>
<br>
EOM

	&mori_footer;

	exit;
}

#--------------------#
# チョコボを野に放つ #
#--------------------#
sub choco_sell {

	&chara_load;

	&chara_check;

	open(IN,"./chocolog/$chara[0].cgi");
	@choco_chara = <IN>;
	close(IN);

	($cfid,$cfpass,$cfbreader,$cfname,$cfsex,$cfblood,$cfno,$cfmaxmax,$cftype,$cfmax1,$cfmax2,$cfmax3,$cfmax4,$cfmax5,$cfmax6,$cfmax7,$cflife,$cftrain,$cfrun,$cfwin,$cfmax,$cf1,$cf2,$cf3,$cf4,$cf5,$cf6,$cf7,$cfgold,$cffather,$cffblood,$cfmother,$cfmblood) = split(/<>/,$choco_chara[0]);

	if (!($cfname) || ($cfname eq "ここに名前を入力")) {
		&error('野に放つチョコボに名前がついていないか存在しません！');
	}

	$money = $cfgold*100;

# もし、強かったチョコボを放った際にアイテムを拾うようにするならここにアイテム取得情報を入力
# 条件入力($cftrainが練習量、$cfwinが勝利数を示します。G1を読み込みたい場合はchocofarm.cgiを参照して下さい)
#	$in{'item'} = 'item';	# アイテム種を指定。itemが武器、defが防具、acsが装飾品になります。
#	$newitem = "武器情報を入力(iniに設定する１行丸ごとを改行せずに)";
#	if ($in{'item'} eq 'item') {
#		$lock_file = "$lockfolder/sitem$in{'id'}.lock";
#		$flock_pre = 'SI';
#	} elsif ($in{'item'} eq 'def') {
#		$lock_file = "$lockfolder/sdefe$in{'id'}.lock";
#		$flock_pre = 'SD';
#	} else {
#		$lock_file = "$lockfolder/acsesa$in{'id'}.lock";
#		$flock_pre = 'SA';
#	}

#	&lock($lock_file,$flock_pre);
#	open(IN,"$souko_folder/$in{'item'}/$in{'id'}.cgi") || &error("キャラクターが見つかりません！$back_form");
#	@souko_item = <IN>;
#	close(IN);

#	$souko_item_num = @souko_item;

#	if ($souko_item_num >= $item_max) {
#		&error("武器倉庫がいっぱいです！$back_form");
#	}

#	push(@souko_item,$newitem);

#	open(OUT,">$souko_folder/$in{'item'}/$in{'id'}.cgi");
#	print OUT @souko_item;
#	close(OUT);
#	&unlock($lock_file,$flock_pre);
#
#
#
# ここまでアイテム取得情報

	if($cfsex){
		$lock_file = "$lockfolder/cos.lock";
		&lock($lock_file,COS);
		open(IN,"./chocoboos.cgi");
		@choco_array = <IN>;
		close(IN);

		# 配列1番目でソート
		@tmp = map {(split /<>/)[0]} @choco_array;
		@chocojun = @choco_array[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

		$hit=0;
		for($i=1;$i<=10;$i++){
			$warikomi=int(rand(99));
			($acy_no,$acy_name,$acy_plice,$acy_run,$acy_win,$acy_blood,$acy_waza,$acy_father,$acy_fatherrank,$acy_mother,$acy_motherrank,$acy_e,$acy_breader) = split(/<>/,$chocojun[$warikomi]);
			if($acy_win < 100 && $acy_blood < 5){$hit=1;last;}
		}

		if(!$hit){ $warikomi +=1; }

		@new=();
		foreach(@choco_array){
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/);
			if($warikomi eq "$cy_no") {
			 	unshift(@new,"$warikomi<>$cfname<>$money<>$cfrun<>$cfwin<>$cfblood<>$cftype<>$cffather<>$cffblood<>$cfmother<>$cfmblood<>$cfno<>$cfbreader<>\n");
			} else {
				push(@new,"$_");
			}
		}

		if(!$hit){
		 	unshift(@new,"$warikomi<>$cfname<>$money<>$cfrun<>$cfwin<>$cfblood<>$cftype<>$cffather<>$cffblood<>$cfmother<>$cfmblood<>$cfno<>$cfbreader<>\n");
		}

		open(OUT,">./chocoboos.cgi");
		print OUT @new;
		close(OUT);

		$lock_file = "$lockfolder/cos.lock";
		&unlock($lock_file,COS);

		$seibetu = "<b>♂</b>";

	} else {
		$lock_file = "$lockfolder/cms.lock";
		&lock($lock_file,CMS);
		open(IN,"./chocoboms.cgi");
		@choco_array = <IN>;
		close(IN);

		# 配列19番目でソート
		@tmp = map {(split /<>/)[0]} @choco_array;
		@chocojun = @choco_array[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

		$hit=0;
		for($i=1;$i<=10;$i++){
			$warikomi=int(rand(99));
			($acy_no,$acy_name,$acy_plice,$acy_run,$acy_win,$acy_blood,$acy_waza,$acy_father,$acy_fatherrank,$acy_mother,$acy_motherrank,$acy_e,$acy_breader) = split(/<>/,$chocojun[$warikomi]);
			if($acy_win < 100 && $acy_blood < 5){$hit=1;last;}
		}

		@new=();
		foreach(@choco_array){
			($cy_no,$cy_name,$cy_plice,$cy_run,$cy_win,$cy_blood,$cy_waza,$cy_father,$cy_fatherrank,$cy_mother,$cy_motherrank,$cy_e,$cy_breader) = split(/<>/);
			if($warikomi eq "$cy_no") {
		 	unshift(@new,"$warikomi<>$cfname<>$money<>$cfrun<>$cfwin<>$cfblood<>$cftype<>$cffather<>$cffblood<>$cfmother<>$cfmblood<>$cfno<>$cfbreader<>\n");
			} else {
			push(@new,"$_");
			}
		}
		if(!$hit){
		 	unshift(@new,"$warikomi<>$cfname<>$money<>$cfrun<>$cfwin<>$cfblood<>$cftype<>$cffather<>$cffblood<>$cfmother<>$cfmblood<>$cfno<>$cfbreader<>\n");
		}

		open(OUT,">./chocoboms.cgi");
		print OUT @new;
		close(OUT);
		$lock_file = "$lockfolder/cms.lock";
		&unlock($lock_file,CMS);

		$seibetu = "<b>♀</b>";

	}

	&get_host;

	if (-e "./chocolog/$chara[0].cgi") { unlink("./chocolog/$chara[0].cgi"); }

	@img_rank = ("<img src = $img_farm/g.gif>","<img src =$img_farm/e.gif>","<img src =$img_farm/d.gif>","<img src =$img_farm/c.gif>","<img src =$img_farm/b.gif>","<img src =$img_farm/a.gif>","<img src =$img_farm/s.gif>","<img src =$img_farm/ss.gif>");

	$cfkettou = $img_rank[$cfblood];
	$cfkettouf = $img_rank[$cffblood];
	$cfkettoum = $img_rank[$cfmblood];

	@type = ('逃げ','先行','普通','差し','追込','自在');
	$waza = "<font color = #33cc66><b>$type[$cftype]</b></font>";

	&header;

	print <<"EOM";
<h1>$cfnameを野に放ちました</h1>
<FONT SIZE=3>
<B>$km_name<BR>
<img src="$img_farm/mog.gif">「また、会えるといいクポね････。元気でね～♪$com」
</FONT></b>
<table border=0>
<tr>
<th>ブリーダー</th><th></th><th>性別</th><th>なまえ</th><th>獲得賞金額</th><th>戦績</th><th>血統</th><th>タイプ</th><th>父</th><th>父血統</th><th>母</th><th>母血統</th></tr>
<tr>
<td align=right  class=\"b2\">$cfbreader</td>
<td class=\"b2\" align = center>
<img src=\"$img_farm/$choco_img[$cfno]\">
</td>
<td  class=\"b2\" align = center>$seibetu</td>
<td  class=\"b2\" align = center>$cfname</td>
<td align=right  class=\"b2\" align = center>$money</td>
<td class=\"b2\" align = center>$cfrun戦$cfwin勝</td>
<td class=\"b2\" align = center>$cfkettou</td>
<td class=\"b2\" align = center>$waza</td>
<td class=\"b2\" align = center>$cffather</td>
<td class=\"b2\" align = center>$cfkettouf</td>
<td class=\"b2\" align = center>$cfmother</td>
<td class=\"b2\" align = center>$cfkettoum</td>
</tr>
</table>
<hr size=0>
<br>
EOM

	&mori_footer;

	exit;
}

#------------------#
#   　名付ける　   #
#------------------#
sub choco_name {


	open(IN,"./rireki.cgi");
	@rireki = <IN>;
	close(IN);

	foreach(@rireki){
			($rid,$rpass,$rname,$rfather,$rmother,$rire[1],$rire[2],$rire[3],$rire[4],$rire[5],$rire[6],$rire[7],$rire[8],$rire[9],$rire[10],$rire[11],$rire[12],$rire[13],$rire[14],$rire[15],$rire[16],$rire[17],$rire[18],$rire[19],$rire[20],$rire[21],$rire[22],$rbreader) = split(/<>/);
if($rname eq "$in{'st_name'}"){&error("ＧⅠウィナーに同じ名前のチョコボがいます！$backform"); }}

	&chara_load;

	&chara_check;

	if (!(-e "./chocolog/$chara[0].cgi")) { &error("名付けるチョコボがいません。"); }

	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&lock($lock_file,'CHC');
	&farm_choco_read;

	$cid = $chara[0];
	$cpass = $chara[1];
	$cbreader = $chara[4];
	$cname = $in{'st_name'};

	&farm_choco_regist;
	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&unlock($lock_file,'CHC');

	&header;

	print <<"EOM";
<h1>$in{'st_name'}は名前をすごく気に入ってくれてるみたいだよ♪</h1>
<hr size=0>
<br>
EOM

	&mori_footer;

	exit;
}

#------------#
#  体力回復  #
#------------#
sub yadoya {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	if($chara[19] < 5000) { &error("お金が足りません$backform"); }
	else { $chara[19] = $chara[19] - 5000; }

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	$in{'mydata'} = $new_chara;

	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&lock($lock_file,'CHC');
	&farm_choco_read;

	if (!(-e "./chocolog/$chara[0].cgi")) { &error("チョコボがいません。"); }
	if($clife eq 1000) { &error("チョコボはまだまだ元気です。"); }

	&get_host;

	$date = time();

	$clife = $clife + int(rand(300)) + 200;
	if($clife > 1000){$clife = 1000;$cmax += 10;}
	$ctrain = $ctrain+1;
	$cmax += 10;

	&farm_choco_regist;
	$lock_file = "$lockfolder/choco$in{'id'}.lock";
	&unlock($lock_file,'CHC');

	$backform = << "EOM";
<form action="./chocofarm.cgi" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name=mydata value="$new_chara">
<input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value="牧場に戻る">
</form>
EOM

	&header;

	print <<"EOM";
<h1>$cnameを放牧しました♪元気いっぱいになりました♪</h1>
<hr size=0>
<br>
EOM

	&mori_footer;

	exit;
}

#------------------#
#　HTMLのフッター　#
#------------------#
sub mori_footer {

	print $backform;

	&choco_footer;
}
