"""1. show ratings of user
2. update locationb
3. show user details
"""
from enum import Enum
from collections import defaultdict


class FoodServiceException(Exception):
    pass


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class FoodService:
    def __init__(self):
        self.users = {}
        self.restaurants = {}
        self.active_user = None
        self.pincodes = defaultdict(list)

    @staticmethod
    def _check_inputs(pincode: int, mobile: int = None) -> None:
        if (mobile
            and (mobile < 0
                 or mobile/100000000 < 9)):
            raise FoodServiceException("Invalid mobile number.")

        if pincode/10000 < 6:
            raise FoodServiceException("Invalid pincode")

    def get_restaurants_for_user(self, criteria: str) -> None:
        candidates = self.pincodes.get(
            self.active_user.pincode)  # Enforce input checking
        if criteria == 'rating':
            candidates.sort(key=lambda cand: cand.avg_rating)

        if criteria == 'price':
            candidates.sort(key=lambda cand: cand.dish_price)

        candidate_names = [candidate.name for candidate in candidates]
        candidate_names.reverse()
        print(candidate_names)

    def place_order(self,
                    restaurant: str,
                    quantity: int):
        try:
            restaurant = self.restaurants.get(restaurant)

            if not restaurant:
                raise FoodServiceException("Invalid restaurant.")
            if not self.active_user:
                raise FoodServiceException("There is no active user.")

            self.active_user._register_order(restaurant, quantity)
        except FoodServiceException as error:
            print(error)

    def register_user(self,
                      name: str,
                      mobile: int,
                      pincode: int,
                      gender: Gender = None):
        try:
            FoodService._check_inputs(pincode, mobile)
            if mobile in self.users:
                raise FoodServiceException("This user already exists.")
            self.users[mobile] = User(name, mobile, pincode, gender)
        except FoodServiceException as error:
            print(error)

    def register_restaurant(self,
                            name: str,
                            pincodes: set,
                            dish_name: int,
                            dish_price: int,
                            quantity: int = 0):
        try:
            for pincode in pincodes:
                FoodService._check_inputs(pincode)

            if name in self.restaurants:
                # This is not a rigorous check, better check would be restaurant ID
                raise FoodServiceException("This Restaurant already exists.")
            restaurant = Restaurant(
                name, pincodes, dish_name, dish_price, quantity)
            self.restaurants[name] = restaurant

            for pincode in pincodes:
                self.pincodes[pincode].append(restaurant)
        except FoodServiceException as error:
            print(error)

    def switch_user(self, mobile):
        try:
            user = self.users.get(mobile)
            if not user:
                raise FoodServiceException(
                    "This mobile hasn't been registered.")
            self.active_user = user
        except FoodServiceException as error:
            print(error)

    def take_review(self,
                    restaurant: str,
                    rating: int,
                    comment: str = None):
        try:
            restaurant = self.restaurants.get(restaurant)
            if not restaurant:
                # This is not a rigorous check, better check would be restaurant ID
                raise FoodServiceException("This Restaurant doesn't exist.")
            self.active_user.give_review(restaurant, rating, comment)
        except FoodServiceException as error:
            print(error)


class User:
    def __init__(self,
                 name: str,
                 mobile: int,
                 pincode: int,
                 gender: Gender = None):

        self.name = name
        self.gender = gender
        self.mobile = mobile
        self.pincode = pincode
        self.reviews = []
        self.orders = []

    def show_details(self):
        print(self.__dict__)  # ask whether we want to print or return

    def _register_order(self, restaurant, quantity: int) -> None:
        if quantity < 0:
            raise FoodServiceException("invalid quantity. Order not placed.")
        if quantity > restaurant.quantity:
            raise FoodServiceException(
                "Insufficient quantity. Order not placed.")
        if self.pincode not in restaurant.pincodes:
            raise FoodServiceException(
                "This restaurant doesn't deliver here. Order not placed.")

        restaurant.quantity -= quantity
        self.orders.append((restaurant.name, restaurant.dish_name, quantity))
        print("Order placed successfully")

    def give_review(self,
                    restaurant,
                    rating: int,
                    comment: str = None):
        if rating < 0 or rating > 5:
            raise FoodServiceException("Invalid rating.")
        if self.pincode not in restaurant.pincodes:
            raise FoodServiceException(
                "You cannot order from or rate this restaurant.")
        review = (rating, comment)
        restaurant.update_review(review)
        self.reviews.append(review)


class Restaurant:
    #check pincodes validity
    def __init__(self,
                 name: str,
                 pincodes: set,
                 dish_name: int,
                 dish_price: int,
                 quantity: int = 0):
        self.name = name
        self.dish_name = dish_name,
        self.dish_price = dish_price,
        self.quantity = quantity
        self.pincodes = pincodes
        self.reviews = []
        self.avg_rating = 0

    def add_quantity(self, quantity: int) -> None:
        self.quantity += quantity

    def show_reviews(self) -> None:
        print(self.reviews)

    def update_review(self, review):
        self.reviews.append(review)
        ratings = [element[0] for element in self.reviews]
        self.avg_rating = (sum(ratings)
                           / float(len(ratings)))
