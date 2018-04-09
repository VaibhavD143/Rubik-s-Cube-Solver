from copy import deepcopy
from image_processing import *
import numpy as np
import cv2
from color_resolver import *


class scan_cube(object):
		
	def __init__(self):
		self.inst = {
		'enter_to_cap': "Press 'spacebar' to capture image",
		'f': "'blue' center in front and 'red' center on top",
		'b' : "'green' center in front and 'red' center on top",
		'u': "'red' center in front and 'green' center on top",
		'l': "'yellow' center in front and 'red' on top",
		'r' : "'white' in front and 'red' on top",
		'd' : "'orange' center in front and 'blue' on top",
		'error' : "Coudn't scan image please try again!",
		'verify': "is detected colors are same as cube face?",
		'verify_inst': "Press 'y' for yes and 'n' to scan again."
		}		
		self.faces = ['f','b','l','r','u','d']
		self.face_center_color = {'f':(255,0,0),'b':(0,255,0),'l':(36,235,235),'r':(255,255,255),'u':(0,0,255),'d':(10,112,255)}
		self.face_color = {'b':(255,0,0),'g':(0,255,0),'y':(36,235,235),'w':(255,255,255),'r':(0,0,255),'o':(10,112,255)}
		self.cell_size = 25
		self.frame_size = 2

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
			frame_copy = deepcopy(frame)
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
				im = cv2.imread("front.jpg")
				rimg = RubiksImage(im,index,name,debug)
				try :
					rimg.analyze_file(im)
				except e:
					print("Exception occored :",e)
					flag = 1
					continue
				print(len(rimg.data))
				if len(rimg.data) == 9:
					rgb_val = rimg.data
					color_name = {}

					for i in range(1,10):
						h,s,v = rgb2hsv(rgb_val[i][0],rgb_val[i][1],rgb_val[i][2])
						color_name[i] = resolve_color(h,s,v)
						if color_name not in ['r','b','g','o','y','w']:
							flag = 1
							print("debug")
							continue

					# top row
					cv2.rectangle(frame_copy,(self.frame_size,frame.shape[0]-3*self.cell_size),(self.cell_size,frame.shape[0]-self.frame_size-2*self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.frame_size,frame.shape[0]-3*self.cell_size+self.frame_size),(self.cell_size-self.frame_size,frame.shape[0]-2*self.cell_size-(2*self.frame_size)),self.face_color[color_name[1]],-1)
					
					cv2.rectangle(frame_copy,(self.cell_size+self.frame_size,frame.shape[0]-3*self.cell_size),(2*self.cell_size,frame.shape[0]-self.frame_size-2*self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(self.cell_size+2*self.frame_size,frame.shape[0]-3*self.cell_size+self.frame_size),(2*self.cell_size-self.frame_size,frame.shape[0]-2*self.cell_size-(2*self.frame_size)),self.face_color[color_name[2]],-1)
					
					
					cv2.rectangle(frame_copy,(2*self.cell_size+self.frame_size,frame.shape[0]-3*self.cell_size),(3*self.cell_size,frame.shape[0]-self.frame_size-2*self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.cell_size+2*self.frame_size,frame.shape[0]-3*self.cell_size+self.frame_size),(3*self.cell_size-self.frame_size,frame.shape[0]-2*self.cell_size-(2*self.frame_size)),self.face_color[color_name[3]],-1)			



					#middle row
					cv2.rectangle(frame_copy,(self.frame_size,frame.shape[0]-2*self.cell_size),(self.cell_size,frame.shape[0]-self.frame_size-self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.frame_size,frame.shape[0]-2*self.cell_size+self.frame_size),(self.cell_size-self.frame_size,frame.shape[0]-self.cell_size-(2*self.frame_size)),self.face_color[color_name[4]],-1)
					
					cv2.rectangle(frame_copy,(self.cell_size+self.frame_size,frame.shape[0]-2*self.cell_size),(2*self.cell_size,frame.shape[0]-self.frame_size-self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(self.cell_size+2*self.frame_size,frame.shape[0]-2*self.cell_size+self.frame_size),(2*self.cell_size-self.frame_size,frame.shape[0]-self.cell_size-(2*self.frame_size)),self.face_color[color_name[5]],-1)
					
					
					cv2.rectangle(frame_copy,(2*self.cell_size+self.frame_size,frame.shape[0]-2*self.cell_size),(3*self.cell_size,frame.shape[0]-self.frame_size-self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.cell_size+2*self.frame_size,frame.shape[0]-2*self.cell_size+self.frame_size),(3*self.cell_size-self.frame_size,frame.shape[0]-self.cell_size-(2*self.frame_size)),self.face_color[color_name[6]],-1)			
					


					#bottom row
					cv2.rectangle(frame_copy,(self.frame_size,frame.shape[0]-self.cell_size),(self.cell_size,frame.shape[0]-self.frame_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.frame_size,frame.shape[0]-self.cell_size+self.frame_size),(self.cell_size-self.frame_size,frame.shape[0]-(2*self.frame_size)),self.face_color[color_name[7]],-1)
					
					cv2.rectangle(frame_copy,(self.cell_size+self.frame_size,frame.shape[0]-self.cell_size),(2*self.cell_size,frame.shape[0]-self.frame_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(self.cell_size+2*self.frame_size,frame.shape[0]-self.cell_size+self.frame_size),(2*self.cell_size-self.frame_size,frame.shape[0]-(2*self.frame_size)),self.face_color[color_name[8]],-1)
					
					
					cv2.rectangle(frame_copy,(2*self.cell_size+self.frame_size,frame.shape[0]-self.cell_size),(3*self.cell_size,frame.shape[0]-self.frame_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.cell_size+2*self.frame_size,frame.shape[0]-self.cell_size+self.frame_size),(3*self.cell_size-self.frame_size,frame.shape[0]-(2*self.frame_size)),self.face_color[color_name[9]],-1)			


					text = self.inst['verify_inst']
					textsize = cv2.getTextSize(text, font, 0.5, 2)[0]
					textX = (frame.shape[1] - textsize[0]) / 2
					textY = frame.shape[0]-20
					cv2.putText(frame_copy, text, (int(textX), int(textY) ), font, 0.5, color2, 2, cv2.LINE_4)

					text = self.inst['verify']
					textsize = cv2.getTextSize(text, font, 1, 2)[0]
					textX = (frame.shape[1] - textsize[0]) / 2
					textY = 30
					cv2.putText(frame_copy, text, (int(textX), int(textY) ), font, 1, color2, 2, cv2.LINE_4)


					cv2.imshow("output",frame_copy)

					if cv2.waitKey(0) & 0xFF == ord('y'):
						cv2.imwrite(face_name+".jpg",frame)
						break

				else:
					flag = 1

		# When everything done, release the capture
		cap.release()
		# cv2.waitKey()
		cv2.destroyAllWindows()
		return color_name


	def get_rgb_of_all_faces(self,size = 3):
		rgb = {}
		for face in self.faces:
			rgb[face] = self.capture_frame(face)
		return rgb

if __name__ == '__main__':
	sc = scan_cube()
	colors = sc.get_rgb_of_all_faces()
	print(colors)
	# # colors = {'f': {1: (44, 66, 97), 2: (46, 75, 115), 3: (158, 133, 49), 4: (29, 91, 164), 5: (190, 60, 24), 6: (171, 49, 13), 7: (238, 108, 24), 8: (234, 133, 86), 9: (67, 186, 159)}}
	# # colors = {'f': {1: (18, 27, 27), 2: (27, 40, 48), 3: (115, 88, 32), 4: (16, 50, 85), 5: (133, 44, 17), 6: (138, 44, 16), 7: (162, 66, 16), 8: (177, 95, 53), 9: (58, 153, 122)}}
	# colors = {'f': {1: (54, 71, 99), 2: (60, 84, 121), 3: (168, 136, 53), 4: (47, 94, 154), 5: (187, 77, 48), 6: (180, 66, 31), 7: (211, 106, 39), 8: (225, 139, 88), 9: (72, 184, 150)}}

	