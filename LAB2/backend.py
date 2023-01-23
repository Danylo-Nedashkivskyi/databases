import psycopg2
import time

tables = {
    1: "Email",
    2: "Folder",
    3: "User"
}

table_args = {
    1: "email_id,email_title,email_date,folder_fk,user_fk",
    2: "folder_name,folder_id,user_fk",
    3: "user_name,user_date"
}

primkeys = {
    1: "email_id",
    2: "folder_name",
    3: "user_name"
}

def connect_db():
    connection = psycopg2.connect(
        user="postgres",
        password="betaliker",
        host="localhost",
        port="5432",
        database="E-mails"
        )
    return connection

def connect(func):
    def inner_func(conn, *args, **kwargs):
        try:
            get = conn.cursor()
            get.execute("SELECT * FROM public.\"User\";")
        except:
            conn = connect_db()
        return func(conn, *args, **kwargs)
    return inner_func

def disconnect_db(conn):
    if conn:
        conn.close()

@connect
def insert_one(conn, table, args):
    sql = "INSERT INTO public.\"{}\" ({}) VALUES (".format(tables[table],table_args[table])
    q_marks = ["".join("%s") for x in args]
    sql += ",".join(q_marks) + ")"
    get = conn.cursor()
    get.execute(sql, args)
    conn.commit()

def tuple_to_dict(tuple, table):
    wdict = dict()
    if table == 1:
        wdict["email_id"] = tuple[0]
        wdict["email_title"] = tuple[1]
        wdict["email_date"] = tuple[2]
        wdict["folder_fk"] = tuple[3]
        wdict["user_fk"] = tuple[4]
    elif table == 2:
        wdict["folder_name"] = tuple[0]
        wdict["folder_id"] = tuple[1]
        wdict["user_fk"] = tuple[2]
    else:
        wdict["user_name"] = tuple[0]
        wdict["user_date"] = tuple[1]
    return wdict

@connect
def select_one(conn, table, category, item):
    sql = "SELECT * FROM public.\"{}\" WHERE {}='{}'".format(tables[table], category, item)
    get = conn.cursor()
    get.execute(sql)
    res = get.fetchone()
    if res:
        return tuple_to_dict(res, table)
    else:
        raise Exception("item {} doesn't exist in table {}".format(item, tables[table]))

@connect
def select_all(conn, table):
    sql = "SELECT * FROM public.\"{}\"".format(tables[table])
    get = conn.cursor()
    get.execute(sql)
    res = get.fetchall()
    return list(map(lambda x: tuple_to_dict(x, table), res))

@connect
def update_one(conn, table, item, args):
    sql_check = "SELECT EXISTS(SELECT 1 FROM public.\"{}\" WHERE {}=%s)".format(tables[table], primkeys[table])
    sql_update = "UPDATE public.\"{}\" SET ".format(tables[table])
    arg_set = "=%s,".join(table_args[table].split(","))
    sql_update += arg_set + "=%s WHERE " + primkeys[table] + "=%s"
    get = conn.cursor()
    get.execute(sql_check, (item,))
    res = get.fetchone()
    newargs = list(args)
    newargs.append(item)
    newargs = tuple(newargs)
    if res[0]:
        get.execute(sql_update, newargs)
        conn.commit()
    else:
        raise Exception("item {} doesn't exist in table {}".format(item, tables[table]))

@connect
def delete_one(conn, table, item):
    sql_check = "SELECT EXISTS(SELECT 1 FROM public.\"{}\" WHERE {}=%s)".format(tables[table], primkeys[table])
    sql_delete = "DELETE FROM public.\"{}\" WHERE {}=%s".format(tables[table], primkeys[table])
    get = conn.cursor()
    get.execute(sql_check, (item,))
    res = get.fetchone()
    if res[0]:
        get.execute(sql_delete, (item,))
        conn.commit()
    else:
        raise Exception("item {} doesn't exist in table {}".format(item, tables[table]))

@connect
def find(conn, item, rel):
    if rel == 1:
        sql = """SELECT email_title,email_date,user_name FROM
            (SELECT L.email_title,L.email_date,R.user_name FROM
            public.\"Email\" L LEFT JOIN public.\"User\" R on L.user_fk=R.user_name
            WHERE R.user_name LIKE \'{}\' GROUP BY L.email_title,L.email_date,R.user_name) as foo""".format(item)
    elif rel == 2:
        sql = """SELECT folder_name,folder_id,user_name FROM
            (SELECT L.folder_name,L.folder_id,R.user_name FROM
            public.\"Folder\" L LEFT JOIN public.\"User\" R on L.user_fk=R.user_name
            WHERE R.user_name LIKE \'{}\' GROUP BY L.folder_name,L.folder_id,R.user_name) as foo""".format(item)
    else:
        sql = """SELECT email_title,email_date,folder_name FROM
            (SELECT L.email_title,L.email_date,R.folder_name FROM
            public.\"Email\" L LEFT JOIN public.\"Folder\" R on L.folder_fk=R.folder_id
            WHERE R.folder_name LIKE \'{}\' GROUP BY L.email_title,L.email_date,R.folder_name) as foo""".format(item)
    get = conn.cursor()
    beg = int(time.time() * 1000)
    get.execute(sql)
    end = int(time.time() * 1000) - beg
    print("Time elapsed searching: {} ms".format(end))
    records = get.fetchall()
    return records

@connect
def randomize(conn, table, n):
    if table == 1:
        sql = """INSERT INTO public."Email" (email_id,email_title,email_date,folder_fk,user_fk)
        SELECT nextval('email_seq'),
        chr(trunc(65+random()*25)::int)||chr(trunc(65+random()*25)::int),
        timestamp '2014-01-10 20:00:00'+random()*(timestamp '2014-01-20 20:00:00'-timestamp '2014-01-10 10:00:00'),
        (SELECT * FROM (SELECT folder_id FROM public."Folder" ORDER BY random()) as foo LIMIT 1) as bar,
        (SELECT * FROM (SELECT user_name FROM public."User" ORDER BY random()) as baz LIMIT 1) as qux
        FROM generate_series(1,{})
        """.format(n)
    elif table == 2:
        sql = """INSERT INTO public."Folder" (folder_name,folder_id,user_fk)
        SELECT chr(trunc(65+random()*25)::int)||chr(trunc(65+random()*25)::int),
        nextval('folder_seq'),
        (SELECT * FROM (SELECT user_name FROM public."User" ORDER BY random()) as foo LIMIT 1) as bar
        FROM generate_series(1,{})
        """.format(n)
    elif table == 3:
        sql = """INSERT INTO public."User" (user_name,user_date)
        SELECT chr(trunc(65+random()*25)::int)||chr(trunc(65+random()*25)::int),
        timestamp '2014-01-10 20:00:00'+random()*(timestamp '2014-01-20 20:00:00'-timestamp '2014-01-10 10:00:00')
        FROM generate_series(1,{})
        """.format(n)
    get = conn.cursor()
    get.execute(sql)
    conn.commit()