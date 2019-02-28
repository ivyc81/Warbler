"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


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


class MessageModelTestCase(TestCase):
    """Tests message model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=10000
        )

        db.session.add(u)

        message = Message(
            text="test",
            user_id=10000,
        )

        db.session.add(message)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(message.liked_by), 0)

    def test_invalid_message(self):
        """checks if not add to database if input not valid"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=10000
        )

        db.session.add(u)

        message = Message(
            text="test",
        )

        db.session.add(message)

        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        message1 = Message(
            user_id=10000
        )

        db.session.add(message1)

        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

    def test_created_by(self):
        """checs user shows up when call messaage.user"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=10000
        )

        db.session.add(u)

        message = Message(
            text="test",
            user_id=10000,
        )

        db.session.add(message)
        db.session.commit()

        self.assertEqual(message.user, u)

    def test_liked_by(self):
        """checks user shows up when call message.liked_by"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=10000
        )

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD",
            id=10001
        )

        db.session.add(u, u1)
        # db.session.add(u1)

        message = Message(
            text="test",
            user_id=10000,
        )

        db.session.add(message)
        u.liked_messages.append(message)

        db.session.commit()

        self.assertIn(u, message.liked_by)
        self.assertNotIn(u1, message.liked_by)


