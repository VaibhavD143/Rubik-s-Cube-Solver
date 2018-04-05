from image_processing import *
import numpy as np
import cv2


class scan_cube(object):
		
	def __init__(self):
		self.inst = {
		'enter_to_cap': "Press 'c' to capture image",
		'front': "'blue' center in front and 'red' center on top",
		'back' : "'green' center in front and 'red' center on top",
		'up': "'red' center in front and 'green' center on top",
		'left': "'yellow' center in front and 'red' on top",
		'right' : "'white' in front and 'red' on top",
		'down' : "'orange' center in front and 'blue' on top",
		'error' : "Coudn't scan image please try again!"
		}		
		self.faces = ['front','back','left','right','up','down']
	
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

		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()

			# Our operations on the frame come here
			# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			cv2.putText(frame,cap_msg,(150,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),4,cv2.LINE_AA)
			cv2.putText(frame,face_msg,(70,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),4,cv2.LINE_AA)

			cv2.imshow("output",frame)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				
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
					face_msg = self.inst['error']

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
	sc = scan_cube()
	print(sc.get_rgb_of_all_faces())
	