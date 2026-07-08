#--------------#
#　関数初期化　#
#--------------#
sub shokika {
	$dmg1 = $chara[18] * (int(rand(3)) + 1);
	$dmg2 = $winner[17] * (int(rand(3)) + 1);
	$clit1 = "";
	$clit2 = "";
	$com1 = "";
	$com2 = "";
	$kawasi1 = "";
	$kawasi2 = "";
	$sake1 = 0;
	$sake2 = 0;
	$kclit = $khp_flg / 10;
	$wclit = $whp_flg / 10;
	$kmclit = $chara[16] / 10;
	$wmclit = $winner[16] / 10;
	$hpplus1 = 0;
	$hpplus2 = 0;
	$kaihuku1 = "";
	$kaihuku2 = "";
}

#------------#
#　HPの計算　#
#------------#
sub hp_sum {
	$khp_flg = $khp_flg - $dmg2 + $hpplus1;
	if ($khp_flg > $chara[16]) { $khp_flg = $chara[16]; }
	$whp_flg = $whp_flg - $dmg1 + $hpplus2;
	if ($whp_flg > $winner[16]) { $whp_flg = $winner[16]; }
}

#------------#
#　勝敗条件　#
#------------#
sub winlose {
	if ($whp_flg <= 0 and $khp_flg > 0) { $win = 1; last; }
	elsif ($khp_flg <= 0 and $whp_flg > 0) { $win = 0; last; }
	elsif ($khp_flg <= 0 and $whp_flg <= 0) { $win = 2; last; }
	else { $win = 3; }
}

#------------------#
#　チャンプの攻撃　#
#------------------#
sub winner_atack {

	# チャンプダメージ計算
	$com2 = "$winner[3]は、$winner[21]で攻撃！！<FONT COLOR=\"$yellow\">$battlecom[$winner[14]]</FONT><br>";

	$wattackpower="w"."$iryoku[$winner[14]]";
	&$wattackpower;

}

#------------------------#
#チャンプアクセサリー加算#
#------------------------#
sub wacs_add {
	$temp_winner[6] = $winner[6];
	$temp_winner[7] = $winner[7];
	$temp_winner[8] = $winner[8];
	$temp_winner[9] = $winner[9];
	$temp_winner[10] = $winner[10];
	$temp_winner[11] = $winner[11];
	$temp_winner[12] = $winner[12];
	$temp_winner[13] = $winner[13];
	$temp_winner[22] = $winner[22];
	$temp_winner[23] = $winner[23];
	$temp_winner[25] = $winner[25];
	$temp_winner[26] = $winner[26];
	$winner[6] += $winner[28];
	$winner[7] += $winner[29];
	$winner[8] += $winner[30];
	$winner[9] += $winner[31];
	$winner[10] += $winner[32];
	$winner[11] += $winner[33];
	$winner[12] += $winner[53];
	$winner[13] += $winner[34];
	if ($winner[37]) {
		require "./wtech/$winner[37].pl";
	} else {
		require "./wtech/0.pl";
	}
	if ($winner[51]) {
		require "./wacstech/$winner[51].pl";
	} else {
		require "./wacstech/0.pl";
	}
}

#------------------#
# チャンプ能力復元 #
#------------------#
sub wacs_sub {
	$winner[6] = $temp_winner[6];
	$winner[7] = $temp_winner[7];
	$winner[8] = $temp_winner[8];
	$winner[9] = $temp_winner[9];
	$winner[10] = $temp_winner[10];
	$winner[11] = $temp_winner[11];
	$winner[12] = $temp_winner[12];
	$winner[13] = $temp_winner[13];
	$winner[22] = $temp_winner[22];
	$winner[23] = $temp_winner[23];
	$winner[25] = $temp_winner[25];
	$winner[26] = $temp_winner[26];
}

