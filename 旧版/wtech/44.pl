sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$dmg2 += ($winner[7] + $winner[39]) * int(rand(360));
		$hpplus2 = int($dmg2 / 10);
		$com2 .= "<font color=\"#009999\" size=4>必殺技！！ダーク・イリュージョン！！！</FONT><br>";
		$kaihuku2 .= "$winner[3] のＨＰが $hpplus2 回復した！♪";
	}
}
sub watowaza{}
1;