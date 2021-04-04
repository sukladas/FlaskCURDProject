# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt
import bcrypt

import MySQLdb
import pymysql
import datetime
import requests
import random
import re
import os

import db

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key= os.urandom(24)

#Connecting to google cloud data base

connection = pymysql.connect(#unix_socket = '/cloudsql/united-time-307112:europe-west2:booksdb',
        host= '35.234.145.114',
        user='booksdb',
        password='abcd1234',
        db='booksdb',
        cursorclass=pymysql.cursors.DictCursor)

cursor=connection.cursor()



@app.route('/')
def login():

   return render_template('login.html')


@app.route('/register')
def about():

   return render_template('register.html')


@app.route('/home')
def home():
    if 'userid' in session:
      return render_template('home.html')
    else :
      return redirect('/')


# Here we are using both GET and POST methods to validate the user then allowing to login
@app.route('/login_validate', methods=['GET','POST'])
def login_validate():
      email=request.form.get('email')

      password_entered=request.form.get('password')
      cursor=connection.cursor()

      data=cursor.execute("""SELECT * FROM `Users` WHERE `Email_ID` LIKE '{}'""".format(email))
      if data>0:
         user=cursor.fetchone()

         password=user['Password']
         if bcrypt.check_password_hash(password, password_entered):
             print('password')
             session["login"]=True
             session['email']=user['Email_ID']
             session['userid']=user['User_ID']
             return redirect(url_for('index'))
             cursor.close()
         else:
              return render_template('login.html')

      else:
              return render_template('login.html')


#Here we are doing the registration of an user and using POST method to add those information to database

@app.route('/add_user', methods=['POST'])
def add_user():

      firstname=request.form.get('ufirstname')
      lastname=request.form.get('ulastname')
      email=request.form.get('uemail')
      password=request.form.get('upassword')

      pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

      result=cursor.execute("SELECT * FROM `Users` WHERE `Email_ID` LIKE '{}' ".format(email))
      data = cursor.fetchall()
      if result>0:

         return redirect('/register')

      else:

          cursor.execute("""INSERT INTO `Users` (`User_ID`,`First_Name`,`Last_Name`,`Email_ID`,`Password`,`User_Role`) VALUES (NULL,'{}','{}','{}','{}','User')"""
                   .format(firstname,lastname,email,pw_hash) )
          connection.commit()



          return render_template('login.html')

@app.route('/index')
def index():
     if 'userid' in session:
        userid = session['userid']
        lib_data = db.get_libraries(userid)
        return render_template('home.html', libraries = lib_data)

     else :
        return redirect('/')


@app.route('/logout')
def logout():
    return redirect('/')

# search route
@app.route("/search", methods = ["POST", "GET"])
def search():
     if 'userid' in session:
        userid = session['userid']
        library_list = db.get_libraryname(userid)

        # if user reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
        # gets user selected library id from form
            libraryid = request.form.get("libraryid")
        # if user provided author of the book
            if request.form.get("author"):


                """
                return rendered result.html page with books from Google Books API written by the provided author that match
                as well as the library id the user selected
                search results
                """
                return render_template("search_results.html",libraryid = request.form.get("libraryid"), books = requests.get("https://www.googleapis.com/books/v1/volumes?q=" +
                               "inauthor:" + request.form.get("author") +
                               "&key=AIzaSyACOxr3O430Dm1qft8xUBFFR3a7CA-zV2g").json())

            # return rendered result.html page with books from Google Books API that match search results
            return render_template("search_results.html",libraryid = request.form.get("libraryid"),books=requests.get("https://www.googleapis.com/books/v1/volumes?q=" +
                            request.form.get("title") + "&key=AIzaSyACOxr3O430Dm1qft8xUBFFR3a7CA-zV2g").json())

        # else if user reached route via GET (as by clicking a link or via redirect)
        else:
            # return rendered search.html page
            return render_template("search.html",library_list = library_list)
     else :
      return redirect('/')

@app.route('/search_results',methods = ['POST'])
def search_results():
    if 'userid' in session:
    #if user selects to add a book from the list of books
        if request.method == "POST":
            #gets the selected books googlebook id  and the selected libraryid from the previous page
            bookid = request.form['bookid']
            libraryid = request.form['libraryid']
            title = request.form['titleval']
            author = request.form['authorval']
            #adds the book to the database storing the googlebooksapi id as well as the users library id to the database
            db.add_books(libraryid , bookid, title, author)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else :
      return redirect('/')

@app.route("/create_library")

def create_library():
    if 'userid' in session:
        return render_template("Create_library.html")
    else :
      return redirect('/')

@app.route('/inserts',methods = ['POST'])
def name_description():

    if request.method == 'POST':

       libraryname = request.form['libraryname']
       Description = request.form['Description']
       userid = session['userid']
       db.add_library(libraryname,Description,userid)
    return render_template("insert.html")
@app.route('/library/<int:library_id>')
def library(library_id):
    books = db.get_bk(library_id)
    return render_template("library.html", books = books)


@app.route('/add_library', methods = ["POST", "GET"])
def add_library():
    if 'userid' in session:
        if request.method == 'POST':
            userid = session['userid']
            name = request.form['name']
            description = request.form['description']
            db.add_lib(name, description, userid)
            flash("Library Added Successfully")
            return redirect(url_for('index'))
    else:
      return redirect('/')

# update library
@app.route('/update_library/<int:library_id>', methods = ["POST", "GET"])
def update_library(library_id):
    if 'userid' in session:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            db.update_lib(library_id,name,description)
            flash("Library Updated Successfully")
            return redirect(url_for('index'))
    else:
      return redirect('/')


@app.route('/delete_library/<int:library_id>', methods=["GET"])
def delete_library(library_id):
    if 'userid' in session:
        db.delete_lib(library_id)
        flash("Library Deleted Successfully")
        return redirect(url_for('index'))
    else:
      return redirect('/')



@app.route('/update_book/<int:book_id>/', methods = ["POST", "GET"])
def update_book(book_id):
    if 'userid' in session:
        if request.method == 'POST':
            name = request.form['name']
            author = request.form['author']
            genre = request.form['genre']
            db.update_bk(book_id,name,author,genre)
            flash("Book Updated Successfully")
            return redirect(url_for('books'))
    else:
      return redirect('/')








@app.route('/edit/<int:library_id>', methods=['GET','POST'])
def edit(library_id):
    if 'userid' in session:
        library = db.get_userlib(library_id)
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            db.update_lib(library_id,name,description)
            flash("Library Updated Successfully")
            return redirect(url_for('index'))
        else:
            return redirect(url_for('edit', library_id=library_id))
    else:
      return redirect('/')

@app.route('/open_book/<int:book_id>/', methods=["GET"])
def open_book(book_id):

    return redirect(url_for('search'))

@app.route('/delete_book/<book_id>/', methods=["GET"])
def delete_book(book_id):
     if 'userid' in session:
        library = db.get_library_id(book_id)
        library_id = library['library_id']
        db.delete_bk(book_id)
        flash("Book Deleted Successfully")
        return redirect(url_for('library',library_id = library_id))
     else:
      return redirect('/')

app.run()
