from flask import Flask, render_template
import requests 
import json

app = Flask(__name__)

# where to find things
our_base = "http://127.0.0.1:8001/"
other_base = "http://127.0.0.1:5000/"

# home page of site, redirects to other pages
@app.route('/')
def home():
    dat = json.loads(requests.get(other_base+"all_employees").content)
    for d in dat:
        d["url"] = our_base + d["name"].replace(' ', '_')
    print(dat)
    return render_template("landing.html", title="Employee Feedback Analysis Portal", graph1url=our_base+"health_graphs", graph2url=our_base+"sentiment_graphs", employees=dat)


# shows the data for a specific employee
@app.route('/<option>')
def show_employee(option):
    name = option.replace('_', ' ')
    print(requests.get(other_base+"get_employee_data",params={'name':name}).content)
    response = json.loads(requests.get(other_base+"get_employee_data",params={'name':name}).content)
    return render_template("employee.html", title=name + " Summary", overall_summary=response["text_sum"], health_image="data:image/png;base64, "+response["ment_image"], belief_image="data:image/png;base64, "+response["belief_image"], belief_alt="", raw_results=response["raw_sum"])

# shows all employees health graphs
@app.route('/health_graphs')
def health_graphs():
    dat = requests.get(other_base+"mental_graphs").content
    image_dict = json.loads(dat)

    new_dict = []
    for k, v in image_dict.items():
        new_dict.append({"image": "data:image/png;base64, "+ v, "image_alt": k})

    return render_template("health_graphs.html",title="All employee mental health graphs", employees=new_dict)


# shows all employees sentiment clouds
@app.route('/sentiment_graphs')
def sentiment_graphs():
    dat = requests.get(other_base+"sentiment_clouds").content
    image_dict = json.loads(dat)

    new_dict = []
    for k, v in image_dict.items():
        new_dict.append({"image": "data:image/png;base64, "+ v, "image_alt": k})

    return render_template("health_graphs.html",title="All employee belief word clouds", employees=new_dict)

# run the app
if __name__ == "__main__":
    print('hi')
    app.run(port=8001)
