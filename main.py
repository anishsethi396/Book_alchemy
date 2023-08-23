from flask import Flask, render_template, request, redirect
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///data/library.sqlite'

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Route handler for the home page.
    This function handles requests to the root URL, and it allows sorting and searching
     of books and renders the home template.
    :return:
    """
    sort_key = request.args.get('sort', 'title')

    search_query = request.args.get('search')
    search = "%{}%".format(search_query)
    if search_query is not None:
        books = Book.query.filter(Book.title.like(search)).all()

    else:
        if sort_key == 'title':
            books = Book.query.order_by(Book.title).all()
        elif sort_key == 'author':
            books = Book.query.join(Author).order_by(Author.name).all()

    for book in books:
        author = Author.query.get(book.author_id)
        book.author = author

        book.cover_image = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg"

    return render_template('home.html', books=books, sort_key=sort_key)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    This function handles requests to the '/add_author URL, and it allows adding a new author to the
    database and renders the 'add_author.html' template
    :return:
    """
    if request.method == 'POST':
        name = request.form['name']
        d_o_b = request.form['birthdate']
        d_o_d = request.form['date_of_death']

        birth_date = datetime.strptime(d_o_b, '%Y-%m-%d').date()
        date_of_death = datetime.strptime(d_o_d, '%Y-%m-%d').date()

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        db.session.add(new_author)
        db.session.commit()
        message = 'Author added successfully!'

        return render_template('add_author.html', message=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
      This function handles requests to the '/add_book' URL , and
    it allows adding a new book to the database and renders the 'add_book.html' template.
    """
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_name = request.form.get('author_name')

        author_id = db.session.query(Author).filter(Author.name == author_name).first().id

        book = Book(
            isbn=isbn,
            title=request.form.get("title"),
            publication_year=int(publication_year),
            author_id=author_id
        )
        db.session.add(book)
        db.session.commit()
        message = 'Book added successfully!'
        return render_template('add_book.html', message=message)
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """

    This function handles requests to the '/delete/<int:book_id>' URL, and
    it allows deleting a book from the database based on the provided book_id.
    """
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