#------------------#
#戦闘回避          #
#------------------#
sub battle_kaihi{

	#挑戦者命中率＆回避率
	$hit_ritu = int(($chara[11] / 10)+51);
	$kaihi_ritu = int(($chara[12] / 20));
	if ($kaihi_ritu > 50) {$kaihi_ritu = 50;}
	$hit_ritu += $item[2] + $item[16];
	$kaihi_ritu += $item[3] + $item[17];

	#相手命中率＆回避率
	$whit_ritu = int(($winner[10] / 10)+51);
	$wkaihi_ritu = int(($winner[11] / 20));
	if ($wkaihi_ritu > 50) {$wkaihi_ritu = 50;}
	$whit_ritu += $winner[52] + $winner[23];
	$wkaihi_ritu += $winner[35] + $winner[26];

	$sake1 += 100 - int($whit_ritu - $kaihi_ritu);
	$sake2 += 100 - int($hit_ritu - $wkaihi_ritu);

	if ($dmg2 < 0) {$dmg2 = $dmg2;}
	elsif ($dmg2 < $item[4]) {$dmg2 = 1;}
	else {$dmg2 = $dmg2 - $item[4];}

	if ($dmg1 < 0) {$dmg1 = $dmg1;}
	elsif ($dmg1 < $winner[25]) {$dmg1 = 1;}
	else {$dmg1 = $dmg1 - $winner[25];}

	#職業別防御ボーナス
	if($chara[14] > 17){$dmg2=int($dmg2/4);}
	elsif($chara[14] > 7){$dmg2=int($dmg2/2);}
	if($winner[14] > 17){$dmg1=int($dmg1/4);}
	elsif($winner[14] > 7){$dmg1=int($dmg1/2);}

	if ($whp_flg < $wmclit) {
		if ($whp_flg < $kclit) {
			if ($i > 15) {
				$dmg2 = $dmg2 * 10;
				$com2 .="<font color=$red size=5>残った力をふりしぼった！！</font><br>";
			}
		}
	} elsif (int($sake1) > int(rand(100))) {
		$dmg2 = 0;
		$kawasi1 = "<FONT SIZE=4 class=\"red\">$chara[4]は身をかわした！</FONT><br>";
	}

	if ($khp_flg < $kmclit) {
		if ($khp_flg < $wclit) {
			if ($i > 15) {
				$dmg1 = $dmg1 * 10;
				$com1 .="<font color=$red size=5>残った力をふりしぼった！！</font><br>";
			}
		}
	} elsif(int($sake2) > int(rand(100))) {
		$dmg1 = 0;
		$kawasi2 = "<FONT SIZE=4 class=\"red\">$winner[3]は身をかわした！</FONT><br>";
	}

}

#------------------------#
#チャンプアクセサリー効果#
#------------------------#
sub wacs_waza {
	&watowaza;
	&wacskouka;
}

#------------------#
#　チャンプの必殺技#
#------------------#
sub winwaza {

	# クリティカル率・戦術率算出
	$wwaza_ritu = int(($winner[13] / 15)) + 10 + $winner[39];
	if ($wwaza_ritu > 75) { $wwaza_ritu = 75; }
	$wwaza_ritu += $winner[36];
	if ($wwaza_ritu > 95) { $wwaza_ritu = 95; }

	# ＨＰが１／１０時に必殺率＋１００％
	if (int($wmaxhp / 10) > $whp_flg && int(rand(4)) > 1) {
		$wwaza_ritu +=999;
		$com2 .="<font class=\"red\" size=4>LIMIT BREAK!!</FONT><br>";
	}

	# 封印球の効果
	if ($item[7] == 19 and $winner[51] != 24 and $winner[51] != 19) {
		if ($winner[14] > 16) {
			$com1 .="<font class=\"red\" size=3>$item[7]が光を放つ！！$winner[3]には効かなかった！！</FONT><br>";
		} elsif ($winner[14] > 7) {
			if (int(rand(5)) == 0) {
				$wwaza_ritu = 0;
				$com1 .="<font class=\"yellow\" size=3>$item[7]が光を放つ！！$winner[3]の必殺技を封じ込めた！！</FONT><br>";
			}
		} else {
			if(int(rand(2)) == 0){
				$winner[51] =0;
				$wwaza_ritu = 0;
				$com1 .="<font class=\"yellow\" size=3>$item[7]が光を放つ！！$winner[3]の必殺技を封じ込めた！！</FONT><br>";
			}
		}
	}

	&whissatu;
}

