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

# アイテムライブラリの読み込み
require 'item.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# 初期状態の設定(初期状態で所持している武器・防具。0は「なし」になります)
$first_item = 0;	# 武器NO
$first_def = 0;		# 防具NO
$first_acs = 0;		# 装飾品NO

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

#ＩＰアドレスでアクセス制限
foreach (@shut_host) {
	$_ =~ s/\*/\.\*/g;
	if ($ENV{'REMOTE_ADDR'} =~ /$_/) {&error("アクセスできません！！");}
	}

if($mode) { &$mode; }

&chara_make;

#----------------------#
#  キャラクタ作成画面  #
#----------------------#
sub chara_make {

	if($chara_stop){
		&error("現在キャラクターの作成登録はできません"); 
	}

	# ヘッダー表示
	&header;

	print <<"EOM";
<h1>キャラクタ作成画面</h1>
<hr size=0>
<form action="$chara_make" method="post">
<input type="hidden" name="mode" value="make_pre">
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
<td>
<input type="text" name="id" size="10" value="$in{'id'}"><br>
△お好きな半角英数字を4～8文字以内でご記入ください。
</td>
</tr>
<tr>
<td class="b1">パスワード</td>
<td>
<input type="password" name="pass" size="10" value="$in{'pass'}"><br>
△お好きな半角英数字を4～8文字以内でご記入ください。
</td>
</tr>
<tr>
<td class="b1">パスワード変更用単語</td>
<td>
<input type="text" name="passchange" size="10" value="$in{'passchange'}"><br>
△パスワードを変更する時のパスワードです。かなり重要なので忘れないようにメモを取るようにお願いします。
</td>
</tr>
<tr>
<td class="b1">ホームページ名</td>
<td>
<input type="text" name="site" size="40" value="$in{'site'}"><br>
△あなたのホームページの名前を入力してください。（ない場合はオススメＨＰ）
</td>
</tr>
<tr>
<td class="b1">URL</td>
<td>
<input type="text" name="url" size="50" value="$in{'url'}"><br>
△あなたのホームページのアドレスを記入してください。（ない場合はオススメＨＰ）
</td>
</tr>
<tr>
<td class="b1">キャラクターの名前</td>
<td>
<input type="text" name="c_name" size="30" value="$in{'c_name'}"><br>
△作成するキャラクターの名前を入力してください。
</td>
</tr>
<tr>
<td class="b1">キャラクターの性別</td>
<td>
<input type="radio" name="sex" value="0">女　
<input type="radio" name="sex" value="1" checked>男<br>
△作成するキャラクターの性別を選択してください。
</td>
</tr>
<tr>
<td class="b1">キャラクターのイメージ</td>
<td><input type="text" name="chara" size="10" value="$in{'chara'}">
<br>
△作成するキャラクターの画像番号を指定してください。
(<a href="$img_all_list" target="_blank">$vote_gazou</a>)
<br>
指定しなかったり、ない番号をしていするとランダムで選ばれます。
</td>
</tr>
<tr>
<td class="b1">キャラクターの初期職業</td>
<td>
<select name="syoku">
<option value="0">$chara_syoku[0]</option>
<option value="1">$chara_syoku[1]</option>
<option value="2">$chara_syoku[2]</option>
<option value="3">$chara_syoku[3]</option>
</select>
</td>
</tr>
<tr>
<td colspan="2" align="center">
<input type="submit" class="btn" value="これで登録">
</td>
</tr>
</table>
</form>
EOM
	# フッター表示
	&footer;

	exit;
}

