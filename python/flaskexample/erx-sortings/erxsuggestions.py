import atexit
import datetime
import pandas as pd
import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = "804E939A466D43538E9EFF67A479696C"
next_date = datetime.date.today()
top_results_for_each_user = {}


# This function creates and returns database connections
def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


# This function creates a {key, value} for each created user id to store the results
def create_user_id_if_not_exist(store_results_in_dict, user_id):
    # checks user id exists
    if user_id in store_results_in_dict:
        return store_results_in_dict
    else:
        store_results_in_dict[user_id] = {'id-type': {}, 'id-instructions': {}, 'type-route': {}, 'type-strength': {}, 'dose-frequency': {}, 'type-strength': {}}
        return store_results_in_dict


# This function obtains top three drug types for each created user id based on drug id's
def get_drug_type_from_id(doctors):
    global top_results_for_each_user
    conn = connect_dev()
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
def get_drugs_strength_route_details(doctors):
    global top_results_for_each_user
    conn = connect_dev()
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
def get_drug_frequency_from_strength(doctors):
    global top_results_for_each_user
    conn = connect_dev()
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
def get_instructions_from_drug_id(doctors):
    global top_results_for_each_user
    conn = connect_dev()
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
    print(top_results_for_each_user)


# it invokes all above data building functions with doctors list for the time periods one month, < 6 months and < 1 year
def build_data(doctors):
    get_drug_type_from_id(doctors)
    get_drug_frequency_from_strength(doctors)
    get_drugs_strength_route_details(doctors)
    get_instructions_from_drug_id(doctors)


# This Function is executed every day by the scheduler.
def data_build_scheduler():
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
    if today_date.day == 3:
        query_to_fetch_doctor_list_for_six_months = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '6 MONTHS' and CURRENT_DATE -INTERVAL '1MONTH'"
        cursor_six = conn.cursor()
        cursor_six.execute(query_to_fetch_doctor_list_for_six_months)
        rows = cursor_six.fetchall()
        doctor_list_six = [row[0] for row in rows]
        print("six", doctor_list_six)
        build_data(doctor_list_six)
    # for employees having data more than  6 months and less than one year
    if today_date == next_date:
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


# This api returns all instructions and drug types for the requested drug id
@app.route('/fetchDrugTypesAndInstructions', methods=['POST'])
def fetch_drug_types_and_instructions_for_drug_id():
        request_data = request.get_json()
        drug_types = top_results_for_each_user[request_data['authenticatedUserId']]['id-type'][request_data['drugId']]
        conn = connect_dev()
        sql_parameters = {'drugTypes': tuple(drug_types)}
        query_to_fetch_drug_type_names = "SELECT drug_type_id, drug_type_nm FROM public.drug_type_ref where drug_type_id in %(drugTypes)s"
        cursor_one = conn.cursor()
        cursor_one.execute(query_to_fetch_drug_type_names, sql_parameters)
        rows = cursor_one.fetchall()
        data = []
        for row in rows:
            data.append(dict(zip(('drug_type_id', 'drug_type_nm'), row)))
        instructions = top_results_for_each_user[request_data['authenticatedUserId']]['id-instructions'][request_data['drugId']]
        return jsonify({'data': data, 'instructions': instructions})


# This api returns all doses(strengths) and  routes for the requested drug type
@app.route('/fetchDosesAndRoutes', methods=['POST'])
def fetch_doses_and_routes_for_drug_id():
    request_data = request.get_json()
    route_id = top_results_for_each_user[request_data['authenticatedUserId']]['type-route'][request_data['drugType']]
    conn = connect_dev()

    sql_parameters = {'routeIds': tuple(route_id)}
    query_to_fetch_drug_type_names = "SELECT drug_route_id, drug_route_nm FROM public.drug_route_ref where drug_route_id in %(routeIds)s"
    cursor_one = conn.cursor()
    cursor_one.execute(query_to_fetch_drug_type_names, sql_parameters)
    rows = cursor_one.fetchall()
    route = []
    for row in rows:
        route.append(dict(zip(('drug_route_id', 'drug_route_nm'), row)))

    strengths = top_results_for_each_user[request_data['authenticatedUserId']]['type-strength'][request_data['drugType']]
    sql_parameters = {'strengths': tuple(strengths)}
    query_to_fetch_drug_type_names = "SELECT dose_id, dose_nm FROM public.drug_dose_ref where dose_id in %(strengths)s"
    cursor_one.execute(query_to_fetch_drug_type_names, sql_parameters)
    rows = cursor_one.fetchall()
    strength = []
    for row in rows:
        strength.append(dict(zip(('dose_id', 'dose_nm'), row)))
    return jsonify({'routes': route, 'strengths': strength})


# This api returns all frequencies for the requested dose id
@app.route('/fetchFrequencies', methods=['POST'])
def fetch_drug_frequencies_for_dose():
    request_data = request.get_json()
    conn = connect_dev()
    frequencies = top_results_for_each_user[request_data['authenticatedUserId']]['dose-frequency'][request_data['doseId']]
    sql_parameters = {'frequencies': tuple(frequencies)}
    query_to_fetch_drug_type_names = "SELECT drug_frequency_id, drug_frequency_nm FROM public.drug_frequency_ref where drug_frequency_id in %(frequencies)s"
    cursor_one = conn.cursor()
    cursor_one.execute(query_to_fetch_drug_type_names, sql_parameters)
    rows = cursor_one.fetchall()
    data = []
    for row in rows:
        data.append(dict(zip(('drug_frequency_id', 'drug_frequency_nm'), row)))
    return jsonify({'data': data})


# it terminate the scheduler during application shutdown
def close_all():
    scheduler.shutdown()
    print("stopped")


if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon='True')
    # The job will be executed on November 6th, 2009
    # scheduler.add_job(scheduler_example,  'interval', days=1, start_date='2019-04-27 00:00:00')
    scheduler.add_job(data_build_scheduler, 'interval', seconds=60)
    scheduler.start()
    atexit.register(close_all)
    app.run()

