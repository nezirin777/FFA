sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		if (int(rand(3)) == 0) {
			$dmg1 = int($mhp / 3) + int($whp_flg / 3);
			$com1 .="<font class=\"blue\" size=4>幻獣ディアボロスを召還！！グラビガ！！</font><br>";
		}
	}
}
sub atowaza{}
1;