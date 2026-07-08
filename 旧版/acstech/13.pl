sub acskouka{
	if (int(rand(5))==0) {
		$sake2 -= 999999;
		$dmg1 += $chara[8] * int(rand(80));
		$com1 .= "<font class=\"red\" size=3>$item[6]が光を放つ！！メテオの効果！！</font><br>";
	}
}
1;