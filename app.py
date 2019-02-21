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

    selected_condition = random.randint(0, 1)

    stimuli_images = ','.join('images/graph' + str(i) + '.png' for i in range(11))
    stimuli_images = stimuli_images.split(',')

    session['user_data'] = dict()
    session['user_data'].update({ 'condition': selected_condition })
    session['user_data'].update({ 'stimuli': stimuli_images })
    session['user_data'].update({'tasks': [
        'What was the smallest percentage change from baseline for (biomarker x)?',
        'Which group has the best survival outcome?',
        'Which patient displayed the fastest complete response in stage x?',
        'At what time point was the most rapid change from baseline seen?',
        'Based on the presented studies about the use of biomarker x for x. is the overall summary favoring the treatment or the control?',
        'Does the plot suggest that a publication bias exists?',
        'Which group has the largest range of data?',
        'Which gene exhibits the largest number/proportion of deletions?',
        'What region(s) are biomarker x most associated with?',
        'Which biomarker has the strongest connection to treatment/test x?',
        'Which genes exhibit truncating mutations?'
    ] })
    session['user_data'].update({'runs': 0 })

    return render_template('display_task.html', task_data = showNextImageAndTask(), data = session['user_data'])

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
        return session['user_data']['stimuli'].pop(rnd_num), session['user_data']['tasks'].pop(rnd_num)
    else:
        return None

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

