sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1 += ($chara[8] + $chara[33]) * int(rand(360));
		$hpplus1 = int($dmg1 / 10);
		$com1 .= "<font class=\"dark\" size=4>必殺技！！ダーク・イリュージョン！！！</font><br>";
		$kaihuku1 .= "$kname のＨＰが $hpplus1 回復した！♪";
	}
}
sub atowaza{}
1;