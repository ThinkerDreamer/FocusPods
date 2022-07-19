import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="focus_pods_db",
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"]
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("drop table if exists users;")
cur.execute("create table users (id serial primary key, "
                                "name varchar (100) NOT NULL,"
                                "email varchar (100) NOT NULL,"
                                "password varchar (50) NOT NULL);"
                                )
cur.execute("insert into users (name, email, password)"
            "values (%s, %s, %s)",
            ("Angel",
            "angel@angel.com",
            "123456")
            )

cur.execute("insert into users (name, email, password)"
            "values (%s, %s, %s)",
            ("Foo",
            "foo@foo.com",
            "0987")
            )

conn.commit()

cur.close()
conn.close()


