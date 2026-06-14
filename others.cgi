#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はT.CUMROさんにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FFA Emilia Ver1.01
#  edit by Emilia
#  http://www5d.biglobe.ne.jp/~sprite/
#  y-kamata@jcom.home.ne.jp
#------------------------------------------------------#
#
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
#------------------------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

#不正者追放プログラム
require './hostkick.pl';

# レジストライブラリの読み込み
require 'sankasya.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
if($mente) { &error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m"); }
if($link_flg){&link_chack;}
&decode;
#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}
if($mode eq 'ihtml_top') { ihtml_top; }
#機種判定
$agent = $ENV{'HTTP_USER_AGENT'};
($browser,$version,$model) = split(/\//,$agent);
if ($browser eq "DoCoMo") {&ihtml_top;}
else{&html_top;}
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
	html_top => <<'__SUB__',
#-----------------#
#  TOPページ表示  #
#-----------------#
sub html_top {

        &read_cwinner;

	&read_winner;

	&get_cookie;

	&class;

	if($wkati) { $ritu = int(($wkati / $wtotal) * 100); }
	else { $ritu = 0; }

	open(IN,"$recode_file");
	@recode = <IN>;
	close(IN);

	($rcount,$rname,$rsite,$rurl) = split(/<>/,$recode[0]);

	if($wsex) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $wlv * $lv_up;

	if($witem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($wi_no,$wi_name,$wi_dmg,$wi_gold,$wi_plus) = split(/<>/);
			if($witem eq $wi_no) { last; }
		}
	}else{ $wi_name = "－"; $i_plus=0;}

	if($wdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($wd_no,$wd_name,$wd_dmg,$wd_gold,$wd_plus) = split(/<>/);
			if($wdef eq $wd_no) { last; }
		}
	}else{ $wd_name = "－"; $d_plus=0;}

	open(IN,"$acs_file");
	@log_acs = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
		if($wacsno eq "$a_no"){ $hit=1;last; }
	}
	if(!$hit) { $a_name="-"; $a_0up=0;$a_1up=0;$a_2up=0;$a_3up=0;$a_4up=0;$a_5up=0;$a_6up=0;$a_lpup=0;$a_hitup=0;$a_kaihiup=0;$a_wazaup=0;}

	# 最大値の設定
	if($wmaxhp > $charamaxhp){$wmaxhp = $charamaxhp}
	if($wn_0 > $charamaxpm){$wn_0 = $charamaxpm;}
	if($wn_1 > $charamaxpm){$wn_1 = $charamaxpm;}
	if($wn_2 > $charamaxpm){$wn_2 = $charamaxpm;}
	if($wn_3 > $charamaxpm){$wn_3 = $charamaxpm;}
	if($wn_4 > $charamaxpm){$wn_4 = $charamaxpm;}
	if($wn_5 > $charamaxpm){$wn_5 = $charamaxpm;}
	if($wn_6 > $charamaxpm){$wn_6 = $charamaxpm;}
	if($wlp  > $charamaxpm){$wlp  = $charamaxpm;}

        if($cw_kati) { $critu = int(($cw_kati / $cw_total) * 100); }
	else { $critu = 0; }

	$cysp = int($cw_sp + $cw_5);

	if($cw_kati > 1000 && $critu > 90) {$crank = "ＳＳ";
	}elsif($cw_kati > 500 && $critu > 90){$crank = "Ｓ";
	}elsif($cw_kati > 300 && $critu > 85){$crank = "Ａ";
	}elsif($cw_kati > 200 && $critu > 80){$crank = "Ｂ";
	}elsif($cw_kati > 100 && $critu > 70){$crank = "Ｃ";
	}elsif($cw_kati > 50){$crank = "Ｄ";
	}elsif($cw_kati > 0){$crank = "Ｅ";
	}

        if($cw_money < 5000){$cls ="新羽";}
     elsif($cw_money < 10000){$cls ="見習";}
     elsif($cw_money < 50000){$cls = "OPEN";}
     elsif($cw_money < 100000){$cls = "グレードⅢ";}
     elsif($cw_money < 300000){$cls = "グレードⅡ";}
     elsif($cw_money < 1999999){$cls = "グレードⅠ";}
     elsif($cw_money > 2000000 or $cw_money = 2000000){$cls = "伝説クラス！";}
  
         if($cw_kon<50) {$kon = "根性なしTT";}
       elsif($cw_kon<100){$kon="まだまだ根性足りない";}
       elsif($cw_kon<200){$kon = "普通のチョコボ";}
       elsif($cw_kon<300 ){$kon = "なかなかの根性";}
       elsif($cw_kon<500){$kon = "すごい根性の持ち主！";}
       elsif($cw_kon>500 or $cy_kon=500){$kon = "鬼の根性！！";}
  
        if($cw_waza == 1) {$waza = "普通";
		}elsif($cw_waza== 2){$waza ="逃げ";
		}elsif($cw_waza== 0){$waza ="？？？？";
		}elsif($cw_waza== 3){$waza = "先行";
		}elsif($cw_waza== 4){$waza = "差し";
		}elsif($cw_waza== 5){$waza = "追い込み";
		}

        if($cw_life >= 99) {$csta = "満腹";
		}elsif($cw_life >= 80){$csta = "腹八分";
		}elsif($cw_life >= 60){$csta = "普通";
		}elsif($cw_life >= 40){$csta = "腹ぺこ";
		}elsif($cw_life >= 20){$csta = "飢餓";
		}elsif($cw_life >= 2){$csta = "餓死寸前";
		}

        $cw_ritu = int(($cw_kon +  $cw_sp) / 30);
         
        if($cw_ritu  <= 1) {$cw_ritu   = "1";}
        elsif($cw_ritu>40){$cw_ritu = "40";}

        open(IN,"$crecode_file");
	@recode = <IN>;
	close(IN);

	($crcount,$crname) = split(/<>/,$recode[0]);

        $cw_money=($cw_money*100);

	# 基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int(($wn_4 / 10)+51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($wn_5 / 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($wlp / 15)) + 10 + $wcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}

	# 能力値バーの詳しい幅設定
	$bw0     = int(1 * ($wn_0 / $divpm));
	$bw1     = int(1 * ($wn_1 / $divpm));
	$bw2     = int(1 * ($wn_2 / $divpm));
	$bw3     = int(1 * ($wn_3 / $divpm));
	$bw4     = int(1 * ($wn_4 / $divpm));
	$bw5     = int(1 * ($wn_5 / $divpm));
	$bw6     = int(1 * ($wn_6 / $divpm));
	$bwlp    = int(1 * ($wlp / $divpm));
	$wi_plus += $a_hitup;
	$wd_plus += $a_kaihiup;
	$bwhit   = int(0.5 * ($hit_ritu + $wi_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $wd_plus));
	$bwwaza  = int(1 * ($waza_ritu + $a_wazaup));
	if($bwhit > 100){$bwhit = 100;}
	if($bwkaihi > 100){$bwkaihi = 100;}
	if($bwwaza > 100){$bwwaza = 100;}

	# ヘッダー表示
	&header;

	# HTMLの表示
	print "<table border=0>\n";
	print "<tr>\n";
	print <<"EOM";
