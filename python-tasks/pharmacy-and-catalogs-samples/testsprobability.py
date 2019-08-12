# v1

import time
import psycopg2 as psycopg2
import pandas as pd
from fuzzywuzzy import fuzz, utils

# query_for_test_ref = "SELECT long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, test_rank FROM lab.lab_test_ref where isactive is true order by test_rank"
# query_for_org_test_xref = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref as lotx inner join lab.lab_test_ref as ltr on lotx.test_id=ltr.test_id LIMIT 300"
from psycopg2.extras import RealDictCursor

query_for_user_uploaded_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref"
# query_for_mapped_and_unmapped_tests = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank , 'mapped' as type FROM lab.lab_org_test_xref lotx inner join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id union all (SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank,'unmapped' as type FROM lab.lab_org_test_xref lotx right join lab.lab_test_ref  ltr on lotx.test_id=ltr.test_id where lotx.test_id is null and ltr.isactive is true order by test_rank)"
query_for_mapped_and_unmapped_tests = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_original_ref"


class ResponseForExcelValidation(Resource):

    def __init__(self, data, response_code, response_message):
        self.data = data
        self.response_code = response_code
        self.response_message = response_message


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ResponseForExcelValidation):
            return {
                'data': obj.data,
                'response_code': obj.response_code,
                'response_message': obj.response_message,
            }
        return super(MyJSONEncoder, self).default(obj)



app.add_resource(ResponseForExcelValidation, '/eqtl/eqtlsbygene')
app.json_encoder = EqtlJSONEncoder


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


def connect_local():
    return psycopg2.connect(database="postgres", user="postgres", password="admin", host="localhost", port="5432")


# used in first api
# used as flags for checking a test matched or not
approximately_matched_tests_bool = None
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
# excel validated data
excel_validated_response = None

# used in second api
unmatched_test_details = None


# it will be used by first api
# it will pre process all test names for comparision and reduces comparision time
# it will convert test names to lowercase(Case Insensitivity)
# orders all words of test names in ascending order(Removing Words Order dependency)
def pre_process(long_common_nm):
    ts = utils.full_process(long_common_nm, force_ascii=True)
    tokens = ts.split()
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


# it will be used by first api
# This function will filter the data and checks for available matches in filtered data
def get_matched_unmatched_data():
    global approximately_matched_tests_bool
    global exactly_matched_tests_bool
    global exactly_matched_tests
    global approximately_matched_tests
    global unmatched_tests
    global excel_validated_response
    # This loop iterates for each test  uploaded by user
    for uploaded_test_index in df_for_uploaded_tests.index:
        # It will filter all tests matching below columns
        # 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs' from db data
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

    excel_validated_response = {"matched": exactly_matched_tests, "approximate": approximately_matched_tests, "unmatched": unmatched_tests}

# it will be used by first api
# It has all the conditions for exact and approximate matchings
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


# first api:  this function will compare all uploaded tests with available tests
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
    start = time.time()
    # pre process both data frames to reduce processing time during comparision
    df_for_uploaded_tests_pre_process = df_for_uploaded_tests.copy()
    df_for_existing_tests_pre_process = df_for_existing_tests.copy()
    df_for_uploaded_tests_pre_process["long_common_nm"] = df_for_uploaded_tests_pre_process["long_common_nm"].apply(pre_process)
    df_for_existing_tests_pre_process["long_common_nm"] = df_for_existing_tests_pre_process["long_common_nm"].apply(pre_process)
    get_matched_unmatched_data()
    # end time calculate time taken
    end = time.time()
    print("Time Taken For Execution: ", (end - start)/60)
    print(len(exactly_matched_tests))
    print(len(approximately_matched_tests))
    print(len(unmatched_tests))


# case-1 it will apply non selected columns exactly
def apply_non_selected_exactly(df, exact):
    global unmatched_test_details
    all_filters = ['loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs']
    filters_selected = ['loinc_system']
    if exact:
        for filter in all_filters:
            if filter not in filters_selected:
                df = df[df[filter] == unmatched_test_details[filter]]
    return df


