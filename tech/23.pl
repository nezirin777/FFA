sub hissatu{}
sub atowaza{
	if ($waza_ritu > int(rand(120))) {
		if ($mode eq 'isekai' or $mode eq 'boss') {
			$com1 .="<font class=\"yellow\" size=4>幻獣カーバンクルを召還！！リフレク！！</FONT>$mnameには効かなかった！！<br>";
		} else {
			$dmg1 += $dmg2;
			$dmg2 = 0;
			$com1 .="<font class=\"yellow\" size=4>幻獣カーバンクルを召還！！リフレク！！（攻撃を反射）</font><br>";
		}
	}
}
1;