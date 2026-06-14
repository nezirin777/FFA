#-----------------------------------------------------#
#　連打防止スクリプト
#　edit by Datch
#  http://shigen.nobg.net/
#
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#-----------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した #
#    いかなる損害に対して作者は一切の責任を負いません。     	#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。   	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#
# 初期設定
# フラグファイルの保存形式（３バイト）
$F_cfg[0]="100";
# フラグファイル収納フォルダ
$F_cfg[1]="charalogflg/";
&flag_load('Dur',$in{'id'});		# 前回リクエスト時間読み込み
$flag[0]=time()-10 if($flag[0] eq '');	# リクエスト記録なし
$_=$flag[0]+2; $flag[0]=time();		# リクエスト間隔計算・時間記録
&flag_save('Dur',$in{'id'});		# 新・リクエスト時間記録
&flag_error('連打禁止') if(time()<$_);	# 連打君排除

# Dflag Ver 1.01 簡易版 by Dutch

sub flag_seek {
	# 項目読み込み／作成
	&flag_error("フラグＩＤ エラー") if(length($F_s[0]) != 3);

	$F_s[2]=(index $F_data[0],$F_s[0])/4;
	if($F_s[2] == -0.25) {
		# 新規項目作成
		@flag=();
		chomp $F_data[0];
		$F_s[2]=(length($F_data[0])+1)/4;
		$F_data[0].=",$F_s[0]\n";
		$F_data[$F_s[2]]="\n";
	} else {
		# フラグ読み込み
		$F_s[3]=$F_data[$F_s[2]];
		chomp $F_s[3];
		@flag=split /<>/,$F_s[3];
	}
}
sub flag_load {
	# エラー対策
	&flag_error("不正なＩＤ") if($_[1] =~ m/[^0-9a-zA-Z]/ || length($_[1]) > 8);

	# データロード
	@F_s=($_[0],$_[1]);
	$F_s[3]=$F_cfg[1].$F_s[1].'_flag.cgi';
	if( !(-e $F_s[3]) ) { $F_data[0]=$F_cfg[0]; } else {
		open(F_FILE,$F_s[3]);
		@F_data=<F_FILE>;
		close(F_FILE);
	}
	&flag_seek();
}
sub flag_save {
	@F_w=@flag;
	if($F_s[1] ne $_[1]) {
		# ユーザーＩＤ違い
		&flag_load($_[0],$_[1]);
	} elsif($F_s[0] ne $_[0]) {
		# フラグＩＤ違い
		@F_s=($_[0],$_[1]);
		&flag_seek();
	}
	@flag=@F_w;
	$F_s[3]=join('<>',@flag);
	$F_data[$F_s[2]]=$F_s[3]."\n";

	$F_s[3]=$F_cfg[1].$F_s[1].'_flag.cgi';
	open(F_FILE,'>'.$F_s[3]);
	print F_FILE @F_data;
	close(F_FILE);
	chmod 0606,$F_s[3];
}
sub flag_error {
	print "Content-type: text/html\n\n$_[0]";
	exit;
}

1;
