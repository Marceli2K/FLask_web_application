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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://siosuser:siosuser@10.100.64.61:3306/siosuser'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(username=email, password=password),
            follow_redirects=True
        )

    def communicator(self, message_recipient, message_title, message_text  ):
        return self.app.post(
            '/communicator',
            data=dict(message_recipient=message_recipient, message_title=message_title, message_text=message_text),
            follow_redirects = True
        )
    
    def test_valid_message_sent(self):
        self.login('p@p.pl','p')
        response = self.communicator('p@p.pl','p','pppp')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message sent', response.data)

   
if __name__ == '__main__':
    unittest.main()

