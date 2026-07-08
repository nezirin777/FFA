sub hissatu{
	if ($waza_ritu > int(rand(120))) {
		if (int(rand(3)) == 0) {
			$sake2 -= 999999;
			$dmg1 = $winner[16] + $mhp_flg;
			$com1 .="<font class=\"yellow\" size=5>時空魔法デジョン！！！</font><br>";
		} else {
			$com1 .="<font class=\"red\" size=5>時空魔法デジョン！！！失敗した。。</font><br>";
		}
	}
}
sub atowaza{}
1;