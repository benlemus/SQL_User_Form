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
    prev = 'home'
    return render_template('home_page.html', posts=posts, prev=prev)


# USERS

''' SHOWS ALL USERS ORDERED BY NAME '''
@app.route('/users')
def list_users():
    users = User.order_by_name()
    return render_template('users.html', users=users)

''' SHOWS USER DETAILS '''
@app.route('/users/<int:user_id>')
def user_details(user_id):
    currentUser = User.query.get_or_404(user_id)
    posts = Post.get_posts_by_id(user_id)
    return render_template('user_details.html', user=currentUser, posts=posts)

''' SHOWS/HANDLES CREATE NEW USER FORM '''
@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        img_url = request.form['img_url']

        new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{new_user.id}')

    return render_template('add_user.html')

''' SHOWS/HANDLES USER EDIT FORM '''
@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
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
                   
    currentUser = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=currentUser)

''' DELETES USER. REDIRECTS TO ALL USERS '''
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter(User.id == f'{user_id}').delete()
    db.session.commit()
    return redirect('/users')


# POSTS

''' SHOWS/HANDLES NEW POST FORM '''
@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect(f'/users/{user_id}')
        elif request.form.get('add'):
            post_title = request.form['title']
            post_content = request.form['content']

            tags = request.form.getlist('checkbox')
            
            new_post = Post(title=post_title, content=post_content, user_id=user_id)

            db.session.add(new_post)
            db.session.commit()

            for tag in tags:
                t = Tag.query.filter(Tag.name == tag).first()
                add_tag = PostTag(post_id=new_post.id, tag_id=t.id)
                db.session.add(add_tag)
                db.session.commit()

            return redirect(f'/posts/{new_post.id}')
        else:
            flash('Could not create post')
        return redirect(f'/users/{user_id}/posts/new')        
    cur_user = User.query.get_or_404(user_id)
    tags = Tag.get_all_tags() 
    return render_template('add_post.html', cur_user=cur_user, tags=tags)

''' SHOWS/HANDLES POSTS DETAILS '''
@app.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    cur_post = Post.query.get_or_404(post_id)
    cur_user = User.query.get_or_404(cur_post.user_id)

    prev = request.args.get('prev')

    if request.method == 'POST':
        if request.form.get('cancel'):
            if request.args.get('prev') == 'user':     
                return redirect(f'/users/{cur_user.id}')
            
            if request.args.get('prev') == 'home': 
                return redirect('/')
            
            if request.args.get('prev') == 'edit':
                return redirect(f'/posts/{cur_post.id}/edit')
            
            # ADD TAG CANCEL REDIRECT
            
            cur_tag = Tag.query.filter(Tag.name == prev).first()
            return redirect(f'/tags/{cur_tag.id}')
        
        elif request.form.get('edit'):
            if request.args.get('prev') == 'home':
                return redirect(f'/posts/{post_id}/edit?prev=home')
            elif request.args.get('prev') == 'user':
                return redirect(f'/posts/{post_id}/edit?prev=user')
            return redirect(f'/posts/{post_id}/edit')

        elif request.form.get('delete'):
            Post.query.filter(Post.id == f'{post_id}').delete()
            db.session.commit()
            return redirect(f'/users/{cur_user.id}')

        return redirect(f'/posts/{post_id}')
    
    if request.method == 'GET':    
        return render_template('post_details.html', post=cur_post, user=cur_user, prev=prev)

''' SHOWS/HANDLES EDIT POST FORM '''
@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def handle_user_edit_post(post_id):
    cur_post = Post.query.get_or_404(post_id)
    prev = request.args.get('prev')

    if request.method == 'POST':
        if request.form.get('cancel'):
            if request.args.get('prev') == 'home':
                return redirect(f'/posts/{post_id}?prev=home')
            elif prev == 'user': 
                return redirect(f'/posts/{post_id}?prev=user')
            return redirect(f'/posts/{post_id}?prev=edit')
        elif request.form.get('update'):
            cur_post.title = request.form['title']
            cur_post.content = request.form['content']

            db.session.commit()

            return redirect(f'/posts/{post_id}?prev=edit')
        else:
            flash('Could not update')
        return redirect(f'/posts/{post_id}/edit')
    if request.method == 'GET':
        return render_template('edit_post.html', p=cur_post, prev=prev)    

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


''' SHOWS SPECIFIC TAG DETAILS '''
@app.route('/tags/<int:tag_id>', methods=['GET', 'POST'])

# ADD TAG DETAILS MULTIPLE CANCEL REDIRECTS
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

''' EDIT TAG, HANDLE CANCEL/UPDATE BTNS '''
@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    t = Tag.query.get_or_404(tag_id)
    if request.method == 'POST':
        if request.form.get('cancel'):
            return redirect(f'/tags/{tag_id}')
        elif request.form.get('update'):
            t.name = request.form['name']
            db.session.commit()
            return redirect(f'/tags/{tag_id}')

    elif request.method == 'GET':
        tag = Tag.query.get_or_404(tag_id)
        return render_template('edit_tag.html', tag=tag)

