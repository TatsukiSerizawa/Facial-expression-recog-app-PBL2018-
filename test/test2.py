#coding: utf-8
import cv2
import cognitive_face as CF
import requests
import sys
import signal
import os
import requests
from time import sleep
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

KEY = ''
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0'
CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

def getRectangle(faceDictionary):
	rect = faceDictionary['faceRectangle']
	left = rect['left']
	top = rect['top']
	right = left + rect['height']
	bottom = top + rect['width']
	return ((left, top), (right, bottom))

def draw(img_url,faces):
	with open(img_url, 'rb') as f:
		binary = f.read()
	img = Image.open(BytesIO(binary))
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',40)
	for face in faces:
		pos = getRectangle(face)
		text = face['faceAttributes']['gender']+'/'+str(face['faceAttributes']['age'])
		if face['faceAttributes']['gender'] == 'male':
			draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+220,pos[1][1]+40), fill='#fff', outline='#fff')
			draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='blue')
		elif face['faceAttributes']['gender'] == 'female':
			draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+260,pos[1][1]+40), fill='#fff', outline='#fff')
			draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='red')
	img.save(img_url, quality=95)

if __name__ == '__main__':
	ESC_KEY = 27
	ENTER_KEY = 13
	INTERVAL= 33
	FRAME_RATE = 30
	ORG_WINDOW_NAME = "org"
	DEVICE_ID = 0
	cascade_file = '/home/tatsuki/anaconda3/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml'
	cascade = cv2.CascadeClassifier(cascade_file)

	cap = cv2.VideoCapture(DEVICE_ID)
	end_flag, c_frame = cap.read()
	height, width, channels = c_frame.shape
	cv2.namedWindow(ORG_WINDOW_NAME)

	while end_flag == True:
		img = c_frame
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))
		for (x, y, w, h) in face_list:
			color = (0, 0, 225)
			pen_w = 3
			cv2.rectangle(c_frame, (x, y), (x+w, y+h), color, thickness = pen_w)
		cv2.imshow(ORG_WINDOW_NAME, c_frame)

		key = cv2.waitKey(INTERVAL)
		if key == ESC_KEY:
			break
		elif key == ENTER_KEY:
			img_url = 'photo.png'
			cv2.imwrite(img_url, c_frame)
			faces = CF.face.detect(img_url, face_id=True, landmarks=False, attributes='age,gender')
			if len(faces)==0:
				print('顔を認識できませんでした')
			else:
				draw(img_url,faces)
				im = cv2.imread(img_url)
				cv2.imshow('face', im)
				cv2.waitKey(0)
				cv2.destroyAllWindows()
		end_flag, c_frame = cap.read()

	cv2.destroyAllWindows()
    #cap.release()