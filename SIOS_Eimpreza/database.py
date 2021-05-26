from SIOS_Eimpreza import app
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, session, redirect, url_for, request
from flask import current_app, Markup, request, Blueprint, url_for
import pymysql
import cryptography
from datetime import datetime
import re
import string
import random
from SIOS_Eimpreza import kalendarz


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://siosuser:siosuser@x.x.x.x:x/siosuser'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(45),unique=True)
    user_name = db.Column(db.String(45))
    user_pass = db.Column(db.String(45))
    user_type = db.Column(db.Integer, default=0)
    user_point = db.Column(db.Integer, default=0)

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(45))
    event_starttime = db.Column(db.TIMESTAMP)
    event_endtime = db.Column(db.TIMESTAMP)
    event_desc = db.Column(db.TEXT)
    event_org = db.Column(db.Integer)
    event_point = db.Column(db.Integer, default=0)

class News(db.Model):
    news_id = db.Column(db.Integer, primary_key=True)
    news_event = db.Column(db.Integer)
    news_text = db.Column(db.TEXT)
    news_pic = db.Column(db.BLOB)

class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(45))

class Notification(db.Model):
    notification_event = db.Column(db.Integer, primary_key=True)
    notification_user = db.Column(db.Integer, primary_key=True)
    notification_isread = db.Column(db.BOOLEAN, default=0)

class Event_tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, primary_key=True)

class Event_user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, primary_key=True)
    event_status = db.Column(db.Integer)
    in_callendar = db.Column(db.Integer)

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message_sender = db.Column(db.Integer)
    message_recipient = db.Column(db.Integer)
    message_title = db.Column(db.String(100))
    message_text = db.Column(db.TEXT)

class Notification_news(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, primary_key=True)
    is_read = db.Column(db.BOOLEAN, default=0)


