import json
import cv2

filelist = json.load(open("./files/study.json"))

for filepath in filelist.keys():
    img = cv2.imread(filepath)
    orgWidth, orgHeight = img.shape[:2]
    size = (int(orgHeight/2), int(orgWidth/2))
    img = cv2.resize(img, size)
    cv2.imwrite(filepath,img)

filelist = json.load(open("./files/test.json"))

for filepath in filelist.keys():
    img = cv2.imread(filepath)
    orgWidth, orgHeight = img.shape[:2]
    size = (int(orgHeight/2), int(orgWidth/2))
    img = cv2.resize(img, size)
    cv2.imwrite(filepath,img)