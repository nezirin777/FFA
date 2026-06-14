#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権は下記の4人にあります。
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
&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}

if($mode eq 'log_in') {
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&ilog_in; }else{&log_in; }}
elsif($mode eq 'ists_win') { &ists_win; }
elsif($mode eq 'imsg_win') { &imsg_win; }
elsif($mode eq 'ihelp_win') { &ihelp_win; }

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
	log_in => <<'__SUB__',
#----------------#
#  ログイン画面  #
#----------------#
sub log_in {
	$chara_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@log_in = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_in){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid") {
			$hit=1; last;
		}
	}
	open (IN,"$winner_file") || &error('オープンエラー','指定された書込みファイルが開けません。');
	$LINE = <IN>;
	close (IN);
	    ($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec)=split(/<>/,$LINE);

if(!$hit) { &error("入力されたIDは登録されていません。");}

open (IN,"$cwinner_file") || &error('オープンエラー','指定された書込みファイルが開けません。');
	$LINE =<IN>;
	close (IN);
	    ($cw_id,$cw_pass,$cwname,$cw_no,$cw_name,$cw_gold,$cw_rank,$cw_sp,$cw_sta,$cw_maxsta,$cw_ex,$cw_total,$cw_kati,$cw_0,$cw_1,$cw_2,$cw_3,$cw_4,$cw_5,$cw_6,$cw_life,$cw_kon,$cw_waza,$cw_money,$host,$date,$cwcount,$clname)=split(/<>/,$LINE);

	$ltime = time();
	$ltime = $ltime - $kdate;
	$vtime = $b_time - $ltime;
	$xtime = $vtime + 1;
	$ztime = $vtime - 1;
	$mtime = $m_time - $ltime;

	if($in{'id'} ne "$kid") {&error("オープンエラー、ID・パスワードが正しくありません。");}
	

	# パスワードを照合
	$match = &decrypt("$in{'pass'}","$kpass");
	if ($match ne 'yes') {
		if($in{'pass'} ne $kpass){ &error("パスワードが違います！"); }}

	if($kmori < $boss) { $kmori = 0; }

	&class;

	if($ksex) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $klv * $lv_up;

	open(IN,"$item_file");
	@log_item = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_item){
		($i_no,$i_name,$i_dmg,$i_gold,$i_plus) = split(/<>/);
		if($kitem eq "$i_no"){ $hit=1;last; }
	}
	if(!$hit) { $i_name="－"; }
	if(!$hit) { $i_dmg="－"; $i_plus=0;}

	open(IN,"$def_file");
	@log_def = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_def){
		($d_no,$d_name,$d_dmg,$d_gold,$d_plus) = split(/<>/);
		if($kdef eq "$d_no"){ $hit=1;last; }
	}
	if(!$hit) { $d_name="-"; }
	if(!$hit) { $d_dmg="-"; $d_plus=0;}

	open(IN,"$acs_file");
	@log_acs = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
		if($kacsno eq "$a_no"){ $hit=1;last; }
	}
	if(!$hit) { $a_name="-"; $a_0up=0;$a_1up=0;$a_2up=0;$a_3up=0;$a_4up=0;$a_5up=0;$a_6up=0;$a_lpup=0;$a_hitup=0;$a_kaihiup=0;$a_wazaup=0;}

	open(IN,"$tac_file");
	@log_tac = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_tac){
		($ktac_no,$ktac_name) = split(/<>/);
		if($ktac eq "$ktac_no"){ $hit=1;last; }
	}
	if(!$hit) { $ktac_name="普通に戦う"; }

	# 最大値の設定
	if($kmaxhp > $charamaxhp){$kmaxhp = $charamaxhp}
	if($kn_0 > $charamaxpm){$kn_0 = $charamaxpm;}
	if($kn_1 > $charamaxpm){$kn_1 = $charamaxpm;}
	if($kn_2 > $charamaxpm){$kn_2 = $charamaxpm;}
	if($kn_3 > $charamaxpm){$kn_3 = $charamaxpm;}
	if($kn_4 > $charamaxpm){$kn_4 = $charamaxpm;}
	if($kn_5 > $charamaxpm){$kn_5 = $charamaxpm;}
	if($kn_6 > $charamaxpm){$kn_6 = $charamaxpm;}
	if($klp  > $charamaxpm){$klp  = $charamaxpm;}
       
        if(!$kmoriturn){$syou ="-";}
        if($kmoriturn==1){$syou ="冒険者";}
        if($kmoriturn==2){$syou ="熟練者";}
        if($kmoriturn==3){$syou ="勇者";}
        if($kmoriturn==4){$syou ="伝説の覇者";}
      

	# 基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int((($kn_4 + $a_4up)/ 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int((($kn_5 + $a_5up)/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int((($klp + $alpup)/ 15)) + 10 + $kcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}

        #宿代計算
        $yado_daix=int($yado_dai*$klv);

	# 能力値バーの詳しい幅設定
	$bw0     = int(1 * ($kn_0 / $divpm));
	$bw1     = int(1 * ($kn_1 / $divpm));
	$bw2     = int(1 * ($kn_2 / $divpm));
	$bw3     = int(1 * ($kn_3 / $divpm));
	$bw4     = int(1 * ($kn_4 / $divpm));
	$bw5     = int(1 * ($kn_5 / $divpm));
	$bw6     = int(1 * ($kn_6 / $divpm));
	$bwlp    = int(1 * ($klp / $divpm));
	$i_plus += $a_hitup;
	$d_plus += $a_kaihiup;
	$bwhit   = int(0.5 * ($hit_ritu + $i_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $d_plus));
	$bwwaza  = int(1 * ($waza_ritu + $a_wazaup));
	if($bwhit > 200){$bwhit = 200;}
	if($bwkaihi > 200){$bwkaihi = 200;}
	if($bwwaza > 200){$bwwaza = 200;}
       
       
	#職歴の表示
	$kmaster = "";
