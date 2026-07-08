sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$dmg1+= (($chara[11]+$chara[33]) * int(rand(50)));
		$com1 .="<font class=\"yellow\" size=5>必殺技ライフ・デジョン！！！</font><br>";
		$hpplus1 = int($dmg1 / 5);
		$kaihuku1 .= "$chara[4] のＨＰが $hpplus1 回復した！♪<br>";
	}
}
sub atowaza{}
1;