from flask import Flask, request, render_template, send_from_directory
from flask_apscheduler import APScheduler
from gsm import SIM800L
from db import db_ops
from datetime import datetime
import zoneinfo

import os 
import time
import logging

con_phonenumber = "YOUR_MOBILE_NUMBER"
SIM800L = SIM800L("YOUR_SERIAL_PORT")

def db_init():
    cwd = os.getcwd()
    database = cwd + '/orangeGSM.db'
    # create a database connection
    try: 
        open(database)
    except:
        conn = db_ops.create_connection(database)
        db_ops.create_db_schema(conn)          
    conn = db_ops.create_connection(database)
    return conn

def db_write(sms):
    conn = db_init()
    with conn:
        #message ('TELE_NUMBER', 'RECEIVED_DATE', RECEIVED_TIME, 'MESSAGE', Action)
        db_ops.create_entry(conn, sms)
    conn.close()

app = Flask(__name__)

def getsmsTask():
    #db_write(SIM800L.read_and_delete_all)
    #message_count = SIM800L.get_msgid()
    SIM800L.read_sms(1)
    for x in range(100):
        x += 1
        message = SIM800L.read_sms(x)
        if not message:
            break
        db_write(message)
        SIM800L.delete_sms(x)
        time.sleep(1)    

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def hello():

    conn = db_init()
    return render_template("index.html", phonenumber=con_phonenumber, db_data=db_ops.read_entries(conn));

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route("/send", methods=["GET", "POST"])
def sendsms():
    SENDSTATUS = "ERROR"
    if request.method == "POST":
        req = request.form     
        SENDSTATUS = SIM800L.send_sms(req['Phonenumber'],req['SMSText'])
    conn = db_init()
    send_message = []
    send_message.append(req['Phonenumber'])
    send_message.append(datetime.today().strftime("%y/%m/%d"))
    send_message.append( datetime.today().strftime("%H:%M:%S"))
    send_message.append(req['SMSText'])
    send_message.append('send')
    db_write(send_message)
    return render_template("index.html", phonenumber=con_phonenumber, db_data=db_ops.read_entries(conn), SENDSTATUS=SENDSTATUS)

scheduler = APScheduler()
scheduler.add_job(id = 'Scheduled SMS Task', func=getsmsTask, trigger="interval", seconds=60, timezone='utc')
scheduler.start()
app.logger.info("Scheduled SMS Task: OK")

# We check if we are running directly or not
if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.run(debug=False, port=8080, host='0.0.0.0')
    app.logger.info("OrangeGSM Started.")

#start via gunicorn3  --bind 0.0.0.0:8080 --access-logfile - app:app    