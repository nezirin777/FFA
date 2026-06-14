package hostkick_elmo;

#-----------------------------------------------------------------------------#
#  既存掲示板補強用 特定ホスト排除スクリプト Version 2.01
#  Script written by 脱走犬エルモ(elmo@to.21.fm)
#
#  ■ このスクリプトは自由に改造して構いません。
#  ■ このスクリプトは、あくまで今使っている掲示板の補助用です。
#     単体では動きません。
#  ■ スクリプトに書かれた著作権表示だけは消さないで下さい。お願いします。
#  ■ Perl以外で書かれた掲示板cgiではこのスクリプトは利用出来ません。（多分..）
#  ■ 質問等は下記でお願いいたします。
#     http://www4.tkcity.net/~elmo/
#-----------------------------------------------------------------------------#

#--------初期設定--------#

# アクセスを禁止するホスト名（いくつでも可）
@kickhost = ('anonymizer');

# プロクシー経由のアクセスを制限
#	0：制限なし
#	1：生IPを漏らすプロクシー経由のみ許可
#	2：1の制限＋プロクシー経由の疑いがあるホストを制限
#	3：2の制限＋jpドメインとIPアドレス（ホスト名が逆引き出来ないホスト）以外は制限
$proxy_kick = 0;

# 上記プロクシー経由のアクセス制限時、特別に許可するホスト
@allowproxy = ('cj3065496-a.stama1.kt.home.ne.jp','M110037.ppp.dion.ne.jp','gwymg01.c-able.ne.jp','N078112.ppp.dion.ne.jp','22.pool0.ipctokyo.att.ne.jp','valley.tv-naruto.ne.jp','cna.ne.jp','dhcp24035.oct-net.ne.jp','Ctyhs1DS33.aic.mesh.ad.jp','ws2.osaka-ue.ac.jp','61.202.73','N073069.ppp.dion.ne.jp','nthrsm012151.adsl.ppp.infoweb.ne.jp','ntthygo09244.ppp.infoweb.ne.jp','kyto043n206.ppp.infoweb.ne.jp ');

# 表示画面のBODYの設定
$body = '<body bgcolor=#ffffff text=#000000>';

#------------------------#
$addr = $ENV{'REMOTE_ADDR'};
$host = $ENV{'REMOTE_HOST'}; unless ($host) { $host = $addr; }
if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

foreach (@kickhost) { if($host =~ /$_/i || $addr =~ /$_/i){ &kick("アクセス出来ません"); } }

if ($proxy_kick){

$hua		= $ENV{'HTTP_USER_AGENT'};
$cache_c	= $ENV{'HTTP_CACHE_CONTROL'};
$cache_i	= $ENV{'HTTP_CACHE_INFO'};
$cli_ip		= $ENV{'HTTP_CLIENT_IP'};
$ht_con		= $ENV{'HTTP_CONNECTION'};
$foward		= $ENV{'HTTP_FORWARDED'};
$ht_from	= $ENV{'HTTP_FROM'};
$pro_con	= $ENV{'HTTP_PROXY_CONNECTION'};
$sp_host	= $ENV{'HTTP_SP_HOST'};
$via		= $ENV{'HTTP_VIA'};
$xfoward	= $ENV{'HTTP_X_FORWARDED_FOR'};
$ht_xon		= $ENV{'HTTP_XONNECTION'};
$xro_con	= $ENV{'HTTP_XROXY_CONNECTION'};

if ($cli_ip =~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) { $letout_ip = $cli_ip; }
elsif ($cli_ip =~ /([\dA-F]{2})([\dA-F]{2})([\dA-F]{2})([\dA-F]{2})/i){
$cli_ip = join('.', hex($1), hex($2), hex($3), hex($4)); 
$letout_ip = $cli_ip;}
if ($foward =~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) { $letout_ip = $foward; }
if ($ht_from =~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) { $letout_ip = $ht_from; }
if ($sp_host =~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) { $letout_ip = $sp_host; }
if ($via =~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) { $letout_ip = $via; }
if ($xfoward =~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) { $letout_ip = $xfoward; }

if ($letout_ip eq '' && $cache_c) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $cache_i) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $pro_con) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $foward) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $ht_xon) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $hua =~/cache|delegate|proxy|squid|via/i) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $via) { $letout_ip = "(proxy)"; }
if ($letout_ip eq '' && $xro_con) { $letout_ip = "(proxy)"; }

$host_head = (split(/\./,$host))[0];
if ($letout_ip eq '' && $host =~ /cache|^cgi|delegate|^dns|^firewall|^ftp|^fw|keeper|^mail|^ns\d{0,2}\.|^news|proxy|squid|^web|^www/i) { $letout_ip = "(proxy)"; }
elsif ($letout_ip eq '' && $host_head !~ /\d{2,}/) { $letout_ip = "(maybe proxy)"; }
if ($letout_ip eq '' && $ht_con !~ /Keep-Alive/i) { $letout_ip = "(maybe proxy)"; }


	$p_flag = 0;
	if ($proxy_kick == 1 && $letout_ip eq "(proxy)")
		{ $p_flag = 1; }
	elsif ($proxy_kick == 2 && ($letout_ip eq "(proxy)" || $letout_ip eq "(maybe proxy)"))
		{ $p_flag = 1; }
	elsif ($proxy_kick == 3){
		if ($host =~ /\.jp/i || $host =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/)
			{ $p_flag = 0; }
		if ($letout_ip eq "(proxy)" || $letout_ip eq "(maybe proxy)")
			{ $p_flag = 1; }
				}

	foreach(@allowproxy)
		{ if($host =~ /$_/i || $addr =~ /$_/i){ $p_flag = 0; } }

if ($p_flag)
	{ &kick("あなたがお使いのホスト( $host )からのアクセスは許可されていません。<br>掲示板管理者に該当ホストの許可を申\し出て下さい。"); }

}


sub kick {
	print "Content-type: text/html\n\n";
	print <<"HYOJI";
<html><head>
<meta http-equiv="Content-type" content="text/html; charset=x-sjis">
</head>$body
<h2>Sorry....</h2>
<p>$_[0]</p><hr>
<p align="right"><font size="-1">Script written by <a href="http://www4.tkcity.net/~elmo/" target="_top">脱走犬エルモ</a></font></p>
</body></html>
HYOJI

exit;
}

1;
