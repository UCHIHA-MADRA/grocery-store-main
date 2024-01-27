from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import model.users_db as users
import model.categories_db as cat
import model.products_db as prod
import model.orders_db as orders

app = Flask(__name__)

# secret key: used to encrypt sessions
# secret keys should not be set like this in production
# instead, it should use a key derivation function
# since this is development, it is okay :)
app.secret_key = 'mykey'

def get_dbconnection():
    conn = sqlite3.connect('database.db') # check database.db # database containing all tables
    return conn

@app.route('/') 
def index(): # default page w/o login
    return render_template('index.html')

@app.route('/home')
def home(): # default page after login
    conn = get_dbconnection()
    # check if session is set and if uid is (0 or None) or not

    if session.get('uid') and session['uid']: # session['uid'] = True if not (0 or None) 
        results = users.get_data(conn, session['uid'])
        return render_template('home.html', name = results[0])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # here, request.form behaves like a dictionary
        username = request.form['username']
        password = request.form['password']
        conn = get_dbconnection()

        results = users.exists(conn, (username, password))

        if results:
            # correct login
            print("exists:", results)
            session['uid'] = results[0]
            return redirect(url_for('home'))
        else:
            # invalid login
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # here, request.form behaves like a dictionary
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        conn = get_dbconnection()

        # 0 is default for user/shopper account
        results = users.register(conn, (name, username, password, 2))

        # results must return last_insert_rowid() so that we have the correct user id of the person.
        # else, redirect to login page.
        
        if results:
            # correct login
            # for debugging purposes
            print("exists:", results)
            session['uid'] = results
            return redirect(url_for('home'))
        else:
            # invalid login
            return render_template('register.html')
    else:
        return render_template('register.html')

# users -> login, register (read, insert)
# admin -> create, read, destroy (managers)

# ---
# inventory -> category, products
# category -> crud

# show categories on category page for managers
@app.route('/category', methods = ['GET', 'POST'])
def category():
    conn = get_dbconnection()
    results = cat.get_data(conn)
    print(results)
    return render_template('showcategory.html', categories = results)

# create categories on category page for managers
@app.route('/category/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['category']
        conn = get_dbconnection()
        cat.create(conn, (name,))
        return render_template('success.html')
    else:
        return render_template('createcategory.html')

# create categories on category page for managers
@app.route('/category/delete', methods = ['GET', 'POST'])
def delete():
    conn = get_dbconnection()
    if request.method == 'POST':
        catid = request.form['catid']
        cat.destroy(conn, (catid,))
        return render_template('success.html')
    else:
        results = cat.get_data(conn)
        return render_template('deletecategory.html', categories = results)

@app.route('/inventory/createproduct', methods = ['POST', 'GET'])
def createproduct():
    
    if request.method == 'POST':
        conn = get_dbconnection()
        name = request.form['productname']
        quantity = request.form['quantity']
        catid = request.form['catid']
        result = prod.create(conn, (name, 1, catid,))
        if result:
            render_template('message.html', message = "Operation was successful")
        else:
            render_template('message.html', message = "Operation was not successful")
    else:
        conn = get_dbconnection()
        results = cat.get_data(conn)
        return render_template('createproduct.html', categories = results)

# show categories on category page for managers
@app.route('/inventory/showproduct', methods = ['GET', 'POST'])
def showproduct():
    conn = get_dbconnection()
    results = prod.get_data(conn)
    print(results)
    return render_template('showproduct.html', results = results)

# show categories on category page for managers
@app.route('/inventory/deleteproduct', methods = ['GET', 'POST'])
def deleteproduct():
    conn = get_dbconnection()
    if request.method == 'POST':
        prodid = request.form['prodid']
        result = prod.destroy(conn, (prodid,))
        if result:
            render_template('message.html', message = "Operation was successful")
        else:
            render_template('message.html', message = "Operation was not successful")
    else:
        results = prod.get_data(conn)
        print(results)
        return render_template('deleteproduct.html', products = results)
    

# HOW TO DISPLAY ALL PRODUCTS FOR USER
# 

# order page (place in cart) : status is 0
    # select all products

    # if request.method = 'post':
        # sql: insert into orders ()
        # orders.create

#
# sql = "SELECT * FROM Products WHERE Name = searchquery"
# sql = "SELECT * FROM Products WHERE Name LIKE"
#

@app.route('/orderproducts', methods = ['GET', 'POST'])
def orderproducts():
    conn = get_dbconnection()
    if request.method == 'POST':
        prodid = request.form['prodid']
        quantity = request.form['quantity']
        session.get('uid') # may be faulty
        result = orders.create(conn, (session['uid'], prodid, quantity, "2023-07-25", 0)) # since status is 0, it is added in cart by default
        if result:
            return render_template('message.html', message = "Operation was successful")
        else:
            return render_template('message.html', message = "Operation was not successful")
    else:
        results = prod.get_data(conn)
        return render_template('orderproducts.html', products = results)


# place order (show items in cart) : sql: update orders set status = 1 where userid = ?
    # select all orders where status = 0 and userid = ?
        # render_template('placeorder.html')

@app.route('/viewcart', methods = ['GET', 'POST'])
def viewcart():
    conn = get_dbconnection()
    if request.method == 'POST': # update status of orders for this user
        # when user clicks on place order button -> update orders in cart to have status = 1 so that they are out of cart and are placed
        if session.get('uid') and session['uid']: # check if user is logged in
            result = orders.update(conn, (session['uid'],)) # get if operation is success or fail
            if result: # display message based on if operation is success or fail
                return render_template('message.html', message = "Operation was successful")
            else:
                return render_template('message.html', message = "Operation was not successful")
        else:
            # redirect to login page since user is not logged in
            return redirect(url_for('login'))
    else:
        # when user has not clicked place order button and is simply viewing cart
        if session.get('uid') and session['uid']: # check if user is logged in
            results =  orders.get_data_user(conn, (session['uid'],))
            return render_template('viewcart.html', orders = results)
        else:
            # redirect to login page
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('uid', default = None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # run the app
    app.run(debug = True)