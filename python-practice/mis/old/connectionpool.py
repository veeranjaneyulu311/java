import psycopg2
from psycopg2 import pool

from constants import DATA_FETCH_SUCCESSFULLY, RES_CODE_MIS1006, RES_CODE_SUCCESS, RES_CODE_FAILURE, \
    OPERATION_FAILED_GENERIC_MESSAGE, RES_CODE_OFG001

try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    print("Error while connecting to PostgreSQL", error)


def transaction_connection_pool(func):
    def wrap(req):
        try:
            # Use getconn() method to Get Connection from connection pool
            ps_connection = threaded_postgreSQL_pool.getconn()
            print("connected to dev database with connection pool")
            result = func(ps_connection, req)
            ps_connection.commit()
            threaded_postgreSQL_pool.putconn(ps_connection)
            validations = [{'message': DATA_FETCH_SUCCESSFULLY, 'errCode': RES_CODE_MIS1006}]
            response = {'data': result, 'responseCode': RES_CODE_SUCCESS, 'responseMessage': DATA_FETCH_SUCCESSFULLY, 'validations': validations}
            return [response, 200]
        except Exception as err:
            print(err)
            ps_connection.rollback()
            threaded_postgreSQL_pool.putconn(ps_connection)
            response = {'responseCode': RES_CODE_FAILURE, 'responseMessage': OPERATION_FAILED_GENERIC_MESSAGE, 'validations': {'errCode': RES_CODE_OFG001, 'errMessage': OPERATION_FAILED_GENERIC_MESSAGE}, 'data': ''}
            return [response, 500]
    return wrap