class Form(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    Int_val_1 = db.Column(db.Integer, default=0)
    Int_val_2 = db.Column(db.Integer, default=0)
    Int_val_3 = db.Column(db.Integer, default=0)
    Int_val_4 = db.Column(db.Integer, default=0)
    Int_val_5 = db.Column(db.Integer, default=0)
    Str_val_1 = db.Column(db.String(45))

@app.route('/editevent/<event_id>', methods=['GET', 'POST'])
def editevent(event_id):
    if request.method == "POST":

        event_name = request.form['event_name']
        event_starttime = request.form['event_starttime']
        event_endtime = request.form['event_endtime']
        event_desc = request.form['event_desc'] 
        current_event= Event.query.filter_by(event_id=event_id).first()

        if(current_event.event_desc!=request.form['event_desc']):
            current_event.event_desc=request.form['event_desc']


        if event_name != "":
            current_event.event_name = event_name


        if event_starttime != "":
            date_start= datetime.strptime(event_starttime, '%Y-%m-%dT%H:%M')
        if event_endtime != "":
            date_end= datetime.strptime(event_endtime, '%Y-%m-%dT%H:%M')
        
        if event_starttime == "" and event_endtime == "":
            print("meh")
        elif event_starttime == "":
            if date_end < current_event.event_starttime:
                return render_template(
                    'message.html',
                    title='Edycja wydarzenia',
                    message='Błędne dane'
                )
        elif event_endtime == "":
            if current_event.event_endtime < date_start:
                return render_template(
                    'message.html',
                    title='Edycja wydarzenia',
                    message='Błędne dane'
                )
        else:
            if date_end < date_start:
                return render_template(
                    'message.html',
                    title='Edycja wydarzenia',
                    message='Błędne dane'
                )
        

        if (event_starttime != ""):# and (date_start >= current_event.event_starttime):
            if date_start >= current_event.event_starttime:
                current_event.event_starttime = date_start
        if (event_endtime != ""):# and (date_end >= current_event.event_starttime):
            if date_end >= current_event.event_starttime:
                current_event.event_endtime = date_end
        db.session.commit()
        return render_template(
            'message.html',
            title='Edycja wydarzenia',
            message='Zmiany zapisano pomyślnie'
        )

    return render_template(
    'editevent.html',
    title='EditEvent',
    year=datetime.now().year
    )

@app.route('/deleteevent/<event_id>', methods=['GET', 'POST'])
def deleteevent(event_id):
    if request.method == "POST":

        current_event= Event.query.filter_by(event_id=event_id).first()
        
        
        db.session.delete(current_event)
        print("xDD")
        db.session.commit()
        return render_template(
            'message.html',
            title='Usuwanie wydarzenia',
            message='Pomyślnie usunięto wydarzenie'
        )

    return render_template(
            'message.html',
            title='Usuwanie wydarzenia',
            message='Pomyślnie usunięto wydarzenie'
        )



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the about page."""
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        user_pass = request.form['user_pass']
        if re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", user_email):
            user = User(user_name=user_name, user_email=user_email, user_pass=user_pass)
            db.session.add(user)
            db.session.commit()
            return render_template(
                'message.html',
                title='Home Page',
                message='User added',
                year=datetime.now().year
            )
        else:
            return render_template(
                'message.html',
                title='Home Page',
                message='Invalid data',
                year=datetime.now().year
            )

    return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year
    ) 

@app.route('/adminOrgTool', methods=['GET', 'POST'])
def adminOrgTool():
    if request.method == 'POST':
        org_name = request.form['org_name']
        org_email = request.form['org_email']
        if re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", org_email):
            LETTERS = string.ascii_letters
            NUMBERS = string.digits  
            PUNCTUATION = string.punctuation    
            printable= f'{LETTERS}{NUMBERS}{PUNCTUATION}'
            printable = list(printable)
            random.shuffle(printable)
            k=8
            random_password = random.choices(printable, k=8)
            random_password = ''.join(random_password)
            orgFull = User(user_name=org_name, user_email=org_email, user_pass=random_password,user_type=1)
            db.session.add(orgFull)
            db.session.commit()
            return render_template(
                    'message.html',
                    title='Dodano organizatora',
                    message='Dodano organizatora ' + org_name,
                    year=datetime.now().year
                )
        else:
            return render_template(
                    'message.html',
                    title='Dodano organizatora',
                    message='Bledne dane',
                    year=datetime.now().year
                )

    return render_template(
        'adminOrgTool.html',
        title='Zarzadzanie organizatorami',
        year=datetime.now().year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the about page."""
    if request.method == 'POST':
        user_email = request.form['user_email']
        user_pass = request.form['user_pass']

        user = User.query.filter_by(user_email=user_email, user_pass=user_pass).first()

        if (user==None):
            return render_template(
                'message.html',
                title='Home Page',
                message='There is no such user. Try again',
                year=datetime.now().year
            ) 
        session['user_id']=user.user_id
        session['user_email']=user.user_email
        session['user_name']=user.user_name
        session['user_pass']=user.user_pass
        session['user_type']=user.user_type
        session['user_point']=user.user_point
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year
    )

@app.route('/addnews', methods=['GET', 'POST'])
def addnews():
    if request.method == 'GET':
        return render_template(
            'addnews.html',
            title='addnews',
            event = request.args.get('event_id'),
            year=datetime.now().year
        ) 
    if request.method == 'POST':
            news_text = request.form['comment']
            news = News(news_event = request.form['event'],news_text = news_text)
            db.session.add(news)
            db.session.commit()
            
            notifi = Notification.query.filter_by(notification_event=request.form['event']).all()   # Add notification for each user that is interested in event conectedd to this news
            for row in notifi:
                newsnoti = Notification_news(event_id=request.form['event'], user_id=row.notification_user, news_id = news.news_id)
                db.session.add(newsnoti) 
            db.session.commit() # end 
        
            return render_template(
                    'message.html',
                    title='Home Page',
                    message='News Added',
                    year=datetime.now().year
                ) 
    

