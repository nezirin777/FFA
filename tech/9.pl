sub hissatu{}
sub atowaza{
	if ($waza_ritu > int(rand(80))) {
		if ($mode eq 'isekai' or $mode eq 'boss' && int(rand(4)) == 1) {
			$com1 .= "$chara[4]が叫んだ！<font size=5>「あ！あれはなんだ！？？？？」</font>$winner[3] $mnameには効かなかった！！<br>";
		} else {
			$sake2 -= 999999;
			$dmg2 = 0;
			$com1 .="$chara[4]が叫んだ！<font size=5>「あ！あれはなんだ！？？？？」</font>$winner[3] $mnameに隙ができた！<br>";
		}
	}
}
1;