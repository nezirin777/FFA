sub acskouka{
	if (int(rand(5))==0) {
		if ($khp_flg < $dmg2) {
			if ($a_23lmt >= 1) {
				$com1 .= "<font class=\"red\" size=3>$item[6]は光らなかった。。。</font><br>";
			} else {
				$a_23lmt++;
				$hpplus1 = $chara[16];
				$dmg2 = 0;
				$com1 .= "<font class=\"white\" size=5>$item[6]が光を放つ！！$chara[4]の傷が完全に回復した！！</font><br>";
			}
		}
	}
}
1;