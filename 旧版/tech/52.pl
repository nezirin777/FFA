sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$sake2 -= 999999;
		$dmg1 = ($chara[8] + $chara[9] + $chara[33]) * int(rand(200));
		$com1 .="<font class=\"red\" size=4>幻獣バハムートを召還！！メガフレア！！</font><br>";
	}
}
sub atowaza{}
1;