@app.route('/removeacc')
def removeacc():
    obj = User.query.filter_by(user_id=session['user_id']).one() #get user by id saved in session
    db.session.delete(obj) #remove user 
    db.session.commit()
    session.pop('user_id', None) #clear session info about logged user
    session.pop('user_email', None)
    session.pop('user_name', None)
    session.pop('user_pass', None)
    session.pop('user_type', None)
    session.pop('user_point', None)
    return render_template( #ACC REM
        'message.html',
        title='Home Page',
        message='Account removed',
        year=datetime.now().year
    ) 

@app.route('/dodaj_wydarzenie', methods=['GET', 'POST'])
def dodaj_wydarzenie():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_starttime = request.form['event_starttime']
        event_endtime = request.form['event_endtime']
        event_point = int(request.form['event_point'])

        event_desc = request.form['event_desc']
        if event_desc=="":
            event_desc="Organizator wydarzenia nie dodał jeszcze opisu"

        if request.form['event_name'] == "" :
            return render_template(
                'message.html',
                title='Home Page',
                message='Musisz okreslic nazwe przy tworzeniu wydarzenia',
                year=datetime.now().year
            )
        if request.form['event_starttime'] == "" or request.form['event_endtime'] == "":
            return render_template(
                'message.html',
                title='Home Page',
                message='Musisz okreslic date przy tworzeniu wydarzenia',
                year=datetime.now().year
            )
        date_start= datetime.strptime(event_starttime, '%Y-%m-%dT%H:%M')
        date_end= datetime.strptime(event_endtime, '%Y-%m-%dT%H:%M')

        if (date_start<datetime.today() and date_start<date_end):
            return render_template(
                'message.html',
                title='Home Page',
                message='Zla data',
                year=datetime.now().year
            )
        if event_point<0:
            return render_template(
                'message.html',
                title='Home Page',
                message='Ujemna ilosc punktow!',
                year=datetime.now().year
            )
        event = Event(event_name=event_name, event_starttime=event_starttime, event_endtime=event_endtime, event_point=event_point,  event_org = session['user_id'], event_desc=event_desc )
        db.session.add(event)
        db.session.commit()
        return render_template(
            'message.html',
            title='Home Page',
            message='Dodano wydarzenie',
            year=datetime.now().year
        )
    return render_template(
        'dodaj_wyd.html',
        title='Dodawanie wydarzenia',
	    year=datetime.now().year
        )

@app.route('/powiadomienia', methods=['GET', 'POST'])
def notification():
    if request.method == 'POST':
        lista = request.form['to_delete']
        lista = lista.replace(',', ' ')
        lista = lista.replace('(', '')
        lista = lista.replace(')', '')
        lista = lista.split()
        try:
            str1 = ''.join(lista[0])
            str2 = ''.join(lista[1])
        except:
            print("Error")
            return render_template('message.html', message ='Nieprawidlowe wydarzenie')

        to_delete = int(float(str1))
        news_id = int(float(str2))
        #Ustawienie powiadomienia jako odczytane
        notifi = Notification_news.query.filter_by(event_id=to_delete, user_id = session['user_id'], news_id = news_id ).first() 
        notifi.is_read = 1
        print(notifi.is_read)
        db.session.commit()
        #end

    return render_template('powiadomienia.html', records = db.session.query(Notification_news, User, Event, News).join(Notification_news, User.user_id == Notification_news.user_id).join(Event, Event.event_id == Notification_news.event_id).join(News, News.news_id == Notification_news.news_id).filter(Notification_news.is_read ==0, User.user_id == session['user_id']).add_columns(User.user_id,Event.event_id,Event.event_name, Event.event_desc, News.news_id, News.news_text).all()
) 



