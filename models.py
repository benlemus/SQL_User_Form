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

    # default='https://cdn-icons-png.flaticon.com/512/6522/6522516.png'


