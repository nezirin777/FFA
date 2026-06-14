sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dhit = int(rand(15)) + 1;
		$dmg1 += ($chara[7] + $chara[12]) * int(rand(80));
		$dmg1 = $dmg1 * $dhit;
		$sake2 -= 999999;
		$com1 .= "<font class=\"white\" size=5>必殺技！！！エンド・オブ・ハート！！！</font><font class=small>$dhit連続ヒット！！</font><br>";
	}
}
sub atowaza{}
1;