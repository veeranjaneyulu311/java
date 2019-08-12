import json

import psycopg2 as psycopg2
import pandas as pd

from fuzzywuzzy import fuzz


query_for_test_ref = "SELECT long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, test_rank FROM lab.lab_test_ref"
query_for_org_test_xref = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref as lotx inner join lab.lab_test_ref as ltr on lotx.test_id=ltr.test_id"


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


input_list = {}
matched_test_names = []
matched_samples = []
matched_dept = []
matched_time = []
matched_is_panel = []
matched_order_obs = []

i = 0


# comparing the user given excel data with available data
def comparing():
    global i
    conn = connect_dev()
    cursor = conn.cursor()
    cursor.execute(query_for_org_test_xref)
    df_xref = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    cursor.execute(query_for_test_ref)
    df_ref = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    df_xref['words'] = df_xref['long_common_nm'].str.lower().str.split(" ")
    df_xref_converted = df_xref.applymap(lambda s: s.lower() if type(s) == str else s)

    for index_given, row_given in df_xref_converted.iterrows():
        matched_test_names_bool = True
        matched_samples_bool = True
        matched_dept_bool = True
        matched_time_bool = True
        matched_is_panel_bool = True
        matched_order_obs_bool = True

        i = i+1
        for index_avail, row_avail in df_ref.iterrows():
                # for word in row_given['words']:
                # word = row_given['words']
                if fuzz.token_set_ratio(row_given['long_common_nm'], row_avail['long_common_nm']) > 90:
                    # print(row_given.to_dict(), row_avail.to_dict())
                    if matched_test_names_bool:
                        matched_test_names.append(row_given.to_dict())
                        matched_test_names_bool = False
                    if (row_avail['loinc_system'] is not None) and (row_given['loinc_system'] in row_avail['loinc_system'].lower()):
                        if matched_samples_bool:
                            matched_samples.append(row_given.to_dict())
                            matched_samples_bool = False
                        if (row_avail['investigation_department'] is not None) and (row_given['investigation_department'] in row_avail['investigation_department'].lower()):
                            if matched_dept_bool:
                                matched_dept.append(row_given.to_dict())
                                matched_dept_bool = False
                            if (row_avail['time_aspect'] is not None) and (row_given['time_aspect'] in row_avail['time_aspect'].lower()):
                                if matched_time_bool:
                                    matched_time.append(row_given.to_dict())
                                    matched_time_bool = False
                                if (row_avail['is_panel'] is not None) and (row_given['is_panel'] == row_avail['is_panel']):
                                    if matched_is_panel_bool:
                                        matched_is_panel.append(row_given.to_dict())
                                        matched_is_panel_bool = False
                                    if (row_avail['order_obs'] is not None) and (row_given['order_obs'] in row_avail['order_obs'].lower()):
                                        if matched_order_obs_bool:
                                            matched_order_obs.append(row_given.to_dict())
                                            matched_order_obs_bool = False

        print(matched_test_names)
        print(matched_samples)
        print(matched_dept)
        print(matched_time)
        print(matched_is_panel)
        print(matched_order_obs)
        if i == 2:
            break


#comparing()


def js():
    blog = {'long_common_nm': 'Basophils', 'loinc_system': 'Bld', 'investigation_department': 'HEMATOLOGY', 'time_aspect': 'Pt', 'is_panel': False, 'order_obs': 'Observation'}
    print(json.dumps(blog))


js()