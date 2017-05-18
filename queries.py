import psycopg2
from connect import connect_to_sql


@connect_to_sql
def sql_select(cursor, query):
    '''Displays the query chosen by the user. Parameter is a dictionary of the relevant properties
    for a simple query. Returns the results of the query. data[0] = list of column names as header,
    data[1] = list of lists, where each nested list represents a row of data.'''
    data = {'header': [],
            'result_set': []}
    if query['filter'] is None:
        cursor.execute("""
                       SELECT {0}
                       FROM {1}
                       ORDER BY {2};
                       """.format(query['columns'], query['table'], query['order_by']))
    else:
        cursor.execute("""
                       SELECT DISTINCT {1}
                       FROM {0}
                       WHERE {2}
                       ORDER BY {3};
                       """.format(query['table'], query['columns'], query['filter'], query['order_by']))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data['header'] = column_names
    data['result_set'] = rows
    return data


@connect_to_sql
def sql_insert(cursor, data_to_insert):
    '''Inserts data into table. data_to_insert = {'table': 'tablename', 'columns': [list of columns],
    'values': [list_of_values]}. Function returns nothing.'''
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   INSERT INTO {0}({1})
                   VALUES ({2});
                   """.format(data_to_insert['table'], ', '.join(data_to_insert['columns']),
                   ', '.join(data_to_insert['values'])))


@connect_to_sql
def sql_update(cursor, data_to_update):
    '''Updates existing record in the database. data_to_update = {'column':[list of column names],
    'values':[list of values for each column] Returns nothing'''
    update_values = []
    for i in range(len(data_to_update['column'])):
        update_values.append(str(data_to_update['column'][i]) + '=' + str(data_to_update['values'][i]))

    cursor.execute(""" UPDATE {1}
                     SET {2}
                     WHERE {3}; 
                     """.format(data_to_update['table'], ', '.join(update_values), data_to_update['filter']))


@connect_to_sql
def sql_delete(cursor, data_to_delete):
    cursor.execute(""" DELETE FROM {1}
                    WHERE {2};
                """.format(data_to_delete['table'], data_to_delete['filter']))


@connect_to_sql
def sql_empty_qry(cursor, query):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""{0}""".format(query))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    data['result_set'] = rows
    return data


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
    question = {'submission_time': result[0][0],
                'view_number': result[0][1],
                'vote_number': result[0][2],
                'title': result[0][3],
                'message': result[0][4],
                'image': result[0][5]}
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
    print("comments:", comments)
    return comments


@connect_to_sql
def sql_update_question_details(cursor, new_question_details):
    cursor.execute("""
                   UPDATE question)
                   SET title = {0}, message = {1}
                   WHERE id = {2}
                   """.format(new_question_details['title'], new_question_details['message'], new_question_details['id']))


@connect_to_sql
def sql_insert_new_question(cursor, question_values):
    cursor.execute("""
                   INSERT INTO question(submission_time, view_number, vote_number, title, message)
                   VALUES ('{0}', {1}, {2}, '{3}', '{4}')
                   """.format(question_values[0], question_values[1],
                              question_values[2], question_values[3], question_values[4]))
    new_id = sql_select_latest_question()
    return new_id[0]


@connect_to_sql
def sql_select_latest_question(cursor):
    cursor.execute("""
                   SELECT max(id) 
                   FROM question
                   """)
    row = cursor.fetchall()
    return row[0]

def sql_insert_answer(cursor, init_answer, question_id):
    cursor.execute("""
                   INSERT INTO answer (submission_time, vote_number, question_id, message)
                   VALUES ('{0}', '{1}', (SELECT id FROM question WHERE id='{2}'),'{3}');
                   """.format(init_answer[0], init_answer[1], question_id, init_answer[2]))


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


