sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$sake2 -= 999999;
		$dmg1 = ($chara[8] + $chara[33]) * int(rand(100));
		$com1 .="<font class=\"red\" size=5>黒魔法フレア！！！</font><br>";
	}
}
sub atowaza{}
1;