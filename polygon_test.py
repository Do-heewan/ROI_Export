import numpy as np
import cv2

points = []     # points 리스트를 만들어 마우스로 점을 찍을때 마다 저장

def cross_product(p1, p2, p3):
    # p1, p2, p3가 주어졌을 때, 두 벡터 (p2 - p1)과 (p3 - p2)의 외적을 구함.
    vector1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
    vector2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])

    # 외적 계산
    cross_product_value = np.cross(vector1, vector2)
    return cross_product_value

def onMouse_polygon(event, x, y, flags, param):
    global title, points

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) > 1 and abs(points[0][0] - x) < 20 and abs(points[0][1] - y) < 20:      # 처음 찍은 점의 거리 20 미만인 점은 처음 점에 찍히도록 하는 함수
            if len(points) >= 3:
                # 점을 3개 이상 찍었을 경우 다각형을 닫게 하기 위함
                points.append(points[0])
                cv2.imshow(title, image)
            else:
                print("다각형을 완성하려면 최소 3개의 점이 필요합니다.")
        else:
            if len(points) >= 2: # 점 두개 이상 찍혔고, 세번째 점을 찍을 때 부터 마지막에 찍힌 세 점의 외적을 계산함
                if cross_product(points[-2], points[-1], (x, y)) > 0: # 외적 계산 값이 음수일 경우 점이 찍히고 양수일 경우 찍히지 않는다. 점은 시계 반대 방향으로 찍힌다.
                    print("내각이 180도를 넘습니다. 점을 추가할 수 없습니다.")
                    return

            # 처음 점 주변에 찍지 않은 경우 points에 점 저장
            points.append([x, y])

        for point in points:
            # 마우스 클릭시 점을 찍는다.
            cv2.circle(image, (point[0], point[1]), 2, (0, 0, 255), thickness=-1)
        if len(points) > 1:
            # 점이 두개 이상 찍힐 때 부터 선을 긋는다. (다각형을 만든다.)
            cv2.polylines(image, [np.array(points)], False, (0, 255, 0), thickness=1)
            if len(points) > 3 and points[0] == points[-1]:
                #다각형이 완성되면 points리스트를 초기화 하여 다음 다각형을 만들 수 있도록 한다.
                points.clear()

        cv2.imshow(title, image)
        clone = image.copy()

image = cv2.imread('input.jpg')
image = cv2.resize(image, (640, 480))

title = "polygon Test"
cv2.imshow(title, image)
cv2.setMouseCallback(title, onMouse_polygon)
cv2.waitKey(0)