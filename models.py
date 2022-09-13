""" SQLAlchemy models for local restaurants finder app. """

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """ User in the website."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    firstname = db.Column(
        db.Text,
        nullable=False,
        unique=False,
    )

    lastname = db.Column(
        db.Text,
        nullable=False,
        unique=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,      
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, firstname, lastname, username, password):
        """ Signs up a user. """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8") 

        user = cls(
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=hashed_pwd
        )
        return user
                

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method. So, call it on the class, not an individual user. It searches for a user whose 
        password hash matches this password and, if it finds such a user, returns that user object. If can't find 
        matching user (or if password is wrong), returns False.
        """

        user = User.query.filter_by(username=username).first()
  
        verify = bcrypt.check_password_hash(user.password, password)
        if user and verify:
            return user

        return False


class FavoriteStores(db.Model):
   
    __tablename__ = 'favorite_stores'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    store_name = db.Column(
        db.String(140),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    store_phone = db.Column(
        db.String,
        nullable = True,
    )
    store_address = db.Column(
        db.String,
        nullable = True
    )

    user = db.relationship('User')


def connect_db(app):
    """Connect this database to provided Flask app. Call this in the Flask app."""

    db.app = app
    db.init_app(app)










