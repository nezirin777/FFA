
#----------------#
#  書き込み処理  #
#----------------#
sub regist {
	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	if($in{'n_0'}+$in{'n_1'}+$in{'n_2'}+$in{'n_3'}+$in{'n_4'}+$in{'n_5'}+$in{'n_6'}>20){
		unlink($lockfile) if(-e $lockfile);
		&error('パラメータが不正です！！');
	}

	&set_cookie;

	&get_host;

	$date = time();

	open(IN,"./charalog/$in{'id'}.cgi");
	@regist = <IN>;
	close(IN);

	# パスワードを暗号化
	if ($in{'pass'} ne "") { $newpass = &encrypt($in{'pass'}); }

	$hit=0;@new=();
	foreach(@regist){
		($cid,$cpass,$csite,$curl,$cname,$csex,$cchara,$cn_0,$cn_1,$cn_2,$cn_3,$cn_4,$cn_5,$cn_6,$csyoku,$chp,$cmaxhp,$cex,$clv,$cgold,$clp,$ctotal,$ckati,$cwaza,$citem,$cmons,$chost,$cdate,$cmori,$cdef,$ctac,$cacsno,$cmoriturn,$ccllv,$cs0,$cs1,$cs2,$cs3,$cs4,$cs5,$cs6,$cs7,$cs8,$cs9,$cs10,$cs11,$cs12,$cs13,$cs14,$cs15,$cs16,$cs17,$cs18,$cs19,$cs20,$cs21,$cs22,$cs23,$cs24,$cs25,$cs26,$cs27,$cs28,$cs29,$cs30,$crec) = split(/<>/);
		if($cid eq "$in{'id'}" and $in{'new'} eq 'new') {
			&error("そのIDはすでに登録されています");
		}elsif($curl eq "$in{'url'}" and $in{'new'} eq 'new'){
			&error("そのURLはすでに登録されています");
		}elsif($cid eq "$kid"){
			unshift(@new,"$kid<>$kpass<>$ksite<>$kurl<>$kname<>$ksex<>$kchara<>$kn_0<>$kn_1<>$kn_2<>$kn_3<>$kn_4<>$kn_5<>$kn_6<>$ksyoku<>$khp<>$kmaxhp<>$kex<>$klv<>$kgold<>$klp<>$ktotal<>$kkati<>$kwaza<>$kitem<>$kmons<>$host<>$date<>$kmori<>$kdef<>$ktac<>$kacsno<>$kmoriturn<>$kcllv<>$ks0<>$ks1<>$ks2<>$ks3<>$ks4<>$ks5<>$ks6<>$ks7<>$ks8<>$ks9<>$ks10<>$ks11<>$ks12<>$ks13<>$ks14<>$ks15<>$ks16<>$ks17<>$ks18<>$ks19<>$ks20<>$ks21<>$ks22<>$ks23<>$ks24<>$ks25<>$ks26<>$ks27<>$ks28<>$ks29<>$ks30<>$krec<>\n");
			$hit=1;last;
		}}

	if(!$hit and $in{'new'} eq 'new'){
		$lp=int(rand(15));
		$hp = int(($in{'n_3'} + $kiso_nouryoku[3]) + (rand($lp) + 1)) + $kiso_hp;
		$ex=0;
		$lv=1;
		$gold=0;
		$n_0 = $kiso_nouryoku[0] + $in{'n_0'};
		$n_1 = $kiso_nouryoku[1] + $in{'n_1'};
		$n_2 = $kiso_nouryoku[2] + $in{'n_2'};
		$n_3 = $kiso_nouryoku[3] + $in{'n_3'};
		$n_4 = $kiso_nouryoku[4] + $in{'n_4'};
		$n_5 = $kiso_nouryoku[5] + $in{'n_5'};
		$n_6 = $kiso_nouryoku[6] + $in{'n_6'};
		$c_syoku = $in{'syoku'};
		unshift(@new,"$in{'id'}<>$newpass<>$in{'site'}<>$in{'url'}<>$in{'c_name'}<>$in{'sex'}<>$in{'chara'}<>$n_0<>$n_1<>$n_2<>$n_3<>$n_4<>$n_5<>$n_6<>$c_syoku<>$hp<>$hp<>$ex<>$lv<>$intgold<>$lp<>$total<>$kati<>$waza<>$item<>$mons<>$host<>$date<>$mori<>$def<>$tac<>$acsno<>0<>1<>$s0<>$s1<>$s2<>$s3<>$s4<>$s5<>$s6<>$s7<>$s8<>$s9<>$s10<>$s11<>$s12<>$s13<>$s14<>$s15<>$s16<>$s17<>$s18<>$s19<>$s20<>$s21<>$s22<>$s23<>$s24<>$s25<>$s26<>$s27<>$s28<>$s29<>$s30<>0<>\n");
	}

	open(OUT,">./charalog/$in{'id'}.cgi");
	print OUT @new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	if($in{'new'}) { &make_end; }
}

