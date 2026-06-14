#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はT.CUMROさんにあります。
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
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　　　　　　　　　　　#
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
if($mode eq 'ichara_make') { &ichara_make; }
elsif($mode eq 'chara_make') { &chara_make; }
elsif($mode eq 'imake_end') { &imake_end; }
elsif($mode eq 'regist') { &regist; }
elsif($mode eq 'make_end') { &make_end; }
elsif($mode eq 'tensyoku') { &tensyoku; }
elsif($mode eq 'ranking') { &ranking;}
elsif($mode eq 'mori_ranking') { &ranking;}
elsif($mode eq 'message') { &message; }
elsif($mode eq 'chara_sts') { &chara_sts;}
elsif($mode eq 'chara_st') { &chara_st;}
elsif($mode eq 'img_reflist') { &img_reflist;}
elsif($mode eq 'img_list') { &img_list;}
elsif($mode eq 'messe') { &messe; }
elsif($mode eq 'sentaku') { &sentaku; }

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

	ranking => <<'__SUB__',
#------------------#
#  ランキング画面  #
#------------------#
sub ranking {

	$ifr = $in{'first'};
	$ito = $in{'end'};

# キャラデータ読み込み
opendir(DIR,'./charalog') or die "$!";
foreach $entry (readdir(DIR)){

if($entry=~/\.cgi/){
open(IN,"./charalog/$entry");
@WORK=<IN>;
if($WORK[0] ne ""){
push(@RANKING, @WORK[0]);
}close(IN);
		}
	}
	closedir(DIR);
	
	if($mode eq 'ranking') {
		@tmp1 = @tmp2 = ();
		foreach (@RANKING) {
	 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
			if($first){
		 		push(@RANK_NEW, $_);
		 		push(@tmp1, $first);
		 		push(@tmp2, $second);
				}
			}
		@RANK_NEW = @RANK_NEW[sort {$tmp1[$b] <=> $tmp1[$a] or
				$tmp2[$b] <=> $tmp2[$a]} 0 .. $#tmp1];
		$ima = time();
		#機種判定
		$agent = $ENV{'HTTP_USER_AGENT'};
		($browser,$version,$model) = split(/\//,$agent);
		if ($browser eq "DoCoMo") {&iheader;}
		else{&header;}

		$sousu = @RANK_NEW;

	print <<"EOM";
<h1>登録者一覧</h1><hr size=0>
<br>現在の登録者数<b>$sousu</b>人<br>
現在登録されているキャラクターの中で、レベル上位<b>$ifr</b>人目から<b>$ito</b>人目を表\示しています。<br>
※名前をクリックすると詳細情報がご覧になれます♪<br>
EOM

	}elsif($mode eq 'mori_ranking') {
		@tmp1 = @tmp2 = ();
		foreach (@RANKING) {
			my ($sid,$spass,$ssite,$surl,$sname,$ssex,$schara,$sn_0,$sn_1,$sn_2,$sn_3,$sn_4,$sn_5,$sn_6,$ssyoku,$shp,$smaxhp,$sex,$slv,$sgold,$slp,$second,$skati,$swaza,$sitem,$smons,$shost,$sdate,$smori,$sdef,$stac,$sacsno,$first) = split(/<>/);
			if($first >= 1){
		 		push(@RANK_NEW, $_);
		 		push(@tmp1, $first);
		 		push(@tmp2, $second);
				}
			}
		@RANK_NEW = @RANK_NEW[sort {$tmp1[$b] <=> $tmp1[$a] or
				$tmp2[$b] <=> $tmp2[$a]} 0 .. $#tmp1];
		$ima = time();
		#機種判定
		$agent = $ENV{'HTTP_USER_AGENT'};
		($browser,$version,$model) = split(/\//,$agent);
		if ($browser eq "DoCoMo") {&iheader;}
		else{&header;}

	$sousu = @RANK_NEW;

	print <<"EOM";
<h1>称号獲得者一覧</h1><hr size=0>
<br>現在の獲得者数<b>$sousu</b>人<br>
称号を獲得したキャラクターの中で、<b>$ifr</b>人目から<b>$ito</b>人目を表\示しています。<br>
※名前をクリックすると詳細情報がご覧になれます♪<br>
EOM
	}

	print "<a href=\"$scripto\">TOPページへ</a>\n";
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser ne "DoCoMo") {print "<table><tr></tr>";}

	$i=1;
	foreach(@RANK_NEW){
		($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$rdate,$rmori,$rdef,$rtac,$racsno,$rmoriturn,$rcllv) = split(/<>/);
		if($i > $ito){ last; }
		$rdate = $rdate + (60*60*24*$limit);
		$niti = $rdate - $ima;
		$niti = int($niti / (60*60*24));
		$rritu = int(($rkati / $rtotal) * 100);
		if($i >= $ifr){
	# 最大値の設定
	if($rmaxhp > $charamaxhp){$rmaxhp = $charamaxhp}
	if($rn_0 > $charamaxpm){$rn_0 = $charamaxpm;}
	if($rn_1 > $charamaxpm){$rn_1 = $charamaxpm;}
	if($rn_2 > $charamaxpm){$rn_2 = $charamaxpm;}
	if($rn_3 > $charamaxpm){$rn_3 = $charamaxpm;}
	if($rn_4 > $charamaxpm){$rn_4 = $charamaxpm;}
	if($rn_5 > $charamaxpm){$rn_5 = $charamaxpm;}
	if($rn_6 > $charamaxpm){$rn_6 = $charamaxpm;}
	if($rlp  > $charamaxpm){$rlp  = $charamaxpm;}
       
	# 基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int(($rn_4 / 10)+51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($rn_5 / 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($rlp / 15)) + 10 + $rcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}

	# 能力値バーの詳しい幅設定
	$bw0     = int(0.5 * ($rn_0 / $divpm));
	$bw1     = int(0.5 * ($rn_1 / $divpm));
	$bw2     = int(0.5 * ($rn_2 / $divpm));
	$bw3     = int(0.5 * ($rn_3 / $divpm));
	$bw4     = int(0.5 * ($rn_4 / $divpm));
	$bw5     = int(0.5 * ($rn_5 / $divpm));
	$bw6     = int(0.5 * ($rn_6 / $divpm));
	$bwlp    = int(0.5 * ($rlp / $divpm));
	$bwhit   = int(0.5 * $hit_ritu);
	$bwkaihi = int(0.5 * $kaihi_ritu);
	$bwwaza  = int(1 * $waza_ritu);
	if($bwhit > 100){$bwhit = 100;}
	if($bwkaihi > 100){$bwkaihi = 100;}
	if($bwwaza > 100){$bwwaza = 100;}

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
			print "$i：<a href=\"$scripta?mode=chara_sts&id=$rid\">$rname</a>／$chara_syoku[$rsyoku]／<a href=\"http\:\/\/$rurl\">$rsite</a><br>\n";
	}else{
		print "<tr>\n";
	print <<"EOM";
<td id="td1" align="center">$i</td>
<td><table border="1"><tr>
<td rowspan="3"><img src="$img_path/$chara_img[$rchara]"></td>
</tr><tr>
<td id="td2" align="center" width="50">サイト</td>
<td align="center" width="100"><a href=\"http\:\/\/$rurl\">$rsite</a></td>
<td id="td2" align="center" width="50">力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw0 height=$bh><br><b>$rn_0</b></td>
<td id="td2" align="center" width="50">魔力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw1 height=$bh><br><b>$rn_1</b></td>
<td id="td2" align="center" width="50">信仰心</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw2 height=$bh><br><b>$rn_2</b></td>
<td id="td2" align="center" width="50">生命力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw3 height=$bh><br><b>$rn_3</b></td>
<td id="td2" align="center">レベル</td>
<td align="center">$rlv</td>
</tr><tr>
<td id="td2" align="center" width="50">HP</td>
<td align="center" width="100">$rmaxhp</td>
<td id="td2" align="center" width="50">器用さ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw4 height=$bh><br><b>$rn_4</b></td>
<td id="td2" align="center" width="50">速さ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw5 height=$bh><br><b>$rn_5</b></td>
<td id="td2" align="center" width="50">魅力</td>
<td align="left" width="100"><img src=\"$bar\" width=$bw6 height=$bh><br><b>$rn_6</b></td>
<td id="td2" align="center" width="50">カルマ</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwlp height=$bh><br><b>$rlp</b></td>
<td id="td2" align="center">勝率</td>
<td align="center">$rritu%</td>
</tr><tr>
<td><a href="$scripta?mode=chara_sts&id=$rid">$rname</a></td>
<td id="td2" align="center" width="50">職業</td>
<td align="center" width="100">$chara_syoku[$rsyoku]</td>
<td id="td2" align="center" width="50">命中率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu%</b></td>
<td id="td2" class="b2" width="80">回避率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwkaihi height=$bh><b><br>$kaihi_ritu%</b></td>
<td id="td2" align="center" width="50">必殺率</td>
<td align="left" width="100"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu%</b></td>
EOM

	if($mode eq 'mori_ranking') {
if($rmoriturn==1){$syou ="冒険者";}
if($rmoriturn==2){$syou ="熟練者";}
if($rmoriturn==3){$syou ="勇者";}
if($rmoriturn==4){$syou ="伝説の覇者";}
print <<"EOM";
<td id="td2" align="center" width="50">獲得称号</td>
<td align="center" width="100">$syou</td>
EOM
	}else{
	print <<"EOM";
<td id="td2" align="center" width="50">戦闘回数</td>
<td align="center" width="100">$rtotal回</td>
EOM
	}
	print <<"EOM";
<td id="td2" align="center">削除まで</td>
<td align="center">残$niti日</td>
</tr></table>
EOM
		print "</tr>\n";
			}
		}
		$i++;
	}

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
		$prevfr = $ifr-10;
		$prevto = $ito-10;
		$ifr += 10;
		$ito += 10;
		$nextlimit = $sousu + 20;
	}else{
		print "</table><p>\n";
		$prevfr = $ifr-20;
		$prevto = $ito-20;
		$ifr += 20;
		$ito += 20;
		$nextlimit = $sousu + 20;
	}
	if($ito > $sousu){$ito = $sousu;}

	if($mode eq 'ranking') {
		if ($prevfr > 0){print "<br><a href=\"$scripta?mode=ranking&first=$prevfr&end=$prevto\">前の 20 件</a> ／";}
		if ($ito < $nextlimit){print "<a href=\"$scripta?mode=ranking&first=$ifr&end=$ito\">次の 20 件</a>\n";}
	}elsif($mode eq 'mori_ranking') {
		if ($prevfr > 0){print "<br><a href=\"$scripta?mode=mori_ranking&first=$prevfr&end=$prevto\">前の 20 件</a> ／";}
		if ($ito < $nextlimit){print "<a href=\"$scripta?mode=mori_ranking&first=$ifr&end=$ito\">次の 20 件</a>\n";}
	}

	exit;
}
__SUB__

	chara_make => <<'__SUB__',
#----------------------#
#  キャラクタ作成画面  #
#----------------------#
sub chara_make {
	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>キャラクタ作成画面</h1>
<hr size=0>
<form action="$scripta" method="post">
<input type="hidden" name="mode" value="make_end">
<table border=1>
<tr>
<td class="b1" colspan="2">
・キャラクターの登録は<b>一人１キャラ</b>でお願いします。二人以上登録されていることが分かった場合は、<b>警告無く削除</b>させていただきます。<br>
・嫌がらせメッセージや、不正行為が発覚した場合は、<b>警告なくキャラクターを削除</b>させていただきます。<br>
・消失したログの復元はしません。記憶の教会でまめにバックアップをとっておいてください。<br>
・更新ボタン連打や、複数のウインドウでのプレイ、各種<b>ボタン連打はキャラログ消失の原因</b>となりますので<b>絶対に止めてください。</b><br>
・サーバーの負荷が大きくなると、サーバー管理者に削除されてしまうかもしれないので、更新ボタン連打は<b>絶対に止めてください。</b><br>
・本ゲームをプレイしてのトラブル・損害などに関しましては、<b>管理者は一切の責任を負いません。</b><br>
以上を良くご了承の上で登録してください。</font>
</td>
</tr>
<tr>
<td class="b1">ID</td>
<td><input type="text" name="id" size="10"><br>△お好きな半角英数字を4～8文字以内でご記入ください。</td>
</tr>
<tr>
<td class="b1">パスワード</td>
<td><input type="password" name="pass" size="10"><br>△お好きな半角英数字を4～8文字以内でご記入ください。</td>
</tr>
<tr>
<td class="b1">ホームページ名</td>
<td><input type="text" name="site" size="40"><br>△あなたのホームページの名前を入力してください。（ない場合はオススメＨＰ）</td>
</tr>
<tr>
<td class="b1">URL</td>
<td><input type="text" name="url" size="50" value="http://"><br>△あなたのホームページのアドレスを記入してください。（ない場合はオススメＨＰ）</td>
</tr>
<tr>
<td class="b1">キャラクターの名前</td>
<td><input type="text" name="c_name" size="30"><br>△作成するキャラクターの名前を入力してください。</td>
</tr>
<tr>
<td class="b1">キャラクターの性別</td>
<td><input type="radio" name="sex" value="0">女　<input type="radio" name="sex" value="1">男<br>△作成するキャラクターの性別を選択してください。</td>
</tr>
<tr>
<td class="b1">キャラクターのイメージ</td>
<td><select name="chara">
EOM

	$i=0;
	foreach(@chara_name){
		print "<option value=\"$i\">$chara_name[$i]\n";
		$i++;
	}

	print <<"EOM";
</select><br>△作成するキャラクターの画像を選択してください。　　(<a href="$scripta?mode=img_list" target="_blank">キャラ画像一覧はこちら</a>）</td>
</tr>
<tr>
<td class="b1">キャラクターの能\力</td>
<td>
	<table border=1>
	<tr>
	<td class="b2" width="70">力</td><td class="b2" width="70">魔力</td><td class="b2" width="70">信仰心</td><td class="b2" width="70">生命力</td><td class="b2" width="70">器用さ</td><td class="b2" width="70">速さ</td><td class="b2" width="70">魅力</td>
	</tr>
	<tr>
EOM

	$point = int(rand(10));
	$point+=4;

	$i=0;$j=0;
	foreach(0..6){
		print "<td>$kiso_nouryoku[$i] + <select name=n_$i>\n";
		foreach(0..$point){
			print "<option value=\"$j\">$j\n";
			$j++;
		}
		print "</select>\n";
		print "</td>\n";
		$i++;$j=0;
	}

	print <<"EOM";
	</tr>
	</table>
△ボーナスポイント「<b>$point</b>」をそれぞれに振り分けてください。(振り分けた合計が、$point以下になるように。<br>又どれかが最低12以上になるように。最高は18までです)
</td>
</tr>
<tr>
<td colspan="2" align="center"><input type="submit" class="btn" value="これで登録"></td>
</tr>
</table>
<input type="hidden" name=point value="$point">
</form>
EOM

	# フッター表示
	&footer;

	exit;
}
__SUB__

	make_end => <<'__SUB__',
#----------------#
#  登録完了画面  #
#----------------#
sub make_end {
	if($chara_stop){ &error("現在キャラクターの作成登録はできません"); }
	if ($in{'id'} =~ m/[^0-9a-zA-Z]/)
	{&error("IDに半角英数字以外の文字が含まれています。"); }
	if ($in{'pass'} =~ m/[^0-9a-zA-Z]/)
	{&error("パスワードに半角英数字以外の文字が含まれています。"); }
	# 職業未選択の場合
		if($in{'syoku'} eq "") {
		if($in{'id'} eq "" or length($in{'id'}) < 4 or length($in{'id'}) > 8) { &error("IDは、4文字以上、8文字以下で入力して下さい。"); }
		elsif($in{'pass'} eq "" or length($in{'pass'}) < 4 or length($in{'pass'}) > 8) { &error("パスワードは、4文字以上、8文字以下で入力して下さい。"); }
		elsif($in{'site'} eq "") { &error("ホームページ名が未記入です"); }
		elsif($in{'url'} eq "") { &error("URLが未記入です"); }
		elsif($in{'c_name'} eq "") { &error("キャラクターの名前が未記入です"); }
		elsif($in{'sex'} eq "") { &error("性別が選択されていません"); }

		$g = $in{'n_0'} + $in{'n_1'} + $in{'n_2'} + $in{'n_3'} + $in{'n_4'} + $in{'n_5'} + $in{'n_6'};

		if($g > $in{'point'}) { &error("ポイントの振り分けが多すぎます。振り分けの合計を、$in{'point'}以下にしてください。"); }

		&header;

		print "<h1>職業選択画面</h1><hr size=0>\n";
		print "あなたがなることができる職業は以下のとおりです。<p>\n";
		print "<form action=\"$scripta\" method=\"post\">\n";
		print "<input type=hidden name=mode value=regist>\n";
		print "<select name=syoku>\n";
		print "<option value=0>$chara_syoku[0]\n";

		open(IN,"$syoku_file");
		@syoku = <IN>;
		close(IN);

	$i=0;$hit=0;
	foreach(@syoku){
		($a,$b,$c,$d,$e,$f,$g,$h) = split(/<>/);
		if($in{'n_0'} + $kiso_nouryoku[0] >= $a and $in{'n_1'} + $kiso_nouryoku[1] >= $b and $in{'n_2'} + $kiso_nouryoku[2] >= $c and $in{'n_3'} + $kiso_nouryoku[3] >= $d and $in{'n_4'} + $kiso_nouryoku[4] >= $e and $in{'n_5'} + $kiso_nouryoku[5] >= $f and $in{'n_6'} + $kiso_nouryoku[6] >= $g and $ksyoku != $i) {
			print "<option value=\"$i\">$chara_syoku[$i]\n";
			$hit=1;
		}
		$i++;
	}

		print "</select>\n";
		print "<input type=hidden name=new value=new>\n";
		print "<input type=hidden name=id value=\"$in{'id'}\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=site value=\"$in{'site'}\">\n";
		print "<input type=hidden name=url value=\"$in{'url'}\">\n";
		print "<input type=hidden name=c_name value=\"$in{'c_name'}\">\n";
		print "<input type=hidden name=sex value=\"$in{'sex'}\">\n";
		print "<input type=hidden name=chara value=\"$in{'chara'}\">\n";
		print "<input type=hidden name=n_0 value=\"$in{'n_0'}\">\n";
		print "<input type=hidden name=n_1 value=\"$in{'n_1'}\">\n";
		print "<input type=hidden name=n_2 value=\"$in{'n_2'}\">\n";
		print "<input type=hidden name=n_3 value=\"$in{'n_3'}\">\n";
		print "<input type=hidden name=n_4 value=\"$in{'n_4'}\">\n";
		print "<input type=hidden name=n_5 value=\"$in{'n_5'}\">\n";
		print "<input type=hidden name=n_6 value=\"$in{'n_6'}\">\n";
		print "<input type=submit class=btn value=\"この職業でOK\"></form>\n";

		&footer;

		exit;
	}else{
		if($in{'sex'}) { $esex = "男"; } else { $esex = "女"; }
		$next_ex = $lv * $lv_up;

		&header;

		print <<"EOM";
<h1>登録完了画面</h1>
以下の内容で登録が完了しました。
<hr size=0>
<p>
<table border=1>
<tr>
<td class="b1">ホームページ</td>
<td colspan="4"><a href="http\:\/\/$in{'url'}">$in{'site'}</a></td>
</tr>
<tr>
<td rowspan="8" align="center"><img src="$img_path/$chara_img[$in{'chara'}]"></td>
<td class="b1">なまえ</td>
<td>$in{'c_name'}</td>
<td class="b1">性別</td>
<td>$esex</td>
</tr>
<tr>
<td class="b1">職業</td>
<td>$chara_syoku[$in{'syoku'}]</td>
<td class="b1">お金</td>
<td>$gold</td>
</tr>
<tr>
<td class="b1">レベル</td>
<td>$lv</td>
<td class="b1">経験値</td>
<td>$ex/$next_ex</td>
</tr>
<tr>
<td class="b1">HP</td>
<td>$hp</td>
<td class="b1"></td>
<td></td>
</tr>
<tr>
<td class="b1">力</td>
<td>$n_0</td>
<td class="b1">魔力</td>
<td>$n_1</td>
</tr>
<tr>
<td class="b1">信仰心</td>
<td>$n_2</td>
<td class="b1">生命力</td>
<td>$n_3</td>
</tr>
<tr>
<td class="b1">器用さ</td>
<td>$n_4</td>
<td class="b1">速さ</td>
<td>$n_5</td>
</tr>
<tr>
<td class="b1">魅力</td>
<td>$n_6</td>
<td class="b1">カルマ</td>
<td>$lp</td>
</tr>
</table>
<form action="$script" method="post">
<input type="hidden" name=mode value=log_in>
<input type="hidden" name=id value="$in{'id'}">
<input type="hidden" name=pass value="$in{'pass'}">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

		&footer;

		exit;
	}
}
__SUB__

	message => <<'__SUB__',
#--------------#
#  メッセージ  #
#--------------#
sub message {
	if($in{'mes'} eq "") { &error("メッセージが記入されていません"); }
	if($in{'mesid'} eq "" && $in{'mesname'} eq "") { &error("相手が指定されていません"); }
	if($in{'id'} eq "test"){&error("テストキャラではメッセージを送信できません！"); }

	&get_time;

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"$message_file");
	@mes_regist = <IN>;
	close(IN);

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		@WORK=<IN>;
		if($WORK[0] ne ""){
		push(@MESSAGE,"@WORK");
		}close(IN);
	}

	}
	closedir(DIR);

	foreach(@MESSAGE) {
		($did,$dpass,$dsite,$durl,$dname) = split(/<>/);
		if($in{'mesid'} eq "$did" || $in{'mesname'} eq "$dname") { $hit=1;last; }
	}

	$mes_max = @mes_regist;

	if($mes_max > $max) { pop(@mes_regist); }

	unshift(@mes_regist,"$did<>$in{'id'}<>$in{'name'}<>$in{'mes'}<>$dname<>$gettime<>\n");

	open(OUT,">$message_file");
	print OUT @mes_regist;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	&header;
	print <<"EOM";
