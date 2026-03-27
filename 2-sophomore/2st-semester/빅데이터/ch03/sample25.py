
data = {
    'bgnde'
    , 'endde'
    , 'sj'
}

print(data)
print(type(data))

data.add('title')
data.add('desc')
data.add('sj')

print(data)
print(type(data))

'''
data.remove('sj')
print(data)

if 'sj' in data:
    data.remove('sj')
else:
    print('sj 데이터 없음')

print(data)
'''

data.discard('sj')
data.discard('sj')
data.discard('sj')

print(data)




