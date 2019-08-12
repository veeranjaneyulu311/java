# v2
import json
import logging
import os
import time
import traceback
import uuid

import numpy
import psycopg2 as psycopg2
from psycopg2 import pool
import pandas as pd
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS
from fuzzywuzzy import fuzz, utils
from psycopg2.extras import RealDictCursor
from threading import Thread

# logging configuration
logger = logging.getLogger("catalog-excel-logging")
handler = logging.FileHandler('labupload.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# The below line converts the application into flask application
app = Flask(__name__)
# The below line handles the CORS issue
cors = CORS(app, resources={r"*": {"origins": "*"}})

# It stores the UUID for each request
response_token = 0


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
        logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'LabTestsUpload','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())


#: This method log's the every request on successful completion
@app.after_request
def end(response):
        response.headers['Response_Token'] = response_token
        # condition to check success or not
        if response.status_code == 200:
                logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'LabTestsUpload','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}", response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, request.get_json())
        return response


# #: It establishes connection pool with the configured database - dev
# try:
#     threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
# except (Exception, psycopg2.DatabaseError) as error:
#     logger.info("Error while connecting to PostgreSQL", error)


#: It establishes connection pool with the configured database - qa
try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_qa", user="drucare_appuser", password="care$app@2233", host="13.234.40.201", port="3388")
except (Exception, psycopg2.DatabaseError) as error :
    logger.info("Error while connecting to PostgreSQL", error)


# testing purpose
def delete():
    conn = threaded_postgreSQL_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("delete from  lab.lab_test_suggest_ref  ")
    cursor.execute("delete from  lab.lab_test_comp_ref ")
    conn.commit()


# it will be used by first api for exact matches
# it will pre process all test names for comparision and reduces comparision time
# it will convert test names to lowercase(Case Insensitivity)
# orders all words of test names in ascending order(Removing Words Order dependency)
def pre_process(long_common_nm):
    ts = utils.full_process(long_common_nm, force_ascii=True)
    stop_words = ['is', 'in', 'the']
    tokens = ts.split()
    # it contains tokens after removing stop words
    tokens = [token for token in tokens if not token in stop_words]
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


# this function gives all possible combinations matching columns if no suggestions found for non-exactly matched tests
def check_for_combinations_matched(df_second, unmatched_test_details):
    # tests with four columns matched
    df_for_test_and_sample_obs_dept_time = pd.DataFrame()
    df_for_test_and_sample_obs_dept_panel = None
    df_for_test_and_sample_obs_time_panel = None
    df_for_test_and_sample_dept_time_panel = None
    df_for_test_and_obs_dept_time_panel = None

    # tests with three columns matched
    df_for_test_and_sample_obs_dept = pd.DataFrame()
    df_for_test_and_sample_obs_time = None
    df_for_test_and_sample_obs_panel = None
    df_for_test_and_sample_dept_time = None
    df_for_test_and_sample_dept_panel = None
    df_for_test_and_sample_time_panel = None
    df_for_test_and_obs_dept_time = None
    df_for_test_and_obs_dept_panel = None
    df_for_test_and_obs_time_panel = None
    df_for_test_and_dept_time_panel = None

    # tests with two columns matched
    df_for_test_and_sample_obs = pd.DataFrame()
    df_for_test_and_sample_dept = None
    df_for_test_and_sample_time = None
    df_for_test_and_sample_panel = None
    df_for_test_and_obs_dept = None
    df_for_test_and_obs_time = None
    df_for_test_and_obs_panel = None
    df_for_test_and_dept_time = None
    df_for_test_and_dept_panel = None
    df_for_test_and_time_panel = None

    # tests with single column matched
    df_for_test_and_sample = df_second[(df_second['loinc_system'] == unmatched_test_details['loinc_system'])]
    df_for_test_obs = df_second[(df_second['order_obs'] == unmatched_test_details['order_obs'])]
    df_for_test_and_dept = df_second[(df_second['investigation_department'] == unmatched_test_details['investigation_department'])]
    df_for_test_and_time = df_second[(df_second['time_aspect'] == unmatched_test_details['time_aspect'])]
    df_for_test_and_panel = df_second[(df_second['is_panel'] == unmatched_test_details['is_panel'])]

    # sample
    # condition for two columns matching
    if not df_for_test_and_sample.empty:
        df_for_test_and_sample_obs = df_for_test_and_sample[df_for_test_and_sample['order_obs'] == unmatched_test_details['order_obs']]
        df_for_test_and_sample_dept = df_for_test_and_sample[df_for_test_and_sample['investigation_department'] == unmatched_test_details['investigation_department']]
        df_for_test_and_sample_time = df_for_test_and_sample[df_for_test_and_sample['time_aspect'] == unmatched_test_details['time_aspect']]
        df_for_test_and_sample_panel = df_for_test_and_sample[df_for_test_and_sample['is_panel'] == unmatched_test_details['is_panel']]
        # condition for three columns matching
        if not df_for_test_and_sample_obs.empty:
            df_for_test_and_sample_obs_dept = df_for_test_and_sample_obs[df_for_test_and_sample_obs['investigation_department']==unmatched_test_details['investigation_department']]
            df_for_test_and_sample_obs_time = df_for_test_and_sample_obs[df_for_test_and_sample_obs['time_aspect'] == unmatched_test_details['time_aspect']]
            df_for_test_and_sample_obs_panel = df_for_test_and_sample_obs[df_for_test_and_sample_obs['is_panel'] == unmatched_test_details['is_panel']]
            # condition for four columns matching
            if not df_for_test_and_sample_obs_dept.empty:
                df_for_test_and_sample_obs_dept_time = df_for_test_and_sample_obs_dept[df_for_test_and_sample_obs_dept['time_aspect'] == unmatched_test_details['time_aspect']]
                df_for_test_and_sample_obs_dept_panel = df_for_test_and_sample_obs_dept[df_for_test_and_sample_obs_dept['is_panel'] == unmatched_test_details['is_panel']]
            if not df_for_test_and_sample_obs_time.empty:
                df_for_test_and_sample_obs_time_panel = df_for_test_and_sample_obs_time[df_for_test_and_sample_obs_time['is_panel'] == unmatched_test_details['is_panel']]
        # condition for three columns matching
        if not df_for_test_and_sample_dept.empty:
            df_for_test_and_sample_dept_time = df_for_test_and_sample_dept[df_for_test_and_sample_dept['time_aspect'] == unmatched_test_details['time_aspect']]
            df_for_test_and_sample_dept_panel = df_for_test_and_sample_dept[df_for_test_and_sample_dept['is_panel'] == unmatched_test_details['is_panel']]
            # condition for four columns matching
            if not df_for_test_and_sample_dept_time.empty:
                df_for_test_and_sample_dept_time_panel = df_for_test_and_sample_dept_time[df_for_test_and_sample_dept_time['is_panel'] == unmatched_test_details['is_panel']]
        # condition for three columns matching
        if not df_for_test_and_sample_time.empty:
            df_for_test_and_sample_time_panel = df_for_test_and_sample_time[df_for_test_and_sample_time['is_panel'] == unmatched_test_details['is_panel']]

    # obs
    # condition for two columns matching
    if not df_for_test_obs.empty:
        df_for_test_and_obs_dept = df_for_test_obs[df_for_test_obs['investigation_department'] == unmatched_test_details['investigation_department']]
        df_for_test_and_obs_time = df_for_test_obs[df_for_test_obs['time_aspect'] == unmatched_test_details['time_aspect']]
        df_for_test_and_obs_panel = df_for_test_obs[df_for_test_obs['is_panel'] == unmatched_test_details['is_panel']]
        # condition for three columns matching
        if not df_for_test_and_obs_dept.empty:
            df_for_test_and_obs_dept_time = df_for_test_and_obs_dept[df_for_test_and_obs_dept['time_aspect'] == unmatched_test_details['time_aspect']]
            df_for_test_and_obs_dept_panel = df_for_test_and_obs_dept[df_for_test_and_obs_dept['is_panel'] == unmatched_test_details['is_panel']]
            # condition for four columns matching
            if not df_for_test_and_obs_dept_time.empty:
                df_for_test_and_obs_dept_time_panel = df_for_test_and_obs_dept_time[df_for_test_and_obs_dept_time['is_panel'] == unmatched_test_details['is_panel']]
        # condition for three columns matching
        if not df_for_test_and_obs_time.empty:
            df_for_test_and_obs_time_panel = df_for_test_and_obs_time[df_for_test_and_obs_time['is_panel'] == unmatched_test_details['is_panel']]

    # dept
    # condition for two columns matching
    if not df_for_test_and_dept.empty:
        df_for_test_and_dept_time = df_for_test_and_dept[df_for_test_and_dept['time_aspect'] == unmatched_test_details['time_aspect']]
        df_for_test_and_dept_panel = df_for_test_and_dept[df_for_test_and_dept['is_panel'] == unmatched_test_details['is_panel']]
        # condition for three columns matching
        if not df_for_test_and_dept_time.empty:
            df_for_test_and_dept_time_panel = df_for_test_and_dept_time[df_for_test_and_dept_time['is_panel'] == unmatched_test_details['is_panel']]

    # panel
    # condition for two columns matching
    if not df_for_test_and_time.empty:
        df_for_test_and_time_panel = df_for_test_and_time[df_for_test_and_time['is_panel'] == unmatched_test_details['is_panel']]

    four_cols_matched = pd.concat([df_for_test_and_sample_obs_dept_time, df_for_test_and_sample_obs_dept_panel,
                                   df_for_test_and_sample_obs_time_panel, df_for_test_and_sample_dept_time_panel,
                                   df_for_test_and_obs_dept_time_panel])

    # conditions to return one of the response
    if four_cols_matched.empty:
        three_cols_matched = pd.concat([df_for_test_and_sample_obs_dept, df_for_test_and_sample_obs_time,
                                       df_for_test_and_sample_obs_panel,
                                       df_for_test_and_sample_dept_time, df_for_test_and_sample_dept_panel,
                                       df_for_test_and_sample_time_panel, df_for_test_and_obs_dept_time,
                                       df_for_test_and_obs_dept_panel,
                                       df_for_test_and_obs_time_panel, df_for_test_and_dept_time_panel])

        if three_cols_matched.empty:
            two_cols_matched = pd.concat(
                [df_for_test_and_sample_obs, df_for_test_and_sample_dept, df_for_test_and_sample_time,
                 df_for_test_and_sample_panel, df_for_test_and_obs_dept, df_for_test_and_obs_time,
                 df_for_test_and_obs_panel, df_for_test_and_dept_time, df_for_test_and_dept_panel,
                 df_for_test_and_time_panel])
            if two_cols_matched.empty:
                one_col_matched = pd.concat(
                    [df_for_test_and_sample, df_for_test_obs, df_for_test_and_dept, df_for_test_and_time,
                     df_for_test_and_panel])
                return one_col_matched
            else:
                return two_cols_matched
        else:
            return three_cols_matched
    else:
        return four_cols_matched


# this function gives approximate matches for each unmatched test
def probability_for_unmatched(unmatched_test_details, df_for_existing_tests, df_for_existing_tests_pre_process):
    # output 1
    approximately_matched_tests_with_remaining_cols_exactly_match = []
    data = None
    # fetch given unmatched  test details
# unmatched_test_name = unmatched_test_details["long_common_nm"]
    df_for_tests_in_db_process_filtered = df_for_existing_tests_pre_process[
        (df_for_existing_tests_pre_process.is_panel == unmatched_test_details['is_panel']) & (
                    df_for_existing_tests_pre_process.order_obs == unmatched_test_details['order_obs']) & (
                    df_for_existing_tests_pre_process.loinc_system == unmatched_test_details['loinc_system']) & (
                    df_for_existing_tests_pre_process.time_aspect == unmatched_test_details['time_aspect']) & ((
                                                                                                                    df_for_existing_tests_pre_process.investigation_department ==
                                                                                                                    unmatched_test_details[
                                                                                                                        'investigation_department']) | (
                                                                                                            df_for_existing_tests_pre_process.investigation_department.isnull()))]
    unmatched_test_name_process = unmatched_test_details["long_common_nm"]

    # function to compare given tests with all available tests for approximate match
    def approximate(filtered_tests_details):
        matched_ratio = fuzz.ratio(filtered_tests_details['long_common_nm'], unmatched_test_name_process)
        if (matched_ratio > 90) and (
                    filtered_tests_details['long_common_nm'] != unmatched_test_name_process):
            approximately_matched_tests_with_remaining_cols_exactly_match.append(json.loads(df_for_existing_tests.loc[filtered_tests_details.name].to_json()).update({'matched_percentage': matched_ratio}))

    # this function will give list of matches from a data frame to jsonify the result by applying conditions on loinc_system, order_obs, time_aspect
    def response_from_dataframe(df):
        nonlocal data
        if unmatched_test_details['loinc_system'] not in ['bld', 'blood', 'ser', 'serum', 'plasma']:
            df = df[df.loinc_system == unmatched_test_details['loinc_system']]
        else:
            df = df[df.loinc_system.isin(['bld', 'blood', 'ser', 'serum', 'plasma'])]
        df = df[((df.order_obs == unmatched_test_details['order_obs']) | (df.order_obs == 'both')) & (df.time_aspect == unmatched_test_details['time_aspect'].lower())]
        df1 = df_for_existing_tests[df_for_existing_tests.index.isin(df.index)]
        if not df1.empty:
            data = json.loads(df1.to_json(orient='records'))

    # this function will check weather a test is approximately matched or not
    def check_for_matching(tests_details):
        matched_ratio = fuzz.ratio(tests_details['long_common_nm'], unmatched_test_name_process)
        if (matched_ratio > 65) and (
                    tests_details['long_common_nm'] != unmatched_test_name_process):
            df_for_existing_tests.at[tests_details.name, 'matched_percentage'] = matched_ratio
            return True
        else:
            return False
# *
    df_for_tests_in_db_process_filtered.apply(approximate, axis=1)
    if len(approximately_matched_tests_with_remaining_cols_exactly_match) == 0:
        # fetching all exactly matched tests by excluding remaining columns
        df_for_exact_matched = df_for_existing_tests_pre_process[df_for_existing_tests_pre_process['long_common_nm'] == unmatched_test_name_process]

        # check matches available for exact
        if df_for_exact_matched.empty:

            # approx match if no exact matches
            df_for_approximately_matched = df_for_existing_tests_pre_process[df_for_existing_tests_pre_process.apply(check_for_matching, axis=1)]
            # check if approximate matches exist
            if not df_for_approximately_matched.empty:
                # output 3
                approx_combinations = check_for_combinations_matched(df_for_approximately_matched, unmatched_test_details)
                if approx_combinations.empty:
                    return None, False
                else:
                    response_from_dataframe(approx_combinations)
            else:
                return None, False
        else:
            # filtering the data:  it calls a function to exclude user selected columns and apply remaining exactly
            # output 1
            exact_combinations = check_for_combinations_matched(df_for_exact_matched, unmatched_test_details)
            if exact_combinations.empty:
                return None, False
            else:
                # it inserts 100% for all test names matching exactly
                for exact_matched_test_index in exact_combinations.index:
                    df_for_existing_tests.at[exact_matched_test_index, 'matched_percentage'] = 100
                response_from_dataframe(exact_combinations)

    # form the output
    if len(approximately_matched_tests_with_remaining_cols_exactly_match) == 0:
        return data, True
    else:
        return approximately_matched_tests_with_remaining_cols_exactly_match, True


# this will fetch all unmatched tests from temporary table and check for approximately matched
# inserts approximate matches into temporary table, also updates is matched column with 'false' for tests with no approximate matches
def get_suggestions(conn, request_data, df_for_existing_tests_pre_process, df_for_existing_tests):
    not_matched_test_list = []
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_to_fetch_unmatched_test_details = "select lab_test_comp_id, long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, created_usr_id, org_id, org_grp_id from lab.lab_test_comp_ref where org_id=%(org_id)s and is_matched is null and process_status=%(status)s"
    query_param = {"org_id": request_data['org_id'], "status": "running"}
    cursor.execute(query_to_fetch_unmatched_test_details, query_param)
    df_for_unmatched_test_details = pd.DataFrame(data=cursor.fetchall(),
                                                 columns=['long_common_nm', 'loinc_system', 'investigation_department',
                                                          'time_aspect', 'is_panel', 'order_obs', 'lab_test_comp_id', 'created_usr_id', 'org_id', 'org_grp_id'])

    df_for_unmatched_test_details_pre_process = df_for_unmatched_test_details.copy()
    df_for_unmatched_test_details_pre_process["long_common_nm"] = df_for_unmatched_test_details_pre_process["long_common_nm"].apply(
        pre_process)

    df_for_unmatched_test_details_pre_process = df_for_unmatched_test_details_pre_process.applymap(
        lambda test: test.lower() if type(test) == str else test)

    for unmatched_test_index in df_for_unmatched_test_details_pre_process.index:
        unmatched_test_details = df_for_unmatched_test_details.loc[unmatched_test_index].to_dict()
        unmatched_test_details_pre_process = df_for_unmatched_test_details_pre_process.loc[
            unmatched_test_index].to_dict()
        result, has_suggestions = probability_for_unmatched(unmatched_test_details_pre_process, df_for_existing_tests, df_for_existing_tests_pre_process)
        # insert suggestions into corresponding table
        if has_suggestions and (result is not None):
            values = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
            test['long_common_nm'], test['loinc_system'], test['investigation_department'], test['time_aspect'], test['is_panel'], test['order_obs'],
            unmatched_test_details['lab_test_comp_id'].item(), test['matched_percentage'], unmatched_test_details['created_usr_id'].item(),
            unmatched_test_details['org_id'].item(), unmatched_test_details['org_grp_id'].item())).decode('utf-8') for
                              test in result)
            cursor.execute(
                "INSERT INTO lab.lab_test_suggest_ref (long_common_nm,loinc_system,investigation_department,time_aspect,is_panel,order_obs,lab_test_comp_id,matched_percentage,created_usr_id,org_id,org_grp_id) VALUES " + values)
        else:
            not_matched_test_list.append(unmatched_test_details)

    # it will update all unmatched tests with is_matched = false
    add_flag = "UPDATE lab.lab_test_comp_ref SET is_matched = false WHERE long_common_nm in %(not_matched)s and org_id =%(org_id)s"
    if len(not_matched_test_list) > 0:
        not_matched = tuple([not_matched_test['long_common_nm'] for not_matched_test in not_matched_test_list])
        sql_parameter = {"not_matched": not_matched, "org_id": request_data['org_id']}
        cursor.execute(add_flag, sql_parameter)


