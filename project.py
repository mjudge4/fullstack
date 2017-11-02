#import Flask class from the flask library
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_create import Base, Restaurant, MenuItem

#create an instance of this class with the name of the running application as the argument
app = Flask(__name__)

#Creates the database and adds tables and columns
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])
    
#Homepage & lists all restaurants
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    items = session.query(Restaurant).all()
    return render_template('restaurant.html', items = items)

#Shows the menu for the restaurant selected
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

#Add a new restaurant
@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        return render_template('newrestaurant.html')
                        


#Shows one menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)
    
#Add a new menu item
@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method =='POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

#Edit a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
       if request.form['name']:
           editedItem.name = request.form['name']
       session.add(editedItem)
       session.commit()
       flash("item edited")
       return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, editedItem = editedItem)
                                                                                                  
#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method =='POST':
        session.delete(deletedItem)
        session.commit()
        flash("item edited")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', deletedItem=deletedItem)    

#makes sure the script only runs if the script is executed directly from the python interpreter
if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(port = 8080)

