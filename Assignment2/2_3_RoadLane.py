import cv2
import numpy as np
from matplotlib import pyplot as plt

file_name = "Lane.jpg"
read_path = r"C:\Users\Pannawit\Documents\GitHub\IoT__CU\Assignment2\Road\\" + file_name
image = cv2.imread(read_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

height, width = edges.shape
mask = np.zeros_like(edges)
trapezoid = np.array([[(width * 0.1, height), (width * 0.9, height), (width * 0.6, height * 0.6), (width * 0.4, height * 0.6)]])
cv2.fillPoly(mask, [trapezoid.astype(int)], 255)
masked_edges = cv2.bitwise_and(edges, mask)

lines = cv2.HoughLinesP(masked_edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=100, maxLineGap=160)
line_image = np.zeros_like(image)

left_lines = []
right_lines = []
for line in lines if lines is not None else []:
    x1, y1, x2, y2 = line[0]
    slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
    if 0.5 < abs(slope):
        if slope < 0:
            left_lines.append((x1, y1, x2, y2))
        else:
            right_lines.append((x1, y1, x2, y2))

if left_lines:
    left_line = np.average(left_lines, axis=0).astype(int)
    cv2.line(line_image, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (255, 0, 0), 5)

if right_lines:
    right_line = np.average(right_lines, axis=0).astype(int)
    cv2.line(line_image, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (255, 0, 0), 5)

combo = cv2.addWeighted(image_rgb, 0.8, line_image, 1, 1)

plt.figure(figsize=(10, 6))
plt.imshow(combo)
plt.title('Lane Detection')
plt.axis('off')
plt.show()