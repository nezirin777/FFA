sub acskouka{
	if (int(rand(5))==0) {
		$item[1] = $item[1] * 2;
		$com1 .= "<font class=\"white\" size=5>$item[6]が光を放つ！！オーラの効果！！！（武器攻撃力２倍効果持続）</font><br>";
	}
}
1;