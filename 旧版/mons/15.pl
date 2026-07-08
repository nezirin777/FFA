sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$dmg2 += int(rand($mrand));
		$dmg2 += $item[4];
		$hpplus2 = $dmg2;
		$sake1 -= 999999;
		$com2 .= "<font classr=\"dark\" size=4>暗黒魔法ドレイン！！！</font><br>";
		$kaihuku2 .= "$mname のＨＰが $hpplus2 回復した！♪";
	}
}
sub mons_atowaza{}
1;