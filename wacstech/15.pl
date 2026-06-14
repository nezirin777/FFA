sub wacskouka{
	if (int(rand(10))==0) {
		$com2 .= "<font class=\"dark\" size=3>$winner[27]が光を放つ！！デジョンの効果！！</FONT><br>";
		if (int(rand(3)) == 0) {
			$sake1 -= 999999;
			$dmg2 = $chara[16];
			$com2 .= "<font class=\"yellow\" size=5>時空魔法デジョン！！！</FONT><br>";
		} else {
			$com2 .= "<font class=\"red\" size=5>時空魔法デジョン！！！失敗した。。</FONT><br>";
		}
	}
}
1;