@app.route('/addnotify', methods=['GET', 'POST'])
def addnotify():
    if request.method == 'GET':
        notifi = Notification(notification_event = request.args['event_id'], notification_user = session['user_id'])
        db.session.add(notifi)
        db.session.commit()
    return redirect(url_for('details', event = request.args['event_id']))

#WYDARZENIA AKTUALNE
@app.route('/wydarzenia',methods=['GET', 'POST'])
def wydarzenia():
    if request.method == 'POST':
        if request.form['tag'] != "":
            return render_template(
                'wydarzenia.html',
                title='Events',
                tagtab = Tag.query.all(),
                eventtab = db.session.query(Event_tag, Event).join(Event_tag, Event_tag.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc, Event_tag.tag_id).filter(Event_tag.tag_id == request.form['tag'], Event.event_endtime > datetime.today()).all()
            )
    return render_template(
        'wydarzenia.html',
        title='Events',
        tagtab = Tag.query.all(),
        eventtab = Event.query.filter(Event.event_endtime > datetime.today()).all()
    )

#WYDARZENIA HISTORYCZNE
@app.route('/wydarzeniaHistoryczne',methods=['GET', 'POST'])
def wydarzeniaHistoryczne():

    if request.method == 'POST':
        if request.form['tag'] != "":
            return render_template(
                'wydarzeniaHistoryczne.html',
                title='Events',
                tagtab = Tag.query.all(),
                eventtab = db.session.query(Event_tag, Event).join(Event_tag, Event_tag.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc, Event_tag.tag_id).filter(Event_tag.tag_id == request.form['tag'], Event.event_endtime < datetime.today()).all()
            )
    return render_template(
        'wydarzeniaHistoryczne.html',
        title='Events',
        tagtab = Tag.query.all(),
        eventtab = Event.query.filter(Event.event_endtime < datetime.today()).all()
    )

@app.context_processor
def utility_processor():#funkcja liczaca po event_id
    def count_user(event_id):
        return Event_user.query.filter_by(event_id = event_id, event_status = not 0).count()
    return dict(count_user=count_user)

#MOJE WYDARZENIA
@app.route('/my_events')
def my_events():
    eveOrganise = Event.query.filter_by(event_org = session['user_id']).all()
    formtab =  db.session.query(Form, Event_user).join(Form, Form.event_id == Event_user.event_id).filter(Form.user_id ==session['user_id'], Event_user.event_status>=2 ).all()
    eventtab2 = db.session.query(Event_user, Event ).join(Event_user, Event_user.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc,  Event_user.event_status).filter(Event_user.user_id ==session['user_id'], Event_user.event_status >= 2 ).all()
    eventtab = db.session.query(Event_user, Event).join(Event_user, Event_user.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc,  Event_user.event_status).filter(Event_user.user_id ==session['user_id'], Event_user.event_status==1 ).all()
   
    return render_template(
        'my_events.html',
        title='Moje wydarzenia',
        eventtab = eventtab,
        eventtab2 = eventtab2,
        formTab = formtab,
        eveOrganise =eveOrganise
    )
#MOJJE WYDARZENIA HISTORYCZNE
@app.route('/my_events_historic')
def my_events_historic():

    #####status
    current_event= Event.query.filter(Event_user.event_status==1, Event.event_endtime < datetime.today()).all()
    
    for x in current_event:
        event_usertab = Event_user.query.filter_by(event_id=x.event_id, user_id = session['user_id']).first()
        print(event_usertab)
        try:
            changestatus(event_usertab)
        except:
            print("Cannot change event_status")



    eveOrganise = Event.query.filter_by(event_org = session['user_id']).all()
    print(eveOrganise)
    formtab =  db.session.query(Form, Event_user).join(Form, Form.event_id == Event_user.event_id).filter(Form.user_id ==session['user_id'], Event_user.event_status>=2 ).all()
    eventtab2 = db.session.query(Event_user, Event ).join(Event_user, Event_user.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc,  Event_user.event_status).filter(Event_user.user_id ==session['user_id'], Event_user.event_status >= 2 ).all()
    eventtab = db.session.query(Event_user, Event).join(Event_user, Event_user.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc,  Event_user.event_status).filter(Event_user.user_id ==session['user_id'], Event_user.event_status==1 ).all()
    return render_template(
        'my_events_historic.html',
        title='Moje wydarzenia',
        eventtab = eventtab,
        eventtab2 = eventtab2,
        formTab = formtab,
        eveOrganise =eveOrganise
    )
