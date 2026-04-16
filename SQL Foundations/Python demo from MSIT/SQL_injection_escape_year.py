from sqlalchemy import create_engine, text

DB_URI="sqlite:///data/textbook.sqlite3"

user_input=input("Enter the year:" )

query = ( """ 
SELECT title FROM books
WHERE publication_year = :search 
""")
print(query)
params = { 'search' : user_input}
engine=create_engine(DB_URI)
with engine.connect() as con:
    results=con.execute(text(query),params)
    rows=results.fetchall()

for row in rows:
    print(row._mapping['title'])