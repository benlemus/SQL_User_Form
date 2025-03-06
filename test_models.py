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
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(first_name="test", last_name="case", img_url="https://www.seosamba.com/media/products/original/tst.png")

            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
            self.user = user

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_create_user(self):
        with app.app_context():
            retrieved_user = User.query.first()

            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.first_name, 'test')
            self.assertEqual(retrieved_user.last_name, 'case')
            self.assertEqual(retrieved_user.img_url, 'https://www.seosamba.com/media/products/original/tst.png')
    
    def test_last_name_is_unique(self):
        with app.app_context():
            user2 = User(first_name="test2", last_name="case", img_url="")

            db.session.add(user2)
            
            with self.assertRaises(Exception):
                db.session.commit()


        
        

        
