from app import app, db
from flask import render_template, redirect, request,flash,url_for,jsonify
from .models import Item 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        stock = request.form.get('stock')
        description = request.form.get('description')

        item = Item(name=name, stock=stock, description=description)

        try:
            db.session.add(item)
            db.session.commit()
            flash('Item added successfully')
        except Exception as e:
            flash('Error occurred while adding the item')
            db.session.rollback()
        
        return redirect(url_for('index'))

    items = Item.query.all()
    return render_template('index.html', items=items)


@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def editItem(id):
    item = Item.query.filter_by(id=id).first()

    if request.method == "POST":
        name = request.form.get('name')
        stock = request.form.get('stock')
        description = request.form.get('description')

        item.name = name
        item.stock = stock
        item.description = description

        try:
            db.session.commit()
            flash("Item updated successfully")
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error occurred while updating the item')
            return redirect(url_for('index'))

    return render_template("edit.html", item=item)


@app.route('/delete/<string:id>', methods=['GET'])
def deleteItem(id):
    item = Item.query.filter_by(id=id).first()

    try:
        db.session.delete(item)
        db.session.commit()

        flash("Item deleted successfully")
        return redirect(url_for('index'))
    except Exception as e:
        flash('Error occurred while deleting the item')
        return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query') 
    results = Item.query.filter(Item.name.ilike(f'%{query}%')).all()
    return render_template("search_results.html", items=results)
