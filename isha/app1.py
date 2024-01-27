from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

'''
import model
import users_db1 as users
import category_db1 as categories
import products_db1 as products
import orders_db1 as orders
'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# secret key: used to encrypt sessions
# secret keys should not be set like this in production
# instead, it should use a key derivation function
# since this is development, it is okay :)
app.secret_key = 'mykey'

#-----------------------------------------------------------CLASSES-------------------------------------------------

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    account_type = db.Column(db.Integer, default=0)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False) 

    category_id = db.relationship("Category", back_populates="category_id")

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)   
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)    
    trans_id = db.Column(db.Integer, nullable=False, unique=True)

    user_id = db.relationship("Users", back_populates="user_id")
    product_id = db.relationship("Products", back_populates="product_id")

db.create_all()

# ----------------------------------------------------- PRODUCT -----------------------------------------------------------------------

# CREATE : add new product

@app.route('/createproduct.html', methods=['GET','POST'])
def add_product():    
    if request.method == "GET":
        return render_template("createproduct.html")

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        category_name = request.form['category_name']
        product_exists = db.session.query(Product).filter_by(name=name).first() is not None
        if product_exists: # check if product exists
            return render_template('message.html', message='Product already exists.') ## either create this page or show up a message -- message.html
        else: # add non-existing product
            category = db.session.query(Category).filter_by(name=category_name).first() 
            catid = category.category_id 
            product = Product(name=name, quantity=quantity, category_id=catid)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('get_products'))

# READ : get_product_data for managers

@app.route("/get_products", methods=['GET'])
def get_products():
    if request.method == "GET":
        products = Product.query.all()
        return render_template("get_products.html", products=products) ## orderproducts.html = get_products.html

## for users: category_wise get_products

@app.route("/get_products/<string:category_name>",methods=["GET","POST"])
def get_products_by_category(category):
    if request.method == "GET":
        return render_template('get_products.html') 
    if request.method == "POST":
        category_name=request.form['category_name']
        category = db.session.query(Category).filter_by(category_name=category_name).first()
        catid = category.category_id
        products = db.session.query(Product).filter_by(category_id=catid)
        return render_template('get_products.html', products=products)

##like function

# UPDATE : update product for managers using product_id

@app.route("/get_products/<int:product_id>/update",methods=["GET","POST"])
def update_product(product_id):
    if request.method == "GET":
        product = db.session.query(Product).filter_by(product_id=product_id).first()
        return render_template('update_product.html') ## create update_product.html   
    if request.method == "POST":
        product = db.session.query(Product).filter_by(product_id=product_id).first()
        name = request.form['name']
        quantity = request.form['quantity']
        category_name = request.form['category_name']
        product.name = name
        product.quantity = quantity
        category = db.session.query(Category).filter_by(name=category_name).first() 
        catid=category.category_id 
        product.category_id = catid
        db.session.commit()
        return redirect(url_for('get_products'))

# DELETE : delete product for managers by product_id 

@app.route("/get_products/<int:product_id>/delete") # create a delete button on get_products.html
def delete_product(product_id):
    product = db.session.query(Product).filter_by(product_id=product_id).delete()
    db.session.commit()
    return redirect(url_for('get_products'))



# ---------------------------------------------------------- CATEGORY ------------------------------------------------------------------

# CREATE : add new category for managers

@app.route('/createcategory.html', methods=['GET','POST'])
def add_category():    
    if request.method == "GET":
        return render_template("createcategory.html")
    if request.method == 'POST':
        name = request.form['name']
        category_exists = db.session.query(Category).filter_by(name=name).first() is not None
        if category_exists: # check if category exists
            return render_template('message.html', message='Category already exists.') ## either create this page or show up a message
        else: # add non-existing category
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('get_categories'))


# READ : get_category_data for managers / users

@app.route("/get_categories")
def get_categories():
    if request.method == "GET":
        categories = Category.query.all()
        return render_template("get_categories.html", categories=categories)

# UPDATE : update category for managers using category_id

@app.route("/get_categories/<int:category_id>/update",methods=["GET","POST"])
def update_category(category_id):
    if request.method == "GET":
        category = db.session.query(Category).filter_by(category_id=category_id).first()
        return render_template('update_category.html') ## create update_category.html   
    if request.method == "POST":
        category = db.session.query(Category).filter_by(category_id=category_id).first()
        name = request.form['name']
        category.name = name
        db.session.commit()
        return redirect(url_for('get_categories'))

# DELETE : delete category for managers by category_id 

@app.route("/get_categories/<int:category_id>/delete") # create a delete button on get_categories.html
def delete_category(category_id):
    category = db.session.query(Product).filter_by(category_id=category_id).delete()
    db.session.commit()
    return redirect(url_for('get_categories'))



# ------------------------------------------------------------ USER --------------------------------------------------------------------

# CREATE : login and redirect to orderproducts.html 

@app.route('/login', methods=['GET','POST'])
def user_login():    
    if request.method == "GET":
        return render_template("login.html") # login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter_by(username=username).first()  # do we ask account_type ?
        if user and user.password == password: # check if user exists and the password matches
            return render_template("orderproducts.html") # redirect existing user to orderproducts.html
        else:
            return render_template('message.html', message='Incorrect Credentials')
        # not letting the user know if the user doesn't exist/ password is wrong so that a user with malicious intent cannot figure 
        # out the password using the username


# CREATE : register if user doesn't exist and redirect to orderproducts.html

@app.route('/register', methods=['GET','POST'])
def user_register():    
    if request.method == "GET":
        return render_template("register.html") # register
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        c_password = request.form['confirm_password']
        user_exists = db.session.query(User).filter_by(username=username).first() is not None # do we ask account_type ? 
        if user_exists: # check if user exists
            return render_template("message.html", message='User already exists. Please log in.') # create user_exits.html
        else: # register non-existing user
            if password == c_password:
                user = User(name=name, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('orderproducts.html'))
            else:
                return render_template("message.html", message='Passwords do not match. Please re-enter.')

# READ : get_user_data for managers 

@app.route('/user_data/<int:account_type>', methods=['GET','POST'])
def get_user_data(account_type):
    if request.method == 'GET':
        return render_template('user_data.html') # create user_data.html ## how to specify users table
    ## do we need an else statement here
    if request.method == 'POST':
        account_type = request.form['account_type']
        user_data = db.session.query(User).filter_by(account_type=account_type)
        return render_template("user_data.html", data = user_data) # create user_exits.html
        
## UPDATE : update the username, password or name of user for users



## DELETE : do we need a delete --- if yes, use db.session.pop()



# ------------------------------------------------------------ ORDER --------------------------------------------------------------------

# --------------------- FOR MANAGERS

# READ : read all placed orders for managers
@app.route("/get_orders")
def get_orders():
    if request.method == "GET":
        orders = Order.query.all()
        return render_template("get_orders.html", orders=orders)

# --------------------- FOR USERS

# CREATE : create new order of a single product using a trans_id for each transaction for managers
@app.route('/createorder.html', methods=['GET','POST'])
def add_order():    
    if request.method == "GET":
        return render_template("showproducts.html") # display products
    if request.method == 'POST':
        product_id = request.form['product_id'] 
        quantity = request.form['quantity'] ## add quantity column in showproducts.html
        product = db.session.query(Product).filter(product_id=product_id).first()
        if quantity > product.quantity : 
            return render_template('message.html', message='Insufficient stock.') 
        else: # add non-existing product
            order = Order(quantity=quantity, status=0, product_id=product_id) # how to incorporate date and user_id, how to ensure we enter the right trans_id ?
            product.quantity = product.quantity - quantity
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('showproducts'))

# READ : read all items placed in cart by the same user for users (something like view cart)
@app.route('/viewcart/<int:product_id>', methods=['GET'])
def viewcart(user_id):
    if request.method == 'GET': 
        orders = db.session.query(Order).filter_by(user_id=user_id, status=0) 
        return render_template("viewcart.html", orders=orders) ## create viewcart.html and add parameters accordingly

# UPDATE : update products/ quantity of a single transaction for users
@app.route("/viewcart/<int:order_id>/update",methods=["GET","POST"])
def update_order(order_id):
    if request.method == "GET":
        order = db.session.query(Order).filter_by(order_id=order_id).first()
        return render_template('update_order.html') ## create update_order.html   
    if request.method == "POST":
        quantity = request.form['quantity']
        order = db.session.query(Order).filter_by(order_id=order_id).first()
        prodid = order.product_id
        product = db.session.query(Product).filter_by(product_id=prodid).first()        
        if quantity > product.quantity : # check if quantity demanded is available
            return render_template("message.html", message='Insufficient stock.') ## or excessive demand ?
        else: # update product.quantity and order.quantity
            product.quantity = product.quantity + order.quantity - quantity
            order.quantity = quantity ## what if someone updates the quantity to 0 ? -- write min=1 on html page
            db.session.commit()
            return redirect(url_for('viewcart'))

# DELETE : delete the order of a single product placed by the user for users
@app.route("/viewcart/<int:order_id>/delete") # create a delete button on get_products.html
def delete_order(order_id):
    order = db.session.query(Order).filter_by(order_id=order_id).delete() ## do we have to update the quantity of the product ? 
    db.session.commit()
    return redirect(url_for('viewcart'))

# PLACE ORDER : by clicking the place order button on the viewcart.html
@app.route('/viewcart/<int:user_id>/place_order')
def place_order(user_id):
    orders = db.session.query(Order).filter_by(user_id=user_id, status=0)
    for order in orders:
        order.status = 1
    db.session.commit()
    return redirect(url_for('vieworders')) ## create vieworders.html


# ------------------------------------------------------------ MAIN --------------------------------------------------------------------

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)