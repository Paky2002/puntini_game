from flask import Flask, send_file, redirect, render_template, request, flash, jsonify
from sqlalchemy import Table, Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import pandas as pd

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caf2.sqlite3'

db = SQLAlchemy(app) # CREO OGGETTO PER I DB

class Partita (db.Model) :
    __tablename__ = "partita"
    id = db.Column('id_partita', db.Integer(), primary_key=True, autoincrement=True, unique=True)
    distanza = db.Column(db.Integer)
    tempo = db.Column(db.String(100))

class Punti (db.Model) :
    __tablename__ = "punti"
    id = db.Column('id_punto', db.Integer(), primary_key=True, autoincrement=True, unique=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    configurazione = db.Column(db.Integer)

db.create_all() 

admin = Admin (app) #CREO IL MIO PANNELLO ADMIN BACKEND
    
admin.add_view (ModelView(Partita, db.session)) #AGGIUNGO DI VEDERE IL DB USER
admin.add_view (ModelView(Punti, db.session)) #AGGIUNGO DI VEDERE IL DB USER

@app.route ('/salva_dati' , methods = ['POST'])
def salva () :
    distanza = request.form ['distanza']
    tempo = request.form ['tempo']

    nuova_partita = Partita (
        distanza = distanza,
        tempo = tempo
    )

    db.session.add (nuova_partita)
    db.session.commit()

    return 'Tutto funziona', 200

@app.route ('/gioco')
def gioco () :
    punti = Punti.query.filter_by (configurazione = 1)
    return render_template ('unisci_i_punti.html', punti = punti)

@app.route ('/load_csv')
def load_csv () :
    df = pd.read_excel('20_punti_4.xlsx')
    nuovi_punti = list ()
    for row in df.itertuples():
        nuovi_punti.append (Punti (
            x = row[2],
            y = row[3],
            configurazione = 1 
        ))
    
    db.session.add_all(nuovi_punti)
    db.session.commit ()
    return '<p>'+df.to_string()+'</p>'

    