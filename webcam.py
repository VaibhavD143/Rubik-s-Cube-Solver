from image_processing import *
import numpy as np
import cv2
from color_resolver import *


class scan_cube(object):
		
	def __init__(self):
		self.inst = {
		'enter_to_cap': "Press 'spacebar' to capture image",
		'front': "'blue' center in front and 'red' center on top",
		'back' : "'green' center in front and 'red' center on top",
		'up': "'red' center in front and 'green' center on top",
		'left': "'yellow' center in front and 'red' on top",
		'right' : "'white' in front and 'red' on top",
		'down' : "'orange' center in front and 'blue' on top",
		'error' : "Coudn't scan image please try again!"
		}		
		self.faces = ['front']#,'back','left','right','up','down']
	
	def capture_frame(self,face_name):
		
		if face_name not in self.faces:
			return False
		cap = cv2.VideoCapture(0)
		cv2.namedWindow("output",cv2.WINDOW_NORMAL)
		cv2.resizeWindow("output",1000,1000)
		cap_msg = self.inst['enter_to_cap']
		face_msg = self.inst[face_name]
		index = 0
		name = face_name+".jpg"
		debug = False
		rimg = None
		color1 = color2 = (255,255,255)
		flag = 0
		while(True):
			ret, frame = cap.read()

			# show innstruction to click
			font = cv2.FONT_HERSHEY_SIMPLEX
			text = cap_msg
			textsize = cv2.getTextSize(text, font, 1, 2)[0]
			textX = (frame.shape[1] - textsize[0]) / 2
			textY = 30
			cv2.putText(frame, text, (int(textX), int(textY) ), font, 1, (255, 255, 255), 3, cv2.FILLED)
			#show which face to scan instruction
			text = face_msg
			textsize = cv2.getTextSize(text, font, 0.5, 2)[0]
			textX = (frame.shape[1] - textsize[0]) / 2
			textY = frame.shape[0]-20
			cv2.putText(frame, text, (int(textX), int(textY) ), font, 0.5, color2, 2, cv2.LINE_4)

			if flag:
				text = self.inst['error']
				textsize = cv2.getTextSize(text, font, 0.5, 2)[0]
				textX = (frame.shape[1] - textsize[0]) / 2
				textY = frame.shape[0]-40
				cv2.putText(frame, text, (int(textX), int(textY) ), font, 0.5, (0,0,255), 2, cv2.LINE_4)
				

			cv2.imshow("output",frame)
			
			if cv2.waitKey(1) & 0xFF == 32:
				
				rimg = RubiksImage(frame,index,name,debug)
				try :
					rimg.analyze_file(frame)
				except :
					pass
				print(len(rimg.data))
				if len(rimg.data) == 9:

					cv2.imwrite(face_name+".jpg",frame)
					break
				else:
					flag = 1

		# When everything done, release the capture
		cap.release()
		cv2.waitKey()
		cv2.destroyAllWindows()
		return rimg.data


	def get_rgb_of_all_faces(self,size = 3):
		rgb = {}
		for face in self.faces:
			rgb[face] = self.capture_frame(face)
		return rgb

if __name__ == '__main__':
	# sc = scan_cube()
	# colors = sc.get_rgb_of_all_faces()
	# print(colors)
	# colors = {'front': {1: (44, 66, 97), 2: (46, 75, 115), 3: (158, 133, 49), 4: (29, 91, 164), 5: (190, 60, 24), 6: (171, 49, 13), 7: (238, 108, 24), 8: (234, 133, 86), 9: (67, 186, 159)}}
	colors = {'front': {1: (18, 27, 27), 2: (27, 40, 48), 3: (115, 88, 32), 4: (16, 50, 85), 5: (133, 44, 17), 6: (138, 44, 16), 7: (162, 66, 16), 8: (177, 95, 53), 9: (58, 153, 122)}}
	ind = 0
	for i in colors['front']:
		h,s,v = rgb2hsv(colors['front'][i][0],colors['front'][i][1],colors['front'][i][2])
		print(ind,(colors['front'][i][0],colors['front'][i][1],colors['front'][i][2]),(h,s,v),resolve_color(h,s,v))