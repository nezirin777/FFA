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
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した #
#    いかなる損害に対して作者は一切の責任を負いません。     	#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。   	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require './jacode.pl';

# レジストライブラリの読み込み
require './regist.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

# [設定はここまで]------------------------------------------------------------#

# これより下は、CGIのわかる方以外は、変更しないほうが良いです。

#-----------------------------------------------------------------------------#
if($mente) { &error("現在バージョンアップ中です。しばらくお待ちください。"); }
&decode;
if (!($ENV{'REQUEST_METHOD'} eq "POST")){&error('そんなページはありません！');}
#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}
if($mode eq 'item_eqq') { &item_shop; }
elsif($mode eq 'item_shop') { &item_shop; }
elsif($mode eq 'item_buy') { &item_buy; }
elsif($mode eq 'item_sell') { &item_sell; }
elsif($mode eq 'def_eqq') {&def_shop; }
elsif($mode eq 'def_shop') { &def_shop; }
elsif($mode eq 'def_buy') { &def_buy; }
elsif($mode eq 'def_sell') { &def_sell; }
elsif($mode eq 'senjutu') { &senjutu; }
elsif($mode eq 'senjutu_henkou') { &senjutu_henkou; }
elsif($mode eq 'tac_eqq') {&senjutu; }
elsif($mode eq 'yado') { &yado; }
elsif($mode eq 'bank_shop') { &bank_shop; }
elsif($mode eq 'bank_buy') { &bank_buy; }
elsif($mode eq 'bank_sell') { &bank_sell; }
elsif($mode eq 'kunren') { &kunren; }
elsif($mode eq 'kunrenok') { &kunrenok; }
elsif($mode eq 'acs_eqq') { &acs_shop; }
elsif($mode eq 'acs_buy') { &acs_buy; }
elsif($mode eq 'acs_sell') { &acs_sell; }
elsif($mode eq 'save_data') { &save_data; }
elsif($mode eq 'load_game') { &load_game; }
exit;

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
	item_shop => <<'__SUB__',
