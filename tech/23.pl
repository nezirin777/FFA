sub hissatu{}
sub atowaza{if($waza_ritu > int(rand(120))) {if($wsyoku > 16 or $mode eq 'isekai' or $mode eq 'boss'){$com1 .="<P><font class=\"yellow\" size=4>幻獣カーバンクルを召還！！リフレク！！</FONT>$wname $mnameには効かなかった！！<P/>";}else{$dmg1 += $dmg2;$dmg2 = 0;$com1 .="<P><font class=\"yellow\" size=4>幻獣カーバンクルを召還！！リフレク！！（攻撃を反射）</font></P>";}}}
1;