import connection
import time
import database_connection

def define_table_headers():
    table_headers = [['Submission Time', 'View number', 'Vote number', 'Title', 'Message'],
                     ['Submission Time', 'Vote number', 'Message','Edit', 'Delete', 'Post Comment', 'Existing Comments'],
                     ['Submission Time', 'Message', 'Edit', 'Delete']]

    return table_headers


@database_connection.connection_handler
def generate_id(cursor):
    cursor.execute("""
                    SELECT id FROM question
                    ORDER BY id DESC 
                    LIMIT 1 
                    """)
    id = cursor.fetchall()

    return id


def add_submission_time():
    return int(time.time())


def get_latest_question_id():
    questions = []
    connection.read_data_from_csv("templates/question.csv", questions)

    return questions[-1]["id"]
