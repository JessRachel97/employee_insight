import requests 
import json
from flask import Flask , jsonify, request, render_template
import base64
import os


app = Flask(__name__)

# where to find things
our_base = request.url + '/'
other_base = our_base + '/'

# home page of site, redirects to other pages
@app.route('/')
def home():
    global our_base
    global other_base
    our_base = request.url + '/'
    other_base = our_base + '/'
    # dat = json.loads(all_employees())
    dat = json.loads(requests.get(other_base+"all_employees").content)
    for d in dat:
        d["id"] = d["id"].strip()
        d["url"] = our_base + d["id"].strip()
    print(dat)
    return render_template("landing.html", title="Employee Feedback Analysis Portal", graph1url=our_base+"health_graphs", graph2url=our_base+"sentiment_graphs", employees=dat)


# shows the data for a specific employee
@app.route('/<option>')
def show_employee(option):
    id = option
    # response = json.loads(get_employee_data(id))
    print(f'url: {other_base} + "get_employee_data')
    response = json.loads(requests.get(other_base+"get_employee_data",params={'id':id}).content)
    return render_template("employee.html", title=response["name"] + " Summary", overall_summary=response["text_sum"], health_image="data:image/png;base64, "+response["ment_image"], belief_image="data:image/png;base64, "+response["belief_image"], belief_alt="", raw_results=response["raw_sum"])

# shows all employees health graphs
@app.route('/health_graphs')
def health_graphs():
    # dat = get_mental_graphs()
    dat = requests.get(other_base+"mental_graphs").content
    image_dict = json.loads(dat)

    new_dict = []
    for k, v in image_dict.items():
        new_dict.append({"image": "data:image/png;base64, "+ v, "image_alt": k})

    return render_template("health_graphs.html",title="All employee mental health graphs", employees=new_dict)


# shows all employees sentiment clouds
@app.route('/sentiment_graphs')
def sentiment_graphs():
    # dat = get_sentiment_clouds()
    dat = requests.get(other_base+"sentiment_clouds").content
    image_dict = json.loads(dat)

    new_dict = []
    for k, v in image_dict.items():
        new_dict.append({"image": "data:image/png;base64, "+ v, "image_alt": k})

    return render_template("health_graphs.html",title="All employee belief word clouds", employees=new_dict)

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
    id = request.args.get('id')
    out = {}
    with open("output/" + id + ".csv") as f:
        name = f.readline()
        out["name"] = name
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


# run the app
if __name__ == "__main__":
    app.run()
