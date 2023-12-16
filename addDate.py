from datetime import datetime, timedelta
from dbConf import db, dataTest, dataTrain

def add_last_3_days_to_data_test():
    # Mendapatkan tanggal terakhir dari dataTest
    last_date_entry = dataTest.query.order_by(dataTest.Date.desc()).first()
    if last_date_entry:
        last_date = last_date_entry.Date
    else:
        last_date = datetime(2022, 1, 1)  # Atur tanggal awal jika tabel kosong

    # Tambahkan 3 data terakhir dari tanggal terakhir
    for i in range(1, 4):
        new_date = last_date + timedelta(days=i)
        new_data_test = dataTest(Date=new_date, Close=0.0)  # Gantilah nilai Close sesuai kebutuhan
        db.session.add(new_data_test)

    db.session.commit()