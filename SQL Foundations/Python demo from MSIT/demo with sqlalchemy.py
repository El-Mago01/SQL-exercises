from sqlalchemy import create_engine, text

DB_URI='sqlite:///textbook.sqlite3'
query=("""
SELECT 
    books.publication_year AS publication_year, 
    books.title AS title, 
    authors.name AS name FROM books 
JOIN authors ON authors.author_id = books.author_id
WHERE publication_year>2000
;
""")
engine=create_engine(DB_URI)
with engine.connect() as connection:
    try:
        result = connection.execute(text(query))
        rows = result.fetchall()
    except Exception as e:
        rows=f"Error, encountered exception /n/n{e}"

print(f"Returned {len(rows)} results")
print(rows)
for row in rows:
    row_dict = row._mapping
    print(f"{row_dict['publication_year']}:{row_dict['title']} ({row_dict['name']})")
