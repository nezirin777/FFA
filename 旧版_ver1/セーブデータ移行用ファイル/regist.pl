#----------------------#
#  キャラ読み込み処理  #
#----------------------#
sub chara_load {

	open(IN,"./charalog/$in{'id'}.cgi") || &error("キャラクターが見つかりません$ENV{'CONTENT_LENGTH'}");
	$chara_log = <IN>;
	close(IN);

	@chara = split(/<>/,$chara_log);

}

#------------------------#
#  アイテム読み込み処理  #
#------------------------#
sub item_load {

	open(IN,"./item/$chara[0].cgi");
	$item_log = <IN>;
	close(IN);

	@item = split(/<>/,$item_log);

}

#--------------------#
#  職業読み込み処理  #
#--------------------#
sub syoku_load {

	open(IN,"./syoku/$chara[0].cgi");
	$syoku_log = <IN>;
	close(IN);

	@syoku_master = split(/<>/,$syoku_log);

}

#------------------------#
#  キャラクターチェック  #
#------------------------#
sub chara_check {

	$chara_log =~ s/</&lt;/g;
	$chara_log =~ s/>/&gt;/g;

	if ($in{'mydata'} ne $chara_log){
		&error('キャラデータ不整合');
	}

}

#----------------#
#  書き込み処理  #
#----------------#
sub chara_regist {

	if ($chara[19] > $gold_max) { $chara[19] = $gold_max; }

	$new_chara = '';

	$new_chara = join('<>',@chara);

	$new_chara .= '<>';

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT $new_chara;
	close(OUT);

}

#--------------------#
#  チャンプ読み込み  #
#--------------------#
sub read_winner {
	open(IN,"$winner_file");
	$winner_log = <IN>;
	close(IN);

	@winner = split(/<>/,$winner_log);
}

#----------------#
#  デコード処理  #
#----------------#
sub decode {

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("投稿量が大きすぎます"); }
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }
	@pairs = split(/&/, $buffer);
	foreach (@pairs) {
		($name,$value) = split(/=/, $_);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# 文字コードをシフトJIS変換
		&jcode'convert(*value, "sjis", "", "z");

		# タグ処理
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\"/&quot;/g;

		# 改行等処理
		$value =~ s/\r//g;
		$value =~ s/\n//g;

		$in{$name} = $value;
	}

	$mode = $in{'mode'};
	$cookie_pass = $in{'pass'};
	$cookie_id = $in{'id'};
}

#----------------#
#  ホスト名取得  #
#----------------#
sub get_host {

	if ($get_remotehost) {
		$host = $ENV{'REMOTE_HOST'};
		$addr = $ENV{'REMOTE_ADDR'};
		if ($host eq "" || $host eq "$addr") {
			$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
		}
		if ($host eq "") { $host = $addr; }
	} else { $host = $ENV{'REMOTE_ADDR'}; }
	$chara[26] = $host;
}

#--------------#
#  エラー処理  #
#--------------#
sub error {

	foreach (keys %lock_flg) {
		if ($lock_flg{$_}) {
			if ($lockkey == 3) {
				foreach (@flock) {
					($flock_file,$flock_pre) = split(/,/);
					if ($flock_file eq $_) {
						last;
					}
				}
			}
			&unlock($_,$flock_pre);
		}
	}

	&header;
	print "<center><hr width=400><h3>ERROR !</h3>\n";
	print "<font color=red><B>$_[0]</B></font>\n";
	print "<hr width=400></center>\n";
	print "<a href = \"$scripto\">$main_titleのTOPへ</a>\n";
	print "</body></html>\n";
	exit;
}

#--------------#
#  クラス設定  #
#--------------#
sub class {

	$class_flg = int($chara[33]/10);

	@class_mark = (
		'■□□□□□<i><b>(Beginner)</b></i>'
		,'■■□□□□<i><b>(Charanger)</b></i>'
		,'■■■□□□<i><b>(LowClass)</b></i>'
		,'■■■■□□<i><b>(NormalClass)</b></i>'
		,'■■■■■□<i><b>(HighClass)</b></i>'
		,'■■■■■■<i><b>(TopClass)</b></i>'
		,'★★★★★★<i><b>(Master)</b></i>'
	);

	$class = $class_mark[$class_flg];
}

