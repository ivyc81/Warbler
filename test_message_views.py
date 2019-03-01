"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.add(self.testuser)
        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id


            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})
            # import pdb; pdb.set_trace()

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_unauthorized_new_message_when_logged_out(self):
        """trying to create new message when logged out should redirect to homepage"""

        resp_post = self.client.post("/messages/new", data={"text": "Hello"})
        resp_post_redirected = self.client.post("/messages/new",
                                                data={"text": "Hello"},
                                                follow_redirects=True)
        resp_get = self.client.post("/messages/new")
        resp_get_redirected = self.client.post("/messages/new",
                                               follow_redirects=True)

        self.assertEqual(resp_post.status_code, 302)
        self.assertIn(b"Access unauthorized.", resp_post_redirected.data)

        self.assertEqual(resp_get.status_code, 302)
        self.assertIn(b"Access unauthorized.", resp_get_redirected.data)

    def test_unauthorized_delete_when_logged_out(self):
        """trying to delete message when logged out should redirect to homepage"""

        u = User(username="other_user",
                 email="other_user@test.com",
                 password="testuser",
                 id=10000)

        message = Message(text="text",
                          user_id=10000,
                          id=10000)

        db.session.add(u)
        db.session.add(message)
        db.session.commit()

        resp_delete = self.client.post("/messages/10000/delete")
        resp_delete_redirected = self.client.post("/messages/10000/delete",
                                                  follow_redirects=True)

        self.assertEqual(resp_delete.status_code, 302)
        self.assertIn(b"Access unauthorized.", resp_delete_redirected.data)

    def test_unauthorized_delete_when_not_author(self):
        """trying to delete message when not author should redirect to homepage"""

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess[CURR_USER_KEY] = self.testuser.id

        logged_in_user = self.client.post("/login", data={"username":"testuser", "password":"testuser"})

        u = User(username="other_user",
                email="other_user@test.com",
                password="testuser",
                id=10000)

        message = Message(text="text",
                        user_id=10000,
                        id=10000)

        db.session.add(u)
        db.session.add(message)
        db.session.commit()

        resp_delete = self.client.post("/messages/10000/delete")
        resp_delete_redirected = self.client.post("/messages/10000/delete",
                                                follow_redirects=True)

        self.assertEqual(resp_delete.status_code, 302)
        self.assertIn(b"Access unauthorized.", resp_delete_redirected.data)

    def test_authorized_delete(self):
        """trying to delete message when authorized"""

        user = User.query.filter(User.username == "testuser").first()

        message = Message(text="text",
                          user_id=user.id,
                          id=10000)

        self.client.post("/login", data={"username": "testuser",
                                         "password": "testuser"})

        db.session.add(message)
        db.session.commit()

        resp_delete = self.client.post("/messages/10000/delete")

        self.assertEqual(resp_delete.status_code, 302)

        deleted_message = Message.query.get(message.id)
        self.assertIsNone(deleted_message)

    




