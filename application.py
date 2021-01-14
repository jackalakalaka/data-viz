'''
Data viz Backend

- See Backend documentation (^ in the code indicates there are additional notes)
at: https://bit.ly/SarsCoViz_Docn
- #* - indicates an issue or to-do
'''

import copy, requests, csv, datetime
from flask import Flask, render_template, url_for, flash, request, redirect #^1
from flask_sqlalchemy import SQLAlchemy # Database ORM ^2
from forms import RegistrationForm, LoginForm


#Main code starts at...

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

'''
#Organizes covid cases & deaths by day data
#Returns tuple: (deaths/d, cases/d)
def orgze_CADBD_St(ogLst):
    #Each is a list of dicts: (1) cases/day, (2) deaths/day,
    #(3) cases/wk, (4) deaths/wk
    CBD, DBD, CBW, DBW = ([] for i in range(4))
    CADBD_St = shave_CADBD_St(ogLst) #Rm unwanted columns      

    dayNum, weekNum = (0 for i in range(1)) #Counters for columns to be appended
    #Iter thru each day starting from 0
    for day in range(0, len(ogLst)/60):
        #Set totals counters to 0 
        casesDay, deathsDay = (0 for i in range(2))
        casesWk, deathsWk = (0 for i in range(2) if day%7==0)
        #Iter thru each state 0-59 for a particular day & add to totals
        for stateNum in range(0,60):
            caseAmt = CADBD_St[day*60 + stateNum]['tot_cases']
            deathAmt = CADBD_St[day*60 + stateNum]['tot_death']
            casesDay += caseAmt
            casesWk += caseAmt
            deathsDay += deathAmt
            deathsWk += deathAmt
        #Append row for day to new list
        rowCBD, rowDBD, rowCBW, rowDBW = ({} for i in range(4))
        #rowCBD['submission_date'] = 
        CBD.append(copy.deepcopy(row))


#Shaves away unwanted columns from fetched covid cases & deaths by day data
def shave_CADBD_St(ogLst):
    #Each is a list of dicts: (1) deaths/d, (2) cases/d
    CADBD_St = []

    for line in ogLst:
        #Remove irrelevant columns, editing ogLst
        rmLst = ['new_case','pnew_case','new_death','pnew_death','created_at',\
            'consent_cases','consent_deaths','conf_cases','prob_cases',\
            'conf_death','prob_death']
        #if col in line - bc for some reason certain cols don't always show up
        [line.pop(col) for col in rmLst if col in line]
        CADBD_St.append(copy.deepcopy(line)) #Turn iterable into regular list
    return CADBD_St

#Compiles state total deaths & cases to total deaths & cases
def CADBD_St_to_CADBD(CADBD_St):
    pass
'''

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


#For showcasing some "posts" on the main page. From a tutorial 
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
'''COVID19CasesAndDeathsByDay = requests.get('https://data.cdc.gov/resource/9mfq-cb36.json?$limit=200000').json()'''

#* - Implement bad request catch

#Get deaths by wk data from organizer fn
DBW_AS_lists = orgze_DBW_AS(COVID19DeathsByWeek_AgeSex) #(deaths/wk, deaths/wk by age, deaths/wk by sex)
listToCsv(DBW_AS_lists[0],'DBW.csv') #Create csv file from DBW_AS_lists's deaths/wk data
'''#Get cases and deaths by day data from organizer function
#orgze_CADBD_St(COVID19CasesAndDeathsByDay)'''


