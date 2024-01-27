# create an update and delete button on get_category.html (UPDATE, DELETE)
# see all categories using the get_category function (READ)
# use createcategory.html to add a category and then redirect to get_category (CREATE)

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import model.users_db as users
import model.categories_db as categories
import model.products_db as products
import model.orders_db as orders

# CREATE : add new category for managers

@app.route('/createcategory.html', methods=['GET','POST'])
def add_category():    
    if request.method == "GET":
        return render_template("createcategory.html")

    if request.method == 'POST':
        name = request.form['name']
        category_exists = db.session.query(categories).filter_by(name=name).first() is not None
        if category_exists: # check if category exists
            return render_template("category_exists.html") ## either create this page or show up a message
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
def update_category(category_id)
    if request.method == "GET":
        category = db.session.query(categories).filter_by(category_id=category_id).first()
        return render_template('update_category.html') ## create update_category.html   
    if request.method == "POST":
        category = db.session.query(categories).filter_by(category_id=category_id).first()
        name = request.form['name']
        category.name = name
        db.session.commit()
        return redirect(url_for('get_categories'))

# DELETE : delete category for managers by category_id 

@app.route("/get_categories/<int:category_id>/delete") # create a delete button on get_categories.html
def delete_category(category_id):
    category = db.session.query(products).filter_by(category_id=category_id).delete()
    db.session.commit()
    return redirect(url_for('get_categories'))
