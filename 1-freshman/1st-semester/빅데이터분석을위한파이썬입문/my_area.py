# ipynb 파일을 py 파일로 만들어줌

PI = 3.14

def square_area(a):
    return a ** 2

def circle_area(r):
    return PI * r ** 2

print('my_area')

print('__name__ : ', __name__)

# 주로 샘플코드 등을 넣어둠
if __name__ == '__main__':
    print('if를 통해 출력')