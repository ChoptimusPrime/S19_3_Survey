from flask import Flask, request, render_template, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, sample
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

current_survey = satisfaction_survey
questions = satisfaction_survey.questions



@app.route('/')
def show_home():
    title = current_survey.title
    return render_template('home.html', title=title)

@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<index>')
def ask_question(index):
    responses = session['responses']
    if len(responses) == len(questions):
        return redirect('/done')
    if int(index) != len(responses):
        flash("Must complete survey in order")
        return redirect(f'/questions/{len(responses)}')
    this_question = questions[int(index)]
    question = this_question.question
    choices = this_question.choices
    return render_template('question.html', question=question, choices=choices)

@app.route('/submit', methods=['POST'])
def next_route():
    responses = session['responses']
    responses.append(request.form['question-choice'])
    session['responses'] = responses
    return redirect('/questions/' + str(len(responses)))

@app.route('/done')
def done():
    return render_template('done.html')