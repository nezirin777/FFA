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
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#
# 日本語ライブラリの読み込み
require './jacode.pl';

# レジストライブラリの読み込み
require './regist.pl';

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
if($mode eq 'ikusei_shop') { &ikusei_shop; }
elsif($mode eq 'ikusei_buy') { &ikusei_buy; }
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
	ikusei_shop => <<'__SUB__',
#----------------#
# お店　表示 　　#
#----------------#
sub ikusei_shop {

	open(IN,"./charalog/$in{'id'}.cgi");
	@omise_in = <IN>;
	close(IN);

	foreach(@omise_in){
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
	if($cy_life > 99) { &error("満腹なのでエサは必要ありません。");}

	$cspeed = int($cy_sp + $cy_5);
	open(IN,"$yasai_file");
	@yasai_array = <IN>;
	close(IN);

	&header;

	print <<"EOM";
<h1>やさい農場</h1>
<hr size=0>
<p>
<FONT SIZE=3>
<B>農場のおばさん</B><BR>
「<b>$kname</b>さんいらっしゃい。<br>
かわいいチョコボに野菜はどうだい？<br>
無農薬だから栄養満点だよ、ちょっと高いけどね。」<br>

<font Size="3"> $knameさんの所持金 ： <b>$kgold</b>　ギル
</font><p>
<br><br>
<table border=0>
<td rowspan=3 class="b2" align="center" width=60 height=60><img src="$img_path/$choco_img[$cy_no]" ></td>
<td class="b2" id="td2"><b>名前</b></td><td  class="b2"><b>$cy_name</b></td>
<tr>
<td class="b2" id="td2"><b>スピード</b></td><td class="b2"><b>$cspeed</b></td>
<tr>
<td class="b2" id="td2"><b>スタミナ</b></td><td class="b2"><b>$cy_sta\/$cy_maxsta</b></td>
</table>
<table border=1>
<tr>
<th class="b2"></th><th class="b2">No.</th><th class="b2">なまえ</th><th class="b2">値段</th><th class="b2">説明</th></tr>
<tr><form action="$scriptiku" method="post">
EOM

	foreach(@yasai_array){
		($ya_no,$ya_name,$ya_gold,$ya_setu) = split(/<>/);
		print "<tr>\n";
		print "<td class=\"b2\"><input type=radio name=item_no value=\"$ya_no\"></td><td align=right class=\"b2\">$ya_no</td><td class=\"b2\">$ya_name</td><td align=center class=\"b2\">$ya_gold</td><td align=center class=\"b2\">$ya_setu</td>\n";
		print "</tr>\n";
	}

	print <<"EOM";
</tr>
</table>
<p>
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$kpass>
<input type=hidden name=mode value=ikusei_buy>
<input type=submit class=btn value="野菜をチョコボに与える">
</form>
EOM
	&footer;

	exit;
}
__SUB__

	ikusei_buy => <<'__SUB__',
#----------------#
#  購入後処理　  #
#----------------#
sub ikusei_buy {

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"./charalog/$in{'id'}.cgi");
	@yasai_in = <IN>;
	close(IN);

	foreach(@yasai_in){
		($kid,$kpass,$ksite,$kurl,$kname,$ksex,$kchara,$kn_0,$kn_1,$kn_2,$kn_3,$kn_4,$kn_5,$kn_6,$ksyoku,$khp,$kmaxhp,$kex,$klv,$kgold,$klp,$ktotal,$kkati,$kwaza,$kitem,$kmons,$khost,$kdate,$kmori,$kdef,$ktac,$kacsno,$kmoriturn,$kcllv,$ks0,$ks1,$ks2,$ks3,$ks4,$ks5,$ks6,$ks7,$ks8,$ks9,$ks10,$ks11,$ks12,$ks13,$ks14,$ks15,$ks16,$ks17,$ks18,$ks19,$ks20,$ks21,$ks22,$ks23,$ks24,$ks25,$ks26,$ks27,$ks28,$ks29,$ks30,$krec) = split(/<>/);
		if($in{'id'} eq "$kid" and $in{'pass'} eq "$kpass") { last; }
	}

	if($in{'id'} ne "$kid" or $in{'pass'} ne "$kpass"){&error("オープンエラー、ID・パスワードが正しくありません。");}

	open(IN,"$chocolog_file");
	@choco_in = <IN>;
	close(IN);

	foreach(@choco_in){
	($cy_id,$cy_pass,$cy_kname,$cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($kid eq "$cy_id"){ $hit=1;last; }
	}

	open(IN,"$yasai_file");
	@yasai_array = <IN>;
	close(IN);

	$hit=0;
	foreach(@yasai_array){
		($ya_no,$ya_name,$ya_gold,$ya_setu) = split(/<>/);
		if($in{'item_no'} eq "$ya_no") { $hit=1;last; }
	}
	if(!$hit) { &error("そんなアイテムは存在しません"); }
	if($kgold < $ya_gold) { &error("お金が足りません"); }

#代金徴収
	$nowgold = $kgold - $ya_gold;
	$now_waza = $cy_waza;

	if($ya_no == 1){
#ギザールの野菜（健康状態だけのランダム）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";

#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "おいしそうにたべた。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life +40;
		}elsif($status == 1){
		$com .= "とりあえずたべた。\n";
		$com1 .="よしよし。\n";
		$nowlife = $cy_life + 20;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="うーん。残さず食べてくれよー。\n";
		$nowlife = $cy_life + 10;
		}

	}elsif($ya_no == 2){
#シルキスの野菜（力がアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_0 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "よく噛んで食べている。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life + 10;
		$now_0 = $cy_0 + 50;
		}elsif($status == 1){
		$com .= "ちょっと食べにくそうだ。\n";
		$com1 .="硬いもんな。\n";
		$nowlife = $cy_life + 5;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="硬いもんな・・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 3){
#レイゲンの野菜（知能か信仰心がアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_1 = "";
	$now_2 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "とてもすっぱそうだが全部食べた。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life + 20;
		$now_1 = $cy_1 + 50;
		}elsif($status == 1){
		$com .= "とてもすっぱそうだが全部食べた。\n";
		$com1 .="えらいぞ。\n";
		$now_2 = $cy_2 + 50;
		$nowlife = $cy_life + 20;
		}elsif($status == 2){
		$com .= "すっぱそうな顔をしている。\n";
		$com1 .="クチをすぼめてるな。\n";
		$nowlife = $cy_life + 10;
		}else{
		$com .= "すっぱそうな顔をしている。\n";
		$com1 .="あ、残した・・・。\n";
		$nowlife = $cy_life + 5;
		}
	}elsif($ya_no == 4){
#ミメットの野菜（スタミナがアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_maxsta = "";
	$now_5 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "ペロリと平らげた。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life + 5;
		$now_maxsta = $cy_maxsta + int(rand(100) + 10);
		$now_5 = $cy_5 - 1;
		}elsif($status == 1){
		$com .= "とりあえず食べた。\n";
		$com1 .="あまり食うと太るかも。\n";
		$nowlife = $cy_life + 3;
		$now_maxsta = $cy_maxsta + int(rand(50) + 5);
		$now_5 = $cy_5 - 1;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="甘いのイヤかな・・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 5){
#クーリエの野菜（生命力がアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_3 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "結局全部食べた。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life + 20;
		$now_3 = $cy_3 + 50;
		}elsif($status == 1){
		$com .= "にがそうに食べた。\n";
		$com1 .="お水あげよう・・・。\n";
		$nowlife = $cy_life + 10;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="苦いもんな・・・。\n";
		$nowlife = $cy_life + 5;
		}
	}elsif($ya_no == 6){
#パサーナの野菜（早さがアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_5 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "残さず全部食べた。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life + 5;
		$now_5 = $cy_5 + 50;
		}elsif($status == 1){
		$com .= "ちょっと食べにくそうだ。\n";
		$com1 .="パサパサしてるもんな。\n";
		$nowlife = $cy_life + 3;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="こういうのダメかな・・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 7){
#タンタルの野菜（器用さがアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_4 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "ポリポリと全部食べた。\n";
		$com1 .="よかったよかった。\n";
		$nowlife = $cy_life + 10;
		$now_4 = $cy_4 + 50;
		}elsif($status == 1){
		$com .= "ちょっと食べにくそうだ。\n";
		$com1 .="食べにくそうだし。\n";
		$nowlife = $cy_life + 5;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="あ、残しちゃった・・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 8){
#カラッカの野菜（魅力がアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_6 = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "全部たべた。\n";
		$com1 .="肌にツヤがでてきたような。\n";
		$nowlife = $cy_life + 5;
		$now_6 = $cy_6 + 50;
		}elsif($status == 1){
		$com .= "とりあえず食べた。\n";
		$com1 .="よしよし。\n";
		$nowlife = $cy_life + 3;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="こういうのダメなのかな・・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 9){
#ミシディアの野菜（根性がアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_kon = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "ガリガリと気合で食べた。\n";
		$com1 .="おお！！気合はいってるなぁ～。\n";
		$nowlife = $cy_life + 5;
		$now_kon = $cy_kon + 50;
		}elsif($status == 1){
		$com .= "とりあえず食べた。\n";
		$com1 .="よしよし。\n";
		$nowlife = $cy_life + 3;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="めちゃめちゃ硬いもんなぁ・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 10){
#エリクサーの野菜（すべてのステータスががアップ）
	$atai = 5;
	$status = "";
	$com = "";
	$com1 = "";
	$nowlife = "";
	$now_kon = "";
        $now_6 = "";
        $now_5 = "";
        $now_4 = "";
        $now_3 = "";
        $now_2 = "";
        $now_1 = "";
        $now_0 = "";
        $now_maxsta = "";
#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "不思議そうな顔をしてたいらげた。\n";
		$com1 .="うおぉぉぉ！！！！。\n";
		$nowlife = $cy_life + 5;
		$now_kon = $cy_kon + 50;
                $now_6 = $cy_6 + 70;
                $now_5 = $cy_5 + 70;
                $now_4 = $cy_4 + 70;
                $now_3 = $cy_3 + 70;
                $now_2 = $cy_2 + 70;
                $now_1 = $cy_1 + 70;
                $now_0 = $cy_0 + 70;
                $now_maxsta = $cy_maxsta + int(rand(500) + 50);
		}elsif($status == 1){
		$com .= "とりあえず食べた。\n";
		$com1 .="よしよし。\n";
		$nowlife = $cy_life + 3;
		}else{
		$com .= "あまり食がすすまなかったようだ。\n";
		$com1 .="高いんだから全部たべてよぉ～TT・・。\n";
		$nowlife = $cy_life + 1;
		}
	}elsif($ya_no == 11){
#不思議な野菜（脚質改善）
	$atai = 20;
	$now_waza = "";
	$nowlife = $cy_life + 0;

#ランダムスタート
	$status = int(rand($atai));

		if($status == 0){
		$com .= "そわそわしだしたぞ。\n";
		$com1 .="おしっこでも我慢してるのかな？\n";
		$now_waza = 3;
		}elsif($status == 1){
		$com .= "のんびり屋さんだなぁ。\n";
		$com1 .="めちゃくちゃゆっくりと食べてるよ。\n";
		$now_waza = 5;
		}elsif($status == 2){
		$com .= "そう急がないでよぉぉ。\n";
		$com1 .="すぐになくなっちゃった。\n";
		$now_waza = 2;
		}elsif($status == 3){
		$com .= "美味しそうな顔して食べるねぇ。\n";
		$com1 .="好物なのかな？\n";
		$now_waza = 4;
		}elsif($status == 4){
		$com .= "そわそわしだしたぞ。\n";
		$com1 .="おしっこでも我慢してるのかな？\n";
		$now_waza = 3;
		}elsif($status == 5){
		$com .= "のんびり屋さんだなぁ。\n";
		$com1 .="めちゃくちゃゆっくりと食べてるよ。\n";
		$now_waza = 5;
		}elsif($status == 6){
		$com .= "そう急がないでよぉぉ。\n";
		$com1 .="すぐになくなっちゃった。\n";
		$now_waza = 2;
		}elsif($status == 7){
		$com .= "美味しそうな顔して食べるねぇ。\n";
		$com1 .="好物なのかな？\n";
		$now_waza = 4;
		}elsif($status == 8){
		$com .= "そわそわしだしたぞ。\n";
		$com1 .="おしっこでも我慢してるのかな？\n";
		$now_waza = 3;
		}elsif($status == 9){
		$com .= "のんびり屋さんだなぁ。\n";
		$com1 .="めちゃくちゃゆっくりと食べてるよ。\n";
		$now_waza = 5;
		}elsif($status == 10){
		$com .= "そう急がないでよぉぉ。\n";
		$com1 .="すぐになくなっちゃった。\n";
		$now_waza = 2;
		}elsif($status == 11){
		$com .= "美味しそうな顔して食べるねぇ。\n";
		$com1 .="好物なのかな？\n";
		$now_waza = 4;
		}elsif($status == 12){
		$com .= "不思議そうな顔してるな。\n";
		$com1 .="不思議だな？\n";
		$now_waza = 0;
		}else{
		$com .= "なんだか普通だなぁ。\n";
		$com1 .="何の感想もないのかな？。\n";
		$now_waza = 1;
		}
	}
	&header;

	open(IN,"$chocolog_file");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($cy_id,$cy_pass,$cy_kname,$cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($kid eq "$cy_id") {
			$cy_life = $nowlife;
			$cy_waza = $now_waza;
			if($now_0 !=0){$cy_0 = $now_0;}
			if($now_1 !=0){$cy_1 = $now_1;}
			if($now_2 !=0){$cy_2 = $now_2;}
			if($now_3 !=0){$cy_3 = $now_3;}
			if($now_4 !=0){$cy_4 = $now_4;}
			if($now_5 !=0){$cy_5 = $now_5;}
			if($now_6 !=0){$cy_6 = $now_6;}
			if($now_kon !=0){$cy_kon = $now_kon;}
                        if($now_maxsta !=0){$cy_maxsta = $now_maxsta;}

			unshift(@item_new,"$cy_id<>$cy_pass<>$cy_kname<>$cy_no<>$cy_name<>$cy_gold<>$cy_rank<>$cy_sp<>$cy_sta<>$cy_maxsta<>$cy_ex<>$cy_total<>$cy_kati<>$cy_0<>$cy_1<>$cy_2<>$cy_3<>$cy_4<>$cy_5<>$cy_6<>$cy_life<>$cy_kon<>$cy_waza<>$cy_money<>\n");
			$hit=1;
		}else{
			push(@item_new,"$_");
		}
	}

	if(!$hit){
	unshift(@item_new,"$cy_id<>$cy_pass<>$cy_kname<>$cy_no<>$cy_name<>$cy_gold<>$cy_rank<>$cy_sp<>$cy_sta<>$cy_maxsta<>$cy_ex<>$cy_total<>$cy_kati<>$cy_0<>$cy_1<>$cy_2<>$cy_3<>$cy_4<>$cy_5<>$cy_6<>$cy_life<>$cy_kon<>$cy_waza<>$cy_money<>\n");
	}

	open(OUT,">$chocolog_file");
	print OUT @item_new;
	close(OUT);

	open(IN,"./charalog/$in{'id'}.cgi");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($iid,$ipass,$isite,$iurl,$iname,$isex,$ichara,$in_0,$in_1,$in_2,$in_3,$in_4,$in_5,$in_6,$isyoku,$ihp,$imaxhp,$iex,$ilv,$igold,$ilp,$itotal,$ikati,$iwaza,$iitem,$imons,$ihost,$idate,$imori,$idef,$itac,$iacsno,$imoriturn,$icllv,$is0,$is1,$is2,$is3,$is4,$is5,$is6,$is7,$is8,$is9,$is10,$is11,$is12,$is13,$is14,$is15,$is16,$is17,$is18,$is19,$is20,$is21,$is22,$is23,$is24,$is25,$is26,$is27,$is28,$is29,$is30,$irec) = split(/<>/);
		if($iid eq "$kid") {
		$igold = $nowgold;
		unshift(@item_new,"$iid<>$ipass<>$isite<>$iurl<>$iname<>$isex<>$ichara<>$in_0<>$in_1<>$in_2<>$in_3<>$in_4<>$in_5<>$in_6<>$isyoku<>$ihp<>$imaxhp<>$iex<>$ilv<>$igold<>$ilp<>$itotal<>$ikati<>$iwaza<>$iitem<>$imons<>$ihost<>$idate<>$imori<>$idef<>$itac<>$iacsno<>$imoriturn<>$icllv<>$is0<>$is1<>$is2<>$is3<>$is4<>$is5<>$is6<>$is7<>$is8<>$is9<>$is10<>$is11<>$is12<>$is13<>$is14<>$is15<>$is16<>$is17<>$is18<>$is19<>$is20<>$is21<>$is22<>$is23<>$is24<>$is25<>$is26<>$is27<>$is28<>$is29<>$is30<>$irec<>\n");
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

	print <<"EOM";
<h1>野菜を与えました・・・。</h1>
<hr size=0>
<div align="center">
<br>
<b>$com</b><br>
<b>$com1</b><br><br>
所持金：$nowgold<br>
</div>
<form action="$scriptiku" method="post">
<input type=hidden name=id value=$kid>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=ikusei_shop>
<input type=submit class=btn value="もっと食べさせる">
</form>

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
	print "<input type=hidden name=id value=$kid>\n";
	print "<input type=hidden name=pass value=$in{'pass'}>\n";
	print "<input type=hidden name=mode value=log_in>\n";
	print "<input type=submit class=btn value=\"ステータス画面へ\">\n";
        print "<A HREF=\"$scripto\">ＴＯＰページへ</A>\n";
	print "</form>\n";
    print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right class=small>\n";
	 print "FFA Emilia・いく改ver1.00 remodeling by <a href=\"http://www3.big.or.jp/~icu/\" target=\"_top\">いく</a><br>\n";
	 print "画像提供 by <a href=\"http://www.wisnet.ne.jp/~jnkw/index.html\" target=\"_top\">Jinkun</a><br>\n";
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
	print "<embed src=\"$shop_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__


);
}
