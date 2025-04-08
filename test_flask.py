from unittest import TestCase
from flask import Flask

from models import db, User, Post, Tag
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()

class UsersTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.session.rollback()
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
            User.query.delete()
            db.session.commit()

    def test_list_users(self): 
        with app.test_client() as client:
            res = client.get('/')
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

            res = client.post('/users/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)     
            self.assertIn(data['first_name'], html)

    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)     
            self.assertNotIn(self.user.last_name, html)


class PostsTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.session.rollback()
            Post.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(first_name="test", last_name="case", img_url="https://www.seosamba.com/media/products/original/tst.png")

            db.session.add(user)
            db.session.commit()

            post = Post(title='test', content='How much wood could a woodchuck chuck, if a woodchuck could chuck wood?', created_at='2025-03-13 16:00:00.000000', user_id=user.id)

            db.session.add(post)
            db.session.commit()

            self.user_id = user.id
            self.user = user

            self.post_id = post.id
            self.post = post

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            Post.query.delete()
            User.query.delete()
            db.session.commit()

    def test_new_post(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/posts/new', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'Add a post for {self.user.full_name}', html)

    def test_handle_new_post_form(self):
        with app.test_client() as client:
            data = {'title':'test2', 'content':"She sells seashells on the seashore. The shells she sells are seashells, I'm sure.", 'created_at':'2025-03-13 17:0:00.000000', 'user_id':self.user_id, 'add':'2'}

            res = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)     
            self.assertIn(self.post.title, html)

            data = {'cancel':'1'}
            res = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)

            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.full_name, html)

    def test_post_details(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.post.title, html)
            self.assertIn(self.user.full_name, html)

    def test_handle_btns(self):
        with app.test_client() as client:
            data = {'cancel': '1'}
            res = client.post(f'/posts/{self.post_id}?prev=user', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.full_name, html)

            data = {'edit': '2'}
            res = client.post(f'/posts/{self.post_id}', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'Edit Post {self.post.title}', html)

            data = {'delete': '3'}
            res = client.post(f'/posts/{self.post_id}', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(self.post.content, html)
        
    def test_edit_post(self):
        with app.test_client() as client:
            res = client.get(f'/posts/{self.post_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'Edit Post {self.post.title}', html)

            data = {'title':'New Title', 'content':'New Content', 'update':'2'}

            res = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('New Title', html)      


class TagsTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.session.rollback()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
            db.session.commit()

            user = User(first_name="test", last_name="case", img_url="https://www.seosamba.com/media/products/original/tst.png")

            db.session.add(user)
            db.session.commit()

            post = Post(title='test', content='How much wood could a woodchuck chuck, if a woodchuck could chuck wood?', created_at='2025-03-13 16:00:00.000000', user_id=user.id)

            tag = Tag(name='tag test')

            db.session.add(post)
            db.session.add(tag)

            db.session.commit()

            self.post_title = post.title
            self.tag_name = tag.name

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
            db.session.commit()

    def test_show_tags(self):
        with app.test_client() as client:
            res = client.get('/tags')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'{self.tag_name}</a>', html)

    def test_handle_new_tag_form(self):
        with app.test_client() as client:
            res = client.get('/tags/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'{self.post_title}</label>', html)

            data =  {'cancel':'1'}
            res = client.post('/tags/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'{self.tag_name}</a>', html)


            data =  {'name': 'test tag2', 'checkbox': self.post_title, 'add':'1'}
            res = client.post('/tags/new', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)



            self.assertEqual(res.status_code, 200)
            self.assertIn(f'{self.post_title}</a>', html)

