from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()


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

    # db.Time? timestamp?
    created_at = db.Column(db.Text)

    # references user id
    user_id = db.Column(db.Integer, unique=True)

