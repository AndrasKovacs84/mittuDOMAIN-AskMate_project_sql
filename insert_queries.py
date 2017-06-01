from connect import connect_to_sql
import select_queries


@connect_to_sql
def sql_insert_new_question(cursor, question_values):
    cursor.execute("""
                   INSERT INTO question(submission_time, view_number, vote_number, title, message, user_mates_id)
                   VALUES ('{0}', {1}, {2}, '{3}', '{4}', {5});
                   """.format(question_values[0], question_values[1],
                              question_values[2], question_values[3],
                              question_values[4], question_values[6]))
    new_id = select_queries.sql_select_latest_question()
    return new_id[0]


@connect_to_sql
def sql_insert_answer(cursor, init_answer, question_id):
    cursor.execute("""
                   INSERT INTO answer (submission_time, vote_number, question_id, message, user_mates_id)
                   VALUES ('{0}', '{1}', (SELECT id FROM question WHERE id='{2}'),'{3}', {4});
                   """.format(init_answer[0], init_answer[1], question_id, init_answer[2], init_answer[3]))


@connect_to_sql
def sql_insert_comment(cursor, comment, user_id):
    print(comment)
    cursor.execute("""
                   INSERT INTO comment ({0}, message, submission_time, user_mates_id)
                   VALUES ({1}, {2}, {3}, {4});
                   """.format(comment['foreign_key'],
                              comment['foreign_key_value'],
                              comment['message'],
                              comment['submission_time'],
                              user_id))


@connect_to_sql
def sql_update_vote_nr(cursor, table, id, amount):
    cursor.execute("""
                   UPDATE {0}
                   SET vote_number = vote_number{1}
                   WHERE id={2}
                   """.format(table, amount, id))


@connect_to_sql
def sql_update_reputation(cursor, table, activity_id, amount_to_change):
    # INNER JOIN {1} ON user_mates.id={1}.user_mates_id
    cursor.execute("""
    UPDATE user_mates
    SET reputation = reputation{0}
    FROM {1}
    WHERE {1}.id={2} AND {1}.user_mates_id=user_mates.id
    """.format(amount_to_change, table, activity_id))