#----------------#
#  登録確認画面  #
#----------------#
sub make_pre {

	if ($in{'id'} =~ m/[^0-9a-zA-Z]/){
		&make_error("IDに半角英数字以外の文字が含まれています。"); 
	}
	elsif ($in{'pass'} =~ m/[^0-9a-zA-Z]/){
		&make_error("パスワードに半角英数字以外の文字が含まれています。"); 
	}
	elsif ($in{'id'} eq "" or length($in{'id'}) < 4 or length($in{'id'}) > 8) {
		&make_error("IDは、4文字以上、8文字以下で入力して下さい。");
	}
	elsif ($in{'pass'} eq "" or length($in{'pass'}) < 4 or length($in{'pass'}) > 8) {
		&make_error("パスワードは、4文字以上、8文字以下で入力して下さい。"); 
	}
	elsif ($in{'c_name'} eq "") {
		&make_error("キャラクターの名前が未記入です"); 
	}
	elsif ($in{'sex'} eq "") {
		&make_error("性別が選択されていません");
	}
	elsif ($in{'syoku'} < 0 || $in{'syoku'} > 4) {
		&make_error("職業が選択されていません");
	}
	elsif($in{'passchange'} eq "") {
		&make_error("パスワード変更用単語が設定されていません");
	}

	if ($name_ban) {
		open(IN,"$all_data_file");
		@all_data = <IN>;
		close(IN);
		foreach (@all_data) {
			@all_chara = split(/<>/);
			if ($all_chara[4] eq $in{'c_name'}) {
				close(IN);
				&make_error("同一名のキャラクターがいます");
			}
		}
	}

	if (-e "./charalog/$in{'id'}.cgi") {
		&make_error("そのIDはすでに使用されています");
	}

	$img_sum = @chara_img;
	if (($in{'chara'} ne 0 && !$in{'chara'}) || $in{'chara'} < 0 || $in{'chara'} > $img_sum){
		$in{'chara'} = int(rand($img_sum));
	}

	if ($in{'site'} eq "") {
		$in{'site'} = 'いくのＣＧＩのＨＰ';
	}
	if ($in{'url'} eq "") {
		$in{'url'} = 'http://www.eriicu.com';
	}

		if($in{'sex'}) { $esex = "男"; } else { $esex = "女"; }
		$next_ex = $lv_up;

		&header;

		print <<"EOM";
<h1>登録確認画面</h1>
以下の内容でよろしいでしょうか？
<hr size=0>

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
<td>$intgold</td>
</tr>
<tr>
<td class="b1">レベル</td>
<td>1</td>
<td class="b1">経験値</td>
<td>0/$next_ex</td>
</tr>
<tr>
<td class="b1">パスワード変更用単語</td>
<td><font color="red" size += "2"><b>$in{'passchange'}</b></font></td>
<td class="b1" colspan="2"><b>※重要なので必ずメモして下さい※</b></td>
</tr>
</table>
<form action="$chara_make" method="post">
<input type=hidden name="mode" value="make_end">
<input type=hidden name="id" value="$in{'id'}">
<input type=hidden name="pass" value="$in{'pass'}">
<input type=hidden name="passchange" value="$in{'passchange'}">
<input type=hidden name="site" value="$in{'site'}">
<input type=hidden name="url" value="$in{'url'}">
<input type=hidden name="c_name" value="$in{'c_name'}">
<input type=hidden name="sex" value="$in{'sex'}">
<input type=hidden name="chara" value="$in{'chara'}">
<input type=hidden name="syoku" value="$in{'syoku'}">
<input type=submit class="btn" value="作成する"></form>
<form action="$chara_make" method="post">
<input type=hidden name="id" value="$in{'id'}">
<input type=hidden name="pass" value="$in{'pass'}">
<input type=hidden name="passchange" value="$in{'passchange'}">
<input type=hidden name="site" value="$in{'site'}">
<input type=hidden name="url" value="$in{'url'}">
<input type=hidden name="c_name" value="$in{'c_name'}">
<input type=hidden name="sex" value="$in{'sex'}">
<input type=hidden name="chara" value="$in{'chara'}">
<input type=hidden name="syoku" value="$in{'syoku'}">
<input type=submit class="btn" value="戻る"></form>
EOM

		&footer;

		exit;
}

