#!/usr/local/bin/perl

# ※使用上の注意事項※
# 必ずバックアップを取って下さい。
# 使用前に必ずsyokuフォルダ、itemフォルダを作成して下さい。

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require './jcode.pl';

# レジストライブラリの読み込み
my $ret = do './regist.pl';

if (!$ret) {
    die "do failed: $! $@";
}

no strict 'refs';

print STDERR "CODE=", *{"main::chara_regist"}{CODE} ? "YES" : "NO", "\n";
print STDERR "SCALAR=", defined *{"main::chara_regist"}{SCALAR} ? "YES" : "NO", "\n";
print STDERR "ARRAY=", defined *{"main::chara_regist"}{ARRAY} ? "YES" : "NO", "\n";
print STDERR "HASH=", defined *{"main::chara_regist"}{HASH} ? "YES" : "NO", "\n";

# レジストライブラリの読み込み
require './sankasya.pl';

# 初期設定ファイルの読み込み
require './data/ffadventure.ini';

# アイテムライブラリの読み込み
require './item.pl';

# 飛空挺データディレクトリ
$chara2 = "./charalog2/";

# 追加職業数の指定。デフォルトから追加した職業数を指定して下さい。
$add_syoku = 0;

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

&decode;

opendir (DIR,'./charalog') or die "$!";
foreach $entry (readdir(DIR)){

	if ($entry =~ /\.cgi/) {
		@syoku_master = ();
		@chara = ();
		@data = ();
		@item = ();
		$new_item = "";
		$new_syoku = "";

		open(IN,"./charalog/$entry");
		@data = <IN>;
		close(IN);

		$data[0] =~ s/\n//g;

		@chara = split(/<>/,$data[0]);

		$in{'id'} = $chara[0];

		if (-e "./syoku/$chara[0].cgi") { next; }

		$l = $add_syoku + 64;
		for ($i=34;$i<=$l;$i++) {
			$s = $i - 34;
			if ($chara[$i]) {
				$syoku_master[$s] = 60;
			}
			$chara[$i] = '';
		}

		$l++;
		$chara[$l] = '';
		$l++;
		$chara[$l] = '';

		foreach (@syoku_master) {
			$new_syoku .="$_<>";
		}

		if ($chara[24]) {
			&item_read($chara[24]);
		} else {
			$item[0] = '素手';
			$item[1] = 0;
			$item[2] = 0;
		}

		if ($chara[29]) {
			&def_read($chara[29]);
		} else {
			$item[3] = '普段着';
			$item[4] = 0;
			$item[5] = 0;
		}

		if ($chara[31]) {
			&acs_read($chara[31]);
		} else {
			$item[6] = 'なし';
			$item[7] = 0;
			$item[8] = 0;
			$item[9] = 0;
			$item[10] = 0;
			$item[11] = 0;
			$item[12] = 0;
			$item[13] = 0;
			$item[14] = 0;
			$item[15] = 0;
			$item[16] = 0;
			$item[17] = 0;
			$item[18] = 0;
		}

		foreach(@item){
			$new_item .="$_<>";
		}


		open(OUT,">./item/$chara[0].cgi");
		print OUT $new_item;
		close(OUT);

		open(OUT,">./syoku/$chara[0].cgi");
		print OUT $new_syoku;
		close(OUT);

		open(IN,"./banklog/$entry");
		@bank = <IN>;
		close(IN);

		$chara[34] = 0;

		(undef,undef,$chara[34]) = split(/<>/,$bank[0]);

		&chara_regist;

		open(IN,"$chara2/$chara[0].cgi");
		@read_data = <IN>;
		close(IN);

		@hitem = split(/,/,$read_data[0]);
		@hdef = split(/,/,$read_data[1]);
		@hacs = split(/,/,$read_data[2]);

		$i = 0;
		foreach (@hitem) {
			if ($i == 0) { $i++; next;}
			elsif ($_ eq '0000') { $i++; next;}
			&item_read($_);
			$i--;
			$souko_acs[$i] = "$ci_no<>$item[0]<>$item[1]<>$ci_gold<>$item[2]<>\n";
			$i++;
		}

		open(OUT,">$souko_folder/item/$chara[0].cgi");
		print OUT @souko_item;
		close(OUT);

		$i = 0;
		foreach (@hdef) {
			if ($i == 0) { $i++; next;}
			elsif ($_ eq '0000') { $i++; next;}
			&def_read($_);
			$i--;
			$souko_def[$i] = "$cd_no<>$item[3]<>$item[4]<>$cd_gold<>$item[5]<>\n";
			$i++;
		}

		open(OUT,">$souko_folder/def/$chara[0].cgi");
		print OUT @souko_def;
		close(OUT);

		$i = 0;
		foreach (@hacs) {
			if ($i == 0) { $i++; next;}
			elsif ($_ eq '0000') { $i++; next;}
			&acs_read($_);
			$i--;
			$souko_acs[$i] = "$a_no<>$item[6]<>$a_gold<>$item[7]<>$item[8]<>$item[9]<>$item[10]<>$item[11]<>$item[12]<>$item[13]<>$item[14]<>$item[15]<>$item[16]<>$item[17]<>$item[18]<>$item[19]<>\n";
			$i++;
		}

		open(OUT,">$souko_folder/acs/$chara[0].cgi");
		print OUT @souko_acs;
		close(OUT);
	}
}

	&header;

	print "処理が完了しました。<br>";

	&footer;

	exit;
