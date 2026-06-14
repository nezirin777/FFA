#!/usr/bin/perl --

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
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
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# レジストライブラリの読み込み
require 'sankasya.pl';

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
if($mente) {
	&error("バージョンアップ中です。２、３０秒ほどお待ち下さい。m(_ _)m");
}
&decode;

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

&log_in;

#----------------#
#  ログイン画面  #
#----------------#
sub log_in {

	if (!( -e "./charalog/$in{'id'}.cgi")) {
		&error('IDが正しくありません！');
	}

	&chara_load;

if(!@chara) { &error("キャラデータが消えている可能\性があります。復元しますか？ただし、一日前のバックアップデータに戻ることになります<form action=\"hukugen.cgi\" method=\"post\"><input type=hidden name=id value=$in{'id'}><input type=hidden name=mode value=log_in><input type=submit style=\"background-color:#9370DB;color:#FFFFFF;border:2 solid BFEFFF\" value=\"復元する\"></form>");}

	&get_host;

	&get_time(time);

	$lock_file = "$lockfolder/login$in{'id'}.lock";
	&lock($lock_file,'LG');

	open(IN,"./loginlog/$in{'id'}.cgi");
	@logindata = <IN>;
	close(IN);

	$logins=@logindata;
	if($logins >= 15){pop(@logindata);}

	if ($in{'pass'} ne $chara[1]) {
			unshift(@logindata,"$in{'pass'}<>$host<>$gettime<>1<>\n");
			open(OUT,">./loginlog/$in{'id'}.cgi");
			print OUT @logindata;
			close(OUT);
			$lock_file = "$lockfolder/login$in{'id'}.lock";
			&unlock($lock_file,'LG');
			&error("パスワードが違います！"); 
	}

	unshift(@logindata,"$in{'pass'}<>$host<>$gettime<>0<>\n");
	open(OUT,">./loginlog/$in{'id'}.cgi");
	print OUT @logindata;
	close(OUT);

	$lock_file = "$lockfolder/login$in{'id'}.lock";
	&unlock($lock_file,'LG');

	$logmiss ="";$logsuc ="";
	foreach(@logindata){
		($logpass,$loghost,$logtime,$lognum)=split(/<>/);
		if($lognum){
			$logmiss .= << "EOM";
<tr>
<td align=center width=40%>$logtime</td>
<td align=center width=30%>$loghost</td>
<td align=center width=30%>$logpass</td>
</tr>
EOM
		} else {
			$logsuc .= << "EOM";
<tr>
<td align=center width=50%>$logtime</td>
<td align=center width=50%>$loghost</td>
</tr>
EOM
		}
	}

	&set_cookie;

	&guest_list;

	&header;

	&guest_view;

       print <<"EOM";
<hr size=0>
<center>
<h1><font color=white><font color=red>$chara[4]</font>でログインしました</font></h1>
<table border=0 width=90%><tr><td width=50%>
<table border=1 width=90%>
<tr><td colspan=2 id="td2" align=center class=b2>最近のログイン状況</td></tr>
<tr><td class="b2" align=center>時間</td><td class="b2" align=center>ホスト</td></tr>
$logsuc
</table></td><td width=50%>
<table border=1 width=90%>
<td colspan=3 id="td2" align=center class=b2>最近のパスワードエラーログインの状況</td></tr>
<tr><td class="b2" align=center>時間</td><td class="b2" align=center>ホスト</td><td class="b2" align=center>入力パスワード</td></tr>
$logmiss
</table></td></tr></table></center>
<br>
<hr size=0>
EOM
	&message_load;

	print"<hr size=0>";

	print <<"EOM";
<center>
<table border=0><tr><td><table border=1>
<tr><td id="td2" align=center class=b2>
<font class="$white">ステータス画面へ</font>
</td></tr>
<tr>
<form action="$script" method="POST">
<td align="center">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="submit" class="btn" value="ステータス画面へ">
</td></form></tr></table>
</td></tr></table></center>
EOM

	&footer;

	exit;
}
#------------------#
#  クッキーの発行  #
#------------------#
sub set_cookie {
	# クッキーは60日間有効
	local($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time+60*24*60*60);

	@month=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);

	$cook="id<>$chara[0]\,pass<>$chara[1]";
	print "Set-Cookie: $ffcookie=$cook; expires=$gmt\n";
}

