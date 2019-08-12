<<<<<<< HEAD
import traceback
from threading import Thread

import psycopg2
from flask import Flask, jsonify, request
import pandas as pd
from psycopg2 import pool
from fuzzywuzzy import utils, fuzz, process
from psycopg2.extras import RealDictCursor
=======

from threading import Thread

from flask import Flask, jsonify, request
import pandas as pd
import psycopg2 as pg
from fuzzywuzzy import utils, fuzz, process
from psycopg2.extras import  RealDictCursor
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
from flask_cors import CORS
import logging
import os
import time
import uuid

# logging configuration
logger = logging.getLogger("pharmacyDrugsMatchingLogging")
<<<<<<< HEAD
handler = logging.FileHandler('excel_drugs_matching.log')
=======
handler = logging.FileHandler('drug_matches.log')
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

<<<<<<< HEAD
app = Flask(__name__)

# command for enabling CORS
=======
app= Flask(__name__)

#command for enabling CORS
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
cors = CORS(app, resources={r"*": {"origins": "*"}})

# It stores the UUID for each request
response_token = 0


<<<<<<< HEAD
#: It establishes connection pool with the configured database
try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error:
    logger.info("Error while connecting to PostgreSQL", error)


=======
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
# It returns the computer name from environment variables. otherwise Unknown Computer
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
<<<<<<< HEAD
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'PHARMACY EXCEL UPLOAD','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
=======
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'PHARMACY EXCEL UPLOAD','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response

<<<<<<< HEAD

# it will be used by first api for exact matches
# it will pre process all test names for comparision and reduces comparision time
# it will convert test names to lowercase(Case Insensitivity)
# orders all words of test names in ascending order(Removing Words Order dependency)
=======
#query_for_importing_excel_uploaded_data= "SELECT drug_brand_nm, dose_nm, drug_type_nm, related_nm FROM public.drug_brand_comp_ref"
#query_for_importing_all_drugs_information = "SELECT  drug_brand_nm, dose_nm, drug_type_nm FROM public.drug_brand_ref"
#Function for connecting to the database

#function for connecting to the database
def connect_dev():
    return pg.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


# Function for using to pre-process the data
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
def pre_process(drug_brand_nm):
    ts = utils.full_process(drug_brand_nm, force_ascii=True)
    stop_words=['-','mg','ml','mg/ml']
    tokens = ts.split()
    tokens= [token for token in tokens if not token in stop_words]
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


<<<<<<< HEAD
=======
# response = {"matched":[],"unmatched":[],"notall":[]}
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
# this function gives approximate matches for each unmatched test
def probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process):

    unmatched_brand_name = unmatched_brand_details["drug_brand_nm"]
<<<<<<< HEAD

    unmatched_brand_name_process = pre_process(unmatched_brand_name)