#----------------#
#  登録完了画面  #
#----------------#
sub make_end {

	&get_host;

	if($chara_stop){ &error("現在キャラクターの作成登録はできません"); }

	if ($in{'id'} =~ m/[^0-9a-zA-Z]/){
		&make_error("IDに半角英数字以外の文字が含まれています。"); 
	}
	elsif ($in{'pass'} =~ m/[^0-9a-zA-Z]/){
		&make_error("パスワードに半角英数字以外の文字が含まれています。"); 
	}
	elsif ($in{'id'} eq "" or length($in{'id'}) < 4 or length($in{'id'}) > 8) {
		&make_error("IDは、4文字以上、8文字以下で入力して下さい。");
	}
	elsif ($in{'pass'} eq "" or length($in{'pass'}) < 4 or length($in{'pass'}) > 8) {
		&make_error("パスワードは、4文字以上、8文字以下で入力して下さい。"); 
	}
	elsif ($in{'c_name'} eq "") {
		&make_error("キャラクターの名前が未記入です"); 
	}
	elsif($in{'sex'} eq "") {
		&make_error("性別が選択されていません");
	}
	elsif($in{'passchange'} eq "") {
		&make_error("パスワード変更用単語が設定されていません");
	}
	elsif($in{'syoku'} eq "") {
		&make_error("職業が選択されていません");
	}
	if($in{'site'} eq "") {
		$in{'site'} = 'いくのＣＧＩのＨＰ';
	}
	if($in{'url'} eq "") {
		$in{'url'} = 'http://www.eriicu.com';
	}

	if ($name_ban && $ip_ban) {
		open(IN,"$all_data_file");
		@all_data = <IN>;
		close(IN);
		foreach (@all_data) {
			@all_chara = split(/<>/);
			if ($all_chara[4] eq $in{'c_name'}) {
				close(IN);
				&make_error("同一名のキャラクターがいます");
			}
			elsif ($all_chara[26] eq $host && $all_chara[0] ne 'test') {
				close(IN);
				&error("同一ＩＰから登録されたキャラがすでに存在します。");
			}
		}
	}
	elsif ($ip_ban) {
		open(IN,"$all_data_file");
		@all_data = <IN>;
		close(IN);
		foreach (@all_data) {
			@all_chara = split(/<>/);
			if ($all_chara[26] eq $host && $all_chara[0] ne 'test') {
				close(IN);
				&error("同一ＩＰから登録されたキャラがすでに存在します。");
			}
		}
	}
	elsif ($name_ban) {
		open(IN,"$all_data_file");
		@all_data = <IN>;
		close(IN);
		foreach (@all_data) {
			@all_chara = split(/<>/);
			if ($all_chara[4] eq $in{'c_name'}) {
				close(IN);
				&make_error("同一名のキャラクターがいます");
			}
		}
	}

	if (-e "./charalog/$in{'id'}.cgi") {
		&make_error("そのIDはすでに使用されています");
	}

	$img_sum = @chara_img;
	if (($in{'chara'} ne 0 && !$in{'chara'}) || $in{'chara'} < 0 || $in{'chara'} > $img_sum){
		$in{'chara'} = int(rand($img_sum));
	}

	if ($in{'syoku'} == 1) {
		$n_0 = 9;
		$n_1 = 14;
		$n_2 = 10;
		$n_3 = 9;
		$n_4 = 11;
		$n_5 = 8;
		$n_6 = 10;
		$lp = 5;
	} elsif ($in{'syoku'} == 2) {
		$n_0 = 9;
		$n_1 = 10;
		$n_2 = 12;
		$n_3 = 9;
		$n_4 = 11;
		$n_5 = 8;
		$n_6 = 12;
		$lp = 5;
	} elsif ($in{'syoku'} == 3) {
		$n_0 = 11;
		$n_1 = 8;
		$n_2 = 8;
		$n_3 = 11;
		$n_4 = 13;
		$n_5 = 8;
		$n_6 = 12;
		$lp = 5;
	} else {
@kiso_nouryoku = ("9","8","8","9","9","8","8");
		$n_0 = 13;
		$n_1 = 8;
		$n_2 = 8;
		$n_3 = 13;
		$n_4 = 11;
		$n_5 = 10;
		$n_6 = 8;
		$lp = 5;
	}

	$newdata = time();

	$new_chara = "$in{'id'}<>$in{'pass'}<>$in{'site'}<>$in{'url'}<>$in{'c_name'}<>$in{'sex'}<>$in{'chara'}<>$n_0<>$n_1<>$n_2<>$n_3<>$n_4<>$n_5<>$n_6<>$in{'syoku'}<>$kiso_hp<>$kiso_hp<>0<>1<>$intgold<>$lp<>0<>0<>$clt_comment<>$first_item<>$sentou_limit<>$host<>$newdata<>$boss<>$first_def<>0<>$first_acs<>0<>1<>";

	if ($first_item) {
		&item_read($first_item);
	} else {
		&item_lose;
	}

	if ($first_def) {
		&def_read($first_def);
	} else {
		&def_lose;
	}

	if ($first_acs) {
		&acs_read($first_acs);
	} else {
		&acs_lose;
	}

	foreach(@item){
		$new_item .="$_<>";
	}

	$lock_file = "$lockfolder/all.lock";
	&lock($lock_file,'ALL');
	open(OUT,">>./$all_data_file"); 
	print OUT "$new_chara\n"; 
	close(OUT); 
	&unlock($lock_file,'ALL');

	open(OUT,">./charalog/$in{'id'}.cgi"); 
	print OUT $new_chara; 
	close(OUT); 

	open(OUT,">./$pass_folder/$in{'id'}.cgi"); 
	print OUT "$in{'pass'}<>$in{'passchange'}<>$newdata<>$host<>\n"; 
	close(OUT); 

	open(OUT,">./item/$in{'id'}.cgi"); 
	print OUT $new_item; 
	close(OUT);

	if($in{'sex'}) { $esex = "男"; } else { $esex = "女"; }
	$next_ex = $lv * $lv_up;

	&all_message("$in{'c_name'}さんが新たにキャラ作成されました！みなさんよろしく！");

		&header;

		print <<"EOM";
<h1>登録完了画面</h1>
以下の内容で登録が完了しました。
<hr size=0>
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
<td>$intgold</td>
</tr>
<tr>
<td class="b1">レベル</td>
<td>1</td>
<td class="b1">経験値</td>
<td>0/$next_ex</td>
</tr>
<tr>
<td class="b1">HP</td>
<td>$kiso_hp</td>
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
<form action="$loginscript" method="post">
<input type="hidden" name=mode value=log_in>
<input type="hidden" name=id value="$in{'id'}">
<input type="hidden" name=pass value="$in{'pass'}">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM

		&footer;

		exit;
}

#--------------------#
#  登録用エラー画面  #
#--------------------#
sub make_error{
	&header;
	print "<center><hr width=400><h3>ERROR !</h3>\n";
	print "<font color=red><B>$_[0]</B></font>\n";
	print "<hr width=400></center>\n";
	print <<"EOM";
<br>
<form action="$chara_make" method="post">
<input type=hidden name="id" value="$in{'id'}">
<input type=hidden name="pass" value="$in{'pass'}">
<input type=hidden name="passchange" value="$in{'passchange'}">
<input type=hidden name="site" value="$in{'site'}">
<input type=hidden name="url" value="$in{'url'}">
<input type=hidden name="c_name" value="$in{'c_name'}">
<input type=hidden name="sex" value="$in{'sex'}">
<input type=hidden name="chara" value="$in{'chara'}">
<input type=hidden name="syoku" value="$in{'syoku'}">
<input type=submit class="btn" value="戻る"></form>
EOM
	print "<a href=\"$scripto\">TOPページへ</a>\n";
	print "</body></html>\n";
	exit;
}