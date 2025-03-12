"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'Milosaysruff01'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def list_users():
    # users = User.query.all()
    users = User.order_by_name()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_details(user_id):
    currentUser = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=currentUser)

@app.route('/users/new')
def add_user():
    return render_template('add_user.html')

@app.route('/users', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

  
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter(User.id == f'{user_id}').delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    currentUser = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=currentUser)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_confirm(user_id):

    currentUser = User.query.get_or_404(user_id)
    currentUser.first_name = request.form['first_name']
    currentUser.last_name = request.form['last_name']
    currentUser.img_url = request.form['img_url']

    db.session.commit()

    return redirect(f'/users/{user_id}')

