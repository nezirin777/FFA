#!/usr/bin/perl -w

#↑ この行はサーバの環境に合わせて書き換えて下さい。
#Internal Server Error が出てしまう場合、下記の記載を試して下さい。

#!/usr/local/bin/perl -w
#!C:/Perl/bin/perl.exe -w

#######################################################################
=pod
すぐ使えるCGI Perl文法チェック&環境調査CGI Ver. 1.0
$RCSfile: test.cgi,v $
$Revision: 1.13 $

Copyright(c) web-ware.org All rights reserved.
http://sugutsukaeru.jp/

このCGIは無料でお使いいただけます。
著作権は作者が保有しています。
ご自身でご利用になる場合改変は自由ですが、再配布および改変品の再配布は
禁止です。
=cut
#######################################################################

#use strict;
#use warnings;

binmode STDOUT;
print "Content-type: text/html;charset=shift_jis\r\n";

my (
%val,
@modules,
@modules_check,
@jclibs,
@smcommands,
@in,
$temp,
);

#デフォルトチェックの設定
@modules = qw(
CGI
File::Basename
File::Path
Jcode
);

@jclibs = qw(
jcode.pl
/usr/lib/jcode.pl
/lib/jcode.pl
);

@smcommands = qw(
/usr/sbin/sendmail
/usr/bin/sendmail
/usr/lib/sendmail
/sbin/sendmail
/bin/sendmail
/lib/sendmail
);

#送信値
if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $temp, $ENV{'CONTENT_LENGTH'});
}
@in = split(/[&;]/, $temp || $ENV{'QUERY_STRING'});

$val{perlversion} = $] >= 5.006?
	sprintf(
		'%s (%vd)',
		$],
		$^V,
	)
		:
	sprintf(
		'%s',
		$],
	)
;

$val{os} = $^O;
($val{myname}) = $0 =~ /([^\/\\:]+)$/;

$val{currentdir} = `pwd`;
unless ($val{currentdir}){
	($val{currentdir}) = ($ENV{'SCRIPT_FILENAME'}||$0) =~ /(.*?)[^\/\\:]+$/;
}

$val{perlpath} = $^X;

foreach (qw(currentdir perlpath)){
	$val{$_} =~ s@\\@/@g;
}

$val{process_user} = sprintf(
	'%s (%s)',
	$> || '',
	eval{ scalar getpwuid($>) },
);

$val{if_owned_by_user} = -o $0;

if (scalar @in){
	foreach my $i (0 .. $#in) {
		# Convert plus to space
		$in[$i] =~ s/\+/ /g;

		# Split into key and value.
		my ($key, $val) = split(/=/,$in[$i],2); # splits on the first =.

		# Convert %XX from hex numbers to alphanumeric
		$key =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;
		$val =~ s/%([A-Fa-f0-9]{2})/pack("c",hex($1))/ge;

		if ($key eq 'targetfile' and $val ne ''){ #チェック対象ファイルの指定
			if ($val =~ /^[\.\/]/ or $val =~ /\//){
				$val{checkresult_error} = sprintf(
					'同じディレクトリ内のファイル名だけを指定して下さい。（%s）',
					$val,
				);
			} elsif ($val =~ /^[\w~-][\w~\.-]*$/){
				$val{targetfile} = $val;
			} else {
				$val{checkresult_error} = sprintf(
					'特殊なファイル名は使えません。（%s）',
					$val,
				);
			}
			if ($val{targetfile}){
				if (-f $val{targetfile}){
					open (COMMAND, "$val{perlpath} -c $val{targetfile} 2>\&1 |")
						and $val{checkresult_checked} = join('', (<COMMAND>))
						or $val{checkresult_error} = sprintf(
							'文法チェックに失敗しました。（%s: %s）',
							$val{targetfile},
							$!
						);
					close (COMMAND);
				} else {
					$val{checkresult_error} = sprintf(
						'指定されたファイルはサーバ上にありません。（%s）',
						$val{targetfile},
					);
				}
			}
		} elsif ($key eq 'modulelist'){ #チェック対象モジュールの指定
			my $count = 0;
			push (@modules,
				map {s/-/::/g; $_}
				grep {/^[\w:-]+$/ and ++$count <= 10}
				split(/\r?\n/, $val)
			);
		}
	}
}

