# ====================================================================
# 상욱님 코드
# ====================================================================
import xml.etree.ElementTree as ET
from os import listdir, getcwd
import os
import os.path
import glob
from pathlib import Path
from tqdm import tqdm
import shutil
# from FR_Capsule import TUtils, FR_Capsule

###################################################################
###     Setting     ###

xml_path = r'C:\git\Inspection_FRcapsule\data\20240215_FR_Capsule_rev3\images'
txt_path = xml_path + "/txt/"


INSPECTION_PART = FR_Capsule.FR_Capsule()

classes = INSPECTION_PART.classes


###################################################################

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
wd = getcwd()

def convert_annotation(xml, basename):
    result_path = txt_path + basename + ".txt"

    txt_file = open(result_path, 'w')

    tree=ET.parse(xml)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    object_exists = 0
    for obj in root.iter('object'):
        object_exists = 1
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)


        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)

        txt_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')



    txt_file.close()
    if object_exists == 0:
        print(basename)
        zero_result_path = zero_path + basename + ".txt"
        shutil.move(result_path, zero_result_path)




TUtils.MakeFolder(txt_path)

pbar = tqdm( glob.glob(os.path.join(xml_path, "*.xml")))

zero_path = txt_path  + "/zero/"
TUtils.MakeFolder(zero_path)
for xml_file in pbar:
    base_file_name = Path(xml_file).stem
    pbar.set_description("Processing ------------ %s    " %base_file_name   )


    convert_annotation(xml_file, base_file_name)


# Check 0 size txt
pbar = tqdm( glob.glob(os.path.join(txt_path, "*.txt")))

zero_file_list = []


for txt_file in pbar:
    size = os.path.getsize(txt_file)
    basename = Path(txt_file).stem

    if size == 0 :
        zero_file_list.append(basename)


if len(zero_file_list) == 0 :
    print("\n\nNone zero file. Convert Finish")
