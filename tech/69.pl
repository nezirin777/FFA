sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$hpplus1 = ($chara[9] + $chara[10] + $chara[33]) + int(rand($chara[20]));
		$dmg1 = 0;
		$com1 .="<font class=\"white\" size=5>光・あれ！！！</font><br>";
		$kaihuku1 .= "$chara[4] のＨＰが $hpplus1 回復した！♪";
	}
}
sub atowaza{}
1;