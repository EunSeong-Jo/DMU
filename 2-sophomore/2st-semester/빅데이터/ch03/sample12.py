
my_book = (2010, 'C언어', 300)
your_book = [2010, '자바', 200]

print(my_book)
print(your_book)

#튜플과리스트 차이
#데이터변경이슈

print('-'*30)
your_book[0] = 2025
your_book.append('자바책입니다.')
your_book.insert(1, '1교시')
#your_book.remove('자바')

print(your_book)
