from sqlalchemy import create_engine, text

DB_URI="sqlite:///data/textbook.sqlite3"

def get_user_selection():
    selection=0
    while selection == 0:
        print("What do you want to do:")
        print("1. find books for a certain year")
        print("2. find a title for a book")
        print("3. search for books in a year range")
        print("4. Search for year range AND title")

        user_select=int(input("what do you want to do: "))
        if 1 <= user_select <=4:
            return user_select
        print("Wrong input, please provide a number from 1 to 4!"
              "")




def get_books_by_year()->list:
    user_input = input("Enter the year: ")

    query = (""" 
    SELECT title FROM books
    WHERE publication_year = :search 
    """)
    print(query)
    params = {'search': user_input}
    engine = create_engine(DB_URI)
    with engine.connect() as con:
        results = con.execute(text(query), params)
        rows = results.fetchall()

    return rows

def get_books_by_title()->list:
    user_input = input("Enter your title: ")

    query = (""" 
    SELECT title FROM books
    WHERE lower(title) LIKE  :search 
    """)
    print(query)
    params = {'search': f"%{(user_input.lower())}%"}
    print(params)
    engine = create_engine(DB_URI)
    with engine.connect() as con:
        results = con.execute(text(query), params)
        rows = results.fetchall()
    print(type(rows))
    return rows


def get_books_by_year_range()->list:
    user_input_A = input("Enter the START year: ")
    user_input_B = input("Enter the END year: ")

    query = (""" 
    SELECT title FROM books
    WHERE publication_year BETWEEN 
    :search_A AND :search_B 
    """)
    print(query)
    params = {'search_A': user_input_A, 'search_B': user_input_B}
    engine = create_engine(DB_URI)
    with engine.connect() as con:
        results = con.execute(text(query), params)
        rows = results.fetchall()

    return rows

def get_books_by_title_and_range()->list:
    user_input_A = input("Enter the START year: ")
    user_input_B = input("Enter the END year  : ")
    user_input_C = input("Enter your title    : ")

    query = (""" 
    SELECT title FROM books
    WHERE (publication_year BETWEEN 
    :search_A AND :search_B ) AND (
    lower(title) LIKE  :search_C )
    """)
    print(query)
    params = {'search_A': user_input_A,
              'search_B': user_input_B,
              'search_C': f"%{(user_input_C.lower())}%"
             }
    engine = create_engine(DB_URI)
    with engine.connect() as con:
        results = con.execute(text(query), params)
        rows = results.fetchall()

    return rows


def main():
    books=[]
    user_selection= get_user_selection()
    if user_selection == 1:
        books=get_books_by_year()
    elif user_selection ==2:
        books=get_books_by_title()
    elif user_selection ==3:
        books=get_books_by_year_range()
    elif user_selection ==4:
        books=get_books_by_title_and_range()

    for book in books:
        print(book._mapping['title'])
if __name__ == "__main__":
    main()

