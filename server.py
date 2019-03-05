from flask import Flask, render_template, redirect, request
import csv
from datetime import datetime

app = Flask(__name__)


@app.route('/list')  # Register the 'http://localhost:5000 **/** ' route to this function.
def route_list():
    questions = []
    with open('templates/question.csv', 'r') as q:
        reader = csv.DictReader(q)
        for line in reader:
            questions.append(line)

    for j in reversed(range(len(questions))):
        for k in range(j):
            if questions[k]['submission_time'] < questions[k + 1]['submission_time']:
                questions[k], questions[k + 1] = questions[k + 1], questions[k]

    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id=None):
    questions = []
    fields = ['ID', 'Submission Time', 'View number', 'Vote number', 'Title', 'Message', 'Imgage']
    with open('templates/question.csv', 'r') as q:
        reader = csv.DictReader(q)
        for line in reader:
            questions.append(line)
    for dicts in questions:
        dicts['submission_time'] = int(dicts['submission_time'])
        dicts['submission_time'] = datetime.utcfromtimestamp(dicts['submission_time']).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('question.html', fields=fields, questions=questions, question_id=question_id)




if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )