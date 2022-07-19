import json
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for
from connection import mydb
import requests

mycursor = mydb.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/view_assignment', methods = ['POST','GET'])
def view_assignments():
    # return redirect(url_for('success',name = user))
    if request.method == "POST":
        assignment_id = request.form['assignment_id']
        contractor_id = request.form["contractor_id"]
        create_date = request.form["create_date"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date" ]
        worker_needed = request.form[ "worker_needed"]
        wage = request.form["wage"]
        skill_needed = request.form[ "skill_needed"]
        city = request.form["city" ]
        worker_assigned = request.form["worker_assigned"]
        status = request.form[ "status"]  


        create = {
                    "assignment_id" : assignment_id,
                    "contractor_id": contractor_id ,
                    "create_date": create_date ,
                    "start_date": start_date,
                    "end_date" : end_date,
                    "worker_needed": worker_needed,
                    "wage": wage,
                    "skill_needed": skill_needed,
                    "city" : city,
                    "worker_assigned": worker_assigned,
                    "status": status          
                }
        data=json.dumps(create)
        
        return redirect(url_for('workers_list', data = data))
    else:
        ans = []
        sql =  "select * from assignments where worker_assigned < worker_needed"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        for i in result:
            fin_ans = {
                        "assignment_id" : i[0],
                        "contractor_id": i[1],
                        "create_date": i[2],
                        "start_date": i[3],
                        "end_date" : i[4],
                        "worker_needed": i[5],
                        "wage": i[6],
                        "skill_needed": i[7],
                        "city" : i[8],
                        "worker_assigned": i[9],
                        "status": i[10]          
                    }
            ans.append(fin_ans)
        return render_template("view_assignment.html", ans=ans)


@app.route('/workers_list/<data>', methods=[ "GET"])
def workers_list(data):
    data = json.loads(data)
    data1 = []
    data1.append(data)
    
    sql =  "select * from workers where city = '"+ data1[0]['city'] +"'" # AND skill_needed = '"+ data1[0]['skill_needed'] +"'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    fin_ans = []        
    for i in result:    
        ans = {
            "worker_id" : i[0],
            "phone_number": i[1],
            "aadhar_number": i[2],
            "dob": i[3],
            "city" : i[4],
            "full_name": i[5],
            "start_date": i[6],
            "notification_token": i[7],
            "skill" : i[8],
                    
        }
        fin_ans.append(ans)

    return render_template("worker_list.html", data=data1, data2 = fin_ans)


app.run(debug = True)


# 5 13