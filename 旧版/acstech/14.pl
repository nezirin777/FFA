sub acskouka{
	if (int(rand(5))==0) {
		$sake2 -= 999999;
		$dmg1 += ($chara[8] + $chara[9]) * int(rand(100));
		$com1 .= "<font class=\"white\" size=3>$item[6]が光を放つ！！アルテマの効果！！</font><br>";
	}
}
1;