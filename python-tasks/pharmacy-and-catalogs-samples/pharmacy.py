from string import digits
import json
from flask import Flask, jsonify, request
import pandas as pd
import psycopg2 as pg
import re
import time
from fuzzywuzzy import utils, fuzz, process
from psycopg2.extras import  RealDictCursor

# app= Flask(__name__)
#query_for_importing_excel_uploaded_data= "SELECT drug_brand_nm, dose_nm, drug_type_nm, related_nm FROM public.drug_brand_comp_ref"
#query_for_importing_all_drugs_information = "SELECT  drug_brand_nm, dose_nm, drug_type_nm FROM public.drug_brand_ref"
#Function for connecting to the database


def connect_dev():
    return pg.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


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
        if 65 <= fuzz.ratio(brand_details['drug_brand_nm'], unmatched_brand_name_process) < 100:
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
            result = response_from_dataframe(df_for_approximately_matched_brands)
            return result, "unmatched"
        else:
                result = unmatched_brand_details
                return result, "notmatched"
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


def get_suggestions():
    # fetch given unmatched  test details
    response = {"matched": [], "unmatched": [], "notall": []}

    conn = connect_dev()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_to_fetch_unmatched_brand_details = "SELECT drug_brand_nm, dose_nm, drug_type_nm FROM drug_brand_comp_ref"
    cursor.execute(query_to_fetch_unmatched_brand_details)
    df_for_unmatched_brand_details = pd.DataFrame(data=cursor.fetchall(), columns=['drug_brand_nm', 'dose_nm', 'drug_type_nm'])
    # fetch all the mapped and unmapped table data
    query_for_drugs_in_db = "SELECT drug_brand_nm, dose_nm, drug_type_nm FROM drug_brand_ref "
    cursor.execute(query_for_drugs_in_db)
    df_for_db_drug_brand_details = pd.DataFrame(data=cursor.fetchall(),
                                                columns=['drug_brand_nm', 'dose_nm', 'drug_type_nm'])

    df_for_db_drug_brand_details_process = df_for_db_drug_brand_details.copy()
    df_for_db_drug_brand_details_process['drug_brand_nm'] = df_for_db_drug_brand_details_process['drug_brand_nm'].apply(pre_process)

    for unmatched_brand_index in df_for_unmatched_brand_details.index:
        unmatched_brand_details = df_for_unmatched_brand_details.loc[unmatched_brand_index].to_dict()
        result, is_matched = probabilty_for_unmatched(unmatched_brand_details, df_for_db_drug_brand_details, df_for_db_drug_brand_details_process)
        if is_matched == "matched":
            response["matched"].append(result)
        elif is_matched == "unmatched":
            unmatched_brand_details["suggest"] = result
            response["unmatched"].append(unmatched_brand_details)
        elif is_matched == "notall":
            response["notall"].append(result)

    print(response)


get_suggestions()