=======

    unmatched_brand_name_process = pre_process(unmatched_brand_name)

    # this function will give list of matches from a data frame to jsonify the result by applying conditions on loinc_system, order_obs, time_aspect
    def response_from_dataframe(df):
        data = None
        df_for_unmatched = df_for_db_drug_brand_details[df_for_db_drug_brand_details.index.isin(df.index)]
        if not df_for_unmatched.empty:
            data = df_for_unmatched.to_dict('records')
        return data

    # this function will check weather a brand is approximately matched or not
    def check_for_matching(brand_details):
        # if 80 <= fuzz.ratio(brand_details['drug_brand_nm'], unmatched_brand_name_process) < 100:
        # it verifies user given brand name fuzzily match with existing
        if (fuzz.ratio(brand_details['drug_brand_nm'], unmatched_brand_name_process) > 80) and (brand_details['drug_brand_nm'] != unmatched_brand_name_process):
            return True
        else:
            return False

    # fetching all exactly matched brands by excluding remaining columns
    df_for_exact_matched_brand = df_for_db_drug_brand_details_process[df_for_db_drug_brand_details_process['drug_brand_nm'] == unmatched_brand_name_process]

    # check matches available for exact
    if df_for_exact_matched_brand.empty:
        # approx match if no exact matches
        df_for_approximately_matched_brands = df_for_db_drug_brand_details_process[df_for_db_drug_brand_details_process.apply(check_for_matching, axis=1)]
        # contains approximately matched brands
        # need to add condition if more than ten records for approximate brands
        if not df_for_approximately_matched_brands.empty:
            # for suggestions
            result = response_from_dataframe(df_for_approximately_matched_brands)
            return result, "unmatched"
        else:
                result = unmatched_brand_details
                return result, "notall"
    else:
            # filtering the data:  it calls a function to exclude user selected columns and apply remaining exactly
            # output 1
        df_for_exact_matched_brand_type = df_for_exact_matched_brand[df_for_exact_matched_brand['drug_type_nm'] == unmatched_brand_details['drug_type_nm']]
        if df_for_exact_matched_brand_type.empty:
            df_for_exact_matched_brand_dose = df_for_exact_matched_brand[
                df_for_exact_matched_brand['dose_nm'] == unmatched_brand_details['dose_nm']]
            if df_for_exact_matched_brand_dose.empty:
                # "type and dose not matched"
                result = response_from_dataframe(df_for_exact_matched_brand)
                return result, "unmatched"
            else:
                #  "type not matched"
                result = response_from_dataframe(df_for_exact_matched_brand)
                return result, "unmatched"
        else:
            df_for_exact_matched_brand_type_dose = df_for_exact_matched_brand_type[
                df_for_exact_matched_brand_type['dose_nm'] == unmatched_brand_details['dose_nm']]
            if df_for_exact_matched_brand_type_dose.empty:
                # "dose not matched"
                result = response_from_dataframe(df_for_exact_matched_brand_type)
                return result, "unmatched"
            else:
                result = unmatched_brand_details
                return result, "matched"


# @app.route('/fetchMatchedAndUnmatchedDrugBrands', methods= ['POST'])
def get_suggestions(request_data, req_url_rule):
    # fetch given unmatched  test details
    response = {"matched": [], "notall": []}

    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_to_fetch_unmatched_brand_details = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm FROM drug_brand_comp_ref"
    cursor.execute(query_to_fetch_unmatched_brand_details)
    df_for_unmatched_brand_details = pd.DataFrame(data=cursor.fetchall(), columns=['drug_brand_comp_id', 'drug_brand_nm', 'dose_nm', 'drug_type_nm'])
    # fetch all the mapped and unmapped table data
    query_for_drugs_in_db = "SELECT drug_brand_nm, dose_nm, drug_type_nm FROM drug_brand_ref "
    cursor.execute(query_for_drugs_in_db)
    df_for_db_drug_brand_details = pd.DataFrame(data=cursor.fetchall(),
                                                columns=['drug_brand_nm', 'dose_nm', 'drug_type_nm'])

    df_for_db_drug_brand_details_process = df_for_db_drug_brand_details.copy()
    df_for_db_drug_brand_details_process['drug_brand_nm'] = df_for_db_drug_brand_details_process['drug_brand_nm'].apply(pre_process)
    start_time = time.time()
    for unmatched_brand_index in df_for_unmatched_brand_details.index:
        unmatched_brand_details = df_for_unmatched_brand_details.loc[unmatched_brand_index].to_dict()
        result, is_matched = probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process)
        if is_matched == "matched":
            response["matched"].append(result)
        elif is_matched == "unmatched":
            # unmatched_brand_details["suggestions"] = result
            suggestions = []
            # print(unmatched_brand_details)
            for brands in result:
                # for inserting user details in suggestion tables
                # brands.update({'brand_id': unmatched_brand_details['drug_brand_comp_id'].item(),
                #                'usr_id': unmatched_brand_details['created_usr_id'].item(),
                #                'org_id': unmatched_brand_details['org_id'].item(),
                #                'org_grp_id': unmatched_brand_details['org_grp_id'].item()})
                brands.update({'brand_id': unmatched_brand_details['drug_brand_comp_id'].item()})
                suggestions.append(tuple(brands.values()))
            # print("----------", len(suggestions))
            values = ','.join(cursor.mogrify("(%s,%s,%s,%s)", x).decode('utf-8') for x in suggestions)
            cursor_save = conn.cursor()
            cursor_save.execute("INSERT INTO drug_brand_suggest_ref (drug_brand_nm,dose_nm,drug_type_nm,drug_brand_comp_id) VALUES " + values)
        elif is_matched == "notall":
            response["notall"].append(result)
    end_time = time.time()
    print(end_time - start_time)
    add_flag_one = "UPDATE public.drug_brand_comp_ref SET is_matched = true WHERE drug_brand_nm in %(matched)s"
    matched = tuple([brand['drug_brand_nm'] for brand in response['matched']])
    sql_parameter = {'matched': matched}
    cursor.execute(add_flag_one, sql_parameter)

    add_flag_two = "UPDATE public.drug_brand_comp_ref SET is_matched = false WHERE drug_brand_nm in %(notall)s"
    notall = tuple([brand['drug_brand_nm'] for brand in response['notall']])
    sql_parameter = {'notall': notall}
    cursor.execute(add_flag_two, sql_parameter)
    conn.commit()
    # return jsonify({"data": response, "responseCode": "E200", "responseMessage": "DATA FETCHED SUCCESSFULLY"})
    print(response)


