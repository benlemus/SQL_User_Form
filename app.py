"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'Milosaysruff01'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

''' ERROR HANDLER '''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

''' FORMATS DATE AND TIME '''
@app.template_filter('format_datetime')
def format_datetime(value):
    return value.strftime('%a %B %d %Y, %I:%M %p')

''' SHOWS HOME PAGE WITH RECENT STORIES '''
@app.route('/')
def home_page():
    posts = Post.get_recent_posts()
    return render_template('home_page.html', posts=posts)


# USERS

''' SHOWS ALL USERS ORDERED BY NAME '''
@app.route('/users')
def list_users():
    users = User.order_by_name()
    return render_template('users.html', users=users)

''' SHOWS SPECIFIC USERS DETAILS '''
@app.route('/users/<int:user_id>')
def user_details(user_id):
    currentUser = User.query.get_or_404(user_id)
    posts = Post.get_posts_by_id(user_id)
    return render_template('user_details.html', user=currentUser, posts=posts)

''' SHOWS CREATE NEW USER FORM '''
@app.route('/users/new')
def add_user():
    return render_template('add_user.html')

''' HANDLES NEW USER FORM. REDIRECTS TO USERS DETAILS'''
@app.route('/users', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

  
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

''' DELETES USER. REDIRECTS TO ALL USERS '''
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter(User.id == f'{user_id}').delete()
    db.session.commit()
    return redirect('/users')

''' SHOWS USER EDIT FORM '''
@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    currentUser = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=currentUser)


''' HANDLES USER EDIT FORM. REDIRECTS TO USER DETAILS '''
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

''' SHOWS NEW POST FORM '''
@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    cur_user = User.query.get_or_404(user_id)
    return render_template('add_post.html', cur_user=cur_user)

''' HANDLES NEW POST FORM '''
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

''' SHOWS POSTS DETAILS '''
@app.route('/posts/<int:post_id>')
def post_details(post_id):
    cur_post = Post.query.get_or_404(post_id)
    cur_user = User.query.get_or_404(cur_post.user_id)

    return render_template('post_details.html', post=cur_post, user=cur_user)

''' HANDLES CANCEL EDIT DELETE BUTTONS '''
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

''' REDIRECTS TO CORRECT PREVIOUS PAGE, HOME PAGE OR USER DETAILS'''
@app.route('/posts/<int:post_id>/2', methods=['GET', 'POST'])
def handle_previous_page(post_id):
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect(f'/')
        
        elif request.form.get('edit'):
            return redirect(f'/posts/{post_id}/edit')

        elif request.form.get('delete'):
            Post.query.filter(Post.id == f'{post_id}').delete()
            db.session.commit()
            return redirect(f'/')
    if request.method == 'GET':
        cur_post = Post.query.get_or_404(post_id)
        cur_user = User.query.get_or_404(cur_post.user_id)

        return render_template('post_details_home.html', post=cur_post, user=cur_user)

''' SHOWS EDIT POST FORM '''
@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    cur_post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', p=cur_post)

''' HANDLES EDIT FORM & REDIRECTS TO POST DETAILS '''
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

# TAGS
''' SHOWS ALL TAGS '''
@app.route('/tags')
def show_tags():
    tags = Tag.get_all_tags()
    return render_template('tags.html', tags=tags)

''' SHOWS NEW TAG FORM AND HANDLES NEW TAG FORM '''
@app.route('/tags/new', methods=['GET','POST'])
def handle_new_tag_form():
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect('/tags')
        elif request.form.get('add'):
            tag_name = request.form['name']
            new_tag = Tag(name=tag_name)

            db.session.add(new_tag)
            db.session.commit()

            return redirect(f'/tags/{new_tag.id}')
    elif request.method == 'GET':
        return render_template('add_tag.html')

    return redirect('/tags/new')

''' SHOWS SPECIFIC TAG DETAILS '''
@app.route('/tags/<int:tag_id>', methods=['GET', 'POST'])
def tag_details(tag_id):
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect(f'/tags')
        
        elif request.form.get('edit'):
            return redirect(f'/tags/{tag_id}/edit')
        
        elif request.form.get('delete'):
            Tag.query.filter(Tag.id == tag_id).delete()
            db.session.commit()
            return redirect('/tags')
        
    elif request.method == 'GET':
        tag = Tag.query.get(tag_id)
        return render_template('tag_details.html', tag=tag)
    
    return render_template('/tags/<int:tag_id>')

''' EDIT TAG, HANDLE CANCEL/UPDATE BTNS '''
@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    t = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect('/tags')
        elif request.form.get('update'):
            t.name = request.form['name']
            db.session.commit()
            return redirect(f'/tags/{tag_id}')

    elif request.method == 'GET':
        tag = Tag.query.get_or_404(tag_id)
        return render_template('edit_tag.html', tag=tag)
    else:
        return redirect(f'/tags/{tag_id}/edit')
