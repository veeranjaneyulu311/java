import atexit
import datetime
import pandas as pd
import psycopg2 as psycopg2
from psycopg2.extras import RealDictCursor
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from itertools import chain
from collections import defaultdict


def connect_local():
    return psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432")


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


dict_id = {}


def user_id(dict_id, key):
    if key in dict_id:
        return dict_id
    else:
        dict_id[key] = {'drugid-type': {}, 'drugid-intr': {}, 'type-route': {}, 'type-strength': {}}
        return dict_id


# def drug_type(dict_id, id,  key, types):
#     if key in dict_id[id]['drugid-type']:
#         dict_id[id]['drugid-type'][key] = types
#         return dict_id
#     else:
#         dict_id[id]['drugid-type'][key] = types
#         return dict_id


# def drug_instr(dict_id, id, key, types):
#     if key in dict_id[id]['drugid-instr']:
#         dict_id[id]['drugid-instr'][key] = types
#         return dict_id
#     else:
#         dict_id[id]['drugid-type'][key] = types
#         return dict_id


def get_drug_type_from_id():
    global dict_id;
    conn = connect_dev()
    cursor = conn.cursor()
    main_query = "SELECT created_usr_id, drug_id, drug_type_id FROM opd.patient_prescription_drugs_trans "
    # sql_parameters = {'doctorlist': tuple(doctors)}
    cursor.execute(main_query)
    dft = pd.DataFrame(cursor.fetchall(), columns=['created_usr_id', 'drug_id', 'drug_type_id'])
    c = dft.groupby(['created_usr_id','drug_id'])['drug_type_id'].value_counts()
    cc = c.groupby('drug_id').head(3)
    result = [label for label, value in cc.iteritems()]
    df1 = pd.DataFrame(result, columns=['created_usr_id', 'drug_id', 'drug_type_id'])
    # l = df1.groupby(['created_usr_id', 'drug_id'])
    df1 = dict(df1.groupby(['created_usr_id', 'drug_id'])['drug_type_id'].apply(list))
    for k, v in df1.items():
        created_user_id, drug_id = k
        user_id(dict_id, created_user_id)
        dict_id[created_user_id]['drugid-type'][drug_id] = v


def get_instructions_from_drug_id():
    global df2
    global dict_id
    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    main_query = "SELECT created_usr_id, drug_id, instruction FROM opd.patient_prescription_drugs_trans"
    cursor.execute(main_query)
    dft = pd.DataFrame(cursor.fetchall(), columns=['created_usr_id', 'drug_id', 'instruction'])
    # getting top 3 instructions for each drug_id
    all_instructions = dft.groupby(['created_usr_id', 'drug_id'])['instruction'].value_counts()
    top_instructions = all_instructions.groupby(['drug_id']).head(3)
    top_instructions_as_result = [label for label, value in top_instructions.iteritems()]
    df = pd.DataFrame(top_instructions_as_result, columns=['created_usr_id', 'drug_id', 'instruction'])
    df2 = dict(df.groupby(['created_usr_id', 'drug_id'])['instruction'].apply(list))
    for k, v in df2.items():
        created_user_id, drug_id = k
        user_id(dict_id, created_user_id)
        dict_id[created_user_id]['drugid-intr'][drug_id] = v
    print(dict_id)



# def combine():
#     global dict3
#     dict3 = defaultdict(list)
#     for k, v in chain(df1.items(), df2.items()):
#         dict3[k].append(v)
#     # for k, v in dict3.items():
#     #     print(k, v)


# def getdict():
#     global dict_id;
#     for k, v in dict3.items():
#         created_user_id, drug_id = k
#         val = v
#         user_id(dict_id, created_user_id)
#         # if len(val) == 2:
#         #     types = val[0]
#         # else:
#         #     types
#         drug_type(dict_id, created_user_id, drug_id, val[0])
#         drug_instr(dict_id, created_user_id, drug_id, val[0])
#     print(dict_id)


get_drug_type_from_id()
get_instructions_from_drug_id()
#combine()
#getdict()
