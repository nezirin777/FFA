sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$dmg1 += ($chara[7] + $chara[8] + $chara[33]) * int(rand(50));
		$com1 .="<font class=\"red\" size=5>ファイガ剣！！！</font><br>";
	}
}
sub atowaza{}
1;