#文法チェックの結果をパース
if ($val{checkresult_checked}){
	$val{stdstr} = sprintf(
		'%s syntax OK',
		$val{targetfile},
	);
	$val{checkresult_checked} =~ m/^\s*$val{stdstr}\s*$/
		and $val{checkresult_error} = sprintf(
			'%s: エラーはありません。',
			$val{targetfile},
			)
		or $val{checkresult_error}  = sprintf(
			'%s: エラーがあります。',
			$val{targetfile},
			)
		;
}

$val{checkresult_checked} ||= ($val{checkresult_error} || '（文法チェックの結果はここに表示されます）');

#モジュールのチェック
for (my $i=0; $i<=$#modules; $i++){
	eval "use $modules[$i];";
	$modules_check[$i]->{name} = $modules[$i];
	$modules_check[$i]->{version} = eval "\$$modules[$i]::VERSION" || undef;
	if ($modules_check[$i]->{version}) {
		$modules_check[$i]->{version_str} = sprintf(
			'利用可能（Ver. %s）',
			$modules_check[$i]->{version},
		);
		if ($modules_check[$i]->{name} eq 'Jcode'){
			$val{if_jcode_pm_avail} = $modules_check[$i]->{name};
		}
	} else {
		$modules_check[$i]->{version_str} = '利用できません';
	}
}

#ライブラリのチェック
for (my $i=0; $i<=$#jclibs; $i++){
	eval "require './$jclibs[$i]';"
		and $val{if_jcode_pl_avail} = $jclibs[$i]
		and last;
}

#コマンドのチェック
for (my $i=0; $i<=$#smcommands; $i++){
	(-x $smcommands[$i])
		and $val{if_sendmail_avail} = $smcommands[$i]
		and last;
}

#表示調整
if ($val{if_jcode_pl_avail}){
	$val{jcodeinfo} = sprintf(
			q{jcode.pl が使えます。（require './%s';）},
			$val{if_jcode_pl_avail},
		);
}
if ($val{if_jcode_pm_avail}){
	$val{jcodeinfo} .= "\n" if $val{jcodeinfo};
	$val{jcodeinfo} .= sprintf(
			q{%s モジュールが使えます。（use %s;）},
			$val{if_jcode_pm_avail},
			$val{if_jcode_pm_avail},
		);
}
if ($val{if_sendmail_avail}){
	$val{sendmailinfo} = sprintf(
			q{%s が使えます。},
			$val{if_sendmail_avail},
		);
}

foreach (@modules_check){
	$val{modulelist} .= sprintf("<tr>
		<td nowrap>%s</td>
		<td nowrap>%s</td>
		</tr>\n",
		$_->{name},
		$_->{version_str}
	);
}