1;


#----------------#
#  デコード処理  #
#----------------#
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("投稿量が大きすぎます"); }
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }
	@pairs = split(/&/, $buffer);
	foreach (@pairs) {
		($name,$value) = split(/=/, $_);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# 文字コードをシフトJIS変換
		&jcode'convert(*value, "sjis", "", "z");

		# タグ処理
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\"/&quot;/g;

		# 改行等処理
		$value =~ s/\r//g;
		$value =~ s/\n//g;

		# 一括削除用
		if ($name eq 'del') { push(@DEL,$value); }

		$in{$name} = $value;
	}
	$mode = $in{'mode'};
	$in{'url'} =~ s/^http\:\/\///;
	$cookie_pass = $in{'pass'};
	$cookie_id = $in{'id'};
    require 'renda.cgi' if($in{'id'} ne '');
}

1;


#----------------#
#  ホスト名取得  #
#----------------#
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($get_remotehost) {
		if ($host eq "" || $host eq "$addr") {
			$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
		}
	}
	if ($host eq "") { $host = $addr; }
}

1;

#--------------#
#  エラー処理  #
#--------------#
sub error {
	if (-e $lockfile) { unlink($lockfile); }
	if (-e $cntlock)  { unlink($cntlock); }

	&header;
	print "<center><hr width=400><h3>ERROR !</h3>\n";
	print "<P><font color=red><B>$_[0]</B></font>\n";
	print "<P><hr width=400></center>\n";
	print "<a href=\"$scripto\">TOPページへ</a>\n";
	print "</body></html>\n";
	exit;
}

1;

#--------------#
#  クラス設定  #
#--------------#
sub class {
	if($chara_flag){
			if($kcllv > 59) {$class = "★★★★★★　　<i><b>(Master)</b></i>";
			}elsif($kcllv < 10){$class = "■□□□□□　　<i><b>(Beginner)</b></i>";
			}elsif($kcllv < 20){$class = "■■□□□□　　<i><b>(Charanger)</b></i>";
			}elsif($kcllv < 30){$class = "■■■□□□　　<i><b>(Low Class)</b></i>";
			}elsif($kcllv < 40){$class = "■■■■□□　　<i><b>(Normal Class)</b></i>";
			}elsif($kcllv < 50){$class = "■■■■■□　　<i><b>(High Class)</b></i>";
			}elsif($kcllv < 60){$class = "■■■■■■　　<i><b>(Top Class)</b></i>";
			}
			}else{
			if($wcllv > 59) {$class = "★★★★★★　　<i><b>(Master)</b></i>";
			}elsif($wcllv < 10){$class = "■□□□□□　　<i><b>(Beginner)</b></i>";
			}elsif($wcllv < 20){$class = "■■□□□□　　<i><b>(Charanger)</b></i>";
			}elsif($wcllv < 30){$class = "■■■□□□　　<i><b>(Low Class)</b></i>";
			}elsif($wcllv < 40){$class = "■■■■□□　　<i><b>(Normal Class)</b></i>";
			}elsif($wcllv < 50){$class = "■■■■■□　　<i><b>(High Class)</b></i>";
			}elsif($wcllv < 60){$class = "■■■■■■　　<i><b>(Top Class)</b></i>";
			}
			}
}

1;


#-------------------------------#
#  ロックファイル：symlink関数  #
#-------------------------------#
sub lock1 {
	local($retry) = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0) { &error("LOCK is BUSY"); }
		sleep(1);
	}
}

1;

#----------------------------#
#  ロックファイル：open関数  #
#----------------------------#
sub lock2 {
	local($retry) = 0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {
			open(LOCK,">$lockfile") || &error("Can't Lock");
			close(LOCK);
			$retry = 1;
			last;
		}
	}
	if (!$retry) { &error("しばらくお待ちになってください(^^;)"); }
}

1;
#----------------------#
#  パスワード暗号処理  #
#----------------------#
sub encrypt {
	local($inpw) = $_[0];
	local(@SALT, $salt, $encrypt);

	@SALT = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $SALT[int(rand(@SALT))] . $SALT[int(rand(@SALT))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}

1;
