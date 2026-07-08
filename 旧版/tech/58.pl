sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 += ($chara[7] + $chara[33]) * int(rand(320));
		$com1 .= "<font class=\"yellow\" size=5>必殺技！！ブラスティングゾーン！！</font><br>";
	}
}
sub atowaza{}
1;