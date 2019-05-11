import atexit
import time

from flask import Flask
import pandas as pd
import numpy as np
import sys
import csv
import json
#from collections import Counter
#np.random.seed(0)

#data = pd.DataFrame(np.random.randint(0, 5, size=(250, 7)), columns=['drug_id', 'drug_type_id', 'drug_route_id', 'drug_frequency_id', 'created_usr_id', 'instruction', 'dose_id'])
#df = pd.DataFrame(data)
#df.to_csv('out.csv', header=True, index=False)
import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

app=Flask(__name__)


def scheduler_example():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


'''
def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


def get_drug_type_id():
#    f = pd.read_csv('out.csv')
    conn = connect_dev()
    query = "SELECT  created_usr_id, drug_id, drug_type_id FROM opd.patient_prescription_drugs_trans where created_usr_id=220180111000005 and drug_id=10450"
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    dft = pd.DataFrame(result)
    dft.columns = result[0].keys()
    a = dft.groupby(['created_usr_id','drug_id'])['drug_type_id'].value_counts()
    x = a.groupby(['created_usr_id','drug_id']).head(3)
    l = [key[2] for key, value in x.iteritems()]
    l = list(dict.fromkeys(l))
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT drug_type_id, drug_type_nm, short_code, description, isactive, created_usr_id, created_dttm, drug_id, org_id, org_grp_id FROM public.drug_type_ref where drug_type_id in %(type)s"
    sqlParameters = {'type': tuple(l)}
    cursor.execute(query, (sqlParameters))
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()
    print(df)

'''


@app.route('/schedulePrint', methods=['GET'])
def data_frames():
    return "sucsess"


def close_all():
    scheduler.shutdown()
    print("stopped")


if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scheduler_example, 'interval', minutes=1)
    scheduler.start()
    atexit.register(close_all)
    app.run()
