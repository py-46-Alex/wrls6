import requests

import atexit
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask.views import MethodView
from servr import get_user


engine = create_engine('postgresql://appadmin:1234@127.0.0.1:5431/appdb')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
# -------------------------------------------------------------
print("создать обьявлние")
data = requests.post('http://127.0.0.1:5000/adv/',
                     json={'head_adv': 'продам тумбурет',
                           'text_of_adv': 'большой тумбурет 4 ноги',
                           'autor': 'npoDaBaH_табуретаф'
                           })

print(data.status_code)
print(data.text)
# -------------------------------------------------------------
print("создать обьявлние")
data = requests.post('http://127.0.0.1:5000/adv/',
                     json={'head_adv': 'продам шкафф',
                           'text_of_adv': 'большой шкаф без скелетов продаю',
                           'autor': 'npoDaBaH3'
                           })

print(data.status_code)
print(data.text)
# -------------------------------------------------------------
print("просмотр  обьявлния")
data = requests.get('http://127.0.0.1:5000/adv/2/')
print(data.status_code)
print(data.text)
# -------------------------------------------------------------
print("удалить  обьявлние")
data = requests.delete('http://127.0.0.1:5000/adv/1/')
print(data.status_code)
print(data.text)
# -------------------------------------------------------------

