sub acskouka{
	if (int(rand(5))==0) {
		$hpplus1 = $chara[9] * int(rand($chara[20]));
		$com1 .= "<font class=\"white\" size=5>$item[6]が光を放つ！！ケアルガの効果！！$chara[4] のＨＰが $hpplus1 回復した！♪</font><br>";
	}
}
1;