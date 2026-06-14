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
<form action="$script_post" method="post">
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
&messe;

exit;

#--------------#
#  メッセージ  #
#--------------#
sub message {

	&chara_load;

	&chara_check;

	if($in{'mes'} eq "") {
		&error("メッセージが記入されていません$back_form");
	}
	elsif($in{'mesid'} eq "" && $in{'mesname'} eq "") {
		&error("相手が指定されていません$back_form");
	}
	elsif($in{'id'} eq "test"){
		&error("テストキャラではメッセージを送信できません！$back_form");
	}

	&get_time(time());

	&get_host;

	&all_data_read;

	$mhit = 0;
	foreach (@RANKING) {
		s/\n//gi;
		s/\r//gi;
		@aite_data = split(/<>/);
		if ($aite_data[0] eq $in{'mesid'} || $aite_data[4] eq $in{'mesname'}) {
			$mhit = 1;
			last;
		}
	}

	if ($aite_data[0] eq $chara[0]) {
		&error("自分にはメッセージを送信できません！$back_form");
	}

	# 相手が見つからない時
	if (!$mhit) {
		&mes_error;
	}

	$now_mes = length($in{'mes'});

	foreach (@ban_word) {
		if(index($in{'mes'},$_) >= 0) {
			$in{'mesname'} = $aite_data[4];
			&error("暴\言は禁止されています");
		}
	}

	if ($now_mes > $mes_size) {
		$in{'mesname'} = $aite_data[4];
		&res("メッセージが長すぎます！半角で$mes_size文字までです！(現在文字数：$now_mes)<br>");
	}

	# 拒否状態の呼び出し
	open(IN,"$ban_file/$aite_data[0].cgi");
	@ban_sts = <IN>;
	close(IN);

	$ban_hit = 0;
	foreach (@ban_sts) {
		s/\n//gi;
		s/\r//gi;
		($banid,$bansts) = split(/<>/);
		if ($banid eq 'all'){
			$ban_hit = 1;
		} elsif ($banid eq $chara[0] && $bansts eq 1) {
			# 拒否してる人からのメッセージ
			$ban_hit = 1;
			last;
		} elsif ($banid eq $chara[0] && $bansts eq 2) {
			# 友達登録してる人からのメッセージ
			$ban_hit = 0;
			last;
		}
	}

	if ($ban_hit || $aite_data[0] eq 'test') {
		&error("メッセージ制限中です$back_form");
	}

	$lock_file = "$lockfolder/messa$aite_data[0].lock";
	&lock($lock_file,'MS');
	open(IN,"$message_file/$aite_data[0].cgi");
	@mes_regist = <IN>;
	close(IN);

	$mes_sum = @mes_regist;

	if($mes_sum > $mes_max) { pop(@mes_regist); }

	unshift(@mes_regist,"$chara[0]<>$chara[4]<>$gettime<>$in{'mes'}<>$host<>\n");

	open(OUT,">$message_file/$aite_data[0].cgi");
	print OUT @mes_regist;
	close(OUT);
	&unlock($lock_file,'MS');

	$lock_file = "$lockfolder/sousin$chara[0].lock";
	&lock($lock_file,'MS');
	open(IN,"$sousin_file/$chara[0].cgi");
	@sousin = <IN>;
	close(IN);

	$mes_sum = @sousin;

	if($mes_sum > $mes_max) { pop(@sousin); }

	unshift(@sousin,"$aite_data[0]<>$aite_data[4]<>$gettime<>$in{'mes'}<>$host<>\n");

	open(OUT,">$sousin_file/$chara[0].cgi");
	print OUT @sousin;
	close(OUT);
	&unlock($lock_file,'MS');

	&header;

	print <<"EOM";
<h1>$aite_data[4]さんへメッセージを送りました。</h1>
<hr size=0>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#------------------#
#メッセージシステム#
#------------------#
sub messe {

	&chara_load;

	&chara_check;

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>好きなキャラクターへメッセージを送る</h1>
<hr>※他のキャラクターへメッセージを送ることができます。
<table width = "100%">
<tr><td class="b2">名前を指定して送る</td>
<form action="$script_post" method="post">
<td class="b2" valign="top">
名前　　　 ：<input type="text" name="mesname" size=10><br>
メッセージ：<input type="text" name="mes" size=50><br><br>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=message>
<input type=submit class=btn value="メッセージを送る">
</td>
</form>
<td class="b2" align="left" valign="top" rowspan=2>
EOM

	&message_load;

	require 'sousin.pl';

	print <<"EOM";
</td></tr>
<tr>
<td class="b2">名前を選んで送る</td>
<td class="b2" valign="top">
<br>
<form action="$script_post" method="post">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=all_list>
<input type=submit class=btn value="一覧から名前を選ぶ">
</form>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="hidden" name="mode" value="ban">
<input type=submit class=btn value="メッセージ拒否">
</form>
<form action="$script_post" method="post">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=friend>
<input type=submit class=btn value="友達登録">
</form>
<form action="$script_post" method="post">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value="limit">
<input type=submit class=btn value="受信凍結">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
</td>
</tr></table>
EOM

	&footer;

	exit;
}

#------------------#
#メッセージシステム#
#------------------#
sub all_list {

	&chara_load;

	&chara_check;

	&all_data_read;

	# 配列19番目でソート
	@tmp = map {(split /<>/)[18]} @RANKING;
	@RANKING = @RANKING[sort {$tmp[$b] <=> $tmp[$a]} 0 .. $#tmp];

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>好きなキャラクターへメッセージを送る</h1>
<hr>※他のキャラクターへメッセージを送ることができます。
<table>
<tr>
<td class="b2">メッセージ</td>
<form action="$script_post" method="post">
<td class="b2" valign="top">
<input type="text" name=mes size=50>
</td></tr>
<tr>
<td class="b2">名前選択</td>
<td class="b2" valign="top">
<select name=mesid size=20>
EOM

	foreach (@RANKING) {
		s/\n//gi;
		s/\r//gi;
		@aite_data = split(/<>/);
		print << "EOM";
<option value = "$aite_data[0]">$aite_data[4]さん(Lv.$aite_data[18])へ
EOM
	}
	print <<"EOM";
</select>
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type="hidden" name="mode" value="message">
<input type=submit class=btn value="メッセージを送る">
</td>
</form>
</tr></table>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#------#
# 返信 #
#------#
sub res {

	&chara_load;

	&chara_check;

	# ヘッダー表示
	&header;

	print <<"EOM";
<h2>$_[0]</h2>
<h1>$in{'mesname'}さんへメッセージを送る</h1>
<form action="$script_post" method="post">
メッセージ：<input type="text" name="mes" size=50 value = "$in{'mes'}"><br><br>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type="hidden" name="mesid" value="$in{'mesid'}">
<input type="hidden" name="mesname" value="$in{'mesname'}">
<input type=hidden name=mode value=message>
<input type=submit class=btn value="メッセージを送る">
</form>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#--------------------#
# 相手が見つからない #
#--------------------#
sub mes_error {

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>相手が見つかりません！</h1>
<form action="$script_post" method="post">
名前　　　 :<input type="text" name="mesname" value="$in{'mesname'}" size="20">
<br>
メッセージ：<input type="text" name="mes" size="50" value ="$in{'mes'}">
<br><br>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=message>
<input type=submit class=btn value="メッセージを送る">
</form>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#----------#
# 受信制限 #
#----------#
sub limit {

	&chara_load;

	&chara_check;

	open(IN,"$ban_file/$chara[0].cgi");
	@ban_sts = <IN>;
	close(IN);

	@new_ban = "";
	$ban_hit = 0;
	@ban_mes = ('解除','設定');
	foreach (@ban_sts) {
		s/\n//gi;
		s/\r//gi;
		($banid,$bansts) = split(/<>/);
		if ($banid eq "all") {
			$ban_hit = 1;
			last;
		}
	}

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>メッセージを友達以外から受信しないようにします</h1><br>
EOM
	if ($ban_hit) {
	print <<"EOM";
現在の設定：制限中<br>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value=limit_do>
<input type=hidden name=bansts value="0">
<input type=submit class=btn value="制限解除">
</form>
EOM
	} else {
	print <<"EOM";
現在の設定：制限解除中<br>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=hidden name=mode value=limit_do>
<input type=hidden name=bansts value="1">
<input type=submit class=btn value="制限する">
</form>
EOM
	}
	print <<"EOM";
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#------------------#
#  拒否・友達登録  #
#------------------#
sub limit_do {

	&chara_load;

	&chara_check;

	# 拒否状態の呼び出し
	$lock_file = "$lockfolder/banfr$chara[0].lock";
	&lock($lock_file,'BF');
	open(IN,"$ban_file/$chara[0].cgi");
	@ban_sts = <IN>;
	close(IN);

	@new_ban = "";
	$ban_hit = 0;
	@ban_mes = ('解除','設定');
	foreach (@ban_sts) {
		s/\n//gi;
		s/\r//gi;
		($banid,$bansts) = split(/<>/);
		if ($banid eq "all") {
			if ($in{'bansts'}) {
				push(@new_ban,"all<>\n");
				$ban_hit = 1;
			}
		} else {
			push(@new_ban,"$_");
		}
	}

	if (!$ban_hit && $in{'bansts'}) {
			push(@new_ban,"all<>\n");
	}

	open(OUT,">$ban_file/$chara[0].cgi");
	print OUT @new_ban;
	close(OUT);
	&unlock($lock_file,'BF');

	&header;

	print <<"EOM";
<h1>制限を$ban_mes[$in{'bansts'}]しました。</h1>
<hr size=0>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

#--------------#
# 拒否システム #
#--------------#
sub ban {

	&chara_load;

	&chara_check;

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>嫌な人からのメッセージを拒否できます</h1>
<table>
<tr>
<form action="$script_post" method="post">
<td class="b2" valign="top">
名前を指定して拒否<br>
<input type="text" name="mesname" size=10>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=ban_do>
<input type=hidden name=bansts value="1">
<input type=submit class=btn value="拒否">
</td>
</form>
</tr>
<tr>
<form action="$script_post" method="post">
<td class="b2" valign="top">
現在の拒否者リスト<br>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value="ban_do">
<input type=hidden name=bansts value="0">
<select name=mesid size=5>
EOM
	# 拒否状態の呼び出し
	open(IN,"$ban_file/$chara[0].cgi");
	@ban_sts = <IN>;
	close(IN);

	$ban_hit = 0;
	foreach (@ban_sts) {
		s/\n//gi;
		s/\r//gi;
		($banid,$bansts,$banname) = split(/<>/);
		if ($bansts eq 1) {
			print << "EOM";
<option value = "$banid">$bannameさん
EOM
			$ban_hit = 1;
		}
	}

	if (!$ban_hit) {
		print "<option value = \"\">いません";
	}
	print <<"EOM";
<input type=submit class=btn value="拒否解除">
</td>
</form>
</tr>
<tr>
<td class="b2" valign="top">
<br>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
</td>
</tr></table>
EOM

	&footer;

	exit;
}

#--------------#
# 友達システム #
#--------------#
sub friend {

	&chara_load;

	&chara_check;

	# ヘッダー表示
	&header;

	print <<"EOM";
<h3>受信凍結中でもメッセージを受け付ける相手を指定できます</h3>
<table>
<tr>
<form action="$script_post" method="post">
<td class="b2" valign="top">
名前を指定して登録<br>
<input type="text" name="mesname" size=10>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=mode value=ban_do>
<input type=hidden name=bansts value="2">
<input type=submit class=btn value="友達登録">
</td>
</form>
</tr>
<tr>
<form action="$script_post" method="post">
<td class="b2" valign="top">
現在の友達リスト<br>
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name=mydata value="$chara_log">
<input type=hidden name=bansts value="0">
<input type=hidden name=mode value="ban_do">
<select name=mesid size=5>
EOM
	# 友達の呼び出し
	open(IN,"$ban_file/$chara[0].cgi");
	@ban_sts = <IN>;
	close(IN);

	$ban_hit = 0;
	foreach (@ban_sts) {
		s/\n//gi;
		s/\r//gi;
		($banid,$bansts,$banname) = split(/<>/);
		if ($bansts eq 2) {
			print << "EOM";
<option value = "$banid">$bannameさん
EOM
			$ban_hit = 1;
		}
	}

	if (!$ban_hit) {
		print "<option value = \"\">いません";
	}
	print <<"EOM";
<input type=submit class=btn value="友達解除">
</td>
</form>
</tr>
<tr>
<td class="b2" valign="top">
<br>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
</td>
</tr></table>
EOM

	&footer;

	exit;
}

#------------------#
#  拒否・友達登録  #
#------------------#
sub ban_do {

	&chara_load;

	&chara_check;

	if($in{'mesid'} eq "" && $in{'mesname'} eq "") {
		&error("相手が指定されていません$back_form");
	}

	&all_data_read;

	$mhit = 0;
	foreach (@RANKING) {
		s/\n//gi;
		s/\r//gi;
		@aite_data = split(/<>/);
		if ($aite_data[0] eq $in{'mesid'} || $aite_data[4] eq $in{'mesname'}) {
			$mhit = 1;
			last;
		}
	}

	if ($aite_data[0] eq $chara[0]) {
		&error("自分は登録できません！$back_form");
	}

	# 相手が見つからない時
	if (!$mhit) {
		&error("相手が見つかりません！$back_form");
	}

	# 拒否状態の呼び出し
	$lock_file = "$lockfolder/banfr$chara[0].lock";
	&lock($lock_file,'BF');
	open(IN,"$ban_file/$chara[0].cgi");
	@ban_sts = <IN>;
	close(IN);

	@new_ban = "";
	$ban_hit = 0;
	@ban_mes = ('解除','拒否登録','友達登録');
	foreach (@ban_sts) {
		s/\n//gi;
		s/\r//gi;
		($banid,$bansts) = split(/<>/);
		if ($banid eq $aite_data[0]) {
			if ($in{'bansts'}) {
				push(@new_ban,"$aite_data[0]<>$in{'bansts'}<>$aite_data[4]<>\n");
			}
			$ban_hit = 1;
		} else {
			push(@new_ban,"$_\n");
		}
	}

	if (!$ban_hit) {
		push(@new_ban,"$aite_data[0]<>$in{'bansts'}<>$aite_data[4]<>\n");
	}

	open(OUT,">$ban_file/$chara[0].cgi");
	print OUT @new_ban;
	close(OUT);
	&unlock($lock_file,'BF');

	&header;

	print <<"EOM";
<h1>$aite_data[4]さんを$ban_mes[$in{'bansts'}]しました。</h1>
<hr size=0>
<form action="$script_post" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="郵便局の最初の画面へ">
</form>
<form action="$script" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$chara_log">
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM

	&footer;

	exit;
}

