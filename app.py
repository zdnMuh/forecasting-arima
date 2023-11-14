from flask import Flask, render_template, redirect, url_for, request
from dbConf import db, dataTrain, dataTest, dataResult
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Cupborneo@localhost/db_goto'
db.init_app(app)
app.config['SECRET_KEY'] = 'kunci_rahasia'

# class MyForm(FlaskForm):
#     name = StringField('Nama')
#     submit = SubmitField('Submit')

@app.route('/dashboard/')
def dashboard():  # put application's code here
    hitung1 = dataTrain.query.count()
    hitung2 = dataTest.query.count()
    return render_template("/home/index.html", hitung1=hitung1, hitung2=hitung2)

@app.route('/train/', methods=['GET', 'POST'])
def train():  # put application's code here
    if request.method == 'POST':
        # Mendapatkan data dari tabel Train
        data_train_records = dataTrain.query.all()

        # Mengambil hanya field Date dan Close
        data_test_records = [(record.Date, record.Close) for record in data_train_records]

        # Memasukkan data ke tabel Test
        for date, close in data_test_records:
            formatted_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
            new_data_test = dataTest(Date=formatted_date, Close=close)
            db.session.add(new_data_test)

        db.session.commit()
        return redirect(url_for("test"))
    data = dataTrain.query.all()
    return render_template("/home/dataTrain.html", value=data)

@app.route('/delete_all_train', methods=['POST'])
def delete_all_train():
    if request.method == 'POST':
        dataTrain.query.delete()
        db.session.commit()
        return redirect(url_for('train'))

@app.route('/test/')
def test():  # put application's code here
    data = dataTest.query.all()
    return render_template("/home/dataTest.html", value=data)

@app.route('/delete_all_test', methods=['POST'])
def delete_all_test():
    if request.method == 'POST':
        dataTest.query.delete()
        db.session.commit()
        return redirect(url_for('test'))

@app.route('/result/')
def result():  # put application's code here
    data = dataResult.query.all()
    return render_template("/home/resultForecast.html", value=data)

@app.route('/login')
def login():  # put application's code here
    data = dataTrain.query.all()
    form = MyForm
    return render_template("/accounts/login.html/", form=form)

@app.route('/regis')
def regis():  # put application's code here
    data = dataTrain.query.all()
    return render_template("/home/register.html/")

@app.route('/')
def home():  # put application's code here
    data = dataTrain.query.all()
    return render_template("/home/home.html/")

@app.route('/tesja')
def hello():
    return render_template("home/cob.html")

# def get_title():
#     return request.endpoint.split('.')[-1].capitalize()

if __name__ == '__main__':
    app.run()
