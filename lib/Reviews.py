from Customer import Customer
class Review:
    all_reviews = []

    def __init__(self, customer, restaurant, rating):
        self._customer = customer
        self._restaurant = restaurant
        self.rating = rating
        Review.all_reviews.append(self)

    def customer(self):
        return self._customer

    def restaurant(self):
        return self._restaurant

    @classmethod
    def all(cls):
        return cls.all_reviews

# creating some restuarant and customer instances
customer1 = Customer("Wallahi", "Billahi")
customer2 = Customer("Nana", "Mkubwa")
restaurant1 = "Restaurant Yetu"
restaurant2 = "Restaurant Bismilah"

# creating some reviews
review1 = Review(customer1, restaurant1, 4.7)
review2 = Review(customer2, restaurant2, 2.8)

# testing instance methods
print(review1.customer())  # Output: 
print(review1.restaurant())  # 

# Test class method
all_reviews = Review.all()
for review in all_reviews:
    print(review.customer().get_full_name(), review.restaurant(), review.rating)

# output : Wallahi Billahi - Restuarant Yetu 4.7
          # Nana Mkubwa - Restuarant  Bismillah 2.8