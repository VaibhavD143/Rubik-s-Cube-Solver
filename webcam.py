from copy import deepcopy
from image_processing import *
import numpy as np
import cv2
from color_resolver import *
import time
import sys

class scan_cube(object):
		
	def __init__(self):
		
		#all the required messages for UI
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
		#required color in center of the face
		self.face_center_color = {'f':(255,0,0),'b':(0,255,0),'l':(36,235,235),'r':(255,255,255),'u':(0,0,255),'d':(10,112,255)}
		#colors to fill a cell of detected face
		self.face_color = {'b':(255,0,0),'g':(0,255,0),'y':(36,235,235),'w':(255,255,255),'r':(0,0,255),'o':(10,112,255)}
		
		#verification cube face size 
		self.cell_size = 25	#size of single frame
		self.frame_size = 2	#size of outer border

		self.window_size = 1000	#window size of recording screen

	def capture_frame(self,face_name):
		"""this fucntion takes face name as argument and captures image untill successful
		detection and verification is also done by this"""

		if face_name not in self.faces:
			return False
		#access to 0th webcam
		cap = cv2.VideoCapture(0)

		#creat customised window
		cv2.namedWindow("output",cv2.WINDOW_NORMAL)
		cv2.resizeWindow("output",self.window_size,self.window_size)
		
		cap_msg = self.inst['enter_to_cap']	#instruction to be shown to capture image
		face_msg = self.inst[face_name]	#instruction to be shown as per the face
		
		index = 0
		name = face_name+".jpg"	#filename to save it loacaly on successful detection
		debug = False	#make it True to run scanning in debug mode (Be careful this will pop-up so many windows)
		rimg = None	#scaning variable
		color1 = color2 = (255,255,255)	#outer border color
		flag = 0	#is it scanning for first time? 0=first time,1= red alert message

		"""This loop takes frame with each iteration and proccess it"""
		while(True):

			ret, frame = cap.read()
			frame_copy = deepcopy(frame)	#copy of frame to use it afterwards
			
			# show innstruction to click
			font = cv2.FONT_HERSHEY_SIMPLEX
			text = cap_msg
			textsize = cv2.getTextSize(text, font, 1, 2)[0]
			textX = (frame.shape[1] - textsize[0]) / 2
			textY = 30
			cv2.putText(frame, text, (int(textX), int(textY) ), font, 1, (255, 255, 255), 3, cv2.FILLED)	#put text on frame at top center
			
			#show which face to scan instruction
			text = face_msg
			textsize = cv2.getTextSize(text, font, 0.5, 2)[0]
			textX = (frame.shape[1] - textsize[0]) / 2
			textY = frame.shape[0]-20
			cv2.putText(frame, text, (int(textX), int(textY) ), font, 0.5, color2, 2, cv2.LINE_4)	#put text on frame at bottomm center

			if flag:
				text = self.inst['error']
				textsize = cv2.getTextSize(text, font, 0.5, 2)[0]
				textX = (frame.shape[1] - textsize[0]) / 2
				textY = frame.shape[0]-40
				cv2.putText(frame, text, (int(textX), int(textY) ), font, 0.5, (0,0,255), 2, cv2.LINE_4)	#show error message above bottom center message
			

			cv2.imshow("output",frame)	#show frame to user
			#is spacebar pressed?
			if cv2.waitKey(1) & 0xFF == 32:	
				# im = cv2.imread("front.jpg")
				rimg = RubiksImage(frame_copy,index,name,debug)	#initialize object of scanner
				try :
					rimg.analyze_file(frame_copy)	#scan caputred image
				except:
					print("Exception occored :",sys.exc_info()[0])	#if any exception occured in scanning proccess
					flag = 1
					continue
				print(len(rimg.data))
				#all the 9 cells are detected?
				if len(rimg.data) == 9:
					rgb_val = rimg.data
					color_name = {}
					#convert rgb value to its corresponding colorname from ['b','g','y','w','r','o']
					for i in range(1,10):
						h,s,v = rgb2hsv(rgb_val[i][0],rgb_val[i][1],rgb_val[i][2])
						color_name[i] = resolve_color(h,s,v)
						print(color_name[i],(h,s,v))
						if color_name[i] not in ['r','b','g','o','y','w']:
							flag = 2
							print(i,"number cell can't be detected")
							break
					#skip whole loop as one or more color is not detected
					if flag == 2:
						flag = 1
						time.sleep(1)
						continue
					# top row of detectected cube face
					#frame of the cell
					cv2.rectangle(frame_copy,(self.frame_size,frame.shape[0]-3*self.cell_size),(self.cell_size,frame.shape[0]-self.frame_size-2*self.cell_size),(0,0,0),self.frame_size)
					#detected color of the cell
					cv2.rectangle(frame_copy,(2*self.frame_size,frame.shape[0]-3*self.cell_size+self.frame_size),(self.cell_size-self.frame_size,frame.shape[0]-2*self.cell_size-(2*self.frame_size)),self.face_color[color_name[1]],-1)
					
					cv2.rectangle(frame_copy,(self.cell_size+self.frame_size,frame.shape[0]-3*self.cell_size),(2*self.cell_size,frame.shape[0]-self.frame_size-2*self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(self.cell_size+2*self.frame_size,frame.shape[0]-3*self.cell_size+self.frame_size),(2*self.cell_size-self.frame_size,frame.shape[0]-2*self.cell_size-(2*self.frame_size)),self.face_color[color_name[2]],-1)
					
					
					cv2.rectangle(frame_copy,(2*self.cell_size+self.frame_size,frame.shape[0]-3*self.cell_size),(3*self.cell_size,frame.shape[0]-self.frame_size-2*self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.cell_size+2*self.frame_size,frame.shape[0]-3*self.cell_size+self.frame_size),(3*self.cell_size-self.frame_size,frame.shape[0]-2*self.cell_size-(2*self.frame_size)),self.face_color[color_name[3]],-1)			



					#middle row of detectected cube face
					cv2.rectangle(frame_copy,(self.frame_size,frame.shape[0]-2*self.cell_size),(self.cell_size,frame.shape[0]-self.frame_size-self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.frame_size,frame.shape[0]-2*self.cell_size+self.frame_size),(self.cell_size-self.frame_size,frame.shape[0]-self.cell_size-(2*self.frame_size)),self.face_color[color_name[4]],-1)
					
					cv2.rectangle(frame_copy,(self.cell_size+self.frame_size,frame.shape[0]-2*self.cell_size),(2*self.cell_size,frame.shape[0]-self.frame_size-self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(self.cell_size+2*self.frame_size,frame.shape[0]-2*self.cell_size+self.frame_size),(2*self.cell_size-self.frame_size,frame.shape[0]-self.cell_size-(2*self.frame_size)),self.face_color[color_name[5]],-1)
					
					
					cv2.rectangle(frame_copy,(2*self.cell_size+self.frame_size,frame.shape[0]-2*self.cell_size),(3*self.cell_size,frame.shape[0]-self.frame_size-self.cell_size),(0,0,0),self.frame_size)
					cv2.rectangle(frame_copy,(2*self.cell_size+2*self.frame_size,frame.shape[0]-2*self.cell_size+self.frame_size),(3*self.cell_size-self.frame_size,frame.shape[0]-self.cell_size-(2*self.frame_size)),self.face_color[color_name[6]],-1)			
					


					#bottom row of detectected cube face
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
					cv2.putText(frame_copy, text, (int(textX), int(textY) ), font, 0.5, color2, 2, cv2.LINE_4) #instruction to verify image with 'y'

					text = self.inst['verify']
					textsize = cv2.getTextSize(text, font, 0.8, 2)[0]
					textX = (frame.shape[1] - textsize[0]) / 2
					textY = 30
					cv2.putText(frame_copy, text, (int(textX), int(textY) ), font, 0.8, color2, 2, cv2.LINE_4)	#verification message


					cv2.imshow("output",frame_copy)	#show final frame with detected colors at bottom left corner

					#if detected color is successfully verified by uer
					if cv2.waitKey(0) & 0xFF == ord('y'):
						cv2.imwrite(face_name+".jpg",frame)	#save it local
						break
				#detected lesser or greater than 9 cell
				else:
					flag = 1	#show error message

		# When everything done, release the capture
		cap.release()
		# cv2.waitKey()
		cv2.destroyAllWindows()
		return color_name

	"""call capture image function for each face of cube"""
	def get_rgb_of_all_faces(self,size = 3):
		rgb = {}
		input_file = open("input_json",'w+')
		for face in self.faces:
			rgb[face] = self.capture_frame(face)
			# print(rgb[face])
			input_file.write(face+' : '+' '.join(rgb[face].values())+'\n')
		return rgb

if __name__ == '__main__':
	sc = scan_cube()
	colors = sc.get_rgb_of_all_faces()
	print(colors)
	
	# # colors = {'f': {1: (44, 66, 97), 2: (46, 75, 115), 3: (158, 133, 49), 4: (29, 91, 164), 5: (190, 60, 24), 6: (171, 49, 13), 7: (238, 108, 24), 8: (234, 133, 86), 9: (67, 186, 159)}}
	# # colors = {'f': {1: (18, 27, 27), 2: (27, 40, 48), 3: (115, 88, 32), 4: (16, 50, 85), 5: (133, 44, 17), 6: (138, 44, 16), 7: (162, 66, 16), 8: (177, 95, 53), 9: (58, 153, 122)}}
	# colors = {'f': {1: (54, 71, 99), 2: (60, 84, 121), 3: (168, 136, 53), 4: (47, 94, 154), 5: (187, 77, 48), 6: (180, 66, 31), 7: (211, 106, 39), 8: (225, 139, 88), 9: (72, 184, 150)}}

	