if ($val{if_owned_by_user}){ #SuExec等
$val{pmtn_list} = '
<tr>
<th colspan="2" class="subheader">CGIファイル</th>
<td class="pmtn">700</td>
<td class="pmtn">rwx------</td>
</tr>
<tr>
<th colspan="2" class="subheader">CGIファイルを置いているディレクトリ</th>
<td class="pmtn">755</td>
<td class="pmtn">rwxr-xr-x</td>
</tr>
<tr>
<th rowspan="2" class="subheader">書き込みファイル</th>
<th class="subheader"> ブラウザで見ない※2</th>
<td class="pmtn">600</td>
<td class="pmtn">rw-------</td>
</tr>
<tr>
<th class="subheader"> ブラウザで見る ※3</th>
<td class="pmtn">644</td>
<td class="pmtn">rw-r--r--</td>
</tr>
<tr>
<th rowspan="2" class="subheader">書き込みディレクトリ<br>
（中にファイルを作ったり<br>
削除したりする場合） </th>
<th class="subheader"> 中のファイルをブラウザで見ない ※2</th>
<td class="pmtn">700</td>
<td class="pmtn">rwx------</td>
</tr>
<tr>
<th class="subheader"> 中のファイルをブラウザで見る ※3</th>
<td class="pmtn">755</td>
<td class="pmtn">rwxr-xr-x</td>
</tr>
';
} else {
$val{pmtn_list} = '
<tr>
<th colspan="2" class="subheader">CGIファイル</th>
<td class="pmtn">755</td>
<td class="pmtn">rwxr-xr-x</td>
</tr>
<tr>
<th colspan="2" class="subheader">CGIファイルを置いているディレクトリ</th>
<td class="pmtn">755</td>
<td class="pmtn">rwxr-xr-x</td>
</tr>
<tr>
<th rowspan="2" class="subheader">書き込みファイル</th>
<th class="subheader"> ブラウザで見ない※2</th>
<td class="pmtn">646</td>
<td class="pmtn">rw-r--rw-</td>
</tr>
<tr>
<th class="subheader"> ブラウザで見る ※3</th>
<td class="pmtn">646</td>
<td class="pmtn">rw-r--rw-</td>
</tr>
<tr>
<th rowspan="2" class="subheader">書き込みディレクトリ<br>
（中にファイルを作ったり<br>
削除したりする場合） </th>
<th class="subheader"> 中のファイルをブラウザで見ない ※2</th>
<td class="pmtn">757</td>
<td class="pmtn">rwxr-xrwx</td>
</tr>
<tr>
<th class="subheader"> 中のファイルをブラウザで見る ※3</th>
<td class="pmtn">757</td>
<td class="pmtn">rwxr-xrwx</td>
</tr>
';
}

$val{template} = '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>すぐ使えるCGI Perl文法チェック&環境調査CGI</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<style type="text/css">
<!--
p, ol, ul, li {
	line-height: 150%;
}
h1 {
	margin: 0.5em 0px 0.5em 0px;
	padding: 0.3em 0.3em 0.3em 0.3em;
	background-color: #6699cc;
	color: #ffffff;
	font-size: 1.3em;
}
h2 {
	margin: 2em 0.5em 0.5em 0px;
	padding: 0.3em 0.3em 0.3em 0.3em;
	border-top: #336699 dashed 1px;
	border-bottom: #336699 dashed 1px;
	font-size: 1.2em;
}
h2.first {
	margin-top: 0.5em;
}
h3 {
	margin: 0.5em 0em 0.5em 0em;
	padding: 0.1em 0.1em 0.1em 0.1em;
	border-top: #999999 solid 1px;
	border-bottom: #999999 solid 1px;
	background-color: #dfdfdf;
	color: #333333;
	font-size: 1em;
}
table {
	margin: 8px 0px 8px 8px;
	border-collapse: collapse;
	border: 1px solid #999999;
	padding: 1px;
}
table th.header {
	background-color: #dfdfdf;
	padding: 3px;
	border: 1px solid #999999;
	text-align: left;
}
table th.subheader {
	padding: 3px;
	border: 1px solid #999999;
	text-align: left;
}
table td {
	padding: 3px;
	font-family: monospace;
}
table td.pmtn {
	text-align: center;
}
code {
	display: block;
	border: solid 1px #999999;
	padding: 8px;
	background-color: #333333;
	color: #ffffff;
	overflow: auto;
	margin: 10px;
}
.msg_info {
	font-size: 0.9em;
}
.msg_error {
	color: #ff0000;
}
-->
</style>
</head>

