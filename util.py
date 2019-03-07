import connection
import time

def define_table_headers():
    table_headers= [['Submission Time', 'View number', 'Vote number', 'Title', 'Message', 'Image'],
                    ['Submission Time', 'Vote number', 'Message']]

    return table_headers

def generate_id(filename):
    q_list = []
    connection.read_data_from_csv(filename, q_list)

    return int(q_list[-1]['id']) + 1


def add_submission_time():
    return int(time.time())


def get_latest_question_id():
    questions = []
    connection.read_data_from_csv("templates/question.csv", questions)

    return questions[-1]["id"]