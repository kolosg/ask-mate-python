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
    connection.read_data_from_csv('templates/'+name+'.csv', data_list)
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


