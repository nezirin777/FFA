sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		if (int(rand(1199)) == 0) {
		$sake1 -=999999;
		$dmg1 = 0;
		$dmg2 += int(rand($mrand)) ** 8; 
		$com2 = "<font class=\"red\" size =6>‚¦‚è‚è‚ñ‚ÌŠÃ‚¢‚³‚³‚â‚«I</font><br>";
		} else {
	$hpplus1 = int(rand($msp)) * 8;
		$kaihuku2 .= "$chara[4] ‚Ì‚g‚o‚ª $hpplus1 ‰ñ•œ‚µ‚½Iô";
		$dmg1 = 0;
		$dmg2 = 0;
		$com2 = "<font class=\"yellow\" size=5>j•Ÿ‚ÌƒLƒXôô</font><br>";
		}
	}
}
sub mons_atowaza{}
1;