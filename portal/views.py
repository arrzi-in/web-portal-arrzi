
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import json
import requests


views = Blueprint('views', __name__) # not necessary to name variable same as file name and not necessay to name




@views.context_processor
def inject_user():
    return dict(session_context=session)


@views.route('/')
def index():
    if not session.get("email"):
        return redirect(url_for('auth.login'))
    else:
        return render_template("index.html")



@views.route('/view_assignment', methods = ['GET'])
def view_assignments():
    # return redirect(url_for('success',email = user))
    if not session.get("email") or session.get('user_level') != 1:       
        return redirect(url_for('auth.logout', status = 'error'))

    ans = []
    # make API call to get workers list
    api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"

    query = {'query': f"select * from assignments where worker_assigned < worker_needed and status = 'active'"}
    headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
    response = requests.post(api_url, json=query, headers=headers)
    response = response.json()

    for i in response['body']['records']:
        fin_ans = {
                    "assignment_id" : i[0]['longValue'],
                    "contractor_id": i[1]['longValue'],
                    "create_date": i[2]['stringValue'],
                    "start_date": i[3]['stringValue'],
                    "end_date" : i[4]['stringValue'],
                    "worker_needed": i[5]['longValue'],
                    "wage": i[6]['longValue'],
                    "skill_needed": i[7]['longValue'],
                    "city" : i[8]['longValue'],
                    "worker_assigned": i[9]['longValue'],
                    "status": i[10]['stringValue']          
                }
        ans.append(fin_ans)
    return render_template("view_assignment.html", ans=ans)



@views.route('/workers_list', methods=[ "POST"])
def workers_list():
    if not session.get("email") or session.get('user_level') != 1:
        return redirect(url_for('auth.logout', status = 'error'))
    if request.method == 'POST':
        
        # initialize list
        data1 = []
        # get assignment data from form
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

        # convert assignment details to json format to parse
        data = {
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
        data1.append(data)

        # make API call to get workers list
        api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"
        city = data1[0]['city']
        query = {'query': f"select * from workers where city =  '{city}' "} # AND skill_needed = '"+ data1[0]['skill_needed'] +"'"
        headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
        response = requests.post(api_url, json=query, headers=headers)
        response = response.json()
        # print("11111111111111111111111111111111111111111111111111111111111111111111111111", response['body']['records'])
        
        fin_ans = []
        for i in response['body']['records']:    
            if 'isNull' in i[2]:
                aadhar_number="None"
            else:
                aadhar_number="i[2]['stringValue']"
            ans = {
                "worker_id" : i[0]['longValue'],
                "phone_number": i[1]['stringValue'],
                "aadhar_number": aadhar_number,
                "dob": i[3]['stringValue'],
                "city" : i[4]['longValue'],
                "full_name": i[5]['stringValue'],
                "start_date": i[6]['stringValue'],
                "notification_token": i[7]['stringValue'],
                "skill" : i[8]['longValue'],
                        
            }
            fin_ans.append(ans)
        return render_template("worker_list.html", data=data1, data2 = fin_ans)


@views.route('/assign_worker', methods=["POST"])
def assign_worker():
    if not session.get("email") or session.get('user_level') != 1:
        return redirect(url_for('auth.logout', status = 'error'))
    if request.method == 'POST':
        assignment_id = request.form.get("assignment_id")
        assigned_worker = request.form.get("worker_assigned")
        worker_id = request.form.getlist("worker_id_check")

        for i in range(len(worker_id)):
            worker_id[i] = int(worker_id[i])
        if len(worker_id) == 0:
            flash('No workers assigned', category='success')
            return redirect(url_for('views.index'))
        else:
            
            for i in worker_id:
                # make API call to check if the worker already has an entry for this assignment
                api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"
                query = {'query': f"select * from `assignment_status` where assignment_id =  '{assignment_id}' and worker_id = '{i}' "}
                headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
                response = requests.post(api_url, json=query, headers=headers)
                response = response.json()
                # print("11111111111111111111111111111111111111111111111111111111111111111111111111", response['body']['records'])
                if len(response['body']['records']) == 0:
                    # make API call to make new entry in assignment_status table
                    api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"
                    query = {'query': f"INSERT INTO `assignment_status` (`assignment_id`,`worker_id`,`status`) VALUES('{assignment_id}', '{i}', 'accepted')"}
                    headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
                    response = requests.post(api_url, json=query, headers=headers)
                    # response = response.json()
                    
                elif len(response['body']['records']) > 0:
                    # make API call to update entry in assignment_status table
                    api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"
                    query = {'query': f"UPDATE `assignment_status` SET status = 'accepted' where assignment_id =  '{assignment_id}' and worker_id = '{i}' "} 
                    headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
                    response = requests.post(api_url, json=query, headers=headers)

                # increment the value of asssigned workers
                assigned_worker = int(assigned_worker) + 1
                # make API call to inccrement assigned_worker in assignment table
                api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"
                query = {'query': f"UPDATE `assignments` SET worker_assigned = {assigned_worker} WHERE assignment_id = {assignment_id} "}
                headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
                response = requests.post(api_url, json=query, headers=headers)
                print(response.json())
            flash(f'{len(worker_id)} workers assigned', category='success')
            return redirect(url_for('views.index'))
        
    else:
        return redirect(url_for('auth.logout' , status = 'error'))