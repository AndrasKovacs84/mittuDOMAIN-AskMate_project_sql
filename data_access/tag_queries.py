from .server_connection.connect import connect_to_sql


@connect_to_sql
def delete_question_tag(cursor, question_id):
    cursor.execute(""" DELETE FROM question_tag WHERE question_id = '{0}'; """.format(question_id))
