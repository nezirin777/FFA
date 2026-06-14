sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 += ($chara[7] + $chara[8] + $chara[9] + $chara[33]) * int(rand(160));
		$com1 .="<font class=\"yellow\" size=5>アルテマ剣！！！</font><br>";
	}
}
sub atowaza{}
1;