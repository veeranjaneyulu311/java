import time

import psycopg2 as psycopg2
import pandas as pd
from fuzzywuzzy import fuzz, utils

query_for_test_ref = "SELECT long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, test_rank FROM lab.lab_test_ref where isactive is true"
query_for_org_test_xref = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref as lotx inner join lab.lab_test_ref as ltr on lotx.test_id=ltr.test_id"


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


matched_test_names = []


def pre_process(x):
    ts = utils.full_process(x, force_ascii=True)
    tokens = ts.split()
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()



def comparing():
    global matched_test_names
    conn = connect_dev()
    cursor = conn.cursor()
    cursor.execute(query_for_org_test_xref)
    df_xref = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    cursor.execute(query_for_test_ref)
    df_ref = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    df_xref_proc = df_xref.copy()
    # print(df_xref)
    df_ref["long_common_nm"] = df_ref["long_common_nm"].apply(pre_process)
    df_xref_proc["long_common_nm"] = df_xref_proc["long_common_nm"].apply(pre_process)
    print(df_xref)
    print(df_ref)

    # print(df_ref)
    # x = df_ref[(df_ref.is_panel == False) & (df_ref.order_obs == "Both") & (df_ref.loinc_system == "Urine") & (df_ref.time_aspect == "Pt") & ((df_ref.investigation_department.isnull()) | (df_ref.investigation_department == "None"))]
    # print(len(x.index))
    # i = 1
    # for index_given, row_given in df_xref.iterrows():
    #     df_filtered = df_ref[(df_ref.is_panel == row_given['is_panel']) & (df_ref.order_obs == row_given['order_obs']) & (df_ref.loinc_system == row_given['loinc_system']) & (df_ref.time_aspect == row_given['time_aspect']) & ((df_ref.investigation_department == row_given['investigation_department']) | (df_ref.investigation_department.isnull()))]
    #     print(row_given.to_dict(), i, len(df_filtered.index))
    #     i = i+1
    #     break


def delete():
    full_process = False
    x="true" if full_process else "false"
    print(x)


delete()
