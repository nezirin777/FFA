#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　edit by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#

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

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# このファイル用設定
$backgif = $sts_back;
$midi = $sts_midi;

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
if ($mente) {
	&error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m");
}

&decode;

	$back_form = << "EOM";
<br>
<form action="$script_pass" method="post">
<input type=hidden name=id value="$in{'id'}">
<input type="hidden" name="mydata" value="$in{'mydata'}">
<input type=submit class=btn value="戻る">
</form>
EOM

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

if ($mode) { &$mode; }
&namechange;

exit;

#-----------------#
#　　パス変更　   #
#-----------------#
sub namechange {

	&chara_load;

	&chara_check;

	if ($chara[0] eq 'test') {&error('テストキャラは変更できません');}

	$phit = 0;
	open(IN,"./$pass_folder/$chara[0].cgi") || ($phit = 1);
	@item_new = <IN>;
	close(IN);

	($ppass,$ptan,$ptime,$phost)=split(/<>/,$item_new[0]);

	&get_time($ptime);

	&header;

	print <<"EOM";
<h1>パスワード変更所</h1>
<hr size=0>
<FONT SIZE=3>
EOM
	if (!$phit) {
	print <<"EOM";
<B>パスワード変更人</B><BR>
「君のパスワードを変更してあげよう。<br>パスワードを変更するには変更用単語が必要だぞ！<br>きちんと覚えているか？間違いすぎるとえらい目に会うから気をつけるんだな。」
</FONT><BR><BR>
<font size=4>あなたのパスワード変更は、前回$gettimeに$phostによって設定されました。(もしくは、パスワード変更用設定をその時にされました。)</font><br>
<form action="$script_pass" method="post">
<table><tr><td>
<input type=hidden name=mode value=passchan>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=password name=pass size=10></td><td>パスワード確認入力</td></tr>
<tr><td><input type=text name=passchange size=20></td><td>パスワード変更用単語</td></tr>
<tr><td><input type=password name=npass size=10></td><td>新しいパスワード（必ずメモを取って忘れないようにして下さい。半角で４～８文字）</td></tr>
<tr><td><input type=password name=nkpass size=10></td><td>新しいパスワードの確認入力</td></tr>
</table>
<input type=submit class=btn value="パスワード変更">
</form>
EOM
	} else {
		print <<"EOM";
<B>パスワード変更人</B><BR>
「君のパスワードを変更するための単語を設定してあげよう。<br>一度設定してしまうと二度と変更ができないので注意が必要だ！<br>（新規登録時に登録していた人はきちんと登録されていませんでした。申\し訳ないですが、もう一度設定お願いします。）」
</FONT><BR><BR>
<form action="$script_pass" method="post">
<table><tr><td>
<input type=hidden name=mode value=$pass_folder>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=password name=pass size=10></td><td>パスワード確認入力</td></tr>
<tr><td><input type=text name=$pass_folder size=20></td><td>パスワード変更用単語（必ずメモを取って忘れないようにして下さい。全角で4文字～10文字）</td></tr>
</table>
<input type=submit class=btn value="パスワード変更用単語設定">
</form>
EOM
	}

	print <<"EOM";
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#-----------------#
#　　変更用設定   #
#-----------------#
sub passchange {

	&chara_load;

	&chara_check;

	if ($in{'pass'} ne $chara[1]) {
		&error("パスワードが違います！！$back_form");
	}

	if ( -e "./$pass_folder/$chara[0].cgi") {
		&error("すでに設定されています！$back_form");
	}

	&get_host;

	$ntime = time();


	@passchan="$chara[1]<>$in{'passchange'}<>$ntime<>$host<>\n";

	open(OUT,">./$pass_folder/$in{'id'}.cgi");
	print OUT @passchan;
	close(OUT);

	&header;

	print <<"EOM";
<h1>パスワード変更用単語の設定をしました。</h1><hr>
<br>パスワード変更用単語の「<font color=white size=5>$in{'passchange'}</font>」は必ず忘れないようにして下さい。
$back_form
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
	&footer;

	exit;
}

#-----------------#
#　　変更用設定   #
#-----------------#
sub passchan {

	$lock_file = "$lockfolder/$in{'id'}.lock";
	&lock($lock_file,'CR');
	&chara_load;

	&chara_check;

	if ($in{'pass'} ne $chara[1]) {
		&error("パスワードが違います！$back_form"); 
	}
	if($in{'passchange'} eq "") {
		&error("パスワード変更用単語が入力されていません！$back_form"); 
	}
	elsif($in{'npass'} eq "") {
		&error("新しいパスワードが入力されていません！$back_form"); 
	}
	elsif($in{'npass'} ne "$in{'nkpass'}") {
		&error("パスワード確認入力が間違っています！$back_form");
	}
	elsif(length($in{'npass'})<4 || length($in{'npass'})>8) {
		&error("パスワードは４～８文字で設定してください！$back_form");
	}

	$lock_file = "$lockfolder/passc$in{'id'}.lock";
	&lock($lock_file,'PSC');
	open(IN,"./$pass_folder/$chara[0].cgi");
	@item_new = <IN>;
	close(IN);

	$hit=0;
	($ppass,$ptan,$ptime,$phost)=split(/<>/,$item_new[0]);

	if ($ptan ne $in{'passchange'}) {
		&error("パスワード・パスワード設定用単語が違います！！"); 
	}

	&get_host;

	$ntime = time();

	unshift(@item_new,"$in{'npass'}<>$ptan<>$ntime<>$host<>\n");

	open(OUT,">./$pass_folder/$chara[0].cgi");
	print OUT @item_new;
	close(OUT);
	&unlock($lock_file,'PSC');

	$chara[1] = $in{'npass'};

	&chara_regist;
	$lock_file = "$lockfolder/$in{'id'}.lock";
	&unlock($lock_file,'CR');

	&header;

	print <<"EOM";
<h1>パスワードを変更しました。</h1><hr>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}
