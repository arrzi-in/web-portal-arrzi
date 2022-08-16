
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from connection import mydb
from flask_bcrypt import check_password_hash

mycursor = mydb.cursor()

auth = Blueprint('auth', __name__) # not necessary to name variable same as file name and not necessay to name



@auth.context_processor
def inject_user():
    return dict(session_context=session)

@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password") # Shubham8@arrzi
        sql =  f"select * from `users` where `email` = '{email}'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if len(result)==0:
            flash('Not a Registered Email! Please contact Admin!', category='error')
            return redirect(url_for('auth.login'))
        print(result[0][5], password)
        if check_password_hash(result[0][5], password)==True:
            session["email"] = result[0][1]
            session["name"] = result[0][2]
            session["phone_number"] = result[0][3]
            session["user_level"] = 1
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


@auth.route('/register', methods = ['GET','POST'])
def register():
    return "Register"