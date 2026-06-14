sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dhit = int(rand(7)) + 1;
		$dmg1 += ($chara[7] + $chara[33]) * int(rand(10));
		$dmg1 = $dmg1 * $dhit;
		$sake2 -= 999999;
		$com1 .="<font class=\"white\" size=5>必殺技！！！超究武神覇斬！！！</font><font class=small>$dhit連続ヒット！！</font><br>";
	}
}
sub atowaza{}
1;