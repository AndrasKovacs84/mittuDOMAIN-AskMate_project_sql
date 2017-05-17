import psycopg2
from connect import connect_to_sql


@connect_to_sql
def sql_select(query):
    '''Displays the query chosen by the user. Parameter is a dictionary of the relevant properties
    for a simple query. Returns the results of the query. data[0] = list of column names as header,
    data[1] = list of lists, where each nested list represents a row of data.'''
    data = {'header': [],
            'result_set': []}
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
def sql_insert(query, data_to_insert):
    '''Inserts data into table. data_to_insert = {'table': 'tablename', 'columns': [list of columns],
    'values': [list_of_values]}. Function returns nothing.'''
    data = {'header': [],
            'result_set': []}
    cursor.execute("""
                   INSERT INTO {0}({1})
                   VALUES ({2})
                   """.format(data_to_insert['table'], ', '.join(data_to_insert['columns']),
                   ', '.join(data_to_insert['values'])))


@connect_to_sql
def sql_update():
    pass


@connect_to_sql
def sql_delete():
    pass
