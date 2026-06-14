sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dhit = int(rand(11))+1;
		$sake2 -= 999999;
		$dmg1 = ($chara[8] + $chara[9] + $chara[33]) * int(rand(100));
		$dmg1 = $dmg1 * $dhit;
		$com1 .="<font class=\"yellow\" size=4>幻獣ナイツ・オブ・ラウンドを召還！！</font><font color=red>$dhit人の騎士が力を貸した！！</font><br>";
	}
}
sub atowaza{}
1;