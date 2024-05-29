from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Book, User, Rating
import csv


# # Session Creation
engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)
session = Session()

def import_books_from_csv(csv_file_path):
    print("Import Books")
    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        csvreader =  csv.DictReader(csvfile, delimiter=';', quotechar='"', escapechar='\\')
        for row in csvreader:
            book = Book(
                isbn=row['ISBN'],
                book_title=row['Book-Title'],
                book_author=row['Book-Author'],
                year_of_publication=int(row['Year-Of-Publication']),
                publisher=row['Publisher'],
                image_url_s=row['Image-URL-S'],
                image_url_m=row['Image-URL-M'],
                image_url_l=row['Image-URL-L']
            )
            session.add(book)
        session.commit()

def import_users_from_csv(csv_file_path):
    print("Import Users")
    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        csvreader =  csv.DictReader(csvfile, delimiter=';', quotechar='"', escapechar='\\')
        for row in csvreader:
            user = User(
                user_id=row['User-ID'],
                location=row['Location'],
                age=row['Age'],
            )
            session.add(user)
        session.commit()

def import_ratings_from_csv(csv_file_path):
    print("Import Ratings")
    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        csvreader =  csv.DictReader(csvfile, delimiter=';', quotechar='"', escapechar='\\')
        for row in csvreader:
            rating = Rating(
                user_id=row['User-ID'],
                isbn=row['ISBN'],
                book_rating=row['Book-Rating'],
            ) 
            session.add(rating)
        session.commit()

# Chemin vers le fichier CSV
# import_books_from_csv('data/books.csv')
# import_users_from_csv('data/users.csv')
import_ratings_from_csv('data/ratings.csv')

