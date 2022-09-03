"""SQLAlchemy models for capstone 1 project """

from readline import append_history_file
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


# #################################################

class User(db.Model):
    """User in the website."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        # autoincrement=True # in postgres id SERIAL primary_key
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

    # image_url = db.Column(
    #     db.Text,
    #     default="/static/images/default-profile-icon.png",
    # )

    password = db.Column(       # think about password
        db.Text,      # db.String, db.Binary(60)
        nullable=False,
    )

    # email = db.Column(
    #     db.Text,
    #     nullable=False,
    #     unique=True,
    # )

    # messages = db.relationship('Message')


    # following = db.relationship(
    #     "User",
    #     secondary="follows",
    #     primaryjoin=(Follows.user_following_id == id),
    #     secondaryjoin=(Follows.user_being_followed_id == id)
    # )

    # likes = db.relationship(
    #     'Message',
    #     secondary="likes"
    # )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    # def is_followed_by(self, other_user):
    #     """Is this user followed by `other_user`?"""

    #     found_user_list = [user for user in self.followers if user == other_user]
    #     return len(found_user_list) == 1

    # def is_following(self, other_user):
    #     """Is this user following `other_use`?"""

    #     found_user_list = [user for user in self.following if user == other_user]
    #     return len(found_user_list) == 1

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8") 

        user = cls(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = User.query.filter_by(username=username).first()  

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)          
            if is_auth:                                             
                return user

        return False

# favorite stores
# class Message(db.Model):
   
#     __tablename__ = 'messages'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     text = db.Column(
#         db.String(140),
#         nullable=False,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='CASCADE'),
#         nullable=False,
#     )

#     user = db.relationship('User')


# #################################################

# goes at the end
def connect_db(app):
    """Connect this database to provided Flask app.

    Call this in the Flask app.
    """

    db.app = app
    db.init_app(app)










