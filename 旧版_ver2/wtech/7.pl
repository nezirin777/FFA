sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$dmg2 = 0;
		$hpplus2 = ($winner[8] + $winner[39]) * int(rand($winner[13]));if ($hpplus2 > $winner[16]/10) {
		$hpplus2 = $winner[16]/10;
	}
$com2 .= "<br><font class=\"yellow\" size=3>白魔法ケアルガ！！！</FONT><br>";
		$kaihuku2 .= "$winner[3] のＨＰが $hpplus2 回復した！♪";
	}
}
sub watowaza{}
1;