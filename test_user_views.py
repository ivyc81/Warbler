"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, FollowersFollowee

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


class UserViewTestCase(TestCase):
    """Test views for users."""

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

    def test_see_follower(self):
        """Can see followers when logged in?"""

        u = User(username="other_user",
                 email="other_user@test.com",
                 password="testuser",
                 id=10000)

        db.session.add(u)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

        resp = c.get("/users/10000/following")
        resp_follower = c.get("/users/10000/followers")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_follower.status_code, 200)

    def test_cant_see_follower(self):
        """Can't see followers when logged out?"""

        u = User(username="other_user",
                 email="other_user@test.com",
                 password="testuser",
                 id=10000)

        db.session.add(u)
        db.session.commit()

        resp_following = self.client.get("/users/10000/following")
        resp_following_redirected = self.client.get("/users/10000/following",
                                                    follow_redirects=True)
        resp_follower = self.client.get("/users/10000/followers")
        resp_follower_redirected = self.client.get("/users/10000/followers",
                                                   follow_redirects=True)

        self.assertEqual(resp_following.status_code, 302)
        self.assertIn(b"Access unauthorized.", resp_following_redirected.data)

        self.assertEqual(resp_follower.status_code, 302)
        self.assertIn(b"Access unauthorized.", resp_follower_redirected.data)

    def test_homepage_if_not_logged_in(self):
        ''' should show home-anon.html if not logged in '''

        resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"New to Warbler?", resp.data)

    def test_homepage_if_logged_in(self):
        '''should show page with user profile card as homepage if logged in'''
        user = User.query.filter(User.username == "testuser").first()
        user.id = 10000
        db.session.commit()

        self.client.post("/login",
                         data={"username": "testuser",
                               "password": "testuser"})

        resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'<a href="/users/10000" class="card-link">', resp.data)

    def test_homepage_shows_messages_from_followed_people(self):
        '''only messages from people we follow should show'''

        followed_u = User(username='followed',
                          password='password',
                          email='followed@test.com',
                          id=999)

        not_followed_u = User(username='not_followed',
                              password='password',
                              email='not_followed@test.com',
                              id=888)

        followed_message = Message(text='Followed (message)',
                                   user_id=999)

        not_followed_message = Message(text='Not followed (message)',
                                       user_id=888)

        db.session.add_all([followed_u,
                            not_followed_u,
                            followed_message,
                            not_followed_message])

        current_user = User.query.filter(User.username == "testuser").first()

        current_user.following.append(followed_u)
        
        db.session.commit()

        self.client.post("/login",
                         data={"username": "testuser",
                               "password": "testuser"})

        resp = self.client.get('/')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Followed (message)', resp.data)
        self.assertNotIn(b'Not followed (message)', resp.data)

    def test_user_profile_when_logged_out(self):
        '''should show user profile page wihtout edit and delete profile'''

        user = User.query.filter(User.username == "testuser").first()
        user.id = 10000
        db.session.commit()

        resp = self.client.get('/users/10000')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'<p class="small">Likes</p>', resp.data)
        self.assertNotIn(b'Edit Profile</a>', resp.data)
        self.assertNotIn(b'Delete Profile</button>', resp.data)

    def test_user_profile_when_logged_in(self):
        '''should show user profile page with edit and delete profile'''

        user = User.query.filter(User.username == "testuser").first()
        user.id = 10000
        db.session.commit()

        self.client.post("/login",
                         data={"username": "testuser",
                               "password": "testuser"})

        resp = self.client.get('/users/10000')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'<p class="small">Likes</p>', resp.data)
        self.assertIn(b'Edit Profile</a>', resp.data)
        self.assertIn(b'Delete Profile</button>', resp.data)


