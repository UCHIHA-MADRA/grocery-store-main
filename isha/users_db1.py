from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import model.users_db as users
import model.categories_db as categories
import model.products_db as products
import model.orders_db as orders


# login and redirect to orderproducts.html (CREATE)

@app.route('/login', methods=['GET','POST'])
def user_login():    
    if request.method == "GET":
        return render_template("login.html") # login

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_exists = db.session.query(users).filter_by(username=username).first() is not None # do we ask account_type ? 
        if user_exists: # check if user exists
            return render_template("orderproducts.html") # redirect existing user to orderproducts.html
        else: # register non-existing user
            return redirect(url_for('register.html')) # with a message : please register ?


# register if user doesn't exist and redirect to orderproducts.html (CREATE)

@app.route('/register', methods=['GET','POST'])
def user_register():    
    if request.method == "GET":
        return render_template("register.html") # register

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        user_exists = db.session.query(users).filter_by(username=username).first() is not None # do we ask account_type ? 
        if user_exists: # check if user exists
            return render_template("user_exists.html") # create user_exits.html
        else: # register non-existing user
            user = User(name=name, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('orderproducts.html'))


# get_user_data for managers (READ)

@app.route('/request_user_data', methods=['GET','POST'])
def get_user_data():
    if request.method == 'GET':
        return render_template('request_user_data.html') # create request_user_data.html ## how to specify users table
    ## do we need an else statement here
    if request.method == 'POST':
        userid = request.form['userid']
        user_exists = db.session.query(users).filter_by(user_id=userid).first() is not None
        user_data = db.session.query(users).filter_by(user_id=userid)
        if user_exists: # check if user exists
            return render_template("user_data.html", data = user_data) # create user_exits.html
        else: # register non-existing user
            return redirect(url_for('incorrect_user_id.html')) # how do we just say 'incorrect user id'?

## UPDATE : no update for user ?

## DELETE : do we need a delete
