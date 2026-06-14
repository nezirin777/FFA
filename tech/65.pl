sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 = ($chara[8] + $chara[9]) * int(rand(100));
		$com1 .= "<font class=\"yellow\" size=5>禁断魔法アルテマ！！</font>";
		if ($waza_ritu > int(rand(80))) {
			$dmg1 += ($chara[9]) * int(rand(80));
			$com1 .= "<font class=\"white\" size=5>ホーリー！！</font>";
		}
		if ($waza_ritu > int(rand(80))) {
			$dmg1 += ($chara[8]) * int(rand(80));
			$com1 .="<font class=\"red\" size=5>フレア！！</font>";
		}
		if ($waza_ritu > int(rand(80))) {
			$dmg1 += ($chara[8]) * int(rand(100));
			$com1 .="<font class=\"red\" size=5>メテオ！！</font>";
		}
		$com1 .= "<br>\n";
		$sake2 -= 999999;
	}
}
sub atowaza{}
1;