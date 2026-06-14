#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権は下記の2人にあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改) 管理モードスクリプト
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
# FF BATTLE de i
#　programed by jun-k
#　http://www5b.biglobe.ne.jp/~jun-kei/
#　jun-kei@vanilla.freemail.ne.jp
#------------------------------------------------------#

#------------------------------------------------------#
# 本スクリプトの作成者はいくですが、スクリプトの著作権はCUMROさん
# にあります、必要な著作権表示を消去して使用することはできません
# 本スクリプトに関してのお問い合わせはいくまでお願いします。
# CUMROには絶対にしないで下さい。
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';
$java_script_temp = $java_script;
$java_script = "";

# 管理人モードのパスワード
$kanripass = '1111';

# キャラ個別保存用フォルダ名(削除用)
$data_folder[0] = "./charalog";
$data_folder[1] = $message_file;
$data_folder[2] = $ban_file;
$data_folder[3] = "$souko_folder/acs";
$data_folder[4] = "$souko_folder/item";
$data_folder[5] = "$souko_folder/def";
$data_folder[6] = "./item";
$data_folder[7] = "./loginlog";
$data_folder[8] = $pass_folder;
$data_folder[9] = "./syoku";
$data_folder[10] = $sousin_file;

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#
&decode;
#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
}

&get_time(time());

&get_host;

$lock_file = "$lockfolder/ad.lock";
&lock($lock_file,'AD');
open(IN,"./kanrilog.cgi");
@logindata = <IN>;
close(IN);

$logins=@logindata;

if($logins >= 20){pop(@logindata);}

unshift(@logindata,"$in{'pass'}<>$host<>$gettime<>\n");

open(OUT,">./kanrilog.cgi");
print OUT @logindata;
close(OUT);
&unlock($lock_file,'AD');

if ($in{'pass'} ne $kanripass) { &error('パスワードを入力して下さい'); }

$back_form = << "EOM";
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

if ($mode) { &$mode; }
&kanri_top;
exit;

#-----------------#
#  管理人モード   #
#-----------------#
sub kanri_top {


	$ima = time();
	$sousu = @RANK_NEW;

	&header;

	print <<"EOM";
<h1>管理モード</h1><hr size=0>
※現在登録されているキャラクターをプレイ頻度が高い順に表\示しています。<br>
※一旦<b>削除</b>すると、二度と復元できなくなるので必ず<b>バックアップ</b>をとってから実行してください。<br><br>
ここ最近の管理モード使用の履歴(何か行動を起こす度にログを取得しています)
<table bgcolor="#000000" cellspacing="1">
<tr><th>ログイン時間</th><th>ホスト</th><th>入力パスワード</th></tr>
EOM
	foreach (@logindata) {
		($pass,$host,$time) = split(/<>/);
		if ($pass eq $kanripass) { print "<tr bgcolor=\"#eeeeee\">"; }
		else { print "<tr bgcolor=\"#ffaaaa\">"; }
		print "<td align=center>$time</td><td align=center>$host</td><td align=center>$pass</td></tr>";
		
	}
	print <<"EOM";
</table>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=del_noplay>
<input type=submit class=btn value="プレイ日数を過ぎたキャラクターデータの完全削除"><br>
(前回戦闘から戦闘せずに$limit日経過してしまったキャラを自動的に削除します)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=kanri_all>
<input type=submit class=btn value="キャラクター一覧"><br>
(ＦＦＡ内のキャラクターを一覧で表\示します)
</form>
<form action="$scriptk" method="post">
<input type="text" name=id size=20>
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=data>
<input type=submit class=btn value="ＩＤ指定キャラクターデータ"><br>
(ＦＦＡ内のキャラクターからＩＤで検索して、詳細なデータを表\示します)
</form>
<form action="$scriptk" method="post">
<input type="text" name=name size=20>
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=data>
<input type=submit class=btn value="名前指定キャラクターデータ"><br>
(ＦＦＡ内のキャラクターから名前で検索して、詳細なデータを表\示します)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=save>
<input type=submit class=btn value="キャラ保存"><br>
(削除日数経過しても削除されないキャラクターを指定します)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=img>
<input type=submit class=btn value="画像の追加"><br>
(./images/charaフォルダ内の画像を自動的に読み取り、ffadventure.iniに追加する用に一覧で出力します。<br>HTMLとCGIが分離されているサーバーでも使用できますので、画像を追加する際などに一時的に画像を入れ、一覧を出力すると便利です。)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku">
<input type=submit class=btn value="職業の編集"><br>
(職業別の細かい設定を変更できます。)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテム一覧"><br>
(アイテムの一覧が見れます。)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技一覧"><br>
(必殺技の一覧が見れます。)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku_add_pre">
<input type=submit class=btn value="職業の追加"><br>
(職業追加の準備ができます。)
</form>
<br>
<br>
<br>
<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=del_all><br>
<input type=submit class=btn value="全ログデータの削除"><br>
(ＦＦＡ内の全キャラクターデータを抹消します)
</form>
EOM
	&footer;

	exit;

}