# This API performs comparision operation by creating a new thread and returns approximate time required for comparision(in minutes)
# for comparing, each brand takes 15 seconds approximately
# required payload {org_id: 1333, org_grp_id: 2775, authenticated_user_id: 220190316000001}
@app.route("/fetchMatchedAndUnmatchedDrugBrands", methods=['POST'])
def fetch_matched_and_unmatched():
    # get the payload from given request
    request_data = request.get_json()
    req_url_rule = request.url_rule

    # Spawn thread to process the data
    thread_for_processing = Thread(target=get_suggestions,
                                   args=(request_data, req_url_rule))
    thread_for_processing.start()
    query_to_fetch_count_of_uploaded_brands = "SELECT count(*) from public.drug_brand_comp_ref where created_usr_id = %(emp_id)s"
    conn = connect_dev()
    cursor = conn.cursor()
    sql_parameters = {"emp_id": request_data['authenticated_user_id']}
    cursor.execute(query_to_fetch_count_of_uploaded_brands, sql_parameters)
    result = cursor.fetchone()[0]
    # time required for completing the comparision in minutes
    time_required = (result*15)/60
    response_for_given_request = [{"time_required": time_required}, 200]
    return jsonify(response_for_given_request[0]), response_for_given_request[1]


# This API is Used For Fetching All The Matched, Unmatched And Completely unmatched Drug Brand Names.
# required payload {"authenticated_user_id":220190316000001}
@app.route("/fetchAllDrugsList", methods=['POST'])
def fetch_all_brands():
    # get the payload from given request
    request_data = request.get_json()
    query_to_fetch_all_brands = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm, is_matched from public.drug_brand_comp_ref where created_usr_id = %(emp_id)s"
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # passing the parameter values into sql query
    sql_parameters = {"emp_id": request_data['authenticated_user_id']}
    cursor.execute(query_to_fetch_all_brands, sql_parameters)
    result = cursor.fetchall()
    return jsonify(result), 200
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0

    # this function will give list of matches from a data frame in order to jsonify the result
    def response_from_dataframe(df):
        data = None
        df_for_unmatched = df_for_db_drug_brand_details[df_for_db_drug_brand_details.index.isin(df.index)]
        if not df_for_unmatched.empty:
            data = df_for_unmatched.to_dict('records')
        return data

