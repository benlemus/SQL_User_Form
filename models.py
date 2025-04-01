from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(15), nullable=False)

    last_name = db.Column(db.String(20), nullable=False, unique=True)

    img_url = db.Column(db.Text, nullable=True)

    @classmethod
    def order_by_name(self):
        return User.query.order_by(User.last_name, User.first_name).all()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    '''model for posts'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(20), nullable=False, unique=True)

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    user = db.relationship('User', backref='posts', cascade="all, delete", lazy='joined')

    tags = db.relationship('Tag', secondary='posts_tags', backref='posts', lazy='joined')

    @classmethod
    def get_posts_by_id(self, user_id):
        return Post.query.filter(Post.user_id == user_id).all()
    
    @classmethod
    def get_recent_posts(self):
        return Post.query.order_by(Post.created_at.desc()).limit(5).all()

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    @classmethod
    def get_all_tags(self):
        return Tag.query.order_by(Tag.name.desc()).all()


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)  