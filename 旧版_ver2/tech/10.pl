sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		$temp_gold =  int(rand($gold)) + 1;
		$com1 .="<font class=\"yellow\">‚¨‹à‚ğ“‚ñ‚¾ô‡Œv$temp_gold‚fƒQƒbƒgô</font><br>";
		$gold += $temp_gold;
	}
}
sub atowaza{}
1;