#WYDARZENIA W KTORYCH  JESTEM ORGANIZATOREM
@app.route('/my_events_organise')
def my_events_organise():
    eveOrganise = Event.query.filter_by(event_org = session['user_id']).all()
    print(eveOrganise)
    formtab =  db.session.query(Form, Event_user).join(Form, Form.event_id == Event_user.event_id).filter(Form.user_id ==session['user_id'], Event_user.event_status>=2 ).all()
    eventtab2 = db.session.query(Event_user, Event ).join(Event_user, Event_user.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc,  Event_user.event_status).filter(Event_user.user_id ==session['user_id'], Event_user.event_status >= 2 ).all()
    eventtab = db.session.query(Event_user, Event).join(Event_user, Event_user.event_id == Event.event_id).add_columns(Event.event_id, Event.event_name, Event.event_desc,  Event_user.event_status).filter(Event_user.user_id ==session['user_id'], Event_user.event_status==1 ).all()
    return render_template(
        'my_events_organise.html',
        title='Moje wydarzenia',
        eventtab = eventtab,
        eventtab2 = eventtab2,
        formTab = formtab,
        eveOrganise =eveOrganise
    )
      
@app.route('/details/<path:event>', methods=['GET', 'POST'])
def details(event):
    if (session.get('user_id')):
        current_event= Event.query.filter_by(event_id=event).first()
        event_user=Event_user(user_id=session['user_id'], event_id=current_event.event_id)
        event_usertab = Event_user.query.filter_by(event_id=event, user_id = session['user_id']).first()


        aa=""
        if (request.method == 'POST'):   
            if (request.form.get('but1')=="participate"):
                participate(event_usertab, event_user, current_event)#weź udział/zrezygnuj z wydarzenia
           
            if (request.form.get('but1')=="add_to_callendar"):
                kalendarz.kalendarz(current_event)#dodawanie wydarzenia do kalendarza google           
                if(event_usertab.event_status==1):
                    event_usertab.in_callendar=1
                    db.session.commit()               
        if (event_usertab):                
            if (event_usertab.in_callendar==0):
                aa="Dodaj do kalendarza"
                
            else: 
                aa="Dodaj ponownie do kalendarza"
        else:
        	aa="Dodaj do kalendarza"
   
    

    
        return render_template(
    		'details.html',
        	title='Events',
        	current_event = Event.query.filter_by(event_id=event).first(),
        	event_usertab = Event_user.query.filter_by(event_id=event, user_id = session['user_id']).first(),
        	notifitab = Notification.query.filter_by(notification_user=session['user_id'], notification_event=event).first(),
        	przycisk_dodaj_do_kalendarza=aa,
        	current_news = News.query.filter_by(news_event=event).all()
    		)    
    else:
        return render_template(
    	    'detailsunlog.html',
        	title='Events',
        	current_event = Event.query.filter_by(event_id=event).first(),
            current_news = News.query.filter_by(news_event=event).all()
           
    	)
            
@app.route('/admintools',methods=['GET', 'POST'])
def admintools():
    if request.method == 'POST':
        if(request.form['user_type']):
            user = User.query.filter_by(user_id=request.form['user_type']).first()
            if user == None:
                return render_template(
                    'admintools.html',
                    title='Admintab',
                    usertab = User.query.all()
                )
            elif user.user_type == 0:
                user.user_type = 1
            elif user.user_type == 1:
                user.user_type = 0
            db.session.commit()
    return render_template(
        'admintools.html',
        title='Admintab',
        usertab = User.query.all()
    )