<td valign="top">
	<form action="$script" method="POST">
	<input type="hidden" name="mode" value="log_in">
	<table border=1>
	<tr><td id="td2" align=center colspan=5 class=b2><font class="$white">前回の続き</font></td></tr>
	<tr><td class=b1>I D</td><td><input type="text" size="10" name="id" value="$c_id"></td>
	<td class=b1>パスワード</td><td><input type="password" size="10" name="pass" value="$c_pass"></td>
	<td><input type="submit" class="btn" value="ログイン"></td></tr></table></form>
	<form action="$scripts" method="POST">
	<input type="hidden" name="mode" value="load_game"></td><td>
	<table border=1>
	<tr><td id="td2" align=center colspan=5 class=b2><font class="$white">記憶の教会から</font></td></tr>
	<tr><td class=b1>I D</td><td><input type="text" size="10" name="id" value="$c_id"></td>
	<td class=b1>パスワード</td><td><input type="password" size="10" name="pass" value="$c_pass"></td>
	<td><input type="submit" class="btn" value="ロード"></td></tr></table></form></td><td>
	<form action="$script" method="POST">
	<input type="hidden" name="mode" value="log_in">
	<table border=1>
	<tr><td id="td2" align=center colspan=5 class=b2><font class="$white">テストプレイ</font></td></tr>
	<tr><input type=hidden name="id" value=test>
	<input type=hidden name="pass" value=test>
	<td><input type="submit" class="btn" value="テストプレイ"></td></tr></table></form>
	<FORM ACTION="$scripta" METHOD="POST"><INPUT TYPE="hidden" NAME="mode" VALUE="chara_make"></td><td>
	<table border=1>
	<tr><td id="td2" align=center colspan=5 class=b2><font class="$white">新規キャラ作成</font></td></tr>
	<tr><td><input type="submit" class="btn" value="新規キャラクタ作成"></td></tr></table></form>
      
