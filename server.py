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
    is_comment = data_manager.count_comments(quest_id)
    comments = data_manager.select_comments()
    count_comments = data_manager.count_answer_comments(quest_id)
    is_answer_comment = data_manager.last_answer_comment(all_answer, count_comments)
    return render_template('question.html', questions=questions, quest_id=int(quest_id), question_headers=table_headers[0],
                           all_answer= all_answer, answer_headers=table_headers[1], is_answer=is_answer, comments=comments,
                           comment_headers=table_headers[2], is_comment=is_comment, count_comments=count_comments, is_answer_comment=is_answer_comment)


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
    return render_template('add-question.html', id=int(quest_id), comment=comment, table=questions, q_fields=table_headers[0])


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
    data_manager.delete_comment(comment_id)
    return redirect(url_for('route_question', quest_id=request.form['question_id']))


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id=None):
    if request.method == 'GET':
        all_answer = data_manager.list_answers()
        table_headers = define_table_headers()
        comment_answer = True
    else:
        quest_id = data_manager.get_question_id_from_answers(answer_id)['question_id']
        data_manager.post_comment_to_answer(quest_id, answer_id, request.form['message'])
        return redirect(url_for('route_question', quest_id=quest_id))
    return render_template('add-question.html', id=int(answer_id), comment_answer=comment_answer, table=all_answer, q_fields=table_headers[1][:-3])


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id=None):
    if request.method == 'GET':
        answer_update = True
        answers = data_manager.list_answers()
    else:
        data_manager.update_answer(request.form['message'], int(answer_id))
        quest_id = str(data_manager.get_question_id_from_answers(answer_id)['question_id'])
        return redirect(url_for('route_question', quest_id=quest_id))
    return render_template('add-question.html', answer_id=int(answer_id), answers=answers, answer_update=answer_update)


@app.route('/search')
def search():
    searchstring = request.args.get('q')

    question_results = data_manager.question_results('%' + searchstring + '%')
    answer_results = data_manager.answer_results('%' + searchstring + '%')

    highlighted_question = data_manager.add_selector_to_search_result(searchstring, question_results)
    highlighted_answer = data_manager.add_selector_to_search_result(searchstring, answer_results)

    table_headers = define_table_headers()
    return render_template('search-results.html', question_results=question_results, answer_results=answer_results,
                           question_headers=table_headers[0], answer_headers=table_headers[1][:-4], searchstring=searchstring,
                           highlighted_question=highlighted_question, highlighted_answer=highlighted_answer)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
