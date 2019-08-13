"""
NAME:          app.py
AUTHOR:        Dr. Alan Davies (Lecturer Health Data Science)
PROFILE:       https://www.research.manchester.ac.uk/portal/alan.davies-2.html
DATE:          05/02/2019
INSTITUTION:   School of Health Sciences/Interaction Analysis and Modelling Lab (IAM), University of Manchester
DESCRIPTION:   Flask main page. Returns the various views of the website and stores user responses in database
               http://127.0.0.1:5000/
"""
import os, sys, random, re
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe

# set db base directory
basedir = os.path.abspath(os.path.dirname(__file__))
n_images = 4

FLASK_DEBUG = 1
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create and configure app
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webdata.db')
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['DEBUG'] = True

# create db instance
#db = SQLAlchemy(app)

# import database class models
#from models import *

#---------------------------------------------------------------------------------
# FUNCTION:     home()
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Runs the home page template.
#
#---------------------------------------------------------------------------------
@app.route('/')
def home():
    initStudy()
    return render_template('home.html')

#---------------------------------------------------------------------------------
# FUNCTION:     getDemographicData()
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Runs the home page template.
#
#---------------------------------------------------------------------------------
@app.route('/demographic_data', methods=['POST'])
def getDemographicData():
    ## ------------ FOR TESTING ONLY ------------------------------##
    form = request.form
    for key in form.keys():
        for value in form.getlist(key):
            print(key, value, file=sys.stderr)
            if "cond0" in value:
                session['user_data']['condition'] = 0
            elif "cond1" in value:
                session['user_data']['condition'] = 1
            elif "cond2" in value:
                session['user_data']['condition'] = 2

    session.modified = True
    print("Condition:", session['user_data']['condition'], file=sys.stderr)
    ## ------------ FOR TESTING ONLY ------------------------------##
    return render_template('demo_data.html')

#---------------------------------------------------------------------------------
# FUNCTION:     graphLiteracyScale()
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Runs the graph literacy page.
#
#---------------------------------------------------------------------------------
@app.route('/graph_literacy', methods=['POST'])
def graphLiteracyScale():
    return render_template('graph_lit.html')

#---------------------------------------------------------------------------------
# FUNCTION:     initStudy()
# INPUT:        void
# OUTPUT:       void
# DESCRIPTION:  Setup the session data structures for the app.
#
#---------------------------------------------------------------------------------
def initStudy():
    # pick a random condition 0 (no prov), 1 (negative prov) or 2 (neutral prov)
    selected_condition = random.randint(0, 2)

    # setup experimental conditions
    session['user_data'] = dict()
    session['user_data'].update({'condition': selected_condition})
    session['user_data'].update({'task_data': None})
    session['user_data'].update({'prog': [50, 5]})
    session.modified = True

#---------------------------------------------------------------------------------
# FUNCTION:     beginStudy()
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Setup the study. Populate the questions and display the initial
#               task
#---------------------------------------------------------------------------------
@app.route('/begin_study', methods=['POST'])
def beginStudy():
    populateQuestions()
    return nextQuestion()

# ---------------------------------------------------------------------------------
# FUNCTION:     nextQuestion
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Main experimental loop. Keeps showing new questions until we
#               run out then changes condition. If both conditions done show end page
# ---------------------------------------------------------------------------------
@app.route('/next_question', methods=['POST'])
def nextQuestion():
    remaining_questions = len(session['user_data']['stimuli'])
    if remaining_questions > 0:
        session['user_data']['task_data'] = showNextImageAndTask()
        question_id = str(session['user_data']['task_data'][0])
        current_question = re.findall(r'\d+', question_id)
        current_question = int(current_question[0])
        condition = int(session['user_data']['condition'])
        session.modified = True

        return render_template('display_task.html', condition=condition,
                               task_data=session['user_data']['task_data'],
                               prov_meta=zip(session['user_data']['meta_data_titles'][current_question], session['user_data']['meta_data'][current_question]),
                               question=current_question, pc=updateProgress())
    else:
        return render_template('final_feedback.html')

#---------------------------------------------------------------------------------
# FUNCTION:     updateProgress()
# INPUT:        void
# OUTPUT:       float
# DESCRIPTION:  Return updated progress value
#
#---------------------------------------------------------------------------------
def updateProgress():
    session['user_data']['prog'][0] += session['user_data']['prog'][1]
    session.modified = True
    return float(session['user_data']['prog'][0])