<h1>$dnameさんへメッセージを送りました。</h1>
<hr size=0>
<form action="$scripta" method="post">
<input type=hidden name=mode value=messe>
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=submit class=btn value="&#63873;">
</form>
EOM
	}else{
	&header;
	print <<"EOM";
<h1>$dnameさんへメッセージを送りました。</h1>
<hr size=0>
<form action="$scripta" method="post">
<input type=hidden name=mode value=messe>
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=submit class=btn value="メッセージ画面へ戻る">
</form>
EOM
	}
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {print "<a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>/\n";&footer;}
	else{print "</body></html>\n";}

	exit;
}
__SUB__

	tensyoku => <<'__SUB__',
#--------#
#  転職  #
#--------#
sub tensyoku {
	if($in{'syoku'} eq 'no') { &error("職業を選択してください。"); }
	$syoku = $in{'syoku'};
	$id = $in{'id'};

	&get_host;

	$date = time();

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi");
	@tensyoku = <IN>;
	close(IN);

	open(IN,"$syoku_file");
	@syokudate = <IN>;
	close(IN);

	($a,$b,$c,$d,$e,$f,$g) = split(/<>/,$syokudate[$in{'syoku'}]);

	if(!$a) { $a = $kiso_nouryoku[0]; }
	if(!$b) { $b = $kiso_nouryoku[1]; }
	if(!$c) { $c = $kiso_nouryoku[2]; }
	if(!$d) { $d = $kiso_nouryoku[3]; }
	if(!$e) { $e = $kiso_nouryoku[4]; }
	if(!$f) { $f = $kiso_nouryoku[5]; }
	if(!$g) { $g = $kiso_nouryoku[6]; }

	$ex = 0;

	@ten_new = ();
	foreach(@tensyoku) {
		($tid,$tpass,$tsite,$turl,$tname,$tsex,$tchara,$tn_0,$tn_1,$tn_2,$tn_3,$tn_4,$tn_5,$tn_6,$tsyoku,$thp,$tmaxhp,$tex,$tlv,$tgold,$tlp,$ttotal,$tkati,$twaza,$titem,$tmons,$thost,$tdate,$tmori,$tdef,$ttac,$tacsno,$tmoriturn,$tcllv,$ts0,$ts1,$ts2,$ts3,$ts4,$ts5,$ts6,$ts7,$ts8,$ts9,$ts10,$ts11,$ts12,$ts13,$ts14,$ts15,$ts16,$ts17,$ts18,$ts19,$ts20,$ts21,$ts22,$ts23,$ts24,$ts25,$ts26,$ts27,$ts28,$ts29,$ts30,$trec) = split(/<>/);
	$tn_0 = int($tn_0) - int($tn_0 / 10);
	$tn_1 = int($tn_1) - int($tn_1 / 10);
	$tn_2 = int($tn_2) - int($tn_2 / 10);
	$tn_3 = int($tn_3) - int($tn_3 / 10);
	$tn_4 = int($tn_4) - int($tn_4 / 10);
	$tn_5 = int($tn_5) - int($tn_5 / 10);
	$tn_6 = int($tn_6) - int($tn_6 / 10);
	$tlp = int($tlp) - int($tn_0 / 5);
	if($tn_0 < 9) { $tn_0 = 9; }
	if($tn_1 < 8) { $tn_1 = 8; }
	if($tn_2 < 8) { $tn_2 = 8; }
	if($tn_3 < 9) { $tn_3 = 9; }
	if($tn_4 < 9) { $tn_4 = 9; }
	if($tn_5 < 8) { $tn_5 = 8; }
	if($tn_6 < 8) { $tn_6 = 8; }
	if($tlp  < 0) { $tlp = 1; }
		if($id eq $tid) {
			unshift(@ten_new,"$tid<>$tpass<>$tsite<>$turl<>$tname<>$tsex<>$tchara<>$tn_0<>$tn_1<>$tn_2<>$tn_3<>$tn_4<>$tn_5<>$tn_6<>$syoku<>$thp<>$tmaxhp<>$ex<>$tlv<>$tgold<>$tlp<>$ttotal<>$tkati<>$twaza<>$titem<>$tmons<>$host<>$date<>$tmori<>$tdef<>0<>$tacsno<>$tmoriturn<>1<>$ts0<>$ts1<>$ts2<>$ts3<>$ts4<>$ts5<>$ts6<>$ts7<>$ts8<>$ts9<>$ts10<>$ts11<>$ts12<>$ts13<>$ts14<>$ts15<>$ts16<>$ts17<>$ts18<>$ts19<>$ts20<>$ts21<>$ts22<>$ts23<>$ts24<>$ts25<>$ts26<>$ts27<>$ts28<>$ts29<>$ts30<>$trec<>\n");
		}else{
			push(@ten_new,"$_");
		}
	}

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @ten_new;
	close(IN);

	&read_winner;

	if($id eq $wid) {
		open(OUT,">$winner_file");
		print OUT "$wid<>$wpass<>$wsite<>$wurl<>$wname<>$wsex<>$wchara<>$tn_0<>$tn_1<>$tn_2<>$tn_3<>$tn_4<>$tn_5<>$tn_6<>$syoku<>$wmaxhp<>$wmaxhp<>$ex<>$tlv<>$wgold<>$wlp<>$wtotal<>$wkati<>$wwaza<>$witem<>$wmons<>$host<>$date<>$wcount<>$lsite<>$lurl<>$lname<>$wmori<>$wdef<>$wtac<>$wacsno<>$wmoriturn<>1<>$ts0<>$ts1<>$ts2<>$ts3<>$ts4<>$ts5<>$ts6<>$ts7<>$ts8<>$ts9<>$ts10<>$ts11<>$ts12<>$ts13<>$ts14<>$ts15<>$ts16<>$ts17<>$ts18<>$ts19<>$ts20<>$ts21<>$ts22<>$ts23<>$ts24<>$ts25<>$ts26<>$ts27<>$ts28<>$ts29<>$ts30<>$wrec<>\n";
		close(OUT);
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>転職しました</h1><hr size=0>
<p>
<form action="$script" method="post">
<input type="hidden" name=id value="$in{'id'}">
<input type="hidden" name=pass value="$in{'pass'}">
<input type="hidden" name=mode value=log_in>
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	ichara_make => <<'__SUB__',
#----------------------#
#  キャラクタ作成画面  #
#----------------------#
sub ichara_make {
	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>キャラ登録画面</h1>
<hr size=0>
<form action="$scripta" method="post">
<input type="hidden" name="mode" value="imake_end">
&#63868;<input type="text" name="id" size="10"><br>
△半角英数字を4～8文字以内<br>
&#63869;<input type="password" name="pass" size="10"><br>
△半角英数字を4～8文字以内<br>
HP<input type="text" name="site" size="40"><br>
△ホームページ名<br>
&#7197;<input type="text" name="url" size="50" value="http://"><br>
△HPアドレス<br>
名前<input type="text" name="c_name" size="30"><br>
△キャラの名前<br>
性別<input type="radio" name="sex" value="0">
女<input type="radio" name="sex" value="1">男<br>
<select name="chara">
EOM

	$i=0;
	foreach(@chara_name){
		print "<option value=\"$i\">$chara_name[$i]\n";
		$i++;
	}

	print <<"EOM";
</select><br>
△キャラ画像<br><hr>
<a href=\"$scripta?mode=img_reflist\">キャラ画像参照</a>
キャラ能\力
EOM

	$point = int(rand(10));
	$point+=4;

	$i=0;$j=0;
	foreach(0..6){
		if($i==0)   {print "<br>力$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		elsif($i==1){print "<br>知$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		elsif($i==2){print "<br>信$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		elsif($i==3){print "<br>生$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		elsif($i==4){print "<br>器$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		elsif($i==5){print "<br>速$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		elsif($i==6){print "<br>魅$kiso_nouryoku[$i] + <select name=n_$i>\n";}
		foreach(0..$point){
			print "<option value=\"$j\">$j\n";
			$j++;
		}
		print "</select>\n";
		$i++;$j=0;
	}

	print <<"EOM";
<br>△ボーナスポイント「<b>$point</b>」最低12以上最高18<br><hr>
<input type="submit" class="btn" value="これで登録">
<input type="hidden" name=point value="$point">
</form>
EOM

	# フッター表示
	&ifooter;

	exit;
}
__SUB__

	imake_end => <<'__SUB__',
#----------------#
#  登録完了画面  #
#----------------#
sub imake_end {
	if($chara_stop){ &error("現在キャラクターの作成登録はできません"); }
	if ($in{'id'} =~ m/[^0-9a-zA-Z]/)
	{&error("IDに半角英数字以外の文字が含まれています。"); }
	if ($in{'pass'} =~ m/[^0-9a-zA-Z]/)
	{&error("パスワードに半角英数字以外の文字が含まれています。"); }
	# 職業未選択の場合
		if($in{'syoku'} eq "") {
		if($in{'id'} eq "" or length($in{'id'}) < 4 or length($in{'id'}) > 8) { &error("IDは、4文字以上、8文字以下で入力して下さい。"); }
		elsif($in{'pass'} eq "" or length($in{'pass'}) < 4 or length($in{'pass'}) > 8) { &error("パスワードは、4文字以上、8文字以下で入力して下さい。"); }
		elsif($in{'site'} eq "") { &error("ホームページ名が未記入です"); }
		elsif($in{'url'} eq "") { &error("URLが未記入です"); }
		elsif($in{'c_name'} eq "") { &error("キャラクターの名前が未記入です"); }
		elsif($in{'sex'} eq "") { &error("性別が選択されていません"); }

		$g = $in{'n_0'} + $in{'n_1'} + $in{'n_2'} + $in{'n_3'} + $in{'n_4'} + $in{'n_5'} + $in{'n_6'};

		if($g > $in{'point'}) { &error("ポイントの振り分けが多すぎます。振り分けの合計を、$in{'point'}以下にしてください。"); }

		&header;

		print "<h1>職業選択画面</h1><hr size=0>\n";
		print "あなたがなることができる職業は以下のとおりです。<p>\n";
		print "<form action=\"$scripta\" method=\"post\">\n";
		print "<input type=hidden name=mode value=regist>\n";
		print "<select name=syoku>\n";
		print "<option value=0>$chara_syoku[0]\n";

		open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$i=0;$hit=0;
	foreach(@syoku){
		($a,$b,$c,$d,$e,$f,$g,$h) = split(/<>/);
		if($in{'n_0'} + $kiso_nouryoku[0] >= $a and $in{'n_1'} + $kiso_nouryoku[1] >= $b and $in{'n_2'} + $kiso_nouryoku[2] >= $c and $in{'n_3'} + $kiso_nouryoku[3] >= $d and $in{'n_4'} + $kiso_nouryoku[4] >= $e and $in{'n_5'} + $kiso_nouryoku[5] >= $f and $in{'n_6'} + $kiso_nouryoku[6] >= $g and $ksyoku != $i) {
			print "<option value=\"$i\">$chara_syoku[$i]\n";
			$hit=1;
		}
		$i++;
	}

		print "</select>\n";
		print "<input type=hidden name=new value=new>\n";
		print "<input type=hidden name=id value=\"$in{'id'}\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=site value=\"$in{'site'}\">\n";
		print "<input type=hidden name=url value=\"$in{'url'}\">\n";
		print "<input type=hidden name=c_name value=\"$in{'c_name'}\">\n";
		print "<input type=hidden name=sex value=\"$in{'sex'}\">\n";
		print "<input type=hidden name=chara value=\"$in{'chara'}\">\n";
		print "<input type=hidden name=n_0 value=\"$in{'n_0'}\">\n";
		print "<input type=hidden name=n_1 value=\"$in{'n_1'}\">\n";
		print "<input type=hidden name=n_2 value=\"$in{'n_2'}\">\n";
		print "<input type=hidden name=n_3 value=\"$in{'n_3'}\">\n";
		print "<input type=hidden name=n_4 value=\"$in{'n_4'}\">\n";
		print "<input type=hidden name=n_5 value=\"$in{'n_5'}\">\n";
		print "<input type=hidden name=n_6 value=\"$in{'n_6'}\">\n";
		print "<input type=submit class=btn value=\"この職業でOK\"></form>\n";

		&ifooter;

		exit;
	}else{
		if($in{'sex'}) { $esex = "男"; } else { $esex = "女"; }
		$next_ex = $lv * $lv_up;

		&header;

		print <<"EOM";
<h1>登録完了画面</h1>
以下の内容で登録が完了しました。
<hr size=0>
<p>
<img src="$img_pathi/$chara_img[$in{'chara'}]"><br>
&#7197;：<a href="http\:\/\/$in{'url'}">$in{'site'}</a>
名：$in{'c_name'}<br>
性：$esex<br>
職：$chara_syoku[$in{'syoku'}]<br>
&#63866;：$gold<br>
LV：$lv<br>
EX：$ex/$next_ex<br>
&#63889;：$hp<br>
力：$n_0<br>
知：$n_1<br>
信：$n_2<br>
生：$n_3<br>
器：$n_4<br>
速：$n_5<br>
魅：$n_6<br>
カ：$lp<br>
<form action="$script" method="post">
<input type="hidden" name=mode value=ilog_in>
<input type="hidden" name=id value="$in{'id'}">
<input type="hidden" name=pass value="$in{'pass'}">
<input type="submit" class="btn" value="&#63873;">
</form>
EOM

		&ifooter;

		exit;
	}
}
__SUB__

	chara_sts => <<'__SUB__',
#----------------#
#ステータス画面  #
#----------------#
sub chara_sts {

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

	if($in{'id'} ne "$kid") {&error("オープンエラー、ID・パスワードが正しくありません。");}
	$yado_daix = int($klv * $yado_dai);

	if(!$hit) { &error("入力されたIDは登録されていません。");}

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

	# 基本値算出
	$divpm = int($charamaxpm / 100);
	$hit_ritu = int(($kn_4 / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($kn_5/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($klp / 15)) + 10 + $kcllv;
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

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {&iheader;}
	else{&header;}

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>$knameさんの詳細情報</h1>
<img src="$img_pathi/$chara_img[$kchara]"><br>
<hr>
名前：$kname<br>
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
<B>$ktac_name</B>
極めたジョブ：$kmaster
EOM
	}else{
	print "<embed src=\"$sts_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	print <<"EOM";
<table align="center"><TR><TD><font size=5>$knameさんのステータス画面</font></TD><TD>
</TD></table>
<hr size=0>
EOM

	print <<"EOM";
<table border=0 align="center" width='50%'>
<tr>
<td valign=top width='100%'>
<table width="100%"><tr>
<tr><td id="td1" colspan="5" class="b2" align="center">キャラクターデータ</td></tr>
<td rowspan="4" align="center" valign=bottom class="b2"><img src="$img_path/$chara_img[$kchara]">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$i_name</td>
<td id="td2" class="b1">攻撃力</td><td align="right" class="b2">$i_dmg</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$d_name</td>
<td id="td2" class="b1">防御力</td><td align="right" class="b2">$d_dmg</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$a_name</td></tr>
</table>
<table width='100%'>
<tr><td id="td1" colspan="5" class="b2" align="center">ステータス</td></tr>
<tr>
<td class="b1" id="td2">なまえ</td><td class="b2">$kname</td>
<td class="b1" id="td2">性別</td><td class="b2">$esex</td></tr>
<tr><td class="b1" id="td2">ジョブ</td><td class="b2">$chara_syoku[$ksyoku]</td>
<td id="td2" align="center" class="b1">ジョブLV</td><td class="b2"><b>$kcllv</b></td></tr>
<tr><td class="b1" id="td2">クラス</td><td colspan=3 class="b2">$class</td></tr>
<tr><td class="b1" id="td2">レベル</td><td class="b2">$klv</td>
<td class="b1" id="td2">経験値</td><td class="b2">$kex/$next_ex</td></tr>
<tr><td class="b1" id="td2">HP</td><td class="b2">$khp\/$kmaxhp</td>
<td class="b1" id="td2">お金</td><td class="b2">$kgold</td></tr>
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
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $a_wazaup%</b></td><td></td></tr>
</table>
<table width="100%"><tr><td id="td2" align="center" class="b1">極めたジョブ</td></tr>
<tr><td colspan=3 align="center" class="b1">$kmaster</td></tr></table>
</table>
EOM
	print "<a href=\"$scripto\">TOPページへ</a>\n";

	}

	$chara_flag=0;

	exit;
}
__SUB__

	messe => <<'__SUB__',

#------------------#
#メッセージシステム#
#------------------#
sub messe {

	open(IN,"./charalog/$in{'id'}.cgi") or &error('ファイルを開けませんでした。');
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	# ヘッダー表示
	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<form action="$scripta" method="post">
<h1>好きなキャラクターへメッセージを送る</h1>
<input type="text" name=mes size=50><br>
<select name=mesid size=20>
EOM
	}else{
	print <<"EOM";
<form action="$scripta" method="post">
<h1>好きなキャラクターへメッセージを送る</h1>
<hr>※他のキャラクターへメッセージを送ることができます。
<table><tr><td class="b2">名前を指定して送る</td>
<td class="b2" valign="top">
<input type="text" name=mesname size=10>名前<br>
<input type="text" name=mes size=50>メッセージ<br>
<br><input type=hidden name=id value=$kid>
<input type=hidden name=name value=$kname>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=message>
<input type=submit class=btn value="メッセージを送る">
</form></td>
EOM
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser ne "DoCoMo") {
	print <<"EOM";
</td><td class="b2" align="left" valign="top" rowspan=2;>
【届いているメッセージ】表\示数<b>$max_gyo</b>件まで<br>
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
			}elsif($kid eq "$hid"){
				print "<hr size=0><small>$knameさんから$hhnameさんへ　＞ 「$hmessage」($htime)</small><br>\n";
			}
		}
	if(!$hit){ print "<hr size=0>$knameさん宛てのメッセージはありません<p>\n"; }
	print "<hr size=0><p>";

	print <<"EOM";
</td></tr>
<tr><form action="$scripta" method="post">
<td class="b2">名前を選んで送る</td>
<td class="b2" valign="top">
<input type="text" name=mes size=50><br>
<select name=mesid size=20>
EOM
	}
	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		push(@MESSAGE, <IN>);
		close(IN);
		}
	}
	closedir(DIR);

	@tmp1 = @tmp2 = ();
	foreach (@MESSAGE) {
 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
		if($first){
	 		push(@RANK_NEW, $_);
	 		push(@tmp1, $first);
			}
		}
	@RANK_NEW = @RANK_NEW[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];

	foreach(@RANK_NEW) {
		($did,$dpass,$dsite,$durl,$dname) = split(/<>/);
		if($kid eq $did) { next; }
		print "<option value=$did>$dnameさんへ\n";
	}

	print <<"EOM";
</select>
<input type=hidden name=id value=$kid>
<input type=hidden name=name value=$kname>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=message>
<input type=submit class=btn value="メッセージを送る">
</form></td></tr></table>
EOM
	}

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {print "<a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>/\n";&footer;}
	else{print "</body></html>\n";}

	exit;
}
__SUB__

	sentaku => <<'__SUB__',
