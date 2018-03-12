import sys
import json
import os
import random
import numpy as np
import cv2
import tensorflow as tf
import study

# 顔認識特徴量ファイル
face_detector = dlib.simple_object_detector("./detector_face.svm")

# 識別ラベルと各ラベル番号に対応する名前
CHARA_NAMES = json.load(open("./chara.json"))
# 顔サイズ
FACE_SIZE = 64
# エリア拡大
ZOOM = 5

# キャラ判定本体
def chara_detect(img, ckpt_path):
    img = cv2.resize(img, (FACE_SIZE, FACE_SIZE))
    # データを入れる配列
    image = []
    # 画像情報を一列にした後、0-1のfloat値にする
    image.append(img.flatten().astype(np.float32)/255.0)
    # numpy形式に変換し、TensorFlowで処理できるようにする
    image = np.asarray(image)
    # 入力画像に対して、各ラベルの確率を出力して返す(study.pyより呼び出し)
    logits = study.inference(image, 1.0)
    # We can just use 'c.eval()' without passing 'sess'
    sess = tf.InteractiveSession()
    # restore(パラメーター読み込み)の準備
    saver = tf.train.Saver()
    # 変数の初期化
    sess.run(tf.initialize_all_variables())
    if ckpt_path:
        # 学習後のパラメーターの読み込み
        saver.restore(sess, ckpt_path)
    # sess.run(logits)と同じ
    softmax = logits.eval()
    # 判定結果
    result = softmax[0]
    # 判定結果を%にして四捨五入
    rates = [round(n * 100.0, 1) for n in result]
    results = []
    # ラベル番号、名前、パーセンテージの辞書を作成
    for index, rate in enumerate(rates):
        name = CHARA_NAMES[str(index)]
        results.append({
            'label': index,
            'name': name,
            'rate': rate
        })
    return results

# 指定した画像(img_path)を学習結果(ckpt_path)を用いて判定する
def evaluation(img_path, ckpt_path):
    charas = []
    # GraphのReset(らしいが、何をしているのかよくわかっていない…)
    tf.reset_default_graph()
    # ファイルを開く
    image = cv2.imread(img_path)
    try:
        height, width, channels = image.shape
        faces = face_detector(image)
    except:
        return None
    if len(faces) > 0:
        for rect in faces:
            # サイズ取得
            face_width = rect.right() - rect.left()
            face_height = rect.bottom() - rect.top()
            # 長方形の場合、弾く
            if abs(face_width - face_height) > 3:
                continue
            # 幅拡大
            xs = int(rect.left() - face_width/ZOOM)
            if(xs < 0):
                xs = 0
            xe = int(rect.right() + face_width/ZOOM)
            if(xe > width):
                xe = width
            # 高さ拡大
            ys = int(rect.top() - face_height/ZOOM)
            if(ys < 0):
                ys = 0
            ye = int(rect.bottom() + face_height/ZOOM)
            if(ye > height):
                ye = height
            # サイズ更新
            face_width = xe - xs
            face_height = ye - ys
            # 横幅がFACE_SIZE以下は弾く
            if face_width >= FACE_SIZE:
                # 顔部分を赤線で囲う
                cv2.rectangle(image, (xs, ys), (xe, ye), (0, 0, 255), thickness=2)
                # 顔だけ切り出し
                dst = image[ys:ye, xs:xe]
                # キャラ判定
                result = chara_detect(dst, ckpt_path)
                # エリア情報を含めた辞書を生成
                chara = {}
                chara["x"] = xs
                chara["y"] = ys
                chara["width"] = face_width
                chara["height"] = face_height
                chara["rank"] = sorted(result, key=lambda x: x['rate'], reverse=True)
                charas.append(chara)
    else:
        # 顔が見つからなければ処理終了
        return None
    # 顔部分を赤線で囲った画像の保存
    cv2.imwrite(img_path, image)

    # 判定結果を返す
    return charas

# コマンドラインからのテスト用
if __name__ == '__main__':
    print(evaluation(sys.argv[1], './imas_model.ckpt'))
