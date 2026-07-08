sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 += ($chara[7] + $chara[9] + $chara[33]) * int(rand(180));
		$com1 .="<font class=\"white\">必殺技！！ホーリースラッシュ！！</font><br>";
	}
}
sub atowaza{}
1;