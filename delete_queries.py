from connect import connect_to_sql


@connect_to_sql
def sql_delete_comment(cursor, column_name, column_id):
    cursor.execute(""" DELETE FROM comment WHERE {0} = '{1}'; """.format(column_name, column_id))


@connect_to_sql
def sql_delete_answer(cursor, question_id,):
    cursor.execute(""" DELETE FROM answer WHERE question_id = '{0}'; """.format(question_id))


@connect_to_sql
def sql_delete_question(cursor, question_id):
    cursor.execute(""" DELETE FROM question WHERE id = '{0}'; """.format(question_id))


@connect_to_sql
def sql_delete_question_tag(cursor, question_id):
    cursor.execute(""" DELETE FROM question_tag WHERE question_id = '{0}'; """.format(question_id))
