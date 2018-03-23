import os
import json
import uuid
from flask import Flask, render_template, request
import pic_eval

OTHER = 13
# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.config['DEBUG'] = True
# 投稿画像の保存先
UPLOAD_FOLDER = './static/images/upload/'
# 識別ラベルと各ラベル番号に対応する名前
CHARA_NAMES = json.load(open("./chara.json", encoding="utf-8"))

# ルーティング。/にアクセス時
@app.route('/')
def index():
    return render_template('index.html')

# 画像投稿時のアクション
@app.route('/detect', methods=['POST'])
def post():
    result = None
    if not request.files['file'].filename == '':
        # アップロードされたファイルを保存
        f = request.files['file']
        if f.filename.split('.')[-1] in ['png', 'jpg']:
            filename = str(uuid.uuid4()) + "." + f.filename.split('.')[-1]
            img_path = UPLOAD_FOLDER + filename
            f.save(img_path)
            # pic_eval.pyへアップロードされた画像を渡す
            result = pic_eval.evaluation(img_path, './imas_model.ckpt')
    if result == None:
        return render_template('index.html', error=True)
    else:
        isAS = False
        rect = [[],[],[],[]]
        for chara in result:
            rect[0].append(chara['x'])
            rect[1].append(chara['y'])
            rect[2].append(chara['width'])
            rect[3].append(chara['height'])
            #if chara['rank'][0]['label'] != OTHER:
            if chara['rank'][0]['rate'] >= 90:
                isAS = True
        return render_template('index.html', img_path=img_path[1:], rect=rect, result=result, isAS=isAS)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')