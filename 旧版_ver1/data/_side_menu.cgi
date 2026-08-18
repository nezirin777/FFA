#================================================
# サイドメニュー・ヘッダー・フッター Created by Merino
#================================================
sub side_menu {
	my($contents) = shift;

	my $yid = $ENV{'QUERY_STRING'} ? '?'.$ENV{'QUERY_STRING'} : '';
	my $title_line = $title_img ? qq|<img src="$title_img" alt="$title">| : $title;
	
	print <<"EOM";
<div align="center">
<div id="page">
	<div id="header">
		<table width="100%">
		<tr><td>
		<h1><a href="$script_index">$title_line</a></h1>
		</td><td align="right" valign="bottom">
		</td></tr></table>
	</div>
	<div id="navigation">
		<div class="menu_button"><a href="$script_index$yid">＠トップ<div class="text_small">トップページ</div></a></div>
		<div class="menu_button"><a href="https://discord.gg/ZkET3e">＠ディスコード<div class="text_small">VIPSTARのDiscordの招待URL</div></a></div>
		<div class="menu_button"><a href="http://oktavia.sakura.ne.jp/monsters/monster.cgi">＠MONSTER'S<div class="text_small">メダルを集めてVIPSを手にいれよう！</div></a></div>
		<div class="menu_button"><a href="http://oktavia.sakura.ne.jp/game/syounin/akimono/index.cgi">＠商人物語<div class="text_small">お金を稼いで目指せ億り人</div></a></div>
		<div class="menu_button"><a href="http://oktavia.sakura.ne.jp/party2/">＠パーティーII<div class="text_small">VIPPERたちと冒険に出よう！</div></a></div>
		<div class="menu_button"><a href="http://oktavia.sakura.ne.jp/ffa/">＠FFA<div class="text_small">手を下すまでもなくカオス</div></a></div>
		<div class="menu_button"><a href="http://w1.oroti.net/~houjo/br2/brlist.cgi">＠ばとるろわいやる<div class="text_small">（　＾ω＾）ちょっと今からみんなに殺し合いをしてもらうおｗｗｗｗ</div></a></div>
	</div>
	<div id="contents">
		$contents
	</div>
EOM
}


#================================================
# footer
#================================================
sub footer {
	print qq|<div id="footer">|;
	print qq|+ ＠パーティーII Ver$VERSION <a href="http://cgi-sweets.com/" target="_blank">CGI-Sweets</a> <a href="http://amaraku.net/" target="_blank">Ama楽.net</a>|; # 著作表示:削除・非表示 禁止!!
	print qq|$copyright +</div></div></div></body></html>|;
}

1;
