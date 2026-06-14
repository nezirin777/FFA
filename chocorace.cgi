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

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
if($mode eq 'chocobattle') { &chocobattle; }
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
	chocobattle => <<'__SUB__',
#--------------#
#  レース画面  #
#--------------#
sub chocobattle {
	if($cbattle_flag) { &error("現在レース中です。少しお待ちになってください。"); }

	$cbattle_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi") or &error('ファイルを開けませんでした。');
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$chocolog_file");
	@log_choco = <IN>;
	close(IN);

	foreach(@log_choco){
	($cy_id,$cy_pass,$cy_kname,$cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($kid eq "$cy_id"){ $hit=1;last; }
	}

	&read_cwinner;

	$ltime = time();
	$ltime = $ltime - $kdate;
	$vtime = $b_time - $ltime;

	if($cw_id eq $kid) { &error("現在チョコボキングなのでレースはできません。"); }

	if($cy_life < 3) { &error("チョコボが弱っています。レースはできません。");}

	if($vtime > 0){
	if($ltime < $b_time or !$ktotal) { &error("あと$vtime秒レースはできません。"); }
			}
	if($in{'site'}) { $ksite = $in{'site'}; }
	if($in{'url'}) { $kurl = $in{'url'}; }
	if($in{'waza'}) { $kwaza = $in{'waza'}; }
	if($in{'c_name'}) { $kname = $in{'c_name'}; }
	$km_flg = int(rand($cw_maxsta));
        if($km_flg<$cw_maxsta/2){$km_flg = $cw_maxsta/2};
        if($km_flg%50 != 0){$km_flg=int($km_flg-($km_flg%50));}
	$wm_flg = $km_flg;
        $tekitou= $km_flg;
        $waza = $cy_waza;
        $wwaza = $cw_waza;
        $wkon = $cw_kon;
        $kon =  $cy_kon;
        $ksta_flg = cy_sta;
	$wsta_flg = cw_sta;

	$i=1;$j=0;@battle_date=();
	foreach(1..$turn) {
if($cw_maxsta < 10000){
		$dmg1 = $cy_5 + $cy_sp * (int(rand(3)) + 1);
		$dmg2 = $cw_5 + $cw_sp * (int(rand(3)) + 1);
}
elsif($cw_maxsta < 10000000){
		$dmg1 = ($cy_5 + $cy_sp * (int(rand(3)) + 1))*5;
		$dmg2 = ($cw_5 + $cw_sp * (int(rand(3)) + 1))*5;
}
elsif($cw_maxsta < 100000000000){
		$dmg1 = ($cy_5 + $cy_sp * (int(rand(3)) + 1))*25;
		$dmg2 = ($cw_5 + $cw_sp * (int(rand(3)) + 1))*25;
}
		$clit1 = "";
		$clit2 = "";
		$com1 = "";
		$com2 = "";
		$kawasi1 = "";
		$kawasi2 = "";
		$battle_mes1 = "";
		$battle_mes2 = "";
		$sake1 = int(rand($cy_5)) - int(rand($cw_4));
		$sake2 = int(rand($cw_5)) - int(rand($cy_4));
		$kclit = $km_flg / 10;
		$wclit = $wm_flg / 10;
		$kmclit = $kmaxhp / 10;
		$wmclit = $wmaxhp / 10;
		$mybar = int(($km_flg /$tekitou ) * 100);
                $myb2 = 100 - $mybar + 1;
                $enbar = int(($wm_flg /$tekitou ) * 100);
                $enb2 = 100 - $enbar + 1;
                $ritu = int(($kon + $cy_sp )/30);
              	$writu = int(($wkon + $cw_sp )/30);
                if($writu >40){$writu= 40;}
                elsif($writu < 0){$writu= 1;}
                if($ritu >40){$ritu= 40;}
                elsif($ritu < 0){$ritu= 1;}
	                  	# 挑戦者走行距離計算
			$com1 = "$knameの$cy_nameが走る！！<p>";
			if(int(rand(9)) == 0) {
				$com1 .= "<font size=5>$kname「ダッシュだ！」</font><p><font color=\"#FF0000\" size=7></font>\n";
				$dmg1 = $dmg1 * 2;
			}
			$dmg1 = $dmg1 + int(rand($cy_5));

			if($cy_life < 40){
				$sdmg1 = int($dmg1 / 2);
				}else{$sdmg1 = int($dmg1 / 3);}

			# キング走行距離計算
			$dmg2 = $dmg2 + int(rand($cw_5));

			if($cw_life < 40){
			$sdmg2 = int($dmg2 / 2);
				}else{$sdmg2 = int($dmg2 / 3);}

			$com2 = "$wnameの$cwnameが走る！！<p>";
                        
                        if(int(rand(100))<$ritu) {
				$clit1 = "<b><font SIZE=5 COLOR=\"$red\">必殺！！チョコボスラッシュラン！！</font></b><P>";
				$dmg1 = $dmg1 * 3;
			}
                        if(int(rand(9))==0) {
				$clit1 = "<b><font SIZE=5 COLOR=\"$blue\">$cy_nameが根性を振り絞る！！スタミナが$kon回復した</font></b><P>";
				$sdmg1 = $sdmg1 -$kon;
			}

                        if(int(rand(9))==0) {
				$clit2 = "<b><font SIZE=5 COLOR=\"$blue\">$cw_nameがチャンプの意地を見せる！！スタミナが$wkon回復した</font></b><P>";
				$sdmg2 = $sdmg2 -$wkon;
			}
			if(int(rand(30)) == 0) {
				$clit1 = "<b><font SIZE=5 COLOR=\"$yellow\">猛ダッシュ！！</font></b><P>";
				$dmg1 = $dmg1 * 3;
			}
                        if(int(rand(100))<$writu) {
				$clit2 = "<b><font SIZE=5 COLOR=\"$red\">必殺！！チャンプストライクダッシュ！！</font></b><P>";
				$dmg2 = $dmg2 * 3;
			}		
                	if(int(rand(30)) == 0) {
				$clit2 = "<font size=5>$wname「そこだ！」</font><p><b><font SIZE=5 COLOR=\"$yellow\">猛ダッシュ！！</font></b><P>";
				$dmg2 = int($dmg2 * 3.5);
			}

			if($wmaxhp > ($kmaxhp * 2) and $i == 1) {
				if($cw_rank - $cy_rank >= $level_sa){
				$sa = $kmaxhp;
				$clit1 .= "<p><font size=5><b>$knameと<font color=red>チョコボの心</font>がひとつになった！</b></font><P>";
					if($wmaxhp < $sa){$dmg1 = $dmg1;}
					elsif($dmg1 > 200 - $sa){$dmg1 = $dmg1;}
					else{$dmg1 = 200 - $sa;}
				}else{
					if(int(rand(4)) == 1){
				$sa = $kmaxhp;
				$clit1 .= "<p><font size=5><b>$knameと<font color=red>チョコボの心</font>がひとつになった！</b></font><P>";
					if($wmaxhp < $sa){$dmg1 = $dmg1;}
					elsif($dmg1 > 200 - $sa){$dmg1 = $dmg1;}
					else{$dmg1 = 200 - $sa;}
					}
				}
			}

			if($kmaxhp > ($wmaxhp * 2) and $i == 1) {
				if($cy_rank - $cw_rank >= $level_sa){
				$wsa = $wmaxhp;
				$clit2 .= "<p><font size=5><b>$wnameと<font color=blue>チョコボの心</font>がひとつになった！</b></font><P>";
					if($kmaxhp < $wsa){$dmg2 = $dmg2;}
					elsif($dmg2 > 200 - $wsa){$dmg2 = $dmg2;}
					else{$dmg2 = 200 - $wsa;}
				}else{
					if(int(rand(4)) == 1){
				$wsa = $wmaxhp;
				$clit2 .= "<p><font size=5><b>$wnameと<font color=blue>チョコボの心</font>がひとつになった！</b></font><P>";
					if($kmaxhp < $wsa){$dmg2 = $dmg2;}
					elsif($dmg2 > 200 - $wsa){$dmg2 = $dmg2;}
					else{$dmg2 = 200 - $wsa;}
					}
				}
			}
	if($waza ==1){if($km_flg > 0){$dmg1 = int($dmg1 * 1);}}

        if($waza ==2){if($km_flg > $km_flg*0.75){$dmg1 = int($dmg1 * 1.5);}
                      else{$dmg1 = int($dmg1 * 0.75);}
		}
        if($waza ==3){if($km_flg > $km_flg*0.6){$dmg1 = int($dmg1 * 1.2);}
                      else{$dmg1 = int($dmg1 * 0.9);}
		}
        if($waza ==4){if($km_flg > $km_flg*0.5){$dmg1 = int($dmg1 * 0.8);}
                      else{$dmg1 = int($dmg1 * 1.7);}
		}
        if($waza ==5){if($km_flg > $km_flg*0.75){$dmg1 = int($dmg1 * 0.6);}
                      else{$dmg1 = int($dmg1 * 3);}
		}   
         
        if($wwaza ==1){if($wm_flg > 0){$dmg2 = int($dmg2 * 1);}}

        if($wwaza ==2){if($wm_flg > $wm_flg*0.75){$dmg2 = int($dmg2 * 1.5);}
                      else{$dmg2 = int($dmg2 * 0.75);}
		}
        if($wwaza ==3){if($wm_flg > $wm_flg*0.6){$dmg2 = int($dmg2 * 1.2);}
                      else{$dmg2 = int($dmg2 * 0.9);}
		}
        if($wwaza ==4){if($wm_flg > $wm_flg*0.5){$dmg2 = int($dmg2 * 0.8);}
                      else{$dmg2 = int($dmg2 * 1.7);}
		}
        if($wwaza ==5){if($wm_flg > $wm_flg*0.75){$dmg2 = int($dmg2 * 0.6);}
                      else{$dmg2 = int($dmg2 * 3);}
		}           

                	if($dmg2 < 0){$dmg2 = $dmg2;}
			elsif($dmg2 < $cd_dmg){$dmg2 = 0;}
			else{$dmg2 = $dmg2 - $cd_dmg;}

			if($dmg1 < 0){$dmg1 = $dmg1;}
			elsif($dmg1 < $wd_dmg){$dmg1 = 0;}
			else{$dmg1 = $dmg1 - $wd_dmg;}

	if($wm_flg < $wmclit){
		if($wm_flg < $kclit){
			if($i > 15){
			$dmg2 = $dmg2 * 5;
			$com2 .="<p><font SIZE=5 COLOR=\"$blue\">最後の追いこみ！！<p>";
				}
			}
	}elsif(int(rand($sake1)) + int(rand($klp)) - int(rand($wlp))> int(rand(40))) {
		$dmg2 = 0;
		$kawasi1 = "<P><FONT SIZE=4 COLOR=\"$green\">$cw_nameはよろけた！</FONT><P>";
	}
	if($km_flg < $kmclit){
		if($km_flg < $wclit){
			if($i > 15){
			$dmg1 = $dmg1 * 5;
			$com1 .="<p><font SIZE=5 COLOR=\"$blue\">最後の追いこみ！！<p>";
				}
			}
	}elsif(int(rand($sake2)) + int(rand($wlp)) - int(rand($klp))> int(rand(40))) {
		$dmg1 = 0;
		$kawasi2 = "<P><FONT SIZE=4 COLOR=\"$green\">$cy_nameはよろけた！</FONT><P>";
	}

	$d_k=int(rand(11))+2;
	$d_w=int(rand(11))+2;
	if((int($cy_5 / 6) + $d_k + 2) >= (int($cw_5 / 6) + $d_w)) {
	$battle_mes1 = "$com1 $clit1 $kawasi2 $cy_name は <font SIZE=3 COLOR=\"$yellow\"><b>$dmg1</b></font> メートル走った。<small>スタミナが<font color=\"$red\">$sdmg1</font>減った。</small><br>";
	if($km_flg - $dmg1 <= 0) { $battle_mes2 = ""; $dmg2 = 0;}
	else{$battle_mes2 = "$com2 $clit2 $kawasi1 $cw_name は <b><font SIZE=3 COLOR=\"$yellow\"><b>$dmg2</b></font> メートル走った。<small>スタミナが<font color=\"$red\">$sdmg2</font>減った。</small><p>";}
	}
	else {$battle_mes1 = "$com2 $clit2 $kawasi1 $cw_name は <font SIZE=3 COLOR=\"$yellow\"><b>$dmg2</b></font> メートル走った。<small>スタミナが<font color=\"$red\">$sdmg2</font>減った。</small><p>";
	if($wm_flg - $dmg2 <= 0) { $battle_mes2 =""; $dmg1 = 0;}
	else{$battle_mes2 = "$com1 $clit1 $kawasi2 $cy_name は <font SIZE=3 COLOR=\"$yellow\"><b>$dmg1</b></font> メートル走った。<small>スタミナが<font color=\"$red\">$sdmg1</font>減った。</small><br>";}
	}

		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0>
<TR>
	<TD CLASS="b2"id="td2" COLSPAN="3" ALIGN="center">
	$iターン
	</TD>
</TR>
<TR>
	<TD ALIGN="center">
	<IMG SRC="$img_path/$choco_img[$cy_no]" width=60 height=60><table width="100%" border=1>
</table>
	</TD>
	<TD>
	</TD>
	<TD ALIGN="center">
	<IMG SRC="$img_path/$choco_img[$cw_no]" width=60 height=60><table width="100%" border=1>
</table></TD>
	</TR>
<TR>
<TD>
<TABLE BORDER=0>
<TR>
	<TD CLASS="b1"id="td2">
	ブリーダー
	</TD>
	<TD CLASS="b1"id="td2">
	なまえ
	</TD>
	<TD CLASS="b1"id="td2">
	スタミナ
	</TD>
	<TD CLASS="b1"id="td2" align="center">
	残りＭ
	</TD>
</TR>
<TR>
	<TD CLASS="b2">
	$kname
	</TD>
	<TD CLASS="b2">
	$cy_name
	</TD>
	<TD CLASS="b2">
	$cy_sta\/$cy_maxsta
	</TD>
	<TD CLASS="b2">
	$km_flg/$tekitou<BR>
	<IMG SRC="$img_path/mrk.gif" WIDTH=$mybar HEIGHT=5 ALIGN=top><IMG SRC="$img_path/mrk_r.gif" WIDTH=$myb2 HEIGHT=5 ALIGN=top>
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT SIZE=5 COLOR="$red">VS</FONT>
</TD>
<TD>
<TABLE BORDER=0>
<TR>
	<TD CLASS="b1"id="td2">
	ブリーダー
	</TD>
	<TD CLASS="b1"id="td2">
	なまえ
	</TD>
	<TD CLASS="b1"id="td2">
	スタミナ
	</TD>
	<TD CLASS="b1"id="td2" align="center">
	残りＭ
	</TD>
</TR>
<TR>
	<TD CLASS="b2">
	$wname
	</TD>
	<TD CLASS="b2">
	$cw_name
	</TD>
	<TD CLASS="b2">
	$cw_sta\/$cw_maxsta
	</TD>
	<TD CLASS="b2">
	$wm_flg/$tekitou<BR>
        <IMG SRC="$img_path/mrk.gif" WIDTH=$enbar HEIGHT=5 ALIGN=top><IMG SRC="$img_path/mrk_r.gif" WIDTH=$enb2 HEIGHT=5 ALIGN=top>
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
<p>
$battle_mes1
<br>
$battle_mes2
<p>
EOM

		$km_flg = $km_flg - $dmg1 - $dmgme2;
		$wm_flg = $wm_flg - $dmg2 - $dmgme1;
		$cy_sta = $cy_sta - $sdmg1;
		$cw_sta = $cw_sta - $sdmg2;

		if($wm_flg <= 0 or $cy_sta <= 0) { $win = 0; last; }
		elsif($km_flg <= 0 or $cw_sta <= 0) { $win = 1; last; }
	
		$i++;
		$j++;

	}

	if($wm_flg <=0){ $mes1 = "<b><font size=5>先頭は$wnameの$cw_name！今ゴールです！</font></b>";}
	if($km_flg <=0){ $mes1 = "<b><font size=5>先頭は$knameの$cy_name！今ゴールです！</font></b>";}

	if($win) {
		if($cw_sta <=0){ $mes1 = "<b><font size=5>$cw_nameの<font color=\"red\">スタミナ</font>が切れてしまった（＞＜</font></b>";}
		$cy_total += 1;
		$cy_kati += 1;
		$exp = int($cw_rank * $kiso_exp + (rand($cy_rank) + 1));
		$cy_ex = $cy_ex + $exp;
		$gold = $cy_rank * 10 ;
		$cy_life -= 3;
		$comment = "<b><font size=5>$knameの勝ち！！</font></b><p><b><font size=5 color=\"#ff0000\">$kname「よくやった$cy_name！」</font></b><p><b><font size=5 color=\"#0000ff\">$cy_name「クエ～♪」</font></b><p>";
	}else{
		if($cy_sta <=0){ $mes1 = "<b><font size=5>$cy_nameの<font color=\"red\">スタミナ</font>が切れてしまった（＞＜</font></b>";}
		$cy_total += 1;
		$exp = int($cw_rank * (rand($cy_rank) + 1));
		$cy_ex = $cy_ex + $exp;
		$gold = int(rand($cy_rank));
		$cy_life -= 3;
		$comment = "<b><font size=5>$knameの負けだ・・・。</font></b><p><b><font size=5 color=\"#0000ff\">$kname「$cy_name～～（T_T）」</font></b><p><b><font size=5 color=\"#ff0000\">$cy_name「クエエエ・・・」</font></b><p>";
	}

	while($cy_ex >= ($cy_rank * $lv_up)) {
		$comment .= "$cy_nameは、ひとまわり成長した！！<p>";
		$hpup = int(rand($cy_3)) + 10;
                  if($cy_maxsta >= 999999) {
                   $cy_maxsta = 999999;
                  }elsif($cy_maxsta < 999999) {
                   $cy_maxsta = $cy_maxsta + $hpup;
                   if($cy_maxsta > 999999){
                   $cy_maxsta = 999999;
                   }
                  }
		$cy_sta = $cy_maxsta;
		$comment .= "スタミナがついた<p>";
		$cy_ex = $cy_ex - ($cy_rank * $lv_up);
		$cy_rank += 1;
                if($cy_0 >= 99999) {
                  $cy_0 = 99999;
                }elsif($cy_0 < 99999) {
                if(int(rand(3)) == 0) { $cy_0 += $cy_rank; $t1 = 1;}
                }
                if($cy_1 >= 99999) {
                 $cy_1 = 99999;
                }elsif($cy_1 < 99999) {
                if(int(rand(3)) == 0) { $cy_1 += $cy_rank; $t2 = 1;}
                }
                if($cy_2 >= 99999) {
                 $cy_2 = 99999;
                }elsif($cy_2 < 99999) {
                if(int(rand(3)) == 0) { $cy_2 += $cy_rank; $t3 = 1;}
                }
                if($cy_3 >= 99999) {
                 $cy_3 = 99999;
                }elsif($cy_3 < 99999) {
                if(int(rand(3)) == 0) { $cy_3 += $cy_rank; $t4 = 1;}
                }
                if($cy_4 >= 99999) {
                 $cy_4 = 99999;
                }elsif($cy_4 < 99999) {
                if(int(rand(3)) == 0) { $cy_4 += $cy_rank; $t5 = 1;}
                }
                if($cy_5 >= 99999) {
                 $cy_5 = 99999;
                }elsif($cy_5 < 99999) {
                if(int(rand(3)) == 0) { $cy_5 += $cy_rank; $t6 = 1;}
                }
                if($cy_6 >= 99999) {
                 $cy_6 = 99999;
                }elsif($cy_6 < 99999) {
                if(int(rand(3)) == 0) { $cy_6 += $cy_rank; $t7 = 1;}
                }
                 if($cy_kon >= 99999) {
                 $cy_kon = 99999;
                }elsif($cy_kon < 99999) {
                if(int(rand(3)) == 0) { $cy_kon += $cy_rank; $t8 = 1;}
                }
		if($t1) { $comment .= "硬派な感じだ♪。"; }
		if($t2) { $comment .= "賢そうに見える♪。"; }
		if($t3) { $comment .= "神々しい感じだ♪。"; }
		if($t4) { $comment .= "元気がいい♪。"; }
		if($t5) { $comment .= "神経質かも♪。"; }
		if($t6) { $comment .= "体がしまってきた♪。"; }
		if($t7) { $comment .= "ちょっぴりかわいい♪。"; }
                if($t8) { $comment .= "根性がついてきた♪。"; }
	}


	if($cy_sta >= int($cy_maxsta / 2)){
		$cy_sta = int($cy_maxsta * 8 / 10 );
	}else{
		$cy_sta = $cy_sta + int(($cy_maxsta) * 5 / 10);}
	
	if($cw_sta >= int($cw_maxsta / 2)){
		$cw_sta = $cw_maxsta;
	}else{
		$cw_sta = $cw_sta + int(($cw_maxsta) * 7 / 10);}

	if($cy_sta >= $cy_maxsta) { $cy_sta = $cy_maxsta; }

	if($cw_sta > $cw_maxsta) { $cw_sta = $cw_maxsta; }

	if($cy_sta <= 0) { $cy_sta = int($cy_maxsta * 4 / 10 ); }
	if($cw_sta <= 0) { $cw_sta = int($cw_maxsta * 4 / 10 ); }
        $kgold = $kgold + $gold;
        # ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"$chocolog_file") or &error('ファイルを開けませんでした。');
	@choco_chara = <IN>;
	close(IN);

	$hit=0;@new=();
	foreach(@choco_chara){
	($c_id,$c_pass,$c_kname,$c_no,$c_name,$c_gold,$c_rank,$c_sp,$c_sta,$c_maxsta,$c_ex,$c_total,$c_kati,$c_0,$c_1,$c_2,$c_3,$c_4,$c_5,$c_6,$c_life,$c_kon,
$c_waza,$c_money) = split(/<>/);
		if($kid eq "$c_id") {$cy_money = $c_money + $gold;
                                     
	unshift(@new,"$cy_id<>$cy_pass<>$kname<>$cy_no<>$cy_name<>$cy_gold<>$cy_rank<>$cy_sp<>$cy_sta<>$cy_maxsta<>$cy_ex<>$cy_total<>$cy_kati<>$cy_0<>$cy_1<>$cy_2<>$cy_3<>$cy_4<>$cy_5<>$cy_6<>$cy_life<>$cy_kon<>$cy_waza<>$cy_money<>\n");
	$hit=1;
	}else{
	push(@new,"$_");
	}
	}

	if(!$hit){
	unshift(@new,"$kid<>$kpass<>$kname<>$cy_no<>$cy_name<>$cy_gold<>$cy_rank<>$cy_sp<>$cy_sta<>$cy_maxsta<>$cy_ex<>$cy_total<>$cy_kati<>$cy_0<>$cy_1<>$cy_2<>$cy_3<>$cy_4<>$cy_5<>$cy_6<>$cy_life<>$cy_kon<>$cy_waza<>$cy_money<>\n");
	}
	
	open(OUT,">$chocolog_file");
	print OUT @new;
	close(OUT);

	if($win){
		@new=();
		open(IN,">$cwinner_file");
		@winnew = <IN>;
		unshift(@new,"$cy_id<>$cy_pass<>$cy_kname<>$cy_no<>$cy_name<>$cy_gold<>$cy_rank<>$cy_sp<>$cy_sta<>$cy_maxsta<>$cy_ex<>$cy_total<>$cy_kati<>$cy_0<>$cy_1<>$cy_2<>$cy_3<>$cy_4<>$cy_5<>$cy_6<>$cy_life<>$cy_kon<>$cy_waza<>$cy_money<>$khost<>$ltime<>1<>$wname<>\n");
		print IN @new;
		close(IN);

	}else{
		$wcount += 1;
		@new=();
		open(IN,">$cwinner_file");
		@winnew = <IN>;
		unshift(@new,"$cw_id<>$cw_pass<>$wname<>$cw_no<>$cw_name<>$cw_gold<>$cw_rank<>$cw_sp<>$cw_sta<>$cw_maxsta<>$cw_ex<>$cw_total<>$cw_kati<>$cw_0<>$cw_1<>$cw_2<>$cw_3<>$cw_4<>$cw_5<>$cw_6<>$cw_life<>$cw_kon<>$cw_waza<>$cw_money<>$host<>$date<>$wcount<>$kname<>\n");
		print IN @new;
		close(IN);

		open(IN,"$crecode_file") or &error('ファイルを開けませんでした。');
		@recode = <IN>;
		close(IN);

		($count,$name) = split(/<>/,$recode[0]);

		if($wcount > $count) {
			open(OUT,">$crecode_file") or &error('ファイルを開けませんでした。');
			print OUT "$wcount<>$wname<>\n";
			close(OUT);
		}
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&regist;

	if($refresh and !$win) { &header2; } else { &header; }

	print "<h1>$knameと$wnameのレース、スタート！！</h1><hr size=0><p>\n";

	$i=0;
	foreach(@battle_date){
		print "$battle_date[$i]";
		$i++;
	}
	
	print "$mes1<p>$comment<p>$cy_nameは、<b>$exp</b>の経験値を手に入れた。$knameは、<b>$gold</b>G手に入れた。<p>\n";

	&footer;

	$cbattle_flag=0;

	exit;
}
__SUB__

	read_cwinner => <<'__SUB__',
#--------------------------#
#  チョコボキング読み込み  #
#--------------------------#
sub read_cwinner {
	open(IN,"$cwinner_file");
	@winner = <IN>;
	close(IN);

	($cw_id,$cw_pass,$wname,$cw_no,$cw_name,$cw_gold,$cw_rank,$cw_sp,$cw_sta,$cw_maxsta,$cw_ex,$cw_total,$cw_kati,$cw_0,$cw_1,$cw_2,$cw_3,$cw_4,$cw_5,$cw_6,$cw_life,$cw_kon,$cw_waza,$cw_money,$host,$date,$wcount,$lname) = split(/<>/,$winner[0]);
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
			
	print "<form action=\"$script\" method=\"post\">\n";
	print "<A HREF=\"$scripto\">ＴＯＰページへ</A>\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$kpass>\n";
	print "<input type=hidden name=mode value=log_in>\n";
	print "<input type=submit class=btn value=\"ステータス画面へ\">\n";
	print "</form>\n";
	}
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
	print "<embed src=\"$ccbattle_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__
set_cookie => <<'__SUB__',
#------------------#
# クッキーの発行 #
#------------------#
sub set_cookie {
# クッキーは60日間有効
local($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+60*24*60*60);

@month=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);
$cook="id<>$cookie_id\,pass<>$cookie_pass";
print "Set-Cookie: FFADV=$cook; expires=$gmt\n";
}
__SUB__

	header2 => <<'__SUB__',
#--------------#
#  強制送還用  #
#--------------#
sub header2 {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="refresh" content="$refresh;URL=http\:\/\/$wurl" target="_new"> 
<STYLE type="text/css">
<!--
body,tr,td,th { font-size: 10pt }
a:hover { color: $alink }
.b1 {background: #9ac;border-color: #ccf #669 #669 #ccf;color:#fff; border-style: solid; border-width: 1px;}
.b2 {background: #669;border-color: #99c #336 #336 #99c;color:#fff; border-style: solid; border-width: 1px; text-align: center}
.b3 {background: #fff;border-color: #ccf #669 #669 #ccf;}
.dmg { color: #FF0000; font-size: 18pt }
.clit { color: #0000FF; font-size: 18pt }
-->
</STYLE>
EOM
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
}
__SUB__
);
}
