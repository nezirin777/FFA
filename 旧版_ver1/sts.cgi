#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権は下記の3人にあります。
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
#　http://www3.big.or.jp/~icu/
#　icus2@hotmail.com
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#     http://www3.big.or.jp/~icu/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require './jacode.pl';

# レジストライブラリの読み込み
require './regist.pl';

# レジストライブラリの読み込み
require './sankasya.pl';

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

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}

if($mode eq 'chara_st'){&chara_st;}
elsif($mode eq 'st_buy') { &st_buy; }

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
	chara_st => <<'__SUB__',
#----------------#
#  ログイン画面  #
#----------------#
sub chara_st {
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
	if($bwhit > 200){$bwhit = 100;}
	if($bwkaihi > 200){$bwkaihi = 100;}
	if($bwwaza > 200){$bwwaza = 100;}


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
        if ($ks23){$kmaster .="$chara_syoku[23]／";}
        if ($ks24){$kmaster .="$chara_syoku[24]／";}
        if ($ks25){$kmaster .="$chara_syoku[25]／";}
        if ($ks26){$kmaster .="$chara_syoku[26]／";}
        if ($ks27){$kmaster .="$chara_syoku[27]／";}
        if ($ks28){$kmaster .="$chara_syoku[28]／";}
        if ($ks29){$kmaster .="$chara_syoku[29]／";}
        if ($ks30){$kmaster .="$chara_syoku[30]／";}

	if($kgold > $gold_max){$kgold = $gold_max;}

	&header;



       print <<"EOM";
<table align="center"><TR><TD><font size=5>$knameさん用ステータス変更画面</font></TD></table>
EOM

	&guest_list;

	&guest_view;

	print <<"EOM";
<hr size=0>
<font class=white>メニュー/</font><a href="$scripta?mode=ranking&first=1&end=20">登録者一覧</a> / <a href="$scripta?mode=mori_ranking&first=1&end=20">魔の森攻略者一覧</a> / <a href="$ranking">\能\力別ランキングへ</a> / <a href="$syoku_html">各職業に必要な特性値</a> /<a href="$scripta?mode=img_list" target="_blank">$vote_gazou</a> /<a href="$bbs">$bbs_title</a> /<a href="$helptext">$helptext_url</a><br>
<font class=white>町の外れ/</font><a href="$sbbs">$sbbs_title</a> / <a href="$vote">$vote_title</a> /<br>

<form action="$scripts" method="post">
<table border=0 align="center" width='100%'>
<tr>
<td valign=top width='50%'>
<table width="100%"><tr>
<tr><td id="td1" colspan="5" class="b2" align="center">キャラクターデータ</td></tr>
<td rowspan="4" align="center" valign=bottom class="b2"><img src="$img_path/$chara_img[$kchara]">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$i_name</td>
<td id="td2" class="b1">攻撃力</td><td align="right" class="b2">$i_dmg</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$d_name</td>
<td id="td2" class="b1">防御力</td><td align="right" class="b2">$d_dmg</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$a_name</td><td id="td2" class="b2">称号</td><td align="right" class="b2"><font color=yellow>$syou</font></td></tr>
</table>

<table width="100%"><tr><td id="td2" align="center" class="b1">極めたジョブ</td></tr>
<tr><td colspan=3 align="center" class="b1">$kmaster</td></tr></table>
<table width="100%"></form>
<tr><td id="td1" colspan="5" class="b2" align="center">その他のコマンド</td></tr><tr><td id="td2"align="center" class="b2">【戦術変更】</td>
<td align="center"colspan="4" class="b2"></form>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=tac_eqq>
<input type=submit class=btn value="戦術を変更"></td></tr>
<tr><td id="td2"align="center" class="b2">【ステータス画面へ】</td>
<td align="center"colspan="4" class="b2"></form>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ"></td></tr>
<tr><td id="td2"align="center" class="b2">【メッセージを送る】</td>
<td align="center"colspan="4" class="b2"></form>
<form action="$scripta" method="post" target="_new">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=messe>
<input type=submit class=btn value="メッセージを送る"></td>
</tr></form></table>
<td valign="top">
<table width='100%'>
<form action="$scriptst" method="post">
<tr><td id="td1" colspan="5" class="b2" align="center">ホームページデータ</td></tr>
<tr><td id="td2" class="b1">ホームページ名</td></tr><tr><td colspan="4"><input type="text" name=site value="$ksite" size=50></td></tr>
<tr><td id="td2" class="b1">ホームページのURL</td></tr><tr><td colspan="4"><input type="text" name=url value="http\:\/\/$kurl" size=60></td></tr>
</table>
<table width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr>
<td class="b1" id="td2">画像設定</td><td class="b2"colspan="4"><select name="chara">
EOM

	$i=0;
	foreach(@chara_name){
		print "<option value=\"$i\">$chara_name[$i]\n";
		$i++;
	}

	print <<"EOM";
</select>　(<a href="$scripta?mode=img_list" target="_blank">キャラ画像一覧はこちら</a>）</td>
</tr></td>
<tr>
<td class="b1" id="td2">なまえ</td><td class="b2">$kname</td>
<td class="b1" id="td2">性別</td><td class="b2">$esex</td></tr>
<tr><td class="b1" id="td2">ジョブ</td><td class="b2">$chara_syoku[$ksyoku]</td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$kcllv</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$klv</td>
<td class="b1" id="td2">経験値</td><td class="b2">$kex/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$khp\/$kmaxhp</td>
<td class="b1" id="td2">お金</td><td class="b2">$kgold\/$gold_max</td></tr>
<tr><td class="b1" id="td2">力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$kn_0 + $a_0up</b></td>
<td class="b1" id="td2">魔力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$kn_1 + $a_1up</b></td></tr>
<tr><td class="b1" id="td2">信仰心</td><td align="left" class="b2"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$kn_2 + $a_2up</b></td>
<td class="b1" id="td2">生命力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$kn_3 + $a_3up</b></td></tr>
<tr><td class="b1" id="td2">器用さ</td><td align="left" class="b2"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$kn_4 + $a_4up</b></td>
<td class="b1" id="td2">速さ</td><td align="left" class="b2"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$kn_5 + $a_5up</b></td></tr>
<tr><td class="b1" id="td2">魅力</td><td align="left" class="b2"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$kn_6 + $a_6up</b></td>
<td class="b1" id="td2">カルマ</td><td align="left" class="b2"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$klp + $a_lpup</b></td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $i_plus%</b></td>
<td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu + $d_plus%</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $a_wazaup%</b></td><td id="td2" class="b2">技名</td><td align="center" class="b2"><B>$ktac_name</B></td></tr>
<tr><td class="b1" id="td2">技発動時コメント</td><td colspan="3" align="center" class="b2"><input type="text" name=waza value="$kwaza" size=50></td></tr>
<tr><td id="td2" class="b1">

変更したステータスを登録><td align="center" colspan=3 class="b2">
<input type=hidden name=id value=$kid>
<input type=hidden name=name value=$kname>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=st_buy>
<input type=submit class=btn value="ステータスを登録する"></td></tr>
</table></form>

</table></form></td></tr></table>
【届いているメッセージ】表\示数<b>$max_gyo</b>件まで
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




	st_buy => <<'__SUB__',
#----------------#
#  変更登録画面  #
#----------------#
sub st_buy {
	if($in{'site'}eq""){ &error("ホームページ名が未記入です"); }
       elsif($in{'url'} eq "") { &error("URLが未記入です"); }
       elsif($in{'id'} eq test){ &error("テストキャラはステータス変更はできません"); }
       $kchara=$in{'chara'};
       $kurl=$in{'url'};
       $ksite=$in{'site'};
       $kwaza=$in{'waza'};

&get_host;

$date = time();

# ファイルロック
if ($lockkey == 1) { &lock1; }
elsif ($lockkey == 2) { &lock2; }

open(IN,"./charalog/$in{'id'}.cgi");
@item_chara = <IN>;
close(IN);


$hit=0;@item_new=();
foreach(@item_chara){
($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
if($iid eq "$in{'id'}") {$isite=$ksite;
$iurl=$kurl;
$ichara=$kchara;
$iwaza=$kwaza;

unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
$hit=1;
}else{
push(@item_new,"$_");
}
}

if(!$hit) { &error("キャラクターが見つかりません"); }

open(OUT,">./charalog/$in{'id'}.cgi");
print OUT @item_new;
close(OUT);

# ロック解除
if (-e $lockfile) { unlink($lockfile); }


&header;

 print <<"EOM";
<h1>$inameさんのステータスを変更しました</h1><br><br>
<form action="$scriptst" method="post">
<input type=hidden name=id value=$in{'id'}>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=chara_st>
<input type=submit class=btn value="ステータス変更画面へ">
</form>
EOM

	&footer;

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



	footer => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {

			print "<a href=\"$scripto\">TOPページへ</a>\n";

	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";

	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
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


);
}
