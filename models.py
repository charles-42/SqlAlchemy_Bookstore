from sqlalchemy import Column, Integer, String, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship 
from datetime import datetime
import math


Base = declarative_base()


class Book(Base):
    __tablename__ = 'Books'
    isbn = Column(String, primary_key=True)
    book_title = Column(String, nullable=False)
    book_author = Column(String, nullable=False)
    year_of_publication = Column(Integer, nullable=False)
    publisher = Column(String, nullable=False)
    image_url_s = Column(String)
    image_url_m = Column(String)
    image_url_l = Column(String)

    ratings = relationship("Rating", back_populates="book")

    def get_book_statistics(self):
        ratings_list = [rating.book_rating for rating in self.ratings]
        if ratings_list:
            count_ratings = len(ratings_list)
            mean_rating = sum(ratings_list) / count_ratings
            variance = sum((x - mean_rating) ** 2 for x in ratings_list) / count_ratings
            std_dev_rating = math.sqrt(variance)
            
            print(f"Le livre {self.isbn} a reçu {count_ratings} notes.")
            print(f"La moyenne des notes est : {round(mean_rating,1)}")
            print(f"L'écart type des notes est : {round(std_dev_rating,1)}")
        
            return count_ratings, mean_rating, std_dev_rating
        
        print(f"Le livre {self.isbn} n'a reçu aucune note.")
        return 0, None, None

    def __repr__(self):
        return f"{self.book_title}[{self.book_author}]({self.year_of_publication})"


class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    location = Column(String, nullable=True)
    age = Column( Integer, nullable=True)

    ratings = relationship("Rating", back_populates="user")

    def get_user_statistics(self):
        
        # # Code sans relation:
        # user_ratings = session.query(Rating).filter(Rating.user_id == self.user_id).all()
        # ratings_list = [rating.book_rating for rating in user_ratings]

        # Code avec relation:
        ratings_list = [rating.book_rating for rating in self.ratings]

        if ratings_list:
            count_ratings = len(ratings_list)
            mean_rating = sum(ratings_list) / count_ratings
            variance = sum((x - mean_rating) ** 2 for x in ratings_list) / count_ratings
            std_dev_rating = math.sqrt(variance)
            print(f"L'utilisateur {self.user_id} a donné {count_ratings} notes.")
            print(f"La moyenne des notes est : {round(mean_rating,1)}")
            print(f"L'écart type des notes est : {round(std_dev_rating,1)}")
            return count_ratings, mean_rating, std_dev_rating
        
        print(f"L'utilisateur {self.user_id} n'a donné aucune note.")
        return 0, None, None

    def __repr__(self):
        return f"User-ID: {self.user_id}, Location: {self.location}, Age: {self.age}"

# Définition de la classe Rating
class Rating(Base):
    __tablename__ = 'Ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    isbn = Column(String, ForeignKey('Books.isbn'))
    book_rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")

    def __repr__(self):
        return f"User-ID: {self.user_id}, ISBN: {self.isbn}, Book-Rating: {self.book_rating}"

    @classmethod
    def get_ratings_statistics(cls, session):
        ratings = session.query(cls.book_rating).all()
        ratings_list = [rating[0] for rating in ratings]
        if ratings_list:
            mean_rating = sum(ratings_list) / len(ratings_list)
            variance = sum((x - mean_rating) ** 2 for x in ratings_list) / len(ratings_list)
            std_dev_rating = math.sqrt(variance)
            print(f"La moyenne des notes est : {round(mean_rating,1)}")
            print(f"L'écart type des notes est : {round(std_dev_rating,1)}")
            return mean_rating, std_dev_rating
        print("Aucune note disponible pour le calcul des statistiques.")
        return None, None
    
class Author(Base):
    __tablename__ = 'Authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
    death_year = Column(Integer, nullable=True)
    nationality = Column(String, nullable=False)

    def get_books(self, session):
        return session.query(Book).filter(Book.book_author == self.author_name).all()

    def __repr__(self):
        return f"{self.author_name} ({self.birth_year} - {self.death_year}), Nationality: {self.nationality}"

class Loan(Base):
    __tablename__ = 'Loans'
    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String, ForeignKey('Books.isbn'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")

    # book = relationship("Book", back_populates="loans")
    # user = relationship("User", back_populates="loans")

    def __repr__(self):
        return f"Loan {self.loan_id}: Book {self.isbn} to User {self.user_id} on {self.start_date}"

    @classmethod
    def create_loan(cls, session, isbn, user_id):
        # Check if the book is available (no active loan)
        active_loan = session.query(Loan).filter_by(isbn=isbn, status="active").first()
        if active_loan:
            print(f"Book {isbn} is not available.")
            return None
        
        # Check if the user has more than 5 loans (active)
        active_loans_count = session.query(Loan).filter_by(user_id=user_id, status="active").count()
        if active_loans_count >= 5:
            print(f"User {user_id} has already 5 active loans.")
            return None

        # Create a new loan
        new_loan = cls(isbn=isbn, user_id=user_id)
        session.add(new_loan)
        session.commit()
        print(f"Loan created: {new_loan}")
        return new_loan

    @classmethod
    def return_book(cls,session, isbn, user_id):
        # Find the loan
        loan = session.query(cls).filter_by(isbn=isbn,user_id=user_id, status="active").first()
        if loan:
            # Update the loan status and end_date
            loan.status = "returned"
            loan.end_date = datetime.now()

            session.commit()
            print(f"Book {isbn} returned by User {user_id}")
            return True
        print(f"Loan not found or already returned.")
        return False


if __name__ == "__main__":
    # Configuration de la base de données
    engine = create_engine('sqlite:///books.db')
    Base.metadata.create_all(engine)    