@app.route('/form/<path:event>', methods=['GET', 'POST'])
def form(event):
    if request.method == 'POST':
        event_id=event
        current_event= Event.query.filter_by(event_id=event).first()
        event_user=Event_user(user_id=session['user_id'], event_id=current_event.event_id)
        event_usertab = Event_user.query.filter_by(event_id=event, user_id = session['user_id']).first()
        addpoints(event_usertab, current_event)
        user_id = session['user_id']
        if (request.form.get('pyt1')=="1"):
            Int_val_1 = 1
        elif(request.form.get('pyt1')=="2"):
            Int_val_1 = 2
        elif(request.form.get('pyt1')=="3"):
            Int_val_1 = 3
        elif(request.form.get('pyt1')=="4"):
            Int_val_1 = 4
        else:
            Int_val_1 = 5
        if (request.form.get('pyt2')=="tak"):
            Int_val_2 = 1
        else:
            Int_val_2 = 0
        if (request.form.get('pyt3')=="tak"):
            Int_val_3 = 1
        else:
            Int_val_3 = 0
        if (request.form.get('pyt4')=="tak"):
            Int_val_4 = 1
        else:
            Int_val_4 = 0
        if (request.form.get('pyt5')=="tak"):
            Int_val_5 = 1
        else:
            Int_val_5 = 0
        print(request.form.get('uwagi'))
        Str_val_1 = request.form.get('uwagi')
        form = Form(event_id = event_id, user_id = user_id, Int_val_1 = Int_val_1, Int_val_2 = Int_val_2, Int_val_3 = Int_val_3, Int_val_4 = Int_val_4, Int_val_5 = Int_val_5, Str_val_1 = Str_val_1)
        db.session.add(form)
        edita = Event_user.query.filter_by(event_id = event, user_id = session['user_id']).first()
        edita.event_status = 3

        try:
            db.session.commit()
        except:
            print("Nastąpił błąd aktualizowania danych w bazie danych!!!")
            return render_template(
                    'message.html',
                    title='Home Page',
                    message='Invalid data',
                    year=datetime.now().year)
        return render_template('message.html',
                              message ='Dziekuje za udzial w ankiecie!')
    return render_template('form.html', records = "xd" ) #('message.html', message ='Dziekuje za udzial w ankiecie!')

#metoda wywyłana w details
def participate(event_usertab,event_user,current_event):
  
    notifi_tab = Notification.query.filter_by(notification_event=current_event.event_id, notification_user = session['user_id']).first()
    
    
    if (event_usertab == None):
        event_user.event_status=1
        event_user.in_callendar=0
        db.session.add(event_user)
        db.session.commit()

        
        if notifi_tab == None: #Dodawanie wydarzenia w którym wzięło się udział do bazy powiadomień
            add_To_notifi(current_event)
    elif(event_usertab.event_status==1):
        event_usertab.event_status=0
        db.session.commit()
        Del_notifi(notifi_tab)#Usunięcie wydarzenia z którego się zrezygnowało z bazy powiadomień
    else:
        if notifi_tab == None:
            add_To_notifi(current_event)
        event_usertab.event_status=1
        db.session.commit()

        #Dodawanie do powiadomień
def add_To_notifi(current_event):
    notifi = Notification(notification_event = current_event.event_id, notification_user = session['user_id'] )   # Add notification for each user that is interested in event conectedd to this news
    db.session.add(notifi) 
    try:
        db.session.commit() # end 
    except:
        print("Nie udało się dodać rekordu")

        #Usuwanie z powiadomień
def Del_notifi(current_event):
    Notification.query.filter_by(notification_event=current_event.notification_event, notification_user = session['user_id']).delete()
    try:
        db.session.commit() # end 
    except:
        print("Nie udało się usunąć rekordu")


