"""
NAME:          app.py
AUTHOR:        Alan Davies
DATE:          05/02/2019
INSTITUTION:   Interaction Analysis and Modelling Lab (IAM), University of Manchester
DESCRIPTION:   Flask main page.
               http://127.0.0.1:5000/
"""
import os, sys, random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

# set db base directory
basedir = os.path.abspath(os.path.dirname(__file__))
n_images = 4
progress_pc = 39.27

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
# FUNCTION:     beginStudy()
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Setup the study.
#
#---------------------------------------------------------------------------------
@app.route('/begin_study', methods=['POST'])
def beginStudy():
    global progress_pc
    progress_pc += 3.57

    # pick a random starting position
    selected_condition = random.randint(0, 1)

    # setup experimental conditions and load task images & questions
    session['user_data'] = dict()
    session['user_data'].update({ 'condition': selected_condition })
    session['user_data'].update({ 'task_data': None })
    session['user_data'].update({ 'runs': 0 })
    populateQuestions()

    session['user_data']['task_data'] = showNextImageAndTask()
    session.modified = True
    return render_template('display_task.html', task_data = session['user_data']['task_data'],  condition=session['user_data']['condition'], pc=progress_pc)

#---------------------------------------------------------------------------------
# FUNCTION:     populateQuestions()
# INPUT:        void
# OUTPUT:       void
# DESCRIPTION:  Add the images and task questions to session data
#
#---------------------------------------------------------------------------------
def populateQuestions():
    global n_images
    stimuli_images = ','.join('images/graph' + str(i) + '.png' for i in range(n_images))
    stimuli_images = stimuli_images.split(',')
    session['user_data'].update({'stimuli': stimuli_images})
    session['user_data'].update({'tasks': [
        'Which group has the best survival outcome?',
        'At what time point was the most rapid change from baseline seen?',
        'What region(s) are biomarker x most associated with?',
        'Other'
    ]})

#---------------------------------------------------------------------------------
# FUNCTION:     showNextImageAndTask()
# INPUT:        void
# OUTPUT:       Tuple
# DESCRIPTION:  Pop another image form the array
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
# INPUT:
# OUTPUT:
# DESCRIPTION:
#
# ---------------------------------------------------------------------------------
@app.route('/submit_answer', methods=['POST'])
def processAnswers():
    global progress_pc
    progress_pc += 3.57

    # TODO: Store given answers in DB and display post answers questions
    return render_template('post_questions.html', condition=session['user_data']['condition'], task_data=session['user_data']['task_data'], pc=progress_pc)

# ---------------------------------------------------------------------------------
# FUNCTION:     nextQuestion
# INPUT:        void
# OUTPUT:       template
# DESCRIPTION:  Main experimental loop. Keeps shoing new questions until we
#               run out then changes condition. If both conditions done show end page
# ---------------------------------------------------------------------------------
@app.route('/next_question', methods=['POST'])
def nextQuestion():
    global progress_pc
    progress_pc += 3.57
    # TODO: Add progress bar to session then update each time a new question

    remaining_questions = len(session['user_data']['stimuli'])
    if remaining_questions > 0:
        session['user_data']['task_data'] = showNextImageAndTask()
        session.modified = True
        return render_template('display_task.html',  condition=session['user_data']['condition'], task_data=session['user_data']['task_data'], pc=progress_pc)
    else:
        # if we run out of questions
        if session['user_data']['runs'] == 0:
            populateQuestions()
            session['user_data']['runs'] += 1
            session['user_data']['condition'] ^= 1
            session.modified = True
            # TODO: Page explaining will see send [condition] with/without

            #task_data = showNextImageAndTask()
            session['user_data']['task_data'] = showNextImageAndTask()
            session.modified = True
            return render_template('display_task.html', condition=session['user_data']['condition'], task_data=session['user_data']["task_data"], pc=progress_pc)
        else:
            # TODO: Show finished experiment page
            return render_template('final_feedback.html')

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

