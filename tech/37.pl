sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dhit = int(rand(7)) + 1;
		$dmg1 = $dmg1 * $dhit;
		$com1 .="<font class=\"yellow\" size=4>必殺技！！！無限乱武！！！</font><font class=small>$dhit連続ヒット！！</font><br>";
	}
}
sub atowaza{}
1;