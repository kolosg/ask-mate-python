import database_connection
import util

@database_connection.connection_handler
def list_all_question(cursor):
    cursor.execute("""
                    SELECT * FROM Question
                    ORDER BY submission_time DESC;
                    """)
    all_question = cursor.fetchall()
    return all_question

@database_connection.connection_handler
def list_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer; 
    """)
    all_answer = cursor.fetchall()
    return all_answer


def count_answers(quest_id):
    any_answer = list_answers()
    return any(answer['question_id'] == int(quest_id) for answer in any_answer)


@database_connection.connection_handler
def ask_new_question(cursor, title, message):
    cursor.execute("""
                    INSERT INTO question (title, message)
                    VALUES (%(add_title)s, %(add_message)s)
                    """,
                   dict(add_title=title, add_message=message))