#---------------------------------------------------------------------------------
# FUNCTION:     populateQuestions()
# INPUT:        void
# OUTPUT:       void
# DESCRIPTION:  Add the images and task questions to session data along
#               with provenance meta and filters
#---------------------------------------------------------------------------------
def populateQuestions():
    global n_images
    stimuli_images = ','.join('images/graph' + str(i) + '.png' for i in range(n_images))
    stimuli_images = stimuli_images.split(',')
    session['user_data'].update({'stimuli': stimuli_images})
    session['user_data'].update({'tasks': [
        'Is the biomarker associated with survival in this patient population?',
        mark_safe('Is there enough evidence to state that there are differences in the effect of drug A<br /> on overall survival (OS) according to the biomarker status for metastatic cancer "K"?'),
        mark_safe('A child has been diagnosed with disease "A", but the disease subtype is unknown.<br />Which two biomarkers would you chose to make the differential diagnosis?'),
        mark_safe('How many patients in the queried sample (n=80)<br /> have genetic alterations co-occurring in 2 or more of the selected genes?')]})

    # main meta data titles
    session['user_data'].update({'meta_data_titles': [['Patient population:','Data collection period:','Countries:','Median follow-up time (method):','Number of events n(%):','Censored observations n(%):','Median survival time (months):'],
                                                      ['Patient population:','Biomarker type:','Sample characteristics:','Year of publication:','Countries:','Plot Footer:'],
                                                      ['Patient population:','Follow-up period:','Enrolment period:','Number of Patients:','Sample characteristics:','Biomarker type:','Year of publication of results:','Countries:'],
                                                      ['Patient population:','Number of Patients:','Number of Samples:','Sample characteristics:','DNA-matched normal controls available?','Year of publication of results:','Countries:','Note:']]})
    # meta data
    session['user_data'].update({'meta_data': [['Retrospective study on patients diagnosed with clinical stage II/III  cancer "J", aged 18-65.','1996-2004','Germany, UK, Norway','15.1 (all patients)',mark_safe('Biomarker+ 44(55)<br />Biomarker- 54(68)'),mark_safe('Biomarker+ 36(45)<br />Biomarker- 26(33)'),mark_safe('Biomarker+ 24.4<br />Biomarker- 18.1')],
                                               ['Metastatic or locally advanced cancer "K", age 18-65 (all studies)','genetic alteration','Formalin-fixed paraffin-embedded (FFPE) primary tumour tissue (all studies)','2015',mark_safe('UK (S1,S4)<br />USA (S2,S3,S5)<br />Norway (S6)'),'Test for interaction between biomarker status and treatment (full dataset): p-value=0.44'],
                                               ['A prospective cohort study in patients diagnosed with cardiovascular disease "A", aged 20-70.','~1 year','2012-2016','300','Blood sample','Protein','2018','France, USA, Sweden'],
                                               ['Patients diagnosed with cancer "D", aged 20-65.','80','80','Primary tumour samples derived from fresh frozen tissue','Yes','2018','Germany, USA, Denmark','Queried genes are altered in 42 (53%) of queried patients (80) in total']]})

    session.modified = True

#---------------------------------------------------------------------------------
# FUNCTION:     showNextImageAndTask()
# INPUT:        void
# OUTPUT:       Tuple
# DESCRIPTION:  Pop another image/task form the array and return them
#
#---------------------------------------------------------------------------------
def showNextImageAndTask():
    remaining_images = len(session['user_data']['stimuli'])
    rnd_num = random.randint(0, remaining_images - 1)
    if remaining_images > 0:
        stimuli = session['user_data']['stimuli'].pop(rnd_num)
        task = session['user_data']['tasks'].pop(rnd_num)
        session.modified = True
        return stimuli, task
    else:
        return None

# ---------------------------------------------------------------------------------
# FUNCTION:     processAnswers()
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Show the post task questions
#
# ---------------------------------------------------------------------------------
@app.route('/submit_answer', methods=['POST'])
def processAnswers():
    return render_template('post_questions.html', condition=session['user_data']['condition'], task_data=session['user_data']['task_data'], pc=updateProgress())

# ---------------------------------------------------------------------------------
# FUNCTION:     finalComments
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Show the final page
#
# ---------------------------------------------------------------------------------
@app.route('/last_page', methods=['POST'])
def finalComments():
    return render_template('final_questions.html')

# ---------------------------------------------------------------------------------
# FUNCTION:     override_url_for()
# INPUT:        void
# OUTPUT:       dict
# DESCRIPTION:  Needed to append last modified time to the static pages
#               to prevent caching issue
# ---------------------------------------------------------------------------------
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

# ---------------------------------------------------------------------------------
# FUNCTION:     dated_url_for()
# INPUT:        string, kwargs
# OUTPUT:       function
# DESCRIPTION:  Needed for caching issue (see override_url_for)
#
# ---------------------------------------------------------------------------------
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)

        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
            print(file_path, file=sys.stderr)

    return url_for(endpoint, **values)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(debug=True)

