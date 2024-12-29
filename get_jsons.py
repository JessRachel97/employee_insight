from flask import Flask , jsonify, request
import base64
import os
import json 

app = Flask(__name__)

# return names and ids for all employees
@app.route('/all_employees')
def all_employees():
    with open('data/employees.json', 'r') as f:
        dat = json.load(f)
    return jsonify(dat)

# return mental health graphs for all employees
@app.route('/mental_graphs')
def get_mental_graphs():
    images = {}
    for filename in os.listdir('graphs'):
        f = os.path.join('graphs/', filename)
        if os.path.isfile(f):
            if 'wc' not in f:
                id = filename.split('.')[0]
                with open(f, "rb") as im_file:
                    encoded = base64.b64encode(im_file.read())
                    images[id] = encoded.decode()
    return jsonify(images)

# return sentiment clouds for all employees
@app.route('/sentiment_clouds')
def get_sentiment_clouds():
    images = {}
    for filename in os.listdir('graphs'):
        f = os.path.join('graphs/', filename)
        if os.path.isfile(f):
            if 'wc' in f:
                id = filename.split('.')[0]
                with open(f, "rb") as im_file:
                    encoded = base64.b64encode(im_file.read())
                    images[id] = encoded.decode()
    return jsonify(images)  

# return all data for a specific employee
@app.route('/get_employee_data')
def get_employee_data():
    name = request.args.get('name')
    out = {}
    with open('data/employees.json', 'r') as f:
        emp_dat = json.load(f)
    id = ''
    for x in emp_dat:
        if x["name"] == name:
            id = x["id"]
            break 
    print(id)
    with open('graphs/' + id + '.png', 'rb') as f:
        encoded = base64.b64encode(f.read())
        out["ment_image"] = encoded.decode()
    with open('graphs/' + id + 'wc.png', 'rb') as f:
        encoded = base64.b64encode(f.read())
        out["belief_image"] = encoded.decode()
    with open('summaries/' + id + '_summary.txt', 'r') as f:
        out["text_sum"] = f.readline()
        out["raw_sum"] = f.readlines()
    return jsonify(out)

if __name__ == "__main__":
    app.run()