# This function will separate all exactly matched and unmatched tests
def get_matched_unmatched_data(*args):
    # used as flag for checking a test matched or not
    exactly_matched_tests_bool = None
    # stores exactly mapped tests
    exactly_matched_tests = []
    # stores unmapped tests
    unmatched_tests = []
    df_for_uploaded_tests = args[0]
    df_for_uploaded_tests_pre_process = args[1]
    df_for_existing_tests_pre_process = args[3]

    # It has all the conditions for exact and approximate matchings
    def check_for_matches_exist(test_name_in_filtered_data, uploaded_test_index_num):
        nonlocal exactly_matched_tests_bool
        # check for exact match
        if df_for_uploaded_tests_pre_process.at[uploaded_test_index_num, 'long_common_nm'] == test_name_in_filtered_data:
            if exactly_matched_tests_bool:
                exactly_matched_tests_bool = False

    # This loop iterates for each test  uploaded by user
    for uploaded_test_index in df_for_uploaded_tests.index:
        # It will filter all tests matching below columns in below mentioned order
        # is_panel, order_obs, loinc_system, time_aspect, investigation_department from db data
        df_for_existing_tests_pre_process_filtered = df_for_existing_tests_pre_process[(
                                                                                                   df_for_existing_tests_pre_process.is_panel ==
                                                                                                   df_for_uploaded_tests_pre_process.at[
                                                                                                       uploaded_test_index, 'is_panel']) & (
                                                                                                   df_for_existing_tests_pre_process.order_obs ==
                                                                                                   df_for_uploaded_tests_pre_process.at[
                                                                                                       uploaded_test_index, 'order_obs']) & (
                                                                                                   df_for_existing_tests_pre_process.loinc_system ==
                                                                                                   df_for_uploaded_tests_pre_process.at[
                                                                                                       uploaded_test_index, 'loinc_system']) & (
                                                                                                   df_for_existing_tests_pre_process.time_aspect ==
                                                                                                   df_for_uploaded_tests_pre_process.at[
                                                                                                       uploaded_test_index, 'time_aspect']) & (
                                                                                                   (
                                                                                                               df_for_existing_tests_pre_process.investigation_department ==
                                                                                                               df_for_uploaded_tests_pre_process.at[
                                                                                                                   uploaded_test_index, 'investigation_department']) | (
                                                                                                       df_for_existing_tests_pre_process.investigation_department.isnull()))]

        # df_for_existing_tests_pre_process_filtered = df_for_existing_tests_pre_process[(df_for_existing_tests_pre_process.long_common_nm=='mchc') &(df_for_existing_tests_pre_process.is_panel == False) & ( df_for_existing_tests_pre_process.order_obs == 'observation') & ( df_for_existing_tests_pre_process.loinc_system =='rbc') & ( df_for_existing_tests_pre_process.time_aspect == 'pt') & ((df_for_existing_tests_pre_process.investigation_department =='hematology') | ( df_for_existing_tests_pre_process.investigation_department.isnull()))]
        exactly_matched_tests_bool = True
        # verifying weather any tests are available for comparision
        # if available, compare each test name of filtered data with the uploaded test name
        if len(df_for_existing_tests_pre_process_filtered.index) != 0:
            df_for_existing_tests_pre_process_filtered['long_common_nm'].apply(func=check_for_matches_exist, args=[uploaded_test_index])

        # condition to check exactly matched or not
        if not exactly_matched_tests_bool:
            exactly_matched_tests.append(json.loads(df_for_uploaded_tests.loc[uploaded_test_index].to_json()))
        else:
            unmatched_tests.append(json.loads(df_for_uploaded_tests.loc[uploaded_test_index].to_json()))

    excel_validated_response = {"matched": exactly_matched_tests, "unmatched": unmatched_tests}
    return excel_validated_response


