sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$hpplus1 = ($chara[13] + $chara[33]) + int(rand($chara[20]));
		$dmg1 = 0;
		$com1 .="<font class=\"white\" size=5>$chara[4]‚Í‰ñ•œ‚Ì‰Ì‚ğ‰Ì‚Á‚½ô</font><br>";
		$kaihuku1 .= "$chara[4] ‚Ì‚g‚o‚ª $hpplus1 ‰ñ•œ‚µ‚½Iô";
	}
}
sub atowaza{}
1;