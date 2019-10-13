import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'book_review'
app.config['MONGO_URI'] = 'mongodb+srv://root:rootUser@myfirstcluster-lrum9.mongodb.net/book_review?retryWrites=true&w=majority'

mongo = PyMongo(app)

#This pulls all books from the DB as a start and displays them on the home page
@app.route('/')
@app.route('/get_book')
def get_book():
    return render_template("books.html", books=mongo.db.books.find())
    
#redirct function to the page where users can add a book   
@app.route('/add_book')
def add_book():
    return render_template('addbook.html') 
    
    
#function to add the book to the database    
@app.route('/insert_book', methods =['POST'])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    return redirect(url_for('get_book'))    


#This function redirects to a view page with more information on the book that was clicked on    
@app.route('/view_book/<book_id>')
def view_book(book_id):
   the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
   return render_template('viewbook.html', book=the_book)
 
 
#This function shows all of the books on the viewbook.html page, when the book is clicked on from the home page   
@app.route('/show_book/<book_id>')
def show_book(book_id):
    books = mongo.db.books
    books.find_one({'_id':ObjectId(book_id)},
    {
    'book_name':request.form.get('book_name')
    })


#function to redirect to the page to edit book details     
@app.route('/edit_book/<book_id>')
def edit_book(book_id):
  the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
  return render_template('editbook.html', book=the_book)
  
  
@app.route('/update_book/<book_id>', methods = ["POST"])
def update_book(book_id):
    books = mongo.db.books
    books.update({'_id': ObjectId(book_id)},
    {
        'book_name':request.form.get('book_name'),
        'author_name':request.form.get('author_name'),
        'cover_link':request.form.get('cover_link'),
        'link':request.form.get('link'),
        'Genre':request.form.get('Genre'),
        'published_date':request.form.get('published_date'),
        'review':request.form.get('review')
    })
    return redirect(url_for('get_book'))

#Deletes a book
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_book'))

if __name__ =='__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug= True)
        
        