# For my lecture assignment

このスクリプトはwebpを利用して画像圧縮を行うスクリプトです。

## usage

事前準備
必要なコマンドをinstall(for Mac)
```
$ brew install webp
$ brew install imagemagick
```

対象となる画像を用意。
```
# 圧縮前と圧縮後の画像の保存先の親ディレクトリを環境変数にセット
$ export VIDEO_COMM_LEC=<your path>
# 画像保存用、圧縮画像保存用のディレクトリを作成
$ cd $VIDEO_COMM_LEC
$ mkdir {image-dataset, result}
```

コマンドの実行
```
$ python3 video-communication-lec.py
```
result.csvファイルに結果が出力されます。