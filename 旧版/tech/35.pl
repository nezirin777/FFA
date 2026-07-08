sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		if (int(rand(5)) == 0) {
			$dmg1 = $mhp + $whp_flg;
			$com1 .="<font class=\"white\" size=6><i>斬・鉄・剣！！</i></font><br>";
		} else {
			$com1 .="<font class=\"white\"><i>斬・鉄・剣！！失敗！！</i></font><br>";
		}
	}
}
sub atowaza{}
1;