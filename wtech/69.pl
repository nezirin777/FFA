sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$hpplus2 = ($winner[8] + $winner[9] + $winner[39]) + int(rand($winner[13]));
		$dmg2 = 0;
		$com2 .= "<font class=\"white\" size=5>光・あれ！！！</font><br>";
		$kaihuku2 .= "$winner[3] のＨＰが $hpplus2 回復した！♪";
	}
}
sub watowaza{}
1;