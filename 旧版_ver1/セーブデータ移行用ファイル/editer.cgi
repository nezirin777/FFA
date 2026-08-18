#!/usr/local/bin/perl

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
# 3. 設置したら皆さんに楽しんでもらう為にも、Webリングへぜひ参加#
#    してくださいm(__)m						#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi　		#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

# 処理するフォルダ
$folder = './acstech';

# 処理するファイルの拡張子
$file = 'pl';

# このファイル用設定
$backgif = $sts_back;
$midi = "";

#================================================================#
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓#
#┃ これより下はCGIに自信のある方以外は扱わないほうが無難です　┃#
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛#
#================================================================#

#--------------#
#　メイン処理　#
#--------------#

opendir(DIR,"$folder") or die "$!";
foreach $entry (readdir(DIR)) {

	if($entry=~/\.$file/){
		open(IN,"$folder/$entry");
		@new = ();
		foreach (<IN>) {
			$_ =~ s/kid/chara\[0\]/gi;
			$_ =~ s/kpass/chara\[1\]/gi;
			$_ =~ s/ksite/chara\[2\]/gi;
			$_ =~ s/kurl/chara\[3\]/gi;
			$_ =~ s/kname/chara\[4\]/gi;
			$_ =~ s/ksex/chara\[5\]/gi;
			$_ =~ s/kchara/chara\[6\]/gi;
			$_ =~ s/kn_0/chara\[7\]/gi;
			$_ =~ s/kn_1/chara\[8\]/gi;
			$_ =~ s/kn_2/chara\[9\]/gi;
			$_ =~ s/kn_3/chara\[10\]/gi;
			$_ =~ s/kn_4/chara\[11\]/gi;
			$_ =~ s/kn_5/chara\[12\]/gi;
			$_ =~ s/kn_6/chara\[13\]/gi;
			$_ =~ s/ksyoku/chara\[14\]/gi;
			$_ =~ s/khp/chara\[15\]/gi;
			$_ =~ s/kmaxhp/chara\[16\]/gi;
			$_ =~ s/kex/chara\[17\]/gi;
			$_ =~ s/klv/chara\[18\]/gi;
			$_ =~ s/kgold/chara\[19\]/gi;
			$_ =~ s/klp/chara\[20\]/gi;
			$_ =~ s/ktotal/chara\[21\]/gi;
			$_ =~ s/kkati/chara\[22\]/gi;
			$_ =~ s/kwaza/chara\[23\]/gi;
			$_ =~ s/kitem/chara\[24\]/gi;
			$_ =~ s/kmons/chara\[25\]/gi;
			$_ =~ s/khost/chara\[26\]/gi;
			$_ =~ s/kdate/chara\[27\]/gi;
			$_ =~ s/kmori/chara\[28\]/gi;
			$_ =~ s/kdef/chara\[29\]/gi;
			$_ =~ s/ktac/chara\[30\]/gi;
			$_ =~ s/kacsno/chara\[31\]/gi;
			$_ =~ s/kmoriturn/chara\[32\]/gi;
			$_ =~ s/kcllv/chara\[33\]/gi;
			$_ =~ s/wid/winner\[0\]/gi;
			$_ =~ s/wsite/winner\[1\]/gi;
			$_ =~ s/wurl/winner\[2\]/gi;
			$_ =~ s/wname/winner\[3\]/gi;
			$_ =~ s/wsex/winner\[4\]/gi;
			$_ =~ s/wchara/winner\[5\]/gi;
			$_ =~ s/wn_0/winner\[6\]/gi;
			$_ =~ s/wn_1/winner\[7\]/gi;
			$_ =~ s/wn_2/winner\[8\]/gi;
			$_ =~ s/wn_3/winner\[9\]/gi;
			$_ =~ s/wn_4/winner\[10\]/gi;
			$_ =~ s/wn_5/winner\[11\]/gi;
			$_ =~ s/wn_6/winner\[12\]/gi;
			$_ =~ s/wlp/winner\[13\]/gi;
			$_ =~ s/wsyoku/winner\[14\]/gi;
			$_ =~ s/whp/winner\[15\]/gi;
			$_ =~ s/wmaxhp/winner\[16\]/gi;
			$_ =~ s/wlv/winner\[17\]/gi;
			$_ =~ s/wtotal/winner\[18\]/gi;
			$_ =~ s/wkati/winner\[19\]/gi;
			$_ =~ s/wwaza/winner\[20\]/gi;
			$_ =~ s/wtac/winner\[37\]/gi;
			$_ =~ s/whost/winner\[38\]/gi;
			$_ =~ s/wcllv/winner\[39\]/gi;
			$_ =~ s/wcount/winner\[44\]/gi;
			$_ =~ s/<p>//gi;
			$_ =~ s/<\/p>/<br>/gi;
			$_ =~ s/<p\/>/<br>/gi;
			$_ =~ s/wi_dmg/winner\[22\]/gi;
			$_ =~ s/wd_dmg/winner\[25\]/gi;
			$_ =~ s/ci_dmg/item\[1\]/gi;
			$_ =~ s/cd_dmg/item\[4\]/gi;
			$_ =~ s/wa_name/winner\[27\]/gi;
			$_ =~ s/wa_kouka/winner\[51\]/gi;
			$_ =~ s/\$a_name/\$item\[6\]/gi;
			$_ =~ s/\$a_kouka/\$item\[7\]/gi;
			$_ =~ s/\;\$/\;\n\t\$/gi;
			$_ =~ s/\;\}/\;\n\}/gi;
			$_ =~ s/\{\$/\{\n\t\$/gi;
			$_ =~ s/\{\i/\{\n\t\i/gi;
			$_ =~ s/f\(/f \(/gi;
			$_ =~ s/\)\{/\) \{/gi;
			$_ =~ s/\=\"/\= \"/gi;
			push(@new,$_);
		}
		close(IN);

		open(OUT,">$folder/$entry");
		print OUT @new;
		close(OUT);
	}
}
closedir(DIR);


&header;

print "処理完了<br>";

&footer;

exit;
