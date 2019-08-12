from flask import Flask, jsonify, request

from contant import RES_CODE_SUCCESS, DATA_FETCH_SUCCESSFULLY, RES_CODE_MIS1006
from dao import fetch_branch_wise_patient_count_dao, sample_api, fetch_branch_wise_patient_count_dao_pool


app = Flask(__name__)


@app.route('/fetchBranchWisePatientCount', methods=['POST'])
def fetch_branch_wise_patient_count():
        request_data = request.get_json()
        print(request_data)
        query_response = fetch_branch_wise_patient_count_dao(request_data)
        validations = [{'message': 'FETCHED SUCCESSFULLY', 'errCode': 'MIS10006'}]
        response_data = jsonify({'data': {'branchWiseList': query_response}, 'responseCode': RES_CODE_SUCCESS, 'responseMessage': DATA_FETCH_SUCCESSFULLY, 'validations': validations})
        return response_data


@app.route('/fetchBranchWisePatientCountPool', methods=['POST'])
def fetch_branch_wise_patient_count_pool():
        request_data = request.get_json()
        print(request_data)
        query_response = fetch_branch_wise_patient_count_dao_pool(request_data)
        validations = [{'message': DATA_FETCH_SUCCESSFULLY, 'errCode': RES_CODE_MIS1006}]
        response_data = jsonify({'data': {'branchWiseList': query_response[0], 'totalCount': query_response[1]}, 'responseCode': RES_CODE_SUCCESS, 'responseMessage': DATA_FETCH_SUCCESSFULLY, 'validations': validations})
        return response_data


@app.route('/sample', methods=['GET'])
def fetch_sample():
        response = sample_api()
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
