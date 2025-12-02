# 컬러 이미지의 가로를 절반으로 줄이고 세로를 3배로 늘려서 color_resize.jpg로 저장하고 화면에 띄우기

import cv2 as cv
import sys

img = cv.imread('C:/Users/asus/Downloads/dmu.jpg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

# print(img[0,0])
# print(img[0,0,1])

# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# gray_small = cv.resize(grad, dsize=(0,0), fx=0.5, fy=0.5)

img = cv.resize(img, dsize=(0,0), fx=0.2, fy=0.2)

resize_img = cv.resize(img, dsize=(0,0), fx=0.5, fy=3)

cv.imwrite('color_resize.jpg', resize_img)

cv.imshow('Image display', resize_img)

cv.waitKey()
cv.destroyAllWindows()


# 웹캠과 연결 시도, 결과를 cap 객체에 저장
# 웹캠이 하나이므로 웹캠 번호를 0으로 지정
# CAP_DSHOW : 웹캠 화면을 화면에 바로 표시
# cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap = cv.VideoCapture(0, cv.CAP_MSMF)

if not cap.isOpened():
    sys.exit("카메라 연결 실패")