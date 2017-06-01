from server_connection.connect import connect_to_sql


@connect_to_sql
def list_questions(cursor, sort='submission_time DESC'):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   SELECT
                   question.id AS "Id",
                   user_mates.user_mates_name AS "Author",
                   question.submission_time AS "Submission time",
                   question.view_number AS "View number",
                   question.vote_number AS "Vote number",
                   question.title AS "Title",
                   question.message AS "Message",
                   question.image AS "Image"
                   FROM question
                   INNER JOIN user_mates
                   ON question.user_mates_id = user_mates.id
                   ORDER BY question.{0};
                   """.format(sort))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    data['result_set'] = rows
    return data


@connect_to_sql
def answers_to_question(cursor, question_id):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   SELECT
                   answer.id AS "Id",
                   user_mates.user_mates_name AS "Author",
                   answer.submission_time AS "Submission time",
                   answer.vote_number AS "Vote number",
                   answer.message AS "Message",
                   answer.image AS "Image"
                   FROM answer
                   INNER JOIN user_mates
                   ON answer.user_mates_id = user_mates.id
                   WHERE answer.question_id = {0}
                   ORDER BY answer.submission_time
                   """.format(question_id))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    for answer in rows:
        comments = sql_gather_comments_for_answer(answer[0])
        data['result_set'].append({'answer': answer, 'comments': comments})
    return data


@connect_to_sql
def gather_comments_for_answer(cursor, answer_id):
    cursor.execute("""
                   SELECT
                   comment.id AS "Id",
                   user_mates.user_mates_name AS "Author",
                   comment.message AS "Message",
                   comment.submission_time AS "Submission time"
                   FROM comment
                   INNER JOIN user_mates
                   ON comment.user_mates_id = user_mates.id
                   WHERE answer_id = {0}
                   ORDER BY comment.submission_time
                   """.format(answer_id))
    comments = cursor.fetchall()
    return comments


@connect_to_sql
def gather_question_comments(cursor, question_id):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   SELECT
                   comment.id AS "Id",
                   user_mates.user_mates_name AS "Author",
                   comment.message AS "Message",
                   comment.submission_time AS "Submission time"
                   FROM comment
                   INNER JOIN user_mates
                   ON comment.user_mates_id = user_mates.id
                   WHERE question_id = {0}
                   ORDER BY comment.submission_time
                   """.format(question_id))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    data['result_set'] = rows
    return data


@connect_to_sql
def get_latest_question(cursor):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   SELECT question.id AS "Id",
                   user_mates.user_mates_name AS "Author",
                   question.submission_time AS "Submission time",
                   question.view_number AS "View number",
                   question.vote_number AS "Vote number",
                   question.title AS "Title",
                   question.message AS "Message",
                   question.image AS "Image"
                   FROM question
                   INNER JOIN user_mates
                   ON question.user_mates_id = user_mates.id
                   ORDER BY question.submission_time DESC
                   LIMIT 5
                   """)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    data['result_set'] = rows
    return data


@connect_to_sql
def get_user_activities_of_id(cursor, user_id):
    """Compiles all activity belonging to user of given user_id."""
    user_activities = {'questions': [],
                       'answers': [],
                       'comments': []}
    cursor.execute("""
                   SELECT id, title, message
                   FROM question
                   WHERE user_mates_id={0}
                   """.format(user_id))
    rows = cursor.fetchall()
    for row in rows:
        user_activities['questions'].append({'id': row[0],
                                             'title': row[1],
                                             'message': row[2]})
    cursor.execute("""
                   SELECT question_id, message
                   FROM answer
                   WHERE user_mates_id={0}
                   """.format(user_id))
    rows = cursor.fetchall()
    for row in rows:
        user_activities['answers'].append({'question_id': row[0],
                                           'message': row[1]})
    cursor.execute("""
                   SELECT question_id, answer_id, message
                   FROM comment
                   WHERE user_mates_id={0}
                   """.format(user_id))
    rows = cursor.fetchall()
    for row in rows:
        user_activities['comments'].append({'question_id': row[0],
                                            'answer_id': row[1],
                                            'message': row[2]})
    return user_activities


@connect_to_sql
def update_vote_nr(cursor, table, id, amount):
    cursor.execute("""
                   UPDATE {0}
                   SET vote_number = vote_number{1}
                   WHERE id={2}
                   """.format(table, amount, id))