#------------------#
#選択バトルシステム#
#------------------#
sub sentaku {

	open(IN,"./charalog/$in{'id'}.cgi") or &error('ファイルを開けませんでした。');
	@battle = <IN>;
	close(IN);

	foreach(@battle){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>好きなキャラと対戦</h1><hr>
対戦するキャラクターを選択して戦闘できます。
<form action="$scriptb" method="post">
EOM
	print "<select name=sentou size=20>\n";

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

	if($entry=~/\.cgi/){
		open(IN,"./charalog/$entry");
		push(@TATAKAI, <IN>);
		close(IN);
		}
	}
	closedir(DIR);
	foreach (@TATAKAI) {
 		my ($aa,$bb,$cc,$dd,$ee,$ff,$gg,$hh,$ii,$jj,$kk,$ll,$mm,$nn,$oo,$pp,$qq,$second,$first,$kacsno,$kmoriturn) = split /<>/;
		if($first){
	 		push(@RANK_NEW, $_);
	 		push(@tmp1, $first);
			}
		}
	@RANK_NEW = @RANK_NEW[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];

	foreach(@RANK_NEW) {
		($tid,$tpass,$tsite,$turl,$tname,$tsex,$tchara,$tn_0,$tn_1,$tn_2,$tn_3,$tn_4,$tn_5,$tn_6,$tsyoku,$thp,$tmaxhp,$tex,$tlv,$tgold,$tlp,$ttotal,$tkati,$twaza,$titem,$tmons,$thost,$tdate,$tmori,$tdef,$ttac,$tacsno,$tmoriturn,$tcllv,$ts0,$ts1,$ts2,$ts3,$ts4,$ts5,$ts6,$ts7,$ts8,$ts9,$ts10,$ts11,$ts12,$ts13,$ts14,$ts15,$ts16,$ts17,$ts18,$ts19,$ts20,$ts21,$ts22,$ts23,$ts24,$ts25,$ts26,$ts27,$ts28,$ts29,$ts30,$trec) = split(/<>/);
		if($kid eq $tid) { next; }
		print "<option value=$tid>$tname(LV$tlv)\n";
	}

print "</select>\n";
print "<input type=hidden name=id value=$kid>\n";
print "<input type=hidden name=name value=$tid>\n";
print "<input type=hidden name=pass value=$kpass>\n";
print "<input type=hidden name=mode value=tatakai>\n";
print "<input type=submit class=btn value=\"挑戦\">\n";
print "</form>\n";

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {print "<a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>/\n";}
	else{print "<a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">ステータス画面へ</a>/\n";}
	&footer;

	exit;
}
__SUB__

	img_list => <<'__SUB__',
#----------------#
#キャラ画像参照  #
#----------------#
sub img_list {

	&header;

	print <<"EOM";
<html><head><title>キャラ一覧</title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<link rel="stylesheet" href="$style_sheet" type"text.css">
</head><BODY>
<TABLE ALIGN="center" BORDER="1" CELLSPACING="3" CELLPADDING="3">
<CAPTION>キャラ一覧</CAPTION>
EOM

	$i=0;$j=9;
	foreach(@chara_name){
		if($j==9){print "<TR>\n";$j=0;}
		print "<td><img src=\"$img_path/$chara_img[$i]\"><br>$chara_name[$i]\n";
		$i++;$j++;
	}

	print "<a href=\"$scripto\">TOP</a>\n";

}
__SUB__

	img_reflist => <<'__SUB__',
#----------------#
#キャラ画像参照  #
#----------------#
sub img_reflist {

	&header;

	print <<"EOM";
<h1>キャラ画像一覧</h1>
EOM

	$i=0;
	foreach(@chara_name){
		print "<a href=\"$img_pathi/$chara_img[$i]\">$chara_name[$i]</a>\n";
		$i++;
	}

	print "<a href=\"$scripto\">TOP</a>\n";

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

	if($mode ne 'messe' and $mode ne 'message' and $mode ne 'img_list' and $access_flg=='1') {
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

	get_time => <<'__SUB__',
#--------------#
#  時間を取得  #
#--------------#
sub get_time {
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 日時のフォーマット
	$gettime = sprintf("%04d/%02d/%02d %02d:%02d",
			$year+1900,$mon+1,$mday,$hour,$min);
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

	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$wrec) = split(/<>/,$winner[0]);
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
		if($mode ne ""){print "<a href=\"$scripto\">TOPページへ</a>\n";}
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

	ifooter => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub ifooter {
	if($refresh and !$win and $mode eq 'ibattle') {
		print "【<b><a href=\"http\:\/\/$wurl\">&#63904;</a></b>】\n";
	}else{
		if($mode ne ""){print "<a href=\"$scripto\">TOP</a>\n";}
	}
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
	print "</DIV></body></html>\n";
}
__SUB__

	set_cookie => <<'__SUB__',
#------------------#
#  クッキーの発行  #
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
);
}
