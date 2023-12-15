class Restaurant:
    def __init__(self, name):
        self.name = name
        self.reviews = []

    def add_review(self, customer, rating, Review):
        review = Review(customer, self, rating)
        self.reviews.append(review)

    def all_reviews(self):
        return self.reviews

    def customers(self):
        unique_customers = set()
        for review in self.reviews:
            unique_customers.add(review.customer())
        return list(unique_customers)
    

class Customer:
    def __init__(self, given_name, family_name):
        self.given_name = given_name
        self.family_name = family_name
        self.reviews = []

    def add_review(self, restaurant, rating, Review):
        review = Review(self, restaurant, rating)
        self.reviews.append(review)
        restaurant.add_review(self, rating)

    def restaurants(self):
        unique_restaurants = set()
        for review in self.reviews:
            unique_restaurants.add(review.restaurant())
        return list(unique_restaurants)