<<<<<<< HEAD
    # this function will check weather a brand is approximately matched or not
    def check_for_matching(brand_details):
        # if 80 <= fuzz.ratio(brand_details['drug_brand_nm'], unmatched_brand_name_process) < 100:
        # it verifies user given brand name fuzzily match with existing
        if (fuzz.ratio(brand_details['drug_brand_nm'], unmatched_brand_name_process) > 80) and (brand_details['drug_brand_nm'] != unmatched_brand_name_process):
            return True
        else:
            return False

    # fetching all exactly matched brands by excluding remaining columns
    df_for_exact_matched_brand = df_for_db_drug_brand_details_process[df_for_db_drug_brand_details_process['drug_brand_nm'] == unmatched_brand_name_process]

    # check matches available for exact
    if df_for_exact_matched_brand.empty:
        # approx match if no exact matches
        df_for_approximately_matched_brands = df_for_db_drug_brand_details_process[df_for_db_drug_brand_details_process.apply(check_for_matching, axis=1)]
        # contains approximately matched brands
        # need to add condition if more than ten records for approximate brands
        if not df_for_approximately_matched_brands.empty:
            # for suggestions
            result = response_from_dataframe(df_for_approximately_matched_brands)
            return result, "unmatched"
        else:
                result = unmatched_brand_details
                return result, "notall"
    else:
            # filtering the data:  it calls a function to exclude user selected columns and apply remaining exactly
            # output 1
        df_for_exact_matched_brand_type = df_for_exact_matched_brand[df_for_exact_matched_brand['drug_type_nm'] == unmatched_brand_details['drug_type_nm']]
        if df_for_exact_matched_brand_type.empty:
            df_for_exact_matched_brand_dose = df_for_exact_matched_brand[
                df_for_exact_matched_brand['dose_nm'] == unmatched_brand_details['dose_nm']]
            if df_for_exact_matched_brand_dose.empty:
                # "type and dose not matched"
                result = response_from_dataframe(df_for_exact_matched_brand)
                return result, "unmatched"
            else:
                #  "type not matched"
                result = response_from_dataframe(df_for_exact_matched_brand)
                return result, "unmatched"
        else:
            df_for_exact_matched_brand_type_dose = df_for_exact_matched_brand_type[
                df_for_exact_matched_brand_type['dose_nm'] == unmatched_brand_details['dose_nm']]
            if df_for_exact_matched_brand_type_dose.empty:
                # "dose not matched"
                result = response_from_dataframe(df_for_exact_matched_brand_type)
                return result, "unmatched"
            else:
                result = unmatched_brand_details
                return result, "matched"


