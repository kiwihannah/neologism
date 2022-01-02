import datetime

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

#
# for person in same_ages:
#     print(person)
#
# user = db.users.find_one({'name':'bobby'}) # Select * user where name = 'bobby'
# print(user)
#
# #3. update
# db.users.update_one({'name':'bobby'},{'$set':{'age':19}})
# db.users.update_many({'name':'Hannah'},{'$set':{'age':20}}) # update all
#
# #4. delete
# db.users.delete_one({'name':'bobby'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)