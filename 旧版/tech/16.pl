sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$sake2 -= 999999;
		$winner[25] = 0;
		$dmg1 = ($chara[8] + $chara[33]) * int(rand(40));
		$com1 .="<font class=\"red\" size=5>赤魔法メルトン！！！（防御力無効）</font><br>";
	}
}
sub atowaza{}
1;