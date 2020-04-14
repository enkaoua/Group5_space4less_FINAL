import unittest

from flask import url_for
from flask_login import login_user, current_user
from flask_testing import TestCase
from app import create_app, db

from app.models import User
from app.config import TestConfig


class BaseCase(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        # Called before every test
        db.create_all()
        # test data
        self.propertyowner = User(username="Atlas", first_name="property", last_name="owner", email="atlas@gmail.com",
                                  roles="property_owner")
        self.propertyowner.set_password('1234')

        self.renter = User(username="Luna", first_name="rent", last_name="er", email="luna@gmail.com",
                           roles="renter")
        self.renter.set_password('5678')
        db.session.add(self.propertyowner)
        db.session.add(self.renter)
        db.session.commit()

    def tearDown(self):
        # to remove test data from database
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get(
            '/logout',
            follow_redirects=True
        )

    def signup(self, username, last_name, first_name,  email, password, roles):
        return self.client.post(
            '/signup',
            data=dict(username=username, first_name=first_name, last_name=last_name, email=email, password=password,
                      roles=roles),
            follow_redirects=True
        )



    def test_login_fails_with_invalid_details(self):
        response = self.login(email='atlas@gmail.com', password='password')
        self.assertIn(b'Invalid username or password', response.data)

    def test_signup_page_valid(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_succeeds_with_valid_details(self):
        response = self.login(email='luna@gmail.com', password='5678')
        self.assertIn(b'Login successful!', response.data)

    def test_registration_valid_details(self):
        count = User.query.count()
        response = self.client.post(url_for('auth.signup'), data=dict(
            username=self.renter_data.get('Luna'),
            first_name=self.renter_data.get('rent'),
            last_name=self.renter_data.get('er'),
            email=self.renter_data.get('email'),
            password=self.renter_data.get('password'),
            roles=self.renter_data.get('role')
        ), follow_redirects=True)
        count2 = User.query.count()
        self.assertEqual(count2 - count, 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    renter_data = dict(username='Luna', first_name="rent", last_name="er", email="luna@gmail.com",
                       roles='renter', password='5678')
    propertyOwner_data = dict(username='Alan', first_name="proper", last_name="own", email="name@gmail.com",
                              roles='property_owner', password='pass')
    post_data = dict(title='property1', content='this is some content', location='earth', space_size='M')



    # def test_adding_a_post_success(self):
    #     with self.client:
    #         self.login(self.propertyowner.email, self.propertyowner.password)
    #         response = self.client.post(
    #             '/post',
    #             data=dict(title='post1', content='content', location='location', space_size='M', current_user=current_user),
    #             follow_redirects=True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #
    # def booking_is_a_success(self):
    #     response = self.client.book(url_for('booking.'))


if __name__ == '__main__':
    unittest.main()
