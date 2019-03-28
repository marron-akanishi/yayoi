import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, make_response, redirect
import pic_eval

OTHER = 13
# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.config['DEBUG'] = True
# 投稿画像の保存先
UPLOAD_FOLDER = './static/images/upload/'

# ルーティング。/にアクセス時
@app.route('/')
def index(error=False):
    res = make_response(render_template('index.html', error=error))
    if request.cookies.get('uid', None) == None:
        res.set_cookie('uid', str(uuid.uuid4()))
    return res

# 画像投稿時のアクション
@app.route('/detect', methods=['POST'])
def post():
    result = None
    filename = request.cookies.get('uid', None)
    if not request.files['file'].filename == '' and filename != None:
        # アップロードされたファイルを保存
        f = request.files['file']
        if f.filename.split('.')[-1] in ['png', 'jpg']:
            filename += "." + f.filename.split('.')[-1]
            img_path = UPLOAD_FOLDER + filename
            f.save(img_path)
            # pic_eval.pyへアップロードされた画像を渡す
            print(request.form.get('isTheater'))
            if request.form.get('isTheater') != None:
                # 識別ラベルと各ラベル番号に対応する名前
                CHARA_NAMES = json.load(open("./chara_52.json", encoding="utf-8"))
                result = pic_eval.evaluation(img_path, './imas_model_52.ckpt', CHARA_NAMES, True)
            else:
                # 識別ラベルと各ラベル番号に対応する名前
                CHARA_NAMES = json.load(open("./chara.json", encoding="utf-8"))
                result = pic_eval.evaluation(img_path, './imas_model.ckpt', CHARA_NAMES, False)
    if result == None:
        return index(True)
    else:
        is765 = False
        rect = [[],[],[],[]]
        for chara in result:
            rect[0].append(chara['x'])
            rect[1].append(chara['y'])
            rect[2].append(chara['width'])
            rect[3].append(chara['height'])
            #if chara['rank'][0]['label'] != OTHER:
            if chara['rank'][0]['rate'] >= 70:
                is765 = True
        timestamp = int(datetime.now().timestamp())
        img_path += "?time={}".format(timestamp)
        return render_template('index.html', img_path=img_path[1:], rect=rect, result=result, is765=is765)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')