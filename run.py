import os
from flask import Flask, render_template, flash, redirect, \
    request, url_for, send_from_directory, jsonify, \
    make_response

from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, MenuItem, User, Review

import random
import string
import httplib2
import json
import requests
from functools import wraps

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from werkzeug.utils import secure_filename

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('google_client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = " Restaurants Catalog Application"


UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    """
    Show JSON representation of a specific restaurant.
    :param restaurant_id: Restaurant's id.
    :return: JSON representation.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem). \
        filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    """
    Show JSON representation of a specific menu item.
    :param restaurant_id: Restaurant's id to which menu item belongs.
    :param menu_id: Menu item's id.
    :return: JSON representation.
    """
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=menuItem.serialize)


@app.route('/menu/<int:menu_id>/review/<int:review_id>/JSON')
def menuItemReviewJSON(menu_id, review_id):
    """
    Show JSON representation of a specific menu item's review.
    :param menu_id: Menu item's id to which review belongs.
    :param review_id: Review's id.
    :return: JSON representation.
    """
    review = session.query(Review).filter_by(menuItem_id=menu_id, id=review_id).one()
    return jsonify(MenuItem_Review=review.serialize)


def login_required(f):
    """
    A decorator function that wraps and replaces user
    authorization in each view.
    :param f: Function to be replaced with the decorator.
    :return: Redirect to login page if the user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            flash("You have to login first!")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """
    Get a file with a specified filename
    :param filename: file's name.
    :return:
    on GET: File with the specified name.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/login')
def showLogin():
    """
    Show application's login page.
    :return:
    on GET: Render login template.
    """

    # Generate random state token to prevent
    # cross-site request forgery attacks
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect',
           methods=['POST'])
def gconnect():
    """
    Connect to Google+ OAuth 2.0 provider.
    :return:
    on POST: Redirect to home page if the connect request has been succeeded.
    Show error message if the connect request has been failed.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'google_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    login_session['access_token'] = access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    Disconnect from Google+ OAuth 2.0 provider.
    :return:
    on GET: Show error message if the disconnect request has been failed.
    """
    print login_session.keys()
    access_token = login_session.get('access_token')
    print 'In gdisconnect access token is %s', access_token
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'User name is: '
    print login_session['username']

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """
    Disconnect from OAuth 2.0 provider based on provider name.
    :return:
    on GET: Redirect to home page if the disconnect request has been succeeded.
    Show error message if the disconnect request has been failed.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in")
    return redirect(url_for('showHome'))


@app.route('/')
def showHome():
    """
    Show application's home page
    :return:
    on GET: Render index template.
    """
    return render_template('index.html')


@app.route('/restaurants')
def showAllRestaurants():
    """
    Show application's restaurants page.
    :return:
    on GET: Render restaurants template with all restaurants found.
    """
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/menus')
def showAllMenus():
    """
    Show application's menu page.
    :return:
    on GET: Render menu template with all menus found.
    """
    menuItems = session.query(MenuItem).all()
    return render_template('menu.html', restaurant=None, menuItems=menuItems)


@app.route('/menus/<path:category>')
def showAllMenusByCategory(category):
    """
    Show application's menus page.
    :param category: Category's name to which all menus belong.
    :return:
    on GET: Render menu template with all menus of a specific category.
    """
    menuItems = session.query(MenuItem).filter_by(category=category).all()
    return render_template('menu.html', restaurant=None, menuItems=menuItems)


@app.route('/restaurant/new',
           methods=['GET', 'POST'])
@login_required
def newRestaurant():
    """
    Create a new restaurant.
    :return:
    on GET: Render new restaurant form template.
    on POST: Redirect to the restaurants page if the create request has been succeeded.
    """
    if request.method == 'POST':
        uploadedFile = request.files['image']
        restaurant = Restaurant(name=request.form['name'],
                                description=request.form['description'],
                                telephone=request.form['telephone'],
                                image=uploadedFile.filename,
                                user_id=login_session['user_id'])

        if uploadedFile and allowed_file(uploadedFile.filename):
            filename = secure_filename(uploadedFile.filename)
            uploadedFile.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))

        session.add(restaurant)
        session.commit()
        flash('New restaurant %s successfully created!' % restaurant.name)
        return redirect(url_for('showAllRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editRestaurant(restaurant_id):
    """
    Edit restaurant with a specific restaurant's id.
    :param restaurant_id: Restaurant's id.
    :return:
    on GET: Render edit restaurant form template.
    on POST: Redirect to the restaurants page if the edit request has been succeeded.
    """
    editedRestaurant = session.query(Restaurant). \
        filter_by(id=restaurant_id).one()

    if editedRestaurant.user_id != login_session['user_id']:
        flash("You are not authorized to edit this restaurant!")
        return redirect('/restaurants')

    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        if request.form['telephone']:
            editedRestaurant.telephone = request.form['telephone']
        if request.form['description']:
            editedRestaurant.description = request.form['description']
        if request.files['image']:
            uploadedFile = request.files['image']
            if uploadedFile and allowed_file(uploadedFile.filename):
                if editedRestaurant.image != '':
                    os.remove(os.path.join(
                        UPLOAD_FOLDER, editedRestaurant.image))
                editedRestaurant.image = uploadedFile.filename
                filename = secure_filename(uploadedFile.filename)
                uploadedFile.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))
        session.add(editedRestaurant)
        session.commit()
        flash('Restaurant %s successfully edited!' % editedRestaurant.name)
        return redirect(url_for('showAllRestaurants'))
    else:
        return render_template('editRestaurant.html',
                               restaurant=editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteRestaurant(restaurant_id):
    """
    Delete restaurant with a specific restaurant's id.
    :param restaurant_id: Restaurant's id.
    :return:
    on GET: Render delete restaurant form template.
    on POST: Redirect to the restaurants page if the delete request has been succeeded.
    """
    deletedRestaurant = session.query(Restaurant). \
        filter_by(id=restaurant_id).one()

    if deletedRestaurant.user_id != login_session['user_id']:
        flash("You are not authorized to delete this restaurant!")
        return redirect('/restaurants')

    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash('Restaurant %s successfully deleted!' % deletedRestaurant.name)
        return redirect(url_for('showAllRestaurants'))
    else:
        return render_template('deleteRestaurant.html',
                               restaurant=deletedRestaurant)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    """
    Show menus of a specific restaurant.
    :param restaurant_id: Restaurant's id to which all rendered menus belong.
    :return:
    on GET: Render menu template with specific restaurant's all menus.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(
        restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant,
                           menuItems=menuItems)


@app.route('/restaurant/<int:restaurant_id>/menu/<path:category>')
def showMenuByCategory(restaurant_id, category):
    """
    Show menus of a specific category that belongs to a specific restaurant.
    :param restaurant_id: Restaurant's id to which all menus belong.
    :param category: Category's name to which all menus belong.
    :return:
    on GET: Render menu template with all menus of a specific category
    that belongs to a specific restaurant.
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, category=category).all()
    return render_template('menu.html', restaurant=restaurant, menuItems=menuItems)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/review',
           methods=['POST'])
