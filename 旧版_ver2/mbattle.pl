#--------------#
#　関数初期化　#
#--------------#
sub shokika {
	$dmg1 = $chara[18] * (int(rand(5)) + 1);
	$dmg2 = $mdmg + int(rand($mrand));
	$clit1 = "";
	$clit2 = "";
	$sake1 = 0;
	$sake2 = 0;
	$com1 = "";
	$com2 = "$mnameが襲いかかった！！";
	$kawasi1 = "";
	$kawasi2 = "";
	$hpplus1 = 0;
	$hpplus2 = 0;
	$kaihuku1 = "";
	$kaihuku2 = "";
	$huin = 0;
}

#------------#
#　HPの計算　#
#------------#
sub hp_sum {
	$khp_flg = $khp_flg - $dmg2 - $dmgme1 + $hpplus1;
	if ($khp_flg > $chara[16]) {
		$khp_flg = $chara[16];
	}
	$mhp = $mhp - $dmg1 + $hpplus2;
	if ($mhp > $mhp_flg) {
		$mhp = $mhp_flg;
	}
}

#------------#
#　勝敗条件　#
#------------#
sub winlose {
	if ($mhp <= 0) { $win = 1; last; }
	elsif ($khp_flg <= 0) { $win = 0; last; }
	else{ $win = 2; }
}

#------------------#
#魔物クリィティカル#
#------------------#
sub mons_clt{
	#クリティカル率算出
	$kclt_ritu = 100 - int($khp_flg / $chara[16] * 100);
	$mclt_ritu = 100 - int($mhp / $mhp_flg * 100);

	# 封印球の効果
	if ($item[7] == 19) {
		if ($mode eq 'boss' or $mode eq 'isekiai') {
	$com1 .= "<font class=\"red\" size=3>$item[6]が光を放つ！！$mnameには効かなかった！！</font><br>";
		} else {
			if (int(rand(2))==0) {
				$huin =1;
				$com1 .= "<font class=\"yellow\" size=3>$item[6]が光を放つ！！$mnameの必殺技を封じ込めた！！</font><br>";
			}
		}
	}

	if ($kclt_ritu > int(rand(100))) {
		$com1 .= "<font color=\"$red\" size=5>クリティカル！！「$chara[23]」</font><br>";
		$dmg1 = $dmg1 * 3;
	}
	if ($mclt_ritu > int(rand(200))) {
		$com2 .= "<font color=\"$red\">クリティカル！！</font><br>";
		$dmg2 = $dmg2 + $item[4];
	}
}

#------------------#
#魔物回避          #
#------------------#
sub mons_kaihi{

	#回避率計算
	$ci_plus = $item[2] + $item[16];
	$cd_plus = $item[5] + $item[17];
	$hit_ritu = int(($chara[11] / 10)+51) + $ci_plus;	

	$sake1 += int(($chara[12] / 20)) + $cd_plus;
	$sake2 += $mkahi - $hit_ritu;

	if ($dmg2 < 0) { $dmg2 = $dmg2; }
	elsif ($dmg2 < $item[4]) { $dmg2 = 0; }
	else{ $dmg2 = $dmg2 - $item[4]; }

	#職業別防御ボーナス
	if ($chara[14] > 17) { $dmg2 = int($dmg2 / 4); }
	elsif ($ksyoku > 7) { $dmg2 = int($dmg2 / 2); }

	if (int($sake1) > int(rand(300))) {
		$dmg2 = 0;
		$kawasi1 = "<FONT SIZE=4 COLOR=\"$red\">$chara[4]は身をかわした！</FONT>";
	}
	if (int($sake2) > int(rand(100))) {
		$dmg1 = 0;
		$kawasi2 = "<FONT SIZE=4 COLOR=\"$red\">$mnameは身をかわした！</FONT>";
	}

}

