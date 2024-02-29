import os
import cv2
import numpy as np

# 240229 tif convert to bmp and resize for yolov5
def transformImage_FRcapsule(dir_data, dest_data, dir_data_format = ".tiff", dest_dat_format = ".bmp", img_size = 1280, new_img_width = 3200):
    # file format 정해야함
    list_files = os.listdir(dir_data)

    list_files_tif = [f for f in list_files if f.endswith(dir_data_format) if "luminance" in f]

    for file_tif in list_files_tif:
        filename = os.path.join(dir_data, file_tif)
        img = cv2.imread(filename)
        img_transform = (img / 1024 * 255).astype(np.float32) * 255
        img_h, img_w, img_c = img.shape
        print(f"image size {img_w} , {img_h}\t{file_tif}")
        new_img_h = int(img_h / img_w * img_size)
        img_transform = cv2.resize(img_transform, (img_size, new_img_h ))
        # img_transform = img_transform[0: img_size, 100: 100 + img_size]

        savename = os.path.join(dest_data, file_tif.replace(dir_data_format, dest_dat_format))
        cv2.imwrite(savename, img_transform)

# 240229 crop bmp image and save to destination
def cropImage_FRcapsule(dir_data, dest_data):
    list_files = os.listdir(dir_data)

    for file_tif in list_files:
        filename = os.path.join(dir_data, file_tif)
        img = cv2.imread(filename)

        filename_origin = file_tif.split(".")[0]
        savename = f""

        # 240229 img size   5000 ~ 7000
        #        transform  2000 ~ 3000
        img_h, img_w, img_c = img.shape
        if (img_h - 1280*2 < 1280):
            N = 3
        else:
            N = (int)((img_h - 1280*2)/(1280-200))  # crop margin

        if (N==3):
            crop_rect = []
            crop_rect.append((0,0, 1280,1280))
            crop_rect.append((0,1280-(int)((img_h - 1280*2 + 1280)/2), 1280,1280))
            crop_rect.append((0,img_h - 1280, 1280,1280))

        for i in range(N):
            savename = os.path.join(dest_data, f"{filename_origin}_{i}.bmp")
            new_img = img[ crop_rect[i][1]: crop_rect[i][1] + crop_rect[i][3],crop_rect[i][0]: crop_rect[i][0] + crop_rect[i][2],:]
            cv2.imwrite(savename, new_img)


def main():
    # tif convert to bmp for yolov5
    img_size = 1280

    dir_data = "G:\\data\\frcapsule\\240228\\ai_data"
    dest_data = "G:\\data\\frcapsule\\240228\\ai_data\\bmp"
    dest_data_1280 = "G:\\data\\frcapsule\\240228\\ai_data\\bmp_1280"

    # transformImage_FRcapsule(dir_data, dest_data)
    cropImage_FRcapsule(dest_data, dest_data_1280)

if __name__=="__main__":
    main()