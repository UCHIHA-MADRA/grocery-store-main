# create an update and delete button on get_products.html (UPDATE, DELETE)
# see all products using the get_products function (READ)
# use createproduct.html to add a product and then redirect to get_products (CREATE)

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import model.users_db as users
import model.categories_db as categories
import model.products_db as products
import model.orders_db as orders

# CREATE : add new product

@app.route('/createproduct.html', methods=['GET','POST'])
def add_product():    
    if request.method == "GET":
        return render_template("createproduct.html")

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        category_name = request.form['category_name']
        product_exists = db.session.query(products).filter_by(name=name).first() is not None
        if product_exists: # check if product exists
            return render_template("product_exists.html") ## either create this page or show up a message
        else: # add non-existing product
            category = db.session.query(categories).filter_by(name=category_name).first() 
            catid = category.category_id # check if this produces the right result
            product = Product(name=name, quantity=quantity, category_id=catid)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('get_products'))


# READ : get_product_data for managers

@app.route("/get_products")
def get_products():
    if request.method == "GET":
        products = Product.query.all()
        return render_template("get_products.html", products=products)

# UPDATE : update product for managers using product_id

@app.route("/get_products/<int:product_id>/update",methods=["GET","POST"])
def update_product(product_id)
    if request.method == "GET":
        product = db.session.query(products).filter_by(product_id=product_id).first()
        return render_template('update_product.html') ## create update_product.html   
    if request.method == "POST":
        product = db.session.query(products).filter_by(product_id=product_id).first()
        name = request.form['name']
        quantity = request.form['quantity']
        category_name = request.form['category_name']
        product.name = name
        product.quantity = quantity
        category = db.session.query(categories).filter_by(name=category_name).first() 
        catid=category.category_id 
        product.category_id = catid
        db.session.commit()
        return redirect(url_for('get_products'))

# DELETE : delete product for managers by product_id 

@app.route("/get_products/<int:product_id>/delete") # create a delete button on get_products.html
def delete_product(product_id):
    product = db.session.query(products).filter_by(product_id=product_id).delete()
    db.session.commit()
    return redirect(url_for('get_products'))