#------------------#
#　戦闘状況      　#
#------------------#
sub monsbattle_sts {

	# 能力値バーの詳しい幅設定
	$hit_ritu = int(($chara[11] / 10) + 51);
	if ($hit_ritu > 150) { $hit_ritu = 150; }
	$kaihi_ritu = int(($chara[12]/ 20));
	if ($kaihi_ritu > 50) {	$kaihi_ritu = 50; }
	$waza_ritu = int(($chara[20] / 15)) + 10 + $chara[33];
	if ($waza_ritu > 75) { $waza_ritu = 75; }
	$ci_plus = $item[2] + $a_hitup;
	$cd_plus = $item[5] + $a_kaihiup;
	$bwhit   = int(0.5 * ($hit_ritu + $ci_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $cd_plus));
	$bwwaza  = int(1 * ($waza_ritu + $item[18]));
	if ($bwhit > 200) { $bwhit = 200; }
	if ($bwkaihi > 200) { $bwkaihi = 200; }
	if ($bwwaza > 200) { $bwwaza = 200; }

	if ($i == 1) {
		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0>
<TR>
	<TD COLSPAN= "3" ALIGN= "center">
	$iターン
	</TD>
</TR>
<TR>
	<TD ALIGN= "center">
	<IMG SRC= "$img_path/$chara_img[$chara[6]]"><table width= "100%">
<tr><td id= "td2" class= "b2">武器</td><td align= "right" class= "b2">$item[0]</td></tr>
<tr><td id= "td2" class= "b2">防具</td><td align= "right" class= "b2">$item[3]</td></tr>
<tr><td id= "td2" class= "b2">アクセサリー</td><td align= "right" class= "b2">$item[6]</td></tr>
<tr><td id= "td2" class= "b2">命中率</td><td align= "left" class= "b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $ci_plus%</b></td></tr>
<tr><td id= "td2" class= "b2">回避率</td><td align= "left" class= "b2"><img src=\"$bar\" width=$bwkaihi height=$bh><br><b>$kaihi_ritu + $cd_plus%</b></td></tr>
<tr><td id= "td2" class= "b2">必殺率</td><td align= "left" class= "b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $item[18]%</b></td></tr>
</table>
	</TD>
	</TR>
<TR>
<TD>
<TABLE>
<TR>
	<TD CLASS= "b1" id= "td2">
	なまえ
	</TD>
	<TD CLASS= "b1" id= "td2">
	HP
	</TD>
	<TD CLASS= "b1" id= "td2">
	職業
	</TD>
	<TD CLASS= "b1" id= "td2">
	LV
	</TD>
</TR>
<TR>
	<TD class= "b2">
	$chara[4]
	</TD>
	<TD class= "b2">
	$khp_flg\/$chara[16]
	</TD>
	<TD class= "b2">
	$chara_syoku[$chara[14]]
	</TD>
	<TD class= "b2">
	$chara[18]
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT SIZE=5 COLOR= "#9999DD">VS</FONT>
</TD>
<TD>
<TABLE>
<TR>
	<TD CLASS= "b1" id= "td2">
	なまえ
	</TD>
	<TD CLASS= "b1" id= "td2">
	HP
	</TD>
</TR>
<TR>
	<TD class= "b2">
	$mname
	</TD>
	<TD class= "b2">
	$mhp/$mhp_flg
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
$com1 $clit1 $kawasi2 $mname に <font class= "yellow">$dmg1</font> のダメージを与えた。<font class= "yellow">$kaihuku1</font><br><br><br>
$com2 $clit2 $kawasi1 $chara[4] に <font class= "red">$dmg2</font> のダメージを与えた。<font class= "yellow">$kaihuku2</font><br><br><br>
EOM
	} else {
		$battle_date[$j] = <<"EOM";
<TABLE BORDER=0>
<TR>
	<TD COLSPAN= "3" ALIGN= "center">
	$iターン
	</TD>
</TR>
<TR>
<TD>
<TABLE>
<TR>
	<TD CLASS= "b1" id= "td2">
	なまえ
	</TD>
	<TD CLASS= "b1" id= "td2">
	HP
	</TD>
</TR>
<TR>
	<TD class= "b2">
	$chara[4]
	</TD>
	<TD class= "b2">
	$khp_flg\/$chara[16]
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT SIZE=5 COLOR= "#9999DD">VS</FONT>
</TD>
<TD>
<TABLE>
<TR>
	<TD CLASS= "b1" id= "td2">
	なまえ
	</TD>
	<TD CLASS= "b1" id= "td2">
	HP
	</TD>
</TR>
<TR>
	<TD class= "b2">
	$mname
	</TD>
	<TD class= "b2">
	$mhp/$mhp_flg
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
$com1 $clit1 $kawasi2 $mname に <font class= "yellow">$dmg1</font> のダメージを与えた。<font class= "yellow">$kaihuku1</font><br><br><br>
$com2 $clit2 $kawasi1 $chara[4] に <font class= "red">$dmg2</font> のダメージを与えた。<font class= "yellow">$kaihuku2</font><br><br><br>
EOM
}
}

