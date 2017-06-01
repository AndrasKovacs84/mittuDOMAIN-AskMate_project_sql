from server_connection.connect import connect_to_sql


@connect_to_sql
def delete_comment(cursor, column_name, column_id):
    cursor.execute(""" DELETE FROM comment WHERE {0} = '{1}'; """.format(column_name, column_id))


@connect_to_sql
def insert_comment(cursor, comment, user_id):
    cursor.execute("""
                   INSERT INTO comment ({0}, message, submission_time, user_mates_id)
                   VALUES ({1}, {2}, {3}, {4});
                   """.format(comment['foreign_key'],
                              comment['foreign_key_value'],
                              comment['message'],
                              comment['submission_time'],
                              user_id))
