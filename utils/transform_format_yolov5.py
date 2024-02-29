import os
import cv2
import numpy as np

# tif convert to bmp for yolov5
img_size = 1280

dir_data = "G:\\data\\frcapsule\\240228\\ai_data"
dest_data = "G:\\data\\frcapsule\\240228\\ai_data\\bmp"

list_files = os.listdir(dir_data)

list_files_tif = [f for f in list_files if f.endswith(".tiff")]

for file_tif in list_files_tif:
    filename = os.path.join(dir_data, file_tif)
    img = cv2.imread(filename)
    img_transform = (img / 1024 * 255).astype(np.float32) * 255
    img_transform = cv2.resize(img_transform, (2048, img_size))
    img_transform = img_transform[0: img_size, 100: 100 + img_size]

    savename = os.path.join(dest_data, file_tif.replace("tiff", "bmp"))
    cv2.imwrite(savename, img_transform)


