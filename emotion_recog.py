# -*- coding: utf-8 -*-

import httplib
import urllib
import base64
import os
import sys
import cv2
import numpy as np
import json
import math

def get_emotion(file_path, headers):
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/emotion/v1.0/recognize?",
                     open(file_path, 'rb'), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print(e.message)

def display_expression(data,img):
    font = cv2.FONT_HERSHEY_PLAIN
    text = "test cyber"
    font_size = 1
    data = json.loads(data)
    for face in data:
        f_rec  =  face['faceRectangle']
        width  =  f_rec['width']
        height =  f_rec['height']
        left   =  f_rec['left']
        top    =  f_rec['top']
        f_rec  =  face['scores']
        f_rec = sorted(f_rec.items(), key=lambda x:x[1],reverse = True)
        cv2.rectangle(img,(left,top),(left+width,top+height),(130,130,130),2)
        cv2.rectangle(img,(left+width,top),(left+width+150,top+50),(130,130,130),-1)

        for i in range(0,5):
            val = round(f_rec[i][1],3)
            emo = f_rec[i][0]
            cv2.rectangle(img,(left+width,top+10*i),(left+width+int(val*150),top+10*(i+1)),(180,180,180),-1)
            cv2.putText(img, emo+" "+str(val),(left+width,top+10*(i+1)),font, font_size,(255,255,255),1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: # python %s /path/to/image' % sys.argv[0]
        quit()

    with open('api_key.txt', 'r') as f:
        key = f.read().rstrip('\n')
    f.close()
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': key,
    }

    data = get_emotion(sys.argv[1], headers)
    img = cv2.imread(sys.argv[1],-1)

    display_expression(data,img)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
