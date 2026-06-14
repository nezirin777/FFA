sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$sake2 -= 999999;
		$dmg1 = ($chara[8] + $chara[9] + $chara[33]) * int(rand(200));
		$com1 .="<font class=\"blue\" size=4>幻獣リヴァイアサンを召還！！大海嘯！！</font><br>";
	}
}
sub atowaza{}
1;