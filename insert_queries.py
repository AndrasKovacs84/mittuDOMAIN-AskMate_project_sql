from connect import connect_to_sql
import select_queries


@connect_to_sql
def sql_insert_new_question(cursor, question_values):
    cursor.execute("""
                   INSERT INTO question(submission_time, view_number, vote_number, title, message)
                   VALUES ('{0}', {1}, {2}, '{3}', '{4}')
                   """.format(question_values[0], question_values[1],
                              question_values[2], question_values[3], question_values[4]))
    new_id = select_queries.sql_select_latest_question()
    return new_id[0]


@connect_to_sql
def sql_insert_answer(cursor, init_answer, question_id):
    cursor.execute("""
                   INSERT INTO answer (submission_time, vote_number, question_id, message)
                   VALUES ('{0}', '{1}', (SELECT id FROM question WHERE id='{2}'),'{3}');
                   """.format(init_answer[0], init_answer[1], question_id, init_answer[2]))


@connect_to_sql
def sql_insert_comment(cursor, comment):
    cursor.execute("""
                   INSERT INTO comment ({0}, message, submission_time)
                   VALUES ({1}, {2}, {3});
                   """.format(comment['foreign_key'], 
                              comment['foreign_key_value'], 
                              comment['message'], 
                              comment['submission_time']))


@connect_to_sql
def sql_update_vote_nr(cursor, table, id, amount):
    cursor.execute("""
                   UPDATE {0}
                   SET vote_number = vote_number{1}
                   WHERE id={2}
                   """.format(table, amount, id))