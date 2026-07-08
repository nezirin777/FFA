#----------------#
#  参加者登録    #
#----------------#
sub guest_list{

	$lock_file = "$lockfolder/sanka$in{'id'}.lock";
	&lock($lock_file,'SK');
	open(GUEST,"$guestfile");
	@guest=<GUEST>;
	close(GUEST);

	$now_time =time();

	$num = 1;
	$blist = '';
	@new_member = ();
	$sanka_hit = 0;
	foreach (@guest) {
		($ntimer,$nname,$nid) = split(/<>/);
			if ($ntimer + $sanka_time > $now_time && $nid ne $chara[0]) {
				$blist .= "<a href=\"$scripta?mode=chara_sts&id=$nid\">$nname</a><font size=\"1\" color=\"#ffff00\">★</font>";
				push(@new_member,"$ntimer<>$nname<>$nid<>\n");
				$num++;
			}
	}

	$blist .= "<a href=\"$scripta?mode=chara_sts&id=$chara[0]\">$chara[4]</a><font size=\"1\" color=\"#ffff00\">★</font>";
	push(@new_member,"$now_time<>$chara[4]<>$chara[0]<>\n");

	open(GUEST,">$guestfile");
	print GUEST @new_member;
	close(GUEST);
	$lock_file = "$lockfolder/sanka$in{'id'}.lock";
	&unlock($lock_file,'SK');

}

#----------------#
#  参加者表示    #
#----------------#
sub guest_view {

	print "<font size=2 color=#aaaaff>現在の冒険者(<B>$num人</B>)：</font>\n";

	if ($blist) {
		print $blist;
	}
	else {
		print '誰もいません';
	}
}

1;