#-----------------#
#  管理人モード   #
#-----------------#
sub kanri_all {


	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

		if($entry=~/\.cgi/){
			open(IN,"./charalog/$entry");
			$WORK=<IN>;
			push(@RANK_NEW,"$WORK\n");
			close(IN);
		}
	}
	closedir(DIR);
	
	@tmp = ();
	if($in{'list'} eq 'other_list') {
		# 配列28番目でソート
		@tmp = map {(split /<>/)[21]} @RANK_NEW;
	}elsif($in{'list'} eq 'ip_list') {
		# 配列28番目でソート
		@tmp = map {(split /<>/)[26]} @RANK_NEW;
	}else{
		# 配列28番目でソート
		@tmp = map {(split /<>/)[27]} @RANK_NEW;
	}

	@RANK_NEW = @RANK_NEW[sort {$tmp[$b] <=> $tmp[$a] } 0 .. $#tmp];

	$ima = time();
	$sousu = @RANK_NEW;

	&header;

	print <<"EOM";
<h1>管理モード</h1><hr size=0>
※現在登録されているキャラクターを表\示しています。<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=kanri_all>
<input type=submit class=btn value="日付順に並び替え">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=kanri_all>
<input type="hidden" name=list value=other_list>
<input type=submit class=btn value="戦闘回数順に並び替え">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=kanri_all>
<input type="hidden" name=list value=ip_list>
<input type=submit class=btn value="ＩＰアドレス順に並び替え">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=kanri_top>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
<hr size=0><p><table border=1>
<tr><th>NO</th><th>ログイン</th><th>キャラ名</th><th>ＩＤ</th><th>パスワード</th><th>サイト名</th><th>ＩＰアドレス</th><th>削除まで</th><th>戦闘回数</th><th>削除</th><th>保存</th><th>詳細</th></tr>
EOM
	$i=1;
	foreach (@RANK_NEW){
		s/\n//;
		s/\r//;
		($rid,$rpass,$rsite,$rurl,$rname,$rsex,$rchara,$rn_0,$rn_1,$rn_2,$rn_3,$rn_4,$rn_5,$rn_6,$rsyoku,$rhp,$rmaxhp,$rex,$rlv,$rgold,$rlp,$rtotal,$rkati,$rwaza,$ritem,$rmons,$rhost,$rdate) = split(/<>/);
		$rdate = $rdate + (60*60*24*$limit);
		$niti = $rdate - $ima;
		$niti = int($niti / (60*60*24));
		if($niti==-11337){$niti_s="<font class=red>日付無し</font>";}else{$niti_s="<font class=yellow>$niti</font>日";}

	print <<"EOM";
<tr>
<td align=left>$i</td>
<td align=center valign=center>
<form action="$script" method="post">
<input type=hidden name=mode value=log_in>
<input type=hidden name="id" value="$rid">
<input type=hidden name="mydata" value="$_">
<input type=submit class=btn value="ログイン">
</td>
<td align=left></form><a href="$scripta?mode=chara_sts&id=$rid">$rname</a></td><td align=left>$rid</td><td align=left>$rpass</td><td align=left><a href=\"$rurl\" target="_blank">$rsite</a></td>
EOM
	if($rhost==$wrhost){$wrhost=$rhost;$rhost="<font class=red>$rhost</font>";}
	print "<td align=left>$rhost</td>";
	print "<td align=left>$niti_s</td>";
	print "<td align=left>$rtotal</td>";

	print <<"EOM";
<form action="$scriptk" method="post">
<td align=center valign=center>
<input type="hidden" name=mode value=del_chara>
<input type=hidden name=id value=$rid>
<input type=hidden name=name value=$rname>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="削除">
</td></form>
<form action="$scriptk" method="post">
<td align=center valign=center>
<input type="hidden" name=mode value=save_chara>
<input type=hidden name=id value=$rid>
<input type=hidden name=name value=$rname>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="保存">
</td></form>
<form action="$scriptk" method="post">
<td align=center valign=center>
<input type=hidden name=id value=$rid>
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=data>
<input type=submit class=btn value="詳細">
</td></form>
EOM
		print "</tr>\n";
		$i++;
	}

	print "</table><p>\n";

	&footer;

	exit;
}

#-----------------#
#  全ログ削除     #
#-----------------#
sub del_all {

	if(!$in{'kakunin'}) {
		$back_form = << "EOM";
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name="kakunin" value="1">
<input type="hidden" name=mode value=del_all>
<input type=submit class=btn value="全ログデータの削除">
</form>
<br>
<br>
<br>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=kanri_top>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM
		&error("本当に消しますか？$back_form");
	}


	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

		open(IN,"./charalog/$entry");
		if ($entry =~ /\.cgi/) {
			push(@RANKING,<IN>);
			close(IN);
		}
	}
	closedir(DIR);

	$del_name="";$su=0;
	foreach (@RANKING){
		my @rchara = split(/<>/);
		if($rchara[0] eq "test"){next;}
		$del_name .= "<b>$rchara[4]</b>/";
		$su++;
		&del_file($rchara[0]);
	}

	&all_data_delete;

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

