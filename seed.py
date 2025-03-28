from models import db, User, Post, Tag, PostTag
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()
    Post.query.delete()

    milo = User(first_name='Milo', last_name='Taylor', img_url='https://i0.wp.com/jimcoda.com/wp-content/uploads/2018/05/E0A6421-Elk-Calf-Yellowstone-Jim-Coda-20140619-830pix.jpg?fit=830%2C553&ssl=1')

    marvin = User(first_name='Marvin', last_name='Lemor', img_url='https://images.photowall.com/products/69237/lion-close-up.jpg?h=699&q=85')

    mojo = User(first_name='Mojo', last_name='Lemus', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq1C2FrebT4DbIExkejoMYfuE92NJBQsDjBg&s')

    kori = User(first_name='Kori', last_name='tAylor', img_url='')


    db.session.add(milo)
    db.session.add(marvin)
    db.session.add(mojo)
    db.session.add(kori)
    db.session.commit()


    post1 = Post(title='walks', content='I like to go on walks to the park to see my friends', user_id=1)

    post2 = Post(title='treats', content='treats are very yummy', user_id=2)

    post3 = Post(title='siblings', content='milo and mojo are my brothers', user_id=2)

    post4 = Post(title='day in the life', content='Wake up, eat, nap, lay in sun, use the litter box, chase marvin, nap, play with milo, nap, eat, run around the house, cause havok', user_id=3)

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.commit()

    funny = Tag(name='funny')
    english = Tag(name='english')

    db.session.add(funny)
    db.session.add(english)
    db.session.commit()

    post_tags = PostTag(post_id=1, tag_id=1)
    post_tags2 = PostTag(post_id=1, tag_id=2)

    db.session.add(post_tags)
    db.session.add(post_tags2)
    db.session.commit()

   