sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$dmg1 += ($chara[7] + $chara[33]) * int(rand(160));
		$com1 .= "<font class=\"yellow\" size=5>必殺技！！ラブディバイド！！</font><br>";
	}
}
sub atowaza{}
1;