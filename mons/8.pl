sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand)) * 2;
		$dmg2 += $item[4];
		$com2 .= "<font class=\"red\" size=5>黒魔法クエイクを発動！！！</font><br>";
	}
}
sub mons_atowaza{}
1;