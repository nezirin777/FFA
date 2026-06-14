sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dhit = int(rand(7))+1;
		$dmg1 = $dmg1 * $dhit;
		$com1 .= "乱れ撃ち！！<font class=small>$dhit連続ヒット！！</font><br>";
	}
}
sub atowaza{}
1;