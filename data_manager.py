import connection
from datetime import datetime
import util

QUESTION_FIELDS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_FIELDS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

def sort_data_by_value(value, name):
    list_of_questions = []
    connection.read_data_from_csv('templates/'+ name + '.csv', list_of_questions)
    for j in reversed(range(len(list_of_questions))):
        for k in range(j):
            if list_of_questions[k][value] < list_of_questions[k + 1][value]:
                list_of_questions[k], list_of_questions[k + 1] = list_of_questions[k + 1], list_of_questions[k]
    if name == 'question':
        connection.write_data_to_csv('templates/' + name + '.csv', QUESTION_FIELDS, list_of_questions)
    else:
        connection.write_data_to_csv('templates/' + name + '.csv', ANSWER_FIELDS, list_of_questions)
    return list_of_questions


def convert_unix_time_to_date(name):
    data_list = []
    connection.read_data_from_csv('templates/'+ name +'.csv', data_list)
    for data in data_list:
        data['submission_time'] = int(data['submission_time'])
        data['submission_time'] = datetime.utcfromtimestamp(data['submission_time']).strftime('%Y-%m-%d %H:%M:%S')

    return data_list


def add_question(title_or_question_id, message):
    ID = util.generate_id("templates/question.csv")
    DATE = util.add_submission_time()
    connection.append_data_to_csv('templates/question.csv', QUESTION_FIELDS, ID, DATE, title_or_question_id, message)


def add_answer(title_or_question_id, message):
    ID = util.generate_id("templates/answer.csv")
    DATE = util.add_submission_time()
    connection.append_data_to_csv("templates/answer.csv", ANSWER_FIELDS, ID, DATE, title_or_question_id, message)


def edit_question(title, message, quest_id):
    questions = []
    connection.read_data_from_csv("templates/question.csv", questions)
    DATE = util.add_submission_time()
    for question in questions:
        if quest_id == question['id']:
            question['title'] = title
            question['message'] = message
            question['submission_time'] = DATE
    connection.write_data_to_csv("templates/question.csv", QUESTION_FIELDS, questions)


def delete_question(quest_id):
    question_data = []
    answer_data = []
    connection.read_data_from_csv("templates/question.csv", question_data)
    connection.read_data_from_csv("templates/answer.csv", answer_data)
    for question in question_data:
        if quest_id == question['id']:
            question_data.remove(question)
    for answer in answer_data[::-1]:
        if quest_id == answer['question_id']:
            answer_data.remove(answer)
    connection.write_data_to_csv("templates/question.csv", QUESTION_FIELDS, question_data)
    connection.write_data_to_csv("templates/answer.csv", ANSWER_FIELDS, answer_data)


def delete_answer(answer_id):
    answer_data = []
    connection.read_data_from_csv("templates/answer.csv", answer_data)
    for answer in answer_data:
        if answer_id == answer['id']:
            question_id = answer['question_id']
            answer_data.remove(answer)
    connection.write_data_to_csv("templates/answer.csv", ANSWER_FIELDS, answer_data)
    return question_id


def count_answers(quest_id):
    answer_data = []
    connection.read_data_from_csv("templates/answer.csv", answer_data)
    return any(answer['question_id'] == quest_id for answer in answer_data)


def increase_view_number(quest_id):
    questions = []
    connection.read_data_from_csv("templates/question.csv", questions)
    for question in questions:
        if quest_id == question['id']:
            question['view_number'] = int(question['view_number'])
            question['view_number'] += 1
    connection.write_data_to_csv("templates/question.csv", QUESTION_FIELDS, questions)