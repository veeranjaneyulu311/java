import psycopg2
from psycopg2 import pool


try:
    threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 15, database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")
except (Exception, psycopg2.DatabaseError) as error :
    print("Error while connecting to PostgreSQL", error)
'''
finally:
    if threaded_postgreSQL_pool:
        threaded_postgreSQL_pool.closeall()
    print("Threaded PostgreSQL connection pool is closed")
'''


def transaction_connection_pool(func):
    def wrap(req):
        try:
            # Use getconn() method to Get Connection from connection pool
            ps_connection = threaded_postgreSQL_pool.getconn()
            print("connected to dev database with connection pool")
            result = func(ps_connection, req)
            ps_connection.commit()
            threaded_postgreSQL_pool.putconn(ps_connection)
            return result
        except Exception as e:
            print(e)
            ps_connection.rollback()
            threaded_postgreSQL_pool.putconn(ps_connection)
            return "failed"
    return wrap
