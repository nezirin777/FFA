sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		if (int(rand(3))==0) {
			$sake1 -= 999999;
			$dmg2 = $khp_flg;
			$dmg2 += $item[4];
			$com2 .= "<font class=\"red\" size=5>時空魔法デジョンを発動！！！</font><br>";
		} else {
			$com2 .= "<font class=\"red\" size=5>時空魔法デジョンを発動！！！失敗！！</font><br>";
		}
	}
}
sub mons_atowaza{}
1;