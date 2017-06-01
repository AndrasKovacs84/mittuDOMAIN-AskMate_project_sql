from .server_connection.connect import connect_to_sql


@connect_to_sql
def get_question_text(cursor, question_id):
    query = """SELECT title, message FROM question WHERE id = %s;"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()[0]


@connect_to_sql
def update_question_view_count(cursor, question_id):
    statement = """
                UPDATE question
                SET view_number = view_number + 1
                WHERE id=%s;
                """
    cursor.execute(statement, (question_id,))


@connect_to_sql
def question_details(cursor, question_id):
    query = """
            SELECT
            id,
            submission_time,
            view_number,
            vote_number,
            title,
            message,
            image
            FROM question
            WHERE id=%s
            """
    cursor.execute(query, (question_id,))
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
    statement = """
                UPDATE question
                SET title = %s, message = %s
                WHERE id = %s;
                """
    print(new_question_details)
    cursor.execute(statement, (new_question_details['title'],
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
    statement = """DELETE FROM question WHERE id = %s"""
    cursor.execute(statement, (question_id,))


@connect_to_sql
def insert_new_question(cursor, question_values):
    statement = """
                INSERT INTO question(submission_time, view_number, vote_number, title, message, user_mates_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """
    cursor.execute(statement, (question_values[0], question_values[1],
                               question_values[2], question_values[3],
                               question_values[4], question_values[6]))
    new_id = select_latest_question()
    return new_id[0]
