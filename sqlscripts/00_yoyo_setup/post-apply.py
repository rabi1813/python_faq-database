import os
import globalvar
from yoyo import step


queries = ""
path_query_file = globalvar.path_query_file

def do_step(conn):
    cursor = conn.cursor()
    for query in queries.splitlines():
        cursor.execute(query)

if os.path.isfile(path_query_file):
    with open(path_query_file, 'r') as query_file:
        queries = query_file.read()
    step(do_step)