def get_suggestions(request_data, req_url_rule, token):
    try:
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUploadProcessThread','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule,
            request_data)
        # fetch given unmatched  test details
        response = {"matched": [], "notall": []}
        conn = threaded_postgreSQL_pool.getconn()
        cursor_one = conn.cursor(cursor_factory=RealDictCursor)

        # updating the flag value that indicates process running
        query_to_update_process_status_flag = "update public.drug_brand_comp_ref set process_status = %(status)s where org_id =%(org_id)s and process_status is null"
        sql_parameter_status_running = {"status": "running", "org_id": request_data["org_id"]}
        cursor_one.execute(query_to_update_process_status_flag, sql_parameter_status_running)
        conn.commit()
        # the below lines will fetch the data from database and convert them into data frames
        # fetch all the brands from temporary table which are uploaded through excel of given organization
        query_to_fetch_unmatched_brand_details = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm, created_usr_id, org_id, org_grp_id FROM drug_brand_comp_ref where org_id =%(org_id)s and process_status =%(status)s"
        cursor_two = conn.cursor(cursor_factory=RealDictCursor)
        sql_parameter_for_unmatched = {"org_id": request_data['org_id'], "status": "running"}
        cursor_two.execute(query_to_fetch_unmatched_brand_details, sql_parameter_for_unmatched)
        df_for_unmatched_brand_details = pd.DataFrame(data=cursor_two.fetchall(), columns=['drug_brand_comp_id', 'drug_brand_nm', 'dose_nm', 'drug_type_nm', 'created_usr_id', 'org_id', 'org_grp_id'])
        # fetch all the mapped and unmapped table data from master table
        query_for_drugs_in_db = "SELECT drug_brand_nm, dose_nm, drug_type_nm FROM drug_brand_ref "
        cursor_two.execute(query_for_drugs_in_db)
        df_for_db_drug_brand_details = pd.DataFrame(data=cursor_two.fetchall(),
                                                    columns=['drug_brand_nm', 'dose_nm', 'drug_type_nm'])

        # below lines will pre process(i.e remove special characters, sorting etc. as mentioned at the pre process function) all the brand names of mater table data
        df_for_db_drug_brand_details_process = df_for_db_drug_brand_details.copy()
        df_for_db_drug_brand_details_process['drug_brand_nm'] = df_for_db_drug_brand_details_process['drug_brand_nm'].apply(pre_process)
        # start_time = time.time()
        # iterating over user uploaded brands to check weather they match with brands available in database
        for unmatched_brand_index in df_for_unmatched_brand_details.index:
            # below field holds user given brand name, dose name, drug type
            unmatched_brand_details = df_for_unmatched_brand_details.loc[unmatched_brand_index].to_dict()
            result, is_matched = probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process)
            # condition to check given brand name exactly matched with any of brand name in database
            if is_matched == "matched":
                response["matched"].append(result)
            # condition to check given brand name  unmatched with any of brand name in database but at least having approximate matches for suggesting
            elif is_matched == "unmatched":
                suggestions = []
                for brands in result:
                    # for inserting user details in suggestion tables
                    brands.update({'brand_id': unmatched_brand_details['drug_brand_comp_id'].item(),
                                   'usr_id': unmatched_brand_details['created_usr_id'].item(),
                                   'org_id': unmatched_brand_details['org_id'].item(),
                                   'org_grp_id': unmatched_brand_details['org_grp_id'].item()})

                    suggestions.append(tuple(brands.values()))
                # print("----------", len(suggestions))
                values = ','.join(cursor_two.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in suggestions)
                cursor_two.execute("INSERT INTO drug_brand_suggest_ref (drug_brand_nm,dose_nm,drug_type_nm,drug_brand_comp_id,created_usr_id,org_id,org_grp_id) VALUES " + values)
            # condition to check given brand name is not matched with any of brand name in database and not having any approximate match
            elif is_matched == "notall":
                response["notall"].append(result)
        # end_time = time.time()
        # the below db calls will update flag (i.e is_matched) column of user uploaded brands table(i.e temporary table) to differentiate matched and completely not brands
        add_flag_one = "UPDATE public.drug_brand_comp_ref SET is_matched = true WHERE drug_brand_nm in %(matched)s and org_id = %(org_id)s"
        matched = tuple([brand['drug_brand_nm'] for brand in response['matched']])
        sql_parameter_matched = {"matched": matched, "org_id": request_data['org_id']}
        cursor_two.execute(add_flag_one, sql_parameter_matched)

        add_flag_two = "UPDATE public.drug_brand_comp_ref SET is_matched = false WHERE drug_brand_nm in %(notall)s and org_id = %(org_id)s"
        notall = tuple([brand['drug_brand_nm'] for brand in response['notall']])
        sql_parameter = {"notall": notall, "org_id": request_data['org_id']}
        cursor_two.execute(add_flag_two, sql_parameter)

        # updating the flag value(i.e process_status column of temporary table) that indicates process completed
        query_to_update_process_status_flag_completed = "update public.drug_brand_comp_ref set process_status = %(status)s where org_id =%(org_id)s and process_status = %(current_status)s"
        sql_parameter_status_completed = {"status": "completed", "org_id": request_data['org_id'], "current_status": "running"}
        cursor_two.execute(query_to_update_process_status_flag_completed, sql_parameter_status_completed)
        conn.commit()
        threaded_postgreSQL_pool.putconn(conn)
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUploadProcessThread','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule,
            request_data)
    except Exception:
        conn.rollback()
        threaded_postgreSQL_pool.putconn(conn)
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUploadProcessThread','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule,
            traceback.format_exc(), request_data)


# This API performs comparision operation by creating a new thread in background and returns approximate time required for comparision(in minutes)
# for comparing, each brand takes 15 seconds approximately
# required payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
@app.route("/fetchMatchedAndUnmatchedDrugBrands", methods=['POST'])
def fetch_matched_and_unmatched():
    try:
        # get the payload from given request
        request_data = request.get_json()
        req_url_rule = request.url_rule

        query_to_fetch_count_of_uploaded_brands = "SELECT count(*) from public.drug_brand_comp_ref where created_usr_id = %(emp_id)s and org_id = %(org_id)s and process_status is null"
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor()
        # passing used parameters into query
        sql_parameters = {"emp_id": request_data['authenticated_user_id'], "org_id": request_data['org_id']}
        cursor.execute(query_to_fetch_count_of_uploaded_brands, sql_parameters)
        result = cursor.fetchone()[0]
        # Spawn thread to process the data
        thread_for_processing = Thread(target=get_suggestions,
                                       args=(request_data, req_url_rule, response_token))
        thread_for_processing.start()

        # time required for completing the comparision in minutes
        time_required = (result*15)/60
        response_for_given_request = {"time_required": time_required}
        threaded_postgreSQL_pool.putconn(conn)
        validations = [{'message': "DATA COMPARISION STARTED SUCCESSFULLY", 'errCode': "RES_CODE_PEU1000"}]
        response = {'data': response_for_given_request, 'responseCode': "E200", 'responseMessage': "DATA COMPARISION STARTED SUCCESSFULLY",
                    'validations': validations}
        return jsonify(response), 200
    except Exception:
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUploadkkkkkk','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 400


