sub whissatu{}
sub watowaza{
	if ($wwaza_ritu > int(rand(120))) {
	if (int(rand(4)) == 0) {
		$com2 .= "<font class=\"yellow\" size=4>幻獣カーバンクルを召還！！リフレク！！</FONT>$chara[4]には効かなかった！！<br>";
	}
else{
		$dmg2 += $dmg1;
		$dmg1 = 0;
		$com2 .= "<font class=\"yellow\" size=4>幻獣カーバンクルを召還！！リフレク！！（攻撃を反射）</FONT><br>";
	}
}}
1;