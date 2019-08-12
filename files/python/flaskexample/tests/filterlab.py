import traceback
from threading import Thread

import psycopg2
from flask import Flask, jsonify, request
import pandas as pd
import psycopg2 as pg
from fuzzywuzzy import utils, fuzz, process
from psycopg2.extras import  RealDictCursor
from flask_cors import CORS
import logging
import os
import time
import uuid

# logging configuration
logger = logging.getLogger("pharmacyDrugsMatchingLogging")
handler = logging.FileHandler('drug_matches.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# command for enabling CORS
cors = CORS(app, resources={r"*": {"origins": "*"}})

# It stores the UUID for each request
response_token = 0


#: It establishes connection pool with the configured database
try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error:
    logger.info("Error while connecting to PostgreSQL", error)


#: It invoke's the respective function of requested api by passing the connection object obtained from connection pool.
#: It add's validations, response data, status code, error messages to the response
#: It also performs transaction management.
#: It log's the failed request's
def transaction_connection_pool(func):
    def wrap(req, token, request_data):
        try:
            # Use getconn() method to Get Connection from connection pool
            ps_connection = threaded_postgreSQL_pool.getconn()
            request_data = req.get_json()
            result = func(ps_connection, request_data)
            ps_connection.commit()
            threaded_postgreSQL_pool.putconn(ps_connection)
            validations = [{'message': "DATA_FETCH_SUCCESSFULLY", 'errCode': "RES_CODE_DBC1000"}]
            response = {'data': result, 'responseCode': "E200", 'responseMessage': "DATA_FETCH_SUCCESSFULLY", 'validations': validations}
            return [response, 200]
        except Exception:
            ps_connection.rollback()
            threaded_postgreSQL_pool.putconn(ps_connection)
            # This method logg's the every method in this whole application only at the time of Exception
            logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}", token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req.url_rule, traceback.format_exc(), request_data)
            response = {'responseCode': "E400", 'responseMessage': "OPERATION_FAILED_GENERIC_MESSAGE", 'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': constants.OPERATION_FAILED_GENERIC_MESSAGE}, 'data': ''}
            return [response, 500]
    return wrap


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
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'PHARMACY EXCEL UPLOAD','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response


# function for connecting to the database
def connect_dev():
    return pg.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


# Function for using to pre-process the data
def pre_process(drug_brand_nm):
    ts = utils.full_process(drug_brand_nm, force_ascii=True)
    stop_words=['-','mg','ml','mg/ml']
    tokens = ts.split()
    tokens= [token for token in tokens if not token in stop_words]
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


# response = {"matched":[],"unmatched":[],"notall":[]}
# this function gives approximate matches for each unmatched test
def probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process):

    unmatched_brand_name = unmatched_brand_details["drug_brand_nm"]

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
            cursor_save.execute("INSERT INTO drug_brand_suggest_ref (drug_brand_comp_id,drug_brand_nm,dose_nm,drug_type_nm) VALUES " + values)
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


# This API performs comparision operation by creating a new thread and returns approximate time required for comparision(in minutes)
# for comparing, each brand takes 15 seconds approximately
# required payload {org_id: 1333, org_grp_id: 2775, authenticated_user_id: 220190316000001}
@app.route("/fetchMatchedAndUnmatchedDrugBrands", methods=['POST'])
def fetch_matched_and_unmatched():
    try:
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
        response_for_given_request = [{"time_required": time_required}]
        validations = [{'message': "DATA_FETCH_SUCCESSFULLY", 'errCode': "RES_CODE_DBC1000"}]
        response = {'data': response_for_given_request, 'responseCode': "E200", 'responseMessage': "DATA_FETCH_SUCCESSFULLY",
                    'validations': validations}
        return jsonify(response), 200

    except Exception:
        ps_connection.rollback()
        threaded_postgreSQL_pool.putconn(ps_connection)
        # This method logg's the every method in this whole application only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION_FAILED_GENERIC_MESSAGE",
                    'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': constants.OPERATION_FAILED_GENERIC_MESSAGE},
                    'data': ''}
        return [response, 500]
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


# This API returns all matched suggestions for given brand_comp_id
# required payload {"drug_brand_comp_id":6724}
@app.route("/fetchSuggestionsForUnmatchedDrugBrands", methods=['POST'])
def fetch_suggestions_for_unmatched():
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
    app.run(host="0.0.0.0", port="8057", debug=True)
