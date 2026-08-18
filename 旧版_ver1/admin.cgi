#!/usr/local/bin/perl

#------------------------------------------------------#
# FF BATTLE de i 管理モードスクリプト
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#

#------------------------------------------------------#
#本スクリプトの作成者はjun-kですが、スクリプトの著作権はCUMROさん
#にあります、必要な著作権表示を消去して使用することはできません
#本スクリプトに関してのお問い合わせはjun-kまでお願いします。
#CUMROには絶対にしないで下さい。
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require './jacode.pl';

# レジストライブラリの読み込み
require './regist.pl';

# レジストライブラリの読み込み
require './sankasya.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

#管理人モードのパスワード
$kanripass = 'koboruto';

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
if($mode eq 'del_chara') { &del_chara;}
elsif($mode eq 'del_all') { &del_all;}
elsif($mode eq 'del_noplay') { &del_noplay;}
elsif($mode eq 'other_list') { &kanri_top;}
elsif($mode eq 'ip_list') { &kanri_top;}
else{&kanri_top;}

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
	kanri_top => <<'__SUB__',
#-----------------#
#  管理人モード   #
#-----------------#
sub kanri_top {

	if($in{'pass'} eq ""){&error("パスワードが入力されていません！！");}
	if($in{'pass'} ne $kanripass){&error("パスワードが違います！！");}

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

		if($entry=~/\.cgi/){
			open(IN,"./charalog/$entry");
			@WORK=<IN>;
			if($WORK[0] ne ""){
			push(@RANKING,"@WORK");
			}close(IN);
		}
	}
	closedir(DIR);

	@tmp1 = @tmp2 = ();
	if($mode eq 'other_list') {
		foreach (@RANKING) {
			my ($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$first,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
			if($rid){push(@RANK_NEW, $_);push(@tmp1, $rtotal);}
			}
	}elsif($mode eq 'ip_list') {
		foreach (@RANKING) {
			my ($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$first,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
			if($rid){push(@RANK_NEW, $_);push(@tmp1, $rhost);}
			}
	}else{
		foreach (@RANKING) {
			my ($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$first,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
			if($rid){push(@RANK_NEW, $_);push(@tmp1, $first);}
			}
		}
	@RANK_NEW = @RANK_NEW[sort {$tmp1[$b] <=> $tmp1[$a] } 0 .. $#tmp1];

	$ima = time();
	$sousu = @RANK_NEW;

	&header;

	print <<"EOM";
<h1>管理モード</h1><hr size=0>
※現在登録されているキャラクターをプレイ頻度が高い順に表\示しています。<br>
※一旦<b>削除</b>すると、二度と復元できなくなるので必ず<b>バックアップ</b>をとってから実行してください。
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=del_all>
<input type=submit class=btn value="全ログデータの削除">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=del_noplay>
<input type=submit class=btn value="プレイ日数を過ぎたキャラクターデータの完全削除">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="日付順に並び替え">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=other_list>
<input type=submit class=btn value="戦闘回数順に並び替え">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=ip_list>
<input type=submit class=btn value="ＩＰアドレス順に並び替え">
</form>
<hr size=0><p><table border=1>
<tr><th>NO</th><th>ログイン</th><th>キャラ名</th><th>ＩＤ</th><th>パスワード</th><th>サイト名</th><th>ＩＰアドレス</th><th>削除まで</th><th>戦闘回数</th><th>魔の森クリア数</th><th>預金額</th><th>教会</th><th>削除</th>
EOM
	$i=1;
	foreach (@RANK_NEW){
		($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$rdate,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
		$rdate = $rdate + (60*60*24*$limit);
		$niti = $rdate - $ima;
		$niti = int($niti / (60*60*24));
		if($niti==-11337){$niti_s="<font class=red>日付無し</font>";}else{$niti_s="<font class=yellow>$niti</font>日";}
		#銀行データ取得
		open(IN,"./banklog/$rid.cgi");
		@item_chara = <IN>;
		close(IN);
		@item_new=();$k_gold="0 G";
		foreach(@item_chara){
			($i_no,$i_pass,$i_gold) = split(/<>/);
			if($i_no){$k_gold="$i_gold G";}
			}
		#教会データ取得
		@item_new=();$s_data="<font class=blue>×</font>";
		open(IN,"./savelog/$rid.cgi");
		@bougu = <IN>;
		close(IN);
		foreach(@bougu){
			($s_id,$s_pass) = split(/<>/);
			if($i_no){$s_data="<font class=yellow>○</font>";}
			}

		print "<tr>\n";
	print <<"EOM";
<td align=left>$i</td>
<td align=center valign=center>
<form action="$script" method="post">
<input type=hidden name=mode value=log_in>
<input type=hidden name=id value=$rid>
<input type=hidden name=pass value=$rpass>
<input type=submit class=btn value="ログイン">
</td>
<td align=left></form><a href="$scripta?mode=chara_sts&id=$rid">$rname</a></td><td align=left>$rid</td><td align=left>$rpass</td><td align=left><a href=\"http\:\/\/$rurl\">$rsite</a></td>
EOM
	if($rhost==$wrhost){$wrhost=$rhost;$rhost="<font class=red>$rhost</font>";}
	print "<td align=left>$rhost</td>";
	print "<td align=left>$niti_s</td>";
	print "<td align=left>$rtotal</td>";

	print <<"EOM";
<td align=left>$rmoriturn</td>
<td align=right>$k_gold</td>
<td align=center>$s_data</td>
<td align=center valign=center>
<form action="$scriptk" method="post">
<input type="hidden" name=mode value=del_chara>
<input type=hidden name=id value=$rid>
<input type=hidden name=name value=$rname>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="削除">
</td></form>
EOM
		print "</tr>\n";
		$i++;
	}

	print "</table><p>\n";

	&footer;

	exit;

}
__SUB__

	del_all => <<'__SUB__',
#-----------------#
#  全ログ削除     #
#-----------------#
sub del_all {

	if($in{'pass'} eq ""){&error("パスワードが入力されていません！！");}
	if($in{'pass'} != $kanripass){&error("パスワードが違います！！");}

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

		open(IN,"./charalog/$entry");
		push(@RANKING,<IN>);
		close(IN);
	}
	closedir(DIR);

	$del_name="";$su=0;
	foreach (@RANKING){
		my ($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$rdate,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
		if($rid eq "test"){next;}
		$del_name.="<b>$rname</b>/";
		$su++;
		&del_file($rid);
		}
	&header;

	print <<"EOM";
<h1>下記のキャラデータを削除しました</h1><hr>
<p>削除データ一覧(合計$su件)</font>
$del_name
<form action="$scriptk" method="post">
<input type=hidden name=mode value=kanri_top>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}
__SUB__

	del_noplay => <<'__SUB__',
#------------------------#
#プレイ日数経過データ削除#
#------------------------#
sub del_noplay {

	if($in{'pass'} eq ""){&error("パスワードが入力されていません！！");}
	if($in{'pass'} != $kanripass){&error("パスワードが違います！！");}

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

		open(IN,"./charalog/$entry");
		push(@RANKING,<IN>);
		close(IN);
	}
	closedir(DIR);

	@tmp1 = @tmp2 = ();
	foreach (@RANKING) {
		my ($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$first,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
		if($rid){
		if($rid eq "test"){next;}
	 		push(@RANK_NEW, $_);
	 		push(@tmp1, $first);
			}
		}
		@RANK_NEW = @RANK_NEW[sort {$tmp1[$b] <=> $tmp1[$a] } 0 .. $#tmp1];

	$ima = time();

	$del_name="";$su=0;
	foreach (@RANK_NEW){
		my ($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$rdate,$rmori,$rdef,$rtac,$racsno,$rmoriturn) = split(/<>/);
		if($rdate){
			$rdate = $rdate + (60*60*24*$limit);
			$niti = $rdate - $ima;
			$niti = int($niti / (60*60*24));
			if($niti<0){
				&del_file($rid);
				$del_name.="<b>$rname</b>/";
				$su++;
				}
			}else{
				&del_file($rid);
				$del_name.="<b>$rname</b>/";
				$su++;
				}
		}
	&header;

	print <<"EOM";
<h1>下記のキャラデータを削除しました</h1><hr>
<p>削除データ一覧(合計$su件)</font>
$del_name
<form action="$scriptk" method="post">
<input type=hidden name=mode value=kanri_top>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}
__SUB__

	del_chara => <<'__SUB__',
#-----------------#
#キャラログ削除   #
#-----------------#
sub del_chara {

	if($in{'id'} eq ""){&error("ＩＤが指定されていません！！");}
	if($in{'pass'} eq ""){&error("パスワードが入力されていません！！");}
	if($in{'pass'} != $kanripass){&error("パスワードが違います！！");}

	&del_file($in{'id'});

	&header;

	print <<"EOM";
<h1>$in{'name'}のログデータを削除しました</h1><hr>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=kanri_top>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
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
	print "<HR SIZE=0 WIDTH=\"100%\"><DIV align=right>\n";
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
#	print "Cache-Control: no-cache\n";
#	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
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
	print "<body>\n";
	print "<embed src=\"$title_midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
}
__SUB__

	del_file => <<'__SUB__',
#--------------------------#
#指定したＩＤのファイル削除#
#--------------------------#
sub del_file {
	local($id) = @_;
	$m_charafile="./charalog/$id.cgi";
	$m_savefile="./savelog/$id.cgi";
	$m_bankfile="./banklog/$id.cgi";
	$m_charafile2="./charalog2/$id.cgi";
	#ログ削除処理
	if(-e $m_charafile){unlink($m_charafile);}
	if(-e $m_savefile){unlink($m_savefile);}
	if(-e $m_bankfile){unlink($m_bankfile);}
	if(-e $m_charafile2){unlink($m_charafile2);}

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	open(IN,"$chocolog_file");
	@item_chara = <IN>;
	close(IN);

	$hit=0;@item_new=();
	foreach(@item_chara){
		($cy_id,$cy_pass,$cy_kname,$cy_no,$cy_name,$cy_gold,$cy_rank,$cy_sp,$cy_sta,$cy_maxsta,$cy_ex,$cy_total,$cy_kati,$cy_0,$cy_1,$cy_2,$cy_3,$cy_4,$cy_5,$cy_6,$cy_life,$cy_kon,$cy_waza,$cy_money) = split(/<>/);
		if($id eq "$cy_id") {

			unshift(@item_new,"");
		}else{
			push(@item_new,"$_");
		}
	}

	open(OUT,">$chocolog_file");
	print OUT @item_new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

}
__SUB__
);
}
