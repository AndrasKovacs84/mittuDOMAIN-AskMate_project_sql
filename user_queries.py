from connect import connect_to_sql

# Every query function with connection to the user_mates table


@connect_to_sql
def sql_insert_user(cursor, user_values):
    query = """INSERT INTO user_mates(user_mates_name, reputation, submission_time)
               VALUES (%s, %s, %s)
            """
    cursor.execute(query, user_values)
