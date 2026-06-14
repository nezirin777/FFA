sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$dwhit = int(rand(15))+1;
		$dmg2 += ($winner[6] + $winner[11]) * int(rand(80));
		$dmg2 = $dmg2 * $dwhit;
		$sake1 -= 999999;
		$com2 .= "<font class=\"white\" size=5>必殺技！！！エンド・オブ・ハート！！！</font><font class=small>$dwhit連続ヒット！！</FONT><br>";
	}
}
sub watowaza{}
1;