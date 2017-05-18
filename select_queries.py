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
                   id AS "Id",
                   submission_time AS "Submission time",
                   view_number AS "View number",
                   vote_number AS "Vote number",
                   title AS "Title",
                   message AS "Message",
                   image AS "Image"
                   FROM question
                   ORDER BY {0};
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
                   id AS "Id",
                   submission_time AS "Submission time",
                   vote_number AS "Vote number",
                   message AS "Message",
                   image AS "Image"
                   FROM answer
                   WHERE question_id={0}
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
                   id AS "Id",
                   message AS "Message",
                   submission_time AS "Submission time"
                   FROM comment
                   WHERE answer_id = {0}
                   """.format(answer_id))
    comments = cursor.fetchall()
    return comments


@connect_to_sql
def sql_update_question_details(cursor, new_question_details):
    cursor.execute("""
                   UPDATE question
                   SET title = {0}, message = {1}
                   WHERE id = {2}
                   """.format(new_question_details['title'], new_question_details['message'], new_question_details['id']))


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
                   id AS "Id",
                   message AS "Message",
                   submission_time AS "Submission time"
                   FROM comment
                   WHERE question_id = {0}
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
