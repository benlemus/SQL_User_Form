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

# post model

class Post(db.Model):
    '''model for posts'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(20), nullable=False, unique=True)

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref='posts')

    @classmethod
    def get_posts_by_id(self, user_id):
        return Post.query.filter(Post.user_id == user_id).all()