def addpoints(event_usertab, current_event):
    if event_usertab:
        if event_usertab.event_status==2 and current_event.event_endtime < datetime.today():
            user=User.query.filter_by(user_id=session['user_id']).first()
            user.user_point = user.user_point + current_event.event_point

def changestatus(event_usertab):
    print(event_usertab)
    if event_usertab:
        if event_usertab.event_status==1:
            event_usertab.event_status=2
            db.session.commit()


@app.route('/communicator', methods=['GET', 'POST'])
def communicator():
    """Renders the about page."""
    if request.method == 'POST':
        message_recipient_email = request.form['message_recipient']
        message_title = request.form['message_title']
        message_text = request.form['message_text']
        
        usertab = User.query.all()
        
        if re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", message_recipient_email):
            for u in usertab:
                if u.user_email == message_recipient_email:  
                    message = Message(message_sender =session ['user_id'], message_recipient = u.user_id, message_title = message_title, message_text = message_text )
                    db.session.add(message)
                    db.session.commit()
            return render_template(
                'message.html',
                title='Home Page',
                message='Message sent',
                year=datetime.now().year
            )
        else:
            return render_template(
                'message.html',
                title='Home Page',
                message='Invalid data',
                year=datetime.now().year
            )

    return render_template(
        'communicator.html',
        title='Message',
        year=datetime.now().year
        
    ) 
@app.route('/inbox')
def inbox():
    return render_template(
        'inbox.html',
        title='Wiadomosci',
        messagetab = db.session.query(Message,User).join(Message, Message.message_sender == User.user_id).add_columns (User.user_email, Message.message_title, Message.message_text).filter(Message.message_recipient == session['user_id']).all(),
    )  
 
@app.route('/raport/<path:event>')
def raport(event):
    current_event= Event.query.filter_by(event_id=event).first()
    formtab = db.session.query(Form,Event).join(Form, Form.event_id == Event.event_id).add_columns(Event.event_id, Form.user_id, Event.event_org, Form.Int_val_1, Form.Int_val_2, Form.Int_val_3, Form.Int_val_4, Form.Int_val_5, Form.Str_val_1).filter(Event.event_id==current_event.event_id, Event.event_org== session['user_id']).all()
    iloscankiet=0
    ocena= [0,0,0,0,0]
    miejsce= [0,0]
    kolejnaedycja= [0,0]
    czas=[0,0]
    bezpieczenstwo= [0,0]
    uwagi=[]
    for form in formtab:
        iloscankiet += 1
        if form.Int_val_1 == 1:
            ocena[0] += 1
        elif form.Int_val_1 == 2:
            ocena[1] += 1
        elif form.Int_val_1 == 3:
            ocena[2] += 1
        elif form.Int_val_1 == 4:
            ocena[3] += 1
        elif form.Int_val_1 == 5:
            ocena[4] += 1
        
        if form.Int_val_2 == 1:
            miejsce[0] += 1
        elif form.Int_val_2 == 2:
            miejsce[1] += 1

        if form.Int_val_3 == 1:
            kolejnaedycja[0] += 1
        elif form.Int_val_3 == 2:
            kolejnaedycja[1] += 1

        if form.Int_val_4 == 1:
            czas[0] += 1
        elif form.Int_val_4 == 2:
            czas[1] += 1

        if form.Int_val_5 == 1:
            bezpieczenstwo[0] += 1
        elif form.Int_val_5 == 2:
            bezpieczenstwo[1] += 1

        if form.Str_val_1 != "":
            uwagi.append(form.Str_val_1)

    return render_template(
        'raport.html',
        title='raport',
        year=datetime.now().year,
        iloscankiet = iloscankiet,
        current_event = current_event,
        ocena= ocena,
        miejsce= miejsce,
        kolejnaedycja= kolejnaedycja,
        czas=czas,
        bezpieczenstwo= bezpieczenstwo,
        uwagi = uwagi
        ) 