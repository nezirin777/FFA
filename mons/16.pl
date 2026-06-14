sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$dmg2 += int(rand($mrand)) * 7;
		$dmg2 += $item[4];
		$sake1 -= 999999;
		$com2 .= "<font class=\"white\" size=5>最強魔法アポガリプス！！！</font><br>";
	}
}
sub mons_atowaza{}
1;