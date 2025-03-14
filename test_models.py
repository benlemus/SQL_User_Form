from unittest import TestCase

from models import db, User, Post
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False


with app.app_context():
    db.drop_all()
    db.create_all()

class UserModelTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.session.rollback()
            User.query.delete()
            db.session.commit()

            user = User(first_name="test", last_name="case", img_url="https://www.seosamba.com/media/products/original/tst.png")

            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
            self.first_name = user.first_name
            self.last_name = user.last_name
            self.img_url = user.img_url
            self.user = user

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            User.query.delete()
            db.session.commit()

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

    def test_order_by_name(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user1 = User(first_name="test", last_name="Bcase", img_url="")

            user2 = User(first_name="test2", last_name="Acase", img_url="")

            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            self.assertEqual(User.order_by_name(), [user2, user1])

    def test_get_full_name(self):
        self.assertEqual(self.user.full_name, f'{self.first_name} {self.last_name}') 

class PostModelTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.session.rollback()
            Post.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(first_name="test", last_name="case", img_url="https://www.seosamba.com/media/products/original/tst.png")

            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

            post = Post(title='test', content='How much wood could a woodchuck chuck, if a woodchuck could chuck wood?', created_at='2025-03-13 16:00:00.000000', user_id=user.id)

            db.session.add(post)
            db.session.commit()

            self.post_id = post.id
            self.post = post

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            Post.query.delete()
            User.query.delete()
            db.session.commit()

    def create_post(self):
        with app.app_context():
            retrieved_post = Post.query.first()

            self.assertIsNotNone(retrieved_post)
            self.assertEqual(retrieved_post.title, 'Testing')
            self.assertEqual(retrieved_post.content, 'How much wood could a woodchuck chuck, if a woodchuck could chuck wood?')
            self.assertEqual(retrieved_post.created_at, '2025-03-13 16:00:00.000000')
            self.assertEqual(retrieved_post.user_id, self.user_id)
    

    def test_get_posts_by_id(self):
        with app.app_context():
            posts = Post.get_posts_by_id(self.post.user_id)

            self.assertEqual(Post.get_posts_by_id(self.user_id), posts)

        