from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_key'

dbdir = 'sqlite:///'+os.path.abspath(os.getcwd()) + '/static/osos.db'
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Osos(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    commonName = db.Column(db.String(100))
    scientificName = db.Column(db.String(100))  
    redList = db.Column(db.String(10))
    link = db.Column(db.String(20))

    def __init__(self, commonName,scientificName,redList,link):
        self.commonName = commonName
        self.scientificName = scientificName
        self.redList = redList
        self.link = link

db.create_all()

data = pd.read_csv('static/data/Osos.csv')
for row in range(data.shape[0]):
    scientificName = data['ScientificName'].iloc[row]
    commonName = data['CommonName'].iloc[row]
    redList = data['IUCNRedListCategory'].iloc[row]
    link = data['Hyperlink'].iloc[row]
    #data['commonName = commonName, scientificName = scientificName, redList = redList, link = link']
    osos = Osos( commonName = commonName, 
    	scientificName = scientificName, redList = redList, 
    	link = link)
    db.session.add(osos)
    db.session.commit()
cols = ['ScientificName','CommonName','IUCNRedListCategory','Hyperlink']
