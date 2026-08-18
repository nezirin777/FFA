# Ver1からVer2へのセーブデータ移行

`convert_to_ver2.py`は、親ディレクトリの`旧版_ver1`にある旧形式の
セーブデータを、Ver2形式へ一括変換する独立したスクリプトです。
変換元のファイルは変更しません。

```
使い方
python convert_to_ver2.py --dry-run
python convert_to_ver2.py --output ..\converted_ver2
```

出力先には、FFA Emiliar Ver2のデータディレクトリへ組み込める形式で
変換済みデータが作成されます。
既存の出力先へ再変換する場合は`--overwrite`を指定してください。

## 変換内容

- `charalog`はVer2の67項目形式へ整形します。`banklog`の銀行残高は、
  Ver2が使用するキャラデータ34番目の項目へ格納します。
- 装備中の武器・防具・装飾品は、Ver1のマスターデータから`item`形式へ
  再構成します。
- `charalog2`は、`souko/item`、`souko/def`、`souko/acs`へ変換します。
- `datalog/winner.cgi`は、Ver2の54項目形式のチャンプデータへ変換します。
  `recode.cgi`も保存し、最高連勝記録をチャンプデータへ引き継ぎます。
- Ver2では旧版の`save_data`および`load_game`機能が廃止されています。
  そのためVer1の`savelog`は破棄せず、出力先の`savelog`へ保管用データ
  として保存します。
- 旧版CGIはHTMLとしてデータを出力するため、旧データ内のHTMLエンティティは
  維持します。CP932で表現できない文字へ変換して壊すことを防ぐためです。
