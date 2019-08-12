# v2
import json
import logging
import os
import time
import traceback
import uuid
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
handler = logging.FileHandler('lab.log')
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


# used as flag for checking a test matched or not
exactly_matched_tests_bool = None
# stores excel data from lab.lab_test_comp_ref
df_for_uploaded_tests = None
# stores excel data after processing
df_for_uploaded_tests_pre_process = None
# stores excel data from lab.lab_test_ref and lab.lab_org_test_ref(mapped tests)
df_for_existing_tests = None
# stores excel data after processing
df_for_existing_tests_pre_process = None
# stores exactly mapped tests
exactly_matched_tests = []
# stores approximately mapped tests
approximately_matched_tests = []
# stores unmapped tests
unmatched_tests = []


query_for_user_uploaded_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref "
query_for_mapped_and_unmapped_tests = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank , 'mapped' as type FROM lab.lab_org_test_xref lotx inner join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id union all (SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank,'unmapped' as type FROM lab.lab_org_test_xref lotx right join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id where lotx.test_id is null and ltr.isactive is true order by test_rank)"


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


#: It establishes connection pool with the configured database
try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    logger.info("Error while connecting to PostgreSQL", error)


#: It invoke's the respective function of requested api by passing the connection object obtained from connection pool.
#: It add's validations, response data, status code, error messages to the response
#: It also performs transaction management.
#: It log's the failed request's
def transaction_connection_pool(func):
    def wrap(request_data, req_url_rule):
        try:
            # Use getconn() method to Get Connection from connection pool
            ps_connection = threaded_postgreSQL_pool.getconn()
            result = func(ps_connection, request_data)
            ps_connection.commit()
            threaded_postgreSQL_pool.putconn(ps_connection)
            response = {'data': result, 'responseCode': "E200", 'responseMessage': "DATA_FETCH_SUCCESSFULLY"}
            return [response, 200]
        except Exception:
            ps_connection.rollback()
            threaded_postgreSQL_pool.putconn(ps_connection)
            # This method logg's the every method in this whole application only at the time of Exception
            logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",response_token, get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req_url_rule, traceback.format_exc(), request_data)
            response = {'responseCode': "E400", 'responseMessage': "OPERATION FAILED", 'data': ''}
            return [response, 500]
    return wrap


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


# it will be used by first api
# This function will filter the data and checks for available matches in filtered data
def get_matched_unmatched_data():
    global exactly_matched_tests_bool
    global exactly_matched_tests
    global approximately_matched_tests
    global unmatched_tests
    # This loop iterates for each test  uploaded by user
    for uploaded_test_index in df_for_uploaded_tests.index:
        # It will filter all tests matching below columns in below mentioned order
        # is_panel, order_obs, loinc_system, time_aspect, investigation_department from db data
        df_for_existing_tests_pre_process_filtered = df_for_existing_tests_pre_process[(
                                                                                                   df_for_existing_tests_pre_process.is_panel ==
                                                                                                   df_for_uploaded_tests.at[
                                                                                                       uploaded_test_index, 'is_panel']) & (
                                                                                                   df_for_existing_tests_pre_process.order_obs ==
                                                                                                   df_for_uploaded_tests.at[
                                                                                                       uploaded_test_index, 'order_obs']) & (
                                                                                                   df_for_existing_tests_pre_process.loinc_system ==
                                                                                                   df_for_uploaded_tests.at[
                                                                                                       uploaded_test_index, 'loinc_system']) & (
                                                                                                   df_for_existing_tests_pre_process.time_aspect ==
                                                                                                   df_for_uploaded_tests.at[
                                                                                                       uploaded_test_index, 'time_aspect']) & (
                                                                                                   (
                                                                                                               df_for_existing_tests_pre_process.investigation_department ==
                                                                                                               df_for_uploaded_tests.at[
                                                                                                                   uploaded_test_index, 'investigation_department']) | (
                                                                                                       df_for_existing_tests_pre_process.investigation_department.isnull()))]
        exactly_matched_tests_bool = True
        print("No.Of filtered rows for matching this test: "+str(len(df_for_existing_tests_pre_process_filtered.index)))
        # verifying weather any tests are available for comparision
        # if available, compare each test name of filtered data with the uploaded test name
        if len(df_for_existing_tests_pre_process_filtered.index) != 0:
            df_for_existing_tests_pre_process_filtered['long_common_nm'].apply(func=check_for_matches_exist, args=[uploaded_test_index])

        # condition to check exactly matched or not
        if not exactly_matched_tests_bool:
            exactly_matched_tests.append(json.loads(df_for_uploaded_tests.loc[uploaded_test_index].to_json()))
        else:
            print("Un Matched tests----- EXCEL: " + str(df_for_uploaded_tests.at[uploaded_test_index, 'long_common_nm']))
            unmatched_tests.append(json.loads(df_for_uploaded_tests.loc[uploaded_test_index].to_json()))

    excel_validated_response = {"matched": exactly_matched_tests, "unmatched": unmatched_tests}
    return excel_validated_response


