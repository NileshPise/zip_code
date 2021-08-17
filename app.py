#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask,request
from flask_cors import CORS
from flask import jsonify
import pymysql
import configparser
import logging

app = Flask(__name__)
CORS(app)

def get_logger(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

log = get_logger('__main__')
log.warning(' Updating secrete key')
# secrete key for app
app.config.update(SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/')
log.info(' Started reading database config file')
path = os.getcwd()
file_path = os.path.join(path, 'database.ini')
config = configparser.ConfigParser()
config.read(file_path)

host = config['mysql']['host']
user = config['mysql']['user']
passwd = config['mysql']['password']
db = config['mysql']['db']

log.info(" Started database connection check")
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='zip_code',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_data(in_zip_code):
    cursor = connection.cursor()
    sql = "SELECT city, state_name FROM zip_code WHERE zip = %s"
    cursor.execute(sql, (in_zip_code,))
    result = cursor.fetchone()
    log = get_logger(' Mysql')
    log.info(result)
    cursor.close()
    return result

@app.route('/zip_code', methods = ['POST'])
def zip_code():
    in_zip_code = request.get_json(force= True)
    in_zip_code = in_zip_code['zip']
    return jsonify(get_data(in_zip_code=in_zip_code))


if __name__ == "__main__":
    app.run(host='localhost',port=5025,debug=False,threaded=True)

