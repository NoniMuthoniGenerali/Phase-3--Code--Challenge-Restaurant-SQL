from sqlalchemy import create_engine, desc
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine('sqlite:///restaurant.db')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    #Table columns 
    id = Column(Integer(), primary_key = True)
    name = Column(String(25))
    price = Column(Integer())

    #Table relationships
    reviews = relationship("Review", back_populates='restaurant')
    customers = association_proxy('reviews', 'customer', 
                                  creator=lambda cus: Review(customer=cus))

    def __repr__(self):
        return f"Restaurant {self.id}: " \
            + f"{self.name} " \
            + f"Price {self.price}"

    @classmethod
    def fanciest(cls):
        restaurant = session.query(cls).order_by(desc(cls.price)).first()
        return restaurant

    def all_reviews(self):
        formatted_reviews = list()
        for review in self.reviews:
            #get customer first_name and last_name form customers table
            customer = session.query(Customer).get(review.customer_id) 
            formatted_review = f"Review for {self.name} by {customer.first_name} {customer.last_name}: {review.rating * '⭐'}"
            formatted_reviews.append(formatted_review)
        return formatted_reviews

class Customer(Base):
    __tablename__ = "customers"

    #Table columns
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(55))
    last_name = Column(String(55))
    #Table relationships
    reviews = relationship("Review", back_populates='customer')
    restaurants = association_proxy('reviews', 'restaurant',
                                    creator=lambda res: Review(restaurant=res))

    def __repr__(self):
        return f"Customer {self.id}: " \
            + f"{self.first_name} " \
            + f"{self.last_name}"
    
    #instance methods
    def full_name(self):
        return f"{self.first_name} {self.last_name}"    

    def favorite_restaurant(self):
        #sort reviews by rating in desc order
        def sort_by_rating(review):
            return review.rating
        sorted_reviews = sorted(self.reviews, key=sort_by_rating, reverse=True)
        #get the id of the first restaurant
        fav_restaurant_id = sorted_reviews[0].restaurant_id
        #loop thru customer reviewed restaurants and find fav_restaurant
        for restaurant in self.restaurants:
            if restaurant.id == fav_restaurant_id:
                return restaurant

    def add_review(self, restaurant, rating):
        review = Review(
            rating = rating,
            restaurant_id=restaurant.id,
            customer_id = self.id
        )
        #add and commit new review to the database
        session.add(review)
        session.commit()
        session.close()

    
    def delete_reviews(self, restaurant):
        #filter reviews relating to a particular customer and restaurant
        restaurant_reviews = session.query(Review).filter_by(customer_id = self.id, restaurant_id = restaurant.id).all()
        #loop thru the reviews and delete them
        for review in restaurant_reviews:
            session.delete(review)
            session.commit()
        session.close()


class Review(Base):
    __tablename__ = "reviews"

    #Table Columns
    id = Column(Integer(), primary_key=True)
    rating = Column(Integer())
    
    #relationship Columns
    restaurant_id = Column(Integer(), ForeignKey("restaurants.id"))
    customer_id = Column(Integer(), ForeignKey("customers.id"))

    #Table relations
    restaurant = relationship("Restaurant", back_populates = "reviews")
    customer = relationship("Customer",back_populates= "reviews")

    def __repr__(self):
        return f"Review( id={self.id}, " + \
        f"rating={self.rating}, " + \
        f"restaurant_id={self.restaurant_id}, " + \
        f"customer_id={self.customer_id})"
    

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.first_name} {self.customer.last_name}: {self.rating}"