# first api:  this function will compare all uploaded tests with available tests
def compare_excel_uploaded_tests_with_database_tests(request_data, req_url_rule, token):
    try:
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogTestsExcelUploadBackground','timeStamp':%s,'apiName':%s,'status':'START','payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule,
            request_data)
        # df_for_uploaded_tests = None
        # df_for_uploaded_tests_pre_process =None
        # df_for_existing_tests = None
        # df_for_existing_tests_pre_process = None
        conn = threaded_postgreSQL_pool.getconn()

        cursor_one = conn.cursor(cursor_factory=RealDictCursor)

        # updating the flag value that indicates process running
        query_to_update_process_status_flag = "update lab.lab_test_comp_ref set process_status = %(status)s where org_id =%(org_id)s and process_status is null"
        sql_parameter_status_running = {"status": "running", "org_id": request_data["org_id"]}
        cursor_one.execute(query_to_update_process_status_flag, sql_parameter_status_running)
        conn.commit()

        # fetch all the excel uploaded data from temporary table and create data frame
        query_to_fetch_uploaded_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, created_usr_id, org_id, org_grp_id from lab.lab_test_comp_ref where org_id =%(org_id)s and process_status =%(status)s"
        sql_parameter_for_unmatched = {"org_id": request_data['org_id'], "status": "running"}
        cursor = conn.cursor()
        cursor.execute(query_to_fetch_uploaded_tests, sql_parameter_for_unmatched)
        df_for_uploaded_tests = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'created_usr_id', 'org_id', 'org_grp_id'])

        query_to_fetch_mapped_and_unmapped_tests = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank , 'mapped' as type FROM lab.lab_org_test_xref lotx inner join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id union all (SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank,'unmapped' as type FROM lab.lab_org_test_xref lotx right join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id where lotx.test_id is null and ltr.isactive is true order by test_rank)"
        # fetch all the tests data from lab.lab_test_ref, lab.lab_org_test_xref(mapped) and create data frame
        cursor.execute(query_to_fetch_mapped_and_unmapped_tests)
        df_for_existing_tests = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank', 'type'])

        # pre process both data frames to reduce processing time during comparision and convert all strings to lower case
        df_for_uploaded_tests_pre_process = df_for_uploaded_tests.copy()
        df_for_existing_tests_pre_process = df_for_existing_tests.copy()

        #
        df_for_uploaded_tests_pre_process["long_common_nm"] = df_for_uploaded_tests_pre_process["long_common_nm"].apply(pre_process)
        df_for_existing_tests_pre_process["long_common_nm"] = df_for_existing_tests_pre_process["long_common_nm"].apply(pre_process)

        # creates empty column for storing the matching percentages
        df_for_existing_tests['matched_percentage'] = numpy.nan
        df_for_uploaded_tests_pre_process = df_for_uploaded_tests_pre_process.applymap(
            lambda drug: drug.lower() if type(drug) == str else drug)
        df_for_existing_tests_pre_process = df_for_existing_tests_pre_process.applymap(
            lambda drug: drug.lower() if type(drug) == str else drug)

        # it updates is_matched flag to true for exactly matched tests
        excel_validated_response = get_matched_unmatched_data(df_for_uploaded_tests, df_for_uploaded_tests_pre_process, df_for_existing_tests, df_for_existing_tests_pre_process)
        add_flag = "UPDATE lab.lab_test_comp_ref SET is_matched = true WHERE long_common_nm in %(matched)s and org_id =%(org_id)s"
        if len(excel_validated_response['matched']) > 0:
            matched = tuple([test['long_common_nm'] for test in excel_validated_response['matched']])
            sql_parameter = {"matched": matched, "org_id": request_data['org_id']}
            cursor.execute(add_flag, sql_parameter)

        get_suggestions(conn, request_data, df_for_existing_tests_pre_process, df_for_existing_tests)

        # updating the flag value(i.e process_status column of temporary table) that indicates process completed
        query_to_update_process_status_flag_completed = "update lab.lab_test_comp_ref set process_status = %(status)s where org_id =%(org_id)s and process_status = %(current_status)s"
        sql_parameter_status_completed = {"status": "completed", "org_id": request_data['org_id'], "current_status": "running"}
        cursor.execute(query_to_update_process_status_flag_completed, sql_parameter_status_completed)
        conn.commit()
        threaded_postgreSQL_pool.putconn(conn)
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogTestsExcelUploadBackground','timeStamp':%s,'apiName':%s,'status':'END','payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule,
            request_data)
    except Exception:
        conn.rollback()
        threaded_postgreSQL_pool.putconn(conn)
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogTestsExcelUploadBackground','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule,
            traceback.format_exc(), request_data)


