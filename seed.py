# To run this file
# (venv) $ createdb restaurants_db
# (venv) $ python seed.py or python3 seed.py


""" sample data for settingup database """

from models import User
from app import db

# delete all tables if exist and create all tables again
db.drop_all()
db.create_all()

# empty all the tables if they are not empty in User modal class
User.query.delete()

# instantiate User and create new users
test_user_1 = User(firstname = 'John', lastname = 'Doe', username='jDoe', password='nopassword')
test_user_2 = User(firstname = 'Prabha', lastname = 'Niroula', username='pran', password='codingnewbie')

# add new users to session(stagin area)
db.session.add(test_user_1)
db.session.add(test_user_2)

# commit them (or save them to database )
db.session.commit()

