import time
import psycopg2 as psycopg2
import pandas as pd
from fuzzywuzzy import fuzz, utils

# query_for_test_ref = "SELECT long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, test_rank FROM lab.lab_test_ref where isactive is true order by test_rank"
# query_for_org_test_xref = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref as lotx inner join lab.lab_test_ref as ltr on lotx.test_id=ltr.test_id LIMIT 300"

query_for_user_uploaded_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref"
query_for_mapped_and_unmapped_tests = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref lotx inner join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id union all (SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref lotx right join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id where lotx.test_id is null and ltr.isactive is true order by test_rank)"


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


approximately_matched_tests_bool = None
exactly_matched_tests_bool = None
df_for_uploaded_tests = None
df_for_uploaded_tests_pre_process = None
df_for_existing_tests = None
df_for_existing_tests_pre_process = None
exactly_matched_tests = []
approximately_matched_tests = []
unmatched_tests = []


# it will pre process all test names for comparision and reduces comparision time
def pre_process(long_common_nm):
    ts = utils.full_process(long_common_nm, force_ascii=True)
    tokens = ts.split()
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


# This function will filter the data and checks for available matches in filtered data
def get_matched_unmatched_data():
    global approximately_matched_tests_bool
    global exactly_matched_tests_bool
    global exactly_matched_tests
    global approximately_matched_tests
    global unmatched_tests
    for uploaded_test_index in df_for_uploaded_tests.index:
        df_for_existing_tests_pre_process_filtered = df_for_existing_tests_pre_process[(df_for_existing_tests_pre_process.is_panel == df_for_uploaded_tests.at[uploaded_test_index, 'is_panel']) & (df_for_existing_tests_pre_process.order_obs == df_for_uploaded_tests.at[uploaded_test_index, 'order_obs']) & (df_for_existing_tests_pre_process.loinc_system == df_for_uploaded_tests.at[uploaded_test_index, 'loinc_system']) & (df_for_existing_tests_pre_process.time_aspect == df_for_uploaded_tests.at[uploaded_test_index, 'time_aspect']) & ((df_for_existing_tests_pre_process.investigation_department == df_for_uploaded_tests.at[uploaded_test_index, 'investigation_department']) | (df_for_existing_tests_pre_process.investigation_department.isnull()))]
        exactly_matched_tests_bool = True
        approximately_matched_tests_bool = True
        print("No.Of filtered rows for matching this test: "+str(len(df_for_existing_tests_pre_process_filtered.index)))
        # verifying weather any tests are available for comparision
        # if available, compare each test name of filtered data with the uploaded test name
        if len(df_for_existing_tests_pre_process_filtered.index) != 0:
            df_for_existing_tests_pre_process_filtered['long_common_nm'].apply(func=check_for_matches_exist, args=[uploaded_test_index])

        # condition to check exactly matched or not
        if not exactly_matched_tests_bool:
            exactly_matched_tests.append(df_for_uploaded_tests.loc[uploaded_test_index].to_dict())
        # condition to check approximately matched or not
        elif not approximately_matched_tests_bool:
            approximately_matched_tests.append(df_for_uploaded_tests.loc[uploaded_test_index].to_dict())
        else:
            print("Un Matched tests----- EXCEL: " + str(df_for_uploaded_tests.at[uploaded_test_index, 'long_common_nm']))
            unmatched_tests.append(df_for_uploaded_tests.loc[uploaded_test_index].to_dict())


def check_for_matches_exist(test_name_in_filtered_data, uploaded_test_index):
    global exactly_matched_tests_bool
    global approximately_matched_tests_bool
    # check for exact match
    if df_for_uploaded_tests_pre_process.at[uploaded_test_index, 'long_common_nm'] == test_name_in_filtered_data:
        print("Exactly Matched tests----- EXCEL: " + str(df_for_uploaded_tests.at[uploaded_test_index, 'long_common_nm']) + " DB: " + test_name_in_filtered_data)
        if exactly_matched_tests_bool:
            exactly_matched_tests_bool = False
    elif fuzz.ratio(df_for_uploaded_tests_pre_process.at[uploaded_test_index, 'long_common_nm'], test_name_in_filtered_data) >= 60:
        print("Approximately Matched tests----- EXCEL: " + str(df_for_uploaded_tests.at[uploaded_test_index, 'long_common_nm']) + " DB: " + test_name_in_filtered_data)
        if approximately_matched_tests_bool:
            approximately_matched_tests_bool = False


# this function will compare all uploaded tests with available tests
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
    df_for_existing_tests = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    start = time.time()
    # pre process both data frames to reduce processing time during comparision
    df_for_uploaded_tests_pre_process = df_for_uploaded_tests.copy()
    df_for_existing_tests_pre_process = df_for_existing_tests.copy()
    df_for_uploaded_tests_pre_process["long_common_nm"] = df_for_uploaded_tests_pre_process["long_common_nm"].apply(pre_process)
    df_for_existing_tests_pre_process["long_common_nm"] = df_for_existing_tests_pre_process["long_common_nm"].apply(pre_process)
    get_matched_unmatched_data()
    end = time.time()
    print("Time Taken For Execution: ", (end - start)/60)
    print(len(exactly_matched_tests))
    print(len(approximately_matched_tests))
    print(len(unmatched_tests))


compare_excel_uploaded_tests_with_database_tests()
