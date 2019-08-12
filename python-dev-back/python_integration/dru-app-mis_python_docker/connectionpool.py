import time
import traceback
import psycopg2
import constants
import controller
from psycopg2 import pool


#: It establishes connection pool with the configured database
try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    controller.logger.info("Error while connecting to PostgreSQL", error)


#: It invoke's the respective function of requested api by passing the connection object obtained from connection pool.
#: It add's validations, response data, status code, error messages to the response
#: It also performs transaction management.
#: It log's the failed request's
def transaction_connection_pool(func):
    def wrap(req, token):
        try:
            # Use getconn() method to Get Connection from connection pool
            ps_connection = threaded_postgreSQL_pool.getconn()
            request_data = req.get_json()
            result = func(ps_connection, request_data)
            ps_connection.commit()
            threaded_postgreSQL_pool.putconn(ps_connection)
            validations = [{'message': constants.DATA_FETCH_SUCCESSFULLY, 'errCode': constants.RES_CODE_MIS1006}]
            response = {'data': result, 'responseCode': constants.RES_CODE_SUCCESS, 'responseMessage': constants.DATA_FETCH_SUCCESSFULLY, 'validations': validations}
            return [response, 200]
        except Exception:
            ps_connection.rollback()
            threaded_postgreSQL_pool.putconn(ps_connection)
            # This method logg's the every method in this whole application only at the time of Exception
            controller.logger.info("{'transactionId':%s,'systemName':%s,'moduleName':'MIS','timeStamp':%s,'apiName':%s,'status':'ERROR','exception':%s,'payLoad':[%s]}",token, controller.get_computer_name(), time.strftime('%Y-%m-%d %H:%M:%S'), req.url_rule, traceback.format_exc(), req.get_json())
            response = {'responseCode': constants.RES_CODE_FAILURE, 'responseMessage': constants.OPERATION_FAILED_GENERIC_MESSAGE, 'validations': {'errCode': constants.RES_CODE_OFG001, 'errMessage': constants.OPERATION_FAILED_GENERIC_MESSAGE}, 'data': ''}
            return [response, 500]
    return wrap


