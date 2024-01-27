from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from Isha.model import *
import users_db1 as users
import category_db1 as categories
import products_db1 as products
import orders_db1 as orders



# CREATE : create new order of a single product using a trans_id for each transaction for managers

# READ : read all placed orders for managers
@app.route("/get_orders")
def get_orders():
    if request.method == "GET":
        orders = Order.query.all()
        return render_template("get_orders.html", orders=orders)

# ----------------------- FOR USERS

# CREATE : create new order of a single product using a trans_id for each transaction for managers
@app.route('/createorder.html', methods=['GET','POST'])
def add_order():    
    if request.method == "GET":
        return render_template("showproducts.html") # display products
    if request.method == 'POST':
        product_id = request.form['product_id'] 
        quantity = request.form['quantity'] ## add quantity column in showproducts.html
        product = db.session.query(products).filter(product_id=product_id).first()
        if quantity > product.quantity : 
            return render_template('message.html', message='Insufficient stock.') 
        else: # add non-existing product
            order = Order(quantity=quantity, status=0, product_id=product_id) # how to incorporate date and user_id, how to ensure we enter the right trans_id ?
            product.quantity = product.quantity - quantity
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('showproducts'))

# READ : read all items placed in cart by the same user for users (something like view cart)
@app.route('/viewcart/<int:product_id>', methods='GET')
def viewcart(user_id):
    if request.method == 'GET': 
        orders = db.session.query(orders).filter_by(user_id=user_id, status=0) 
        return render_template("viewcart.html", orders=orders) ## create viewcart.html and add parameters accordingly

# UPDATE : update products/ quantity of a single transaction for users
@app.route("/viewcart/<int:order_id>/update",methods=["GET","POST"])
def update_order(order_id):
    if request.method == "GET":
        order = db.session.query(orders).filter_by(order_id=order_id).first()
        return render_template('update_order.html') ## create update_order.html   
    if request.method == "POST":
        quantity = request.form['quantity']
        order = db.session.query(orders).filter_by(order_id=order_id).first()
        prodid = order.product_id
        product = db.session.query(products).filter_by(product_id=prodid).first()        
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
    order = db.session.query(orders).filter_by(order_id=order_id).delete() ## do we have to update the quantity of the product ? 
    db.session.commit()
    return redirect(url_for('viewcart'))

# PLACE ORDER : by clicking the place order button on the viewcart.html
@app.route('/viewcart/<int:user_id>/place_order')
def place_order(user_id):
    orders = db.session.query(orders).filter_by(user_id=user_id, status=0)
    for order in orders:
        order.status = 1
    db.session.commit()
    return redirect(url_for('vieworders.html')) ## create vieworders.html

#------------------------------------------- SEARCH FUNCTION FOR CATEGORIES / PRODUCTS : MIHIR

#------------------------------------------- HTMLS, BOOTSTRAP : MIHIR