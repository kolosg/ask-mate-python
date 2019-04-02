import database_connection
from datetime import datetime


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
                    SELECT * FROM answer
                    ORDER BY submission_time DESC; 
    """)
    all_answer = cursor.fetchall()
    return all_answer


def count_answers(quest_id, func):
    table = func
    return any(record['question_id'] == int(quest_id) for record in table)


def count_comments(quest_id):
    table = select_comments()
    return any(record['question_id'] == int(quest_id) for record in table if record['answer_id'] == None)


def count_answer_comments(quest_id):
    bools = []
    answers = list_answers()
    comments = select_comments()
    for answer in answers:
        if answer['question_id'] == int(quest_id):
            bools.append(any(comment['answer_id'] == answer['id'] for comment in comments))

    return bools



def last_answer_comment(dict, list_of_bools):
    for i in range(len(dict)):
        for j in range(len(list_of_bools)):
            if i == j:
                dict[i]['bool'] = list_of_bools[j]

    return dict


@database_connection.connection_handler
def ask_new_question(cursor, title, message):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message)
                    VALUES (%(dt)s, 0, 0, %(add_title)s, %(add_message)s)
                    """, dict(dt=dt, add_title=title, add_message=message))



@database_connection.connection_handler
def update_question(cursor, title, message, quest_id):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s, message = %(message)s
                    WHERE id = %(quest_id)s
                    """, dict(title=title, message=message, quest_id=quest_id))


@database_connection.connection_handler
def delete_question(cursor, quest_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(quest_id)s
                    """, dict(quest_id=quest_id))
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(quest_id)s
                    """, dict(quest_id=quest_id))
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(quest_id)s
                    """, dict(quest_id=quest_id))




@database_connection.connection_handler
def get_latest_id(cursor):
    cursor.execute("""
                    SELECT id FROM question
                    ORDER BY id DESC
                    LIMIT 1 
                    """)
    return cursor.fetchone()


@database_connection.connection_handler
def post_answer(cursor, quest_id, message):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO answer(submission_time, vote_number, question_id, message)
                    VALUES(%(dt)s, 0, %(quest_id)s, %(message)s)
                    """, dict(dt=dt, quest_id=quest_id, message=message))

@database_connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s
                    """, dict(answer_id=answer_id))
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s
                    """, dict(answer_id=answer_id))


@database_connection.connection_handler
def get_question_id_to_delete(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s
                    """, dict(answer_id=answer_id))
    return cursor.fetchone()


@database_connection.connection_handler
def increase_view_number(cursor, quest_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(quest_id)s
                    """, dict(quest_id=quest_id))


@database_connection.connection_handler
def list_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM Question
                    ORDER BY submission_time DESC
                    LIMIT 5
                    """)
    latest_questions = cursor.fetchall()
    return latest_questions


@database_connection.connection_handler
def post_comment_to_question(cursor, quest_id, message):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment(question_id, message, submission_time)
                    VALUES(%(quest_id)s, %(message)s, %(dt)s)
                    """, dict(quest_id=quest_id, message=message, dt=dt))


@database_connection.connection_handler
def select_comments(cursor):
    cursor.execute("""
                    SELECT submission_time, message, question_id, id, answer_id FROM comment
                    ORDER BY submission_time DESC
                    """)
    comments = cursor.fetchall()
    return comments


@database_connection.connection_handler
def get_comment_ids(cursor):
    cursor.execute("""
                    SELECT id FROM comment
                    """)
    ids = cursor.fetchall()
    return str(ids['id'])


@database_connection.connection_handler
def update_comment(cursor, message, comment_id):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s, submission_time = %(dt)s
                    WHERE id = %(comment_id)s
                    """, dict(message=message, comment_id=comment_id, dt=dt))

@database_connection.connection_handler
def get_question_id(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment 
                    WHERE id = %(comment_id)s
                    """, dict(comment_id=comment_id))
    return cursor.fetchone()


@database_connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s
                    """, dict(comment_id=comment_id))


@database_connection.connection_handler
def get_question_id_from_answers(cursor, answer_id):
    cursor.execute("""
                    SELECT answer.id, answer.question_id, comment.answer_id
                    FROM answer
                    INNER JOIN comment ON comment.answer_id = answer_id
                    WHERE answer.id = %(answer_id)s
                    """, dict(answer_id=answer_id))
    return cursor.fetchone()


@database_connection.connection_handler
def post_comment_to_answer(cursor, quest_id, answer_id, message):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO comment(question_id, answer_id, message, submission_time)
                    VALUES(%(quest_id)s, %(answer_id)s, %(message)s, %(dt)s)
                    """, dict(quest_id=int(quest_id), answer_id=answer_id, message=message, dt=dt))

@database_connection.connection_handler
def update_answer(cursor, message, answer_id):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s, submission_time = %(dt)s
                    WHERE id = %(answer_id)s
                    """, dict(message=message, answer_id=answer_id, dt=dt))


@database_connection.connection_handler
def question_results(cursor, search):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE title ILIKE %(search)s OR message ILIKE %(search)s
                    ORDER BY submission_time DESC 
                    """, dict(search=search))
    result = cursor.fetchall()
    return result

@database_connection.connection_handler
def answer_results(cursor, search):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE message ILIKE %(search)s
                    ORDER BY submission_time DESC 
                    """, dict(search=search))
    result = cursor.fetchall()
    return result

def add_selector_to_search_result(search_phrase, dicts):
    for dict in dicts:
        for key, value in dict.items():
            if key == 'message' or key == 'title':
                if search_phrase.lower() in value:
                    dict[key] = dict[key].replace(search_phrase.lower(), '<span id="highlight">' + search_phrase.lower() + '</span>')
                elif search_phrase.upper() in value:
                    dict[key] = dict[key].replace(search_phrase.upper(), '<span id="highlight">' + search_phrase.upper() + '</span>')
                elif search_phrase.capitalize() in value:
                    dict[key] = dict[key].replace(search_phrase.capitalize(), '<span id="highlight">' + search_phrase.capitalize() + '</span>')

    return dicts


@database_connection.connection_handler
def registration_data_to_table(cursor, firstname, lastname, username, password):
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
                    INSERT INTO user_information (first_name, last_name, user_name, password, reg_date)
                     VALUES (%(firstname)s, %(lastname)s, %(username)s, %(password)s, %(regdate)s)
                     """, dict(firstname=firstname, lastname=lastname, username=username, password=password, regdate=dt))


@database_connection.connection_handler
def get_hash_pw(cursor, login_name):
    cursor.execute("""
                    SELECT password FROM user_information
                    WHERE user_name = %(login_name)s
                    """, dict(login_name=login_name))

    return cursor.fetchone()


@database_connection.connection_handler
def check_username_already_exist(cursor, username):
    cursor.execute("""
                    SELECT user_name FROM user_information
                    WHERE user_name = %(username)s
                    """, dict(username=username))

    return cursor.fetchone()
