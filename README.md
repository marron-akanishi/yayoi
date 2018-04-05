# yayoi
iM@S chara detect with TensorFlow  

## なにこれ
アイマスのキャラである765PRO AS組の13人を識別するプログラムです。  

## 動作環境  
Python 3.5以降で動くと思います。  
requirements.txtに沿って必要なライブラリをpipでインストールしてください。  
### 特定のライブラリが動かない場合
#### dlib
dlibのビルドにはcmakeとboostが必要となります。  
Windowsの場合は[AFD](https://github.com/marron-akanishi/AFD)の参考URLを見てください。  
Ubuntuの場合はpipを実行する前に`sudo apt install cmake libboost-python-dev`を実行してください。  
#### cv2
Ubuntuで実行するとcv2をimportした際に以下のエラーが発生する場合があります。  
```
ImportError: libSM.so.6: cannot open shared object file: No such file or directory
ImportError: libXrender.so.1: cannot open shared object file: No such file or directory
```
発生した場合は`sudo apt install libsm6 libxrender1`を実行してください。

## ファイル構成
static/ -> WebUIを動かすのに必要なファイル群  
templates/ -> レンダリング用HTMLファイル  
chara.json -> タグとキャラ名を関連付けるJSONファイル  
checkpoint, imas_model.ckpt* -> キャラ判定用モデル  
detector_face.svm -> 顔判定用特徴量ファイル  
pic_eval.py -> キャラ判定器本体スクリプト  
study.py -> 学習用スクリプト  
web.py -> WebUI用スクリプト  

## 使い方  
学習にはデータセットが必要となるため、ここでは説明しません。  
[Tagger](https://github.com/marron-akanishi/tagger)で作成したデータセットをそのまま使えるようにしてあるはずです。  
すでに学習済みのファイルを入れてありますので、実行するだけなら可能です。  
ただ単に`python web.py`と実行すれば動きます。  
ただ、`./static/images/yayoi_sd.png`を現在消した状態にしています。  
過去のコミットを覗くと出てくるので、それを利用してください。  

## 動作画像
![サンプル](https://raw.githubusercontent.com/marron-akanishi/yayoi/master/images/detect_test.png)

## 問題点
まだまだ精度が甘いです。AS組以外の区別があまり出来ません。  
90%を切るとAS組以外と判定するようにしていますが、正しいキャラでもAS組以外と判定しまうことがあります。判定詳細をよく見てください。  
~~また、ずっと画像を投げていると`./static/images/upload/`内に大量に画像が溜まっていくので、定期的に削除してください。~~  
テストでCookieに一意なキーを置くようにし、それをファイル名として使うようにしました。  

## 参考
このスクリプトは以下のリポジトリからほとんどのスクリプトをお借りしました。  
[AkiyoshiOkano/zuckerberg-detect-ai](https://goo.gl/WBmzbt)