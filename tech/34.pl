sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$dmg1 += ($chara[7] + $chara[11] + $chara[12] + $chara[33]) * int(rand(80));
		$com1 .="<font class=\"white\">必殺技！！燕返し！！</font><br>";
	}
}
sub atowaza{}
1;