if ($ks0){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[0]</td></font>";}
if ($ks1){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[1]</td></font>";}
if ($ks2){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[2]</td></font>";}
if ($ks3){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[3]</td></tr></font>";}
if ($ks4){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[4]</td></font>";}
if ($ks5){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[5]</td></font>";}
if ($ks6){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[6]</td></font>";}
if ($ks7){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[7]</td></tr></font>";}
if ($ks8){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[8]</td></font>";}
if ($ks9){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[9]</td></font>";}
if ($ks10){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[10]</td></font>";}
if ($ks11){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[11]</td></tr></font>";}
if ($ks12){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[12]</td></font>";}
if ($ks13){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[13]</td></font>";}
if ($ks14){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[14]</td></font>";}
if ($ks15){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[15]</td></tr></font>";}
if ($ks16){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[16]</td></font>";}
if ($ks17){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[17]</td></font>";}
if ($ks18){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[18]</td></font>";}
if ($ks19){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[19]</td></tr></font>";}
if ($ks20){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[20]</td></font>";}
if ($ks21){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[21]</td></font>";}
if ($ks22){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[22]</td></font>";}
if ($ks23){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[23]</td></tr></font>";}
if ($ks24){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[24]</td></font>";}
if ($ks25){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[25]</td></font>";}
if ($ks26){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[26]</td></font>";}
if ($ks27){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[27]</td></tr></font>";}
if ($ks28){$kmaster .="<tr><td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[28]</td></font>";}
if ($ks29){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[29]</td></font>";}
if ($ks30){$kmaster .="<td nowrap align=center width=25% class=b1><font color=white>$chara_syoku[30]</td></font>";}

	if($kgold > $gold_max){$kgold = $gold_max;}

	&header;

	 
	&guest_list;

	&guest_view;
       print <<"EOM";

	<hr size=0>
	<font class=white>メニュー/</font><a href="$scripta?mode=ranking&first=1&end=20">登録者一覧</a> / <a href="$scripta?mode=mori_ranking&first=1&end=20">称号獲得者一覧</a> / <a href="$ranking">\能\力別ランキングへ</a> / <a href="$syoku_html">各職業に必要な特性値</a> /<a href="$scripta?mode=img_list" target="_blank">$vote_gazou</a> /<a href="$bbs">$bbs_title</a> /<a href="$helptext">$helptext_url</a><br>
<font class=white>町の外れ/</font><a href="$sbbs">$sbbs_title</a> / <a href="$vote">$vote_title</a> /<br>
<table align="center"width="100%">
<TR><td rowspan="2"  align="center" class="b2" width=70 height=60><img src="$img_path/$chara_img[$wchara]">
<TD id="td1" align="center" colspan=2 class="b2">現在のチャンプ<a href="$scripta?mode=chara_sts&id=$wid"><B>$wname</B></a>さん($wcount連勝中)</TD><td rowspan="2" align="center" VALIGN="middle" valign=bottom class="b2" width=70 height=60><img src="$img_path/$choco_img[$cw_no]" ><TD id="td1" align="center" colspan=2 class="b2">現在のチャンプ<a href="$scripta?mode=chara_sts&id=$cw_id"><B>$cwname</B></a>さん($cwcount連勝中)</TD></TR>
	<TR><td id="td2"align="center" class="b2">現在のHP</td><TD class="b2"align="center"><B>$whp\/$wmaxhp</B></TD><td id="td2"align="center" class="b2">現在のHP</td><TD class="b2"align="center"><B>$cw_sta\/$cw_maxsta</B></TD></TR></table>
</TD></TR></table></TD></table>
<hr size=0>

<table border=0 align="center" width='100%'>
<tr>
<td valign=top width='50%'>
EOM
if($ltime < $b_time or !$ktotal and $ztime > 0){
       print <<"EOM";
<FORM NAME="form1">
戦闘開始可能\まで残り<INPUT TYPE="text" NAME="clock" SIZE="3">秒です。(更新の目安に使って下さい)
EOM
}
       print <<"EOM";
<table width="100%"><tr>
</FORM><form action="$scriptb" method="post">
<tr><td id="td1" colspan="5" class="b2" align="center">キャラクターデータ</td></tr>
<td rowspan="4" align="center" valign=bottom class="b2"><img src="$img_path/$chara_img[$kchara]">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$i_name</td>
<td id="td2" class="b1">攻撃力</td><td align="right" class="b2">$i_dmg</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$d_name</td>
<td id="td2" class="b1">防御力</td><td align="right" class="b2">$d_dmg</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$a_name</td>
	
<td id="td2" class="b2">称号</td><td align="center" class="b2"><font color=yellow>$syou</font></td></tr>
</table>

<table width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr><td class="b1" id="td2">ジョブ</td><td class="b2">$chara_syoku[$ksyoku]</td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$kcllv</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$klv</td>
<td class="b1" id="td2">経験値</td><td class="b2">$kex/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$khp\/$kmaxhp</td>
<td class="b1" id="td2">お金</td><td class="b2">$kgold\/$gold_max</td></tr>
<tr><td class="b1" id="td2">チャンピオンを目指す</td><td colspan="3" align="center" class="b2">
<input type="hidden" name=mode value=battle>
<input type="hidden" name=id value="$kid">
<input type="hidden" name=pass value="$kpass">
EOM

	if($wid eq $kid) { print "現在チャンプなので闘えません\n";
	}elsif($kurl eq $lurl and $chanp_milit == 1) { print "チャンプと戦った直後なので疲れて闘えません\n";
	}elsif($ltime > $b_time or !$ktotal) {
		print "<input type=\"submit\" class=btn value=\"チャンプに挑戦\">\n";
	}else{
		print "$ztime秒後闘えるようになります。\n";
	}

	print <<"EOM";
<br>※賞金：$wgold G
</td>
</tr></form>
<tr><td class="b1" id="td2" class="b2">
<form action="$scripta" method="post">
好きなキャラと対戦</td><td align="center" colspan="3" class="b2">
EOM
	if(!$kmons) { print "１度チャンプに挑戦してください\n";}
	elsif($ltime > $b_time or !$ktotal) {
print "<input type=hidden name=id value=$kid>\n";
print "<input type=hidden name=name value=$tid>\n";
print "<input type=hidden name=pass value=$kpass>\n";
print "<input type=hidden name=mode value=sentaku>\n";
print "<input type=submit class=btn value=\"好きなキャラに挑戦\">\n";
	}else{print "$ztime秒後闘えるようになります。\n";}
print <<"EOM";
</td>
</table>
<table width="100%"><tr><td id="td2" align="center" class="b1">極めたジョブ</td></tr>
<tr><td colspan=3 align="center" class="b1">$kmaster</td></tr></table>
</form>
<table width="100%">
EOM

	open(IN,"$chocolog_file");
	@chocobo = <IN>;
	close(IN);

	$i=0;$hit=0;
	foreach(@chocobo){
	($cy_id,$cy_pass,$cy_kname,$cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);

	if($kid eq "$cy_id" and $kpass eq "$cy_pass") {

		$cyado_daix = int($cy_rank * $yado_dai);
		$cysp = int($cy_sp + $cy_5);
             	$cy_ritu = int(($cy_kon +  $cy_sp) / 30);
                if($cy_kati) { $critu = int(($cy_kati / $cy_total) * 100); }
		else { $critu = 0; }

		if($cy_kati >= 1000 && $critu > 90) {$crank = "ＳＳ";
		}elsif($cy_kati >= 500 && $critu > 90){$crank = "Ｓ";
		}elsif($cy_kati >= 300 && $critu > 85){$crank = "Ａ";
		}elsif($cy_kati >= 200 && $critu > 80){$crank = "Ｂ";
		}elsif($cy_kati >= 100 && $critu > 70){$crank = "Ｃ";
		}elsif($cy_kati >= 50){$crank = "Ｄ";
		}elsif($cy_kati >= 0){$crank = "Ｅ";
		}

              if($cy_money < 5000) {$cls = "新羽";
		}elsif($cy_money < 10000){$cls = "見習い";
		}elsif($cy_money < 50000){$cls = "OPEN";
		}elsif($cy_money < 100000){$cls = "グレードⅢ";
		}elsif($cy_money < 300000){$cls = "グレードⅡ";
		}elsif($cy_money < 1999999){$cls = "グレードⅠ";
		}elsif($cy_money > 2000000 or $cy_money = 2000000){$cls = "伝説クラス！";
		}

              if($cy_ritu  <= 1) {$cy_ritu   = "1";
              }elsif($cy_ritu>40){$cy_ritu = "40";
		}
 
               $money=($cy_money*100);

                if($cy_waza == 1) {$waza = "普通";
		}elsif($cy_waza== 2){$waza ="逃げ";
		}elsif($cy_waza== 0){$waza ="？？？？";
		}elsif($cy_waza== 3){$waza = "先行";
		}elsif($cy_waza== 4){$waza = "差し";
		}elsif($cy_waza== 5){$waza = "追い込み";
		}
              
              if($cy_kon<50) {$kon = "根性なしTT";
		}elsif($cy_kon<100){$kon="まだまだ根性足りない";
		}elsif($cy_kon<200){$kon = "普通のチョコボ";
		}elsif($cy_kon<300 ){$kon = "なかなかの根性";
		}elsif($cy_kon<500){$kon = "すごい根性の持ち主！";
		}elsif($cy_kon>500 or $cy_kon=500){$kon = "鬼の根性！！";
		}

             
		if($cy_life >= 99) {$csta = "満腹";
		}elsif($cy_life >= 80){$csta = "腹八分";
		}elsif($cy_life >= 60){$csta = "普通";
		}elsif($cy_life >= 40){$csta = "腹ぺこ";
		}elsif($cy_life >= 20){$csta = "飢餓";
		}elsif($cy_life >= 2){$csta = "餓死寸前";
		}

	print "<tr><td class=\"b2\"id=\"td1\"  colspan=6 align=center>チョコボセンター</td>\n";
	print "<tr><td align=\"center\" class=\"b2\"rowspan=4 colspan=2><img src=\"$img_path/$choco_img[$cy_no]\" ></td>\n";
	print "<td class=\"b1\"id=\"td2\">なまえ</td><td class=\"b2\">$cy_name</td><td class=\"b1\"id=\"td2\">ランク</td><td class=\"b2\">$crank</td>\n";
	print "<tr><td class=\"b1\"id=\"td2\">スピード</td><td class=\"b2\">$cysp</td><td class=\"b1\"id=\"td2\">スタミナ</td><td class=\"b2\">$cy_sta\/$cy_maxsta</td>\n";
       print "<tr><td class=\"b1\"id=\"td2\">脚質</td><td class=\"b2\">$waza</td><td class=\"b1\"id=\"td2\">クラス</td><td class=\"b2\">$cls</td>\n";
       print "<tr><td class=\"b1\"id=\"td2\">必殺率</td><td class=\"b2\">$cy_ritu%</td><td class=\"b1\"id=\"td2\">根性</td><td class=\"b2\">$kon</td>\n";
       print "<tr><td class=\"b1\"id=\"td2\"colspan=2 align=\"center\">じょうたい</td><td class=\"b2\" colspan=4 align=\"center\">$csta</td>\n";
       print "<tr><td class=\"b1\"id=\"td2\"colspan=2 align=\"center\">獲得本賞金</td><td class=\"b2\" colspan=4 align=\"center\">$moneyギルを獲得</td>\n";
	print "<tr><td class=\"b1\"id=\"td2\" colspan=2 align=center>\n";
	print "<form action=\"$scriptiku\" method=\"post\">\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$kpass>\n";
	print "<input type=hidden name=mode value=ikusei_shop>\n";
	print "チョコボの育成</td>\n";
	print "<td class=\"b2\"align=\"center\"colspan=4><input type=\"submit\"class=btn value=\"えさを与える\"></td>\n";
	print "<tr><td colspan=6>\n";
	print "※あなた好みのチョコボに育てましょう</td></tr>\n";
	print "</form>\n";

	print "<tr><td class=\"b1\" id=\"td2\"colspan=2 align=center>\n";
	print "<form action=\"$scriptyadoc\" method=\"post\">\n";
	print "チョコボの宿</td>\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$kpass>\n";
	print "<input type=hidden name=mode value=cyado>\n";
	print "<td class=\"b2\"align=\"center\" colspan=4><input type=\"submit\" class=btn value=\"休憩\"></td>\n";
	print "<tr><td colspan=6>\n";
	print "※<b>$cyado_daix</b>Gで疲れたチョコボを元気にさせます。</td></tr>\n";
	print "</form>\n";

	print "<tr><td class=\"b1\"id=\"td2\" colspan=2 align=center>\n";
	print "<form action=\"$scriptchor\" method=\"post\">\n";
	print "キングに挑戦</td>\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$kpass>\n";
	print "<input type=hidden name=mode value=chocobattle>\n";
	print "\n";

	if($cw_id eq "$cy_id"){ print "<td class=\"b2\" align=\"center\" colspan=4>現在チョコボキングです</td>\n";
	}elsif($ltime > $m_time or !$ktotal) {
		print "<td class=\"b2\"align=\"center\"  colspan=4><input type=\"submit\"class=btn  value=\"チョコボキングに挑戦\"></td>\n";
	}else{
		print "<td class=\"b2\"align=\"center\"  colspan=4>$mtime秒後レースできます。</td>\n";
		
}
print "</form>\n";
print "<tr><td class=\"b1\"id=\"td2\" colspan=2 align=center>\n";
	print "<form action=\"$scriptrace\" method=\"post\">\n";
	print "チョコボレース</td>\n";
        print "<td class=\"b2\"align=\"center\"  colspan=4>\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$kpass>\n";
	print "<input type=hidden name=mode value=race>\n";
	print "\n";

	if($ltime > $m_time or !$ktotal) {
print"<select name=mode>\n";
print"<option value=\"race0\">新羽戦\n";
if($cy_money > 10000){print"<option value=\"race1\">オープン戦\n";}
if($cy_money > 50000){print"<option value=\"race2\">グレードⅢ\n";}
if($cy_money > 100000){print"<option value=\"race3\">グレードⅡ\n";}
if($cy_money > 300000){print"<option value=\"race4\">グレードⅠ\n";}
if($cy_money > 2000000){print"<option value=\"race5\">伝説羽国際レース！！\n";}
print"</select>\n";
		print "<input type=\"submit\"class=btn  value=\"レースに出場\"></td>\n";
	}else{
		print "$mtime秒後レースできます。</td>\n";

}
}
}
	print <<"EOM";
</tr>
</table></form>

<td valign="top">
<table width="100%">
<tr><td id="td1" colspan="4" class="b2" align="center">お店に行く</td></tr>
<tr><td bgcolor="#cbfffe" align="center">【旅の宿】(<b>$yado_daix</b>G)</td>
<td bgcolor="#cbfffe" align="center">【武器屋】</td>
<td bgcolor="#cbfffe" align="center">【防具屋】</td>
<td bgcolor="#cbfffe" align="center">【チョコボ屋】</td></tr>
<tr><td align="center" class="b2">
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=yado>
<input type=submit class=btn value="体力を回復"></td>
<td align="center" class="b2"></form>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=item_eqq>
<input type=submit class=btn value="武器を買う"></td>
<td align="center" class="b2"></form>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid><input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=def_eqq>
<input type=submit class=btn value="防具を買う"></td>
<td align="center" class="b2"></form>
<form action="$scriptcho" method="post"><input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=choco_eqq0>
<input type=submit class=btn value="チョコボを買う"></td></form>
<tr><td bgcolor="#cbfffe" align="center">【訓練所】</td>
<td bgcolor="#cbfffe" align="center">【怪しい店】</td>
<td bgcolor="#cbfffe" align="center">【銀　行】</td>
<td bgcolor="#cbfffe" align="center">【飛空艇】</td></tr>
<tr><td align="center" class="b2">
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=kunren>
<input type=submit class=btn value="鍛えに行く"></td>
<td align="center" class="b2"></form>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=acs_eqq>
<input type=submit class=btn value="装飾店"></td>
<td align="center" class="b2"></form>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=bank_shop>
<input type=submit class=btn value="　銀行　"></td>
<td align="center" class="b2"></form>
<form action="$script_c_house" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=c_house>
<input type=submit class=btn value="飛空艇"></td>
</tr></form>
<tr><td bgcolor="#cbfffe" align="center">【記憶の教会】</td>
<td bgcolor="#cbfffe" align="center">【更新所】</td>
<td bgcolor="#cbfffe" align="center">【ステータスの変更】</td>
</tr>
<tr><td align="center" class="b2">
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=save_data>
<input type=submit class=btn value="記憶の教会">
</td><td align="center" class="b2"></form>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="画面更新">
</td><td align="center" class="b2"></form>
<form action="$scriptst" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=chara_st>
<input type=submit class=btn value="ステータスの変更">
</td></tr></table>
<table width="100%">
<tr><td id="td1" colspan="2" class="b2" align="center">冒険に出かける</td></tr>
<tr><td id="td2" class="b1"></form>
<form action="$scripta" method="post">
転職の神殿</td>
<td align="center" class="b2">
<select name=syoku>
<option value="no">選択してください
EOM

	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$i=0;$hit=0;
	foreach(@syoku){
		($a,$b,$c,$d,$e,$f,$g,$h,$k0,$k1,$k2,$k3,$k4,$k5,$k6,$k7,$k8,$k9,$k10,$k11,$k12,$k13,$k14,$k15,$k16,$k17,$k18,$k19,$k20,$k21,$k22,$k23,$k24,$k25,$k26,$k27,$k28,$k29,$k30) = split(/<>/);
		if($kn_0 >= $a and $kn_1 >= $b and $kn_2 >= $c and $kn_3 >= $d and $kn_4 >= $e and $kn_5 >= $f and $kn_6 >= $g and $klv >= $h and $ks0 >= $k0 and $ks1 >= $k1 and $ks2 >= $k2 and $ks3 >= $k3 and $ks4 >= $k4 and $ks5 >= $k5 and $ks6 >= $k6 and $ks7 >= $k7 and $ks8 >= $k8 and $ks9 >= $k9 and $ks10 >= $k10 and $ks11 >= $k11 and $ks12 >= $k12 and $ks13 >= $k13 and $ks14 >= $k14 and $ks15 >= $k15 and $ks16 >= $k16 and $ks17 >= $k17 and $ks18 >= $k18 and $ks19 >= $k19 and $ks20 >= $k20 and $ks21 >= $k21 and $ks22 >=  $k22 and $ks23 >=  $k23 and $ks24 >=  $k24 and $ks25 >=  $k25 and $ks26 >=  $k26 and $ks27 >=  $k27 and $ks28 >=  $k28 and $ks29 >=  $k29 and $ks30 >= $k30 and $ksyoku != $i) {
			print "<option value=\"$i\">$chara_syoku[$i]\n";
			$hit=1;
		}
		$i++;
	}
	print <<"EOM";
</select>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=tensyoku>
EOM

	if(!$hit) { print "現在転職できる職業はありません"; }
	else { print "<input type=submit class=btn value=\"転職する\">\n"; }
	print <<"EOM";
</td></tr><tr><td colspan=2>
※ 転職すると、現在の能\力値がランダムで下がります</td></tr>
<tr></form><td class="b1" id="td2">
<form action="$scriptm" method="post">
周辺の探索</td>
<td align="center" class="b2">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=monster>
EOM

	if(!$kmons) { print "１度チャンプに挑戦してください\n";
	}elsif($ltime >= $m_time or !$ktotal) {
		print <<"EOM";
<select name=mode>
<option value="monster0">その辺に出かける（弱い敵が出現！）
<option value="monster1">近くの洞窟（強い敵が出現！）
<option value="monster2">ダークダンジョン（かなり強い敵が出現！）
<option value="monster3">ミシディアの塔（鬼のような敵が出現！）
</select>
<input type=submit class=btn value="モンスターと闘う">
EOM
	}else{print "$mtime秒後闘えるようになります。<br>\n";}

	print <<"EOM";
</td></tr><tr><td colspan=2>
※修行の旅にいけます。</td></tr>
</form>
EOM

	if($klv%3 == 0){
	print "<tr><td class=\"b1\">\n";
	print "<form action=\"$scriptm\" method=\"post\">\n";
	print "突然の出現</td>\n";
	print "<td align=\"center\" class=\"b2\">\n";
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$kpass>\n";
	print "<input type=hidden name=mode value=genei>\n";
	print "\n";


	if(!$kmons) { print "１度チャンプに挑戦してください\n";
	}elsif($ltime >= $m_time or !$ktotal) {
	print "<input type=submit class=btn value=\"幻影の城へ\"><br>\n";

	      
            
	}else{
		print "$mtime秒後行けるようになります。<br>\n";
	}

	print "<tr><td colspan=2>\n";
	print "※財宝が眠ると言われる「幻影の城」にいけます。</td></tr>\n";
	print "</form>\n";
}

	print <<"EOM";

</td></tr>
<tr><td class="b1" id="td2">
<form action="$scriptm" method="post">
レジェンドプレイス</td>
<td align="center" class="b2">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=boss>
EOM

	if(!$kmori) { print "１度チャンプに挑戦してください\n";
	}elsif($ltime >= $m_time or !$ktotal) {
		print <<"EOM";
<select name=mode>
<option value="boss0">うわさのほこら（初心者を口を開けて・・）
EOM
if($kmoriturn>0){print "<option value=\"boss1\">古の神殿（熟練者も命を落とすという・・）\n";}
if($kmoriturn>1){print "<option value=\"boss2\">勇者の洞窟（伝説の勇者が訪れたという・・）\n";}
if($kmoriturn>2){print "<option value=\"boss3\">ガイアフォース（神のみが入ることを許されている・・）\n";}
print <<"EOM";
</select>
<input type=submit class=btn value="伝説に挑む">
EOM
	}else{print "$mtime秒後闘えるようになります。<br>\n";}

	print <<"EOM";
</td></tr><tr><td colspan=2>
※でんせつの場所へ訪れることができます。</td></tr>
</form>
<tr><td class="b1" id="td2">
<form action="$scriptm" method="post">
異世界</td><td align="center" class="b2">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=isekiai>
EOM
	if(!$kmons) { print "１度チャンプに挑戦してください\n";
	}elsif($ltime >= $m_time or !$ktotal) {
		if($klv < $isekai_lvl) {print "レベルが$isekai_lvlを超えるまで行けません。<br>\n";
		}else{print "<input type=submit class=btn value=\"異世界へ行く\"><br>\n";}
	}else{print "$mtime秒後闘えるようになります。<br>\n";}

	print <<"EOM";
</td></tr><tr><td colspan=2>※神々の領域と言われるこの世界に足をふみいれて、無事に帰ったものは誰一人いない・・・</td></tr>
<tr></form>
<td class="b1" id="td2">
<form action="$scriptb" method="post">天下一武道会</td><td align="center" class="b2">
EOM

	if(!$kmons) { print "１度チャンプに挑戦してください\n";}
	elsif($ltime > $b_time or !$ktotal) {
	&read_nuki;
		if($nuki_check){
		print <<"EOM";
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=katinuki>
<input type=hidden name=no value=1>
<input type=submit class=btn value="武道会に出場">
EOM
		}else{$sannkasu=$tenka_su-$sousu;print "あと$sannkasu人参加するまで開催されません。";}
	}else{print "$ztime秒後闘えるようになります。\n";}

		print <<"EOM";
</td></tr><tr><td colspan=2>※レベルの上位のキャラに対して勝ち抜き戦を挑みます、優勝すると賞金が貰えます。</td></tr>

</table></form></td></tr></table>
【届いているメッセージ】表\示数<b>$max_gyo</b>件まで</table>
EOM
	open(IN,"$message_file");
	@MESSAGE_LOG = <IN>;
	close(IN);

	$hit=0;$i=1;
	foreach(@MESSAGE_LOG){
		($pid,$hid,$hname,$hmessage,$hhname,$htime) = split(/<>/);
		if($kid eq "$pid"){
			# タグの排除
			$hmessage =~ s/</&lt;/g;
			$hmessage =~ s/>/&gt;/g;
			if($max_gyo < $i) { last; }
				print "<hr size=0><font color=$red><small><b>$hnameさん</b>　＞ 「<b>$hmessage</b>」($htime)</small></b></font><br>\n";
				$hit=1;$i++;
			}
		}
	if(!$hit){ print "<hr size=0>$knameさん宛てのメッセージはありません<p>\n"; }
	print "<hr size=0><p>";

	&footer;

	$chara_flag=0;

	exit;
}
__SUB__

	

	ilog_in => <<'__SUB__',

#----------------#
#  ログイン画面  #
#----------------#
sub ilog_in {
	$chara_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@log_in = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_in){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid") {
			$hit=1; last;
		}
	}
	# パスワードを照合
	$match = &decrypt("$in{'pass'}","$kpass");
	if ($match ne 'yes') {
		if($in{'pass'} ne $kpass){ &error("パスワードが違います！"); }}

	open (IN,"$winner_file") || &error('オープンエラー','指定された書込みファイルが開けません。');
	$LINE = <IN>;
	close (IN);
	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec)=split(/<>/,$LINE);

	$ltime = time();
	$ltime = $ltime - $kdate;
	$vtime = $b_time - $ltime;
	$xtime = $vtime + 1;
	$ztime = $vtime - 1;
	$mtime = $m_time - $ltime;
	if($in{'id'} ne "$kid") {&error("オープンエラー、ID・パスワードが正しくありません。");}
	$yado_daix = int($klv * $yado_dai);

	if(!$hit) { &error("入力されたIDは登録されていません。又はパスワードが違います。"); }
	if($kmori < $boss) { $kmori = 0; }

	&class;

	if($ksex) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $klv * $lv_up;

	open(IN,"$item_file");
	@log_item = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_item){
		($i_no,$i_name,$i_dmg,$i_gold) = split(/<>/);
		if($kitem eq "$i_no"){ $hit=1;last; }
	}
	if(!$hit) { $i_name="－"; }
	if(!$hit) { $i_dmg="－"; }

	open(IN,"$def_file");
	@log_def = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_def){
		($d_no,$d_name,$d_dmg,$d_gold) = split(/<>/);
		if($kdef eq "$d_no"){ $hit=1;last; }
	}
	if(!$hit) { $d_name="-"; }
	if(!$hit) { $d_dmg="-"; }

	open(IN,"$tac_file");
	@log_tac = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_tac){
		($ktac_no,$ktac_name) = split(/<>/);
		if($ktac eq "$ktac_no"){ $hit=1;last; }
	}
	if(!$hit) { $ktac_name="普通に戦う"; }

	&iheader;

	print <<"EOM";
<h1>$knameさん用画面</h1>
<HR>
<img src="$img_pathi/$chara_img[$kchara]"><br>
LV：$klv<br>
JLV：$kcllv<br>
&#63889;$khp\/$kmaxhp<br><hr>
[<a href="$script?mode=ists_win&id=$kid&pass=$kpass">&#63873;</a>
<a href="$script?mode=imsg_win&id=$kid&pass=$kpass">&#63863;</a>
<a href="$scripta?mode=ranking&first=1&end=10">&#63719;</a>
<a href="$script?mode=ihelp_win&id=$kid&pass=$kpass">？</a>]<br><hr>
<form action="$scriptm" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
EOM

	if(!$kmons) { print "[－\n";
	}elsif($ltime >= $m_time or !$ktotal) {
		print <<"EOM";
<select name=mode>
<option value="monster0">初心者の森
<option value="monster1">熟練者の森
<option value="monster2">暗黒の森
</select>
<input type=submit class=btn value="探索"></form>
EOM
	}else{print "－\n";}

	print "[\n";
	if($klv%3 == 0){
	if(!$kmons) { print "－\n";
	}elsif($ltime >= $m_time or !$ktotal) {
	print "<a href=\"$scriptm?mode=genei&id=$kid&pass=$kpass\">幻</a>\n";
	}else{print "－\n";}
	}
if($kmori < $boss) { print "－"; 
	}elsif($ltime >= $m_time or !$ktotal) {
	print "<a href=\"$scriptm?mode=boss&id=$kid&pass=$kpass\">森</a>\n";
	}else{print "－\n";}
if($klv < $isekai_lvl) { print "－"; 
	}else{print "<a href=\"$scriptm?mode=isekiai&id=$kid&pass=$kpass\">異</a>\n";}
	print <<"EOM";
<a href="$scriptb?mode=himatubusi&id=$kid&pass=$kpass">暇</a>
EOM
	&read_nuki;
	if($nuki_check){print "<a href=\"$scriptb?mode=katinuki&id=$kid&pass=$kpass&no=1\">天</a>]<br>";}
	else{print "－]<br>";}

		print <<"EOM";
<hr>[<a href="$scripts?mode=yado&id=$kid&pass=$kpass">&#63687;</a>
<a href="$scripts?mode=item_eqq&id=$kid&pass=$kpass">武</a>
<a href="$scripts?mode=def_eqq&id=$kid&pass=$kpass">防</a>
<a href="$scripts?mode=acs_eqq&id=$kid&pass=$kpass">ア</a>
<a href="$scripts?mode=kunren&id=$kid&pass=$kpass">訓</a>
<a href="$scripts?mode=save_data&id=$kid&pass=$kpass">教</a>
<a href="$scripts?mode=bank_shop&id=$kid&pass=$kpass">&#63688;</a>]<br>
<hr>
&#63904;：<b>$wname</b><font color="$red">$wcount</font>連勝中<br>
$lname の <A HREF=\"http\:\/\/$lurl\" TARGET=\"_blank\">$lsite</A> に勝利！<br>
<hr>
<form action="$scriptb" method="post">
コメント：<input type="text" name=waza value="$kwaza" size=50>
<input type="hidden" name=mode value=battle>
<input type="hidden" name=id value="$kid">
<input type="hidden" name=pass value="$kpass">
<input type="submit" value="&#63904;に挑戦">
</form>
※賞金：$wgold G
<form action="$scripta" method="post">
<input type="hidden" name=id value=$kid>
<input type="hidden" name=name value=$tid>
<input type="hidden" name=pass value=$kpass>
<input type="hidden" name=mode value=sentaku>
<input type="submit" class=btn value="選択して挑戦"></form>
EOM

	&ifooter;

	$chara_flag=0;

	exit;
}
__SUB__

	ists_win => <<'__SUB__',
#----------------#
#  ステータス画面#
#----------------#
sub ists_win {
	$chara_flag=1;

	open(IN,"./charalog/$in{'id'}.cgi");
	@log_in = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_in){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid") {
			$hit=1; last;
		}
	}
	# パスワードを照合
	$match = &decrypt("$in{'pass'}","$kpass");
	if ($match ne 'yes') {
		if($in{'pass'} ne $kpass){ &error("パスワードが違います！"); }}

	open (IN,"$winner_file") || &error('オープンエラー','指定された書込みファイルが開けません。');
	$LINE = <IN>;
	close (IN);
	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec)=split(/<>/,$LINE);

	$ltime = time();
	$ltime = $ltime - $kdate;
	$vtime = $b_time - $ltime;
	$xtime = $vtime + 1;
	$ztime = $vtime - 1;
	$mtime = $m_time - $ltime;
	if($in{'id'} ne "$kid") {&error("オープンエラー、ID・パスワードが正しくありません。");}
	$yado_daix = int($klv * $yado_dai);

	if(!$hit) { &error("入力されたIDは登録されていません。又はパスワードが違います。"); }
	if($kmori < $boss) { $kmori = 0; }

	&class;

	if($ksex) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $klv * $lv_up;

	open(IN,"$item_file");
	@log_item = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_item){
		($i_no,$i_name,$i_dmg,$i_gold,$i_plus) = split(/<>/);
		if($kitem eq "$i_no"){ $hit=1;last; }
	}
	if(!$hit) { $i_name="－"; }
	if(!$hit) { $i_dmg="－"; }

	open(IN,"$def_file");
	@log_def = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_def){
		($d_no,$d_name,$d_dmg,$d_gold,$d_plus) = split(/<>/);
		if($kdef eq "$d_no"){ $hit=1;last; }
	}
	if(!$hit) { $d_name="-"; }
	if(!$hit) { $d_dmg="-"; }

	open(IN,"$acs_file");
	@log_acs = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
		if($kacsno eq "$a_no"){ $hit=1;last; }
	}
	if(!$hit) { $a_name="-"; $a_0up=0;$a_1up=0;$a_2up=0;$a_3up=0;$a_4up=0;$a_5up=0;$a_6up=0;$a_lpup=0;$a_hitup=0;$a_kaihiup=0;$a_wazaup=0;}

	open(IN,"$tac_file");
	@log_tac = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_tac){
		($ktac_no,$ktac_name) = split(/<>/);
		if($ktac eq "$ktac_no"){ $hit=1;last; }
	}
	if(!$hit) { $ktac_name="普通に戦う"; }

	# 基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int(($kn_4 / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($kn_5/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($klp / 15)) + 10 + $kcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}
	$i_plus += $a_hitup;
	$d_plus += $a_kaihiup;

	#職歴の表示
	$kmaster = "　";
	if ($ks0){$kmaster .="$chara_syoku[0]／";}
	if ($ks1){$kmaster .="$chara_syoku[1]／";}
	if ($ks2){$kmaster .="$chara_syoku[2]／";}
	if ($ks3){$kmaster .="$chara_syoku[3]／";}
	if ($ks4){$kmaster .="$chara_syoku[4]／";}
	if ($ks5){$kmaster .="$chara_syoku[5]／";}
	if ($ks6){$kmaster .="$chara_syoku[6]／";}
	if ($ks7){$kmaster .="$chara_syoku[7]／";}
	if ($ks8){$kmaster .="$chara_syoku[8]／";}
	if ($ks9){$kmaster .="$chara_syoku[9]／";}
	if ($ks10){$kmaster .="$chara_syoku[10]／";}
	if ($ks11){$kmaster .="$chara_syoku[11]／";}
	if ($ks12){$kmaster .="$chara_syoku[12]／";}
	if ($ks13){$kmaster .="$chara_syoku[13]／";}
	if ($ks14){$kmaster .="$chara_syoku[14]／";}
	if ($ks15){$kmaster .="$chara_syoku[15]／";}
	if ($ks16){$kmaster .="$chara_syoku[16]／";}
	if ($ks17){$kmaster .="$chara_syoku[17]／";}
	if ($ks18){$kmaster .="$chara_syoku[18]／";}
	if ($ks19){$kmaster .="$chara_syoku[19]／";}
	if ($ks20){$kmaster .="$chara_syoku[20]／";}
	if ($ks21){$kmaster .="$chara_syoku[21]／";}
	if ($ks22){$kmaster .="$chara_syoku[22]／";}

	&iheader;

	print <<"EOM";
<h1>$knameさん用画面</h1>
<img src="$img_pathi/$chara_img[$kchara]"><br>
[<a href="$script?mode=ilog_in&id=$kid&pass=$kpass">&#63873;</a>
<a href="$script?mode=imsg_win&id=$kid&pass=$kpass">&#63863;</a>
<a href="$script?mode=ihelp_win&id=$kid&pass=$kpass">？</a>]<br>
<hr>
<input type="text" name=c_name value="$kname"><br>
武：$i_name<br>
防：$d_name<br>
ア：$a_name<br>
職：$chara_syoku[$ksyoku]<br>
$class<br>
LV：$klv<br>
JLV：$kcllv<br>
EX：$kex/$next_ex<br>
&#63866;：$kgold<br>
&#63889;：<br>
$khp\/$kmaxhp<br>
力：$kn_0 + $a_0up<br>
知：$kn_1 + $a_1up<br>
信：$kn_2 + $a_2up<br>
生：$kn_3 + $a_3up<br>
器：$kn_4 + $a_4up<br>
速：$kn_5 + $a_5up<br>
魅：$kn_6 + $a_6up<br>
カ：$klp + $a_lpup<br>
命：$hit_ritu + $i_plus%<br>
回：$kaihi_ritu + $d_plus%<br>
必：$waza_ritu + $a_wazaup%<br><hr>
EOM
	print <<"EOM";
<form action="$scripts" method="post">
<B>$ktac_name</B>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=tac_eqq>
<input type=submit class=btn value="戦術変更">
</form>
<form action="$scripta" method="post">
<select name=syoku>
<option value="no">職選択
EOM

	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$i=0;$hit=0;
	foreach(@syoku){
		($a,$b,$c,$d,$e,$f,$g,$h,$k0,$k1,$k2,$k3,$k4,$k5,$k6,$k7,$k8,$k9,$k10,$k11,$k12,$k13,$k14,$k15,$k16,$k17,$k18,$k19,$k20,$k21,$k22) = split(/<>/);
		if($kn_0 >= $a and $kn_1 >= $b and $kn_2 >= $c and $kn_3 >= $d and $kn_4 >= $e and $kn_5 >= $f and $kn_6 >= $g and $klv >= $h and $ks0 >= $k0 and $ks1 >= $k1 and $ks2 >= $k2 and $ks3 >= $k3 and $ks4 >= $k4 and $ks5 >= $k5 and $ks6 >= $k6 and $ks7 >= $k7 and $ks8 >= $k8 and $ks9 >= $k9 and $ks10 >= $k10 and $ks11 >= $k11 and $ks12 >= $k12 and $ks13 >= $k13 and $ks14 >= $k14 and $ks15 >= $k15 and $ks16 >= $k16 and $ks17 >= $k17 and $ks18 >= $k18 and $ks19 >= $k19 and $ks20 >= $k20 and $ks21 >= $k21 and $ks22 >= $k22 and $ksyoku != $i) {
			print "<option value=\"$i\">$chara_syoku[$i]\n";
			$hit=1;
		}
		$i++;
	}
	print <<"EOM";
</select>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=tensyoku>
EOM

	if(!$hit) { print "転職不可"; }
	else { print "<input type=submit class=btn value=\"転職\">\n"; }

	print "</form><br>";
	print <<"EOM";
極めたジョブ：$kmaster
EOM
	$chara_flag=0;

	&ifooter;

	exit;
}
__SUB__

	imsg_win => <<'__SUB__',
#----------------#
#  メッセージ画面#
#----------------#
sub imsg_win {

	&iheader;

	open(IN,"./charalog/$in{'id'}.cgi");
	@log_in = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_in){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid") {
			$hit=1; last;
		}
	}
	# パスワードを照合
	$match = &decrypt("$in{'pass'}","$kpass");
	if ($match ne 'yes') {
		if($in{'pass'} ne $kpass){ &error("パスワードが違います！"); }}

	print <<"EOM";
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=ilog_in>
<input type=submit class=btn value="&#63873;">
</form><br>
<form action="$scripta" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=name value=$kname>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=messe>
<input type=submit class=btn value="&#63858;">
</form>
【届いているメッセージ】<br>
EOM
	open(IN,"$message_file");
	@MESSAGE_LOG = <IN>;
	close(IN);

	$hit=0;$i=1;
	foreach(@MESSAGE_LOG){
		($pid,$hid,$hname,$hmessage,$hhname,$htime) = split(/<>/);
		if($kid eq "$pid"){
			# タグの排除
			$hmessage =~ s/</&lt;/g;
			$hmessage =~ s/>/&gt;/g;
			if($max_gyo < $i) { last; }
			print "<hr size=0><font color=$red><small><b>＞$hname</b>　： 「<b>$hmessage</b>」($htime)</small></b></font><br>\n";
			$hit=1;$i++;
		}elsif($kid eq "$hid"){
			print "<hr size=0><small>$kname＞$hhname　： 「$hmessage」($htime)</small><br>\n";
		}
	}
	if(!$hit){ print "<hr size=0>$knameさん宛てのメッセージはありません<p>\n"; }
	print "<hr size=0><p>";

	print <<"EOM";
<br>
EOM
	&ifooter;
	exit;
}
__SUB__

	ihelp_win => <<'__SUB__',
#----------------#
#  ヘルプ画面    #
#----------------#
sub ihelp_win {

	&iheader;

	open(IN,"./charalog/$in{'id'}.cgi");
	@log_in = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_in){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid") {
			$hit=1; last;
		}
	}
	# パスワードを照合
	$match = &decrypt("$in{'pass'}","$kpass");
	if ($match ne 'yes') {
		if($in{'pass'} ne $kpass){ &error("パスワードが違います！"); }}

	print <<"EOM";
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="&#63873;">
</form><br>
<BR>
[アイコン説明]</P>
<P>&#63868; ＩＤ<BR>
&#63869; パスワード<BR>
&#63904; チャンプ<BR>
&#63719; 登録者一覧<BR>
&#63873; ステータス<BR>
&#63889; キャラＨＰ<BR>
モ モンスター<BR>
幻 幻影の城<BR>
魔 魔の森<BR>
異 異世界<BR>
暇 暇つぶし<BR>
天 天下武道会<BR>
&#63687; 宿屋<BR>
武 武器屋<BR>
防 防具屋<BR>
ア アクセサリー屋<BR>
訓 訓練所<BR>
教 記憶の教会<BR>
&#63688; 銀行<BR>
&#63863; ﾒｯｾｰｼﾞ確認<BR>
&#63858; ﾒｯｾｰｼﾞ送信<BR>
&#63814; モンスターHP<BR>
</P>
EOM
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
if($ltime < $b_time or !$ktotal and $ztime > 0){
	print <<"EOM";
<SCRIPT LANGUAGE="JavaScript">
<!--
	var start=new Date();
	start=Date.parse(start)/1000;
	var counts=$ztime;
	function CountDown(){
		var now=new Date();
		now=Date.parse(now)/1000;
		var x=parseInt(counts-(now-start),10);
		document.form1.clock.value=x;
		if(x>0){
			setTimeout("CountDown()", 1000)
		}	}
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

	iheader => <<'__SUB__',
#------------------#
#  HTMLのヘッダー  #
#------------------#
sub iheader {
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html><head><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
EOM
	print "<link rel=\"stylesheet\" href=$style_sheet type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
}
__SUB__

	footer => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {
	
			print "<a href=\"$scripto\">TOPページへ</a>\n";

	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	 print "FFA Emilia・いく改ver1.00 remodeling by <a href=\"http://www3.big.or.jp/~icu/\" target=\"_top\">いく</a><br>\n";
	 print "画像提供 by <a href=\"http://www.wisnet.ne.jp/~jnkw/index.html\" target=\"_top\">Jinkun</a><br>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 edit by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Emilia</a><br>\n";
        
	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
if($ltime < $b_time or !$ktotal and $ztime > 0){
	print <<"EOM";
<SCRIPT language="JavaScript">
<!--
setTimeout("CountDown()",500);
//-->
</SCRIPT>
EOM
}
	print "</DIV></body></html>\n";
}
__SUB__

	ifooter => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub ifooter {
			print "<a href=\"$scripto\">TOP</a>\n";
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	decrypt => <<'__SUB__',
#----------------------#
#  パスワード照合処理  #
#----------------------#
sub decrypt {
	local($inpw, $logpw) = @_;
	local($salt, $key, $check);

	$salt = $logpw =~ /^\$1\$(.*)\$/ && $1 || substr($logpw, 0, 2);
	$check = "no";
	if (crypt($inpw, $salt) eq "$logpw" || crypt($inpw, '$1$' . $salt) eq "$logpw")
		{ $check = "yes"; }
	return $check;
}
__SUB__

	read_nuki => <<'__SUB__',
#--------------------#
#  勝ち抜き読み込み  #
#--------------------#
sub read_nuki {

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		push(@winner, <IN>);
		close(IN);
		}
	}
	closedir(DIR);

	@tmp1 = @tmp2 = ();
	foreach (@winner) {
 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
		if($first){
			if($aa ne $kid){
		 		push(@WORK, $_);
		 		push(@tmp1, $first);
				}
			}
		}
	$sousu = @WORK;
	@WORK = @WORK[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];
	$i=0;
	$imax=$tenka_su+1;
	foreach (@WORK) {
 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
		if($i==$imax or $i == $sousu){last;}
 		push(@RANK_NEW, $_);
 		push(@tmp2, $first);
		$i++;
		}
	@RANK_NEW = @RANK_NEW[sort {$tmp2[$a] <=> $tmp2[$b]} 0 .. $#tmp2];

	$sousu = @RANK_NEW -1;
	if($sousu>=$tenka_su){$nuki_check=1;}else{$nuki_check=0;}
}
__SUB__
);
}