# This API performs comparision operation by creating a new thread in background and returns approximate time required for comparision(in minutes)
# for comparing, each brand takes 15 seconds approximately
# payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
# response
@app.route("/fetchMatchedAndUnmatchedTests", methods=['POST'])
def fetch_matched_and_unmatched():
    try:
        # Spawn thread to process the data
        request_data = request.get_json()
        req_url_rule = request.url_rule
        conn = threaded_postgreSQL_pool.getconn()
        cursor = conn.cursor()
        query_to_fetch_count_of_uploaded_tests = "SELECT count(*) from lab.lab_test_comp_ref where created_usr_id = %(emp_id)s and org_id = %(org_id)s and process_status is null"
        # passing used parameters into query
        sql_parameters_for_count = {"emp_id": request_data['authenticated_user_id'], "org_id": request_data['org_id']}
        cursor.execute(query_to_fetch_count_of_uploaded_tests, sql_parameters_for_count)
        result = cursor.fetchone()[0]
        thread_for_processing = Thread(target=compare_excel_uploaded_tests_with_database_tests, args=(request_data, req_url_rule, response_token))
        thread_for_processing.start()
        time_required = (result*15)/60
        response_for_given_request = {"time_required": "IT WILL TAKE " + str(time_required) + " MINUTES TO VERIFY THE DRUGS IN OUR ORGANIZATION"}
        threaded_postgreSQL_pool.putconn(conn)
        validations = [{'message': "DATA COMPARISION STARTED SUCCESSFULLY", 'errCode': "RES_CODE_TEU1000"}]
        response = {'data': response_for_given_request, 'responseCode': "E200", 'responseMessage': "DATA COMPARISION STARTED SUCCESSFULLY",
                    'validations': validations}
        return jsonify(response), 200
    except Exception:
        threaded_postgreSQL_pool.putconn(conn)
        # This is logged only at the time of Exception
        logger.info(
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogTestsExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 400


# This API checks weather background process completed
# for comparing, each brand takes 15 seconds approximately
# payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
# response {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001}
# process_status = running (indicates background process is going on)
# process_status = completed (indicates background process is completed)
@app.route("/checkIsCompareCompleted", methods=['POST'])
def check_is_comparison_completed():
    try:
        # get the payload from given request
        request_data = request.get_json()
        query_to_check_is_running = "SELECT exists (SELECT 1 FROM lab.lab_test_comp_ref WHERE  process_status = %(status)s and org_id = %(org_id)s LIMIT 1)"
        query_to_check_is_completed = "SELECT exists (SELECT 1 FROM lab.lab_test_comp_ref WHERE  process_status = %(status)s and org_id = %(org_id)s LIMIT 1)"
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
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogLabExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
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
@app.route("/fetchAllTestsList", methods=['POST'])
def fetch_all_brands():
    try:
        # get the payload from given request
        request_data = request.get_json()
        query_to_fetch_all_brands_uploaded = "SELECT lab_test_comp_id, long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, is_matched from lab.lab_test_comp_ref where org_id = %(org_id)s and process_status = %(status)s"
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
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogLabExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE",
                    'validations': {'errCode': "RES_CODE_OFG001", 'errMessage': "OPERATION FAILED GENERIC MESSAGE"},
                    'data': ''}
        return jsonify(response), 400


