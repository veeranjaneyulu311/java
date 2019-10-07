import traceback
from threading import Thread

import numpy
import psycopg2
from flask import Flask, jsonify, request
import pandas as pd
from psycopg2 import pool
from fuzzywuzzy import utils, fuzz, process
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import logging
import os
import time
import uuid

# logging configuration
logger = logging.getLogger("pharmacyDrugsMatchingLogging")
handler = logging.FileHandler('excel_drugs_matching.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

#: Queries Used In All Below API'S
#: API - fetchMatchedAndUnmatchedDrugBrands
query_to_fetch_count_of_uploaded_brands = "SELECT count(*) from public.drug_brand_comp_ref where created_usr_id = %(emp_id)s and org_id = %(org_id)s and process_status is null"

#: API - checkIsCompareCompleted
query_to_check_is_running = "SELECT exists (SELECT 1 FROM drug_brand_comp_ref WHERE  process_status = %(status)s and org_id = %(org_id)s LIMIT 1)"
query_to_check_is_completed = "SELECT exists (SELECT 1 FROM drug_brand_comp_ref WHERE  process_status = %(status)s and org_id = %(org_id)s LIMIT 1)"


# command for enabling CORS
cors = CORS(app, resources={r"*": {"origins": "*"}})

# It stores the UUID for each request
response_token = 0


#: It establishes connection pool with the configured database
try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error:
    logger.info("Error while connecting to PostgreSQL", error)


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
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'PHARMACY EXCEL UPLOAD','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'PHARMACY EXCEL UPLOAD','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response


# it will be used by first api for exact matches
# it will pre process all test names for comparision and reduces comparision time
# it will convert test names to lowercase(Case Insensitivity)
# orders all words of test names in ascending order(Removing Words Order dependency)
def pre_process(drug_brand_nm):
    ts = utils.full_process(drug_brand_nm, force_ascii=True)
    stop_words=['-','mg','ml','mg/ml']
    tokens = ts.split()
    tokens= [token for token in tokens if not token in stop_words]
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


# this function gives approximate matches for each unmatched test
def probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process):
    unmatched_brand_name = unmatched_brand_details["drug_brand_nm"]

    unmatched_brand_name_process = pre_process(unmatched_brand_name)

    # this function will give list of matches from a data frame in order to jsonify the result
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
        matched_ratio = fuzz.ratio(brand_details['drug_brand_nm'], unmatched_brand_name_process)
        if (matched_ratio > 65) and (brand_details['drug_brand_nm'] != unmatched_brand_name_process):
            df_for_db_drug_brand_details.at[brand_details.name, 'matched_percntg'] = matched_ratio
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
        # stores matched percentage as 100 for exact matched brands
        for exact_matched_brand_index in df_for_exact_matched_brand.index:
            df_for_db_drug_brand_details.at[exact_matched_brand_index, 'matched_percntg'] = 100
        df_for_exact_matched_brand_type = df_for_exact_matched_brand[df_for_exact_matched_brand['drug_type_nm'] == unmatched_brand_details['drug_type_nm'].lower()]
        if df_for_exact_matched_brand_type.empty:
            df_for_exact_matched_brand_dose = df_for_exact_matched_brand[
                df_for_exact_matched_brand['dose_nm'] == unmatched_brand_details['dose_nm'].lower()]
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
                df_for_exact_matched_brand_type['dose_nm'] == unmatched_brand_details['dose_nm'].lower()]
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

        # creates empty column for storing the matching percentages
        df_for_db_drug_brand_details['matched_percntg'] = numpy.nan
        df_for_db_drug_brand_details_process = df_for_db_drug_brand_details_process.applymap(lambda drug: drug.lower() if type(drug) == str else drug)
        # start_time = time.time()
        # iterating over user uploaded brands to check weather they match with brands available in database
        for unmatched_brand_index in df_for_unmatched_brand_details.index:
            # print("start")
            # below field holds user given brand name, dose name, drug type
            unmatched_brand_details = df_for_unmatched_brand_details.loc[unmatched_brand_index].to_dict()
            result, is_matched = probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process)
            # condition to check given brand name exactly matched with any of brand name in database
            if is_matched == "matched":
                response["matched"].append(result)
            # condition to check given brand name  unmatched with any of brand name in database but at least having approximate matches for suggesting
            elif is_matched == "unmatched":
                values = ','.join(cursor_two.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", (brand['drug_brand_nm'], brand['dose_nm'], brand['drug_type_nm'], brand['matched_percntg'],unmatched_brand_details['drug_brand_comp_id'].item(), unmatched_brand_details['created_usr_id'].item(), unmatched_brand_details['org_id'].item(), unmatched_brand_details['org_grp_id'].item())).decode('utf-8') for brand in result)
                cursor_two.execute("INSERT INTO drug_brand_suggest_ref (drug_brand_nm,dose_nm,drug_type_nm,matched_percntg,drug_brand_comp_id,created_usr_id,org_id,org_grp_id) VALUES " + values)
            # condition to check given brand name is not matched with any of brand name in database and not having any approximate match
            elif is_matched == "notall":
                response["notall"].append(result)
            # print("end")
        # end_time = time.time()
        # the below db calls will update flag (i.e is_matched) column of user uploaded brands table(i.e temporary table) to differentiate matched and completely not brands
        matched = tuple([brand['drug_brand_nm'] for brand in response['matched']])
        # no completely matched list
        if len(matched) > 0:
            add_flag_one = "UPDATE public.drug_brand_comp_ref SET is_matched = true WHERE drug_brand_nm in %(matched)s and org_id = %(org_id)s"
            sql_parameter_matched = {"matched": matched, "org_id": request_data['org_id']}
            cursor_two.execute(add_flag_one, sql_parameter_matched)

        notall = tuple([brand['drug_brand_nm'] for brand in response['notall']])
        # no completely unmatched list
        if len(notall) > 0:
            add_flag_two = "UPDATE public.drug_brand_comp_ref SET is_matched = false WHERE drug_brand_nm in %(notall)s and org_id = %(org_id)s"
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


#: This API starts comparision operation by creating a new thread in background and returns approximate time required for completing the comparision(in minutes)
#: For comparing, each brand takes it 15 seconds approximately
#: payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
@app.route("/fetchMatchedAndUnmatchedDrugBrands", methods=['POST'])
def fetch_matched_and_unmatched():
    try:
        # get the payload from given request
        request_data = request.get_json()
        req_url_rule = request.url_rule
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor()

        # passing used parameters into query
        sql_parameters_for_count = {"emp_id": request_data['authenticated_user_id'], "org_id": request_data['org_id']}
        cursor.execute(query_to_fetch_count_of_uploaded_brands, sql_parameters_for_count)
        result = cursor.fetchone()[0]
        # Spawn thread to process the data
        thread_for_processing = Thread(target=get_suggestions,
                                       args=(request_data, req_url_rule, response_token))
        thread_for_processing.start()

        # time required for completing the comparision in minutes
        time_required = (result*15)/60
        response_for_given_request = {"time_required": "IT WILL TAKE " + str(time_required) + " MINUTES TO VERIFY THE DRUGS IN OUR ORGANIZATION"}
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


# This API checks weather background process is completed or not.
# payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
# process_status = running (indicates background process is going on)
# process_status = completed (indicates background process is going on)
@app.route("/checkIsCompareCompleted", methods=['POST'])
def check_is_comparison_completed():
    try:
        # get the payload from given request
        request_data = request.get_json()
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor()
        sql_parameters = {"status": "running", "org_id": request_data['org_id']}
        cursor.execute(query_to_check_is_running, sql_parameters)
        is_running = cursor.fetchone()[0]
        # condition to check organization having data to process and started processing
        if is_running:
            response_for_given_request = {"time_not_required": False}
        else:
            sql_parameters = {"status": "completed", "org_id": request_data['org_id']}
            cursor.execute(query_to_check_is_completed, sql_parameters)
            is_completed = cursor.fetchone()[0]
            # condition to check organization having data to process and completed processing
            if is_completed:
                response_for_given_request = {"time_not_required": True}
            # organization not having data to process
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
# payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
# is_matched = true (indicates brand is exactly matched)
# is_matched = false (indicates completely unmatched i.e no suggestions)
# is_matched = null (indicates unmatched i.e having suggestions)
@app.route("/fetchAllDrugsList", methods=['POST'])
def fetch_all_brands():
    try:
        # get the payload from given request
        request_data = request.get_json()
        query_to_fetch_all_brands_uploaded = "SELECT drug_brand_comp_id, drug_brand_nm, dose_nm, drug_type_nm, is_matched from public.drug_brand_comp_ref where org_id = %(org_id)s and process_status = %(status)s"
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # passing the parameter values into sql query
        sql_parameters = {"org_id": request_data['org_id'], "status": "completed"}
        cursor.execute(query_to_fetch_all_brands_uploaded, sql_parameters)
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


# This API returns all matched suggestions for given brand_comp_id in that organization
# required payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001, "drug_brand_comp_id":6724}
@app.route("/fetchSuggestionsForUnmatchedDrugBrands", methods=['POST'])
def fetch_suggestions_for_unmatched():
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


# This api will update unmatched brands with user selected brand from provided suggestions
# required payload {
#         "dose_nm": "2 mg",
#         "drug_brand_comp_id": 6724,
#         "drug_brand_nm": "Andial",
#         "drug_type_nm": "Calcimax d-1000",
#         "is_matched": true/false
#     }
@app.route("/updateUnmatchedBrandWithSelectedBrand", methods=['POST'])
def update_unmatched_brand_with_selected_brand():
    try:
        conn = threaded_postgreSQL_pool.getconn()
        # get the payload from given request
        request_data = request.get_json()
        cursor = conn.cursor()

        # is_matched is true then update user uploaded brand with selected brand and add it to exactly matched list
        # is_matched is false then add user uploaded brand to completely  unmatched list
        if request_data['is_matched']:
            query_to_update_unmatched_brand_with_selected_brand = "UPDATE public.drug_brand_comp_ref SET drug_brand_nm=%(drug_brand_nm)s, dose_nm=%(dose_nm)s, drug_type_nm=%(drug_type_nm)s, is_matched=%(is_matched)s WHERE drug_brand_comp_id=%(drug_brand_comp_id)s and org_id=%(org_id)s"

            # passing the parameter values into sql query
            sql_parameters = {'drug_brand_nm': request_data['drug_brand_nm'], 'dose_nm': request_data['dose_nm'],
                              'drug_type_nm': request_data['drug_type_nm'], 'is_matched': request_data['is_matched'],
                              'drug_brand_comp_id': request_data['drug_brand_comp_id'], 'org_id': request_data['org_id']}
            cursor.execute(query_to_update_unmatched_brand_with_selected_brand, sql_parameters)
        else:
            query_to_add_unmatched_brand_into_completly_unmatched_brands = "UPDATE public.drug_brand_comp_ref SET is_matched=%(is_matched)s WHERE drug_brand_comp_id=%(drug_brand_comp_id)s and org_id=%(org_id)s"

            # passing the parameter values into sql query
            sql_parameters = {'is_matched': request_data['is_matched'],
                              'drug_brand_comp_id': request_data['drug_brand_comp_id'],
                              'org_id': request_data['org_id']}
            cursor.execute(query_to_add_unmatched_brand_into_completly_unmatched_brands, sql_parameters)

        # it removes all suggestions for the selected brand
        query_to_remove_suggestions_selected_brand = " DELETE FROM public.drug_brand_suggest_ref WHERE drug_brand_comp_id=%(drug_brand_comp_id)s and org_id=%(org_id)s "
        sql_parameters_for_removing_suggestions = {'drug_brand_comp_id': request_data['drug_brand_comp_id'], 'org_id': request_data['org_id']}
        cursor.execute(query_to_remove_suggestions_selected_brand, sql_parameters_for_removing_suggestions)

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


# This api will insert completely unmatched drug brands into drug_brand_ref table and removes them from temporary table
# payload {"org_id": 1333, "org_grp_id": 2775, "created_user_id": 220190316000001, "new_drug_list":[{ "dose_nm": "2 mg","drug_brand_comp_id": 6724,"drug_brand_nm": "Andial","drug_type_nm": "Calcimax d-1000"}]}
@app.route("/insertNewDrugBrand", methods=['POST'])
def insert_new_drug_brand_brand():
    try:
        conn = threaded_postgreSQL_pool.getconn()
        # get the payload from given request
        request_data = request.get_json()
        new_drug_list = request_data['new_drug_list']
        cursor = conn.cursor()
        values = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s)", (new_items['drug_brand_nm'], new_items['dose_nm'], new_items['drug_type_nm'], request_data['created_user_id'], request_data['org_id'], request_data['org_grp_id'])).decode('utf-8') for new_items in new_drug_list)
        print(values)
        query_to_insert_new_drug_brand = "INSERT INTO PUBLIC.DRUG_BRAND_REF( DRUG_BRAND_NM, DOSE_NM, DRUG_TYPE_NM, CREATED_USR_ID, ORG_ID, ORG_GRP_ID ) VALUES " + values
        cursor.execute(query_to_insert_new_drug_brand)
        query_to_remove_new_drugs_from_temp_table = "DELETE FROM PUBLIC.DRUG_BRAND_COMP_REF WHERE drug_brand_comp_id in %(inserted_drug_brands_list)s AND ORG_ID=%(ord_id)s"
        inserted_drug_brands_list = tuple([drug_list['drug_brand_comp_id'] for drug_list in new_drug_list])
        sql_query_parameters = {"ord_id": request_data['org_id'], "inserted_drug_brands_list": inserted_drug_brands_list}
        cursor.execute(query_to_remove_new_drugs_from_temp_table, sql_query_parameters)
        conn.commit()
        threaded_postgreSQL_pool.putconn(conn)
        response = {'data': "Records Inserted Successfully", 'responseCode': "E200", 'responseMessage': "DATA INSERTED SUCCESSFULLY"}
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
    app.run(host="127.0.0.1", port="5000", debug=True)
