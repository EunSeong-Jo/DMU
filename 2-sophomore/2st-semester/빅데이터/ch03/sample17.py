
tuple_value = ('1', '2', '3', '4')
list_value = ['5', '6', '7', '8']

print(type(list_value))
print(type(tuple_value))

tuple_to_list = list(tuple_value)
list_to_tuple = tuple(list_value)

print(type(list_to_tuple))
print(type(tuple_to_list))

