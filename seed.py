""" sample data for settingup database. """

from models import User, FavoriteStores
from app import db

db.drop_all()
db.create_all()

# empty all the tables if they are not empty in modal classes
User.query.delete()
FavoriteStores.query.delete()

test_user_1 = User(firstname = 'John', lastname = 'Doe', username='jDoe', password='nopassword')
test_user_2 = User(firstname = 'Prabha', lastname = 'Niroula', username='pran', password='codingnewbie')

db.session.add(test_user_1)
db.session.add(test_user_2)
db.session.commit()

fav_store_1 = FavoriteStores(store_name='General Store', user_id = test_user_1.id, store_phone = '000-000-0000', store_address = '108050305 E Bethany Pl ')
fav_store_2 = FavoriteStores(store_name='Fancy Center', user_id = test_user_2.id, store_phone = '000-000-4674', store_address = '100300 Dayton Street, 80010')

db.session.add(fav_store_1)
db.session.add(fav_store_2)
db.session.commit()


