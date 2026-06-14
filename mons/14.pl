sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		$tgold = int(rand($chara[19] /7));
		$gold -= $tgold;
		$com2 .= "<font class=\"red\">お金を盗まれた！！$tgoldＧマイナス！！</font><br>";
	}
}
sub mons_atowaza{}
1;