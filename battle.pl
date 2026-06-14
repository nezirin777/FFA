@iryoku=('syokuzero','syokuone','syokutwo','syokuthree','syokufour','syokufive','syokusix','syokuseven','syokueight','syokunine','syokuten','syokueleven','syokutwelve','syokuthirteen','syokufourteen','syokufifteen','syokusixteen','syokuseventeen','syokueighteen','syokunineteen','syokutwenty','syokutwentyone','syokutwentytwo','syokutwentythree','syokutwentyfour','syokutwentyfive','syokutwentysix','syokutwentyseven','syokutwentyeight','syokutwentynine','syokuthirty','syokuthirtyone','syokuthirtytwo','syokuthirtythree','syokuthirtyfour','syokuthirtyfive','syokuthirtysix','syokuthirtyseven','syokuthirtyeight','syokuthirtynine','syokufourty');
#------------------#
#　挑戦者の攻撃  　#
#------------------#
sub tyousensya {
	# 挑戦者ダメージ計算
	if($kitem){ $com1 = "<p>$knameは、$ci_nameで攻撃！！<FONT COLOR=\"$yellow\">$battlecom[$ksyoku]</FONT></p>"; }
	else{ $com1 = "<p>$knameは、素手で攻撃！！ </p>";}

$attackpower=$iryoku[$ksyoku];
&$attackpower;

}
#------------------#
#　挑戦者の必殺技　#
#------------------#
sub tyosenwaza {

	#機種判定
	$agent = $ENV{'HTTP_USER_AGENT'};
	($browser,$version,$model) = split(/\//,$agent);
	if ($browser eq "DoCoMo") {$com1="";}

	# クリティカル
	$waza_ritu = int(($klp / 15)) + 10 + $kcllv;
	if($waza_ritu > 75){$waza_ritu = 75;}
	$waza_ritu += $a_wazaup;
	if($waza_ritu > 95){$waza_ritu = 95;}
	if($mode eq 'isekiai' or $mode eq 'genei'){$waza_ritu = int($waza_ritu/3);}
	elsif($mode eq 'boss'){$waza_ritu = int($waza_ritu/2);}
	#ＨＰが１／１０時に必殺率＋１００％
	if(int($kmaxhp / 10) > $khp_flg && int(rand(4))>1){
		$waza_ritu +=999;
		$com1 .="<P><font class=\"red\" size=4>LIMIT BREAK!!</font></P>";
		}

	# 封印球の効果
	if($wa_kouka == 19 and $a_kouka != 24 and $a_kouka != 19){
		if($ksyoku > 16 or $mode eq 'boss' or $mode eq 'isekiai'){$com2 .="<P><font color=\"$red\">$wa_nameが光を放つ！！$kname には効かなかった！！</font></P>";}
		elsif($ksyoku > 7){if(int(rand(5))==0){$waza_ritu = 0;$com2 .="<P><font color=\"$yellow\">$wa_nameが光を放つ！！$kname の必殺技を封じ込めた！！</font></P>";}}
		else{if(int(rand(2))==0){$a_kouka =0;$waza_ritu = 0;$com2 .="<P><font color=\"$yellow\">$wa_nameが光を放つ！！$kname の必殺技を封じ込めた！！</font></P>";}}
	}

	if($ktac){&hissatu;}
}
#------------------#
#　レベルアップ  　#
#------------------#
sub levelup {
	if($klv < $charamaxlv){
	#職業別ボーナス加算処理
	open(IN,"$syoku_file");
	@syoku = <IN>;
	close(IN);
	my ($a,$b,$c,$d,$e,$f,$g,$h,$k0,$k1,$k2,$k3,$k4,$k5,$k6,$k7,$k8,$k9,$k10,$k11,$k12,$k13,$k14,$k15,$k16,$k17,$k18,$k19,$k20,$k21,$k22,$k23,$k24,$k25,$k26,$k27,$k28,$k29,$k30,$sy_0,$sy_1,$sy_2,$sy_3,$sy_4,$sy_5,$sy_6,$sylp) = split(/<>/,$syoku[$ksyoku]);
$as0=0;$as1=0;$as2=0;$as3=0;$as4=0;$as5=0;$as6=0;$as7=0;$ahp=0;
$t1=0;$t2=0;$t3=0;$t4=0;$t5=0;$t6=0;$t7=0;$t8=0;$hit=0;
	while($kex >= ($klv * $lv_up)){
	$kex = $kex - int($klv*$lv_up);
	$lvup+=1;
	$klv+=1;
	$hpup = int((rand($kn_3)) * 3 + $kn_3);
	$k0up = int(rand($sy_0)) + 1;
	$k1up = int(rand($sy_1)) + 1;
	$k2up = int(rand($sy_2)) + 1;
	$k3up = int(rand($sy_3)) + 1;
	$k4up = int(rand($sy_4)) + 1;
	$k5up = int(rand($sy_5)) + 1;
	$k6up = int(rand($sy_6)) + 1;
	$klpup = int(rand($sylp)) + 1;
	$kmaxhp = $kmaxhp + $hpup;
		if($kmaxhp < $charamaxhp){$ahp+=$hpup;$hit=1;}else{$ahp+=$charamaxhp-$kmaxhp+$hpup;$kmaxhp = $charamaxhp;}
	if(int(rand(2)) == 0) { $kn_0 += $k0up;
		if($kn_0 < $charamaxpm){$t1=1;$as0 += $k0up;}else{$as0+=$charamaxpm-$kn_0+$k0up;$kn_0 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $kn_1 += $k1up;
		if($kn_1 < $charamaxpm){$t2=1;$as1 += $k1up;}else{$as1+=$charamaxpm-$kn_1+$k1up;$kn_1 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $kn_2 += $k2up;
		if($kn_2 < $charamaxpm){$t3=1;$as2 += $k2up;}else{$as2+=$charamaxpm-$kn_2+$k2up;$kn_2 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $kn_3 += $k3up;
		if($kn_3 < $charamaxpm){$t4=1;$as3 += $k3up;}else{$as3+=$charamaxpm-$kn_3+$k3up;$kn_3 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $kn_4 += $k4up;
		if($kn_4 < $charamaxpm){$t5=1;$as4 += $k4up;}else{$as4+=$charamaxpm-$kn_4+$k4up;$kn_4 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $kn_5 += $k5up;
		if($kn_5 < $charamaxpm){$t6=1;$as5 += $k5up;}else{$as5+=$charamaxpm-$kn_5+$k5up;$kn_5 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $kn_6 += $k6up;
		if($kn_6 < $charamaxpm){$t7=1;$as6 += $k6up;}else{$as6+=$charamaxpm-$kn_6+$k6up;$kn_6 = $charamaxpm;}}
	if(int(rand(2)) == 0) { $klp  += $klpup;
		if($klp  < $charamaxpm){$t8=1;$as7 += $klpup;}else{$as7+=$charamaxpm-$klp+$klpup;$klp  = $charamaxpm;}}

}
if ($lvup != 0){
$comment .= "<p><font class=red size=7>レベルが$lvup上がった！</font><p/>";
$klvbf = $kcllv;
$kcllv += $lvup;
		#ジョブマスターの処理
		if($kcllv > 59 && $klvbf <=59){$comment .= "<font class=red size=5>$chara_syoku[$ksyoku]をマスターした！！新しい必殺技を覚えた！！</font></P>";}
		if($kcllv > 60){$kcllv=60;}
		if($kcllv == 60){
			if($ksyoku==0){$ks0=1;}
			elsif($ksyoku==1){$ks1=1;}
			elsif($ksyoku==2){$ks2=1;}
			elsif($ksyoku==3){$ks3=1;}
			elsif($ksyoku==4){$ks4=1;}
			elsif($ksyoku==5){$ks5=1;}
			elsif($ksyoku==6){$ks6=1;}
			elsif($ksyoku==7){$ks7=1;}
			elsif($ksyoku==8){$ks8=1;}
			elsif($ksyoku==9){$ks9=1;}
			elsif($ksyoku==10){$ks10=1;}
			elsif($ksyoku==11){$ks11=1;}
			elsif($ksyoku==12){$ks12=1;}
			elsif($ksyoku==13){$ks13=1;}
			elsif($ksyoku==14){$ks14=1;}
			elsif($ksyoku==15){$ks15=1;}
			elsif($ksyoku==16){$ks16=1;}
			elsif($ksyoku==17){$ks17=1;}
			elsif($ksyoku==18){$ks18=1;}
			elsif($ksyoku==19){$ks19=1;}
			elsif($ksyoku==20){$ks20=1;}
			elsif($ksyoku==21){$ks21=1;}
			elsif($ksyoku==22){$ks22=1;}
			elsif($ksyoku==23){$ks23=1;}
                        elsif($ksyoku==24){$ks24=1;}
                        elsif($ksyoku==25){$ks25=1;}
                        elsif($ksyoku==26){$ks26=1;}
                        elsif($ksyoku==27){$ks27=1;}
                        elsif($ksyoku==28){$ks28=1;}
                        elsif($ksyoku==29){$ks29=1;}
                        elsif($ksyoku==30){$ks30=1;}
                        }

		$khp = $kmaxhp;

if($hit){$comment .= "ＨＰが<font class=yellow>$ahp</font>上がった！！";}
if($t1) { $comment .= "力が<font class=yellow>$as0</font>上がった。"; }
if($t2) { $comment .= "魔力が<font class=yellow>$as1</font>上がった。"; }
if($t3) { $comment .= "信仰心が<font class=yellow>$as2</font>上がった。"; }
if($t4) { $comment .= "生命力が<font class=yellow>$as3</font>上がった。"; }
if($t5) { $comment .= "器用さが<font class=yellow>$as4</font>上がった。"; }
if($t6) { $comment .= "速さが<font class=yellow>$as5</font>上がった。"; }
if($t7) { $comment .= "魅力が<font class=yellow>$as6</font>上がった。"; }
if($t8) { $comment .= "カルマが<font class=yellow>$as7</font>上がった。"; }
	
}
}
}
#------------------#
#　武器防具読み込み#
#------------------#
sub item_read {

	if($kitem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($ci_no,$ci_name,$ci_dmg,$ci_gold,$ci_plus) = split(/<>/);
			if($kitem eq $ci_no) { last; }
		}
	}
	if($witem){
		open(IN,"$item_file");
		@battle_item = <IN>;
		close(IN);

		foreach(@battle_item){
			($wi_no,$wi_name,$wi_dmg,$wi_gold,$wi_plus) = split(/<>/);
			if($witem eq $wi_no) { last; }
		}
	}

	if($kdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($cd_no,$cd_name,$cd_dmg,$cd_gold,$cd_plus) = split(/<>/);
			if($kdef eq $cd_no) { last; }
		}
	}
	if($wdef){
		open(IN,"$def_file");
		@battle_def = <IN>;
		close(IN);

		foreach(@battle_def){
			($wd_no,$wd_name,$wd_dmg,$wd_gold,$wd_plus) = split(/<>/);
			if($wdef eq $wd_no) { last; }
		}
	}

	$hit=0;
	if($kacsno){
		open(IN,"$acs_file");
		@log_acs = <IN>;
		close(IN);

		foreach(@log_acs){
			($a_no,$a_name,$a_gold,$a_kouka,$a_0up,$a_1up,$a_2up,$a_3up,$a_4up,$a_5up,$a_6up,$a_lpup,$a_hitup,$a_kaihiup,$a_wazaup) = split(/<>/);
			if($kacsno eq "$a_no"){$hit=1;last; }
		}
		if(!$hit) { $a_name="-";$a_kouka=0; $a_0up=0;$a_1up=0;$a_2up=0;$a_3up=0;$a_4up=0;$a_5up=0;$a_6up=0;$a_lpup=0;$a_hitup=0;$a_kaihiup=0;$a_wazaup=0;}
	}
	$hit=0;
	if($wacsno){
		open(IN,"$acs_file");
		@log_acs = <IN>;
		close(IN);

		foreach(@log_acs){
			($wa_no,$wa_name,$wa_gold,$wa_kouka,$wa_0up,$wa_1up,$wa_2up,$wa_3up,$wa_4up,$wa_5up,$wa_6up,$wa_lpup,$wa_hitup,$wa_kaihiup,$wa_wazaup) = split(/<>/);
			if($wacsno eq "$wa_no"){$hit=1;last; }
		}
		if(!$hit) { $wa_name="-";$wa_kouka=0; $wa_0up=0;$wa_1up=0;$wa_2up=0;$wa_3up=0;$wa_4up=0;$wa_5up=0;$wa_6up=0;$wa_lpup=0;$wa_hitup=0;$wa_kaihiup=0;$wa_wazaup=0;}
	}

}
#------------------#
#挑アクセサリー効果#
#------------------#
sub acs_waza {

	if($ktac){&atowaza;}
	if($a_kouka && !$wazawaza){require "./acstech/$a_kouka.pl";$wazawaza=1;}
	if($a_kouka){&acskouka;}

}
#------------------#
#挑アクセサリー加算#
#------------------#
sub acs_add {
	$kn_0 += $a_0up;
	$kn_1 += $a_1up;
	$kn_2 += $a_2up;
	$kn_3 += $a_3up;
	$kn_4 += $a_4up;
	$kn_5 += $a_5up;
	$kn_6 += $a_6up;
	$klp  += $a_lpup;
if($ktac){require "./tech/$ktac.pl";}
}
#------------------#
#挑アクセサリー減算#
#------------------#
sub acs_sub {
	$kn_0 -= $a_0up;
	$kn_1 -= $a_1up;
	$kn_2 -= $a_2up;
	$kn_3 -= $a_3up;
	$kn_4 -= $a_4up;
	$kn_5 -= $a_5up;
	$kn_6 -= $a_6up;
	$klp  -= $a_lpup;
}

sub syokuzero{$dmg1 += int(rand($kn_0)) + $ci_dmg;}
sub syokuone{$dmg1 += int(rand($kn_1)) + $ci_dmg;}
sub syokutwo{$dmg1 += int(rand($kn_2)) + $ci_dmg;}
sub syokuthree{$dmg1 += int(rand($kn_4)) + $ci_dmg;}
sub syokufour{$dmg1 += int(rand($kn_1)) + $ci_dmg;}
sub syokufive{$dmg1 += int(rand($kn_1)) + $ci_dmg;}
sub syokusix{$dmg1 += int(rand($kn_2)) + int(rand($kn_6)) + $ci_dmg;}
sub syokuseven{$dmg1 += int(rand($kn_1)) + int(rand($kn_6)) + $ci_dmg;}
sub syokueight{$dmg1 += int(rand($kn_0)) + int(rand($kn_4)) + $ci_dmg;}
sub syokunine{$dmg1 += int(rand($kn_1)) + int(rand($kn_2)) + $ci_dmg;}
sub syokuten{$dmg1 += int(rand($kn_0)) + int(rand($kn_2)) + $ci_dmg;}
sub syokueleven{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + $ci_dmg;}
sub syokutwelve{$dmg1 += int(rand($kn_0)) + int(rand($kn_3)) + $ci_dmg;}
sub syokuthirteen{$dmg1 += int(rand($kn_0)) + int(rand($kn_4)) + $ci_dmg;}
sub syokufourteen{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + $ci_dmg;}
sub syokufifteen{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + $ci_dmg;}
sub syokusixteen{$dmg1 += int(rand($kn_0)) + int(rand($kn_4)) + $ci_dmg;}
sub syokuseventeen{$dmg1 += int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_6)) + $ci_dmg;}
sub syokueighteen{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp) + $ci_dmg;}
sub syokunineteen{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp) + $ci_dmg;}
sub syokutwenty{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp) + $ci_dmg;}
sub syokutwentyone{$dmg1 += int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp) + $ci_dmg;}
sub syokutwentytwo{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 2) + $ci_dmg;}
sub syokutwentythree{$dmg1 += int(rand($kn_0)) + $ci_dmg;}
sub syokutwentyfour{$dmg1 += ((int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 2) + $ci_dmg;}
sub syokutwentyfive{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int((rand($kn_4))*5) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 2) + $ci_dmg;}
sub syokutwentysix{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 2) + $ci_dmg;}
sub syokutwentyseven{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 3) + $ci_dmg;}
sub syokutwentyeight{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 3) + $ci_dmg;}
sub syokutwentynine{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 4) + $ci_dmg;}
sub syokuthirty{$dmg1 += ((int(rand($kn_0)) + int(rand($kn_1)) + int(rand($kn_2)) + int(rand($kn_3)) + int(rand($kn_4)) + int(rand($kn_5)) + int(rand($kn_6)) + int($klp)) * 5) + $ci_dmg;}

1;
