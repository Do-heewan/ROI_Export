import numpy as np
import cv2

drawing = False
pt1 = (-1, -1)

def onMouse_ellipse(event, x, y, flags, param):    # 타원 그리는 함수
    global title, pt1, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True  # 드래그 허용
        pt1 = (x, y)    # 클릭 시 좌표 저장

    elif event == cv2.EVENT_MOUSEMOVE:
        if (drawing==True): # 드래그가 허용된 동안 (왼쪽 버튼이 눌러진 상태) 타원을 그림
            ellipse_center = ((x - pt1[0]) // 2 + pt1[0], (y - pt1[1]) // 2 + pt1[1])
            ellipse_axes = ((x - pt1[0]) // 2, (y - pt1[1]) // 2)
            tmp = image.copy()  # 타원이 그려질 때 마다 복사된 image에 저장
            cv2.ellipse(tmp, ellipse_center, ellipse_axes, 0, 0, 360, (255, 0, 0), 1)
            cv2.imshow(title, tmp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False # 드래그 거부
        ellipse_center = ((x - pt1[0]) // 2 + pt1[0], (y - pt1[1]) // 2 + pt1[1])
        ellipse_axes = ((x - pt1[0]) // 2, (y - pt1[1]) // 2)
        cv2.ellipse(image, ellipse_center, ellipse_axes, 0, 0, 360, (0, 255, 0), 2)
        cv2.imshow(title, image)    # 버튼을 뗄시 현재 마우스의 좌표까지의 타원이 그려짐

image = cv2.imread('input.jpg')
image = cv2.resize(image, (640, 480))



title = "ellipse Test"
cv2.imshow(title, image)
cv2.setMouseCallback(title, onMouse_ellipse)
cv2.waitKey(0)