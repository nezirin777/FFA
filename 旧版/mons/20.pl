sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		if (int(rand(2))==0) {
			$sake1 -= 999999;
			$dmg2 = $khp_flg + $chara[16];
			$com2 .= "<font class=\"red\" size=5>斬・鉄・剣！！！</font><font color =#cc6633 size = 5><br>「私に斬れぬものなどない」</font><br>";
		} else {
			$dmg2 += int(rand($mrand)) * 10;
			$dmg2 += $item[4];
			$com2 .= "<font class=\"red\" size=5>斬・鉄・剣！！！</font><br>";
		}
	}
}
sub mons_atowaza{}
1;