sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 = 0;
		$hpplus1 = ($chara[9] + $chara[33]) + int(rand($chara[20]));
		$com1 .="<font class=\"white\" size=5>白魔法ケアルガ！！！</font><br>";
		$kaihuku1 .= "$chara[4] のＨＰが $hpplus1 回復した！♪";
	}
}
sub atowaza{}
1;