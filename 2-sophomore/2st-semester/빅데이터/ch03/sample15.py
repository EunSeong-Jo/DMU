#import copy
import copy

list_value = ['1', '2', '3', '4', '5', '6', '7', '8']

new_value = list_value[::]

print(list_value)
print(new_value)

list_value[0] = '11'

print('-'*30)
print(list_value)
print(new_value)

print('='*30)
#------------------------------------------------------
list_value = [['1', '2'], ['3', '4'], ['5', '6'], ['7', '8']]

#new_value = list_value[::]
new_value = copy.deepcopy(list_value)

print(list_value)
print(new_value)

list_value[0][0] = '11'

print('-'*30)
print(list_value)
print(new_value)

del new_value

print(new_value)