# it will be used by first api
# It has all the conditions for exact and approximate matchings
def check_for_matches_exist(test_name_in_filtered_data, uploaded_test_index):
    global exactly_matched_tests_bool
    # check for exact match
    if df_for_uploaded_tests_pre_process.at[uploaded_test_index, 'long_common_nm'] == test_name_in_filtered_data:
        print("Exactly Matched tests----- EXCEL: " + str(df_for_uploaded_tests.at[uploaded_test_index, 'long_common_nm']) + " DB: " + test_name_in_filtered_data)
        if exactly_matched_tests_bool:
            exactly_matched_tests_bool = False


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
    print("end")


# this function gives approximate matches for each unmatched test
def probabilty_for_unmatched(unmatched_test_details, df_for_tests_in_db, df_for_tests_in_db_process):
    # output 1
    approximately_matched_tests_with_remaining_cols_exactly_match = []
    data = None
    # fetch given unmatched  test details

    unmatched_test_name = unmatched_test_details["long_common_nm"]

    df_for_tests_in_db_process_filtered = df_for_tests_in_db_process[
        (df_for_tests_in_db_process.is_panel == unmatched_test_details['is_panel']) & (
                    df_for_tests_in_db_process.order_obs == unmatched_test_details['order_obs']) & (
                    df_for_tests_in_db_process.loinc_system == unmatched_test_details['loinc_system']) & (
                    df_for_tests_in_db_process.time_aspect == unmatched_test_details['time_aspect']) & ((
                                                                                                                    df_for_tests_in_db_process.investigation_department ==
                                                                                                                    unmatched_test_details[
                                                                                                                        'investigation_department']) | (
                                                                                                            df_for_tests_in_db_process.investigation_department.isnull()))]
    unmatched_test_name_process = pre_process(unmatched_test_name)

    # function to compare given tests with all available tests for approximate match
    def approximate(filtered_tests_details):
        if 65 <= fuzz.ratio(filtered_tests_details['long_common_nm'], unmatched_test_name_process) < 100:
            print(fuzz.ratio(filtered_tests_details['long_common_nm'], unmatched_test_name_process), filtered_tests_details['long_common_nm'], unmatched_test_name_process)
            approximately_matched_tests_with_remaining_cols_exactly_match.append(json.loads(df_for_tests_in_db.loc[filtered_tests_details.name].to_json()))

    # this function will give list of matches from a data frame to jsonify the result by applying conditions on loinc_system, order_obs, time_aspect
    def response_from_dataframe(df):
        nonlocal data
        if unmatched_test_details['loinc_system'].lower() not in ['bld', 'blood', 'ser', 'serum', 'plasma']:
            df = df[df.loinc_system.str.lower() == unmatched_test_details['loinc_system'].lower()]
        else:
            df = df[df.loinc_system.str.lower().isin(['bld', 'blood', 'ser', 'serum', 'plasma'])]
        df = df[((df.order_obs.str.lower() == unmatched_test_details['order_obs'].lower()) | (df.order_obs.str.lower() == 'both')) & (df.time_aspect.str.lower() == unmatched_test_details['time_aspect'].lower())]
        df1 = df_for_tests_in_db[df_for_tests_in_db.index.isin(df.index)]
        if not df1.empty:
            data = json.loads(df1.to_json(orient='records'))

    # this function will check weather a test is approximately matched or not
    def check_for_matching(tests_details):
        if 65 <= fuzz.ratio(tests_details['long_common_nm'], unmatched_test_name_process) < 100:
            return True
        else:
            return False

    df_for_tests_in_db_process_filtered.apply(approximate, axis=1)
    if len(approximately_matched_tests_with_remaining_cols_exactly_match) == 0:
        # fetching all exactly matched tests by excluding remaining columns
        df_for_exact_matched = df_for_tests_in_db_process[df_for_tests_in_db_process['long_common_nm'] == unmatched_test_name_process]

        # check matches available for exact
        if df_for_exact_matched.empty:
            # approx match if no exact matches
            df_for_approximately_matched = df_for_tests_in_db_process[df_for_tests_in_db_process.apply(check_for_matching, axis=1)]
            # check if approximate matches exist
            if not df_for_approximately_matched.empty:
                # output 3
                approx_combinations = check_for_combinations_matched(df_for_approximately_matched, unmatched_test_details)
                if approx_combinations.empty:
                    print("no matchings")
                else:
                    response_from_dataframe(approx_combinations)
            else:
                print("no matchings")
        else:
            # filtering the data:  it calls a function to exclude user selected columns and apply remaining exactly
            # output 1
            exact_combinations = check_for_combinations_matched(df_for_exact_matched, unmatched_test_details)
            if exact_combinations.empty:
                print("no matchings")
            else:
                response_from_dataframe(exact_combinations)
    if len(approximately_matched_tests_with_remaining_cols_exactly_match) == 0:
        suggest = {'test': unmatched_test_name, 'approx': data}
    else:
        suggest = {'test': unmatched_test_name, 'approx': approximately_matched_tests_with_remaining_cols_exactly_match}
    return suggest


