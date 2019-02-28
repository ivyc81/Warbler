"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, FollowersFollowee

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app
from sqlalchemy.exc import IntegrityError

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_method(self):
        ''' determine if repr method looks like <User #1: testuser, test@test.com>'''

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=10000
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(str(u), '<User #10000: testuser, test@test.com>')

    def test_is_following(self):
        ''' determine if user1 is following user2 is detected when is_following is called '''

        user1 = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD",
                id=10000
                )

        user2 = User(
                email="test2@test.com",
                username="testuser2",
                password="HASHED_PASSWORD",
                id=20000
                )
        
        user1.following.append(user2)
        db.session.commit()

        result = user1.is_following(user2)

        self.assertTrue(result)

    def test_is_not_following(self):
        ''' determine if user1 is not detected as following user2 when not following '''

        user1 = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD",
                id=10000
                )

        user2 = User(
                email="test2@test.com",
                username="testuser2",
                password="HASHED_PASSWORD",
                id=20000
                )

        result = user1.is_following(user2)

        self.assertFalse(result)

    def test_is_followed_by(self):
        ''' determine if user2 is considered a follower of user1 '''

        user1 = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD",
                id=10000
                )

        user2 = User(
                email="test2@test.com",
                username="testuser2",
                password="HASHED_PASSWORD",
                id=20000
                )
        
        user1.followers.append(user2)
        db.session.commit()

        result = user1.is_followed_by(user2)

        self.assertTrue(result)

    def test_is_not_followed_by(self):
        ''' determine if user2 is not detected as a follower of user1 when not following '''

        user1 = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD",
                id=10000
                )

        user2 = User(
                email="test2@test.com",
                username="testuser2",
                password="HASHED_PASSWORD",
                id=20000
                )

        result = user1.is_followed_by(user2)

        self.assertFalse(result)

    def test_successful_user_signup(self):
        ''' determine that user is created when valid credentials are input '''

        user = User(
               email="test@test.com",
               username="testuser",
               password="HASHED_PASSWORD",
               id=10000
               )
        
        db.session.add(user)
        db.session.commit()

        result = User.query.get(10000)

        self.assertTrue(result)

    def test_unsuccessful_user_signup(self):
        ''' determine that user is created when invalid credentials are input '''

        user = User(
               username="testuser",
               id=10000
               )

        user2 = User(
               email="test@test.com",
               password="HASHED_PASSWORD",
               id=20000
               )

        user3 = User(
               username="testuser3",
               email="test3@test.com",
               password="HASHED_PASSWORD",
               id=30000
               )

        user4 = User(
               username="testuser3",
               email="test3@test.com",
               password="HASHED_PASSWORD",
               id=40000
               )

        db.session.add(user)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        db.session.add(user2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        
        # test non-unique values on creation of user
        db.session.add(user3)
        db.session.commit()
        db.session.add(user4)

        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
    
    def test_successful_authentication_of_user(self):
        ''' check if user authenticates when credentials are correct '''

        user = User.signup(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD",
                image_url="url"
                )

        db.session.add(user)
        db.session.commit()

        result = User.authenticate("testuser", "HASHED_PASSWORD")

        self.assertIs(result, user)

    def test_unsuccessful_authentication_of_user(self):
        ''' check if user authentication fails when credentials are incorrect '''

        user = User.signup(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD",
                image_url="url"
                )

        db.session.add(user)
        db.session.commit()

        result = User.authenticate("wrong_name", "HASHED_PASSWORD")

        self.assertFalse(result)

        result2 = User.authenticate("testuser", "wrong_pswd")

        self.assertFalse(result2)