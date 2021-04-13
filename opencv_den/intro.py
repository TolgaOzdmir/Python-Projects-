import cv2
import numpy as np
from matplotlib import pyplot as plt

# Opening image
img = cv2.imread("levha.jpg")

h, w = img.shape[:2]
print(h, w, img.shape)

roi = img[40:400, 150:420]
cv2.imshow("image", img)
cv2.waitKey(0)

cv2.imshow("image", roi)
cv2.waitKey(0)

new_h, new_w = 200, 200
ratio = new_h / w
dim = (new_w, int(h * ratio))
cv2.imshow("image", cv2.resize(img, dim))
cv2.waitKey(0)

# We are copying the original image,
# as it is an in-place operation.
output = img.copy()

# Using the rectangle() function to create a rectangle.
rectangle = cv2.rectangle(output, (100, 100),
                          (600, 200), (255, 0, 0), 2)
cv2.imshow("image", output)
cv2.waitKey(0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("image", img)
cv2.waitKey(0)

cv2.imwrite("gray.jpg", img)

cv2.destroyAllWindows()
