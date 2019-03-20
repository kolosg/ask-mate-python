from flask import Flask, render_template, redirect, request, url_for
import data_manager
from util import define_table_headers


app = Flask(__name__)


@app.route('/')
def route_index():
    latest_questions = data_manager.list_latest_questions()
    table_headers = define_table_headers()
    return render_template('index.html', latest_questions=latest_questions, question_headers=table_headers[0])


@app.route('/list')
def route_list():
    all_question = data_manager.list_all_question()
    table_headers = define_table_headers()
    return render_template('list.html', all_question=all_question, question_headers=table_headers[0])


@app.route('/question/<quest_id>')
def route_question(quest_id=None):
    data_manager.increase_view_number(quest_id)
    all_answer = data_manager.list_answers()
    table_headers = define_table_headers()
    questions = data_manager.list_all_question()
    is_answer = data_manager.count_answers(quest_id, data_manager.list_answers())
    is_comment = data_manager.count_answers(quest_id, data_manager.select_comments())
    comments = data_manager.select_comments()
    return render_template('question.html', questions=questions, quest_id=int(quest_id), question_headers=table_headers[0],
                           all_answer= all_answer, answer_headers=table_headers[1], is_answer=is_answer, comments=comments,
                           comment_headers=table_headers[2], is_comment=is_comment)


@app.route('/add-question', methods=['GET', 'POST'])
def route_ask_question(quest_id=None):
    if request.method == 'POST':
        data_manager.ask_new_question(request.form['title'], request.form['message'])
        return redirect('/question/' + str(data_manager.get_latest_id()['id']))


    return render_template('add-question.html', quest_id=quest_id)


@app.route('/question/<quest_id>/edit', methods=['GET', 'POST'])
def route_edit_question(quest_id=None):
    if request.method == 'GET':
        update = True
        questions = data_manager.list_all_question()
    else:
        data_manager.update_question(request.form['title'], request.form['message'], int(quest_id))
        return redirect('/question/' + quest_id)
    return render_template('add-question.html', quest_id=int(quest_id), questions=questions, update=update)


@app.route('/question/<quest_id>/delete', methods=['POST'])
def route_delete_question(quest_id=None):
    data_manager.delete_all_answer_of_question(quest_id)
    data_manager.delete_question(int(quest_id))
    return redirect('/list')


@app.route('/question/<quest_id>/new-answer', methods=["GET", "POST"])
def post_answer(quest_id=None):
    questions = data_manager.list_all_question()
    table_headers = define_table_headers()
    if request.method == "POST":
        data_manager.post_answer(quest_id, request.form["message"])

        return redirect("/question/" + quest_id)

    return render_template("new-answer.html", quest_id=int(quest_id), questions=questions, q_fields=table_headers[0])


@app.route("/answer/<answer_id>/delete", methods=["POST"])
def route_delete_answer(answer_id=None):
    quest_id = data_manager.get_question_id_to_delete(int(answer_id))
    data_manager.delete_answer(int(answer_id))
    return redirect(url_for('route_question', quest_id=quest_id["question_id"]))


@app.route("/question/<quest_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_question(quest_id=None):
    if request.method == 'GET':
        questions = data_manager.list_all_question()
        table_headers = define_table_headers()
        comment = True
    else:
        data_manager.post_comment_to_question(quest_id, request.form['message'])
        return redirect(url_for('route_question', quest_id=int(quest_id)))
    return render_template('add-question.html', quest_id=int(quest_id), comment=comment, questions=questions, q_fields=table_headers[0])


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id=None):
    if request.method == 'GET':
        comments = data_manager.select_comments()
    else:
        quest_id = data_manager.get_question_id(int(comment_id))
        data_manager.update_comment(request.form['message'], int(comment_id))
        return redirect(url_for('route_question', quest_id=quest_id["question_id"]))
    return render_template('edit.html', comment_id=int(comment_id), comments=comments)


@app.route("/comments/<comment_id>/delete", methods=["POST"])
def route_delete_comment(comment_id=None):
    quest_id = data_manager.get_question_id(int(comment_id))
    data_manager.delete_comment(comment_id)
    return redirect(url_for('route_question', quest_id=quest_id["question_id"]))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
