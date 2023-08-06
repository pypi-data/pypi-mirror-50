

import cv2
import numpy as np
from PIL import Image

# img_path = "../day01/robot2.jpg"
# im = Image.open(img_path)
# print(type(im))
# for i in im:
#     print(i)
# img_data = cv2.imread(img_path)
# print(type(img_data))


# target_size=(331,331,3)

img_data = np.linspace(0, 255, 331*331*3).reshape( 331,331,3).astype(np.uint8)
print(type(img_data))
for i in img_data:
    print(i)
# cv2.imwrite("img.jpg",img_data) # 在当前目录下会生成一张img.jpg的图片


#

# img = image.load_img('./006315.jpg', target_size=(331,331,3))
# img = image.img_to_array(img)
# img = img/255
# s = ""
# img.reshape(1, 331, 331, 3)


