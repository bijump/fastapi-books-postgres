from sqlalchemy import Boolean,Integer,ForeignKey,String,Column,Select
from sqlalchemy.orm import registry,relationship,sessionmaker
from database import Base,engine
from contextlib import contextmanager

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
class Author(Base):
    __tablename__="authors"
    author_id=Column(Integer,primary_key=True)
    first_name=Column(String(length=50))
    last_name=Column(String(length=50))

    def __repr__(self):
        return('<Author(author id={0},first name={1},last name={2})>'.format(self.author_id,self.first_name,self.last_name))
class Book(Base):
    __tablename__="books"
    book_id=Column(Integer,primary_key=True)
    title=Column(String(length=255))
    number_of_pages=Column(Integer)
    def __repr__(self):
        return('<Book(book id={0},title={1},pages={2})>'.format(self.book_id,self.title,self.number_of_pages))
class BookAuthor(Base):
    __tablename__="bookauthors"
    book_author_id=Column(Integer,primary_key=True)
    author_id=Column(Integer,ForeignKey('authors.author_id'))
    book_id=Column(Integer,ForeignKey('books.book_id'))
    author=relationship("Author")
    book=relationship("Book")

    def __repr__(self):
        return('<BookAuthor(book author id={0},book author={1},book title={2},pages={3})>'.format(self.book_author_id,self.author.first_name,self.book.title,self.book.number_of_pages))

def add_book(book:Book,author:Author):
    with session_scope() as session:
        existing_book=session.execute(Select(Book).filter(Book.title==book.title and Book.number_of_pages==book.number_of_pages)).scalar()
        if existing_book is not None:
            print("Book already exists")
            return
        print("Adding book")
        session.add(book)
        existing_author=session.execute(Select(Author).filter(Author.first_name==author.first_name and Author.last_names==author.last_name)).scalar()
        if existing_author is not None:
            print("Author already exists")
            session.flush()
            pairing=BookAuthor(author_id=existing_author.author_id,book_id=book.book_id)
        else:
            session.add(author)
            session.flush()
            pairing=BookAuthor(author_id=author.author_id,book_id=book.book_id)
        session.add(pairing)
        #session.commit()
        print("New book information added")
        