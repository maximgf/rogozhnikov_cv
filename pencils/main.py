import cv2
from scipy.spatial import distance

count = 0
for img in range(1, 13):
    raw = cv2.imread(f"images/img ({img}).jpg")
    image = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (7, 7), 0)
    _, thresh = cv2.threshold(image, 120, 255, 0)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    countwo = count
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        points = cv2.boxPoints(cv2.minAreaRect(cnt))
        w_e = distance.euclidean(points[0], points[1])
        h_e = distance.euclidean(points[0], points[3])
        if (h_e > 3 * w_e and h_e > 1000) or (w_e > 3 * h_e and w_e > 1000):
            count += 1
    print(img,")",count - countwo)
print("Sum pencils:", count)
