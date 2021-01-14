'''
Data viz Backend

- See Backend documentation (^ in the code indicates there are additional notes)
at https://bit.ly/SarsCoViz_Docn
- #* - indicates an issue or to-do
- Feedback welcome!
'''

import copy, requests, csv, datetime
from flask import Flask, render_template, url_for, flash, request, redirect #^1
from flask_sqlalchemy import SQLAlchemy # Database ORM ^2
from forms import RegistrationForm, LoginForm


#Shaves down & organizes fetched covid deaths/wk data
#Returns tuple: (deaths/wk, deaths/wk by age, deaths/wk by sex)
def orgze_DBW_AS(ogLst):
    #Each is a list of dicts: (1) deaths/wk by sex, (2) deaths/wk by age,
    #(3) deaths/wk... all along w/ general cause deaths
    DBW_S, DBW_A, DBW = ([] for i in range(3))

    for line in ogLst:
        #Remove irrelevant columns, editing ogLst
        rmLst = ['data_as_of','state','mmwr_week']
        [line.pop(col) for col in rmLst]
        #Construct DBW_S only from rows of all ages in ogLst
        if line['age_group'] == 'All Ages':
            DBW_S.append(copy.deepcopy(line)) #Turn iterable into regular list
        #Construct DBW_S only from rows of all sexes in ogLst
        if line['sex'] == 'All Sex':
            DBW_A.append(copy.deepcopy(line)) #Turn iterable into regular list
        #Construct DBW only from rows of all ages & sexes in ogLst
        if line['sex']=='All Sex' and line['age_group']=='All Ages':
            DBW.append(copy.deepcopy(line)) #Turn iterable into regular list
    #end for line in ogLst:

    #Remove now-meaningless cols from the new lists; add wk #'s
    for i1, ln1 in enumerate(DBW_S):
        del ln1['age_group']
        ln1['wkNum'] = i1+1

    for i2, ln2 in enumerate(DBW_A):
        del ln2['sex']
        ln2['wkNum'] = i2+1

    for i3, ln3 in enumerate(DBW):
        del ln3['age_group']
        del ln3['sex']
        ln3['wkNum'] = i3+1

    return (DBW, DBW_A, DBW_S)
#Converts list to csv file
def listToCsv(lst,csvFilename):
    #Obtain list of lst's keys
    keys = []
    [keys.append(key) for key in lst[0]]
    #newline='' removes spacing b/w commas
    with open(csvFilename, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        #Write keys of csv header line - .writerow convention
        writer.writerow(lst[0])
        #Writes 1 row at a time thru whole list
        for row in lst:
            #Build row of values (not keys)
            csvRow = []
            for key in keys:
                csvRow.append(row[key])
            writer.writerow(csvRow)


#Constructor sends app var to instance of Flask class & tells where to look
#for template/html and static/CSS-Js files
application = Flask(__name__, template_folder='./', static_folder="/")
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #Ensures pages reload
#Secret key: protects against modifying cookies, cross-site requests, forgery
#attacks, etc ****not public - hardcoded
application.config['SECRET_KEY'] = 'dcf825233586379d01d31beb7d7b5306'
#This will create a site.db file, w/ /// indicating relative path
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Disables default nofos


'''
#Creates instance of database. Db structure will be of classes/models
db = SQLAlchemy(application) #^3
#Define classes that inherit from db.Model aka have their own db's ^4
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #20 is max username char limit; cannot be NULL—needs a username
    username = db.Column(db.String(20), unique=True, nullable=False)
    #120 is max email char limit; can't be null either
    email = db.Column(db.String(120), unique=True, nullable=False)
    #propic doesn't need to be unique—users will have same default.jpg propic
    #Can add default propic \
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False) # Pw's will be hashed

    #One (User) to many (Post)s backref relationship
    # lazy gets all related posts rather than selected ones
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self): # Defs how User obj is printed
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #Datetime column type; utcnow fn is passed into default as arg
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #Integer is related user's primary key; posts need author, so not nullable
    """Referencing User db's table/column name w/ user.id, so lowercase as is
    default name for User. Same default name rule for Post class ("post")"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): # Defs how Post obj is printed
        return f"Post('{self.title}', '{self.date_posted}')"
'''


#For showcasing some "posts" on the main page. From a tutorial - may be useful
posts = [
    {
        'author': 'Jack Carson',
        'title': 'Update 1',
        'content': "As of today, the web app has launched. If there's anything\
         I've learned during the process of setting this up—from getting into\
         WebDev, learning Python Flask as well as D3.js, and setting up\
        hosting—it's that tasks take 5 times longer than expected. My next\
         goal is to continue expressing analyzed COVID data with several more\
         API-sourced charts!",
        'date_posted': '21 September 2020 at 17:35EST'
    }
]


'''Routes to particular pages'''
#Homepage
@application.route("/")
@application.route("/home") #another web addr option to same route
def home():
    return render_template("index.html", title='SARSCoViz - Plots')

#About page
@application.route("/about")
def about():
    return render_template("about.html", title='SARSCoViz - About')

#Account registration page
@application.route("/register", methods=['GET', 'POST']) #methods for user
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Shows flash msg w/ success alert  category
        flash(f'Account created for {form.username.data}', 'success')
        #Redirect function goes back to home page
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

#User login page
@application.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#Dummy page for showcasing posts dict. From tutorial
@application.route("/updates", methods=['GET','POST'])
def updates():
    return render_template("updates.html", title='SARSCoViz - Updates', posts=posts)


#Use requests.get() to fetch data in json format from web, and use .json() to return as dict
COVID19DeathsByWeek_AgeSex = requests.get('https://data.cdc.gov/resource/vsak-wrfu.json?$limit=200000').json()
#Might use this API once it's fixed -the data's out of order in many ways
'''COVID19CasesAndDeathsByDay = requests.get('https://data.cdc.gov/resource/9mfq-cb36.json?$limit=200000').json()'''

#* - Implement bad request catch

#Get deaths by wk data from organizer fn
DBW_AS_lists = orgze_DBW_AS(COVID19DeathsByWeek_AgeSex) #(deaths/wk, deaths/wk by age, deaths/wk by sex)
listToCsv(DBW_AS_lists[0],'DBW.csv') #Create csv file from DBW_AS_lists's deaths/wk data


#Remove need to restart server for every change by running in debug mode
"""__name__ is __main__ if script is run w/ Python directly. So if we are
running it directly then debug mode engages"""
if __name__ == '__main__':
    application.run(debug=True)