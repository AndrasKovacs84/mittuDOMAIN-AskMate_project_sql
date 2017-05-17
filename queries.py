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
                       """.format(query['table'], ", ".join(query['columns']), query['filter'], query['order_by']))
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
