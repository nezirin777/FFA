sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 += ($chara[7] + $chara[9] + $chara[33]) * int(rand(80));
		$com1 .= "<font class=\"white\" size=5>ホーリー剣！！！</font><br>";
	}
}
sub atowaza{}
1;