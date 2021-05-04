
from food_ordering_service import FoodService, Gender

service = FoodService()
service.register_user('a', 987654321, 117211, Gender.MALE)
print("user registered")

service.register_user('b', 985654321, 123456, Gender.MALE)
print("user registered")

service.register_user('c', 945654321, 654321, Gender.MALE)
print("user registered")

service.register_restaurant('x', [117211, 123456], 'dish', 100, 5)
print("restarant reg")

service.register_restaurant('y', [123456, 654321], "burger", 120, 3)
print("restarant reg")


service.switch_user(987654321)
print("switched")
service.place_order('x', 2)


service.switch_user(985654321)
print("switched")
service.place_order('x', 6)

service.restaurants['x'].add_quantity(2)
print("qty added")

service.switch_user(987654321)
print("switched")
service.place_order('x', 5)

service.switch_user(985654321)
print("switched")
service.get_restaurants_for_user("price")

service.switch_user(987654321)
print("switched")

service.take_review('x', 5, 'dfdf')


service.restaurants['x'].show_reviews()


print("------")
