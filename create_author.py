# Importer les classes et créer une session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Book, Author
from faker import Faker
import random

# Session Creation
engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)
session = Session()

# Utiliser Faker pour générer des données fictives
faker = Faker()

# Lister tous les auteurs distincts (en ignorant majuscules, minuscules et espaces)
authors = session.query(Book.book_author).distinct().all()

# Générer des dates de naissance entre 1800 et 2000
def generate_birth_year():
    return random.randint(1800, 2000)

# Générer des dates de décès basées sur les conditions
def generate_death_year(birth_year):
    current_year = 2024
    death_year = random.randint(birth_year+20, min(birth_year + 100, current_year))
    return death_year if death_year <= current_year else None


# Insérer les auteurs dans la table `Author`
for author in authors:
    
    birth_year=generate_birth_year()

    new_author = Author(
        author_name=author[0],
        birth_year=birth_year,
        death_year=generate_death_year(birth_year),
        nationality=faker.country()
    )
    session.add(new_author)

session.commit()

print("Authors inserted into the Authors table.")
