# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from models import Base, Book, User, Rating, Loan, Author

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def session(engine,tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    clear_mappers()

@pytest.fixture(scope='module')
def books(session):
    book_1 = Book(isbn="1", book_title="Test Book", book_author="Test Author", year_of_publication=2020, publisher="Test Publisher")
    book_2 = Book(isbn="2", book_title="Test Book", book_author="Test Author", year_of_publication=2020, publisher="Test Publisher")
    session.add_all([book_1,book_2])
    session.commit()
    return [book_1,book_2]

@pytest.fixture(scope='module')
def users(session):
    user_1 = User(user_id=1, location="Test Location", age=30)
    user_2 = User(user_id=2, location="Test Location", age=30)
    user_3 = User(user_id=3, location="Test Location", age=30)
    session.add_all([user_1,user_2,user_3])
    session.commit()
    return [user_1,user_2,user_3]


def test_book_statistics(session,books,users):

    assert books[0].get_book_statistics() == (0, None, None)

    rating1 = Rating(user_id=users[0].user_id, isbn=books[0].isbn, book_rating=4)
    rating2 = Rating(user_id=users[1].user_id, isbn=books[0].isbn, book_rating=5)
    session.add_all([rating1, rating2])
    session.commit()

    assert books[0].get_book_statistics() == (2, 4.5, 0.5)

def test_user_statistics(session, users,books):

    assert users[2].get_user_statistics() == (0, None, None)

    rating1 = Rating(user_id=users[2].user_id, isbn=books[0].isbn, book_rating=4)
    rating2 = Rating(user_id=users[2].user_id, isbn=books[1].isbn, book_rating=5)
    session.add_all([rating1, rating2])
    session.commit()

    assert users[2].get_user_statistics() == (2, 4.5, 0.5)

def test_rating_statistics(session):

    mean, std_dev = Rating.get_ratings_statistics(session)
    assert mean == 4.5
    assert round(std_dev, 1) == 0.5

def test_create_loan(session,users,books):

    loan = Loan.create_loan(session,books[0].isbn, users[0].user_id)
    assert loan is not None
    assert loan.status == "active"

def test_return_loan(session,users,books ):

    loan = Loan.create_loan(session,books[1].isbn, users[1].user_id)
    result = Loan.return_book(session,books[1].isbn, users[1].user_id)
    assert result is True
    assert loan.status == "returned"