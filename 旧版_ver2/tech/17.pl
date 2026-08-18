sub hissatu{}
sub atowaza{
	if ($waza_ritu > int(rand(120))) {
		if ($mode eq 'isekai' or $mode eq 'boss') {
			$com2 .="<font class=\"red\" size=5>赤魔法ウオール！！！</FONT>$mnameには効かなかった！！<br>";
		} else {
			$sake1 += 999;
			$dmg2 = 0;
			$com1 .="<font class=\"white\" size=5>赤魔法ウオール！！！（全ての攻撃を無効）</font><br>";
		}
	}
}
1;