#--------------------#
# ファイルロック開始 #
#--------------------#
sub lock {

	# symlink関数
	if ($lockkey == 1) {
		local($retry) = 5;
		while (!symlink(".", $_[0])) {
			if (--$retry <= 0) {
				&error("LOCK is BUSY");
			}
			sleep(1);
		}
	}
	# open関数
	elsif ($lockkey == 2) {
		local($retry) = 0;
		foreach (1 .. 5) {
			if (-e $_[0]) {
				sleep(1); 
			}
			else {
				open(LOCK,">$_[0]") || &error("Can't Lock");
				close(LOCK);
				$retry = 1;
				last;
			}
		}
		if (!$retry) {
			if ((stat $_[0])[9] > time() - 300) {
				unlink($_[0]);
			} else {
				&error("しばらくお待ちになってください(^^;)");
			}
		}
	}
	# flock関数
	elsif ($lockkey == 3) {
		open($_[1],">$_[0]");
		flock(2,$_[1]);
		push(@flock,"$_[0],$_[1],\n");
	}

	$lock_flg{$_[0]} = 1;
}

#---------------------#
#  ロックファイル解除 #
#---------------------#
sub unlock {
	
	if ($lockkey == 3) {
		flock(8,$_[1]);
		close($_[1]);
		unlink($_[0]);
	} else {
		if (-e $_[0]) {
			unlink($_[0]);
		}
	}
	$lock_flg{$_[0]} = 0;
}

#------------------#
#  HTMLのヘッダー  #
#------------------#
sub header {
	print "Cache-Control: no-cache\n";
	print "Pragma: no-cache\n";
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<SCRIPT Language="JavaScript" src="$java_script" type="text/javascript">
</SCRIPT>
EOM
	&time_view;
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
//-->
</STYLE>
<link rel="stylesheet" href="$style_sheet" type="text/css">
<title>$main_title</title></head>
<body background="$backgif" bgcolor="$bgcolor" text="$text" link="$link" vlink="$vlink" alink="$alink">
EOM
	if($midi_set){
		print "<embed src=\"$midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	}
}

#------------#
#  タイマー  #
#------------#
sub time_view{
	if($ltime < $b_time  and $ztime > 0){
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
	setTimeout("CountDown()",500);
//-->
</SCRIPT>
EOM
	}
}

#------------------#
#　HTMLのフッター　#
#------------------#
sub footer {

	# 著作権表示・改変厳禁

	print << "EOM";
<a href = "$scripto">$main_titleのTOPへ</a>
<HR SIZE=0 WIDTH="100%"><DIV align=right>
FFA いく改ver2.00 edit by <a href="http://www.eriicu.com" target="_top">いく</a><br>
FFA Emilia Ver1.01 remodeled by Classic(閉鎖)<br>
FF Battle De I v3.06 remodeling by <a href="http://www.mj-world.jp/" target="_blank">jun-k</a>(更新停止中)<br>
FF ADVENTURE(改) v1.040 remodeled by <a href="http://www.gun-online.com" target="_blank">ＧＵＮ</a><br>
FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) <a href="http://www5c.biglobe.ne.jp/~ma-ti/" target="_blank">現配布元(管理者ma-ti)</a><br>
</DIV></body></html>
EOM
}

#------------------#
#　メッセージ表示　#
#------------------#
sub message_load {

	print "【届いているメッセージ】表\示数<b>$max_gyo</b>件まで";
	open(IN,"$message_file/$chara[0].cgi");
	@MESSAGE_LOG = <IN>;
	close(IN);

	$hit=0;$i=1;
	foreach(@MESSAGE_LOG){
		($hid,$hname,$htime,$hmessage,$hhost) = split(/<>/);
		if ($max_gyo < $i) {
			last;
		}
		print <<"EOM";
<hr size=0>
<table><tr>
<td>
<font color="$red">
<small><b>$hnameさん</b>　＞ 「<b>$hmessage</b>」$htime\[$hhost\]</small>
</font>
</td>
EOM
		if ($hid ne 'sys') {
			print <<"EOM";
<td>
<table>
<tr>
<form action="$script_post" method="POST">
<td>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="hidden" name="mode" value="res">
<input type="hidden" name="mesid" value="$hid">
<input type="hidden" name="mesname" value="$hname">
<input type="submit" class="btn" value="返信">
</td>
</form>
<form action="$script_post" method="post">
<td>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name="bansts" value="2">
<input type=hidden name="mode" value="ban_do">
<input type="hidden" name="mesid" value="$hid">
<input type="hidden" name="mesname" value="$hname">
<input type=submit class=btn value="友達登録">
</td>
</form>
<form action="$script_post" method="post">
<td>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name="bansts" value="1">
<input type=hidden name="mode" value="ban_do">
<input type="hidden" name="mesid" value="$hid">
<input type="hidden" name="mesname" value="$hname">
<input type=submit class=btn value="拒否">
</td>
</form>
</tr></table></td>
EOM
}
		print <<"EOM";
</tr></table>
EOM
		$hit=1;$i++;
	}
	if(!$hit){
		print "<hr size=0><font color=$red>$chara[4]さん宛てのメッセージはありません</font>\n";
	}
	print "<hr size=0>";

	print "【全員宛てメッセージ】表\示数<b>$all_max_gyo</b>件まで";
	open(IN,"$all_message_file");
	@MESSAGE_LOG = <IN>;
	close(IN);

	$hit=0;$i=1;
	foreach(@MESSAGE_LOG){
		($hid,$hname,$htime,$hmessage,$hhost) = split(/<>/);
			if($max_gyo < $i) {
				last;
			}
			print <<"EOM";
<hr size=0>
<font color="$red">
<small>「<b>$hmessage</b>」$htime\[$hhost\]</small>
</font><br>
EOM
				$hit=1;$i++;
	}

	if(!$hit){
		print "<hr size=0><font color=$red>全員宛てのメッセージはありません</font>\n";
	}
	print "<hr size=0>";
}

