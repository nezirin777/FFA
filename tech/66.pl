sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 =($chara[7] + $chara[8] + $chara[9] + $chara[10] + $chara[11] + $chara[12] + $chara[13] + $chara[20] + $chara[33]) * int(rand(800));
		$sake2 -= 999999;
		$com1 .="<font class=\"white\" size=5>最強魔法アポガリプス！！！</font><br>";
	}
}
sub atowaza{}
1;