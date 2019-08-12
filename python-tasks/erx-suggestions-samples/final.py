import atexit
import datetime
import pandas as pd
import psycopg2 as psycopg2
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import logging

# logging configuration

logger = logging.getLogger("Erx-Suggestions")
handler = logging.FileHandler('erxSuggestions.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# configuration for converting an application into flask application
app = Flask(__name__)

# command for enabling CORS
cors = CORS(app, resources={r"*": {"origins": "*"}})

next_date = datetime.date.today()


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


def get_drug_type_from_id(doctors):
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    main_query = "SELECT drug_brand_id, drug_id, drug_type_id, created_usr_id FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorlist)s"
    sql_parameters = {'doctorlist': tuple(doctors)}
    cursor.execute(main_query, sql_parameters)
    rows = cursor.fetchall()
    dft = pd.DataFrame(rows)
    dft.columns = rows[0].keys()
    # print(dft)
    all_drug_ids = dft.groupby(['drug_id'])['drug_type_id'].value_counts()
    top_drug_ids = all_drug_ids.groupby(['drug_id']).head(3)
    print(top_drug_ids)
    drug_types = [key[1] for key, value in top_drug_ids.iteritems()]
    drug_types = list(dict.fromkeys(drug_types))
    conn = connect_dev()
    # cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    query = "SELECT drug_type_id, drug_type_nm FROM public.drug_type_ref where drug_type_id in %(type)s"
    sql_parameters = {'type': tuple(drug_types)}
    cursor.execute(query, sql_parameters)
    df = pd.DataFrame(cursor.fetchall(), columns=['drug_type_id', 'drug_type_nm'])


def get_drugs_strength_route_details(doctors):
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    main_query = "SELECT drug_type_id, drug_route_id, created_usr_id, dose_id FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorslist)s"
    sql_parameters = {'doctorslist': tuple(doctors)}
    cursor.execute(main_query, sql_parameters)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()
    all_drug_dose_filter = df.groupby(['drug_type_id'])['dose_id'].value_counts()
    top3_drug_dose= all_drug_dose_filter.groupby(['drug_type_id']).head(3)
    print(pd.DataFrame([top3_drug_dose]))
    dose_types = [key[1] for key, value in top3_drug_dose.iteritems()]
    dose_types = list(dict.fromkeys(dose_types))
    # print(dose_types)
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    first_query = "SELECT dose_id, dose_nm FROM public.drug_dose_ref where dose_id in %(type)s"
    sql_parameters = {'type': tuple(dose_types)}
    cursor.execute(first_query, sql_parameters)
    rows = cursor.fetchall()
    # print("doses",rows)

    all_drug_route_filter = df.groupby(['drug_type_id'])['drug_route_id'].value_counts()
    top3_drug_routes= all_drug_route_filter.groupby(['drug_type_id']).head(3)
    # print(top3_drug_routes)
    route_ids = [key[1] for key, value in top3_drug_routes.iteritems()]
    route_ids = list(dict.fromkeys(route_ids))
    # print(k)
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    second_query = "SELECT drug_route_id, drug_route_nm FROM public.drug_route_ref where drug_route_id in %(type)s"
    sql_parameters = {'type': tuple(route_ids)}
    cursor.execute(second_query, sql_parameters)
    row = cursor.fetchall()
    print("routes", row)


def get_drug_frequency_from_strength(doctors):
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    main_query = "SELECT drug_frequency_id, created_usr_id, dose_id FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorslist)s"
    sql_parameters = {'doctorslist': tuple(doctors)}
    cursor.execute(main_query, sql_parameters)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()

    all_drug_frequency_filter = df.groupby(['dose_id'])['drug_frequency_id'].value_counts()
    top3_drug_frequency = all_drug_frequency_filter.groupby('dose_id').head(3)
    # print(top3_drug_frequency)
    frequency_ids = [key[1] for key, value in top3_drug_frequency.iteritems()]
    frequency_ids = list(dict.fromkeys(frequency_ids))

    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT drug_frequency_id, drug_frequency_nm FROM public.drug_frequency_ref where drug_frequency_id in %(type)s"
    sql_parameters = {'type': tuple(frequency_ids)}
    cursor.execute(query, sql_parameters)
    rows = cursor.fetchall()
    print("frequency", rows)


def get_instructions_from_drug_id(doctors):
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    main_query = "SELECT drug_id, instruction, created_usr_id  FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorslist)s"
    sql_parameters = {'doctorslist': tuple(doctors)}
    cursor.execute(main_query, sql_parameters)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()

    # getting top 3 instructions for each drug_id
    all_instructions = df.groupby(['drug_id'])['instruction'].value_counts()
    top_instructions = all_instructions.groupby(['drug_id']).head(3)
    print("instructions", top_instructions)

    # # insert the top results
    # values = ','.join(cursor.mogrify("(%s,%s)", x).decode('utf-8') for x, y in top_instructions.iteritems())
    # print(values)
    # conn_loc = connect_local()
    # cursor_loc = conn_loc.cursor()
    # cursor_loc.execute("INSERT INTO test (drug_id, instructions) VALUES " + values)
    # conn_loc.commit()


# it invoke all above data building functions with doctor list
def build_data(doctors):
    get_drug_type_from_id(doctors)
   # get_drug_frequency_from_strength(doctors)
   # get_drugs_strength_route_details(doctors)
   # get_instructions_from_drug_id(doctors)


# get_instructions_from_drug_id()
def scheduler_example():
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"), "1min")
    global next_date
    today_date = datetime.date.today()
    conn = connect_dev()
    # today_date = datetime.date(2019, 5, 30)
    # for employees having data less than one month
    query_to_fetch_doctor_list_for_one_month = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm >= CURRENT_DATE -INTERVAL '1MONTH'"
    cursor_one = conn.cursor()
    cursor_one.execute(query_to_fetch_doctor_list_for_one_month)
    rows = cursor_one.fetchall()
    doctor_list_one = [row[0] for row in rows]
    print("one", doctor_list_one)
    build_data(doctor_list_one)
    # for employees having data more than one month and less than 6 months
    if today_date.day == 12:
        query_to_fetch_doctor_list_for_six_months = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '6 MONTHS' and CURRENT_DATE -INTERVAL '1MONTH'"
        cursor_six = conn.cursor()
        cursor_six.execute(query_to_fetch_doctor_list_for_six_months)
        rows = cursor_six.fetchall()
        doctor_list_six = [row[0] for row in rows]
        print("six", doctor_list_six)
        build_data(doctor_list_six)
    # for employees having data more than  6 months and less than one year
    if today_date == datetime.date(2019, 5, 30):
        query_to_fetch_doctor_list_for_one_year = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '12 MONTHS' and CURRENT_DATE -INTERVAL '6 MONTHs'"
        cursor_one_year = conn.cursor()
        cursor_one_year.execute(query_to_fetch_doctor_list_for_one_year)
        rows = cursor_one_year.fetchall()
        doctor_list_one_year = [row[0] for row in rows]
        print("one year", doctor_list_one_year)
        build_data(doctor_list_one_year)
        # this is to configure the next date for data processing
        if next_date.month in [3, 5, 6, 7, 8, 10, 11]:
            next_date = next_date + datetime.timedelta(days=92)
        elif next_date.month in [4, 9]:
            next_date = next_date + datetime.timedelta(days=91)
        elif next_date.month in [12, 1]:
            if next_date.year/4 == 0:
                next_date = next_date + datetime.timedelta(days=91)
            if next_date.year/4 != 0:
                next_date = next_date + datetime.timedelta(days=90)
        elif next_date.month is 2:
            if next_date.year%4 == 0:
                next_date = next_date + datetime.timedelta(days=90)
            if next_date.year%4 != 0:
                next_date = next_date + datetime.timedelta(days=89)
    # for employees having data more than one year
    if today_date == datetime.date(2019, 4, 29):
        print("6 months")


# it terminate the scheduler during application shutdown
def close_all():
    scheduler.shutdown()
    print("stopped")


if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon='True')
    # The job will be executed on November 6th, 2009
    # scheduler.add_job(scheduler_example,  'interval', days=1, start_date='2019-04-27 00:00:00')
    scheduler.add_job(scheduler_example, 'interval', seconds=2)
    scheduler.start()
    atexit.register(close_all)
    app.run()

