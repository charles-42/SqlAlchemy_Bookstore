from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Book, Rating, User, Author, Loan


# # Session Creation
engine = create_engine('sqlite:///books.db')
Session = sessionmaker(bind=engine)
session = Session()

# # Vérifier le nombre de livre dans la base
# count = session.query(func.count(Book.isbn)).scalar()

# print(f"Le nombre de lignes dans la table book est: {count}")

# # Requête pour filtrer les livres dont le titre comporte "The Hobbit"
# books_with_hobbit = session.query(Book).filter(Book.book_title.like('%The Hobbit%')).all()

# # Affichage des résultats
# for book in books_with_hobbit:
#     print(book)


# # Obtenir les statistiques des notes
# Rating.get_ratings_statistics(session)


# # Obtenir les statistiques d'un utilisateur
# user_id = 276747  # Remplacez par l'ID de l'utilisateur dont vous voulez obtenir les statistiques
# user = session.get(User, user_id)
# if user:
#     user.get_user_statistics()    
# else:
#     print(f"L'utilisateur {user_id} n'existe pas.")

# # Obtenir les statistiques d'un livre
# isbn = '034545104X'  # Remplacez par l'ISBN du livre dont vous voulez obtenir les statistiques
# book = session.get(Book, isbn)
# if book:
#     print(book)
#     book.get_book_statistics()   
# else:
#     print(f"Le livre {isbn} n'existe pas.")

# # Obtenir les livres d'un auteur
# author_name = 'Jane Austen'  # Remplacez par l'ISBN du livre dont vous voulez obtenir les statistiques


# author = session.query(Author).filter(Author.author_name == author_name).first()
# if author:
#     books = author.get_books(session)
#     if books:
#         for book in books:
#             print(book)    
#     else:
#         print(f"{author_name} n'a pas de livres référencées dans la base")
# else:
#         print(f"{author_name} ne figure pas dans la base des auteurs")



# Créer un prêt
isbn = '0002005018'  # Remplacez par l'ISBN du livre
user_id_1 = 1  # Remplacez par l'ID de l'utilisateur
user_id_2 = 2  # Remplacez par l'ID de l'utilisateur

# Loan.create_loan(session, isbn, user_id_1)
# Loan.create_loan(session, isbn, user_id_2)

Loan.return_book(session, isbn, user_id_2)

Loan.create_loan(session, isbn, user_id_2)