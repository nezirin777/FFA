sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$sake1 -= 999999;
		$dmg2 += int(rand($mrand)) * 5;
		$dmg2 += $item[4];
		$com2 .= "<font class=\"blue\" size=5>青魔法ショック・ウェーブ・パルサーを発動！！！</font><br>";
	}
}
sub mons_atowaza{}
1;