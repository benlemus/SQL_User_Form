from models import db, User
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

    milo = User(first_name='Milo', last_name='Taylor', img_url='https://i0.wp.com/jimcoda.com/wp-content/uploads/2018/05/E0A6421-Elk-Calf-Yellowstone-Jim-Coda-20140619-830pix.jpg?fit=830%2C553&ssl=1')

    marvin = User(first_name='Marvin', last_name='Lemor', img_url='https://images.photowall.com/products/69237/lion-close-up.jpg?h=699&q=85')

    mojo = User(first_name='Mojo', last_name='Lemus', img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq1C2FrebT4DbIExkejoMYfuE92NJBQsDjBg&s')

    kori = User(first_name='Kori', last_name='tAylor', img_url='')


    db.session.add(milo)
    db.session.add(marvin)
    db.session.add(mojo)
    db.session.add(kori)
    db.session.commit()