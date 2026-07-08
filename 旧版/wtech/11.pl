sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$dmg2 = $dmg2 + (($winner[10] + $winner[39]) * int(rand(50)));
		$com2 .= "<font class=\"yellow\" size=5>必殺技ライフ・デジョン！！！</FONT><br>";
		$hpplus2 = int($dmg2 /5);
		$kaihuku2 .= "$winner[3] のＨＰが $hpplus2 回復した！♪";
	}
}
sub watowaza{}
1;