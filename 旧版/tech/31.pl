sub hissatu{
	if ($waza_ritu > int(rand(80 + 40 * $ora))) {
		$item[1] = $item[1] * 2;
		$ora++;
		$com1 .="<font class=\"yellow\" size=5>古代魔法オーラ！！！（武器攻撃力２倍効果持続）</font><br>";
	}
}
sub atowaza{}
1;