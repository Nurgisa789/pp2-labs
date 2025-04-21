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

    PhoneBookTable = """CREATE TABLE PhoneBook(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NULL,
        phone_number VARCHAR(50) NOT NULL
    )"""
    cur.execute(PhoneBookTable)

    with open('Lab11/phonebook.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO PhoneBook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                (row[1], row[2], row[3]))

    '''
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")
    cur.execute(
        "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
        (first_name, last_name, phone_number))
    '''
    cur.execute("SELECT * FROM PhoneBook")
    for record in cur.fetchall():
        print(record)

    '''
    cur.execute("SELECT * FROM PhoneBook WHERE first_name = %s", ('John',))
    rows = cur.fetchall()
    print(rows)
    '''
    '''
    delete = "DELETE from PhoneBook WHERE first_name = %s"
    cur.execute(delete, ('John',))
    '''

    cur.execute("""
        CREATE OR REPLACE FUNCTION get_records_by_pattern_func(pattern TEXT)
        RETURNS TABLE (id INTEGER, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR)
        AS $$
        BEGIN
            RETURN QUERY SELECT * FROM PhoneBook WHERE PhoneBook.first_name LIKE pattern OR PhoneBook.last_name LIKE pattern OR PhoneBook.phone_number LIKE pattern; 
        END;
        $$
         LANGUAGE plpgsql;
    """)
    cur.execute("SELECT * FROM get_records_by_pattern_func(%s)", ('Bob',))
    rows = cur.fetchall()
    for record in rows:
        print(record)

    cur.execute("""
    CREATE OR REPLACE PROCEDURE insert_user(name VARCHAR(50), phone_number VARCHAR(50))
    LANGUAGE plpgsql
    AS $$
    BEGIN
        -- check if user already exists
        IF EXISTS (SELECT * FROM PhoneBook WHERE first_name = name) THEN
            -- update phone number
            UPDATE PhoneBook SET phone_number = insert_user.phone_number WHERE first_name = insert_user.name;
        ELSE
            -- insert new user
            INSERT INTO PhoneBook (first_name, phone_number) VALUES (name, phone_number);
        END IF;
    END;
    $$
    """)
    cur.execute('CALL insert_user(%s, %s)', ('ABA', '123456789'))

    '''''
    cur.execute("""
        CREATE OR REPLACE PROCEDURE insert_many_users(
          users_list text[],
          OUT incorrect_data text[]
        ) AS $$
        DECLARE
          i integer := 1;
          name text;
          phone text;
        BEGIN
          -- Loop through each name and phone number
          WHILE i <= array_length(users_list, 1) LOOP
            -- Split each user's data into name and phone number
            name := split_part(users_list[i], ',', 1);
            phone := split_part(users_list[i], ',', 2);
            -- Check correctness of phone number
            IF length(phone) <> 10 OR NOT phone ~ E'^\\d+$' THEN
              -- If phone number is incorrect, add to incorrect_data array
              incorrect_data := array_append(incorrect_data, name || ': ' || phone);
            ELSE
              -- If phone number is correct, insert new user into table
              INSERT INTO PhoneBook (first_name, phone_number) VALUES (name, phone);
            END IF;
            i := i + 1;
          END LOOP;
        END;
        $$ LANGUAGE plpgsql;
    """)
    users_list = [
        "Ann,1234567890",
        "Bob,5551234",
        "Chris,123-456-7890"
    ]
    cur.callproc('insert_many_users', (users_list, []))
    result = cur.fetchone()
    print(result[0])
    if result[1]:
        print('Incorrect data:', result[1])
    '''''
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

    cur.execute("""
    CREATE OR REPLACE PROCEDURE delete_user_by_username_or_phone(
        p_username VARCHAR(50),
        p_phone VARCHAR(50)
    )
    AS $$
    BEGIN  
        -- Delete from phonebook table
        DELETE FROM phonebook
        WHERE first_name = p_username OR phone_number = p_phone;
    
        -- Raise an exception if no rows were affected
        IF NOT FOUND THEN
            RAISE EXCEPTION 'No rows found for username or phone %, %', p_username, p_phone;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)
    cur.execute("CALL delete_user_by_username_or_phone('John', '5551234');")

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')