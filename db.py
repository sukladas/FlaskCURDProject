import pymysql

connection = pymysql.connect(#unix_socket = '/cloudsql/united-time-307112:europe-west2:booksdb',
        host= '35.234.145.114',
        user='booksdb',
        password='abcd1234',
        db='booksdb',
        cursorclass= pymysql.cursors.DictCursor)


def add_users(username,password):
    cur=connection.cursor()
    cur.execute("INSERT INTO Users (username,password) VALUES (%s,%s)", (username,password))
    connection.commit()

def get_users():
    cur=connection.cursor()
    cur.execute("SELECT * FROM Users ")
    books = cur.fetchall()
    return books

def add_library(libraryname,Description,userid):
    cur=connection.cursor()
    cur.execute("INSERT INTO Libraries (name,description,user_id) VALUES (%s,%s,%s)", (libraryname,Description,userid))
    connection.commit()

def get_libraryname(userid):
    cur=connection.cursor()
    cur.execute("SELECT name ,library_id  FROM Libraries where user_id = '%s' " %userid)
    library_name = cur.fetchall()
    return library_name

def add_books(libraryid,bookid,title,author):
    cur=connection.cursor()
    cur.execute("INSERT INTO books (library_id,Googlebooksapiid,title,author) VALUES (%s,%s,%s,%s) ",(libraryid,bookid,title,author))
    connection.commit()

def add_users(username, password):
    cur = connection.cursor()
    cur.execute("INSERT INTO Users (username,password) VALUES (%s,%s)", (username, password))
    connection.commit()


def get_users():
    cur = connection.cursor()
    cur.execute("SELECT * FROM Users ")
    books = cur.fetchall()
    return books


def add_lib(libraryname, Description, userid):
    cur = connection.cursor()
    cur.execute("INSERT INTO Libraries (name,description,user_id) VALUES (%s,%s,%s)",
                (libraryname, Description, userid))
    connection.commit()








def get_libraries(user_id):
    cur=connection.cursor()
    cur.execute("SELECT * FROM Libraries WHERE user_id = %s",(user_id))
    libraries = cur.fetchall()
    return libraries


def update_lib(library_id,name,description):
    cur=connection.cursor()
    cur.execute("UPDATE Libraries SET name = %s, description = %s WHERE library_id = %s",(name,description,library_id))
    connection.commit()


def delete_lib(library_id):
    cur=connection.cursor()
    cur.execute("DELETE FROM Libraries WHERE library_id = %s", library_id)
    connection.commit()

def get_bk(library_id):
    cur=connection.cursor()
    cur.execute("SELECT * FROM books WHERE library_id = %s",(library_id))
    books = cur.fetchall()
    return books

def update_bk(book_id,name,author,genre):
    cur=connection.cursor()
    cur.execute("UPDATE books SET name = %s, author = %s, genre = %s WHERE book_id = %s",(name,author,genre,book_id))
    connection.commit()


def get_userlib(library_id):
    cur=connection.cursor()
    cur.execute("SELECT * FROM Libraries WHERE library_id = %s",(library_id))
    library = cur.fetchone()
    return library

def delete_bk(book_id):
    cur=connection.cursor()
    cur.execute("DELETE FROM books WHERE book_id = %s", book_id)
    connection.commit()

def get_library_id(book_id):
    cur=connection.cursor()
    cur.execute("SELECT * FROM books WHERE book_id = %s",(book_id))
    library = cur.fetchone()
    return library




# sql = """insert into `Users` (username, password)
#          values (%s, %s)
#     """
#
# test = connectdb()
# test.cursor().execute(sql,('sukla','abcd1234'))
# query = test.cursor().execute('select * from Users')
# test.commit()
# print(query)



