"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from SIOS_Eimpreza import app
from SIOS_Eimpreza import database
from SIOS_Eimpreza import kalendarz
from markupsafe import escape



app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year
    )
@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='Informacje',

        year=datetime.now().year
    )

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Renders the about page."""
    if request.method == 'POST':    
        if (session['user_pass'] == request.form['user_pass']): #Remove account
            if (request.form.getlist("remove")):
                return redirect(url_for('removeacc'))
        return render_template(#ACC NOT REM
            'message.html',
            title='Home Page',
            message='Not removed',
            year=datetime.now().year
        ) 
    return render_template( #Generate profile
        'profile.html',
        title='Profile',
        year=datetime.now().year,
        message='Profile',
    ) 

@app.route('/logout')
def logout():
    # remove user data from the session if it's there
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    session.pop('user_pass', None)
    session.pop('user_type', None)
    session.pop('user_point', None)
    return redirect(url_for('home'))






