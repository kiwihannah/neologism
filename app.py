from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.words

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/new', methods=['POST'])
def new_words():
    word_receive = request.form['word_give']
    definition_receive = request.form['definition_give']
    time_receive = request.form['time_give']

    doc = {
        'word': word_receive,
        'definition': definition_receive,
        'ins_date': time_receive,
        'upd_date': ''
    }

    db.neologism.insert_one(doc)

    return jsonify({'msg': 'Your word has been saved'})

#2. find
@app.route('/find', methods=['POST'])
def find_words():
    keyword_receive = request.form['keyword_give']
    try:
        result = db.neologism.find_one({'word':keyword_receive})['definition']
    except:
        result = 'no results'
    return jsonify({'msg': result})

#3. update
@app.route('/update', methods=['POST'])
def update_word():
    word_receive = request.form['word_give']
    definition_receive = request.form['definition_give']
    time_receive = request.form['time_give']
    db.neologism.update_one({'word':word_receive},{'$set':{'definition':definition_receive, 'upd_date':time_receive}})

#4. delete
@app.route('/delete', methods=['POST'])
def delete_word():
    word_receive = request.form['word_give']
    db.neologism.delete_one({'word':word_receive})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)