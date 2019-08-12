import psycopg2


# without connection pool


def connect_local():
    return psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1", port="5432")


def connect_dev():
    return psycopg2.connect(database="drucare_dev", user="drucare_emp", password="Dru@143$care", host="192.168.1.111", port="5432")


def transaction_management_local(func):
    def wrap():
        try:
            conn = connect_local()
            print("connected to local database")
            result = func(conn)
            conn.commit()
            return result
        except Exception as e:
            print(e)
            conn.rollback()
            return "failed"
    return wrap


def transaction_management_dev(func):
    def wrap(req):
        try:
            conn = connect_dev()
            print("connected to dev database without connection pool")
            result = func(conn, req)
            conn.commit()
            return result
        except Exception as e:
            print(e)
            conn.rollback()
            return "failed"
    return wrap
