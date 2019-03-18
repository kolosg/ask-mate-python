from flask import Flask, render_template, redirect, request
import data_manager
from util import define_table_headers, get_latest_question_id

app = Flask(__name__)


@app.route('/')
def route_index():
    return redirect('/list')


@app.route('/list')
def route_list():
    all_question = data_manager.list_all_question()
    return render_template('list.html', all_question=all_question)


@app.route('/question/<quest_id>')
def route_question(quest_id=None):
    all_answer = data_manager.list_answers()
    table_headers = define_table_headers()
    questions = data_manager.list_all_question()
    is_answer = data_manager.count_answers(quest_id)
    return render_template('question.html', questions=questions, quest_id=int(quest_id), question_headers=table_headers[0], all_answer= all_answer, answer_headers=table_headers[1], is_answer=is_answer)


'''
@app.route('/question/<quest_id>')
def route_question(quest_id=None):
    data_manager.increase_view_number(quest_id)
    questions = data_manager.convert_unix_time_to_date('question')
    data_manager.sort_data_by_value('submission_time', 'answer')
    answers = data_manager.convert_unix_time_to_date('answer')
    table_headers = define_table_headers()
    any_answer = data_manager.count_answers(quest_id)
    return render_template('question.html', q_fields=table_headers[0], a_fields=table_headers[1],
                           questions=questions, answers=answers, quest_id=quest_id, any_answer=any_answer)


@app.route('/question/<quest_id>/new-answer', methods=["GET", "POST"])
def post_answer(quest_id=None):
    questions = data_manager.convert_unix_time_to_date('question')
    table_headers = define_table_headers()
    if request.method == "POST":
        data_manager.add_answer(quest_id, request.form["message"])

        return redirect("/question/" + quest_id)

    return render_template("new-answer.html", quest_id=quest_id, questions=questions, q_fields=table_headers[0])


@app.route('/add-question', methods=['GET', 'POST'])
def route_ask_question(quest_id=None):
    if request.method == 'POST':
        data_manager.add_question(request.form['title'], request.form['message'])
        return redirect('/question/' + get_latest_question_id())
    return render_template('add-question.html', quest_id=quest_id)


@app.route('/question/<quest_id>/edit', methods=['GET', 'POST'])
def route_edit_question(quest_id=None):
    if request.method == 'GET':
        update = True
        questions_list = data_manager.sort_data_by_value('submission_time', 'question')
    else:
        data_manager.edit_question(request.form['title'], request.form['message'], quest_id)
        return redirect('/question/' + quest_id)
    return render_template('add-question.html', quest_id=quest_id, questions_list=questions_list, update=update)


@app.route('/question/<quest_id>/delete', methods=['POST'])
def route_delete_question(quest_id=None):
    data_manager.delete_question(quest_id)
    return redirect('/list')


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def route_delete_answer(answer_id=None):
    question_id = data_manager.delete_answer(answer_id)
    return redirect('question/' + question_id)'''


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