# This API returns all matched suggestions for given brand_comp_id in that organization
# required payload {"org_id": 1333, "org_grp_id": 2775, "authenticated_user_id": 220190316000001, "lab_test_comp_id":6724}
@app.route("/fetchSuggestionsForUnmatchedTests", methods=['POST'])
def fetch_suggestions_for_unmatched():
    try:
        conn = threaded_postgreSQL_pool.getconn()
        # get the payload from given request
        request_data = request.get_json()
        query_to_fetch_suggestions = "SELECT lab_test_comp_id, long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs FROM lab.lab_test_suggest_ref where lab_test_comp_id = %(comp_id)s and org_id = %(org_id)s"
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # passing the parameter values into sql query
        sql_parameters = {'comp_id': request_data['lab_test_comp_id'], 'org_id': request_data['org_id']}
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
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogLabExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule, traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE", 'data': ''}
        return jsonify(response), 400


# This api will update unmatched brands with user selected brand from provided suggestions
# {
#          "long_common_nm": "2 mg",
#          "loinc_system": 6724,
#          "investigation_department": "Andial",
#          "time_aspect": "Calcimax d-1000",
# 	       "is_panel":
#          "order_obs":
#          "is_matched": true/false
# }
@app.route("/updateUnmatchedTestWithSelectedTest", methods=['POST'])
def update_unmatched_brand_with_selected_brand():
    try:
        conn = threaded_postgreSQL_pool.getconn()
        # get the payload from given request
        request_data = request.get_json()
        cursor = conn.cursor()

        # is_matched is true then update user uploaded brand with selected brand and add it to exactly matched list
        # is_matched is false then add user uploaded brand to completely  unmatched list
        if request_data['is_matched']:
            query_to_update_unmatched_test_with_selected_test = "UPDATE lab.lab_test_comp_ref SET long_common_nm=%(long_common_nm)s, loinc_system=%(loinc_system)s, investigation_department=%(investigation_department)s, time_aspect=%(time_aspect)s, is_panel=%(is_panel)s, order_obs=%(order_obs)s, is_matched=%(is_matched)s WHERE lab_test_comp_id=%(lab_test_comp_id)s and org_id=%(org_id)s"

            # passing the parameter values into sql query
            sql_parameters = {'long_common_nm': request_data['long_common_nm'],
                              'loinc_system': request_data['loinc_system'], 'investigation_department': request_data['investigation_department'], 'time_aspect': request_data['time_aspect'], 'is_panel': request_data['is_panel'], 'order_obs': request_data['order_obs'], 'is_matched': request_data['is_matched'],
                              'lab_test_comp_id': request_data['lab_test_comp_id'], 'org_id': request_data['org_id']}
            cursor.execute(query_to_update_unmatched_test_with_selected_test, sql_parameters)
        else:
            query_to_add_unmatched_test_into_completly_unmatched_test = "UPDATE lab.lab_test_comp_ref SET is_matched=%(is_matched)s WHERE lab_test_comp_id=%(lab_test_comp_id)s and org_id=%(org_id)s"

            # passing the parameter values into sql query
            sql_parameters = {'is_matched': request_data['is_matched'],
                              'lab_test_comp_id': request_data['lab_test_comp_id'],
                              'org_id': request_data['org_id']}
            cursor.execute(query_to_add_unmatched_test_into_completly_unmatched_test, sql_parameters)

        # it removes all suggestions for the selected brand
        query_to_remove_suggestions_selected_brand = " DELETE FROM lab.lab_test_suggest_ref WHERE lab_test_comp_id=%(lab_test_comp_id)s and org_id=%(org_id)s "
        sql_parameters_for_removing_suggestions = {'lab_test_comp_id': request_data['lab_test_comp_id'], 'org_id': request_data['org_id']}
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
            "{'transactionId':%s,'systemName':%s,'moduleName':'CatalogLabExcelUpload','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",
            response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), request.url_rule,
            traceback.format_exc(), request_data)
        response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED GENERIC MESSAGE", 'data': ''}
        return jsonify(response), 400


if __name__ == '__main__':
    delete()
    app.run(host="127.0.0.1", debug=True)


