sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$dmg2 = ($winner[7] + $winner[39]) * int(rand(20));
		$hpplus2 = $dmg2;
		$sake1 -= 999999;
		$com2 .= "<font color=\"#009999\" size=4>暗黒魔法ドレイン！！！</FONT><br>";
		$kaihuku2 .= "$winner[3] のＨＰが $hpplus2 回復した！♪";
	}
}
sub watowaza{}
1;