import cv2
import numpy as np

drawing = False         # 마우스 움직임 감지
points = []             # 마우스 클릭 지점 좌표를 저장하는 리스트
pt1 = (-1, -1)          # 타원의 중심 초기좌표
mode = "NULL"           # 1 또는 2 버튼을 누를 시 전환되는 모드 (1 : ellipse, 2 : polygon)
count = 1               # 파일 저장시 이미지 생성 순서



def cross_product(p1, p2, p3):
    # p1, p2, p3가 주어졌을 때, 두 벡터 (p2 - p1)과 (p3 - p2)의 외적을 구함.
    vector1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
    vector2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])

    # 외적 계산
    cross_product_value = np.cross(vector1, vector2)
    return cross_product_value



def ROI_export(event, x, y, param, flags):
    global title, pt1, drawing, points, mode, count

    if mode == "ellipse":
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True  # 드래그 허용
            pt1 = (x, y)  # 클릭 시 좌표 저장

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:  # 드래그가 허용된 동안 (왼쪽 버튼이 눌러진 상태) 타원을 그림
                ellipse_axes = ((x - pt1[0]) // 2, (y - pt1[1]) // 2)                   # 마우스의 현재 위치의 좌표와 처음 찍은 좌표의 차이가 타원의 장축, 단축이 된다.
                ellipse_center = (ellipse_axes[0] + pt1[0], ellipse_axes[1] + pt1[1])   # 처음 좌표에서 ellipse_axes 만큼 더한 값이 타원의 중심이 된다.
                tmp = ellipse_image.copy()  # 마우스가 움직일 때 마다 복사 이미지 생성
                cv2.ellipse(tmp, ellipse_center, ellipse_axes, 0, 0, 360, (255, 0, 0), 1) # 복사된 이미지에 타원 생성
                cv2.imshow(title, tmp) # 마우스의 움직임에 따라 타원이 그려짐

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False  # 드래그 거부
            cv2.imshow(title, ellipse_image)  # 버튼을 뗄시 현재 마우스의 좌표까지의 타원이 그려짐

            mask = np.zeros_like(image)     # mask 이미지 생성

            ellipse_axes = ((x - pt1[0]) // 2, (y - pt1[1]) // 2)
            ellipse_center = (ellipse_axes[0] + pt1[0], ellipse_axes[1] + pt1[1])

            cv2.ellipse(mask, ellipse_center, ellipse_axes, 0, 0, 360, (255, 255, 255), thickness=-1)       # mask 이미지에 타원 삽입
            result = cv2.bitwise_and(image, mask)           # result에 원본 이미지와 mask 이미지 중 겹치는 부분 추출
            cv2.imwrite(f"noh{count:04d}.jpg", result)       # 파일로 저장
            count += 1      # 카운트 증가



    elif mode == "polygon":
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) > 1 and abs(points[0][0] - x) < 20 and abs(points[0][1] - y) < 20:  # 처음 찍은 점의 거리 20 미만인 점은 처음 점에 찍히도록 하는 함수
                if len(points) >= 3:
                    # 점을 3개 이상 찍었을 경우 다각형을 닫게 하기 위함
                    points.append(points[0])
                    cv2.imshow(title, polygon_image)
            else:
                if len(points) >= 2:  # 점 두개 이상 찍혔고, 세번째 점을 찍을 때 부터 마지막에 찍힌 세 점의 외적을 계산함
                    if cross_product(points[-2], points[-1],
                                     (x, y)) > 0:  # 외적 계산 값이 음수일 경우 점이 찍히고 양수일 경우 찍히지 않는다. 점은 시계 반대 방향으로 찍힌다.
                        return

                # 처음 점 주변에 찍지 않은 경우 points에 점 저장
                points.append([x, y])

            for point in points:
                # 마우스 클릭시 점을 찍는다.
                cv2.circle(polygon_image, (point[0], point[1]), 2, (0, 0, 255), thickness=-1)
            if len(points) > 1:
                # 점이 두개 이상 찍힐 때 부터 선을 긋는다.
                cv2.polylines(polygon_image, [np.array(points)], False, (0, 255, 0), thickness=1)
                if len(points) > 3 and points[0] == points[-1]:
                    # points에 4개 이상의 점이 들어 있어야 다각형이 완성된다. (처음 찍힌 점과 마지막 찍힌 점이 같기 때문에)

                    mask = np.zeros_like(image) # mask 이미지 생성
                    cv2.fillPoly(mask, [np.array(points)], (255, 255, 255)) # mask 이미지에 다각형 삽입
                    result = cv2.bitwise_and(image, mask) # result에 원본 이미지와 mask 이미지 중 겹치는 부분 추출
                    cv2.imwrite(f"noh{count:04d}.jpg", result) # 파일로 저장
                    count += 1 # 카운트 증가

                    points.clear()          # 다각형이 완성되면 points리스트를 초기화 하여 다음 다각형을 만들 수 있도록 한다.

        cv2.imshow(title, polygon_image)



image = cv2.imread('input.jpg')
image = cv2.resize(image, (640, 480))


title = "ROI_export"
cv2.imshow(title, image)
cv2.setMouseCallback(title, ROI_export)


while True:
    key = cv2.waitKeyEx(1)

    if key == (27):     # ESC를 눌러 종료
        break
    elif key == ord('1'):   # 1 버튼을 눌러 타원 모드 진입 // 다시 누를 시 None 모드
        if mode == "ellipse":
            mode = "NULL"
        else:
            mode = "ellipse"
            ellipse_image = image.copy()
            tmp = ellipse_image.copy()  # 타원이 그려질 때 마다 복사된 image에 저장
            cv2.putText(ellipse_image, f"{mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if drawing == True:
                cv2.imshow(title, tmp)
            elif drawing == False:
                cv2.imshow(title, ellipse_image)
    elif key == ord('2'):   # 2 버튼을 눌러 다각형 모드 진입 // 다시 누를 시 None 모드
        if mode == "polygon":
            mode = "NULL"
        else:
            mode = "polygon"
            polygon_image = image.copy()
            cv2.putText(polygon_image, f"{mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow(title, polygon_image)
    elif mode == "NULL":
        nullimage = image.copy()
        cv2.putText(nullimage, "NULL", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow(title, nullimage)

cv2.destroyAllWindows()