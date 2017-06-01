from .server_connection.connect import connect_to_sql


@connect_to_sql
def get_usernames(cursor, question_id=None):
    if question_id is None:
        cursor.execute("""SELECT user_mates_name FROM user_mates""")
        return cursor.fetchall()
    else:
        cursor.execute("""
                       SELECT user_mates_id
                       FROM question
                       WHERE id = {0}
                       """.format(question_id))
        user_id = cursor.fetchall()[0][0]
        cursor.execute("""
                       SELECT user_mates_name
                       FROM user_mates
                       WHERE id = {0}
                       """.format(user_id))
        return cursor.fetchall()[0][0]


@connect_to_sql
def get_user_id(cursor, username):
    cursor.execute("""
                   SELECT id FROM user_mates
                   WHERE user_mates_name='{0}'
                   """.format(username))
    return cursor.fetchall()


@connect_to_sql
def get_user_data_of_id(cursor, user_id):
    user_data = {'name': '',
                 'reputation': '',
                 'submission_time': ''}
    cursor.execute("""
                   SELECT user_mates_name, reputation, submission_time
                   FROM user_mates
                   WHERE id={0}
                   """.format(user_id))
    rows = cursor.fetchall()
    user_data['name'] = rows[0][0]
    user_data['reputation'] = rows[0][1]
    user_data['submission_time'] = rows[0][2]
    return user_data


@connect_to_sql
def update_reputation(cursor, table, activity_id, amount_to_change):
    cursor.execute("""
    UPDATE user_mates
    SET reputation = reputation{0}
    FROM {1}
    WHERE {1}.id={2} AND {1}.user_mates_id=user_mates.id
    """.format(amount_to_change, table, activity_id))


@connect_to_sql
def insert_user(cursor, user_values):
    query = """INSERT INTO user_mates(user_mates_name, reputation, submission_time)
               VALUES (%s, %s, %s)
            """
    cursor.execute(query, user_values)


@connect_to_sql
def list_users(cursor):
    data = {'header': [],
            'result_set': []}
    cursor.execute("""SELECT id, user_mates_name AS "User name", submission_time AS "Registration Date"
                    FROM user_mates """)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data['header'] = column_names
    data['result_set'] = rows
    return data
