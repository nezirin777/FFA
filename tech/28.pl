sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$sake2 -= 999999;
		$dmg1 = ($chara[8] + $chara[9] + $chara[33]) * int(rand(300));
		$com1 .="<font class=\"white\" size=5>神聖魔法ジハード！！！</font><br>";
	}
}
sub atowaza{}
1;