#------------------------#
#プレイ日数経過データ削除#
#------------------------#
sub del_noplay {

	opendir(DIR,'./charalog') or die "$!";
	foreach $entry (readdir(DIR)){

		if ($entry =~ /\.cgi/) {
			open(IN,"./charalog/$entry");
			push(@RANKING,<IN>);
			close(IN);
		}

	}
	closedir(DIR);

	open(IN,"./save_log.cgi");
	@save_chara = <IN>;
	close(IN);

	$ima = time();

	$del_name="";$su=0;
	foreach (@RANKING){
		$save = 0;
		my @rchara = split(/<>/);
		foreach (@save_chara) {
			s/\n//g;
			s/\r//g;
			@save = split(/<>/);
			if ($save[0] eq $rchara[0]) { $save = 1;last; }
		}
		if ($save) { next; }
		if($rchara[27]){
			$rchara[27] = $rchara[27] + (60*60*24*$limit);
			$niti = $rchara[27] - $ima;
			$niti = int($niti / (60*60*24));
			if ($niti < 0) {
				&del_file($rchara[0]);
				$del_name.="<b>$rchara[4]</b>/";
				$su++;
			}
		} else {
			&del_file($rchara[0]);
			$del_name.="<b>$rchara[4]</b>/";
			$su++;
		}
	}

	&all_data_delete;

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

#-----------------#
#キャラログ削除   #
#-----------------#
sub del_chara {

	if(!$in{'kakunin'}) {
		$back_form = << "EOM";
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name="kakunin" value="1">
<input type="hidden" name="id" value="$in{'id'}">
<input type="hidden" name="name" value="$in{'name'}">
<input type="hidden" name=mode value=del_chara>
<input type=submit class=btn value="削除">
</form>
<br>
<br>
<br>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=kanri_top>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM
		&error("$in{'name'}さんを本当に消しますか？$back_form");
	}

	if($in{'id'} eq ""){&error("ＩＤが指定されていません！！");}

	&del_file($in{'id'});

	&all_data_delete;

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

#--------------------------#
#指定したＩＤのファイル削除#
#--------------------------#
sub del_file {

	local($id) = @_;
	foreach (@data_folder) {
		$m_charafile="$_/$id.cgi";
		#ログ削除処理
		if(-e $m_charafile){unlink($m_charafile);}
	}

	push(@no_data,"$id");
}

#------------------#
#全体ファイルの更新#
#------------------#
sub all_data_delete{

		opendir (DIR,'./charalog') or die "$!";
		foreach $entry (readdir(DIR)){

			if ($entry =~ /\.cgi/) {
				open(IN,"./charalog/$entry");
				$WORK=<IN>;
				$WORK =~ s/\n//gi;
				$WORK =~ s/\r//gi;
				push(@temp_member,"$WORK\n");
				close(IN);		
			}
		}
		closedir(DIR);

		# 配列19番目でソート
		@tmp = map {(split /<>/)[18]} @temp_member;
		@RANKING = @temp_member[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

		open(OUT,">$all_data_file");
		print OUT @RANKING;
		close(OUT);

}

#-----------------#
#  管理人モード   #
#-----------------#
sub data {

	if ($in{'name'}) {
		&all_data_read;

		$hit = 0;
		foreach(@RANKING){
			@chara_data = split(/<>/);
			if ($in{'name'} eq $chara_data[4]) { $hit=1;last; }
		}

		$back_form = << "EOM";
<form action=$scriptk method=post>
もう一度検索する
<input type=hidden name=mode value=data>
<input type=hidden name=pass value=$in{'pass'}>
<input type=text name=name size=20>
<input type=submit class=btn value=検索>
</form>
<form action=$scriptk method=post>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value=戻る>
</form>
EOM

		if(!$hit){&error("キャラクターが見つかりません。$back_form");}
		$in{'id'} = $chara_data[0];
	}

	open(IN,"./charalog/$in{'id'}.cgi");
	$chara_log = <IN>;
	close(IN);

	@chara = split(/<>/,$chara_log);

	$ima = time();

	&header;

	print <<"EOM";
<h1>管理モード</h1><hr size=0>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
<hr size=0><table border=1>
<tr><th>ログイン</th><th>キャラ名</th><th>ＩＤ</th><th>パスワード</th><th>変更用単語</th><th>パスワード変更ホスト</th><th>サイト名</th><th>ＩＰアドレス</th><th>削除まで</th><th>戦闘回数</th><th>削除</th><th>保存</th></tr>
EOM
		$rdate = $chara[27] + (60*60*24*$limit);
		$niti = $rdate - $ima;
		$niti = int($niti / (60*60*24));
		$niti_s="$niti日";
		# パスワードデータ取得
		open(IN,"$pass_folder/$chara[0].cgi");
		@pass_data = <IN>;
		close(IN);
		(undef,$i_pass,undef,$phost) = split(/<>/,$pass_data[0]);

		$rhost = "<font class=red>$chara[26]</font>";
	print <<"EOM";
<tr>
<form action="$script" method="post">
<td align=center valign=center>
<input type=hidden name=mode value=log_in>
<input type=hidden name=id value=$chara[0]>
<input type=hidden name="mydata" value="$chara_log">
<input type=submit class=btn value="ログイン">
</td></form>
<td align=left>
<a href="$scripta?mode=chara_sts&id=$chara[0]">
$chara[4]</a></td>
<td align=left>$chara[0]</td>
<td align=left>
$chara[1]</td>
<td>$i_pass</td>
<td>$phost</td>
<td align=left><a href="$chara[3]" TARGET="_blank">$chara[2]</a></td>
<td align=left>$rhost</td>
<td align=left>$niti_s</td>
<td align=left>$chara[21]</td>
<form action="$scriptk" method="post">
<td align=center valign=center>
<input type="hidden" name=mode value=del_chara>
<input type=hidden name=id value="$chara[0]">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="削除">
</td></form>
<form action="$scriptk" method="post">
<td align=center valign=center>
<input type="hidden" name=mode value=save_chara>
<input type=hidden name=id value="$chara[0]">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="保存">
</td></form>
</tr></table><br>
EOM

	&message_load;

	require 'sousin.pl';

	&footer;

	exit;

}

#------------#
# キャラ保存 #
#------------#
sub save {

	open(IN,"./save_log.cgi");
	@save = <IN>;
	close(IN);

	&header;
	print <<"EOM";
<font size=3>
ここではプレイ日数経過キャラクターデータの完全削除で削除されないキャラクターを指定できます。<br>
なお、ここで指定キャラでも個別削除は有効ですので、ご注意下さい。</font>
<form action="$scriptk" method="post">
<input type="text" name="id" size=20>
<input type="hidden" name="pass" value=$in{'pass'}>
<input type="hidden" name=mode value=save_chara>
<input type=submit class=btn value="ＩＤ指定保存">
</form>
<form action="$scriptk" method="post">
<TABLE BORDER=0>
<TR>
<TD ALIGN="center" CLASS="b2" id="td1"></TD>
<TD ALIGN="center" CLASS="b2" id="td1">ＩＤ</TD>
<TD ALIGN="center" CLASS="b2" id="td1">キャラ名</TD>
</tr>
EOM
	foreach(@save){
		($tid,$tname) = split(/<>/);

		print "<TR><td class=b2 align = center id=td1>\n";
		print "<input type=radio name=id value=$tid></td>\n";
		print "<TD class=b1 align = center>\n";
		print "$tid\n";
		print "</TD>\n";
		print "<TD  class=b1 align = center>\n";
		print "$tname\n";
		print "</TD></tr>\n";
	}
	print <<"EOM";
</table>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=save_del>
<input type=submit class=btn value="リストから削除">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}

#------------#
# キャラ保存 #
#------------#
sub save_chara {

	&chara_load;

	open(IN,"./save_log.cgi");
	@rank = <IN>;
	close(IN);

	foreach(@rank){
		($sid)=split(/<>/);
		if ($sid eq $chara[0]) {
			$back_form = << "EOM";
<form action="$scriptk" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" class="btn" value="戻る">
</form>
EOM
			&error("登録済みです$back_form");
		}
	}

	push(@rank,"$chara[0]<>$chara[4]<>\n");

	open(OUT,">./save_log.cgi");
	print OUT @rank;
	close(OUT);

	&header;

	print <<"EOM";
$chara[4]さんを保存キャラリストに追加しました<br>
<form action="$scriptk" method="post">
<input type="text" name=id size=20>
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=save_chara>
<input type=submit class=btn value="ＩＤ指定保存">
</form>
<form action="$scriptk" method="post">
<TABLE BORDER=0>
<TR><TD ALIGN="center" CLASS="b2" id="td1"></TD>
<TD ALIGN="center" CLASS="b2" id="td1">ＩＤ</TD>
<TD ALIGN="center" CLASS="b2" id="td1">キャラ名</TD>
</tr>
EOM

	foreach(@rank){
		($tid,$tname) = split(/<>/);

		print "<TR><td class=b2 align = center id=td1>\n";
		print "<input type=radio name=id value=$tid></td>\n";
		print "<TD class=b1 align = center>\n";
		print "$tid\n";
		print "</TD>\n";
		print "<TD  class=b1 align = center>\n";
		print "$tname\n";
		print "</TD></tr>\n";
	}
print "</table>";
	print <<"EOM";
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=save_del>
<input type=submit class=btn value="リストから削除">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 保存解除 #
#----------#
sub save_del {

	open(IN,"./save_log.cgi");
	@rank = <IN>;
	close(IN);

	@ranknew=();
	foreach(@rank){
		($sid)=split(/<>/);
		if($sid ne $in{'id'}){push(@ranknew,"$_");}
	}

	open(OUT,">./save_log.cgi");
	print OUT @ranknew;
	close(OUT);

	&header;

	print <<"EOM";
解除しました<br>
<form action="$scriptk" method="post">
<input type="text" name=id size=20>
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value=save_chara>
<input type=submit class=btn value="ＩＤ指定保存">
</form>
<form action="$scriptk" method="post">
<TABLE BORDER=0>
<TR><TD ALIGN="center" CLASS="b2" id="td1"></TD>
<TD ALIGN="center" CLASS="b2" id="td1">ＩＤ</TD>
<TD ALIGN="center" CLASS="b2" id="td1">キャラ名</TD>
</tr>
EOM
	foreach(@ranknew){
		($tid,$tname) = split(/<>/);

		print "<TR><td class=b2 align = center id=td1>\n";
		print "<input type=radio name=id value=$tid></td>\n";
		print "<TD class=b1 align = center>\n";
		print "$tid\n";
		print "</TD>\n";
		print "<TD  class=b1 align = center>\n";
		print "$tname\n";
		print "</TD></tr>\n";
	}

	print <<"EOM";
</table>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=mode value=save_del>
<input type=submit class=btn value="リストから削除">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 画像一覧 #
#----------#
sub img {

	$i = 0;
	$s = 0;
	$img_all = "";
	$img_tag[$s] = "<tr>\n";
	$html_link1 = "\[<a href = \"./img_all$s.html\">$s</a>\]";
	opendir(DIR,'./images/chara') or die "$!";
	foreach $entry (readdir(DIR)){


		if ($entry=~/\.(gif|jpg|png|bmp)/) {
			$img_all .= "\$chara_img\[$i\] = \"$entry\"\;<br>\n";
			$img_tag[$s] .= "<td align=\"center\" valign=\"bottom\"><img src=\"$img_path/$entry\"><br>$i</td>\n";
			$i++;
			if ($i % 5 == 0) {
				$img_tag[$s] .= "</tr>\n<tr>\n";
				if ($i % 30 == 0) {
					$s++;
					$img_tag[$s] .= "<tr>";
					$html_link1 .= "\[<a href = \"./img_all$s.html\">$s</a>\]";
				}
			}
		}
	}
	closedir(DIR);

	$s = 0;
	$html_link = "";
	foreach (@img_tag) {
		$html_tag = <<"EOM";
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Pragma" content="no-cache">
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<SCRIPT Language="JavaScript" src="$java_script_temp" type="text/javascript">
</SCRIPT>
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
<link rel="stylesheet" href="$style_sheet" type="text/css">
<title>画像一覧</title></head>
<body background="$backgif" bgcolor="$bgcolor" text="$text" link="$link" vlink="$vlink" alink="$alink">
<center>
<table border="1">
$img_tag[$s]
</tr>
</table>
画像一覧別ページ<br>
$html_link1
</center>
<HR SIZE=0 WIDTH="100%"><DIV align=right>
FFA いく改ver2.00 edit by <a href="http://www.eriicu.com" target="_top">いく</a><br>
FFA Emilia Ver1.01 remodeled by Classic(閉鎖)<br>
FF Battle De I v3.06 remodeling by <a href="http://www.mj-world.jp/" target="_blank">jun-k</a>(更新停止中)<br>
FF ADVENTURE(改) v1.040 remodeled by <a href="http://www.gun-online.com" target="_blank">ＧＵＮ</a><br>
FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) <a href="http://www5c.biglobe.ne.jp/~ma-ti/" target="_blank">現配布元(管理者ma-ti)</a><br>
</DIV></body></html>
EOM

		open(OUT,">./img_all$s.html");
		print OUT $html_tag;
		close(OUT);
		$html_link .= "<a href = \"./img_all$s.html\" target=\"_blank\">img_all$s.html</a><br>";
		$s++;
	}

	&header;

	print << "EOM";
以下のテーブル内をffadventure.iniにある指定箇所にコピーペーストして下さい。<br>
また、ffaicuフォルダ内に<br>
$html_link
というファイル作成されました。<br>
キャラ画像一覧が出力されているので、ぜひご利用下さい。
<table border="1">
<tr><td>
$img_all
</td></tr>
</table>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 職業一覧 #
#----------#
sub syoku {

	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$syoku_sum = @chara_syoku + 1;

	&header;

	print <<"EOM";
職業一覧<br>
<TABLE BORDER=0>
<TR>
EOM
	$s = 0;
	foreach (@chara_syoku) {
		print <<"EOM";
<form action="$scriptk" method="post">
<TD class=b1 align = center>
$chara_syoku[$s]<br>
<input type="hidden" name="syoku" value="$s">
<input type="hidden" name="mode" value="syoku_pre">
<input type=hidden name=pass value=$in{'pass'}>
<input type="submit" class="btn" value="変更" size="20">
</TD>
</form>
EOM
		$s++;
		if ($s % 10 == 0) { print "</tr>\n<tr>\n"; }
	}

	print <<"EOM";
</tr>
</table>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 職業能力 #
#----------#
sub syoku_pre {

	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	@skill = split(/<>/,$syoku[$in{'syoku'}],17);
	@syoku_require = split(/<>/,$skill[16]);
	pop(@skill);

	$syoku_sum = @chara_syoku + 1;

	&header;

	print <<"EOM";
<h1>$chara_syoku[$in{'syoku'}]能\力一覧</h1><br>
<form action="$scriptk" method="post">
<input type="hidden" name="syoku" value="$in{'syoku'}">
<input type="hidden" name="mode" value="syoku_change">
<input type=hidden name=pass value=$in{'pass'}>
<TABLE BORDER=0>
<TR>
<TD ALIGN="center" CLASS="b2" id="td1" colspan="8">転職必須能\力</TD>
<TD ALIGN="center" CLASS="b2" id="td1" colspan="8">能\力上昇値</TD>
</tr>
<tr>
<TH><font size=1>力</font></TH>
<TH><font size=1>魔力</font></TH>
<TH><font size=1>信仰心</font></TH>
<TH><font size=1>生命力</font></TH>
<TH><font size=1>器用さ</font></TH>
<TH><font size=1>速さ</font></TH>
<TH><font size=1>魅力</font></TH>
<TH><font size=1>カルマ</font></TH>
<TH><font size=1>力</font></TH>
<TH><font size=1>魔力</font></TH>
<TH><font size=1>信仰心</font></TH>
<TH><font size=1>生命力</font></TH>
<TH><font size=1>器用さ</font></TH>
<TH><font size=1>速さ</font></TH>
<TH><font size=1>魅力</font></TH>
<TH><font size=1>カルマ</font></TH>
</tr>
<tr>
EOM
	
	for ($i=0;$i<=15;$i++) {
		print <<"EOM";
<TD class=b1 align = center>
<input type="text" name="skill$i" value="$skill[$i]" size="4">
</TD>
EOM
	}
			print <<"EOM";
</tr>
</table><br>
<table>
<tr>
<TD ALIGN="center" CLASS="b2" id="td1" colspan="$syoku_sum">
転職必須習得職業レベル
</TD>
</tr>
<tr>
EOM
	$m = 0;
	foreach (@chara_syoku) {
		print "<TH><font size=1>$_</font></TH>";
		print <<"EOM";
<TD class=b1 align = center>
<input type="text" name="master$m" value="$syoku_require[$m]" size="2">
</TD>
EOM
		$m++;
		if ($m % 10 == 0) { print"</tr>\n<tr>\n"; }
	}
	print <<"EOM";
</tr>
</table>
<input type="submit" class="btn" value="$chara_syoku[$in{'syoku'}]の能\力変更" size="20">
</form>
<table><tr>
<td valign="top">
<form action="$scriptk" method="post">
武器屋販売アイテム
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>威力</th><th>価格</th><th>命中率補正</th></tr>
EOM
	open(IN,"$item_folder/item$in{'syoku'}.ini");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_sell>
<input type="hidden" name="syoku" value="$in{'syoku'}">
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=item>
<input type=submit class=btn value="削除">
</form>
</td><td valign="top">
<form action="$scriptk" method="post">
防具屋販売アイテム
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>威力</th><th>価格</th><th>回避率補正</th></tr>
EOM
	open(IN,"$def_folder/def$in{'syoku'}.ini");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_sell>
<input type="hidden" name="syoku" value="$in{'syoku'}">
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=def>
<input type=submit class=btn value="削除">
</form>
</td></tr></table>
<form action="$scriptk" method="post">
装飾品店販売アイテム
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>価格</th><th>効果</th><th>力</th><th>魔力</th><th>信仰心</th><th>生命力</th><th>器用さ</th><th>速さ</th><th>魅力</th><th>カルマ</th><th>命中率</th><th>回避率</th><th>必殺率</th><th>説明</th></tr>
EOM
	open(IN,"$acs_folder/acs$in{'syoku'}.ini");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_sell>
<input type="hidden" name="syoku" value="$in{'syoku'}">
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=acs>
<input type=submit class=btn value="削除">
</form>
<form action="$scriptk" method="post">
使用可能\必殺技<br>
使用条件とは、1でマスターじゃないと使用できないもの、0でマスターしてなくとも使える必殺技となります。
<table>
<tr>
<th></th><th>No.</th><th>技名</th><th>説明</th><th>使用条件</th></tr>
EOM
	open(IN,"$tac_folder/tac$in{'syoku'}.ini");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_sell>
<input type="hidden" name="syoku" value="$in{'syoku'}">
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=tac>
<input type=submit class=btn value="削除">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku">
<input type=submit class=btn value="職業の一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 職業編集 #
#----------#
sub syoku_change {

	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$newskill = "";
	for ($i=0;$i<=15;$i++) {
		$hash = "skill$i";
		$newskill .= "$in{$hash}<>";
	}

	$m = 0;
	foreach (@chara_syoku) {
		$hash = "master$m";
		$newskill .= "$in{$hash}<>";
		$m++;
	}

	$syoku[$in{'syoku'}] = "$newskill\n";

	open(OUT,">$syoku_file");
	print OUT @syoku;
	close(OUT);

	&header;

	print <<"EOM";
変更しました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku">
<input type=submit class=btn value="職業の一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 道具削除 #
#----------#
sub item_sell {

	$folder = "$in{'item'}\_folder";

	open(IN,"$$folder/$in{'item'}$in{'syoku'}.ini");
	@item_array = <IN>;
	close(IN);

	splice(@item_array,$in{'item_no'},1);

	open(OUT,">$$folder/$in{'item'}$in{'syoku'}.ini");
	print OUT @item_array;
	close(OUT);

	&header;

	print <<"EOM";
削除しました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku">
<input type=submit class=btn value="職業の一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 道具一覧 #
#----------#
sub item_all {

	&header;

	print <<"EOM";
<h1>どのアイテムを見ますか？</h1>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all_item">
<input type=submit class=btn value="武器">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all_def">
<input type=submit class=btn value="防具">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all_acs">
<input type=submit class=btn value="装飾品">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 道具一覧 #
#----------#
sub item_all_item {

	&header;

	print <<"EOM";
<h1>武器一覧</h1>
<form action="$scriptk" method="post">
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>威力</th><th>価格</th><th>命中率補正</th></tr>
EOM
	open(IN,"$item_file");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=item>
<input type=submit class=btn value="編集">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=new_item_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=item>
<input type=submit class=btn value="新しく武器を追加する">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 道具一覧 #
#----------#
sub item_all_def {

	&header;

	print <<"EOM";
<h1>防具一覧</h1>
<form action="$scriptk" method="post">
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>威力</th><th>価格</th><th>回避率補正</th></tr>
EOM
	open(IN,"$def_file");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=def>
<input type=submit class=btn value="編集">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=new_item_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=def>
<input type=submit class=btn value="新しく防具を追加する">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 道具一覧 #
#----------#
sub item_all_acs {

	&header;

	print <<"EOM";
<h1>装飾品一覧</h1>
<form action="$scriptk" method="post">
<table>
<tr>
<th></th><th>No.</th><th>なまえ</th><th>価格</th><th>効果</th><th>力</th><th>魔力</th><th>信仰心</th><th>生命力</th><th>器用さ</th><th>速さ</th><th>魅力</th><th>カルマ</th><th>命中率</th><th>回避率</th><th>必殺率</th><th>説明</th></tr>
EOM
	open(IN,"$acs_file");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=item_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=acs>
<input type=submit class=btn value="編集">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=new_item_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=hidden name=item value=acs>
<input type=submit class=btn value="新しく装飾品を追加する">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 道具編集 #
#----------#
sub item_edit {

	$file = "$in{'item'}\_file";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	$item_array[$in{'item_no'}] =~ s/\n//g;
	$item_array[$in{'item_no'}] =~ s/\r//g;

	if ($in{'item'} eq 'acs') {
		$list = '<th>No.</th><th>なまえ</th><th>価格</th><th>効果</th><th>力</th><th>魔力</th><th>信仰心</th><th>生命力</th></tr>';
		$list2 = '<tr><th>器用さ</th><th>速さ</th><th>魅力</th><th>カルマ</th><th>命中率</th><th>回避率</th><th>必殺率</th><th>説明</th></tr>';
	} else {
		$list = '<th>No.</th><th>なまえ</th><th>威力</th><th>価格</th><th>命中/回避率補正</th></tr>';
	}

	&header;

	@item_data = split(/<>/,$item_array[$in{'item_no'}]);

	print <<"EOM";
<h1>$item_data[1]の編集</h1>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_edit_end">
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=item value="$in{'item'}">
<input type="hidden" name="item_skill0" value="$item_data[0]">
<table>
$list
<tr>
<td class=b1 align="center">$item_data[0]</td>
EOM
	$i = 0;
	foreach (@item_data) {
		if ($i == 0) { $i++; next; }
		print "<td class=b1><input type=\"text\" name=\"item_skill$i\" value=\"$_\"></td>";
		$i++;
		if ($i == 8) { print "</tr>$list2<tr>"; }
	}

	$i--;

	print <<"EOM";
</tr></table>
<input type="hidden" name="item_num" value="$i">
<input type=submit class=btn value="能\力の編集">
</form>
特定の職業への追加
<TABLE BORDER=0>
<TR>
EOM
	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$s = 0;
	foreach (@chara_syoku) {
		print <<"EOM";
<form action="$scriptk" method="post">
<TD class=b1 align = center>
$chara_syoku[$s]<br>
<input type="hidden" name="syoku" value="$s">
<input type="hidden" name="mode" value="syoku_item_add">
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=item value="$in{'item'}">
<input type=hidden name=pass value=$in{'pass'}>
<input type="submit" class="btn" value="この職業に追加" size="20">
</TD>
</form>
EOM
		$s++;
		if ($s % 6 == 0) { print "</tr>\n<tr>\n"; }
	}

	print <<"EOM";
</tr>
</table>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="player_item">
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=item value="$in{'item'}">
<input type="text" name=id value="">
<input type=submit class=btn value="プレイヤーの倉庫に入れる(ID指定)">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_delete">
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=item value="$in{'item'}">
<input type=submit class=btn value="このアイテムを削除する"><br>
(プレイヤーの倉庫からはなくならないので、一度流通し始めてしまったアイテムを削除することはオススメできません。)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#------------------#
# 道具ファイル編集 #
#------------------#
sub item_edit_end {

	$file = "$in{'item'}\_file";
	$folder = "$in{'item'}\_folder";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	$newitem = "";
	for ($i=0;$i<=$in{'item_num'};$i++) {
		$hash = "item_skill$i";
		$newitem .= "$in{$hash}<>";
	}

	$item_array[$in{'item_no'}] = "$newitem\n";

	open(OUT,">$$file");
	print OUT @item_array;
	close(OUT);

	# 職業別の道具ファイルの同じ道具も一斉変換
	opendir (DIR,"$$folder") or die "$!";
	foreach $entry (readdir(DIR)){
		if ($entry =~ /\.ini/) {
			if ($file eq "$folder/$entry") { next; }
			open(IN,"$$folder/$entry");
			@item_data = <IN>;
			close(IN);

			open(OUT,">$$folder/$entry");
			foreach (@item_data) {
				($i_no) = split(/<>/);
				if ($in{'item_skill0'} ne $i_no) {
					print OUT $_;
				} else {
					print OUT "$newitem\n";
				}
			}
			close(OUT);
		}
	}
	closedir(DIR);

	&header;

	print <<"EOM";
変更しました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type=hidden name=item value=$in{'item'}>
<input type="hidden" name=mode value="item_edit">
<input type=submit class=btn value="道具詳細に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#--------------#
# 職業道具追加 #
#--------------#
sub syoku_item_add {

	$file = "$in{'item'}\_file";
	$folder = "$in{'item'}\_folder";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	$newitem = $item_array[$in{'item_no'}];

	open(IN,"$$folder/$in{'item'}$in{'syoku'}\.ini");
	@item_data = <IN>;
	close(IN);

	push(@item_data,$newitem);

	# 配列1番目でソート
	@tmp = map {(split /<>/)[0]} @item_data;
	@item_data = @item_data[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

	open(OUT,">$$folder/$in{'item'}$in{'syoku'}\.ini");
	print OUT @item_data;
	close(OUT);

	&header;

	print <<"EOM";
変更しました<br>
EOM
if ($in{'item'} eq 'tac') {
	print <<"EOM";
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=mode value="waza_edit">
<input type=submit class=btn value="必殺技詳細に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技の一覧に戻る">
</form>
EOM
} else {
	print <<"EOM";
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type=hidden name=item value=$in{'item'}>
<input type="hidden" name=mode value="item_edit">
<input type=submit class=btn value="道具詳細に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧に戻る">
</form>
EOM
}
	print <<"EOM";
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#----------------------#
# キャラ倉庫に道具追加 #
#----------------------#
sub player_item {

	$file = "$in{'item'}\_file";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	$newitem = $item_array[$in{'item_no'}];

	if ($in{'item'} eq 'item') {
		$lock_file = "$lockfolder/sitem$in{'id'}.lock";
		$flock_pre = 'SI';
	} elsif ($in{'item'} eq 'def') {
		$lock_file = "$lockfolder/sdefe$in{'id'}.lock";
		$flock_pre = 'SD';
	} else {
		$lock_file = "$lockfolder/acsesa$in{'id'}.lock";
		$flock_pre = 'SA';
	}

	&lock($lock_file,$flock_pre);
	open(IN,"$souko_folder/$in{'item'}/$in{'id'}.cgi");
	@souko_item = <IN>;
	close(IN);

	$souko_item_num = @souko_item;

	if ($souko_item_num >= $item_max) {
		&error("武器倉庫がいっぱいです！$back_form");
	}

	push(@souko_item,$newitem);

	open(OUT,">$souko_folder/$in{'item'}/$in{'id'}.cgi");
	print OUT @souko_item;
	close(OUT);

	&unlock($lock_file,$flock_pre);


	&header;

	print <<"EOM";
アイテムを倉庫に入れました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type=hidden name=item value=$in{'item'}>
<input type="hidden" name=mode value="item_edit">
<input type=submit class=btn value="道具詳細に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#------------#
# 新道具追加 #
#------------#
sub new_item_edit {

	$file = "$in{'item'}\_file";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	if ($in{'item'} eq 'acs') {
		$list = '<th>No.</th><th>なまえ</th><th>価格</th><th>効果</th><th>力</th><th>魔力</th><th>信仰心</th><th>生命力</th></tr>';
		$list2 = '<tr><th>器用さ</th><th>速さ</th><th>魅力</th><th>カルマ</th><th>命中率</th><th>回避率</th><th>必殺率</th><th>説明</th></tr>';
	} else {
		$list = '<th>No.</th><th>なまえ</th><th>威力</th><th>価格</th><th>命中/回避率補正</th></tr>';
	}

	$data_sum = @item_array - 2;	# 最後２行はなし用と改行なため

	$item_array[$data_sum] =~ s/\n//g;
	$item_array[$data_sum] =~ s/\r//g;

	@item_data = split(/<>/,$item_array[$data_sum]);

	$new_no = $item_data[0] + 1;

	$new_no = sprintf("%04d",$new_no);

	&header;

	print <<"EOM";
<h1>新しいアイテムの追加（$in{'item'}）</h1>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="new_item_add">
<input type="hidden" name=item value="$in{'item'}">
<input type="hidden" name="item_skill0" value="$new_no">
<table>
$list
<tr>
<td class=b1 align="center">$new_no</td>
EOM
	$i = 0;
	foreach (@item_data) {
		if ($i == 0) { $i++; next; }
		print "<td class=b1><input type=\"text\" name=\"item_skill$i\"></td>";
		$i++;
		if ($i == 8) { print "</tr>$list2<tr>"; }
	}

	$i--;

	print <<"EOM";
</tr></table>
<input type="hidden" name="item_num" value="$i">
<input type=submit class=btn value="新しくアイテムを追加する">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#------------#
# 新道具追加 #
#------------#
sub new_item_add {

	$file = "$in{'item'}\_file";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	$newitem = "";
	for ($i=0;$i<=$in{'item_num'};$i++) {
		$hash = "item_skill$i";
		$newitem .= "$in{$hash}<>";
	}

	push(@item_array,"$newitem\n");

	# 配列1番目でソート
	@tmp = map {(split /<>/)[0]} @item_array;
	@item_array = @item_array[sort {$tmp[$a] <=> $tmp[$b]} 0 .. $#tmp];

	open(OUT,">$$file");
	print OUT @item_array;
	close(OUT);

	&header;

	print <<"EOM";
追加しました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技の一覧">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 道具削除 #
#----------#
sub item_delete {

	$file = "$in{'item'}\_file";
	$folder = "$in{'item'}\_folder";

	open(IN,"$$file");
	@item_array = <IN>;
	close(IN);

	@item_data = split(/<>/,$item_array[$in{'item_no'}]);

	splice(@item_array,$in{'item_no'},1);

	open(OUT,">$$file");
	print OUT @item_array;
	close(OUT);

	# 職業別の道具ファイルの同じ道具も一斉削除
	opendir (DIR,"$$folder") or die "$!";
	foreach $entry (readdir(DIR)){
		if ($entry =~ /\.ini/) {
			if ($file eq "$folder/$entry") { next; }
			open(IN,"$$folder/$entry");
			@item_data = <IN>;
			close(IN);

			open(OUT,">$$folder/$entry");
			foreach (@item_data) {
				($i_no) = split(/<>/);
				if ($item_data[0] eq $i_no) {
					next;
				}
				print OUT $_;
			}
			close(OUT);
		}
	}
	closedir(DIR);

	&header;

	print <<"EOM";
削除しました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_all">
<input type=submit class=btn value="アイテムの一覧">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技の一覧">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#------------#
# 新職業追加 #
#------------#
sub syoku_add_pre {

	$syoku_sum = @chara_syoku;
	$next_syoku = $syoku_sum;

	&header;

	print <<"EOM";
<h1>新しい職業の追加</h1><br>
新しい職業を追加するための準備を行います。<br>
以下の項目を全て記入して下さい。<br>
<b><font color="$yellow" size = 3>なお、ここで間違えた場合、直接plファイルなどを書き換えないといけないので、慎重に入力していただくようにお願いします。</font></b>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku_add" size="40">
攻撃時コメント<br>
攻撃の時に出る職業別の台詞です。<br>
<input type=text name="bcomment" value=""><br><br><br>
攻撃力判定用サブルーチン名<br>
<b><font color="$red" size = 2>syokuの後に次の数字である<font color="$yellow" size = 3>$next_syoku</font>の英語名を入れて下さい。<br>初期状態ではsyokuthirtyが30番の職業のグランドマスター用なので、<br>31はsyokuthirtyoneという感じに次の数字である<font color="$yellow" size = 3>$next_syoku</font>の英語名を入力して下さい。<br>必ず、半角小文字英字で入力して下さい。<br>間違えるとエラーが出てしまいます。</font></b><br>
<input type=text name="asub" value="syoku" size="20"><br><br><br>
攻撃力に反映させる能\力の倍率<br>
<b><font color="$red" size = 2>攻撃力決定の際の計算で、影響を及ぼす能\力の倍数を決めます。<br>0を入力すればその能\力は攻撃力へ及ぼしません。<br>参考としてはグランドマスターの場合は全てが1になっております。<br>必ず、半角数字で入力して下さい。<br>小数でも可能\です。<br>なお、全体というのは武器以外の全ての数値を足したあとにかける数値になります。<br>管理人などの職業では2になっております。</font></b><br>
<table bgcolor="#ffffff">
<tr><th>力</th><th>魔力</th><th>信仰心</th><th>生命力</th><th>器用さ</th><th>速さ</th><th>魅力</th><th>全体</th><th>武器</th></tr>
<tr>
<td align="center"><input type=text name="a1" value="0" size="5"></td>
<td align="center"><input type=text name="a2" value="0" size="5"></td>
<td align="center"><input type=text name="a3" value="0" size="5"></td>
<td align="center"><input type=text name="a4" value="0" size="5"></td>
<td align="center"><input type=text name="a5" value="0" size="5"></td>
<td align="center"><input type=text name="a6" value="0" size="5"></td>
<td align="center"><input type=text name="a7" value="0" size="5"></td>
<td align="center"><input type=text name="at" value="0" size="5"></td>
<td align="center"><input type=text name="ai" value="0" size="5"></td>
</tr>
</table><br>
<input type=submit class=btn value="新しく職業を追加する">
</form>
<hr>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#----------#
# 職業追加 #
#----------#
sub syoku_add {

	if ($in{'a1'} =~ /[^0-9]/ || $in{'a2'} =~ /[^0-9]/ || $in{'a3'} =~ /[^0-9]/ || $in{'a4'} =~ /[^0-9]/ || $in{'a5'} =~ /[^0-9]/ || $in{'a6'} =~ /[^0-9]/ || $in{'a7'} =~ /[^0-9]/ || $in{'at'} =~ /[^0-9]/ || $in{'ai'} =~ /[^0-9]/ || $in{'asub'} =~ /[^_a-z]/) {
		&error("規則にそっていない入力値がありました。$back_form");
	}

	if ($in{'a1'} eq "" || $in{'a2'} eq "" || $in{'a3'} eq "" || $in{'a4'} eq "" || $in{'a5'} eq "" || $in{'a6'} eq "" || $in{'a7'} eq "" || $in{'at'} eq "" || $in{'ai'} eq "" || $in{'asub'} eq "" || $in{'bcomment'} eq "") {
		&error("入力されていない項目があります。$back_form");
	}

	$atacksub = << "EOM";
sub $in{'asub'} {
	\$dmg1 \+\= (int(rand(\$chara\[7\] \* $in{'a1'})) \+ int(rand(\$chara\[8\] \* $in{'a2'})) \+ int(rand(\$chara\[9\] \* $in{'a3'})) \+ int(rand(\$chara\[10\] \* $in{'a4'})) \+ int(rand(\$chara\[11\] \* $in{'a5'})) \+ int(rand(\$chara\[12\] \* $in{'a6'})) \+ int(rand(\$chara\[13\] \* $in{'a7'})) \+ int(\$chara\[20\])) \* $in{'at'} \+ \$item\[1\] \* $in{'ai'}\;
}
EOM
chomp($atacksub);

	$watacksub = << "EOM";
sub w$in{'asub'} {
	\$dmg2 \+\= (int(rand(\$winner\[6\] \* $in{'a1'})) \+ int(rand(\$winner\[7\] \* $in{'a2'})) \+ int(rand(\$winner\[8\] \* $in{'a3'})) \+ int(rand(\$winner\[9\] \* $in{'a4'})) \+ int(rand(\$winner\[10\] \* $in{'a5'})) \+ int(rand(\$winner\[11\] \* $in{'a6'})) \+ int(rand(\$winner\[12\] \* $in{'a7'})) \+ int(\$winner\[13\]))  \* $in{'at'} \+ \$winner\[22\] \* $in{'ai'}\;
}
EOM
chomp($watacksub);

	open(IN,"./battle.pl");
	@new = ();
	foreach (<IN>) {
		$_ =~ s/\"\)\;\#コメント/\"\,\n\t\"$in{'bcomment'}\"\)\;\#コメント/i;
		$_ =~ s/\'\)\;\#職業別攻撃力決定ここまで/\'\,\'$in{'asub'}\'\)\;\#職業別攻撃力決定ここまで/i;
		$_ =~ s/\}\#攻撃力計算ここまで/\}\n$atacksub\#攻撃力計算ここまで/i;
		push(@new,$_);
	}
	close(IN);

	open(OUT,">./battle.pl");
	print OUT @new;
	close(OUT);

	open(IN,"./wbattle.pl");
	@new = ();
	foreach (<IN>) {
		$_ =~ s/\}\#チャンプ攻撃力計算ここまで/\}\n$watacksub\#チャンプ攻撃力計算ここまで/i;
		push(@new,$_);
	}
	close(IN);

	open(OUT,">./wbattle.pl");
	print OUT @new;
	close(OUT);

	$syoku_sum = @chara_syoku - 1;
	$next_syoku = $syoku_sum + 1;

	&header;

	print <<"EOM";
職業追加準備が整いました<br>
ffadventure.ini内の<br>
\$chara_syoku[$syoku_sum] = \"$chara_syoku[$syoku_sum]\"\;<br>
の下に<br>
\$chara_syoku[$next_syoku] = \"新しい職業名\"\;<br>
を追加して下さい。<br>
追加後、職業の編集で細かい詳細を決定すれば職業の追加が完了します<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="syoku_add_pre">
<input type=submit class=btn value="職業の追加に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#--------#
# 技一覧 #
#--------#
sub waza_all {

	&header;

	print <<"EOM";
<h1>技一覧</h1><br>
<form action="$scriptk" method="post">
使用条件とは、その必殺技を使用するのに現在の職業がマスターである必要があるかどうかを示すもので、マスターじゃないと使用できないものが1、マスターでなくとも使用できるのが0として表\示されています。<br>
<table>
<tr>
<th></th><th>No.</th><th>技名</th><th>説明</th><th>使用条件</th></tr>
EOM
	open(IN,"$tac_file");
	@item_array = <IN>;
	close(IN);

	$ino = 0;
	foreach (@item_array) {
		@item = ();
		@item = split(/<>/);
		print <<"EOM";
<tr><td class=b1 align="center">
<input type=radio name=item_no value="$ino">
</td>
EOM
		foreach (@item) {
			print <<"EOM";
<td align=right class=b1>$_</td>
EOM
		}
		print "</tr>\n";
		$ino++;
	}

	print <<"EOM";
</table>
<input type=hidden name=mode value=waza_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="編集">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=mode value=new_waza_edit>
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="新しく必殺技を追加する">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 新技追加 #
#----------#
sub new_waza_edit {

	open(IN,"$tac_file");
	@item_array = <IN>;
	close(IN);

	$data_sum = @item_array - 1;	# 最後２行はなし用と改行なため

	$item_array[$data_sum] =~ s/\n//g;
	$item_array[$data_sum] =~ s/\r//g;

	@item_data = split(/<>/,$item_array[$data_sum]);

	$new_no = $item_data[0] + 1;

	&header;

	print <<"EOM";
<h1>新しい必殺技の追加</h1><br>
まずは、必殺技用の新しいファイルをダウンロードしてきて下さい。<br>
<a href="http://www.eriicu.com" target="_blank">いくのＣＧＩのＨＰ</a><br>
それを挑戦者用のファイル名を<br>
$new_no.pl<br>
としてtechフォルダに入れて下さい。<br>
チャンプ用のファイルを<br>
$new_no.pl<br>
としてwtechフォルダに入れて下さい。<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="new_item_add">
<input type="hidden" name=item value="tac">
<input type="hidden" name="item_skill0" value="$new_no">
<table>
<tr>
<th>No.</th><th>必殺技名</th><th>説明</th><th>使用条件</th>
</tr>
<tr>
<td class=b1 align="center">$new_no</td>
EOM
	$i = 0;
	foreach (@item_data) {
		if ($i == 0) { $i++; next; }
		print "<td class=b1><input type=\"text\" name=\"item_skill$i\"></td>";
		$i++;
		if ($i == 8) { print "</tr>$list2<tr>"; }
	}

	$i--;

	print <<"EOM";
</tr></table>
<input type="hidden" name="item_num" value="$i">
<input type=submit class=btn value="新しく必殺技を追加する">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技の一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#--------#
# 技編集 #
#--------#
sub waza_edit {

	open(IN,"$tac_file");
	@item_array = <IN>;
	close(IN);

	$item_array[$in{'item_no'}] =~ s/\n//g;
	$item_array[$in{'item_no'}] =~ s/\r//g;

	&header;

	@item_data = split(/<>/,$item_array[$in{'item_no'}]);

	print <<"EOM";
<h1>$item_data[1]の編集</h1>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_edit_end">
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name="item_skill0" value="$item_data[0]">
<table>
<tr>
<th>No.</th><th>必殺技名</th><th>説明</th><th>使用条件</th>
</tr>
<tr>
<td class=b1 align="center">$item_data[0]</td>
EOM
	$i = 0;
	foreach (@item_data) {
		if ($i == 0) { $i++; next; }
		print "<td class=b1><input type=\"text\" name=\"item_skill$i\" value=\"$_\"></td>";
		$i++;
	}

	$i--;

	print <<"EOM";
</tr></table>
<input type="hidden" name="item_num" value="$i">
<input type=submit class=btn value="必殺技の編集">
</form>
特定の職業への追加
<TABLE BORDER=0>
<TR>
EOM
	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);

	$s = 0;
	foreach (@chara_syoku) {
		print <<"EOM";
<form action="$scriptk" method="post">
<TD class=b1 align = center>
$chara_syoku[$s]<br>
<input type="hidden" name="syoku" value="$s">
<input type="hidden" name="mode" value="syoku_item_add">
<input type="hidden" name="item_no" value="$in{'item_no'}">
<input type="hidden" name="item" value="tac">
<input type=hidden name=pass value=$in{'pass'}>
<input type="submit" class="btn" value="この職業に追加" size="20">
</TD>
</form>
EOM
		$s++;
		if ($s % 6 == 0) { print "</tr>\n<tr>\n"; }
	}

	print <<"EOM";
</tr>
</table>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="item_delete">
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=item value="tac">
<input type=submit class=btn value="この技を削除する"><br>
(この必殺技を戦術に設定しているプレイヤーの必殺技までは変更されません。)
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技の一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

#--------------------#
# 必殺技ファイル編集 #
#--------------------#
sub waza_edit_end {

	open(IN,"$tac_file");
	@item_array = <IN>;
	close(IN);

	$newitem = "";
	for ($i=0;$i<=$in{'item_num'};$i++) {
		$hash = "item_skill$i";
		$newitem .= "$in{$hash}<>";
	}

	$item_array[$in{'item_no'}] = "$newitem\n";

	open(OUT,">$tac_file");
	print OUT @item_array;
	close(OUT);

	# 職業別の必殺技ファイルの同じ必殺技も一斉変換
	opendir (DIR,"$tac_folder") or die "$!";
	foreach $entry (readdir(DIR)){
		if ($entry =~ /\.ini/) {
			if ($tac_file eq "$tac_folder/$entry") { next; }
			open(IN,"$tac_folder/$entry");
			@item_data = <IN>;
			close(IN);

			open(OUT,">$tac_folder/$entry");
			foreach (@item_data) {
				($i_no) = split(/<>/);
				if ($in{'item_skill0'} ne $i_no) {
					print OUT $_;
				} else {
					print OUT "$newitem\n";
				}
			}
			close(OUT);
		}
	}
	closedir(DIR);

	&header;

	print <<"EOM";
変更しました<br>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=item_no value="$in{'item_no'}">
<input type="hidden" name=mode value="waza_edit">
<input type=submit class=btn value="必殺技詳細に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type="hidden" name=mode value="waza_all">
<input type=submit class=btn value="必殺技の一覧に戻る">
</form>
<form action="$scriptk" method="post">
<input type=hidden name=pass value=$in{'pass'}>
<input type=submit class=btn value="管理TOPに戻る">
</form>
EOM

	&footer;

	exit;

}

