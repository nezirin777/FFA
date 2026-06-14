sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$sake1 += 999;
		$sake2 -= 999999;
		$dmg1+= (($chara[7] + $chara[33]) * int(rand(60)));
		$com1 .="<font class=\"white\" size=5>ハイウインド！！</font><br>";
	}
}
sub atowaza{}
1;