#------------------#
#戦闘結果判定      #
#------------------#
sub sentoukeka{
	if ($win==1) {
		$chara[22] += 1;
		$gold = $mgold + int(rand($mgold)+1);
		$chara[19] += $gold;
		if ($chara[19] > $gold_max) {
			$chara[19] = $gold_max;
		}
		elsif ($chara[19] < 0) {
			$chara[19] = 0;
		}
 		$comment = "<b><font size=5>$chara[4]は、戦闘に勝利した！！</font></b><br>";
	} elsif ($win==2) {
		$mex = int($mex/2);
		$comment = "<b><font size=5>$chara[4]は、逃げ出した・・・♪</font></b><br>";
	} else {
		$mex = 1;
		$chara[19] = int(($chara[19] / 100));
		$comment = "<b><font size=5>$chara[4]は、戦闘に負けた・・・。</font></b><br>";
	}
		$chara[17] = $chara[17] + $mex;
		$chara[21] ++;
		$chara[25] --;
		$chara[27] = time();
		$chara[28] = $boss;
}

#------------------#
#戦闘結果判定      #
#------------------#
sub legend_sentoukeka{
	if ($win==1) {
		$chara[22] += 1;
		$gold = $mgold + int(rand($mgold)+1);
		$chara[19] += $gold;
		if ($chara[19] > $gold_max) {
			$chara[19] = $gold_max;
		}
		elsif ($chara[19] < 0) {
			$chara[19] = 0;
		}
		$chara[28] -= 1;
		if ($chara[28] == 0) {
			$comment = "<b><font color=yellow size=5>$chara[4]は、レジェンドプレイスを攻略した！！新しい称号が与えられます！！</font></b><br>";
			&all_message("$chara[4]さんが新たにレジェンドプレイスを攻略され、称号が上がりました！");
			if ($chara[32] < $in{'boss_file'} + 1) {
				$chara[32] = $in{'boss_file'} + 1;
			}
		} else {
			$comment = "<b><font size=5>$chara[4]は、戦闘に勝利した！！ＨＰが少し回復した♪</font></b><br>";
		}
	} elsif ($win==2) {
		$mex = int($mex/2);
		$chara[28] = $boss;
		$comment = "<b><font size=5>$chara[4]は、逃げ出した・・・♪</font></b><br>";
	} else {
		$mex = 1;
		$chara[28] = $boss;
		$chara[19] = int(($chara[19] / 100));
		$comment = "<b><font size=5>$chara[4]は、戦闘に負けた・・・。</font></b><br>";
	}
		$chara[17] = $chara[17] + $mex;
		$chara[21] ++;
		$chara[25] --;
		$chara[27] = time();
}

#--------------#
# 時間チェック #
#--------------#
sub time_check{
	$ltime = time();
	$ltime = $ltime - $chara[27];
	$vtime = $m_time - $ltime;

	if ($vtime > 0) {
		&error("あと$vtime秒間闘えません。");
	}
}

#----------------------#
# モンスデータ呼び出し #
#----------------------#
sub mons_read{

	($mname,$mex,$mrand,$msp,$mdmg,$mkahi,$monstac,$mons_ritu,$mgold) = split(/<>/,$MONSTER[$r_no]);

	if ($monstac) {
		require "./mons/$monstac.pl";
	} else {
		require "./mons/0.pl";
	}

}

#------------------#
# 戦闘後のＨＰ処理 #
#------------------#
sub hp_after{
	$chara[15] = $khp_flg + int(rand($chara[10]));
	if ($chara[15] > $chara[16]) { $chara[15] = $chara[16]; }
	if ($chara[15] <= 0) { $chara[15] = $chara[16]; }
}

#----------------------#
# 戦闘後のフッター処理 #
#----------------------#
sub mons_footer{
	if ($win) {
		print "$comment $chara[4]は、$mexの経験値を手に入れた。<b>$gold</b>G手に入れた。<br>\n";
	} else {
		print "$comment $chara[4]は、$mexの経験値を手に入れた。お金が100分の1になった・・・(涙)<br>\n";
	}

	print <<"EOM";
<form action="$script" method="POST">
<input type="hidden" name="mode" value="log_in">
<input type="hidden" name="id" value="$chara[0]">
<input type="hidden" name="mydata" value="$new_chara">
<input type="submit" class="btn" value="ステータス画面へ">
</form>
EOM
}
1;