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
            "created_at timestamptz NOT NULL,"
            "password varchar (50) NOT NULL);"
            )
            
cur.execute("drop table if exists rooms;")
cur.execute("create table rooms (id serial primary key, "
            "name varchar (100),"
            "created_at timestamptz NOT NULL);"
            )

cur.execute("drop table if exists rooms_users;")
cur.execute("create table rooms_users (room_id serial references rooms(id),"
            "user_id integer references users(id));"
            )
            
cur.execute("insert into rooms (name, created_at)"
            "values (%s, %s)",
            ("First room",
             "2020-01-01 00:00:00")
            )

cur.execute("insert into users (name, email, created_at, password)"
            "values (%s, %s, %s, %s)",
            ("Angel",
            "angel@angel.com",
             "1971-09-18",
            "123456")
            )

cur.execute("insert into users (name, email, created_at, password)"
            "values (%s, %s, %s, %s)",
            ("Shae",
             "shae@scannedinavian.com",
             "1971-09-18",
             "0987")
            )

cur.execute("insert into rooms_users (room_id, user_id)"
            "values (%s, %s)",
            (1, 1)        
            )

cur.execute("insert into rooms_users (room_id, user_id)"
            "values (%s, %s)",
            (1, 2)        
            )

conn.commit()

cur.close()
conn.close()
