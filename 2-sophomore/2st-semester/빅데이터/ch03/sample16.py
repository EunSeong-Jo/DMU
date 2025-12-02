#import copy
import copy

list_value_1 = ['1', '2', '3', '4']
list_value_2 = ['5', '6', '7', '8']

list_value_3 = list_value_1 + list_value_2

print(list_value_3)

print(id(list_value_1))
print(id(list_value_2))
print(id(list_value_3))

#list_value_1 = list_value_1 + list_value_2
#print(list_value_1)

#list_value_1.append(list_value_2)
list_value_1.extend(list_value_2)
print(list_value_1)


