import sqlite3
from icecream import ic as print


#Step 1 - Setuup / Initialize Database
def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")
        raise

#Step 2 - Create a Table in the Database
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE
    )
    """ # SQL needs 3 sets of double quotes

    try:
        with connection:
            connection.execute(query)
            print(f"Table users was created!")
    except Exception as e:
        print(f"Error: {e}")
        raise

#Step 3 - Fill the database with data: add User to DataBase
def insert_user(connection, name:str, age:int, email:str ):
    query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (name, age, email))
            print(f"User: {name} was added to your database")
    except Exception as e:
        print(e)
        raise

def return_user_id_from_name(connection, name: str) -> list[tuple]:
        query = f"SELECT * FROM users WHERE name = '{name}'"
        print(query)

        try:
            with connection:
                rows = connection.execute(query).fetchall()
            print (rows)
            for user_id,name,age,email in rows:
                return user_id
        except Exception as e:
            print(f"Oh Oh Oh, weer een fout!{e}")

# Step 4 Query all Users in Database
def fetch_users(connection, condition: str=None) -> list[tuple]:
    query= "SELECT * FROM users"
    if condition:
        query += f" WHERE {condition}"
    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(e)

# Step 5 Delete a User from the Database
def delete_user(connection, user_id: int):
    query = "DELETE FROM users WHERE id = ?"
    try:
        with connection:
            connection.execute(query,str((user_id)))
            print (f"{user_id} was deleted")
    except Exception as e:
        print(e)
        raise(e)
# Step 6Update an existing User
def update_user(connection, user_id:int, name: str, age: int, email: str, ):
    update_list=[("name",name),("age", age),("email", email)]
    for key,value in update_list:
        print(f"this is key: {key} and new value: {value}")
        query = f"UPDATE users SET {key} = ? WHERE id = ?"
        try:
            with connection:
                connection.execute(query, (value, user_id))
                print (f"DB record {user_id} was updated with {key} to new value {value} ")
        except Exception as e:
            print(e)
            raise(e)

# Main Function Wrapper

def main():
    connection = get_connection(("my_first_db.db"))

    #Create my table
    try:
        while True:
            create_table(connection)
            start = int(input("Enter option (1-Add, 2-Delete, 3-Update, 4-Search, 5-AddMAny, 6-Return ID)"))
            if start == 1:
                name = input("Enter name:")
                age = int(input("Enter age:"))
                email = input("Enter email:")
                insert_user(connection,name,age,email)
            elif start == 4:
                print("All Users:")
                for user in fetch_users(connection):
                    print(user)
            elif start == 2:
                print("Delete User")
                user_id = int(input("What user id should be deleted:"))
                delete_user(connection,user_id)
            elif start == 3:
                print("Update User:")
                user_id = int(input("What user id should be updated:"))
                name = input("Enter new name:")
                age = int(input("Enter new age:"))
                email = input("Enter new email:")
                update_user(connection,user_id,name,age,email)
            elif start == 6:
                print("Fetching the user_ID:")
                name = input("Enter the name:")
                user_id = return_user_id_from_name(connection, name)
                if user_id != None:
                    print(f"The user_ID of {name} is: {user_id}")
                else:
                    print(f"The user {name} is not found in the database")
    except KeyboardInterrupt:
        connection.close()
        print("\nStopped by user")
    finally:
        connection.close()




if __name__ == "__main__":
    main()