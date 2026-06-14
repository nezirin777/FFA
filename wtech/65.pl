sub whissatu{
	if ($wwaza_ritu > int(rand(120))) {
		$dmg2 = ($winner[7] + $winner[8]) * int(rand(100));
		$com2 .= "<font class=\"yellow\" size=5>禁断魔法アルテマ！！</font>";if ($wwaza_ritu > int(rand(80))) {
		$dmg2 += ($winner[8]) * int(rand(80));
		$com2 .= "<font class=\"white\" size=5>ホーリー！！</font>";
	}
if ($wwaza_ritu > int(rand(80))) {
		$dmg2 += ($winner[7]) * int(rand(80));
		$com2 .= "<font class=\"red\" size=5>フレア！！</font>";
	}
if ($wwaza_ritu > int(rand(80))) {
		$dmg2 += ($winner[7]) * int(rand(100));
		$com2 .= "<font class=\"red\" size=5>メテオ！！</font>";
	}
$sake1 -= 999999;
	}
}
sub watowaza{}
1;