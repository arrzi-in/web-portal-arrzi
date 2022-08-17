from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_bcrypt import check_password_hash, generate_password_hash
import requests


auth = Blueprint('auth', __name__) # not necessary to name variable same as file name and not necessay to name



@auth.context_processor
def inject_user():
    return dict(session_context=session)

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password") # Shubham8@arrzi

        # make API call to get workers list
        api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"

        query = {'query': f"select * from `portal_users` where `email` = '{email}'"}
        headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
        response = requests.post(api_url, json=query, headers=headers)
        response = response.json()
        # print("111111111111111111111111111",response)
        
        if len(response['body']['records'])==0:
            flash('Not a Registered Email! Please contact Admin!', category='error')
            return redirect(url_for('auth.login'))
        # print(response['body']['records'][5]['stringValue'], password)
        if check_password_hash(response['body']['records'][0][5]['stringValue'], password)==True:
            session["email"] = response['body']['records'][0][1]['stringValue']
            session["name"] = response['body']['records'][0][2]['stringValue']
            session["phone_number"] = response['body']['records'][0][3]['stringValue']
            session["user_level"] = response['body']['records'][0][4]['longValue']
            flash('Login Successful!', category='success')
            return redirect(url_for('views.index', session = session))
        else:
            flash('Wrong Password! try again!', category='error')
            return redirect(url_for('auth.login'))

    else:
        return render_template("login.html")


@auth.route("/logout/<status>", methods=['GET'])
def logout(status):
    session.clear()
    if status == 'error':
        flash('Not logged in! Login first!', category='error')
    elif status == 'success':
        flash('Successfully ogged out', category='success')
    return redirect(url_for("auth.login"))


@auth.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        phone_number = request.form.get("phone_number")
        user_level = int(1)
        pw_hash = generate_password_hash(password).decode('utf8')
        # print("111111111111111111111111111111111111111111111111111111111111111111111", pw_hash,)
        # make API call to get workers list
        api_url = "https://8m2febviee.execute-api.ap-south-1.amazonaws.com/Dev/flask"

        query = {'query': f'INSERT INTO `portal_users`(`email`, `full_name`, `phone_number`, `user_level`, `password`) VALUES ("{email}","{name}",{phone_number},{user_level},"{pw_hash}") '}
        headers = {'Content-type': 'application/json', 'authToken':'282e23176845652581e80b39776ad09b8e59652b69106509053efd2f8c53d821'}
        response = requests.post(api_url, json=query, headers=headers)
        response = response.json()
        print(response)
        flash('Admin account created successfully', category='success')
        return redirect(url_for('auth.login'))
    else:
        return render_template("register.html")