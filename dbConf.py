from flask_sqlalchemy import SQLAlchemy

# database
db = SQLAlchemy()

class dataTrain(db.Model):
    __tablename__ = 'gotojk'
    Date = db.Column(db.Date, primary_key=True)
    Open = db.Column(db.Integer)
    High = db.Column(db.Integer)
    Low = db.Column(db.Integer)
    Close = db.Column(db.Integer)
    Adj = db.Column(db.Integer)
    Volume = db.Column(db.Integer)
    # Definisikan kolom lain sesuai dengan struktur tabel

class dataTest(db.Model):
    __tablename__ = 'datatest'
    Date = db.Column(db.Date, primary_key=True)
    Close = db.Column(db.Integer)