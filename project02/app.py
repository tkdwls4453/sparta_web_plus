from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('52.79.226.1', 27017, username="test", password="test")
db = client.dbsparta_plus_week2

@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.words.find({},{'_id': False}))
    msg = request.args.get('msg')
    return render_template("index.html", words = words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}",headers={"Authorization": "Token 868b9b2ac3e666089546c855ae5672b5b8205645"})
    result = r.json()

    if r.status_code != 200:
        return redirect(url_for('main', msg='Word not found in dictionary; Try another word'))

    status_receive = request.args.get('status_give', 'new')
    return render_template("detail.html", word=keyword, result=result, status = status_receive)



@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive = request.form['word_give']
    definition_receive = request.form['definition_give']

    doc = {
        'word': word_receive,
        'definition': definition_receive
    }
    print(doc)
    db.words.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'{word_receive} 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form['word_give']
    db.words.delete_one({"word":word_receive})
    return jsonify({'result': 'success', 'msg': f'{word_receive} 삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)