from unittest import TestCase

from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
    db.drop_all()
    db.create_all()

class FlaskTestCase(TestCase):
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

    def test_list_users(self): 
        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.first_name, html)

    def test_user_details(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.last_name, html) 

    def test_create_user(self):
        with app.test_client() as client:
            data = {'first_name':'test2', 'last_name':'case2', 'img_url': ''}

            res = client.post('/users', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)     
            self.assertIn(data['first_name'], html)

    def test_delete_user(self):
        # TODO
        pass