'''
#* - WIP; turning what's below into functions, and the cases and deaths by day/week data is wrong
with open('temp_CADBD.csv', 'r') as read2: #Cases & deaths by day
    #CADBD_reader is an iterable of a list of dicts
    CADBD_reader = csv.DictReader(read2, delimiter=',')

    CADBD = [] #list of dicts: cases & deaths by day
    
    #List of 60 lists of dicts, w/ index for each state's daily case info
    #60 states/regions total
    #Paired w/ CADBD_byState_labels for construction
    CADBD_byState = [[], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], []]
    #State labels dict that corresponds to by-day and by-wk lists
    CADBD_byState_labels = {0:'CO'} #Will grow as CADBD_byState is filled

    #For each line in CADBD indicates state # (as each state appears
    #in top-bottom order in CADBD/temp_CADBD.csv)
    stateCnt = 0
    #Related to stateCnt, indicates label of each state. Starts w/ Colorado
    state = 'CO'
    #Iterate thru each line and fills in CADBD_byState & CADBD_byState_labels
    for line in CADBD:
        #When read state changes, alter state & stateCnt & append new info
        if state != line['state']:
            state = line['state'] #Set state equal to new state label
            stateCnt=stateCnt+1 #Increment stateCnt
            CADBD_byState_labels[stateCnt] = state #Add new state to labels dict
        del line['state'] #Remove line's 'state' key-value pair
        #Append altered line to corresponding nested state list in CADBD_byState
        CADBD_byState[stateCnt].append(line)
    #end for

    print(CADBD_byState_labels)

    print('THIS IS WRONG. Currently working on fixing it -Jack')
    for i in range(0,60):
        print(CADBD_byState_labels[i],'last day cases (>= last week cases):',CADBD_byState[i][-1]['tot_cases'],'and deaths (>= last week deaths)\
        in nested list:',CADBD_byState[i][-1]['tot_death'])
    
    print('CO last day cases (>= last week cases):',CADBD[297]['tot_cases'],'and deaths (>= last week deaths) in og list:',\
        CADBD[297]['tot_death'])

    #Convert CADBD_byState to CADBW_byState
    #List (of 60 lists of dics) w/ an index for each of 60 states's weekly case info
    CADBW_byState = [[], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], [],\
        [], [], [], [], [], [], [], [], [], []]
    #For each state in daily data, change data to weekly
    for state, stateInfo in enumerate(CADBD_byState): #stateInfo is a list
        dayCnt = -1 #Rst day of wk counter for this state, including day 1Feb2020 as 1st wk
        weekCnt = 0 #Rst week counter {0 to n-1} for next state

        for dayInfo in stateInfo: #For each of state's days in CADBD_byState:
            if dayCnt==1: #If iterating on new wk,
                wkDict = {} #append empty dict to state list for this wk
                CADBW_byState[state].append(wkDict)
                #Insert partial data from CADBD_byState
                CADBW_byState[state][weekCnt]['tot_cases'] = int(dayInfo['tot_cases'])
                CADBW_byState[state][weekCnt]['tot_death'] = int(dayInfo['tot_death'])
            elif dayCnt == -1: #Special case to include 1Feb2020 as 1st wk
                wkDict = {} #append empty dict to state list
                CADBW_byState[state].append(wkDict)
                CADBW_byState[state][0]['tot_cases'] = int(dayInfo['tot_cases'])
                CADBW_byState[state][0]['tot_death'] = int(dayInfo['tot_death'])
                dayCnt = 7 #Indicate "week" is fully accounted for
            else:
                #Add partial data from CADBD_byState
                CADBW_byState[state][weekCnt]['tot_cases'] += int(dayInfo['tot_cases'])
                CADBW_byState[state][weekCnt]['tot_death'] += int(dayInfo['tot_death'])

            #Increment counters, and insert weekCntNum col entry into each wk's data row
            if dayCnt!=7:
                dayCnt += 1
            else:
                CADBW_byState[state][weekCnt]['weekNum'] = weekCnt + 1
                dayCnt = 1
                weekCnt +=1
            #end for dayInfo in CADBD_byState:

        #Chk that final row is a full week. If not, discard
        if dayCnt!=1: #If dayCnt was not just-previously 7:
            CADBW_byState[state].pop(weekCnt)

    for stateData, stateLabel in zip(CADBW_byState, CADBD_byState_labels):
        print(stateLabel)
        for wkData in stateData:
            print(wkData)
        print('\n')
    for i in range(0,60):
        print(CADBD_byState_labels[i],'last week cases:',CADBW_byState[i][-1]['tot_cases'],'and deaths:',CADBW_byState[i][-1]['tot_death'])
    #Convert CADBW_byState to CADBW
    CADBW = []
    numWeeks = CADBW_byState[0][-1]['weekNum']
    for weekNum in range(0,numWeeks): #For each week, sum states' data
        print('\n\n')
        for stateIndex in range(0,60): #Iterate thru each state and add its data to total
            if stateIndex==0: #If iterating at new week, append fields & 1st state's data to CADBW
                CADBW.append(CADBW_byState[0][weekNum])
                #Cast str's as int
                CADBW[weekNum]['tot_cases'] = int(CADBW[weekNum]['tot_cases'])
                CADBW[weekNum]['tot_death'] = int(CADBW[weekNum]['tot_death'])
                print(int(CADBW[weekNum]['tot_cases']))
            else: #Add particular state's data to totally for weekNum'th week
                CADBW[weekNum]['tot_cases'] += int(CADBW_byState[stateIndex][weekNum]['tot_cases'])
                CADBW[weekNum]['tot_death'] += int(CADBW_byState[stateIndex][weekNum]['tot_death'])
                print(int(CADBW_byState[stateIndex][weekNum]['tot_cases']))
    for elem in CADBW:
        print(elem)
# end with open('temp_CADBD.csv', 'r')

#Create cases and deaths by day .csv to be called by js
with open('CADBD.csv', 'w', newline='') as write4: # newline='' removes spacing b/w commas
    writer = csv.writer(write4)

    #Write keys of csv header line - .writerow convention
    writer.writerow(CADBW_byState[0])

    #Writes 1 row at a time thru whole list
    for row in CADBW_byState:
        csvRow = [row['submission_date'], row['tot_cases'],\
            row['tot_death'], row['weekNum']]
        writer.writerow(csvRow)
# end with open('DBW_A.csv', 'w', newline='')
'''


#Remove need to restart server for every change by running in debug mode
"""__name__ is __main__ if script is run w/ Python directly. So if we are
running it directly then debug mode engages"""
if __name__ == '__main__':
    application.run(debug=True)