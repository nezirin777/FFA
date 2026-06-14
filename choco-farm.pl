#------------------#
#　HTMLのフッター　#
#------------------#
sub choco_footer {
	
	# 著作権表示・改変厳禁
	print << "EOM";
<a href = "$scripto">$main_titleのTOPへ</a>
<HR SIZE=0 WIDTH="100%"><DIV align=right>
チョコボ牧場 edit by <a href="http://www.eriicu.com" target="_blank">いく</a><br>
FFA いく改ver2.00 edit by <a href="http://www.eriicu.com" target="_blank">いく</a><br>
FFA Emilia Ver1.01 remodeled by Classic(閉鎖)<br>
FF Battle De I v3.06 remodeling by <a href="http://www.mj-world.jp/" target="_blank">jun-k</a>(更新停止中)<br>
FF ADVENTURE(改) v1.040 remodeled by <a href="http://www.gun-online.com" target="_blank">ＧＵＮ</a><br>
FF ADVENTURE v0.43 edit by D.Takamiya(CUMRO) <a href="http://www5c.biglobe.ne.jp/~ma-ti/" target="_blank">現配布元(管理者ma-ti)</a><br>
</DIV></body></html>
EOM

}

#--------------------#
#　牧場チャンプ読込　#
#--------------------#
sub read_farm_winner {
	open(IN,"./farmwinner.cgi");
	@cwinner = <IN>;
	close(IN);

	($wcid,$wcpass,$wcbreader,$wcsite,$wcurl,$wcname,$wcno,$wctype,$wcrun,$wcwin,$wcmax,$wc0,$wc1,$wc2,$wc3,$wc4,$wc5,$wc6,$wcren,$wclname,$wclsite,$wclurl,$wclbreader) = split(/<>/,$cwinner[0]);
}

#----------------#
#　チョコボ読込　#
#----------------#
sub farm_choco_read {
	open(IN,"./chocolog/$chara[0].cgi");
	@choco_chara = <IN>;
	close(IN);

	($cid,$cpass,$cbreader,$cname,$csex,$cblood,$cno,$cmaxmax,$ctype,$cmax0,$cmax1,$cmax2,$cmax3,$cmax4,$cmax5,$cmax6,$clife,$ctrain,$crun,$cwin,$cmax,$c0,$c1,$c2,$c3,$c4,$c5,$c6,$cgold,$cfather,$cfblood,$cmother,$cmblood) = split(/<>/,$choco_chara[0]);

}

#----------------#
#　チョコボ読込　#
#----------------#
sub farm_choco_regist {

	@choco_new = "$cid<>$cpass<>$cbreader<>$cname<>$csex<>$cblood<>$cno<>$cmaxmax<>$ctype<>$cmax0<>$cmax1<>$cmax2<>$cmax3<>$cmax4<>$cmax5<>$cmax6<>$clife<>$ctrain<>$crun<>$cwin<>$cmax<>$c0<>$c1<>$c2<>$c3<>$c4<>$c5<>$c6<>$cgold<>$cfather<>$cfblood<>$cmother<>$cmblood<>";

	open(OUT,">./chocolog/$chara[0].cgi");
	print OUT @choco_new;
	close(OUT);

}

#--------------------#
#  レース用ヘッダー  #
#--------------------#
sub race_header {
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
<title>$main_title</title>
<script type="text/javascript">
<!--
var xPos1,xPos2,xPos3,xPos4,xPos5;
var turn = 0;
function move() {
	setTimeout("move1()", 5000);
}
$java_com
function finish() {
	document.all.comment3.innerHTML = "$next_com";
	document.all.comment2.innerHTML = "$comment<br>";
}
// -->
</script>
</head>
<body background="$backgif" bgcolor="$bgcolor" text="$text" link="$link" vlink="$vlink" alink="$alink" onload = "move()">
EOM
	if($midi_set){
		print "<embed src=\"$midi\" type=\"audio/midi\" height=\"2\" autostart=\"true\" repeat=\"true\" save=\"false\" volume=\"100\" width=\"2\">\n";
	}
}

1;