from connect import connect_to_sql


@connect_to_sql
def sql_get_question_text(cursor, question_id):
    cursor.execute("""
                   SELECT title, message FROM question WHERE id = '{0}';
                   """.format(question_id)
                   )
    return cursor.fetchall()[0]


@connect_to_sql
def sql_list_questions(cursor, sort='submission_time DESC'):
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
def sql_update_question_view_count(cursor, question_id):
    cursor.execute("""
                   UPDATE question
                   SET view_number = view_number + 1
                   WHERE id={0}
                   """.format(question_id))


@connect_to_sql
def sql_question_details(cursor, question_id):
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
def sql_answers_to_question(cursor, question_id):
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
def sql_gather_comments_for_answer(cursor, answer_id):
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
def sql_update_question_details(cursor, new_question_details):
    cursor.execute("""
                   UPDATE question
                   SET title = {0}, message = {1}
                   WHERE id = {2}
                   """.format(new_question_details['title'],
                              new_question_details['message'],
                              new_question_details['id']))


@connect_to_sql
def sql_select_latest_question(cursor):
    cursor.execute("""
                   SELECT max(id)
                   FROM question
                   """)
    row = cursor.fetchall()
    return row[0]


@connect_to_sql
def sql_gather_question_comments(cursor, question_id):
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
def sql_answer_details(cursor, answer_id):
    cursor.execute("""
                   SELECT
                   id AS "Id",
                   submission_time AS "Submission time",
                   vote_number AS "Vote number",
                   question_id AS "Question id",
                   message AS "Message",
                   image AS "Image"
                   FROM answer
                   WHERE id={0}
                   """.format(answer_id))
    result = cursor.fetchall()
    answer = {'id': result[0][0],
              'submission_time': result[0][1],
              'vote_number': result[0][2],
              'question_id': result[0][3],
              'message': result[0][4],
              'image': result[0][5]}
    return answer


@connect_to_sql
def sql_get_latest_question(cursor):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   SELECT id AS "Id",
                   submission_time AS "Submission time",
                   view_number AS "View number",
                   vote_number AS "Vote number",
                   title AS "Title",
                   message AS "Message",
                   image AS "Image"
                   FROM question
                   ORDER BY submission_time DESC
                   LIMIT 5
                   """)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    data['result_set'] = rows
    return data


@connect_to_sql
def sql_get_usernames(cursor, id=None):
    if id is None:
        cursor.execute("""SELECT user_mates_name FROM user_mates""")
        return cursor.fetchall()
    else:
        cursor.execute("""SELECT user_mates_name FROM user_mates
                       WHERE id={0}""".format(id))
        return cursor.fetchall()


@connect_to_sql
def sql_get_user_id(cursor, username):
    cursor.execute("""
                   SELECT id FROM user_mates
                   WHERE user_mates_name='{0}'
                   """.format(username))
    return cursor.fetchall()
