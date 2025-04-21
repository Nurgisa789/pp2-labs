import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="0123"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL
        );
    """)
    conn.commit()
    print("PhoneBook table created.")

def upload_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) >= 2:
                first_name = row[0].strip()
                phone = row[2].strip().replace('"', '') if len(row) > 2 else ''
                try:
                    cur.execute(
                        "INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)",
                        (first_name, phone)
                    )
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    print(f"Skipped duplicate phone: {phone}")
                else:
                    conn.commit()
    print("CSV upload complete.")

def insert_from_console():
    name = input("Enter user's first name: ")
    phone = input("Enter user's phone number: ")
    cur.execute(
        "INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("User added.")

def update_user():
    id = input("Enter user ID to update: ")
    field = input("What do you want to update? (first_name/phone): ").strip()
    if field not in ['first_name', 'phone']:
        print("Invalid field.")
        return
    new_value = input(f"Enter new value for {field}: ")
    cur.execute(f"UPDATE PhoneBook SET {field} = %s WHERE id = %s", (new_value, id))
    conn.commit()
    print("User updated.")

def query_data():
    filter_type = input("Filter by (first_name/phone/all): ").strip()
    if filter_type == "all":
        cur.execute("SELECT * FROM PhoneBook")
    else:
        value = input(f"Enter value for {filter_type}: ")
        cur.execute(f"SELECT * FROM PhoneBook WHERE {filter_type} = %s", (value,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    if not rows:
        print("No data found.")

def delete_user():
    by = input("Delete by (first_name/phone): ").strip()
    if by not in ['first_name', 'phone']:
        print("Invalid option.")
        return
    value = input(f"Enter value to delete by {by}: ")
    cur.execute(f"DELETE FROM PhoneBook WHERE {by} = %s", (value,))
    conn.commit()
    print("User deleted.")

def main():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Upload from CSV")
        print("2. Insert new user from console")
        print("3. Update user")
        print("4. Query users")
        print("5. Delete user")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            upload_from_csv("Lab10/phonebook/PhoneBook_data.csv")
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_user()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()