sub wacskouka{
	if (int(rand(30))==1) {
		if ($whp_flg < $dmg1) {
			if ($wa_22lmt >= 3) {
				$winner[51] == 0;
				$com2 .= "<font class=\"green\" size=3>$winner[27]は光らなかった。。。</FONT><br>";
			} else {
				$wa_22lmt++;
				$dmg2 += $dmg1;
				$dmg1 = 0;
				$com2 .= "<font class=\"white\" size=3>$winner[27]が光を放つ！！$chara[4]の攻撃を跳ね返した！！</FONT><br>";
			}
		}
	}
}
1;