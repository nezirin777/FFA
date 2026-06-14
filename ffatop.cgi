#!/usr/local/bin/perl

#------------------------------------------------------#
#　本スクリプトの著作権はいくにあります。
#いかなる理由があってもこの表記を削除することはできません
#違反を発見した場合、スクリプトの利用を停止していただく
#だけでなく、然るべき処置をさせていただきます。
#------------------------------------------------------#
#  FF ADVENTURE(いく改)
#　remodeling by いく
#　http://www.eriicu.com
#　icu@kcc.zaq.ne.jp
#------------------------------------------------------#
#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した #
#    いかなる損害に対して作者は一切の責任を負いません。     	#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。   	#
#    http://icus.s13.xrea.com/cgi-bin/cbbs/cbbs.cgi             #
#    直接メールによる質問は一切お受けいたしておりません。   	#
#---------------------------------------------------------------#

# 日本語ライブラリの読み込み
require 'jcode.pl';

# レジストライブラリの読み込み
require 'regist.pl';

# 初期設定ファイルの読み込み
require 'data/ffadventure.ini';

open(IN,"$winner_file") or &error('ファイルを開けませんでした。');
	@winner = <IN>;
	close(IN);

	($wid,$wpass,$wsite,$wurl,$wname,$wsex,$wchara,$wn_0,$wn_1,$wn_2,$wn_3,$wn_4,$wn_5,$wn_6,$wsyoku,$whp,$wmaxhp,$wex,$wlv,$wgold,$wlp,$wtotal,$wkati,$wwaza,$witem,$wmons,$whost,$wdate,$wcount,$lsite,$lurl,$lname) = split(/<>/,$winner[0]);


if($mente) {
print "Content-type: text/html\n\n";
print "現在サーバー移転中です。しばらくお待ちください。\n";
exit;}

print "Content-type: text/html\n\n";
print <<"EOM";
<td valign="top" align="center">
<table border=1 width="100%" hight="100%">
<tr><td align="center" class="b2" colspan=2><font color="#ffffff">現在のＦＦＡチャンプ</font></td>
</tr>
<tr>
<td rowspan="2"  align="center" class="b2" width=70 height=60><img src="$img_path/$chara_img[$wchara]"></td>
<td align="center" class="b1"><font color="#ffffff">$chara_syoku[$wsyoku]の$wnameさんが<br><font color=red size =7>$wcount</font>連勝中です。</font></td>
</tr>
<tr>
</tr>
</table>
FFA 小窓表示 script by <a href=http://www.eriicu.com>いく</a>
EOM
	print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";

exit;
