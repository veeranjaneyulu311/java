import atexit
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

app = Flask(__name__)

next_date = datetime.date(2019, 5, 30)


def scheduler_example():
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"), "1min")
    today_date = datetime.date.today()
    #today_date = datetime.date(2019, 5, 30)
    global next_date
    # for employees having data less than one month
    query_to_fetch_doctor_list_for_one_month = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm >= CURRENT_DATE -INTERVAL '1MONTH'"

    # for employees having data more than one month and less than 6 months
    if today_date.day == 10:
        query_to_fetch_doctor_list_for_six_months = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '6 MONTHS' and CURRENT_DATE -INTERVAL '1MONTH'"
    # for employees having data more than  6 months and less than one year
    if today_date == datetime.date(2019, 5, 30):
        query_to_fetch_doctor_list_for_one_year  = "select ppdt.created_usr_id, ppdt.created_dttm, ppdt.rn from(select created_usr_id, created_dttm, row_number() over (partition by created_usr_id order by created_dttm) as rn from opd.patient_prescription_drugs_trans)  as ppdt where ppdt.rn=1 and ppdt.created_dttm between CURRENT_DATE -INTERVAL '12 MONTHS' and CURRENT_DATE -INTERVAL '6 MONTHs'"

        if next_date.month in [3, 5, 6, 7, 8, 10, 11]:
            next_date = next_date + datetime.timedelta(days=92)
        elif next_date.month in [4, 9]:
            next_date = next_date + datetime.timedelta(days=91)
        elif next_date.month in [12, 1]:
            if next_date.year/4 == 0:
                next_date = next_date + datetime.timedelta(days=91)
            if next_date.year/4 != 0:
                next_date = next_date + datetime.timedelta(days=90)
        elif next_date.month is 2:
            if next_date.year%4 == 0:
                next_date = next_date + datetime.timedelta(days=90)
            if next_date.year%4 != 0:
                next_date = next_date + datetime.timedelta(days=89)

    # for employees having data more than one year
    if today_date == datetime.date(2019, 4, 29):

        print("6 months")


def close_all():
    scheduler.shutdown()
    print("stopped")


if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon='True')
    # The job will be executed on November 6th, 2009
    # scheduler.add_job(scheduler_example,  'interval', days=1, start_date='2019-04-27 00:00:00')
    scheduler.add_job(scheduler_example, 'interval', seconds=2)
    scheduler.start()
    atexit.register(close_all)
    app.run()
