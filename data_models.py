from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return f"Author's id = {self.id}, name = {self.name}, birth_date = {self.birth_date}" \
               f", date_of_death = {self.date_of_death}"

    def __str__(self):
        return self.__repr__()


class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.id'))

    def __repr__(self):
        return f"Book's id = {self.id}, isbn = {self.isbn}, title = {self.title}" \
               f", publication_year = {self.publication_year}, author_id = {self.author_id}"

    def __str__(self):
        return self.__repr__()
