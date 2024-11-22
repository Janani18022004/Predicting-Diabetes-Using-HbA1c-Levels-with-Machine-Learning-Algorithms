from flask import Flask, render_template, flash, request, session, send_file
import pickle
import numpy as np
import mysql.connector
import sys

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')




@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/AURemove")
def AURemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
    cursor = conn.cursor()
    cursor.execute(
        "delete from regtb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('User  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3diabetesbd')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/Diabetes")
def Diabetes():
    return render_template('Diabetes.html')


@app.route("/diabetes", methods=['GET', 'POST'])
def diabetes():
    if request.method == 'POST':

        Answer = ''
        Prescription = ''

        uname = session['uname']
        age1 = request.form['age']
        hypertension = request.form['hypertension']
        heart_disease = request.form['heart_disease']
        bmi = request.form['bmi']
        HbA1c_level = request.form['HbA1c_level']
        blood_glucose_level = request.form['blood_glucose_level']

        filename2 = 'model.pkl'
        classifier2 = pickle.load(open(filename2, 'rb'))

        data = np.array([[int(age1), int(hypertension), int(heart_disease), float(bmi), float(HbA1c_level),
                          float(blood_glucose_level)]])
        print(data)
        my_prediction = classifier2.predict(data)
        print(my_prediction[0])

        if my_prediction == 1:

            session['Ans'] = 'Yes'

            Answer = session['uname'] + ' :According to our Calculations, You have  Diabetes'

            print('Hello:According to our Calculations, You have Diabetes')

            Prescription = "Sulfonylureas: These drugs stimulate the pancreas to release more insulin. Some examples include glipizide (Glucotrol and Glucotrol XL), glyburide (Micronase, Glynase, and Diabeta), and glimepiride (Amaryl). "

        else:
            Answer = session['uname'] + " Congratulations!!  You DON'T have Diabetes "

            print('Congratulations!! You DON T have Diabetes ')
            Prescription = "Nil"

            session['Ans'] = 'No'

        return render_template('Answer.html', data=Answer, pre=Prescription)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
