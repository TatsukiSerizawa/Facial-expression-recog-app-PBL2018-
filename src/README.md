# PBL本番環境

本番と言いつつローカル……

## 内容

・cgi-bin/analysis.py: 写真をapiに渡して分析結果を返して結果を表示する

・index.html: 自撮りをして写真をアップロードする

## 実行方法

このディレクトリ上で以下のコマンドを実行

```
$ python3 -m http.server --cgi
```
