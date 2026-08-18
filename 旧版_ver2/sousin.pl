#------------------#
#　メッセージ表示　#
#------------------#
	print "【送信したメッセージ】表\示数<b>$max_gyo</b>件まで";
	open(IN,"$sousin_file/$chara[0].cgi");
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
<small><b>$hnameさんへ</b>　＞ 「<b>$hmessage</b>」$htime\[$hhost\]</small>
</font>
</td>
EOM

		print <<"EOM";
</tr></table>
EOM
		$hit=1;$i++;
	}
	if(!$hit){
		print "<hr size=0><font color=$red>$chara[4]さんが送信したメッセージはありません</font>\n";
	}
	print "<hr size=0>";

1;