sub wacskouka{
	if (int(rand(15))==0) {
		$hpplus2 = $winner[8] * int(rand($winner[13]));
		$com2 .= "<font class=\"yellow\" size=3>$winner[27]が光を放つ！！ケアルガの効果！！$winner[3] のＨＰが $hpplus2 回復した！♪</FONT><br>";
	}
}
1;