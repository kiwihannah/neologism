# 기본 db 크롤링

from flask import Flask
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.words

import requests
from bs4 import BeautifulSoup

# 요청을 막아둔 사이트들이 많음. 브라우저에서 엔터친것처럼 효과를 내줌
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%9D%B8%ED%84%B0%EB%84%B7_%EC%8B%A0%EC%A1%B0%EC%96%B4_%EB%AA%A9%EB%A1%9D',headers=headers)

# beautiful soup 형태로 만들기
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#mw-content-text > div.mw-parser-output > ul')

# 테스트 db 삽입
for tr in trs:
    a_tags = tr.select('li')
    for a_tag in a_tags:
        if a_tag is not None:
            word = a_tag.text.split(':')[0]
            definition = a_tag.text.split(':')[1]
            print(f'word: {word}, definition: {definition}')

            doc = {
                'word': word,
                'definition': definition,
                'ins_date': 'wiki',
                'upd_date': 'wiki'
            }

            db.neologism.insert_one(doc)
