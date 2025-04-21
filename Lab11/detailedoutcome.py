import psycopg2
import csv

conn = None
cur = None
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="0123"
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS PhoneBook CASCADE")

    cur.execute("""
        CREATE TABLE PhoneBook(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone_number VARCHAR(50) NOT NULL
        )
    """)

    with open('Lab11/phonebook.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO PhoneBook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                (row[1], row[2], row[3]))

    print("Current PhoneBook data:")
    cur.execute("SELECT * FROM PhoneBook")
    for record in cur.fetchall():
        print(record)

    print("Searching for records with 'Bob' using function...")
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_records_by_pattern_func(pattern TEXT)
        RETURNS TABLE (id INTEGER, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR)
        AS $$
        BEGIN
            RETURN QUERY SELECT * FROM PhoneBook WHERE PhoneBook.first_name LIKE pattern 
                         OR PhoneBook.last_name LIKE pattern 
                         OR PhoneBook.phone_number LIKE pattern; 
        END;
        $$
        LANGUAGE plpgsql;
    """)
    cur.execute("SELECT * FROM get_records_by_pattern_func(%s)", ('Bob',))
    rows = cur.fetchall()
    for record in rows:
        print(record)

    print("Inserting user 'ABA' or updating if exists...")
    cur.execute("""
        CREATE OR REPLACE PROCEDURE insert_user(name VARCHAR(50), phone_number VARCHAR(50))
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF EXISTS (SELECT * FROM PhoneBook WHERE first_name = name) THEN
                UPDATE PhoneBook SET phone_number = insert_user.phone_number WHERE first_name = insert_user.name;
            ELSE
                INSERT INTO PhoneBook (first_name, phone_number) VALUES (name, phone_number);
            END IF;
        END;
        $$;
    """)
    cur.execute('CALL insert_user(%s, %s)', ('ABC', '1234567'))

    cur.execute("SELECT * FROM PhoneBook")
    for record in cur.fetchall():
        print(record)

    print("Pagination (limit=1, offset=2):")
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_users_with_pagination(
            limit_val INTEGER,
            offset_val INTEGER
        ) RETURNS SETOF PhoneBook AS $$
        BEGIN
            RETURN QUERY SELECT * FROM PhoneBook LIMIT limit_val OFFSET offset_val;
        END;
        $$ LANGUAGE plpgsql;
    """)
    cur.execute("SELECT * FROM get_users_with_pagination(1, 2)")
    paginated = cur.fetchall()
    for row in paginated:
        print(row)

    print("Deleting user with name 'John' or phone '5551234'...")
    cur.execute("""
        CREATE OR REPLACE PROCEDURE delete_user_by_username_or_phone(
            p_username VARCHAR(50),
            p_phone VARCHAR(50)
        )
        AS $$
        BEGIN  
            DELETE FROM phonebook
            WHERE first_name = p_username OR phone_number = p_phone;

            IF NOT FOUND THEN
                RAISE EXCEPTION 'No rows found for username or phone %, %', p_username, p_phone;
            END IF;
        END;
        $$ LANGUAGE plpgsql;
    """)
    cur.execute("CALL delete_user_by_username_or_phone('John', '5551234')")

    print("PhoneBook data:")
    cur.execute("SELECT * FROM PhoneBook")
    for record in cur.fetchall():
        print(record)

except (Exception, psycopg2.DatabaseError) as error:
    print("ERROR:", error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print("Database connection closed")
