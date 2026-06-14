sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$sake2 -= 999999;
		$dmg1 =($chara[8] + $chara[9] + $chara[33]) * int(rand(160));
		$com1 .="<font class=\"white\" size=5>禁断魔法アルテマ！！！</font><br>";
	}
}
sub atowaza{}
1;