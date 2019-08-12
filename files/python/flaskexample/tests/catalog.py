# v2
import json

import psycopg2 as psycopg2
import pandas as pd
from flask import Flask, request
from flask.json import jsonify
from fuzzywuzzy import fuzz, utils
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
# used in first api
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


query_for_user_uploaded_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref"
query_for_mapped_and_unmapped_tests = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank , 'mapped' as type FROM lab.lab_org_test_xref lotx inner join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id union all (SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank,'unmapped' as type FROM lab.lab_org_test_xref lotx right join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id where lotx.test_id is null and ltr.isactive is true order by test_rank)"

# delete below query
# query_for_mapped_and_unmapped_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_original_ref"


# This function establishes connection to database
def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


# delete this function after testing
def connect_local():
    return psycopg2.connect(database="postgres", user="postgres", password="admin", host="localhost", port="5432")


# it will be used by first api for exact matches
# it will pre process all test names for comparision and reduces comparision time
# it will convert test names to lowercase(Case Insensitivity)
# orders all words of test names in ascending order(Removing Words Order dependency)
def pre_process(long_common_nm):
    ts = utils.full_process(long_common_nm, force_ascii=True)
    stop_words = ['is', 'in', 'the']
    tokens = ts.split()
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
        # It will filter all tests matching below columns
        # 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs' from db data
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

    s = "UPDATE lab.lab_test_comp_ref SET matched = True WHERE long_common_nm in % (tests)s"

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


# first api:  this function will compare all uploaded tests with available tests
@app.route("/test")
def compare_excel_uploaded_tests_with_database_tests():
    global df_for_uploaded_tests
    global df_for_uploaded_tests_pre_process
    global df_for_existing_tests
    global df_for_existing_tests_pre_process
    conn = connect_dev()
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
    return jsonify({"data": excel_validated_response, "Response code": "E200", "Response Message": "FETCHED SUCCESSFULLY"})


# case-1 it will apply non selected columns exactly
def apply_non_selected_exactly(df_after_tests_matching, unmatched_test_details, filters_selected):
    filters_selected = ['is_panel']
    all_filters = ['loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs']
    for filter in all_filters:
        if filter not in filters_selected:
            df_after_tests_matching = df_after_tests_matching[df_after_tests_matching[filter] == unmatched_test_details[filter]]
    return df_after_tests_matching


# this function gives all possible combinations matching columns
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


# second api
@app.route('/fetchApproximate', methods=['POST'])
def probabilty_for_unmatched():
    # output 1
    approximately_matched_tests_with_remaining_cols_exactly_match = []
    data = None
    request_data = request.get_json()
    unmatched_test_name = request_data['unmatched_test_name']
    filters_selected = None
    # fetch given unmatched  test details
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_to_fetch_unmatched_test_details = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref where long_common_nm ilike %(test_name)s "
    # query_to_fetch_unmatched_test_details = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref where long_common_nm = %(test_name)s "
    query_parameter = {'test_name': unmatched_test_name}
    cursor.execute(query_to_fetch_unmatched_test_details, query_parameter)
    unmatched_test_details = dict(cursor.fetchone())
    print(unmatched_test_details)

    # fetch all the mapped and unmapped table data
    cursor.execute(query_for_mapped_and_unmapped_tests)
    # df_for_tests_in_db = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank', 'type'])
    df_for_tests_in_db = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs'])

    # pre processing the data for comparision
    df_for_tests_in_db_process = df_for_tests_in_db.copy()
    df_for_tests_in_db_process["long_common_nm"] = df_for_tests_in_db_process["long_common_nm"].apply(pre_process)
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

    def response_from_dataframe(df):
        nonlocal data
        if unmatched_test_details['loinc_system'].lower() not in ['bld', 'blood', 'ser', 'serum', 'plasma']:
            df = df[df.loinc_system.str.lower() == unmatched_test_details['loinc_system'].lower()]
        df = df[df.loinc_system.str.lower().isin(['bld', 'blood', 'ser', 'serum', 'plasma'])]
        df = df[((df.order_obs.str.lower() == unmatched_test_details['order_obs'].lower()) | (df.order_obs.str.lower() == 'both')) & (df.time_aspect.str.lower() == unmatched_test_details['time_aspect'].lower())]
        df1 = df_for_tests_in_db[df_for_tests_in_db.index.isin(df.index)]
        if not df1.empty:
            data = json.loads(df1.to_json(orient='records'))

    def filter_fn(tests_details):
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
            df_for_approximately_matched = df_for_tests_in_db_process[df_for_tests_in_db_process.apply(filter_fn, axis=1)]
            # check if approximate matches exist
            if not df_for_approximately_matched.empty:
                # output 4
                # filtering the data: it calls a function to exclude user selected columns and apply remaining exactly
                approxi_matched_tests_excluding_selected_cols = apply_non_selected_exactly(df_for_approximately_matched, unmatched_test_details, filters_selected)
                if approxi_matched_tests_excluding_selected_cols.empty:
                    # output 5
                    approx_combinations = check_for_combinations_matched(df_for_approximately_matched, unmatched_test_details)
                    if approx_combinations.empty:
                        print("no matchings")
                    else:
                        response_from_dataframe(approx_combinations)
                else:
                    response_from_dataframe(approxi_matched_tests_excluding_selected_cols)
            else:
                print("no matchings")
        else:
            # filtering the data:  it calls a function to exclude user selected columns and apply remaining exactly
            # output 2
            exactly_matched_tests_excluding_selected_cols = apply_non_selected_exactly(df_for_exact_matched, unmatched_test_details, filters_selected)
            if exactly_matched_tests_excluding_selected_cols.empty:
                # output 3
                exact_combinations = check_for_combinations_matched(df_for_exact_matched, unmatched_test_details)
                if exact_combinations.empty:
                    print("no matchings")
                else:
                    response_from_dataframe(exact_combinations)
            else:
                response_from_dataframe(exactly_matched_tests_excluding_selected_cols)
    print(approximately_matched_tests_with_remaining_cols_exactly_match)
    print(data)
    if len(approximately_matched_tests_with_remaining_cols_exactly_match) == 0:
        suggest = {'test': unmatched_test_name, 'approx': data}
    else:
        suggest = {'test': unmatched_test_name, 'approx': approximately_matched_tests_with_remaining_cols_exactly_match}
    return jsonify(suggest)


if __name__ == '__main__':
    app.run(debug=True)
