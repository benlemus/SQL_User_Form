"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
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
    users = User.order_by_name()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_details(user_id):
    currentUser = User.query.get_or_404(user_id)
    posts = Post.get_posts_by_id(user_id)
    return render_template('user_details.html', user=currentUser, posts=posts)

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

    if request.form.get('cancel'):
        return redirect(f'/users/{user_id}')
    elif request.form.get('update'):
        currentUser = User.query.get_or_404(user_id)
        currentUser.first_name = request.form['first_name']
        currentUser.last_name = request.form['last_name']
        currentUser.img_url = request.form['img_url']

        db.session.commit()

        return redirect(f'/users/{user_id}')
    else:
        flash('Could not update')
    return redirect(f'/users/{user_id}/edit')


# POSTS

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    cur_user = User.query.get_or_404(user_id)
    return render_template('add_post.html', cur_user=cur_user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_new_post_form(user_id):
    if request.form.get('cancel'):
        return redirect(f'/users/{user_id}')
    elif request.form.get('add'):
        post_title = request.form['title']
        post_content = request.form['content']
        
        new_post = Post(title=post_title, content=post_content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/posts/{new_post.id}')
    else:
        flash('Could not create post')
    return redirect(f'/users/{user_id}/posts/new')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    cur_post = Post.query.get_or_404(post_id)
    cur_user = User.query.get_or_404(cur_post.user_id)

    return render_template('post_details.html', post=cur_post, user=cur_user)

@app.route('/posts/<int:post_id>', methods=['POST'])
def handle_btns(post_id):
    cur_post = Post.query.get_or_404(post_id)
    cur_user = User.query.get_or_404(cur_post.user_id)

    if request.form.get('cancel'):
        return redirect(f'/users/{cur_user.id}')
    
    elif request.form.get('edit'):
        return redirect(f'/posts/{post_id}/edit')

    elif request.form.get('delete'):
        Post.query.filter(Post.id == f'{post_id}').delete()
        db.session.commit()
        return redirect(f'/users/{cur_user.id}')
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    cur_post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', p=cur_post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    p = Post.query.get_or_404(post_id)

    if request.form.get('cancel'):
        return redirect(f'/posts/{post_id}')
    elif request.form.get('update'):
        p.title = request.form['title']
        p.content = request.form['content']

        db.session.commit()

        return redirect(f'/posts/{post_id}')
    else:
        flash('Could not update')
    return redirect(f'/posts/{post_id}/edit')

