from .server_connection.connect import connect_to_sql


@connect_to_sql
def get_question_text(cursor, question_id):
    cursor.execute("""
                   SELECT title, message FROM question WHERE id = '{0}';
                   """.format(question_id))
    return cursor.fetchall()[0]


@connect_to_sql
def update_question_view_count(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = view_number + 1
                   WHERE id={0}
                   """.format(question_id))


@connect_to_sql
def question_details(cursor, question_id):
    cursor.execute("""
                   SELECT
                   id AS "Id",
                   submission_time AS "Submission time",
                   view_number AS "View number",
                   vote_number AS "Vote number",
                   title AS "Title",
                   message AS "Message",
                   image AS "Image"
                   FROM question
                   WHERE id={0}
                   """.format(question_id))
    result = cursor.fetchall()
    question = {'id': result[0][0],
                'submission_time': result[0][1],
                'view_number': result[0][2],
                'vote_number': result[0][3],
                'title': result[0][4],
                'message': result[0][5],
                'image': result[0][6]}
    return question


@connect_to_sql
def update_question_details(cursor, new_question_details):
    cursor.execute("""
                   UPDATE question
                   SET title = {0}, message = {1}
                   WHERE id = {2}
                   """.format(new_question_details['title'],
                              new_question_details['message'],
                              new_question_details['id']))


@connect_to_sql
def select_latest_question(cursor):
    cursor.execute("""
                   SELECT max(id)
                   FROM question
                   """)
    row = cursor.fetchall()
    return row[0]


@connect_to_sql
def delete_question(cursor, question_id):
    cursor.execute(""" DELETE FROM question WHERE id = '{0}'; """.format(question_id))


@connect_to_sql
def insert_new_question(cursor, question_values):
    cursor.execute("""
                   INSERT INTO question(submission_time, view_number, vote_number, title, message, user_mates_id)
                   VALUES ('{0}', {1}, {2}, '{3}', '{4}', {5});
                   """.format(question_values[0], question_values[1],
                              question_values[2], question_values[3],
                              question_values[4], question_values[6]))
    new_id = select_latest_question()
    return new_id[0]
