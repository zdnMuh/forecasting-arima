from flask import Flask, render_template, redirect, url_for, request
from dbConf import db, dataTrain, dataTest, dataResult
from datetime import datetime
from forms import uploadForm
import pandas as pd
# from arima import forecastArima
from forecast import forecastArima, calculateError
from tesjani import ambil
from scrape import saveScrape

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Cupborneo@localhost/db_goto'
db.init_app(app)

app.config['SECRET_KEY'] = 'kunci_rahasia'

@app.route('/dashboard/')
def dashboard():  # put application's code here
    hitung1 = dataTrain.query.count()
    hitung2 = dataTest.query.count()
    return render_template("/home/index.html", hitung1=hitung1, hitung2=hitung2)

@app.route('/train/', methods=['GET', 'POST'])
def train():  # put application's code here
    if request.method == 'POST':
        # Mendapatkan data dari tabel Train
        dataTrainRecords = dataTrain.query.all()

        # Mengambil hanya field Date dan Close
        dataTestRecords = [(record.Date, record.Close) for record in dataTrainRecords]

        # Memasukkan data ke tabel Test
        for date, close in dataTestRecords:
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
            newDataTest = dataTest(Date=formatted_date, Close=close)
            db.session.add(newDataTest)

        db.session.commit()
        return redirect(url_for("test"))
    data = dataTrain.query.all()
    return render_template("/home/dataTrain.html", value=data)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    form = uploadForm()

    if form.validate_on_submit():
        csv_file = form.csv_file.data
        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            train_data = dataTrain(
                Date=row['Date'],
                Open=row['Open'],
                High=row['High'],
                Low=row['Low'],
                Close=row['Close'],
                Adj=row['Adj Close'],
                Volume=row['Volume']
            )
            db.session.add(train_data)

        db.session.commit()
        return redirect(url_for('train'))

    return render_template('/home/upload.html', title='Upload', form=form)

@app.route('/deleteAllTrain/', methods=['POST'])
def deleteAllTrain():
    if request.method == 'POST':
        dataTrain.query.delete()
        db.session.commit()
        return redirect(url_for('train'))

@app.route('/test/', methods=['GET', 'POST'])
def test():
    data = dataTest.query.all()
    if request.method == 'POST':
        forecastArima()
        return redirect(url_for('result'))

    return render_template("/home/dataTest.html", value=data)

@app.route('/deleteAllTest', methods=['POST'])
def deleteAllTest():
    if request.method == 'POST':
        dataTest.query.delete()
        db.session.commit()
        return redirect(url_for('test'))

@app.route('/result/')
def result():  # put application's code here
    data = dataResult.query.all()
    dates = [result.Date.strftime('%Y-%m-%d') for result in data]
    close = [result.Close for result in data]
    result = [result.Result for result in data]
    rmse = calculateError()
    return render_template("home/resultForecast.html", value=data, dates=dates, close=close, result=result, rmse=rmse)

@app.route('/deleteAllResult/', methods=['POST'])
def deleteAllResult():
    if request.method == 'POST':
        dataResult.query.delete()
        db.session.commit()
        return redirect(url_for('result'))

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

@app.route('/scrape/', methods=['POST', 'GET'])
def scraping():
    if request.method == 'POST':
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        saveScrape(symbol=symbol, startDate=start_date, endDate=end_date)

        return redirect(url_for('train'))

    return render_template('/home/scrapeForm.html')

@app.route('/tesja/')
def hello():
    data = ambil()
    return data

# def get_title():
#     return request.endpoint.split('.')[-1].capitalize()

if __name__ == '__main__':
    app.run()