# this function gives all possible combinations matching columns
def check_for_combinations_matched(df_second):
    # tests with four columns matched
    df_for_test_and_sample_obs_dept_time = None
    df_for_test_and_sample_obs_dept_panel = None
    df_for_test_and_sample_obs_time_panel = None
    df_for_test_and_sample_dept_time_panel = None
    df_for_test_and_obs_dept_time_panel = None

    # tests with three columns matched
    df_for_test_and_sample_obs_dept = None
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
    df_for_test_and_sample_obs = None
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
            df_for_test_and_sample_obs_time = df_for_test_and_sample_obs[df_for_test_and_sample_obs['time_aspect']==unmatched_test_details['time_aspect']]
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

    print(df_for_test_and_sample_obs)
    print(df_for_test_and_sample_dept)
    print(df_for_test_and_sample_time)
    print(df_for_test_and_sample_panel)
    print(df_for_test_and_obs_dept)
    print(df_for_test_and_obs_time)
    print(df_for_test_and_obs_panel)
    print(df_for_test_and_dept_time)
    print(df_for_test_and_dept_panel)
    print(df_for_test_and_time_panel)

    print(df_for_test_and_sample_obs_dept)
    print(df_for_test_and_sample_obs_time)
    print(df_for_test_and_sample_obs_panel)
    print(df_for_test_and_sample_dept_time)
    print(df_for_test_and_sample_dept_panel)
    print(df_for_test_and_sample_time_panel)
    print(df_for_test_and_obs_dept_time)
    print(df_for_test_and_obs_dept_panel)
    print(df_for_test_and_obs_time_panel)
    print(df_for_test_and_dept_time_panel)

    print(df_for_test_and_sample_obs_dept_time)
    print(df_for_test_and_sample_obs_dept_panel)
    print(df_for_test_and_sample_obs_time_panel)
    print(df_for_test_and_sample_dept_time_panel)
    print(df_for_test_and_obs_dept_time_panel)

    print("end")


# second api
def probabilty_for_unmatched(unmatched_test_name):
    global unmatched_test_details

    # fetch given test details
    #conn = connect_dev()
    conn = connect_local()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # query_to_fetch_unmatched_test_details="select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref where long_common_nm = %(test_name)s "
    query_to_fetch_unmatched_test_details = "select long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs from lab.lab_test_comp_ref where long_common_nm = %(test_name)s "
    query_parameter = {'test_name': unmatched_test_name}
    cursor.execute(query_to_fetch_unmatched_test_details, query_parameter)
    unmatched_test_details = dict(cursor.fetchone())
    print(unmatched_test_details)

    # fetch all the mapped and unmapped table data
    cursor.execute(query_for_mapped_and_unmapped_tests)
    # df_for_tests_in_db = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank', 'type'])
    df_for_tests_in_db = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs'])
    # print(df_for_tests_in_db.head(4150))
    # exact matches for test
    df_for_exact_matched = df_for_tests_in_db[df_for_tests_in_db['long_common_nm'] == unmatched_test_name]

    # check matches availbale for exact
    if df_for_exact_matched.empty:
        print("no exact matches")
        # approx match if no exact matches
        df_for_approximately_matched = df_for_tests_in_db[df_for_tests_in_db.long_common_nm.str.contains(unmatched_test_name)]
        # check if approximate matches exist
        if df_for_approximately_matched.empty:
            pass
        else:
            df_for_approximately_matched_after_filters_apply = apply_non_selected_exactly(df_for_approximately_matched, True)
            if df_for_approximately_matched_after_filters_apply.empty:
                check_for_combinations_matched(df_for_approximately_matched)
            else:
                pass
        print(df_for_approximately_matched_after_filters_apply)
    else:
        print("exact matched")
        # print(df_for_exact_matched)
        check_for_combinations_matched(df_for_exact_matched)
        # df_after_applying_non_selected_exactly = apply_non_selected_exactly(df_for_exact_matched, True)
        # print(df_after_applying_non_selected_exactly)
        # if df_after_applying_non_selected_exactly.empty:
        #     print("all")
        #     df_after_levels = check_for_combinations_matched(df_for_exact_matched)
        #     print(df_after_levels)


probabilty_for_unmatched('first')
# compare_excel_uploaded_tests_with_database_tests()

