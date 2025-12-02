
my_book = (2010, 'C언어', 300, '1교시')
your_book = [2010, '자바', 200, '2교시']
#            0,     1,     2,    3
#new_book = [your_book[1], your_book[2]]
#new_book = your_book[1:4]
#new_book = your_book[:4]
#new_book = your_book[1:]

#new_book = your_book[-1:]
#new_book = your_book[len(your_book) - 1]

#new_book = your_book[-2:]
new_book = your_book[:]

print(my_book)
print(your_book)
print(new_book)

print(id(my_book))
print(id(your_book))
print(id(new_book))