# this will fetch all unmatched tests from temporary table and check for approximately matched
def get_suggestions(conn):
    response = []
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_to_fetch_unmatched_test_details = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref where is_matched is false"
    # query_to_fetch_unmatched_test_details = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref where long_common_nm = %(test_name)s "
    cursor.execute(query_to_fetch_unmatched_test_details)
    df_for_unmatched_test_details = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs'])
    # fetch all the mapped and unmapped table data
    cursor.execute(query_for_mapped_and_unmapped_tests)
    df_for_tests_in_db = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank', 'type'])
    # pre processing the data for comparision
    df_for_tests_in_db_process = df_for_tests_in_db.copy()
    df_for_tests_in_db_process["long_common_nm"] = df_for_tests_in_db_process["long_common_nm"].apply(pre_process)

    for unmatched_test_index in df_for_unmatched_test_details.index:
        unmatched_test_details = df_for_unmatched_test_details.loc[unmatched_test_index].to_dict()
        result = probabilty_for_unmatched(unmatched_test_details, df_for_tests_in_db, df_for_tests_in_db_process)
        response.append(result)
    return response


# first api:  this function will compare all uploaded tests with available tests
@transaction_connection_pool
def compare_excel_uploaded_tests_with_database_tests(conn, req):
    global df_for_uploaded_tests
    global df_for_uploaded_tests_pre_process
    global df_for_existing_tests
    global df_for_existing_tests_pre_process
    cursor = conn.cursor()
    # fetch all the excel uploaded data from temporary table and create data frame
    cursor.execute(query_for_user_uploaded_tests)
    df_for_uploaded_tests = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs'])
    # fetch all the tests data from lab.lab_test_ref, lab.lab_org_test_xref(mapped) and create data frame
    cursor.execute(query_for_mapped_and_unmapped_tests)
    df_for_existing_tests = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank', 'type'])
    # pre process both data frames to reduce processing time during comparision
    df_for_uploaded_tests_pre_process = df_for_uploaded_tests.copy()
    df_for_existing_tests_pre_process = df_for_existing_tests.copy()
    df_for_uploaded_tests_pre_process["long_common_nm"] = df_for_uploaded_tests_pre_process["long_common_nm"].apply(pre_process)
    df_for_existing_tests_pre_process["long_common_nm"] = df_for_existing_tests_pre_process["long_common_nm"].apply(pre_process)
    excel_validated_response = get_matched_unmatched_data()
    add_flag = "UPDATE lab.lab_test_comp_ref SET is_matched = true WHERE long_common_nm in %(matched)s"
    matched = tuple([test['long_common_nm'] for test in excel_validated_response['matched']])
    sql_parameter = {'matched': matched}
    cursor.execute(add_flag, sql_parameter)
    suggestions = get_suggestions(conn)
    excel_validated_response["suggestions"] = suggestions
    #return excel_validated_response
    print(excel_validated_response)


@app.route("/fetchMatchedAndUnmatched", methods=['POST'])
def fetch_matched_and_unmatched():
    # Spawn thread to process the data
    request_data = request.get_json()
    req_url_rule = request.url_rule
    thread_for_processing = Thread(target=compare_excel_uploaded_tests_with_database_tests, args=(request_data, req_url_rule))
    thread_for_processing.start()
    response_for_given_request = ["Please Wait For Few Minutes", 200]
    return jsonify(response_for_given_request[0]), response_for_given_request[1]


if __name__ == '__main__':
    app.run(host="192.168.2.72", debug=True)

