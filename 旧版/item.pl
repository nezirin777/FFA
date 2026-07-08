#------------#
#　武器読込　#
#------------#
sub item_read {
	open(IN,"$item_file");
	@battle_item = <IN>;
	close(IN);

	$hit=0;
	foreach(@battle_item){
		($ci_no,$item[0],$item[1],$ci_gold,$item[2]) = split(/<>/);
		if($_[0] eq $ci_no) {$hit=1;last;}
	}
	if (!$hit) {
		$ci_no = 0;
		$item[0] = '素手';
		$item[1] = 0;
		$ci_gold = 0;
		$item[2] = 0;
	}
}

#------------#
#　防具読込　#
#------------#
sub def_read {
	open(IN,"$def_file");
	@battle_def = <IN>;
	close(IN);

	$hit=0;
	foreach(@battle_def){
		($cd_no,$item[3],$item[4],$cd_gold,$item[5]) = split(/<>/);
		if($_[0] eq $cd_no) {$hit=1;last;}
	}
	if (!$hit) {
		$cd_no = 0;
		$item[3] = '普段着';
		$item[4] = 0;
		$cd_gold = 0;
		$item[5] = 0;
	}
}

#--------------#
#　装飾品読込　#
#--------------#
sub acs_read {
	open(IN,"$acs_file");
	@log_acs = <IN>;
	close(IN);

	$hit=0;
	foreach(@log_acs){
		($a_no,$item[6],$a_gold,$item[7],$item[8],$item[9],$item[10],$item[11],$item[12],$item[13],$item[14],$item[15],$item[16],$item[17],$item[18],$item[19]) = split(/<>/);
		if($_[0] eq $a_no){$hit=1;last; }
	}
	if(!$hit) {
		$a_no = 0;
		$a_gold = 0;
		$item[6] = 'なし';
		$item[7] = 0;
		$item[8] = 0;
		$item[9] = 0;
		$item[10] = 0;
		$item[11] = 0;
		$item[12] = 0;
		$item[13] = 0;
		$item[14] = 0;
		$item[15] = 0;
		$item[16] = 0;
		$item[17] = 0;
		$item[18] = 0;
		$item[19] = '-';
	}
}

#----------------------------#
#　アイテムファイル書き込み　#
#----------------------------#
sub item_regist {

	$new_item = "";
	foreach(@item){
		$new_item .="$_<>";
	}
	open(OUT,">./item/$chara[0].cgi"); 
	print OUT $new_item; 
	close(OUT);

}

#----------------------#
#　武器ファイル初期化　#
#----------------------#
sub item_lose{
	$item[0] = '素手';
	$item[1] = 0;
	$item[2] = 0;
}

#----------------------#
#　防具ファイル初期化　#
#----------------------#
sub def_lose{
	$item[3] = '普段着';
	$item[4] = 0;
	$item[5] = 0;
}

#------------------------#
#　装飾品ファイル初期化　#
#------------------------#
sub acs_lose {
	$item[6] = 'なし';
	$item[7] = 0;
	$item[8] = 0;
	$item[9] = 0;
	$item[10] = 0;
	$item[11] = 0;
	$item[12] = 0;
	$item[13] = 0;
	$item[14] = 0;
	$item[15] = 0;
	$item[16] = 0;
	$item[17] = 0;
	$item[18] = 0;
	$item[19] = '-';
}

#------------------------------------#
# 便利なフッター(キャラデータ更新後) #
#------------------------------------#
sub shopfooter {
	print <<"EOM";
<hr>
<form action="$item_shop" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="武器屋へ">
</form>
<form action="$def_shop" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="防具屋へ">
</form>
<form action="$acs_shop" method="post">
<input type=hidden name=id value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="装飾品屋へ">
</form>
<form action="$script_souko" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="アイテム倉庫へ">
</form>
<form action="$script_bank" method="post">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type=submit class=btn value="銀行へ">
</form>
<form action="$script" method="post">
<input type=hidden name=id value=$chara[0]>
<input type="hidden" name="mydata" value="$new_chara">
<input type=hidden name=mode value=log_in>
<input type=submit class=btn value="ステータス画面へ">
</form>
EOM
}

1;