@login_required
def submitReview(restaurant_id, menu_id):
    """
    Submit review to a specific menu item.
    :param restaurant_id: Restaurant's id to which menu item belongs.
    :param menu_id: Menu item's id to which review belongs.
    :return:
    on POST: Render item template with the requested menu item.
    """
    restaurant = session.query(Restaurant). \
        filter_by(id=restaurant_id).one()

    menuItem = session.query(MenuItem). \
        filter_by(id=menu_id).one()

    if restaurant and menuItem:
        review = Review(content=request.form['content'],
                        rate=int(request.form['rate']),
                        user_id=int(login_session['user_id']),
                        menuItem_id=menu_id)
        session.add(review)
        session.commit()
        flash('New review successfully made!')
        return redirect(url_for('showMenuItem',
                                menu_id=menu_id))
    else:
        return redirect(url_for('showAllMenus'))


@app.route('/menu/<int:menu_id>')
def showMenuItem(menu_id):
    """
    Show application's item page.
    :param menu_id: Menu item's id.
    :return:
    on GET: Render item template
    """
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    creator = getUserInfo(menuItem.user_id)
    reviews = session.query(Review).filter_by(menuItem_id=menu_id).all()
    return render_template('item.html', item=menuItem,
                           creator=creator, reviews=reviews)


