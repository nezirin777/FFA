sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$hpplus2 = int(rand($mhp)) * 2;
		$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
		$dmg2 = 0;
		$com2 = "<font class=\"yellow\" size=5>白魔法ケアルガ！！！</font><br>";
	}
}
sub mons_atowaza{}
1;