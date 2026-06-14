sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$dhit = int(rand(7)) + 1;
		$dmg1 = $dmg1 * $dhit;
		$com1 .= "<font class=\"yellow\" size=4>分身の術！！</font><font color=red>$dhit体の分身が一斉に攻撃！！</font><br>";
	}
}
sub atowaza{}
1;