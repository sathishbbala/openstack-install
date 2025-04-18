from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)
app.secret_key='admin_123'

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("/home/debian/crud_app/students.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from students")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email_address=request.form['email_address']
        phone_number=request.form['phone_number']
        con=sql.connect("/home/debian/crud_app/students.db")
        cur=con.cursor()
        cur.execute("insert into students(first_name,last_name,email_address,phone_number) values (?,?,?,?)",(first_name,last_name,email_address,phone_number))
        con.commit()
        flash('Record Added','success')
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:id>",methods=['POST','GET'])
def edit_user(id):
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email_address=request.form['email_address']
        phone_number=request.form['phone_number']
        con=sql.connect("/home/debian/crud_app/students.db")
        cur=con.cursor()
        cur.execute("update students set FIRST_NAME=?,LAST_NAME=?,EMAIL_ADDRESS=?,PHONE_NUMBER=? where ID=?",(first_name,last_name,email_address,phone_number,id))
        con.commit()
        flash('Record Updated','success')
        return redirect(url_for("index"))
    con=sql.connect("/home/debian/crud_app/students.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from students where ID=?",(id,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)

@app.route("/delete_user/<string:id>",methods=['GET'])
def delete_user(id):
    con=sql.connect("/home/debian/crud_app/students.db")
    cur=con.cursor()
    cur.execute("delete from students where ID=?",(id,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))

if __name__=='__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
