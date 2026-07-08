sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$dmg1 = int($dmg1 * 0.1);
		$com2 .= "<font class=\"yellow\">防御魔法マイティガード！！！</font><br>";
	}
}
sub mons_atowaza{}
1;