# This API checks weather background process completed
# for comparing, each brand takes 15 seconds approximately
# required payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
# reponse {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
@app.route("/checkIsCompareCompleted", methods=['POST'])
def check_is_comparison_completed():
    try:
        # get the payload from given request
        request_data = request.get_json()
        query_to_check_is_running = "SELECT exists (SELECT 1 FROM drug_brand_comp_ref WHERE  process_status = %(status)s and org_id = %(org_id)s LIMIT 1)"
        query_to_check_is_completed = "SELECT exists (SELECT 1 FROM drug_brand_comp_ref WHERE  process_status = %(status)s and org_id = %(org_id)s LIMIT 1)"
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor()
        sql_parameters = {"status": "running", "org_id": request_data['org_id']}
        cursor.execute(query_to_check_is_running, sql_parameters)
        is_running = cursor.fetchone()[0]
        if is_running:
            response_for_given_request = {"time_not_required": False}
        else:
            sql_parameters = {"status": "completed", "org_id": request_data['org_id']}
            cursor.execute(query_to_check_is_completed, sql_parameters)
            is_completed = cursor.fetchone()[0]
            if is_completed:
                response_for_given_request = {"time_not_required": True}
            else:
                response_for_given_request = {"time_not_required": None}
        threaded_postgreSQL_pool.putconn(conn)
        validations = [{'message': "DATA FETCHED SUCCESSFULLY", 'errCode': "RES_CODE_DBC1000"}]
        response = {'data': response_for_given_request, 'responseCode': "E200", 'responseMessage': "DATA FETCHED SUCCESSFULLY",
                    'validations': validations}
        return jsonify(response), 200
    except Exception:
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 500


# This API is Used For Fetching All The Matched, Unmatched And Completely unmatched Drug Brand Names.
# required payload {"org_id":220190316000001}
@app.route("/fetchAllDrugsList", methods=['POST'])
def fetch_all_brands():
    try:
        # get the payload from given request
        request_data = request.get_json()
        query_to_fetch_all_brands = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm, is_matched from public.drug_brand_comp_ref where org_id = %(org_id)s and process_status = %(status)s"
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # passing the parameter values into sql query
        sql_parameters = {"org_id": request_data['org_id'], "status": "completed"}
        cursor.execute(query_to_fetch_all_brands, sql_parameters)
        result = cursor.fetchall()
        threaded_postgreSQL_pool.putconn(conn)
        validations = [{'message': "DATA FETCHED SUCCESSFULLY", 'errCode': "RES_CODE_PEU1000"}]
        response = {'data': result, 'responseCode': "E200", 'responseMessage': "DATA FETCHED SUCCESSFULLY",
                    'validations': validations}
        return jsonify(response), 200
    except Exception:
        conn.rollback()
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 400


=======
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
# This API returns all matched suggestions for given brand_comp_id
# required payload {"drug_brand_comp_id":6724}
@app.route("/fetchSuggestionsForUnmatchedDrugBrands", methods=['POST'])
def fetch_suggestions_for_unmatched():
<<<<<<< HEAD
    try:
        conn = threaded_postgreSQL_pool.getconn()
        # get the payload from given request
        request_data = request.get_json()
        query_to_fetch_suggestions = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm FROM public.drug_brand_suggest_ref where drug_brand_comp_id = %(comp_id)s and org_id = %(org_id)s"
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # passing the parameter values into sql query
        sql_parameters = {'comp_id': request_data['drug_brand_comp_id'], 'org_id': request_data['org_id']}
        cursor.execute(query_to_fetch_suggestions, sql_parameters)
        response = cursor.fetchall()
        threaded_postgreSQL_pool.putconn(conn)
        validations = [{'message': "DATA FETCHED SUCCESSFULLY", 'errCode': "RES_CODE_PEU1000"}]
        response = {'data': response, 'responseCode': "E200", 'responseMessage': "DATA FETCHED SUCCESSFULLY",
                    'validations': validations}
        return jsonify(response), 200
    except Exception:
        conn.rollback()
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE", 'data': ''}
        return jsonify(response), 400