#----------------#
#  アイテム表示  #
#----------------#
sub item_shop {


	open(IN,"./charalog/$in{'id'}.cgi");
	@buki = <IN>;
	close(IN);

$hit=0;
	foreach(@buki){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$itemsell_file");
	@log_item = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_item){
		($si_no,$si_name,$si_dmg,$si_gold) = split(/<>/);
		if($kitem eq "$si_no"){ $hit=1;last; }
	}
	if(!$hit) { $si_name="－"; }
	if(!$hit) { $si_dmg="－"; }
	if(!$hit) { $si_gold="－"; }

	$ui_gold = int($si_gold / 3) * 2;


	open(IN,"$item_file[$ksyoku]");
	@item_array = <IN>;
	close(IN);

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>武器屋</h1>
<hr size=0>
<br><hr>現在の所持金：$kgold Ｇ<br>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=item_sell>
<input type=submit class=btn value="売る">
</form>現在の装備品：$si_name：$ui_gold<br>
EOM

	foreach(@item_array){
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print "<a href=\"$scripts?mode=item_buy&id=$kid&pass=$kpass&item_no=$ino\">$iname：($igold G)</a><br>\n";
	}

	print "<p><a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>";
	}
	else{
	print <<"EOM";
<h1>武器屋</h1>
<hr size=0>
<p>
<form action="$scripts" method="post">
<FONT SIZE=3>
<B>武器屋のマスター</B><BR>
「いらっしゃい！いい武器揃ってるよ～。この大陸の中じゃ、うちが一番の品揃えだよ！<BR>
　あ、なんだい、<B>$kname</B>じゃないか。元気にしてたかい？
<BR>今は$chara_syoku[$ksyoku]をやってるのか。
<BR>昨日$chara_syoku[$ksyoku]用の武器を入荷したんだよ！
<BR>
　まあ、ゆっくり見ていってくれ。
<BR><BR>そうそう！最近装備品の下取りもはじめたんだ。」
</FONT>
<br><hr>現在の所持金：$kgold Ｇ<br>
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>威力</th><th>価格</th></tr>
<tr><th><input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=item_sell>
<input type=submit class=btn value="売る">
</th></form><th>現在の装備品</th><th>$si_name</th><th>$si_dmg</th><th>$ui_gold</th><form action="$scripts" method="post">
EOM

	foreach(@item_array){
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print "<tr>\n";
		print "<td class=b1><input type=radio name=item_no value=\"$ino\"></td><td align=right class=b1>$ino</td><td class=b1>$iname</td><td align=right class=b1>？</td><td align=right class=b1>$igold</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<p>
<input type=hidden name=id value=$in{'id'}>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=item_buy>
<input type=submit class=btn value="武器を買う">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	item_buy => <<'__SUB__',
#----------------#
#  アイテム買う  #
#----------------#
sub item_buy {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@buki = <IN>;
	close(IN);
$hit=0;
	foreach(@buki){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}
	open(IN,"$item_file[$ksyoku]");
	@item_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@item_array){
		($i_no,$i_name,$i_dmg,$i_gold) = split(/<>/);
		if($in{'item_no'} eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			if($igold < $i_gold) { &error("お金が足りません"); }
			else { $igold = $igold - $i_gold; }
			if($iacsno == '\n'){$iacsno='0';$imoriturn='0';}
			unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$i_no<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@item_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @item_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>アイテムを買いました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$in{'id'}>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	item_sell => <<'__SUB__',
#----------------#
#  アイテム売る  #
#----------------#
sub item_sell {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@buki = <IN>;
	close(IN);

$hit=0;
	foreach(@buki){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$itemsell_file");
	@item_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@item_array){
		($i_no,$i_name,$i_dmg,$i_gold) = split(/<>/);
		if($kitem eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }
	if(!$kitem) { &error("そんなアイテムは存在しません"); }
	$ui_gold = int($i_gold / 3) * 2;

	&get_host;

	$date = time();



	open(IN,"./charalog/$in{'id'}.cgi");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			$igold = $igold + $ui_gold;
			if($igold > $gold_max){$igold = $gold_max;}
			unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<><>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@item_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @item_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>アイテムを売りました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	def_shop => <<'__SUB__',
#----------------#
#  防具表示      #
#----------------#
sub def_shop {

	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

$hit=0;
	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$defsell_file");
	@log_def = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_def){
		($si_no,$si_name,$si_dmg,$si_gold) = split(/<>/);
		if($kdef eq "$si_no"){ $hit=1;last; }
	}
	if(!$hit) { $si_name="－"; }
	if(!$hit) { $si_dmg="－"; }
	if(!$hit) { $si_gold="－"; }

	$ui_gold = int($si_gold / 3) * 2;


	open(IN,"$def_file[$ksyoku]");
	@def_array = <IN>;
	close(IN);

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>防具屋</h1>
<hr size=0>
<br><hr>現在の所持金：$kgold Ｇ<br>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=item_sell>
<input type=submit class=btn value="売る">
</form>現在の装備品：$si_name：$ui_gold<br>
EOM

	foreach(@def_array){
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print "<a href=\"$scripts?mode=def_buy&id=$kid&pass=$kpass&def_no=$ino\">$iname：($igold G)</a><br>\n";
	}

	print "<p><a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>";
	}else{
	print <<"EOM";
<h1>防具屋</h1>
<hr size=0>
<p>
<form action="$scripts" method="post">
<FONT SIZE=3>
<B>防具のマスター</B><BR>
「いらっしゃい！いい防具揃ってるよ～。この大陸の中じゃ、うちが一番の品揃えだよ！<BR>
　あ、なんだい、<B>$kname</B>じゃないか。元気にしてたかい？
<BR>今は$chara_syoku[$ksyoku]をやってるのか。
<BR>昨日$chara_syoku[$ksyoku]用の防具を入荷したんだよ！
<BR>
　まあ、ゆっくり見ていってくれ。
<BR><BR>そうそう！最近装備品の下取りもはじめたんだ。」
</FONT>
<br><hr>現在の所持金：$kgold Ｇ<br>
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>防御力</th><th>価格</th></tr>
<tr><th><input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=def_sell>
<input type=submit class=btn value="売る">
</th></form><th>現在の装備品</th><th>$si_name</th><th>$si_dmg</th><th>$ui_gold</th><form action="$scripts" method="post">
EOM

	foreach(@def_array){
		($ino,$iname,$idmg,$igold) = split(/<>/);
		print "<tr>\n";
		print "<td class=b1><input type=radio name=def_no value=\"$ino\"></td><td align=right class=b1>$ino</td><td class=b1>$iname</td><td align=right class=b1>？</td><td align=right class=b1>$igold</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<p>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=def_buy>
<input type=submit class=btn value="防具を買う">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	def_buy => <<'__SUB__',
#----------------#
#  防具を買う    #
#----------------#
sub def_buy {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

$hit=0;
	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$def_file[$ksyoku]");
	@def_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@def_array){
		($i_no,$i_name,$i_dmg,$i_gold) = split(/<>/);
		if($in{'def_no'} eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi");
	@def_chara = <IN>;
	close(IN);

	$hit=0;@def_new=();
	foreach(@def_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			if($igold < $i_gold) { &error("お金が足りません"); }
			else { $igold = $igold - $i_gold; }
			unshift(@def_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$i_no<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@def_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @def_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>アイテムを買いました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	def_sell => <<'__SUB__',
#----------------#
#  防具を売る    #
#----------------#
sub def_sell {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

$hit=0;
	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$defsell_file");
	@def_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@def_array){
		($i_no,$i_name,$i_dmg,$i_gold) = split(/<>/);
		if($kdef eq "$i_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }
	if(!$kdef) { &error("そんなアイテムは存在しません"); }
	$ui_gold = int($i_gold / 3) * 2;

	&get_host;

	$date = time();



	open(IN,"./charalog/$in{'id'}.cgi");
	@def_chara = <IN>;
	close(IN);

	$hit=0;@def_new=();
	foreach(@def_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			$igold = $igold + $ui_gold;
			if($igold > $gold_max){$igold = $gold_max;}
			unshift(@def_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<><>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@def_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @def_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>防具を売りました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	senjutu => <<'__SUB__',
#----------------#
#  戦術表示      #
#----------------#
sub senjutu {

	open(IN,"./charalog/$in{'id'}.cgi");
	@senjutu = <IN>;
	close(IN);

$hit=0;
	foreach(@senjutu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	if($ksyoku==0){$ks_syoku=$ks0;}
	elsif($ksyoku==1){$ks_syoku=$ks1;}
	elsif($ksyoku==2){$ks_syoku=$ks2;}
	elsif($ksyoku==3){$ks_syoku=$ks3;}
	elsif($ksyoku==4){$ks_syoku=$ks4;}
	elsif($ksyoku==5){$ks_syoku=$ks5;}
	elsif($ksyoku==6){$ks_syoku=$ks6;}
	elsif($ksyoku==7){$ks_syoku=$ks7;}
	elsif($ksyoku==8){$ks_syoku=$ks8;}
	elsif($ksyoku==9){$ks_syoku=$ks9;}
	elsif($ksyoku==10){$ks_syoku=$ks10;}
	elsif($ksyoku==11){$ks_syoku=$ks11;}
	elsif($ksyoku==12){$ks_syoku=$ks12;}
	elsif($ksyoku==13){$ks_syoku=$ks13;}
	elsif($ksyoku==14){$ks_syoku=$ks14;}
	elsif($ksyoku==15){$ks_syoku=$ks15;}
	elsif($ksyoku==16){$ks_syoku=$ks16;}
	elsif($ksyoku==17){$ks_syoku=$ks17;}
	elsif($ksyoku==18){$ks_syoku=$ks18;}
	elsif($ksyoku==19){$ks_syoku=$ks19;}
	elsif($ksyoku==20){$ks_syoku=$ks20;}
	elsif($ksyoku==21){$ks_syoku=$ks21;}
	elsif($ksyoku==22){$ks_syoku=$ks22;}
        elsif($ksyoku==23){$ks_syoku=$ks23;}
        elsif($ksyoku==24){$ks_syoku=$ks24;}
        elsif($ksyoku==25){$ks_syoku=$ks25;}
        elsif($ksyoku==26){$ks_syoku=$ks26;}
        elsif($ksyoku==27){$ks_syoku=$ks27;}
        elsif($ksyoku==28){$ks_syoku=$ks28;}
        elsif($ksyoku==29){$ks_syoku=$ks29;}
        elsif($ksyoku==30){$ks_syoku=$ks30;}

	open(IN,"$tac_file[$ksyoku]");
	@gettac = <IN>;
	close(IN);
	foreach (@gettac){
		($ks_no,$ks_name,$ks_plus,$ks_ms) = split(/<>/);
		if($ks_ms == 0 or $ks_ms == $ks_syoku){push(@log_senjutu,"$_");}
		}

	#マスターした戦術のインクルード
	if($ks0==1 and $ksyoku!=0){
		open(IN,"$tac_file[0]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks1==1 and $ksyoku!=1){
		open(IN,"$tac_file[1]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks2==1 and $ksyoku!=2){
		open(IN,"$tac_file[2]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks3==1 and $ksyoku!=3){
		open(IN,"$tac_file[3]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks4==1 and $ksyoku!=4){
		open(IN,"$tac_file[4]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks5==1 and $ksyoku!=5){
		open(IN,"$tac_file[5]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks6==1 and $ksyoku!=6){
		open(IN,"$tac_file[6]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks7==1 and $ksyoku!=7){
		open(IN,"$tac_file[7]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks8==1 and $ksyoku!=8){
		open(IN,"$tac_file[8]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks9==1 and $ksyoku!=9){
		open(IN,"$tac_file[9]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks10==1 and $ksyoku!=10){
		open(IN,"$tac_file[10]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks11==1 and $ksyoku!=11){
		open(IN,"$tac_file[11]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks12==1 and $ksyoku!=12){
		open(IN,"$tac_file[12]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks13==1 and $ksyoku!=13){
		open(IN,"$tac_file[13]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks14==1 and $ksyoku!=14){
		open(IN,"$tac_file[14]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks15==1 and $ksyoku!=15){
		open(IN,"$tac_file[15]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks16==1 and $ksyoku!=16){
		open(IN,"$tac_file[16]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks17==1 and $ksyoku!=17){
		open(IN,"$tac_file[17]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks18==1 and $ksyoku!=18){
		open(IN,"$tac_file[18]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks19==1 and $ksyoku!=19){
		open(IN,"$tac_file[19]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks20==1 and $ksyoku!=20){
		open(IN,"$tac_file[20]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks21==1 and $ksyoku!=21){
		open(IN,"$tac_file[21]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks22==1 and $ksyoku!=22){
		open(IN,"$tac_file[22]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks23==1 and $ksyoku!=23){
		open(IN,"$tac_file[23]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks24==1 and $ksyoku!=24){
		open(IN,"$tac_file[24]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks25==1 and $ksyoku!=25){
		open(IN,"$tac_file[25]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks26==1 and $ksyoku!=26){
		open(IN,"$tac_file[26]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks27==1 and $ksyoku!=27){
		open(IN,"$tac_file[27]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks28==1 and $ksyoku!=28){
		open(IN,"$tac_file[28]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks29==1 and $ksyoku!=29){
		open(IN,"$tac_file[29]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks30==1 and $ksyoku!=30){
		open(IN,"$tac_file[30]");
		push(@log_senjutu, <IN>);
		close(IN);}


	$hit=0;
	foreach(@log_senjutu){
		($ks_no,$ks_name) = split(/<>/);
		if($ktac eq "$ks_no"){ $hit=1;last; }
	}
	if(!$hit) { $ks_name="普通に戦う"; }

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>作戦会議室</h1>
<hr size=0>
現在の戦術：<br>
EOM
	foreach(@log_senjutu){
		($s_no,$s_name,$s_point,$s_mas) = split(/<>/);
		print "<a href=\"$scripts?mode=senjutu_henkou&id=$kid&pass=$kpass&senjutu_no=$s_no\">$s_name</a><br>\n";
		}
	print "<p><a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>";
	}else{
	print <<"EOM";
<h1>作戦会議室</h1>
<hr size=0>
<p>
<BR>
<table>
<tr>
<th colspan=2>戦術</th>
<tr><th>現在の戦術</th><th>$ks_name</th><form action="$scripts" method="post">
EOM

	foreach(@log_senjutu){
		($s_no,$s_name,$s_point,$s_mas) = split(/<>/);
		print "<tr>\n";
		print "<td class=b1><input type=radio name=senjutu_no value=\"$s_no\"></td><td class=b1>$s_name</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<p>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=senjutu_henkou>
<input type=submit class=btn value="変更する">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	senjutu_henkou => <<'__SUB__',
#----------------#
#  戦術変更      #
#----------------#
sub senjutu_henkou {

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@senjutu = <IN>;
	close(IN);

$hit=0;
	foreach(@senjutu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}
	open(IN,"$tac_file[$ksyoku]");
	@gettac = <IN>;
	close(IN);
	foreach (@gettac){
		($ks_no,$ks_name,$ks_plus,$ks_ms) = split(/<>/);
		if($ks_ms == 0){push(@log_senjutu,"$_");}
		}

	#マスターした戦術のインクルード
	if($ks0==1){
		open(IN,"$tac_file[0]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks1==1){
		open(IN,"$tac_file[1]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks2==1){
		open(IN,"$tac_file[2]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks3==1){
		open(IN,"$tac_file[3]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks4==1){
		open(IN,"$tac_file[4]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks5==1){
		open(IN,"$tac_file[5]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks6==1){
		open(IN,"$tac_file[6]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks7==1){
		open(IN,"$tac_file[7]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks8==1){
		open(IN,"$tac_file[8]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks9==1){
		open(IN,"$tac_file[9]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks10==1){
		open(IN,"$tac_file[10]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks11==1){
		open(IN,"$tac_file[11]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks12==1){
		open(IN,"$tac_file[12]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks13==1){
		open(IN,"$tac_file[13]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks14==1){
		open(IN,"$tac_file[14]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks15==1){
		open(IN,"$tac_file[15]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks16==1){
		open(IN,"$tac_file[16]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks17==1){
		open(IN,"$tac_file[17]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks18==1){
		open(IN,"$tac_file[18]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks19==1){
		open(IN,"$tac_file[19]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks20==1){
		open(IN,"$tac_file[20]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks21==1){
		open(IN,"$tac_file[21]");
		push(@log_senjutu, <IN>);
		close(IN);}
	if($ks22==1){
		open(IN,"$tac_file[22]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks23==1){
		open(IN,"$tac_file[23]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks24==1){
		open(IN,"$tac_file[24]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks25==1){
		open(IN,"$tac_file[25]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks26==1){
		open(IN,"$tac_file[26]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks27==1){
		open(IN,"$tac_file[27]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks28==1){
		open(IN,"$tac_file[28]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks29==1){
		open(IN,"$tac_file[29]");
		push(@log_senjutu, <IN>);
		close(IN);}
        if($ks30==1){
		open(IN,"$tac_file[30]");
		push(@log_senjutu, <IN>);
		close(IN);}

	$hit=0;
	foreach(@log_senjutu){
		($s_no,$s_name) = split(/<>/);
		if($in{'senjutu_no'} eq "$s_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんな戦術はありません"); }

	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi");
	@senjutu_chara = <IN>;
	close(IN);

	$hit=0;@senjutu_new=();
	foreach(@senjutu_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			if($iacsno == '\n'){$iacsno='0';$imoriturn='0';}
			unshift(@senjutu_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$s_no<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@senjutu_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @senjutu_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	print <<"EOM";
<h1>変更しました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
__SUB__

	yado => <<'__SUB__',
#------------#
#  体力回復  #
#------------#
sub yado {
	&get_host;

	$date = time();

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi");
	@YADO = <IN>;
	close(IN);

	$hit=0;@yado_new=();
	foreach(@YADO){
		($yid,$ypass,$ysite,$yurl,$yname,$ysex,$ychara,$yn_0,$yn_1,$yn_2,$yn_3,$yn_4,$yn_5,$yn_6,$ysyoku,$yhp,$ymaxhp,$yex,$ylv,$ygold,$ylp,$ytotal,$ykati,$ywaza,$yitem,$ymons,$yhost,$ydate,$ymori,$ydef,$ytac,$yacsno,$ymoriturn,$ycllv,$ys0,$ys1,$ys2,$ys3,$ys4,$ys5,$ys6,$ys7,$ys8,$ys9,$ys10,$ys11,$ys12,$ys13,$ys14,$ys15,$ys16,$ys17,$ys18,$ys19,$ys20,$ys21,$ys22,$ys23,$ys24,$ys25,$ys26,$ys27,$ys28,$ys29,$ys30,$yrec) = split(/<>/);

	if($ymori < $boss) { $ymori = 0; }
	$yado_daix = int($ylv * $yado_dai);
		if($in{'id'} eq "$yid" && $in{'pass'} eq "$ypass") {
			if($ygold < $yado_daix) { &error("お金が足りません"); }
			else { $ygold = $ygold - $yado_daix; }
			unshift(@yado_new,"$yid<>$ypass<>$ysite<>$yurl<>$yname<>$ysex<>$ychara<>$yn_0<>$yn_1<>$yn_2<>$yn_3<>$yn_4<>$yn_5<>$yn_6<>$ysyoku<>$ymaxhp<>$ymaxhp<>$yex<>$ylv<>$ygold<>$ylp<>$ytotal<>$ykati<>$ywaza<>$yitem<>$ymons<>$host<>$ydate<>$ymori<>$ydef<>$ytac<>$yacsno<>$ymoriturn<>$ycllv<>$ys0<>$ys1<>$ys2<>$ys3<>$ys4<>$ys5<>$ys6<>$ys7<>$ys8<>$ys9<>$ys10<>$ys11<>$ys12<>$ys13<>$ys14<>$ys15<>$ys16<>$ys17<>$ys18<>$ys19<>$ys20<>$ys21<>$ys22<>$ys23<>$ys24<>$ys25<>$ys26<>$ys27<>$ys28<>$ys29<>$ys30<>$yrec<>\n");$hit=1;last;
		}
	}

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @yado_new;
	close(OUT);

	&read_winner;

	if($wid eq "$in{'id'}") {
		open(OUT,">$winner_file");
		print OUT "$wid<>$wpass<>$wsite<>$wurl<>$wname<>$wsex<>$wchara<>$wn_0<>$wn_1<>$wn_2<>$wn_3<>$wn_4<>$wn_5<>$wn_6<>$wsyoku<>$wmaxhp<>$wmaxhp<>$wex<>$wlv<>$wgold<>$wlp<>$wtotal<>$wkati<>$wwaza<>$witem<>$wmons<>$host<>$ydate<>$wcount<>$lsite<>$lurl<>$lname<>$wmori<>$wdef<>$wtac<>$wacsno<>$wmoriturn<>$wcllv<>$ws0<>$ws1<>$ws2<>$ws3<>$ws4<>$ws5<>$ws6<>$ws7<>$ws8<>$ws9<>$ws10<>$ws11<>$ws12<>$ws13<>$ws14<>$ws15<>$ws16<>$ws17<>$ws18<>$ws19<>$ws20<>$ws21<>$ws22<>$ws23<>$ws24<>$ws25<>$ws26<>$ws27<>$ws28<>$ws29<>$ws30<>$wrec<>\n";
		close(OUT);
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>体力を回復しました</h1>
<hr size=0>
<a href="$script?mode=log_in&id=$in{'id'}&pass=$in{'pass'}">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>体力を回復しました</h1>
<hr size=0>
<form action="$script" method="post">
<input type=hidden name=mode value=log_in>
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	bank_shop => <<'__SUB__',
#----------------#
# 銀行表示 　　  #
#----------------#
sub bank_shop {
    &get_host;

    $date = time();

    # ファイルロック
    if ($lockkey == 1) { &lock1; }
    elsif ($lockkey == 2) { &lock2; }

$chara_flag=1;

open(IN,"./charalog/$in{'id'}.cgi");
@log_in = <IN>;
close(IN);

$hit=0;
foreach(@log_in){
($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

open(IN,"./banklog/$in{'id'}.cgi");
@battle_item = <IN>;
close(IN);

foreach(@battle_item){
($ki_no,$ki_pass,$ki_gold) = split(/<>/);
if($kid eq $ki_no) { last; }
else{ $ki_gold = 0; }
}

$ki_tesuu = $ki_gold;
$kgold_tesuu = $kgold;

# ロック解除
    if (-e $lockfile) { unlink($lockfile); }

&header;

print <<"EOM";
<h1>銀行</h1>
<hr size=0>
<font Size="3"> $knameさんの現在の<br>
　　　所持金：<b>$kgold</b>ギル  ／<br>
　　　　　　　預金可能\額　：<b><font color=$yellow>$kgold_tesuu</font></b>ギル<br>
　　　預金　：<b>$ki_gold</b>ギル／<br>
　　　　　　　引出可能\額  ：<b><font color=$yellow>$ki_tesuu</font></b>ギル
</font><p>
<font color=$yellow><b>最高預け入れ額 $bank_max ギル</b></font>を超えた分は<a href="http://www.corcocu.co.jp/CCONA/">動物愛護団体</a>に寄付されます。<br>
<form action="$scripts" method="post">
<input type="text" name=azukeru value="$azuke" size=10>000 ギル
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=bank_sell>
<input type=submit class=btn value="ギルを預ける">
</form>
<form action="$scripts" method="post">
<input type="text" name=dasu value="$dasu" size=10>000 ギル
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=bank_buy>
<input type=submit class=btn value="ギルを出す">
</form>
EOM
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
print <<"EOM";
<a href="$script?mode=log_in&id=$in{'id'}&pass=$in{'pass'}">&#63873;</a>
EOM
	}else{
print <<"EOM";
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
}

&footer;

exit;
}
__SUB__

	bank_buy => <<'__SUB__',
#----------------#
# お金を出す #
#----------------#
sub bank_buy {
if($in{'dasu'} eq ""){
&error("金額が入力されていません。");
}

$bank_id = $in{'id'};
$bank_pass = $in{'pass'};
$dasu = $in{'dasu'};

if($dasu < 0) { &error("マイナスは入力出来ません。"); }
else { $dasuru = int($dasu) * 1000; }

if($dasu =~ /[^0-9]/){&error('エラー！','数値不正のため受け付けません');}
if(!($dasu >= 0 && $dasu <= $bank_max)) { &error("不正な値です！"); }

&get_host;

$date = time();

# ファイルロック
if ($lockkey == 1) { &lock1; }
elsif ($lockkey == 2) { &lock2; }

open(IN,"./banklog/$in{'id'}.cgi");
@item_chara = <IN>;
close(IN);

$hit=0;@item_new=();
foreach(@item_chara){
($i_no,$i_pass,$i_gold) = split(/<>/);
if($i_no eq "$bank_id") {
if((int($dasu) * 1000) > $i_gold) { &error("預金額を超えています！！"); }
else { $i_gold = $i_gold - $dasuru; }
unshift(@item_new,"$i_no<>$i_pass<>$i_gold<>\n");
$hit=1;
}else{
push(@item_new,"$_");
}
}

if(!$hit){ &error("預かっているお金はありません。"); }

open(OUT,">./banklog/$in{'id'}.cgi");
print OUT @item_new;
close(OUT);

open(IN,"./charalog/$in{'id'}.cgi");
@item_chara = <IN>;
close(IN);

$hit=0;@item_new=();
foreach(@item_chara){
($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
if($iid eq "$bank_id" && $ipass eq "$in{'pass'}") {
$i_gold = $igold + $dasuru;
if($gold_max < $i_gold){$i_gold=$gold_max;}
unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$i_gold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
$hit=1;last;
}}


if(!$hit) { &error("キャラクターが見つかりません"); }

open(OUT,">./charalog/$in{'id'}.cgi");
print OUT @item_new;
close(OUT);

# ロック解除
if (-e $lockfile) { unlink($lockfile); }

&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
print <<"EOM";
<h1>ご利用ありがとうございました</h1>
<hr size=0>
<a href="$script?mode=log_in&id=$in{'id'}&pass=$in{'pass'}">&#63873;</a>
EOM
	}else{
print <<"EOM";
<h1>ご利用ありがとうございました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value="$bank_id">
<input type=hidden name=pass value="$bank_pass">
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}
&footer;

exit;
}
__SUB__

	bank_sell => <<'__SUB__',
#----------------#
# お金を預ける   #
#----------------#
sub bank_sell {
if($in{'azukeru'} eq ""){
&error("金額が入力されていません。");
}
if($in{'azukeru'} =~ /[^0-9]/){&error('エラー！','数値不正のため受け付けません');}

$bank_id = $in{'id'};
$bank_pass = $in{'pass'};
$azuke = $in{'azukeru'};

if($azuke < 0) { &error("マイナスは入力出来ません。"); }
else { $azukeru = int($azuke) * 1000; }
&get_host;
if(!($azuke >= 0 && $azuke <= $bank_max)) { &error("不正な値です！"); }

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
if($iid eq "$bank_id" && $ipass eq "$in{'pass'}") {
if(int($azuke) * 1000 > $igold) { &error("ギルが足りません"); }
else { $i_gold = $igold-$azukeru; }
unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$i_gold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
$hit=1;last
}
}

if(!$hit) { &error("キャラクターが見つかりません"); }

open(OUT,">./charalog/$in{'id'}.cgi");
print OUT @item_new;
close(OUT);

open(IN,"./banklog/$in{'id'}.cgi");
@item_chara = <IN>;
close(IN);

$hit=0;@item_new=();
foreach(@item_chara){
($i_no,$i_pass,$i_gold) = split(/<>/);
if($i_no eq "$bank_id") {
$i_gold = $i_gold + $azukeru;
if($bank_max <$i_gold){$i_gold = $bank_max;}
unshift(@item_new,"$i_no<>$i_pass<>$i_gold<>\n");
$hit=1;
}else{
push(@item_new,"$_");
}
}

if(!$hit){
unshift(@item_new,"$bank_id<>$bank_pass<>$azukeru<>\n");
}

open(OUT,">./banklog/$in{'id'}.cgi");
print OUT @item_new;
close(OUT);

# ロック解除
if (-e $lockfile) { unlink($lockfile); }

&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
print <<"EOM";
<h1>ご利用ありがとうございました</h1>
<hr size=0>
<a href="$script?mode=log_in&id=$in{'id'}&pass=$in{'pass'}">&#63873;</a>
EOM
	}else{
print <<"EOM";
<h1>ギルを預けました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value="$bank_id">
<input type=hidden name=pass value="$bank_pass">
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

&footer;

exit;
}
__SUB__

	kunren => <<'__SUB__',
#----------------#
#  訓練所        #
#----------------#
sub kunren {

	open(IN,"./charalog/$in{'id'}.cgi");
	@kunren = <IN>;
	close(IN);

	foreach(@kunren){
		($pid,$ppass,$psite,$purl,$pname,$psex,$pchara,$pn_0,$pn_1,$pn_2,$pn_3,$pn_4,$pn_5,$pn_6,$psyoku,$php,$pmaxhp,$pex,$plv,$pgold,$plp,$ptotal,$pkati,$pwaza,$pitem,$pmons,$phost,$pdate,$pmori,$pdef,$ptac,$pacsno,$pmoriturn,$pcllv,$ps0,$ps1,$ps2,$ps3,$ps4,$ps5,$ps6,$ps7,$ps8,$ps9,$ps10,$ps11,$ps12,$ps13,$ps14,$ps15,$ps16,$ps17,$ps18,$ps19,$ps20,$ps21,$ps22,$ps23,$ps24,$ps25,$ps26,$ps27,$ps28,$ps29,$ps30,$prec) = split(/<>/);
		if($in{'id'} eq "$pid" && $in{'pass'} eq "$ppass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}
	$pdai = int(($pn_0+$pn_1+$pn_2+$pn_3+$pn_4+$pn_5+$pn_6+$plp) / 8) * $kun_point;
	$prm0_gold = $pn_0 * $pdai;
	$prm1_gold = $pn_1 * $pdai;
	$prm2_gold = $pn_2 * $pdai;
	$prm3_gold = $pn_3 * $pdai;
	$prm4_gold = $pn_4 * $pdai;
	$prm5_gold = $pn_5 * $pdai;
	$prm6_gold = $pn_6 * $pdai;
	$prm7_gold = $plp * $pdai;
	$prm8_gold = $pmaxhp * $kun_point;

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>訓練所</h1>
<hr size=0>
<form action="$scripts" method="post">
<br><hr>現在の所持金：$pgold Ｇ<br>
</FONT>
<input type=radio name=prm_no value=0 selected>力   を鍛える($pn_0/$charamaxpm)$prm0_gold Ｇ<br>
<input type=radio name=prm_no value=1>魔力を鍛える($pn_1/$charamaxpm)$prm1_gold Ｇ<br>
<input type=radio name=prm_no value=2>信仰心を鍛える($pn_2/$charamaxpm)$prm2_gold Ｇ<br>
<input type=radio name=prm_no value=3>生命力を鍛える($pn_3/$charamaxpm)$prm3_gold Ｇ<br>
<input type=radio name=prm_no value=4>器用さを鍛える($pn_4/$charamaxpm)$prm4_gold Ｇ<br>
<input type=radio name=prm_no value=5>速さ　を鍛える($pn_5/$charamaxpm)$prm5_gold Ｇ<br>
<input type=radio name=prm_no value=6>魅力　を鍛える($pn_6/$charamaxpm)$prm6_gold Ｇ<br>
<input type=radio name=prm_no value=7>カルマを鍛える($plp/$charamaxpm)$prm7_gold Ｇ<br>
<input type=radio name=prm_no value=8>ＨＰ　を鍛える($pmaxhp/$charamaxhp)$prm8_gold Ｇ<br>
<input type=hidden name=id value=$pid>
<input type=hidden name=pass value=$ppass>
<input type=hidden name=mode value=kunrenok>
<input type=submit class=btn value="訓練する">
</form>
<a href="$script?mode=log_in&id=$pid&pass=$ppass">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>訓練所</h1>
<hr size=0>
<form action="$scripts" method="post">
<FONT SIZE=3>
<B>訓練所の先生</B><BR>
「よく来たな！<BR>
　私が見たところ<B>$pname</B>の力はまだそんなもんではない！
<BR>お前の潜在\能\力を引き出す手伝いをしてやろうか？。
<BR>タダではできんが・・・・どうする？
<BR>まあ、じっくり考えてくれ。」
<br><hr>現在の所持金：$pgold Ｇ<br>
</FONT>
<table>
<tr><th></th><th>No.</th><th>鍛えたいパラメータ</th><th>現在値</th><th>最大値</th><th>価格</th></tr>
<tr><td class=b1><input type=radio name=prm_no value=0 selected></td><td align=right class=b1>0001</td><td class=b1>力   を鍛える</td><td class=b1>$pn_0</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm0_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=1></td><td align=right class=b1>0002</td><td class=b1>魔力を鍛える</td><td class=b1>$pn_1</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm1_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=2></td><td align=right class=b1>0003</td><td class=b1>信仰心を鍛える</td><td class=b1>$pn_2</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm2_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=3></td><td align=right class=b1>0004</td><td class=b1>生命力を鍛える</td><td class=b1>$pn_3</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm3_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=4></td><td align=right class=b1>0005</td><td class=b1>器用さを鍛える</td><td class=b1>$pn_4</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm4_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=5></td><td align=right class=b1>0006</td><td class=b1>速さ　を鍛える</td><td class=b1>$pn_5</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm5_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=6></td><td align=right class=b1>0007</td><td class=b1>魅力　を鍛える</td><td class=b1>$pn_6</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm6_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=7></td><td align=right class=b1>0008</td><td class=b1>カルマを鍛える</td><td class=b1>$plp</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm7_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=8></td><td align=right class=b1>0009</td><td class=b1>ＨＰ　を鍛える</td><td class=b1>$pmaxhp</td><td class=b1>$charamaxhp</td><td align=right class=b1>$prm8_gold Ｇ</td></tr>
</table>
<input type=hidden name=id value=$pid>
<input type=hidden name=pass value=$ppass>
<input type=hidden name=mode value=kunrenok>
<input type=submit class=btn value="訓練する">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$pid>
<input type=hidden name=pass value=$ppass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}
	&footer;

	exit;
}
__SUB__

	kunrenok => <<'__SUB__',
#----------------#
#  訓練する      #
#----------------#
sub kunrenok {

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi");
	@kunren = <IN>;
	close(IN);

	foreach(@kunren){
		($pid,$ppass,$psite,$purl,$pname,$psex,$pchara,$pn_0,$pn_1,$pn_2,$pn_3,$pn_4,$pn_5,$pn_6,$psyoku,$php,$pmaxhp,$pex,$plv,$pgold,$plp,$ptotal,$pkati,$pwaza,$pitem,$pmons,$phost,$pdate,$pmori,$pdef,$ptac,$pacsno,$pmoriturn,$pcllv,$ps0,$ps1,$ps2,$ps3,$ps4,$ps5,$ps6,$ps7,$ps8,$ps9,$ps10,$ps11,$ps12,$ps13,$ps14,$ps15,$ps16,$ps17,$ps18,$ps19,$ps20,$ps21,$ps22,$ps23,$ps24,$ps25,$ps26,$ps27,$ps28,$ps29,$ps30,$prec) = split(/<>/);
		if($in{'id'} eq "$pid" && $in{'pass'} eq "$ppass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	$pdai = int(($pn_0+$pn_1+$pn_2+$pn_3+$pn_4+$pn_5+$pn_6+$plp) / 8) * $kun_point;

	if($in{'prm_no'} eq "0") {$pgold = $pn_0 * $pdai;}
	elsif($in{'prm_no'} eq "1") {$pgold = $pn_1 * $pdai;}
	elsif($in{'prm_no'} eq "2") {$pgold = $pn_2 * $pdai;}
	elsif($in{'prm_no'} eq "3") {$pgold = $pn_3 * $pdai;}
	elsif($in{'prm_no'} eq "4") {$pgold = $pn_4 * $pdai;}
	elsif($in{'prm_no'} eq "5") {$pgold = $pn_5 * $pdai;}
	elsif($in{'prm_no'} eq "6") {$pgold = $pn_6 * $pdai;}
	elsif($in{'prm_no'} eq "7") {$pgold = $plp * $pdai;}
	elsif($in{'prm_no'} eq "8") {$pgold = $pmaxhp * $kun_point;}
	else{&error("訓練するパラメータを選択してください！"); }

	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi");
	@kunren_chara = <IN>;
	close(IN);

	$hit=0;@kunren_new=();
	foreach(@kunren_chara){
		($poid,$popass,$posite,$pourl,$poname,$posex,$pochara,$pon_0,$pon_1,$pon_2,$pon_3,$pon_4,$pon_5,$pon_6,$posyoku,$pohp,$pomaxhp,$poex,$polv,$pogold,$polp,$pototal,$pokati,$powaza,$poitem,$pomons,$pohost,$podate,$pomori,$podef,$potac,$pacsno,$pmoriturn,$pcllv,$ps0,$ps1,$ps2,$ps3,$ps4,$ps5,$ps6,$ps7,$ps8,$ps9,$ps10,$ps11,$ps12,$ps13,$ps14,$ps15,$ps16,$ps17,$ps18,$ps19,$ps20,$ps21,$ps22,$ps23,$ps24,$ps25,$ps26,$ps27,$ps28,$ps29,$ps30,$prec) = split(/<>/);
		if($poid eq "$pid") {
			if($pogold < $pgold) { &error("お金が足りません"); }
			else { $pogold -= $pgold; }
		$points = int(rand(8))+1;
		if($in{'prm_no'} eq "0") { $pon_0 += $points; $t1 = 1;}
		elsif($in{'prm_no'} eq "1") { $pon_1 += $points; $t2 = 1;}
		elsif($in{'prm_no'} eq "2") { $pon_2 += $points; $t3 = 1;}
		elsif($in{'prm_no'} eq "3") { $pon_3 += $points; $t4 = 1;}
		elsif($in{'prm_no'} eq "4") { $pon_4 += $points; $t5 = 1;}
		elsif($in{'prm_no'} eq "5") { $pon_5 += $points; $t6 = 1;}
		elsif($in{'prm_no'} eq "6") { $pon_6 += $points; $t7 = 1;}
		elsif($in{'prm_no'} eq "7") { $polp += $points; $t8 = 1;}
		elsif($in{'prm_no'} eq "8") { $pomaxhp += $pon_3; $t9 = 1;}
		if($pon_0 > $charamaxpm)  { $pon_0 = $charamaxpm;$t1 = 0;$comment .= "力はもう最大値に達しています。";}
		if($pon_1 > $charamaxpm)  { $pon_1 = $charamaxpm;$t2 = 0;$comment .= "魔力はもう最大値に達しています。";}
		if($pon_2 > $charamaxpm)  { $pon_2 = $charamaxpm;$t3 = 0;$comment .= "信仰心はもう最大値に達しています。";}
		if($pon_3 > $charamaxpm)  { $pon_3 = $charamaxpm;$t4 = 0;$comment .= "生命力はもう最大値に達しています。";}
		if($pon_4 > $charamaxpm)  { $pon_4 = $charamaxpm;$t5 = 0;$comment .= "器用さはもう最大値に達しています。";}
		if($pon_5 > $charamaxpm)  { $pon_5 = $charamaxpm;$t6 = 0;$comment .= "速さはもう最大値に達しています。";}
		if($pon_6 > $charamaxpm)  { $pon_6 = $charamaxpm;$t7 = 0;$comment .= "魅力はもう最大値に達しています。";}
		if($polp  > $charamaxpm)  { $polp  = $charamaxpm;$t8 = 0;$comment .= "カルマはもう最大値に達しています。";}
		if($pomaxhp > $charamaxhp)  { $pomaxhp  = $charamaxhp;$t9 = 0;$comment .= "ＨＰはもう最大値に達しています。";}
		if($t1) { $comment .= "力が$points上がった。"; }
		if($t2) { $comment .= "魔力が$points上がった。"; }
		if($t3) { $comment .= "信仰心が$points上がった。"; }
		if($t4) { $comment .= "生命力が$points上がった。"; }
		if($t5) { $comment .= "器用さが$points上がった。"; }
		if($t6) { $comment .= "速さが$points上がった。"; }
		if($t7) { $comment .= "魅力が$points上がった。"; }
		if($t8) { $comment .= "カルマが$points上がった。"; }
		if($t9) { $comment .= "ＨＰが$pon_3上がった。"; }
			unshift(@kunren_new,"$poid<>$popass<>$posite<>$pourl<>$poname<>$posex<>$pochara<>$pon_0<>$pon_1<>$pon_2<>$pon_3<>$pon_4<>$pon_5<>$pon_6<>$posyoku<>$pohp<>$pomaxhp<>$poex<>$polv<>$pogold<>$polp<>$pototal<>$pokati<>$powaza<>$poitem<>$pomons<>$host<>$podate<>$pomori<>$podef<>$potac<>$pacsno<>$pmoriturn<>$pcllv<>$ps0<>$ps1<>$ps2<>$ps3<>$ps4<>$ps5<>$ps6<>$ps7<>$ps8<>$ps9<>$ps10<>$ps11<>$ps12<>$ps13<>$ps14<>$ps15<>$ps16<>$ps17<>$ps18<>$ps19<>$ps20<>$ps21<>$ps22<>$ps23<>$ps24<>$ps25<>$ps26<>$ps27<>$ps28<>$ps29<>$ps30<>$prec<>\n");
			$hit=1;
		}else{
			push(@kunren_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @kunren_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

        open(IN,"./charalog/$in{'id'}.cgi");
	@kunren = <IN>;
	close(IN);

	foreach(@kunren){
		($pid,$ppass,$psite,$purl,$pname,$psex,$pchara,$pon_0,$pon_1,$pon_2,$pon_3,$pon_4,$pon_5,$pon_6,$psyoku,$php,$pomaxhp,$pex,$plv,$pgold,$polp,$ptotal,$pkati,$pwaza,$pitem,$pmons,$phost,$pdate,$pmori,$pdef,$ptac,$pacsno,$pmoriturn,$pcllv,$ps0,$ps1,$ps2,$ps3,$ps4,$ps5,$ps6,$ps7,$ps8,$ps9,$ps10,$ps11,$ps12,$ps13,$ps14,$ps15,$ps16,$ps17,$ps18,$ps19,$ps20,$ps21,$ps22,$ps23,$ps24,$ps25,$ps26,$ps27,$ps28,$ps29,$ps30,$prec) = split(/<>/);
		if($in{'id'} eq "$pid" && $in{'pass'} eq "$ppass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	$pdai = int(($pon_0+$pon_1+$pon_2+$pon_3+$pon_4+$pon_5+$pon_6+$polp) / 8) * $kun_point;
	$prm0_gold = $pon_0 * $pdai;
	$prm1_gold = $pon_1 * $pdai;
	$prm2_gold = $pon_2 * $pdai;
	$prm3_gold = $pon_3 * $pdai;
	$prm4_gold = $pon_4 * $pdai;
	$prm5_gold = $pon_5 * $pdai;
	$prm6_gold = $pon_6 * $pdai;
	$prm7_gold = $polp * $pdai;
	$prm8_gold = $pomaxhp * $kun_point;

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>$comment</h1>
<BR>もっと潜在\能\力を引き出してやろうか？。
<br><hr>現在の所持金：$pogold Ｇ<br>
<form action="$scripts" method="post">
<input type=radio name=prm_no value=0 selected>力   を鍛える($pon_0/$charamaxpm)$prm0_gold Ｇ<br>
<input type=radio name=prm_no value=1>魔力を鍛える($pon_1/$charamaxpm)$prm1_gold Ｇ<br>
<input type=radio name=prm_no value=2>信仰心を鍛える($pon_2/$charamaxpm)$prm2_gold Ｇ<br>
<input type=radio name=prm_no value=3>生命力を鍛える($pon_3/$charamaxpm)$prm3_gold Ｇ<br>
<input type=radio name=prm_no value=4>器用さを鍛える($pon_4/$charamaxpm)$prm4_gold Ｇ<br>
<input type=radio name=prm_no value=5>速さ　を鍛える($pon_5/$charamaxpm)$prm5_gold Ｇ<br>
<input type=radio name=prm_no value=6>魅力　を鍛える($pon_6/$charamaxpm)$prm6_gold Ｇ<br>
<input type=radio name=prm_no value=7>カルマを鍛える($polp/$charamaxpm)$prm7_gold Ｇ<br>
<input type=radio name=prm_no value=8>ＨＰ　を鍛える($pomaxhp/$charamaxhp)$prm8_gold Ｇ<br>
<input type=hidden name=id value=$pid>
<input type=hidden name=pass value=$ppass>
<input type=hidden name=mode value=kunrenok>
<input type=submit class=btn value="更に訓練する">
</form>
<a href="$script?mode=log_in&id=$pid&pass=$ppass">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>$comment</h1>
<BR>もっと潜在\能\力を引き出してやろうか？。
<br><hr>現在の所持金：$pgold Ｇ<br>
<form action="$scripts" method="post">
<table>
<tr><th></th><th>No.</th><th>鍛えたいパラメータ</th><th>現在値</th><th>最大値</th><th>価格</th></tr>
<tr><td class=b1><input type=radio name=prm_no value=0 selected></td><td align=right class=b1>0001</td><td class=b1>力   を鍛える</td><td class=b1>$pon_0</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm0_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=1></td><td align=right class=b1>0002</td><td class=b1>魔力を鍛える</td><td class=b1>$pon_1</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm1_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=2></td><td align=right class=b1>0003</td><td class=b1>信仰心を鍛える</td><td class=b1>$pon_2</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm2_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=3></td><td align=right class=b1>0004</td><td class=b1>生命力を鍛える</td><td class=b1>$pon_3</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm3_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=4></td><td align=right class=b1>0005</td><td class=b1>器用さを鍛える</td><td class=b1>$pon_4</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm4_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=5></td><td align=right class=b1>0006</td><td class=b1>速さ　を鍛える</td><td class=b1>$pon_5</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm5_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=6></td><td align=right class=b1>0007</td><td class=b1>魅力　を鍛える</td><td class=b1>$pon_6</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm6_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=7></td><td align=right class=b1>0008</td><td class=b1>カルマを鍛える</td><td class=b1>$polp</td><td class=b1>$charamaxpm</td><td align=right class=b1>$prm7_gold Ｇ</td></tr>
<tr><td class=b1><input type=radio name=prm_no value=8></td><td align=right class=b1>0009</td><td class=b1>ＨＰ　を鍛える</td><td class=b1>$pomaxhp</td><td class=b1>$charamaxhp</td><td align=right class=b1>$prm8_gold Ｇ</td></tr>
</table>
<input type=hidden name=id value=$pid>
<input type=hidden name=pass value=$ppass>
<input type=hidden name=mode value=kunrenok>
<input type=submit class=btn value="更に訓練する">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$pid>
<input type=hidden name=pass value=$ppass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	acs_shop => <<'__SUB__',
#----------------#
#アクセサリー表示#
#----------------#
sub acs_shop {

	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$acssell_file");
	@logsell_acs = <IN>;
	close(IN);

	$hit=0;
	foreach(@logsell_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
		if($kacsno eq "$a_no"){ $hit=1;last; }
	}
	if(!$hit) { $a_name="-"; $a_gold=0;$a_0up=0;$a_1up=0;$a_2up=0;$a_3up=0;$a_4up=0;$a_5up=0;$a_6up=0;$a_lpup=0;$a_hitup=0;$a_kaihiup=0;$a_wazaup=0;}

	$ui_gold = int($a_gold / 3) * 2;

	open(IN,"$acs_file[$ksyoku]");
	@acs_array = <IN>;
	close(IN);

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>アクセサリーショップ</h1>
<hr size=0>
<br><hr>現在の所持金：$kgold Ｇ<br>
<form action="$scripts" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=acs_sell>
<input type=submit class=btn value="売る"></form>
<br>現在の装備品：$a_name／$ui_gold G<br><form action="$scripts" method="post">
EOM

	foreach(@acs_array){
		($ai_no,$ai_name,$ai_gold,$ai_kouka,$ai_0up,$ai_1up,$ai_2up,$ai_3up,$ai_4up,$ai_5up,$ai_6up,$ai_lpup,$ai_hitup,$ai_kaihiup,$ai_wazaup) = split(/<>/);
		print "<a href=\"$scripts?mode=acs_buy&id=$kid&pass=$kpass&acs_no=$ai_no\">$ai_name：($ai_gold G)</a><br>\n";
	}

	print "<p><a href=\"$script?mode=log_in&id=$kid&pass=$kpass\">&#63873;</a>";
	}else{
	print <<"EOM";
<h1>アクセサリーショップ</h1>
<hr size=0>
<p>
<form action="$scripts" method="post">
<FONT SIZE=3>
<B>不気味な主人</B><BR>
「ふっ。。冷やかしならさっさと帰りな。。。<BR>
　ん？、おまえ<B>$kname</B>じゃないか。
<BR>おまえ柄にもなく$chara_syoku[$ksyoku]をやってるらしいじゃないか。。。
<BR>
この店の品物をおまえごときが使えこなせると思っているのか？
<BR><BR>で、どれを買うんだ？」
</FONT>
<br><hr>現在の所持金：$kgold Ｇ<br>
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>価格</th><th>説明</th></tr>
<tr><th><input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=acs_sell>
<input type=submit class=btn value="売る">
</th></form><th>現在の装備品</th><th>$a_name</th><th>$ui_gold</th><form action="$scripts" method="post">
EOM

	foreach(@acs_array){
		($ai_no,$ai_name,$ai_gold,$ai_kouka,$ai_0up,$ai_1up,$ai_2up,$ai_3up,$ai_4up,$ai_5up,$ai_6up,$ai_lpup,$ai_hitup,$ai_kaihiup,$ai_wazaup,$ai_msg) = split(/<>/);
		print "<tr>\n";
		print "<td class=b1><input type=radio name=acs_no value=\"$ai_no\"></td><td align=right class=b1>$ai_no</td><td class=b1>$ai_name</td><td align=right class=b1>$ai_gold</td><td align=left>$ai_msg</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<p>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=acs_buy>
<input type=submit class=btn value="アクセサリーを買う">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	acs_buy => <<'__SUB__',
#----------------#
#アクセサリー買う#
#----------------#
sub acs_buy {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	$hit=0;
	open(IN,"$acs_file[$ksyoku]");
	@log_acs = <IN>;
	close(IN);

	foreach(@log_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
		if($in{'acs_no'} eq "$a_no"){ $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }

	&get_host;

	$date = time();

	$hit=0;@def_new=();
	foreach(@bougu){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			if($igold < $a_gold) { &error("お金が足りません"); }
			else { $igold = $igold - $a_gold; }
			unshift(@def_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<>$a_no<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@def_new,"$_");
		}
	}


	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @def_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>アクセサリーを買いました</h1>
<hr size=0>
<a href="$script?mode=log_in&id=$kid&pass=$kpass">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>アクセサリーを買いました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	acs_sell => <<'__SUB__',
#----------------#
#アクセサリー売る#
#----------------#
sub acs_sell {


	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }


	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	$hit=0;
	open(IN,"$acs_file");
	@log_acs = <IN>;
	close(IN);

	foreach(@log_acs){
		($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
		if($kacsno eq "$a_no"){ $hit=1;last; }
	}

	if(!$hit) { &error("そんなアイテムは存在しません"); }
	if(!$kacsno) { &error("そんなアイテムは存在しません"); }
	$ui_gold = int($a_gold / 3) * 2;

	&get_host;

	$date = time();

	$hit=0;@def_new=();
	foreach(@bougu){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
			$igold = $igold + $ui_gold;
			if($igold > $gold_max){$igold = $gold_max;}
			unshift(@def_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$host<>$idate<>$imori<>$idef<>$itac<><>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
			$hit=1;
		}else{
			push(@def_new,"$_");
		}
	}

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @def_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>アクセサリーを売りました</h1>
<hr size=0>
<a href="$script?mode=log_in&id=$kid&pass=$kpass">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>アクセサリーを売りました</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	save_data => <<'__SUB__',
#----------------#
#記憶の教会      #
#----------------#
sub save_data {

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);
	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" && $in{'pass'} eq "$kpass") { $hit=1;last; }
	}
	if(!$hit) {&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(OUT,">./savelog/$in{'id'}.cgi");
	print OUT @bougu;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>記憶の教会</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<FONT SIZE=3>
<B>神父さま</B><BR>
「あなたのこれまでの記憶を、ここに記しました。。<BR>
もしそなたが記憶を無くしたとき、全ての所持金と引き換えに<br>
記憶を取り戻すことができるであろう。。。」<br>
<a href="$script?mode=log_in&id=$kid&pass=$kpass">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>記憶の教会</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<FONT SIZE=3>
<B>神父さま</B><BR>
「あなたのこれまでの記憶を、ここに記しました。。<BR>
もしそなたが記憶を無くしたとき、全ての所持金と引き換えに<br>
記憶を取り戻すことができるであろう。。。」<br>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

	&footer;

	exit;
}
__SUB__

	load_game => <<'__SUB__',
#----------------#
#記憶の教会再開  #
#----------------#
sub load_game {
	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./savelog/$in{'id'}.cgi");
	@bougu = <IN>;
	close(IN);

	$hit=0;@new=();
	foreach(@bougu){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid") {
			# パスワードを照合
			$match = &decrypt("$in{'pass'}","$kpass");
			if ($match ne 'yes') {
		if($in{'pass'} ne $kpass){&error("パスワードが違います！"); }}
			$kex = 0;
			$kgold = 0;
			unshift(@new,"$kid<>$kpass<>$ksite<>$kurl<>$kname<>$ksex<>$kchara<>$kn_0<>$kn_1<>$kn_2<>$kn_3<>$kn_4<>$kn_5<>$kn_6<>$ksyoku<>$khp<>$kmaxhp<>$kex<>$klv<>$kgold<>$klp<>$ktotal<>$kkati<>$kwaza<>$kitem<>$kmons<>$host<>$date<>$kmori<>$kdef<>$ktac<>$kacsno<>$kmoriturn<>$kcllv<>$ks0<>$ks1<>$ks2<>$ks3<>$ks4<>$ks5<>$ks6<>$ks7<>$ks8<>$ks9<>$ks10<>$ks11<>$ks12<>$ks13<>$ks14<>$ks15<>$ks16<>$ks17<>$ks18<>$ks19<>$ks20<>$ks21<>$ks22<>$ks23<>$ks24<>$ks25<>$ks26<>$ks27<>$ks28<>$ks29<>$ks30<>$krec<>\n");
			$hit=1;
			last;
		}
	}
	if(!$hit) { &error("記憶の教会にあなたの記録がありません");}

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @new;
	close(OUT);

	open(IN,"./banklog/$in{'id'}.cgi");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($i_no,$i_pass,$i_gold) = split(/<>/);
	if($i_no eq "$in{'id'}") {
		$i_gold = 0;
		unshift(@item_new,"$i_no<>$i_pass<>$i_gold<>\n");
		$hit=1;
	}else{
		push(@item_new,"$_");
		}
	}

	if(!$hit){
		unshift(@item_new,"$in{'id'}<>$in{'pass'}<>0<>\n");
	}

	open(OUT,">./banklog/$in{'id'}.cgi");
	print OUT @item_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	$m_charafile2="./charalog2/$in{'id'}.cgi";
	if(-e $m_charafile2){unlink($m_charafile2);}

	&header;

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
	print <<"EOM";
<h1>記憶の教会</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<FONT SIZE=3>
<B>神父さま</B><BR>
「おお！$knameよ。。。記憶を失ったしまったのか？<BR>
ボタン連打や、更新ボタンをプレイ中に押すと記憶が無くなったしまうのじゃ。。。<br>
気をつけるが良い。。。
記憶を失うと、銀行の預金通帳や所持金を奪われるだけでなく、今まで手に入れた勲章も全て失う事になってしまうからのぉ。。。」<br>
<a href="$script?mode=log_in&id=$kid&pass=$kpass">&#63873;</a>
EOM
	}else{
	print <<"EOM";
<h1>記憶の教会</h1>
<hr size=0>
<p>
<form action="$script" method="post">
<FONT SIZE=3>
<B>神父さま</B><BR>
「おお！$knameよ。。。記憶を失ったしまったのか？<BR>
ボタン連打や、更新ボタンをプレイ中に押すと記憶が無くなったしまうのじゃ。。。<br>
気をつけるが良い。。。
記憶を失うと、銀行の預金通帳や所持金を奪われるだけでなく、今まで手に入れた勲章も全て失う事になってしまうからのぉ。。。」<br>
<form action="$script" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	}

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

	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname,$wmori,$wdef,$wtac,$wacsno,$wmoriturn,$wcllv,$ws0,$ws1,$ws2,$ws3,$ws4,$ws5,$ws6,$ws7,$ws8,$ws9,$ws10,$ws11,$ws12,$ws13,$ws14,$ws15,$ws16,$ws17,$ws18,$ws19,$ws20,$ws21,$ws22,$ws23,$ws24,$ws25,$ws26,$ws27,$ws28,$ws29,$ws30,$wrec) = split(/<>/,$winner[0]);
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

	footer => <<'__SUB__',
#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {
	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {
		print "<a href=\"$scripto\">TOP</a>\n";
		print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
		 print "FFA Emilia Ver1.01 remodeling by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Classic</a><br>(配布停止中)<br>\n";
        print "$vergj remodeling by <a href=\"http://www5b.biglobe.ne.jp/~jun-kei/\" target=\"_top\">jun-k</a><br>\n";
        print "チョコボレース v1.00 edit by <a href=\"http://www8.big.or.jp/~k-kiku/ff/index.html\" target=\"_top\">Laldar</a><br>\n";
	print "チョコボレース(改） v1.01 edit by <a href=\"http://www5d.biglobe.ne.jp/~sprite/\" target=\"_top\">Emilia</a><br>\n";

	print "$verg remodeling by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";
	print "$ver by <a href=\"http://www.interq.or.jp/sun/cumro/\">D.Takamiya(CUMRO)</a><br>\n";
        print "飛空艇 edit by <a href=\"http://tender.rose.ne.jp/\" target=\"_top\">Tender Net</a><br>\n";
	}
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
  background-image : url($shop_back);
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
	print "<link rel=\"stylesheet\" href=\"$style_sheet\" type\"text.css\">\n";
	print "<title>$main_title</title></head>\n";
	print "<body background=\"$shop_back\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	print "<embed src=\"$shop_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__
);
}