</td></tr></table>
<table border=0 width='90%'><tr><td align="center" talign="center" class="b1"><MARQUEE>$telop_message</MARQUEE></td></tr></table>
EOM

	open(GUEST,"$guestfile");
	@member=<GUEST>;
	close(GUEST);

	$num = @member;

	print "<font size=2 color=#aaaaff>現在の冒険者(<B>$num人</B>)：</font>\n";

	foreach $line (@member) {
	($ntimer,$nname,$nid,$nhost) = split(/ \, /, $line);

	if(!@member){@member = '辺りには誰もいません・・・'; $num = 0;}
	print "<a href=\"$scripta?mode=chara_sts&id=$nid\">$nname</a><font size=1 color=#ffff00>★</font>";
	}
	print <<"EOM";
<br>現在の連勝記録は、$rnameさんの「<A HREF=\"http\:\/\/$rurl\" TARGET=\"_blank\"><FONT SIZE=\"3\" COLOR=\"#6666BB\">$rsite</FONT></A>」、$rcount連勝です。新記録を出したサイト名の横には、<IMG SRC="$mark">マークがつきます。
<table border=0 width='100%'>
<tr>
<td width="500" valign="top">
	<table border=1 width="100%">
	<tr>
	<td id="td1" colspan=5 align="center" class="b2"><font class="$white">$wcount連勝中</font><font color="#FFFF00">($lname の <A HREF=\"http\:\/\/$lurl\" TARGET=\"_blank\">$lsite</A> に勝利！！)</font></td>
	</tr>
	<tr>
	<td id="td2" align="center" class="b1">ホームページ</td>
	<td colspan="4"><a href="http\:\/\/$wurl"><b>$wsite</b></a>
EOM
	if($rurl eq "$wurl") {
		print "<IMG SRC=\"$mark\" border=0>\n";
	}

$wmaster = "";
if ($ws0){$wmaster .="<tr><td nowrap align=center width=20% class=b1>$chara_syoku[0]</td>";}
if ($ws1){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[1]</td>";}
if ($ws2){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[2]</td>";}
if ($ws3){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[3]</td>";}
if ($ws4){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[4]</td></tr>";}
if ($ws5){$wmaster .="<tr><td nowrap align=center width=20% class=b1>$chara_syoku[5]</td>";}
if ($ws6){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[6]</td>";}
if ($ws7){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[7]</td>";}
if ($ws8){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[8]</td>";}
if ($ws9){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[9]</td></tr>";}
if ($ws10){$wmaster .="<tr><td nowrap align=center width=20% class=b1>$chara_syoku[10]</td>";}
if ($ws11){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[11]</td>";}
if ($ws12){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[12]</td>";}
if ($ws13){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[13]</td>";}
if ($ws14){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[14]</td></tr>";}
if ($ws15){$wmaster .="<tr><td nowrap align=center width=20% class=b1>$chara_syoku[15]</td>";}
if ($ws16){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[16]</td>";}
if ($ws17){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[17]</td>";}
if ($ws18){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[18]</td>";}
if ($ws19){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[19]</td></tr>";}
if ($ws20){$wmaster .="<tr><td align=center class=b1>$chara_syoku[20]</td>";}
if ($ws21){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[21]</td>";}
if ($ws22){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[22]</td>";}
if ($ws23){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[23]</td>";}
if ($ws24){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[24]</td></tr>";}
if ($ws25){$wmaster .="<tr><td nowrap align=center width=20% class=b1>$chara_syoku[25]</td>";}
if ($ws26){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[26]</td>";}
if ($ws27){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[27]</td>";}
if ($ws28){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[28]</td>";}
if ($ws29){$wmaster .="<td nowrap align=center width=20% class=b1>$chara_syoku[29]</td></tr>";}
if ($ws30){$wmaster .="<tr><td nowrap align=center width=20% class=b1>$chara_syoku[30]</td>";}

	$kyouyuu="";$index=0;
	foreach (@site_url) {
		$kyouyuu.="<a href=\"$_\">$site_title[$index]</a>/";
		$index++;
		}

	print <<"EOM";
</td></tr><tr>
<td align="center" rowspan="11" valign=bottom><img src="$img_path/$chara_img[$wchara]"><p><font color=$white>$wtotal</font>戦<font color=$white>$wkati</font>勝中<br>勝率：$ritu\%<br>
<table width="100%" border=1>
<tr><td id="td2" class="b2">武器</td><td align="center" class="b2">$wi_name</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="center" class="b2">$wd_name</td></tr>
<tr><td id="td2" class="b2">飾り</td><td align="center" class="b2">$a_name</td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $wi_plus %</b></td></tr>
<tr><td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu + $wd_plus %</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $a_wazaup%</b></td><td></td></tr>
</table></td><tr>
<td id="td2" align="center" class="b1">なまえ</td><td class="b2"><b>$wname</b></td>
<td id="td2" align="center" class="b1">性別</td><td class="b2"><b>$esex</b></td></tr>
<tr><td id="td2" align="center" class="b1">ジョブ</td><td class="b2"><b>$chara_syoku[$wsyoku]</b></td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$wcllv</b></td></tr>
<tr><td id="td2" align="center" class="b1">クラス</td><td colspan=3 class="b2"><b>$class</b></td></tr>
<tr><td id="td2" align="center" class="b1">レベル</td><td class="b2"><b>$wlv</b></td>
<td id="td2" align="left" class="b1">経験値</td><td class="b2"><b>$wex/$next_ex</b></td></tr>
<tr><td id="td2" align="left" class="b1">HP</td><td class="b2"><b>$whp\/$wmaxhp</b></td>
<td id="td2" align="left" class="b1">賞金</td><td class="b2"><b>$wgold</b></td></tr>
<tr><td id="td2" align="left" class="b1">力</td><td class="b2"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$wn_0 + $a_0up</b></td>
<td id="td2" align="left" class="b1">魔力</td><td class="b2"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$wn_1 + $a_1up</b></td></tr>
<tr><td id="td2" align="left" class="b1">信仰心</td><td class="b2"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$wn_2 + $a_2up</b></td>
<td id="td2" align="left" class="b1">生命力</td><td class="b2"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$wn_3 + $a_3up</b></td>	</tr>
<tr><td id="td2" align="left" class="b1">器用さ</td><td class="b2"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$wn_4 + $a_4up</b></td>
<td id="td2" align="left" class="b1">速さ</td><td class="b2"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$wn_5 + $a_5up</b></td></tr>
<tr><td id="td2" align="left" class="b1">魅力</td><td class="b2"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$wn_6 + $a_6up</b></td>
<td id="td2" align="left" class="b1">カルマ</td><td class="b2"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$wlp + $a_lpup</b></td></tr>
</table>
<table width="100%" border=1><tr><td id="td2" align="center" class="b1">極めたジョブ</td></tr>
<tr><td colspan=3 align="center" class="b1">$wmaster</td></tr></table>
</td>
<td valign="top">
<td valign="top" align="left">
	<table border=1>
	<td colspan=5 align="center" class="b2"><font color="#FFFFFF">チョコボレース速報</font></td>
	<tr>
	<td colspan=5 align="center">連勝記録は<b>$crnameさん</b>の<b>$crcount連勝</b>です</td>
	<tr>
	<td colspan=5 align="center" class="b2"><font color="#FFFFFF">チョコボキング$cwcount連勝中</font></td>
	</tr>
	<tr>
	<td align="center" rowspan="7" valign=bottom><img src="$img_path/$choco_img[$cw_no]" width=60 height=60><p>勝率：$critu\%</td>
	<td align="center" class="b1" colspan=2>ブリーダー</td><td colspan=2><b>$cwname</b></td>
	<tr><td align="center" class="b1">なまえ</td><td><b>$cw_name</b></td>
	<td align="center" class="b1">ランク</td><td><b>$crank</b></td></tr>
	<tr><td align="center" class="b1">スピード</td><td><b>$cysp</b></td>
	<td align="center" class="b1">スタミナ</td><td><b>$cw_sta/$cw_maxsta</b></td></tr><tr><td align="center" class="b1">クラス</td><td><b>$cls</b></td>
	<td align="center" class="b1">根性</td><td><b>$kon</b></td></tr>
        <tr><td align="center" class="b1">状態</td><td><b>$csta</b></td>
	<td align="center" class="b1">脚質</td><td><b>$waza</b></td></tr>
        <tr><td align="center" class="b1">必殺率</td><td><b>$cw_ritu%</b></td>
        <td align="center" class="b1">総賞金</td><td><b>$cw_moneyギル</b></td>
	<tr><td colspan=4 align="center">$clname に勝利！！</td></tr>
	</table>


[<B><FONT COLOR=$yellow>$main_title の遊び方</FONT></B>]
<OL>
<LI>まず、「新規キャラクター登録」ボタンを押して、キャラクターを作成します。
<LI>キャラクターの作成が完了したら、このページの右上にあるところからログインして、あなた専用のステータス画面に入ります。
<LI>そこであなたの行動を選択することができます。
<LI>一度キャラクターを作成したら、右上のところからログインして遊びます。新規にキャラクターを作れるのは、一人に一つのキャラクターのみです。
<LI>これは、HPバトラーではなく、キャラバトラーです。キャラクターを育てていくゲームです。
<LI>能\力を振り分けることができキャラクターの能\力をご自分で決めることができます。(ここで決めた能\力はごくまれにしか上昇しないので、慎重に)
<LI><b>$limit日</b>以上闘わなければ、キャラクターのデータが削除されます。
<LI>一度戦闘すると<b>$b_time</b>秒経過しないと再び戦闘できません。
</OL>
</td>
</tr>
</table>
<hr size=0>
<font color=$white>共有設置者/<a href="$homepage" TARGET="_top">$home_title</a> / $kyouyuu<br>
<font color=$white>メニュー/</font><a href="$scripta?mode=ranking&first=1&end=20">登録者一覧</a> / <a href="$scripta?mode=mori_ranking&first=1&end=20">レジェンドプレイス攻略者一覧</a> / <a href="$ranking">\能\力別ランキングへ</a> / <a href="$syoku_html">各職業に必要な特性値</a> /<a href="$scripta?mode=img_list"  target="_blank">$vote_gazou</a> /<a href="$bbs">$bbs_title</a> /<a href="$helptext">$helptext_url</a><br>
<font color=$white>町の外れ/</font><a href="$sbbs">$sbbs_title</a> / <a href="$vote">$vote_title</a> /<br><p>
<table border=0 width="100%">
<TR><TD class="b1" bgcolor="#000000" align="center"><B>連絡事項</B></font></TD></TR>
<TR><TD class="b2">$kanri_message</TD></TR></table>
	<form action="$scriptk" method="POST">
	<input type="hidden" name="mode" value="kanri">
	<table><td><input type="password" size="10" name="pass"></td>	<td><input type="submit" class="btn" value="管理者"></td></tr></table></form>
EOM

	# フッター表示
	&footer;

	exit;
}
__SUB__

	read_winner => <<'__SUB__',
#--------------------#
#  チャンプ読み込み  #
#--------------------#
sub read_winner {
	open(IN,"$winner_file");
	@winner = <IN>;
	close(IN);

	chomp(@winner);

	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec) = split(/<>/,$winner[0]);
}
__SUB__

read_cwinner => <<'__SUB__',
#--------------------#
#  キング読み込み    #
#--------------------#
sub read_cwinner {
	open(IN,"$cwinner_file") or &error('ファイルを開けませんでした。');
	@winner = <IN>;
	close(IN);

	($cw_id,$cw_pass,$cwname,$cw_no,$cw_name,$cw_gold,$cw_rank,$cw_sp,$cw_sta,$cw_maxsta,$cw_ex,$cw_total,$cw_kati,$cw_0,$cw_1,$cw_2,$cw_3,$cw_4,$cw_5,$cw_6,$cw_life,$cw_kon,$cw_waza,$cw_money,$host,$date,$cwcount,$clname) = split(/<>/,$winner[0]);
}
__SUB__

	get_cookie => <<'__SUB__',
#------------------#
#  クッキーを取得  #
#------------------#
sub get_cookie {
	@pairs = split(/;/, $ENV{'HTTP_COOKIE'});
	foreach (@pairs) {
		local($key,$val) = split(/=/);
		$key =~ s/\s//g;
		$GET{$key} = $val;
	}
	@pairs = split(/,/, $GET{'FFADV'});
	foreach (@pairs) {
		local($key,$val) = split(/<>/);
		$COOK{$key} = $val;
	}
	$c_id  = $COOK{'id'};
	$c_pass = $COOK{'pass'};
}
__SUB__

	ihtml_top => <<'__SUB__',
#-----------------#
#  TOPページ表示  #
#-----------------#
sub ihtml_top {
	&read_winner;

	&class;

	if($wkati) { $ritu = int(($wkati / $wtotal) * 100); }
	else { $ritu = 0; }

	open(IN,"$recode_file");
	@recode = <IN>;
	close(IN);

	($rcount,$rname,$rsite,$rurl) = split(/<>/,$recode[0]);

	if($wsex) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $wlv * $lv_up;

	if($witem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($wi_no,$wi_name,$wi_dmg) = split(/<>/);
			if($witem eq $wi_no) { last; }
		}
	}else{ $wi_name = "－"; }

	if($wdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($wd_no,$wd_name,$wd_dmg) = split(/<>/);
			if($wdef eq $wd_no) { last; }
		}
	}else{ $wd_name = "－"; }

	# ヘッダー表示
	&iheader;

	# HTMLの表示
print "<form action=\"$script\" method=\"POST\">\n";
print "<input type=\"hidden\" name=\"mode\" value=\"log_in\">\n";
open(GUEST,"$guestfile");
	@member=<GUEST>;
	close(GUEST);

	$num = @member;

	print <<"EOM";
<font size=2 color=#aaaaff>現在(<B>$num人</B>)：</font><br>
EOM

	print <<"EOM";
前回の続き：<br>
&#63868;<input type="text" size="10" name="id" value="$c_id"><br>
&#63869;<input type="password" size="10" name="pass" value="$c_pass"><br>
<input type="submit" class="btn" value="&#63920;"></form>
記憶の教会から：<br>
<form action="$scripts" method="POST">
<input type="hidden" name="mode" value="load_game">
&#63868;<input type="text" size="10" name="id" value="$c_id"><br>
&#63869;<input type="password" size="10" name="pass" value="$c_pass"><br>
<input type="submit" class="btn" value="&#63920;"></form>
<img src="$img_pathi/$chara_img[$wchara]"><br>
&#63904;：<b>$wname</b><font color="$red">$wcount</font>連勝中<br>
$lname の <A HREF=\"http\:\/\/$lurl\" TARGET=\"_blank\">$lsite</A> に勝利！<br>
<MARQUEE>$telop_message</MARQUEE><br>
[<a href="$isetumei">説明</a><a href="$scripta?mode=ichara_make">登録</a><a href="$scripta?mode=ranking&first=1&end=10">&#63719;</a><a href=\"$scripta?mode=img_reflist\">画</a>]
EOM
	# フッター表示
	&ifooter;

	exit;
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
	print "<embed src=\"$title_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__

	iheader => <<'__SUB__',
#------------------#
#  HTMLのヘッダー  #
#------------------#
sub iheader {
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html><head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
EOM
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
}
__SUB__

	footer => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {
	if($refresh and !$win and $mode eq 'battle') {
		print "【<b><a href=\"http\:\/\/$wurl\">チャンプのホームページへ</a></b>】\n";
	}else{
		if($mode ne ""){
			print "<a href=\"$scripto\">TOPページへ</a>\n";
		}
		if($kid and $mode ne 'log_in' and $mode ne 'tensyoku' and $mode ne 'yado') { 
			print " / <a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">ステータス画面へ</a>\n";
		}
		if($mode eq 'kunren') { 
			print " / <a href=\"$script?mode=log_in&id=$pid&pass=$ppass\">ステータス画面へ</a>\n";
		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
	 print "FFA Emilia・いく改ver1.00 remodeling by <a href=\"http://www3.big.or.jp/~icu/\" target=\"_top\">いく</a><br>\n";
	 print "画像提供 by <a href=\"http://www.wisnet.ne.jp/~jnkw/index.html\" target=\"_top\">Jinkun</a><br>\n";
	 print "FFA Emilia Ver1.01 remodeled by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 remodeled by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        
	print "$verg remodeled by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver edit by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
        print "連打防止 edit by <a href=\"http://shigen.nobg.net/\" target=\"_top\">Dutch</a><br>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	ifooter => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub ifooter {
	if($refresh and !$win and $mode eq 'ibattle') {
		print "【<b><a href=\"http\:\/\/$wurl\">&#63904;</a></b>】\n";
	}else{
		if($mode ne ""){
			print "<a href=\"$scripto\">TOP</a>\n";
		}
		if($kid and $mode ne 'ilog_in' and $mode ne 'itensyoku' and $mode ne 'iyado') { 
			print " / <a href=\"$script?mode=ilog_in&id=$kid&pass=$kpass\">&#63873;</a>\n";
		}
		if($mode eq 'ikunren') { 
			print " / <a href=\"$script?mode=ilog_in&id=$pid&pass=$ppass\">&#63873;</a>\n";
		}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	link_chack => <<'__SUB__',
#------------------#
#直リンクチェック  #
#------------------#
sub link_chack {
	#直リンク防止処理
	$geturl = $ENV{'HTTP_REFERER'};
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	#直リンク抑止機能使用に案内するＵＲＬ
	$guid ="<H1>呼び出し元が正しくありません！！</H1>";
	if ($top_url){$guid.="<a href=\"$top_url\">$top_url</a>から入りなおしてください。";}
	else{
		$guid.="<p><font color=$yellow size=4>共有サイト一覧</font><p>";
		$index=0;
		foreach (@site_url) {
			$guid.="<a href=\"$_\">$site_title[$index]</a>/";
			$index++;
			}
		}
	if($geturl eq "" and $browser ne "DoCoMo"){
	&header;
	print "<center><hr width=400><h3>ERROR !</h3>\n";
	print "<P><font color=$red><B>$guid</B></font>\n";
	print "<P><hr width=400></center>\n";
	print "</body></html>\n";
	exit;
	} 
}
__SUB__
);
}
