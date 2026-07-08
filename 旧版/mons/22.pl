sub mons_waza{
	if ($mons_ritu > int(rand(100))) {
		if (int(rand(2))==0) {
			$charadown[7] = int(rand(3));
			$charadown[8] = int(rand(3));
			$charadown[9] = int(rand(3));
			$charadown[10] = int(rand(3));
			$charadown[11] = int(rand(3));
			$charadown[12] = int(rand(3));
			$charadown[13] = int(rand(3));
			$charadown[20] = int(rand(3));
			$chara[7] -= $charadown[7];
			$chara[8] -= $charadown[8];
			$chara[9] -= $charadown[9];
			$chara[10] -= $charadown[10];
			$chara[11] -= $charadown[11];
			$chara[12] -= $charadown[12];
			$chara[13] -= $charadown[13];
			$chara[20] -= $charadown[20];
			$sake1 -= 999999;
			$dmg2 += int(rand($mrand)) * 2;
			$com2 .= <<"EOM";
<font class=\"red\" size=5>臭い息！！！</font><br>
<font class =\"white\" size = 2>
力が<font class =\"yellow\">$charadown[7]</font>下がった。<br>
魔力が<font class =\"yellow\">$charadown[8]</font>下がった。<br>
信仰心が<font class =\"yellow\">$charadown[9]</font>下がった。<br>
生命力が<font class =\"yellow\">$charadown[10]</font>下がった。<br>
器用さが<font class =\"yellow\">$charadown[11]</font>下がった。<br>
速さが<font class =\"yellow\">$charadown[12]</font>下がった。<br>
魅力が<font class =\"yellow\">$charadown[13]</font>下がった。<br>
カルマが<font class =\"yellow\">$charadown[20]</font>下がった。
</font><br>
EOM
		} else {
			$dmg2 += int(rand($mrand)) * 10;
			$dmg2 += $item[4];
			$com2 .= "<font class=\"red\" size=5>臭い息！！！</font><br>";
		}
	}
}
sub mons_atowaza{}
1;