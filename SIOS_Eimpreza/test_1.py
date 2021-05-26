import unittest
from SIOS_Eimpreza import app
from SIOS_Eimpreza import views
from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from SIOS_Eimpreza import database
from SIOS_Eimpreza import kalendarz
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
import cryptography
from flask import session

db = SQLAlchemy(app)
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootdrut123@x.x.x.x:x/mydb'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def register(self, email, password):
        return self.app.post(
            '/register',
            data=dict(username=email, password=password),
            follow_redirects=True
        )
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(username=email, password=password),
            follow_redirects=True
        )
    def profile(self,password, remove):
        return self.app.post(
            '/profile',
            data=dict(password=password, remove=remove),
            follow_redirects=True
        )
    def addnews(self, comment):
        return self.app.post(
            '/addnews',
            data=dict(comment=comment),
            follow_redirects=True
    )
    def dodaj_wydarzenie(self, eventname, eventdate, eventtime, idorg):
        return self.app.post(
            '/dodaj_wydarzenie',
            data=dict(eventname=eventname, eventdate=eventdate,eventtime=eventtime, idorg=idorg),
            follow_redirects=True
        
        )
    def test_valid_user_registration(self):
        response = self.register('test@test.test', 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added', response.data)
    def test_valid_user_login(self):
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_unvalid1_user_delete(self):
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.profile('FlaskIsAwesome', None)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Not removed', response.data)

    def test_unvalid2_user_delete(self):
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.profile('yea', 'remove')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Not removed', response.data)

    def test_valid_user_delete(self):
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.profile('FlaskIsAwesome', 'remove')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account removed', response.data)
        
	#test dodania aktualności
    def test_valid_news_add(self):
        response = self.addnews('TEST')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'News Added', response.data)


    def test_unvalid_eventdate(self):
        response = self.dodaj_wydarzenie('JuwenaliaTEST', '2019-01-01', '12:00', 13)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Zla data', response.data)

    #def test_valid_eventdate(self):
    #    response = self.dodaj_wydarzenie('JuwenaliaTEST', '2021-01-01', '12:00', 13)
    #    self.assertEqual(response.status_code, 200)
    #    self.assertIn(b'Event added', response.data)


if __name__ == '__main__':
    unittest.main()
