sub wacskouka{
	if ($item[7] == 19) {
		if (int(rand(5))==0) {
			$dmg2 = $dmg2 * 10;
			$sake1 -= 999999;
			$com2 .= "<font class=\"green\" size=3>$winner[27]が光を放つ！！$item[6]に封じ込めれれた力を解放！！</FONT><br>";
		}
	}
}
1;