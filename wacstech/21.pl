sub wacskouka{
	if (int(rand(2))==0) {
		$sake1 -= 999999;
		$dmg2 += ($winner[7] + $winner[8]) * int(rand(500));
		$com2 .= "<font class=\"green\" size=3>$winner[27]が光を放つ！！時の狭間より古の魔神を呼び寄せた！！グランドクロス！！</FONT><br>";
	}
}
1;