sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$sake2 -= 999999;
		$dmg1 = ($chara[8] + $chara[33]) * int(rand(100));
		$com1 .="<font class=\"red\" size=4>幻獣イフリートを召還！！地獄の火炎！！</font><br>";
	}
}
sub atowaza{}
1;