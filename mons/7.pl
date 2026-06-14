sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$sake1 -= 999999;
		$dmg2 += int($khp_flg / 5);
		$com2 .= "<font class=\"red\" size=5>重力魔法グラビガを発動！！！</font><br>";
	}
}
sub mons_atowaza{}
1;