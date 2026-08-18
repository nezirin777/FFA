sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dhit = int(rand(15))+1;
		$dmg1 = ($chara[8] + $chara[33]) * int(rand(10));
		$dmg1 = $dmg1 * $dhit;
		$sake2 -= 999999;
		$com1 .="<font class=\"yellow\" size=5>黒魔法メテオ！！！</font><font class=small>$dhit連続ヒット！！</font><br>";
	}
}
sub atowaza{}
1;