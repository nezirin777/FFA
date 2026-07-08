sub hissatu{}
sub atowaza{
	if ($waza_ritu > int(rand(120))) {
		if ($mode eq 'isekai' or $mode eq 'boss') {
			$com1 .="<font class=\"yellow\" size=5>時空魔法ストップ！！！</FONT>$mnameには効かなかった！！<br>";
		} else {
			$sake2 -= 999999;
			$dmg2 = 0;
			$com1 .="<font class=\"yellow\" size=5>時空魔法ストップ！！！</font>$winner[3] $mnameの動きを止めた！<br>";
		}
	}
}
1;