sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand))*3;
		$dmg2 += $item[4]*3;
		$com2 .= "<font class=\"red\" size=5>メガ・フレア！！！</font><br>";
	}
}
sub mons_atowaza{}
1;