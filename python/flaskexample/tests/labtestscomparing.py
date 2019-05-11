import time

import psycopg2 as psycopg2
import pandas as pd
from fuzzywuzzy import fuzz,utils

query_for_test_ref = "SELECT long_common_nm, loinc_system, investigation_department, time_aspect, is_panel, order_obs, test_rank FROM lab.lab_test_ref where isactive is true"
query_for_org_test_xref = "SELECT ltr.long_common_nm, ltr.loinc_system, ltr.investigation_department, ltr.time_aspect, ltr.is_panel, ltr.order_obs, ltr.test_rank FROM lab.lab_org_test_xref as lotx inner join lab.lab_test_ref as ltr on lotx.test_id=ltr.test_id LIMIT 500"


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


matched_test_names_bool = True
df_xref = None
df_xref_proc = None
matched_test_names = []
unmatched_test_names = []


def pre_process(x):
    ts = utils.full_process(x, force_ascii=True)
    tokens = ts.split()
    sorted_string = u" ".join(sorted(tokens))
    return sorted_string.strip()


def mapping_test_name(filtered_rows, ind):
    global matched_test_names_bool
    global matched_test_names
    if fuzz.ratio(df_xref_proc.at[ind, 'long_common_nm'], filtered_rows) >= 100:
        print("Matched tests----- EXCEL: " + str(df_xref.at[ind, 'long_common_nm']) + " DB: " + filtered_rows)
        if matched_test_names_bool:
            matched_test_names_bool = False
            matched_test_names.append(df_xref.loc[ind].to_dict())


def comparing_time_improved():
    global matched_test_names_bool
    global matched_test_names
    global df_xref
    global df_xref_proc
    conn = connect_dev()
    cursor = conn.cursor()
    cursor.execute(query_for_org_test_xref)
    df_xref = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    cursor.execute(query_for_test_ref)
    df_ref = pd.DataFrame(data=cursor.fetchall(), columns=['long_common_nm', 'loinc_system', 'investigation_department', 'time_aspect', 'is_panel', 'order_obs', 'test_rank'])
    start = time.time()
    df_xref_proc=df_xref.copy()
    df_ref["long_common_nm"] = df_ref["long_common_nm"].apply(pre_process)
    df_xref_proc["long_common_nm"] = df_xref_proc["long_common_nm"].apply(pre_process)
    i=1
    for ind in df_xref.index:
        df_filtered = df_ref[(df_ref.is_panel == df_xref.at[ind, 'is_panel']) & (df_ref.order_obs == df_xref.at[ind, 'order_obs']) & (df_ref.loinc_system == df_xref.at[ind, 'loinc_system']) & (df_ref.time_aspect == df_xref.at[ind, 'time_aspect']) & ((df_ref.investigation_department == df_xref.at[ind, 'investigation_department']) | (df_ref.investigation_department.isnull()))]
        matched_test_names_bool = True
        print("filtered rows for this test: "+str(len(df_filtered.index)))
        if len(df_filtered.index) != 0:
            df_filtered['long_common_nm'].apply(func=mapping_test_name, args=[ind])
        # if i == 3:
        #     break
        # i = i + 1
        if matched_test_names_bool:
            unmatched_test_names.append(df_xref.loc[ind].to_dict())

    end = time.time()
    # print(len(matched_test_names))
    print((end -start)/60)


comparing_time_improved()