#--------------------------#
# チャンプ職業別攻撃力付加 #
#--------------------------#
sub wsyokuzero{
	$dmg2 += int(rand($winner[6])) + $winner[22];
}
sub wsyokuone{
	$dmg2 += int(rand($winner[7])) + $winner[22];
}
sub wsyokutwo{
	$dmg2 += int(rand($winner[8])) + $winner[22];
}
sub wsyokuthree{
	$dmg2 += int(rand($winner[10])) + $winner[22];
}
sub wsyokufour{
	$dmg2 += int(rand($winner[7])) + $winner[22];
}
sub wsyokufive{
	$dmg2 += int(rand($winner[7])) + $winner[22];
}
sub wsyokusix{
	$dmg2 += int(rand($winner[8])) + int(rand($winner[12])) + $winner[22];
}
sub wsyokuseven{
	$dmg2 += int(rand($winner[7])) + int(rand($winner[12])) + $winner[22];
}
sub wsyokueight{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[10])) + $winner[22];
}
sub wsyokunine{
	$dmg2 += int(rand($winner[7])) + int(rand($winner[8])) + $winner[22];
}
sub wsyokuten{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[8])) + $winner[22];
}
sub wsyokueleven{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + $winner[22];
}
sub wsyokutwelve{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[9])) + $winner[22];
}
sub wsyokuthirteen{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[10])) + $winner[22];
}
sub wsyokufourteen{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + $winner[22];
}
sub wsyokufifteen{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + $winner[22];
}
sub wsyokusixteen{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[10])) + $winner[22];
}
sub wsyokuseventeen{
	$dmg2 += int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[12])) + $winner[22];
}
sub wsyokueighteen{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]) + $winner[22];
}
sub wsyokunineteen{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]) + $winner[22];
}
sub wsyokutwenty{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]) + $winner[22];
}
sub wsyokutwentyone{
	$dmg2 += int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]) + $winner[22];
}
sub wsyokutwentytwo{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13])) * 2) + $winner[22];
}
sub wsyokutwentythree{
	$dmg2 += int(rand($winner[6])) + $winner[22];
}
sub wsyokutwentyfour{
	$dmg2 += ((int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13])) * 2) + $winner[22];
}
sub wsyokutwentyfive{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int((rand($winner[10]))*5) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13])) * 2) + $winner[22];
}
sub wsyokutwentysix{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13])) * 2) + $winner[22];
}
sub wsyokutwentyseven{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13])) * 2) + $winner[22];
}
sub wsyokutwentyeight{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]))) + $winner[22];
}
sub wsyokutwentynine{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]))) + $winner[22];
}
sub wsyokuthirty{
	$dmg2 += ((int(rand($winner[6])) + int(rand($winner[7])) + int(rand($winner[8])) + int(rand($winner[9])) + int(rand($winner[10])) + int(rand($winner[11])) + int(rand($winner[12])) + int($winner[13]))) + $winner[22];
}#チャンプ攻撃力計算ここまで

