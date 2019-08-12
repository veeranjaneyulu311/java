import atexit
import datetime
import logging
import os
import time
import traceback
import uuid
import pandas as pd
import psycopg2 as psycopg2
from psycopg2 import pool
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify


app = Flask(__name__)

# The below line handles the CORS issue
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.secret_key = "804E939A466D43538E9EFF67A479696C"
response_token = 0
next_date = datetime.date.today()
started = True
top_results_for_each_user = {}


# logging configuration
logger = logging.getLogger("erx-top-suggestions")
handler = logging.FileHandler('erx-suggestions.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    logger.info("Error while connecting to PostgreSQL", error)


# This function creates a {key, value} for each created user id to store the results
def create_user_id_if_not_exist(store_results_in_dict, user_id):
    # checks user id exists
    if user_id in store_results_in_dict:
        return store_results_in_dict
    else:
        store_results_in_dict[user_id] = {'id-type': {}, 'id-instructions': {}, 'type-route': {}, 'type-strength': {}, 'dose-frequency': {}, 'type-strength': {}}
        return store_results_in_dict


# This function obtains top three drug types for each created user id based on drug id's
def get_drug_type_from_id(doctors, conn):
    global top_results_for_each_user
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    fetch_drug_trans = "SELECT created_usr_id, drug_id, drug_type_id FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorlist)s"
    sql_parameters = {'doctorlist': tuple(doctors)}
    cursor.execute(fetch_drug_trans, sql_parameters)
    rows = cursor.fetchall()
    # It forms data frame for above fetched transaction data
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()
    all_drug_types = df.groupby(['created_usr_id', 'drug_id'])['drug_type_id'].value_counts()
    top3_drug_types = all_drug_types.groupby(['created_usr_id', 'drug_id']).head(3)
    # The below lines store obtained top drug types into result dictionary
    top3_drug_types_as_list = [label for label, value in top3_drug_types.iteritems()]
    as_data_frame = pd.DataFrame(top3_drug_types_as_list, columns=['created_usr_id', 'drug_id', 'drug_type_id'])
    df = dict(as_data_frame.groupby(['created_usr_id', 'drug_id'])['drug_type_id'].apply(list))
    for label, val in df.items():
        created_user_id, drug_id = label
        create_user_id_if_not_exist(top_results_for_each_user, created_user_id)
        top_results_for_each_user[created_user_id]['id-type'][drug_id] = val


# This function obtains top three strengths and routes for each created user id based on drug types
def get_drugs_strength_route_details(doctors, conn):
    global top_results_for_each_user
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    fetch_drug_trans = "SELECT created_usr_id, drug_type_id, dose_id, drug_route_id FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorlist)s"
    sql_parameters = {'doctorlist': tuple(doctors)}
    cursor.execute(fetch_drug_trans, sql_parameters)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()

    # To get top three doses
    all_drug_doses = df.groupby(['created_usr_id', 'drug_type_id'])['dose_id'].value_counts()
    top3_drug_doses = all_drug_doses.groupby(['drug_type_id']).head(3)
    # The below lines store obtained top doses into result dictionary
    top3_drug_doses_as_list = [label for label, value in top3_drug_doses.iteritems()]
    as_data_frame = pd.DataFrame(top3_drug_doses_as_list, columns=['created_usr_id', 'drug_type_id', 'dose_id'])
    as_dict = dict(as_data_frame.groupby(['created_usr_id', 'drug_type_id'])['dose_id'].apply(list))
    for label, val in as_dict.items():
        created_user_id, drug_type_id = label
        create_user_id_if_not_exist(top_results_for_each_user, created_user_id)
        top_results_for_each_user[created_user_id]['type-strength'][drug_type_id] = val

    # To get top three routes
    all_drug_routes = df.groupby(['created_usr_id', 'drug_type_id'])['drug_route_id'].value_counts()
    top3_drug_routes = all_drug_routes.groupby(['drug_type_id']).head(3)
    # The below lines store obtained top strengths into result dictionary
    top3_drug_routes_as_list = [label for label, value in top3_drug_routes.iteritems()]
    as_data_frame = pd.DataFrame(top3_drug_routes_as_list, columns=['created_usr_id', 'drug_type_id', 'drug_route_id'])
    as_dict = dict(as_data_frame.groupby(['created_usr_id', 'drug_type_id'])['drug_route_id'].apply(list))
    for label, val in as_dict.items():
        created_user_id, drug_type_id = label
        create_user_id_if_not_exist(top_results_for_each_user, created_user_id)
        top_results_for_each_user[created_user_id]['type-route'][drug_type_id] = val


# This function obtains top three frequencies for each created user id based on strengths
def get_drug_frequency_from_strength(doctors, conn):
    global top_results_for_each_user
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    fetch_drug_trans = "SELECT created_usr_id, dose_id, drug_frequency_id  FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorlist)s"
    sql_parameters = {'doctorlist': tuple(doctors)}
    cursor.execute(fetch_drug_trans, sql_parameters)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()
    all_drug_frequencies = df.groupby(['created_usr_id', 'dose_id'])['drug_frequency_id'].value_counts()
    top3_drug_frequencies = all_drug_frequencies.groupby('dose_id').head(3)
    top3_drug_frequencies_as_list = [label for label, value in top3_drug_frequencies.iteritems()]
    as_data_frame = pd.DataFrame(top3_drug_frequencies_as_list, columns=['created_usr_id', 'dose_id', 'drug_frequency_id'])
    as_dict = dict(as_data_frame.groupby(['created_usr_id', 'dose_id'])['drug_frequency_id'].apply(list))
    for label, val in as_dict.items():
        created_user_id, dose_id = label
        create_user_id_if_not_exist(top_results_for_each_user, created_user_id)
        top_results_for_each_user[created_user_id]['dose-frequency'][dose_id] = val


# This function obtains top three instructions for each created user id based on drug id's
def get_instructions_from_drug_id(doctors, conn):
    global top_results_for_each_user
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    fetch_drug_trans = "SELECT created_usr_id, drug_id, instruction FROM opd.patient_prescription_drugs_trans where created_usr_id in %(doctorlist)s"
    sql_parameters = {'doctorlist': tuple(doctors)}
    cursor.execute(fetch_drug_trans, sql_parameters)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = rows[0].keys()

    all_drug_instructions = df.groupby(['created_usr_id', 'drug_id'])['instruction'].value_counts()
    top3_drug_instructions = all_drug_instructions.groupby(['drug_id']).head(3)
    top3_drug_instructions_as_list = [label for label, value in top3_drug_instructions.iteritems()]
    as_data_frame = pd.DataFrame(top3_drug_instructions_as_list, columns=['created_usr_id', 'drug_id', 'instruction'])
    as_dict = dict(as_data_frame.groupby(['created_usr_id', 'drug_id'])['instruction'].apply(list))
    for label, val in as_dict.items():
        created_user_id, drug_id = label
        create_user_id_if_not_exist(top_results_for_each_user, created_user_id)
        top_results_for_each_user[created_user_id]['id-instructions'][drug_id] = val
    # print(top_results_for_each_user)


# it invokes all above data building functions with doctors list for the time periods one month, < 6 months and < 1 year
def build_data(doctors, conn):
    get_drug_type_from_id(doctors, conn)
    get_drug_frequency_from_strength(doctors, conn)
    get_drugs_strength_route_details(doctors, conn)
    get_instructions_from_drug_id(doctors, conn)


# This Function gets executed on every day by the scheduler.
def data_build_scheduler():
    global next_date
    global started
    # get today's date
    # print(datetime.datetime.now().time())
    today_date = datetime.date.today()
    conn = threaded_postgreSQL_pool.getconn()
    # today_date = datetime.date(2019, 5, 30)

    # for fetching employees having data less than one month
    query_to_fetch_doctor_list_for_one_month = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm >= CURRENT_DATE -INTERVAL '1MONTH'"
    cursor_one = conn.cursor()
    cursor_one.execute(query_to_fetch_doctor_list_for_one_month)
    rows = cursor_one.fetchall()
    doctor_list_one = [row[0] for row in rows]
    logger.info("SCHEDULER: EXECUTED FOR EMPLOYEES LESS THAN ONE MONTH ---" + str(datetime.datetime.now()))
    build_data(doctor_list_one, conn)

    # for fetching employees having data more than one month and less than 6 months
    if today_date.day == 3 or started:
        query_to_fetch_doctor_list_for_six_months = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '6 MONTHS' and CURRENT_DATE -INTERVAL '1MONTH'"
        cursor_six = conn.cursor()
        cursor_six.execute(query_to_fetch_doctor_list_for_six_months)
        rows = cursor_six.fetchall()
        doctor_list_six = [row[0] for row in rows]
        logger.info("SCHEDULER: EXECUTED FOR EMPLOYEES MORE THAN ONE MONTH AND LESS THAN SIX MONTHS ---" + str(datetime.datetime.now()))
        build_data(doctor_list_six, conn)
    # for employees having data more than  6 months and less than one year
    if today_date == next_date or started:
        query_to_fetch_doctor_list_for_one_year = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '12 MONTHS' and CURRENT_DATE -INTERVAL '6 MONTHs'"
        cursor_one_year = conn.cursor()
        cursor_one_year.execute(query_to_fetch_doctor_list_for_one_year)
        rows = cursor_one_year.fetchall()
        doctor_list_one_year = [row[0] for row in rows]
        logger.info("SCHEDULER: EXECUTED FOR EMPLOYEES MORE THAN SIX MONTHS AND LESS THAN ONE YEAR ---" + str(datetime.datetime.now()))
        build_data(doctor_list_one_year, conn)
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
    threaded_postgreSQL_pool.putconn(conn)
    started = False


# It returns the computer name from environment variables. otherwise Unknown Computer. It is for logging purpose
def get_computer_name():
        if os.getenv('HOSTNAME') is not None:
                return os.getenv('HOSTNAME')
        elif os.getenv('COMPUTERNAME') is not None:
                return os.getenv('COMPUTERNAME')
        else:
                return 'Unknown Computer'


#: This method log's the every request given
@app.before_request
def start():
        global response_token
        response_token = str(uuid.uuid4()).upper()
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'Erx-Suggestions','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        # condition to check success or not
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'Erx-Suggestions','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response


# This api returns all instructions and drug types for the requested drug id
@app.route('/fetchDrugTypesAndInstructions', methods=['POST'])
def fetch_drug_types_and_instructions_for_drug_id():
    try:
        request_data = request.get_json()
        conn = threaded_postgreSQL_pool.getconn()
        try:
            drug_types = top_results_for_each_user[request_data['authenticated_user_id']]['id-type'][request_data['drug_id']]
            sql_parameters = {'drug_types': tuple(drug_types)}
            query_to_fetch_drug_type_names = "SELECT drug_type_id, drug_type_nm FROM public.drug_type_ref where drug_type_id in %(drug_types)s"
            cursor_one = conn.cursor()
            cursor_one.execute(query_to_fetch_drug_type_names, sql_parameters)
            rows = cursor_one.fetchall()
            data = []
            for row in rows:
                data.append(dict(zip(('drug_type_id', 'drug_type_nm'), row)))
        except KeyError:
            data = []
        try:
            instructions = top_results_for_each_user[request_data['authenticated_user_id']]['id-instructions'][request_data['drug_id']]
        except KeyError:
            instructions = []
        threaded_postgreSQL_pool.putconn(conn)
        return jsonify({'data': {'drug_types': data, 'instructions': instructions}, 'response_code': "E200", 'response_message': "DATA FETCHED SUCCESSFULLY"})
    except Exception:
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'Erx-Suggestions','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_ES001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 500


# This api returns all doses(strengths) and  routes for the requested drug type
@app.route('/fetchDosesAndRoutes', methods=['POST'])
def fetch_doses_and_routes_for_drug_id():
    try:
        request_data = request.get_json()
        conn = threaded_postgreSQL_pool.getconn()
        try:
            route_id = top_results_for_each_user[request_data['authenticated_user_id']]['type-route'][request_data['drug_type']]
            sql_parameters = {'route_ids': tuple(route_id)}
            query_to_fetch_drug_route_names = "SELECT drug_route_id, drug_route_nm FROM public.drug_route_ref where drug_route_id in %(route_ids)s"
            cursor_one = conn.cursor()
            cursor_one.execute(query_to_fetch_drug_route_names, sql_parameters)
            rows = cursor_one.fetchall()
            route = []
            for row in rows:
                route.append(dict(zip(('drug_route_id', 'drug_route_nm'), row)))
        except KeyError:
            route = []
        try:
            strengths = top_results_for_each_user[request_data['authenticated_user_id']]['type-strength'][request_data['drug_type']]
            sql_parameters = {'strengths': tuple(strengths)}
            query_to_fetch_dose_names = "SELECT dose_id, dose_nm FROM public.drug_dose_ref where dose_id in %(strengths)s"
            cursor_one.execute(query_to_fetch_dose_names, sql_parameters)
            rows = cursor_one.fetchall()
            strength = []
            for row in rows:
                strength.append(dict(zip(('dose_id', 'dose_nm'), row)))
        except KeyError:
            strength = []
        threaded_postgreSQL_pool.putconn(conn)
        return jsonify({'data': {'routes': route, 'strengths': strength}, 'response_code': "E200", 'response_message': "DATA FETCHED SUCCESSFULLY"})
    except Exception:
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'Erx-Suggestions','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_ES001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 500


# This api returns all frequencies for the requested dose id
@app.route('/fetchFrequencies', methods=['POST'])
def fetch_drug_frequencies_for_dose():
    try:
        request_data = request.get_json()
        conn = threaded_postgreSQL_pool.getconn()
        try:
            frequencies = top_results_for_each_user[request_data['authenticated_user_id']]['dose-frequency'][request_data['dose_id']]
            sql_parameters = {'frequencies': tuple(frequencies)}
            query_to_fetch_frequency_names = "SELECT drug_frequency_id, drug_frequency_nm FROM public.drug_frequency_ref where drug_frequency_id in %(frequencies)s"
            cursor_one = conn.cursor()
            cursor_one.execute(query_to_fetch_frequency_names, sql_parameters)
            rows = cursor_one.fetchall()
            data = []
            for row in rows:
                data.append(dict(zip(('drug_frequency_id', 'drug_frequency_nm'), row)))
        except KeyError:
            data = []
        threaded_postgreSQL_pool.putconn(conn)
        return jsonify({'data': {'frequencies': data}, 'response_code': "E200", 'response_message': "DATA FETCHED SUCCESSFULLY"})
    except Exception:
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'Erx-Suggestions','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_ES001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 500


# it terminate the scheduler during application shutdown
def close_all():
    scheduler.shutdown()
    logger.info("TERMINATED")


# scheduler configuration
scheduler = BackgroundScheduler(daemon='True')

# The job will be executed on given start date for first time and thereafter it executes for every day
# scheduler.add_job(data_build_scheduler,  'interval', days=1, start_date='2019-07-19 12:02:00')

scheduler.add_job(data_build_scheduler, 'interval', days=1, start_date=str(datetime.datetime.now() + datetime.timedelta(seconds=60)))
scheduler.start()
atexit.register(close_all)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)