<body bgcolor="#FFFFFF" text="#000000">
<h1>すぐ使えるCGI Perl環境調査CGI</h1>
<h2 class="first">Perl 文法チェック</h2>
<ol>
<li>下の「チェック対象CGIファイル名」にチェックしたい Perl CGI のファイル名を入力して、「文法チェック」ボタンを押して下さい。</li>
<li>結果は、「文法チェック結果」欄に表示されます。</li>
</ol>
<form method="post" action="%_myname_%">
チェック対象CGIファイル名（例： target.cgi ）
<input type="text" name="targetfile" value="">
<input type="submit" value="文法チェック">
<h3>文法チェック結果 </h3>
<p class="msg_error">%_checkresult_error_%</p>
<code>%_checkresult_checked_%</code>
<h2>サーバ環境チェックの結果</h2>
<table border="1">
<tr>
<th class="header">OS</th>
<td>%_os_%</td>
</tr>
<tr>
<th class="header">Perl のパス</th>
<td>%_perlpath_%</td>
</tr>
<tr>
<th class="header">現在のディレクトリの絶対パス表記</th>
<td>%_currentdir_%</td>
</tr>
<tr>
<th class="header">Perl のバージョン</th>
<td>%_perlversion_%</td>
</tr>
<tr>
<th class="header">日本語文字コード関係</th>
<td>%_jcodeinfo_%</td>
</tr>
<tr>
<th class="header"> メールツール</th>
<td>%_sendmailinfo_%</td>
</tr>
<tr>
<th class="header">モジュール</th>
<td>
<table border="1">
%_modulelist_%
</table>
<p class="msg_info">※ 一部の標準モジュールは利用できる場合でも「利用できません」と表示される場合があります。</p>
</td>
</tr>
<tr>
<th class="header">その他のモジュール</th>
<td>1モジュール/1行でチェックしたいモジュールを記入して下さい。<br>
（10行まで。結果は上に表示されます。）<br>
<textarea name="modulelist" cols="20" rows="4"></textarea>
<input type="submit" value="モジュールチェック">
</td>
</tr>
</table>
<h2>CGI設定チェックの結果</h2>
<p class="msg_info">※このパートはUNIX系の環境のみ対応しています。</p>
<p>CGI はユーザ %_process_user_% の権限で実行されています。 </p>
<table border="1">
<thead>
<tr>
<th colspan="2" class="header">対象ファイル</th>
<th colspan="2" class="header">適したパーミッション ※1</th>
</tr>
</thead>
%_pmtn_list_%
</table>
<p>※1 これ以外のパターンもありえます。お使いのサーバのマニュアル等で指示があればそちらを優先して下さい。<br>
※2 管理者用のログファイルなど。FTPダウンロードのみの場合。 <br>
※3 画像や、ホームページの内容を更新したりする場合。 ブラウザからダウンロードする場合も含みます。</p>
</form>
<div>
<hr>
<a href="http://sugutsukaeru.jp/">すぐ使えるCGI</a> Perl文法チェック&環境調査CGI Ver. 1.0
</div>
</body>
</html>
';

foreach (qw(
	checkresult_error
	checkresult_checked
	os
	perlpath
	currentdir
	perlversion
	jcodeinfo
	sendmailinfo
	process_user
)){
	if ($val{$_}){
		$val{template} =~ s/%_${_}_%/&text2html($val{$_})/eg;
	} else {
		$val{template} =~ s/%_${_}_%//g;
	}
}

foreach (qw(
	myname
	modulelist
	pmtn_list
)){
	$val{template} =~ s/%_${_}_%/$val{$_}/g;
}

print "Content-Lenght: ".length($val{template})."\r\n";
print "\r\n";
print "$val{template}";

sub text4textarea($){
	my $string = shift;
	if ($string){
		$string =~ s/\&/\&amp;/g;
		$string =~ s/#/\&#35;/g;
		$string =~ s/</\&lt;/g;
		$string =~ s/>/\&gt;/g;
		$string =~ s/"/\&quot;/g;
		$string =~ s/'/\&#39;/g;
		$string =~ s/%/\&#37;/g;
	}
	return $string;
}

sub text2html($){
	my $string = &text4textarea(shift);
	($string) or return $string;

	$string =~ s/\t/\&nbsp;\&nbsp;\&nbsp;\&nbsp;/g;
	$string =~ s/ (?= )/\&nbsp;/g;
	$string =~ s/\&nbsp; /\&nbsp;\&nbsp;/g;

	my $br = '<br>';
	$string =~ s/\r?\n/$br/g;
	return $string;
}
