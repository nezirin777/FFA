sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$sake1 -= 999999;
		$ksex = int(rand(2));
		if ($ksex == 1) { $seibetu = "男"; }
		elsif ($ksex == 0) { $seibetu = "女"; }
		$com2 .= "<font class=\"red\" size=5>性転換！！！</font><font color =#cc6633 size = 2><br>性別がランダムに変化する！$seibetuになった！</font><br>";
	}
}
sub mons_atowaza{}
1;