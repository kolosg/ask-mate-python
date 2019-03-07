from flask import Flask, render_template, redirect, request
from data_manager import sort_data_by_value, convert_unix_time_to_date, add_question, add_answer
from util import define_table_headers, get_latest_question_id


app = Flask(__name__)


@app.route('/')
def route_index():
    return redirect('/list')


@app.route('/list')
def route_list():
    questions_list = sort_data_by_value('submission_time')
    return render_template('list.html', questions_list=questions_list)


@app.route('/question/<quest_id>')
def route_question(quest_id=None):
    questions = convert_unix_time_to_date('question')
    answers = convert_unix_time_to_date('answer')
    table_headers = define_table_headers()
    return render_template('question.html', q_fields=table_headers[0], a_fields=table_headers[1], questions=questions, answers=answers, quest_id=quest_id)


@app.route('/question/<quest_id>/new-answer', methods=["GET", "POST"])
def post_answer(quest_id=None):
    if request.method == "POST":
        add_answer(quest_id, request.form["message"])

        return redirect("/question/" + quest_id)

    return render_template("new-answer.html", quest_id=quest_id)


@app.route('/add-question', methods=['GET', 'POST'])
def route_ask_question(quest_id=None):
    if request.method == 'POST':
        add_question(request.form['title'], request.form['message'])
        return redirect('/question/' + get_latest_question_id())
    return render_template('add-question.html', quest_id=quest_id)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