#------------------#
#　戦闘状況        #
#------------------#
sub battle_sts {

	# 能力値バーの詳しい幅設定
	$hit_ritu = int(($chara[11] / 10) + 51);
	if($hit_ritu > 150){$hit_ritu = 150;}
	$kaihi_ritu = int(($chara[12]/ 20));
	if($kaihi_ritu > 50){$kaihi_ritu = 50;}
	$waza_ritu = int(($chara[20] / 15)) + 10 + $chara[33];
	if($waza_ritu > 75){$waza_ritu = 75;}
	$ci_plus = $item[2] + $item[16];
	$cd_plus = $item[5] + $item[17];
	$bwhit   = int(0.5 * ($hit_ritu + $ci_plus));
	$bwkaihi = int(0.5 * ($kaihi_ritu + $cd_plus));
	$bwwaza  = int(1 * ($waza_ritu + $item[18]));
	if($bwhit > 200){$bwhit = 200;}
	if($bwkaihi > 200){$bwkaihi = 200;}
	if($bwwaza > 200){$bwwaza = 200;}

	# 能力値バーの詳しい幅設定
	$whit_ritu = int(($winner[10] / 10) + 51);
	if($whit_ritu > 150){$whit_ritu = 150;}
	$wkaihi_ritu = int(($winner[11] / 20));
	if($wkaihi_ritu > 50){$wkaihi_ritu = 50;}
	$wwaza_ritu = int(($winner[13] / 15)) + 10 + $winner[39];
	if($wwaza_ritu > 75){$wwaza_ritu = 75;}
	$wi_plus = $winner[23] + $winner[52];
	$wd_plus = $winner[26] + $winner[35];
	$bwwhit   = int(0.5 * ($whit_ritu + $wi_plus));
	$bwwkaihi = int(0.5 * ($wkaihi_ritu + $wd_plus));
	$bwwwaza  = int(1 * ($wwaza_ritu + $winner[36]));
	if($bwwhit > 200){$bwwhit = 200;}
	if($bwwkaihi > 200){$bwwkaihi = 200;}
	if($bwwwaza > 200){$bwwwaza = 200;}

	if($i == 1){
		$battle_date[$j] = <<"EOM";
<TABLE>
<TR>
	<TD COLSPAN="3" ALIGN="center">
	$iターン
	</TD>
</TR>
<TR>
	<TD ALIGN="center">
	<IMG SRC="$img_path/$chara_img[$chara[6]]"><table width="100%">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$item[0]</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$item[3]</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$item[6]</td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwhit height=$bh><br><b>$hit_ritu + $ci_plus%</b></td></tr>
<tr><td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwkaihi height=$bh><br><b>$kaihi_ritu + $cd_plus%</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwaza height=$bh><br><b>$waza_ritu + $item[18]%</b></td></tr>
</table>
	</TD>
	<TD>
	</TD>
	<TD ALIGN="center">
	<IMG SRC="$img_path/$chara_img[$winner[5]]"><table width="100%">
<tr><td id="td2" class="b2">武器</td><td align="right" class="b2">$winner[21]</td></tr>
<tr><td id="td2" class="b2">防具</td><td align="right" class="b2">$winner[24]</td></tr>
<tr><td id="td2" class="b2">アクセサリー</td><td align="right" class="b2">$winner[27]</td></tr>
<tr><td id="td2" class="b2">命中率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwhit height=$bh><br><b>$whit_ritu + $wi_plus%</b></td></tr>
<tr><td id="td2" class="b2">回避率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwkaihi height=$bh><br><b>$wkaihi_ritu + $wd_plus%</b></td></tr>
<tr><td id="td2" class="b2">必殺率</td><td align="left" class="b2"><img src=\"$bar\" width=$bwwwaza height=$bh><br><b>$wwaza_ritu + $winner[36]%</b></td></tr>
</table></TD>
	</TR>
<TR>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
	<TD CLASS="b1" id="td2">
	職業
	</TD>
	<TD CLASS="b1" id="td2">
	LV
	</TD>
</TR>
<TR>
	<TD class="b2">
	$chara[4]
	</TD>
	<TD class="b2">
	$khp_flg\/$chara[16]
	</TD>
	<TD class="b2">
	$chara_syoku[$chara[14]]
	</TD>
	<TD class="b2">
	$chara[18]
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT class=red size=5>VS</FONT>
</TD>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
	<TD CLASS="b1" id="td2">
	職業
	</TD>
	<TD CLASS="b1" id="td2">
	LV
	</TD>
</TR>
<TR>
	<TD class="b2">
	$winner[3]
	</TD>
	<TD class="b2">
	$whp_flg\/$winner[16]
	</TD>
	<TD class="b2">
	$chara_syoku[$winner[14]]
	</TD>
	<TD class="b2">
	$winner[17]
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
$com1 $clit1 $kawasi2 $winner[3] に <font class=yellow>$dmg1</font> のダメージを与えた。<font class=yellow>$kaihuku1</FONT><br><br>
$com2 $clit2 $kawasi1 $chara[4] に <font class=red>$dmg2</font> のダメージを与えた。<font class=yellow>$kaihuku2</FONT><br><br>
EOM
	}else{

		$battle_date[$j] = <<"EOM";
<TABLE>
<TR>
	<TD COLSPAN="3" ALIGN="center">
	$iターン
	</TD>
</TR>
<TR>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
</TR>
<TR>
	<TD class="b2">
	$chara[4]
	</TD>
	<TD class="b2">
	$khp_flg\/$chara[16]
	</TD>
</TR>
</TABLE>
</TD>
<TD>
<FONT class=red size=5>VS</FONT>
</TD>
<TD>
<TABLE>
<TR>
	<TD CLASS="b1" id="td2">
	なまえ
	</TD>
	<TD CLASS="b1" id="td2">
	HP
	</TD>
</TR>
<TR>
	<TD class="b2">
	$winner[3]
	</TD>
	<TD class="b2">
	$whp_flg\/$winner[16]
	</TD>
</TR>
</TABLE>
</TD>
</TR>
</TABLE>
$com1 $clit1 $kawasi2 $winner[3] に <font class=yellow>$dmg1</font> のダメージを与えた。<font class=yellow>$kaihuku1</FONT><br><br>
$com2 $clit2 $kawasi1 $chara[4] に <font class=red>$dmg2</font> のダメージを与えた。<font class=yellow>$kaihuku2</FONT><br><br>
EOM
	}

}

#------------------#
#戦闘クリィティカル#
#------------------#
sub battle_clt {
	#クリティカル率算出
	$kclt_ritu = 100 - int($khp_flg / $chara[16] * 100);
	$wclt_ritu = 100 - int($whp_flg / $winner[16] * 100);

	if($mode eq 'battle'){
		if($i == 1){
			if(($winner[17] - $chara[18] >= $level_sa) or $item[1] < $winner[22]){
				$com1 .= "<font color=$blue size=5>逆転必殺技発動！！</font>$winner[3]の防具が一時的に効果無効！！<br>";
				$dmg1 = $dmg1 * $gyakuten;
				$sake2 = int(0)-999999;
				$winner[22] = 0;
			}
		}
	}

	if($kclt_ritu > int(rand(100))) {
		$clit1 = "<font color=$red size=5>クリティカル！！「<b>$chara[23]</b>」</FONT><br>";
		$dmg1 = $dmg1 * 2;
		$dmg1 += $winner[22];
	}

	if($mode eq 'battle'){
		if($i == 1){
			if(($chara[18] - $winner[17] >= $level_sa) or $winner[22] < $item[4]){
				$com2 .= "<font color=$red size=5>逆転必殺技発動！！</font>$chara[4]の防具が一時的に効果無効！！<br>";
				$dmg2 = $dmg2 * 100;
				$sake1 -= 999999;
				$cd_dmg = 0;
			}
		}
	}

	if($wclt_ritu > int(rand(100))) {
		$clit2 = "<font color=$red size=5>クリティカル！！「<b>$winner[20]</b>」</FONT><br>";
		$dmg2 = $dmg2 * 2;
		$dmg2 += $item[4];
	}
}

#------------------#
#戦闘結果判定      #
#------------------#
sub sentoukeka{
	if ($win == 1) {
		$chara[21] += 1;
		$chara[22] += 1;
		$exp = int($winner[17] * $kiso_exp);
		$winner[50] = int($winner[44] * $chara[17] * $syoukin);
		$comment = "<b><font size=5>$chara[4]は、戦闘に勝利した！！</font></b><br>";
	} elsif($win == 2) {
		$win = 1;
		$chara[21] += 1;
		$exp = int($winner[17] * $kiso_exp);
		$chara[15] = 1;
		$winner[15] = 1;
		$winner[50] = int($winner[44] * $chara[17] * $syoukin);
		$comment = "<b><font size=5>$chara[4]は、$winner[3]と相打ちした！！</font></b><br>";
	} elsif($win == 3) {
		$chara[21] += 1;
		$exp = int($winner[17] * $kiso_exp);
		$gold = 0;
		$winner[50] += int($winner[44] * $chara[17] * $syoukin);
		$comment = "<b><font size=5>$chara[4]は、$wnameと勝負が決まらなかった。。。</font></b><br>";
	} else {
		$chara[21] += 1;
		$exp = $winner[17];
		$gold = 0;
		$chara[19] = int(($chara[19] / 2));
		$winner[50] += int($winner[44] * $chara[17] * $syoukin);
		$comment = "<b><font size=5>$chara[4]は、戦闘に負けた・・・。</font></b><br>";
		$chara[28] = $boss;
	}
		$chara[17] = $chara[17] + $exp;
		$chara[27] = time();
}
1;