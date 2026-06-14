sub hissatu{
	if ($waza_ritu > int(rand(80))) {
		$dmg1 += ($chara[7] + $chara[11] + $chara[12] + $chara[33]) * int(rand(80));
		$com1 .="<font class=\"yellow\" size=6>$chara[4]‚Í‘å‚«‚È‹C‚Ì‰ò‚ğ$mname $winner[3]‚É•ú‚Á‚½II</font><br>";
	}
}
sub atowaza{}
1;