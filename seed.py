from models import db, User
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()

    milo = User(first_name='Milo', last_name='Taylor', img_url='https://miro.medium.com/v2/resize:fit:720/format:webp/1*rIkmavUeqyRySwlQdA9kKg.jpeg')
    marvin = User(first_name='Marvin', last_name='Lemor')

    db.session.add(milo)
    db.session.add(marvin)
    db.session.commit()