=======
    conn = connect_dev()
    # get the payload from given request
    request_data = request.get_json()
    query_to_fetch_suggestions = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm FROM public.drug_brand_suggest_ref where drug_brand_comp_id = %(comp_id)s"
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # passing the parameter values into sql query
    sql_parameters = {'comp_id': request_data['drug_brand_comp_id']}
    cursor.execute(query_to_fetch_suggestions, sql_parameters)
    response = cursor.fetchall()
    return jsonify(response), 200
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0


# This api will update unmatched brands with user selected brand from provided suggestions
# required payload {
#         "dose_nm": "2 mg",
#         "drug_brand_comp_id": 6724,
#         "drug_brand_nm": "Andial",
#         "drug_type_nm": "Calcimax d-1000",
#         "is_matched": true
#     }
@app.route("/updateUnmatchedBrandWithSelectedBrand", methods=['POST'])
def update_unmatched_brand_with_selected_brand():
<<<<<<< HEAD
    try:
        conn = threaded_postgreSQL_pool.getconn()
        # get the payload from given request
        request_data = request.get_json()
        query_to_update_unmatched_brand_with_selected_brand = "UPDATE public.drug_brand_comp_ref SET drug_brand_nm=%(drug_brand_nm)s, dose_nm=%(dose_nm)s, drug_type_nm=%(drug_type_nm)s, is_matched=%(is_matched)s WHERE drug_brand_comp_id=%(drug_brand_comp_id)s and org_id=%(org_id)s"
        cursor = conn.cursor()
        # passing the parameter values into sql query
        sql_parameters = {'drug_brand_nm': request_data['drug_brand_nm'], 'dose_nm': request_data['dose_nm'],
                          'drug_type_nm': request_data['drug_type_nm'], 'is_matched': request_data['is_matched'],
                          'drug_brand_comp_id': request_data['drug_brand_comp_id'], 'org_id': request_data['org_id']}
        cursor.execute(query_to_update_unmatched_brand_with_selected_brand, sql_parameters)
        conn.commit()
        threaded_postgreSQL_pool.putconn(conn)
        response = {'data': "Records Updated Successfully", 'responseCode': "E200", 'responseMessage': "DATA UPDATED SUCCESSFULLY"}
        return jsonify(response), 200
    except Exception:
        conn.rollback()
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'PharmacyExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule,
            traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE", 'data': ''}
        return jsonify(response), 400


if __name__ == '__main__':
    app.run(host="192.168.2.72", port="8057", debug=True)
=======
    conn = connect_dev()
    # get the payload from given request
    request_data = request.get_json()
    query_to_update_unmatched_brand_with_selected_brand = "UPDATE public.drug_brand_comp_ref SET drug_brand_nm=%(drug_brand_nm)s, dose_nm=%(dose_nm)s, drug_type_nm=%(drug_type_nm)s, is_matched=%(is_matched)s WHERE drug_brand_comp_id=%(drug_brand_comp_id)s"
    cursor = conn.cursor()
    # passing the parameter values into sql query
    sql_parameters = {'drug_brand_nm': request_data['drug_brand_nm'], 'dose_nm': request_data['dose_nm'],
                      'drug_type_nm': request_data['drug_type_nm'], 'is_matched': request_data['is_matched'],
                      'drug_brand_comp_id': request_data['drug_brand_comp_id']}
    cursor.execute(query_to_update_unmatched_brand_with_selected_brand, sql_parameters)
    conn.commit()
    return jsonify("Updated Successfully"), 200


if __name__ == '__main__':
    app.run(host="192.168.2.72", debug=True)
>>>>>>> ee8202577f838f56d5f5c8f14f754d78500c44b0
