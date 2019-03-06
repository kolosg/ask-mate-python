import connection
from datetime import datetime


def sort_data_by_value(value):
    list_of_questions = []
    connection.read_data_from_csv('templates/question.csv', list_of_questions)
    for j in reversed(range(len(list_of_questions))):
        for k in range(j):
            if list_of_questions[k][value] < list_of_questions[k + 1][value]:
                list_of_questions[k], list_of_questions[k + 1] = list_of_questions[k + 1], list_of_questions[k]

    return list_of_questions


def convert_unix_time_to_date(name):
    data_list = []
    connection.read_data_from_csv('templates/'+name+'.csv', data_list)
    for data in data_list:
        data['submission_time'] = int(data['submission_time'])
        data['submission_time'] = datetime.utcfromtimestamp(data['submission_time']).strftime('%Y-%m-%d %H:%M:%S')

    return data_list
