sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		if (int(rand(1))==0) {
			$hpplus2 = int(rand($mrand)) * 2;
			$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
			$com2 = "<font class=\"yellow\" size=5>白魔法ケアルガ！！！</font><br>";
		} else {
			$sake1 -= 999999;
			$dmg2 += int(rand($mrand)) * 3;
			$dmg2 += $item[4];
			$com2 .= "<font class=\"white\" size=5>禁断の魔法アルテマを発動！！！</font><br>";
		}
	}
}
sub mons_atowaza{}
1;