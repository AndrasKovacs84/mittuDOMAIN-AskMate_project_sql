from connect import connect_to_sql

# Every query function with connection to the user_mates table


@connect_to_sql
def sql_insert_user(cursor, user_values):
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

