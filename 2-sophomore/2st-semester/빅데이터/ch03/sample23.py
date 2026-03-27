
data = {
    'bgnde': '2025.03.01'
    , 'endde': '2025.03.01'
    , 'sj': '삼일절'
}
print(data)
print(type(data))
print(len(data))

print(data.keys())
print(type(data.keys()))

print('-'*30)
for key in data.keys():
    print(key)

print(data.values())
for value in data.values():
    print(value)

print('-'*30)
print(data.items())
for item in data.items():
    print(item)
    print(type(item))






