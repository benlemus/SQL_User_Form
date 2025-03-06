from unittest import TestCase

from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
    db.drop_all()
    db.create_all()

class ModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()
    
    def tearDown(self):
        db.session.rollback()

