from flask_sqlalchemy import SQLAlchemy

# database
db = SQLAlchemy()

class dataTrain(db.Model):
    __tablename__ = 'gotojk'
    Date = db.Column(db.Date, primary_key=True)
    Open = db.Column(db.Float)
    High = db.Column(db.Float)
    Low = db.Column(db.Float)
    Close = db.Column(db.Float)
    Adj = db.Column(db.Float)
    Volume = db.Column(db.Float)
    # Definisikan kolom lain sesuai dengan struktur tabel

class dataTest(db.Model):
    __tablename__ = 'datatest'
    Date = db.Column(db.Date, primary_key=True)
    Close = db.Column(db.Float)

class dataResult(db.Model):
    __tablename__ = 'result'
    Date = db.Column(db.Date, primary_key=True)
    Close = db.Column(db.Float)