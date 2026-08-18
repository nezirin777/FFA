sub acskouka{
	if (int(rand(2))==0) {
		$sake2 -= 999999;
		$dmg1 += ($chara[8] + $chara[9]) * int(rand(500));
		$com1 .= "<font class=\"green\" size=3>$item[6]が光を放つ！！時の狭間より古の魔神を呼び寄せた！！グランドクロス！！</font><br>";
	}
}
1;