#----------------------------#
#　全員へのメッセージ書込み　#
#----------------------------#
sub all_message {

	&get_time(time());
	$lock_file = "$lockfolder/alm.lock";
	&lock($lock_file,'ALM');
	open(IN,"$all_message_file");
	@MESSAGE_LOG = <IN>;
	close(IN);

	$message_num = @MESSAGE_LOG;

	if ($message_num > $all_mes_max) { pop(@MESSAGE_LOG); }

	unshift(@MESSAGE_LOG,"$chara[0]<>$chara[4]<>$gettime<>$_[0]<>$host<>\n");

	open(OUT,">$all_message_file");
	print OUT @MESSAGE_LOG;
	close(OUT);
	&unlock($lock_file,'ALM');
}

#--------------#
#  時間を取得  #
#--------------#
sub get_time {
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($_[0]);
	@week = ('日','月','火','水','木','金','土');

	# 日時のフォーマット
	$gettime = sprintf("%04d年%02d月%02d日(%s)%02d時%02d分",$year+1900,$mon+1,$mday,$week[$wday],$hour,$min);
}

#------------------------#
#  全員データの取り出し  #
#------------------------#
sub all_data_read {
	$lock_file = "$lockfolder/tim.lock";
	&lock($lock_file,'TM');
	open(IN,"$all_data_time");
	@all_time = <IN>;
	close(IN);

	$hit=0;
	foreach(@all_time){
		($rankmode,$ranktime) = split(/<>/);
		if ($rankmode eq "all") { $hit=1;last; }
	}

	$ltime = time();
	$btime = $ltime - $ranktime;
	$ztime = int($btime/3600);

	if ($btime > 3600*24 || !$hit) {

		$hit=0;
		@item_new=();
		foreach (@all_time) {
			($rankmode,$ranktime) = split(/<>/);
			if ($rankmode eq "all") {
				unshift(@item_new,"all<>$ltime<>\n");
				$hit=1;
			} else {
				push(@item_new,"$_");
			}
		}

		if (!$hit) { unshift(@item_new,"all<>$ltime<>\n"); }

		open(OUT,">$all_data_time");
		print OUT @item_new;
		close(OUT);
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');

		opendir (DIR,'./charalog') or die "$!";
		foreach $entry (readdir(DIR)){

			if ($entry =~ /\.cgi/) {
				open(IN,"./charalog/$entry");
				$WORK=<IN>;
				$WORK =~ s/\n//gi;
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

	} else {
		$lock_file = "$lockfolder/tim.lock";
		&unlock($lock_file,'TM');

		open(IN,"$all_data_file");
		@RANKING = <IN>;
		close(IN);

	}

}

#--------------------------------#
#  全員データからの名前取り出し  #
#--------------------------------#
sub all_name_search {

	&all_data_read;

	$aite_hit = 0;
	foreach (@RANKING) {
		($aiteid,undef,undef,undef,$rname) = split(/<>/);
		if ($rname eq $_[0]) {
			$aite_hit = 1;
			last;
		}
	}

	if (!$aite_hit) {
		&error("相手の名前が見つかりません！$_[1]");
	}
}

1;
