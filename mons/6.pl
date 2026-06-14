sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$dmhit = int(rand(7))+1;
		$sake1 -= 999999;
		$dmg2 = int(rand($mrand)) * $dmhit;
		$dmg2 += $item[4];
		$com2 .= "<font class=\"red\" size=5>古代魔法メテオ！！！</font><font color=red>$dmhitヒット！！</font><br>";
	}
}
sub mons_atowaza{}
1;