
#--- [注意事項] ----------------------------------------------------------------------------------------#
# 著作権は放棄していませんので、この参加者表示ライブラリのみを使う場合は				#
# フッター部分に											#
#  print "参加者\表\示 edit by <a href=\"http://www2.to/meeting/\" target=\"_top\">ＧＵＮ</a><br>\n";	#
# と記述して下さい       										#
#    直接メールによる質問は一切お受けいたしておりません。						#
#-------------------------------------------------------------------------------------------------------#
#----------------#
#  参加者登録    #
#----------------#
sub guest_list{

	&get_host;

	open(IN,"./charalog/$in{'id'}.cgi");
	@SANKA = <IN>;
	close(IN);

	$hit = 0;
	foreach(@SANKA){
		($jid,$jpass,$jsite,$jurl,$jname,$jsex,$jchara,$jn_0,$jn_1,$jn_2,$jn_3,$jn_4,$jn_5,$jn_6,$jsyoku,$jhp,$jmaxhp,$jex,$jlv,$jgold,$jlp,$jtotal,$jkati,$jwaza,$jitem,$jmons,$jhost,$jdate,$jmori,$jdef,$jtac,$jacsno,$jmoriturn,$jcllv) = split(/<>/);
		if($in{'id'} eq "$jid" and $in{'pass'} eq "$jpass") {
			$hit=1; last;
		}
	}

if($hit){

open(GUEST,"$guestfile");
@guest=<GUEST>;
close(GUEST);
$flag=1;
$times = time;
undef(@member);
foreach $line (@guest) {
($timer,$name,$id,$host) = split(/ \, /, $line);
if( $times-65 > $timer){
$line = '';
next;
}
if((($jname eq "$name")&&($id eq $jid)) && $flag){
$line = "$times \, $jname \, $jid \, $jhost \, \n";
$flag = 0;
}
if($jname eq "$name"){
push (@member, "<a href=\"$scripta?mode=chara_sts&id=$jid\">$jname</a><font size=1 color=#aaaaff>★</font>");
}
}
if($flag){
push(@guest,"$times \, $jname \, $jid \, $jhost \, \n");
if($name ne $jname){
push(@member, "<a href=\"$scripta?mode=chara_sts&id=$jid\">$jname</a><font size=1 color=#aaaaff>★</font>"); 
       }
}
	
open(GUEST,">$guestfile");
print GUEST @guest;
close(GUEST);
}

}

1;

#----------------#
#  参加者表示    #
#----------------#

sub guest_view {
	open(GUEST,"$guestfile");
	@member=<GUEST>;
	close(GUEST);

	$num = @member;

	print "<font size=2 color=#aaaaff>現在の冒険者(<B>$num人</B>)：</font>\n";

	foreach $line (@member) {
	($ntimer,$nname,$nid,$nhost) = split(/ \, /, $line);

	if(!@member){@member = '辺りには誰もいません・・・'; $num = 0;}
	print "<a href=\"$scripta?mode=chara_sts&id=$nid\">$nname</a><font size=1 color=#ffff00>★</font>";
	}
}

1;
