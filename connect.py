import psycopg2
import personal_config


def connect_to_sql(func):
    def with_connection(*args):
        # setup connection string
        connect_str = personal_config.my_connection()
        # use our connection values to establish a connection
        conn = psycopg2.connect(host=connect_str["host"],
                                user=connect_str["user"],
                                password=connect_str["passwd"],
                                dbname=connect_str["dbname"])
        try:
            # set autocommit option, to do every query when we call it
            conn.autocommit = True
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            rv = func(cursor, *args)
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return rv
    return with_connection