@app.route('/restaurant/<int:restaurant_id>/menu/new',
           methods=['GET', 'POST'])
@login_required
def newMenuItem(restaurant_id):
    """
    Create a menu item with a specific restaurant's id.
    :param restaurant_id: Restaurant's id to which new menu item belongs.
    :return:
    on GET: Render new menu form template.
    on POST: Redirect to the menu page if the create request has been succeeded.
    """
    restaurant = session.query(Restaurant). \
        filter_by(id=restaurant_id).one()

    if restaurant.user_id != login_session['user_id']:
        flash("You are not authorized to create this menu!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))

    if request.method == 'POST':
        uploadedFile = request.files['image']
        menuItem = MenuItem(name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            category=request.form['category'],
                            image=uploadedFile.filename,
                            restaurant_id=restaurant_id,
                            user_id=restaurant.user_id)

        if uploadedFile and allowed_file(uploadedFile.filename):
            filename = secure_filename(uploadedFile.filename)
            uploadedFile.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))

        session.add(menuItem)
        session.commit()
        flash('New menu %s successfully created!' % menuItem.name)
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('newMenu.html',
                               restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editMenuItem(restaurant_id, menu_id):
    """
    Edit menu item with a specific menu item's id.
    :param restaurant_id: Restaurant's id to which new menu item belongs.
    :param menu_id: Menu item's id.
    :return:
    on GET: Render edit menu form template.
    on POST: Redirect to the menu page if the edit request has been succeeded.
    """
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

    if editedItem.user_id != login_session['user_id']:
        flash("You are not authorized to edit this menu!")
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['category']:
            editedItem.category = request.form['category']
        if request.files['image']:
            uploadedFile = request.files['image']
            if uploadedFile and allowed_file(uploadedFile.filename):
                if editedItem.image != '':
                    os.remove(os.path.join(
                        UPLOAD_FOLDER, editedItem.image))
                editedItem.image = uploadedFile.filename
                filename = secure_filename(uploadedFile.filename)
                uploadedFile.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))

        session.add(editedItem)
        session.commit()
        flash('Menu %s successfully edited!' % editedItem.name)
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('editMenu.html',
                               restaurant_id=restaurant_id,
                               item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteMenuItem(restaurant_id, menu_id):
    """
    Delete menu item with a specific menu item's id.
    :param restaurant_id: Restaurant's id to which new menu item belongs.
    :param menu_id: Menu item's id.
    :return:
    on GET: Render delete menu form template.
    on POST: Redirect to the menu page if the delete request has been succeeded.
    """
    deletedMenuItem = session.query(MenuItem). \
        filter_by(id=menu_id).one()

    if deletedMenuItem.user_id != login_session['user_id']:
        flash("You are not authorized to delete this menu!")
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))

    if request.method == 'POST':
        session.delete(deletedMenuItem)
        session.commit()
        flash('Menu %s successfully deleted!' % deletedMenuItem.name)
        return redirect(url_for('showMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenu.html',
                               restaurant_id=restaurant_id,
                               menuItem=deletedMenuItem)


def createUser(login_session):
    """
    Create a new user object.
    :param login_session: Login session that contains user attributes.
    :return: User's id of the newly created user object.
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    Get user with a specific id.
    :param user_id: User's id.
    :return: User object if the id is exists.
    """
    user = session.query(User).filter_by(
        id=user_id).one()
    return user


def getUserID(email):
    """
    Get id of a user with a specific email address.
    :param email: User's email address.
    :return: User's id if the email address is exists, None otherwise.
    """
    try:
        user = session.query(User).filter_by(
            email=email).one()
        return user.id
    except:
        return None


def allowed_file(filename):
    """
    Test if the file's extension is allowed or not.
    :param filename: File's name.
    :return: True if the file's extension is allowed, false otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] \
           in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.secret_key = 'Secret_Key'
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
