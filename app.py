import csv
import os
import uuid
from flask_restful import Resource, Api , reqparse
from flask import Flask, jsonify, request
from flask_cors import CORS
from averagedata import FilterData

app = Flask(__name__)
CORS(app)
api = Api(app)
#define variable 
@app.route('/upload/csv', methods=['POST'])
def upload_csv():
    if request.method == 'POST':
        f = request.files['file']
        save_path = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        #delete all files in data folder
        #give admin permission to delete files
        os.system('sudo chmod 9010 data')
        #delete all files in data folder
        os.system('sudo rm -rf data/*')
        for file in os.listdir(save_path):
            os.remove(os.path.join(save_path, file))
        #save file in data folder
        file_path = os.path.join(save_path,'data.csv')
        f.save(file_path)
        data = FilterData(file_path).filter_data_asJson()
       #datasummary = FilterData(file_path).data_summary()
        #send as api response in json format
        return data
@app.route('/getsummary', methods=['GET'])
def get_summary():
    if request.method == 'GET':
        #find file in data folder
        save_path = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(file_path, 'data.csv')
        datasummary = FilterData(file_path).data_summary()
        #send as api response in json format
        return datasummary
#Custom date range
@app.route('/getsummary/date', methods=['POST'])
def get_transactions_by_date():
    if request.method == 'POST':
        #file_path = os.path.join(os.getcwd(), 'data', 'data3.csv')
        save_path = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(save_path, 'data.csv')
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        data = FilterData(file_path).filter_data_asJson(start_date, end_date)
        #send as api response in json format
        return data
if __name__ == '__main__':
    app.run(debug=True)
