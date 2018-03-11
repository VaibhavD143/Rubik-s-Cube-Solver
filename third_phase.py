from notation import *

class third_phase(mycube):
	ans = []
	"""constructor gets current state (i.e, second stage solved) and initializes the super class (i.e the generic cube)"""
	def __init__(self, c_state):
		self.up = c_state.up
		self.down = c_state.down
		self.back = c_state.back
		self.front = c_state.front
		self.right = c_state.right
		self.left = c_state.left

	def solve(self):

		self.set_corners_acc_center()
		print('-------------------------------------------- All corner set -------------------------------------------------')
		self.print_cube_with_faces()
		
		return(self.ans)

	def set_corner_of_face(self,front_face,back_face,up,down,left,right,front,back,name):
		pair_front_f = [0,2,8,6]
		pair_front_s = [2,8,6,0]
		pair_back_f = [2,0,6,8]
		pair_back_s = [0,6,8,2]
		move = [up,right,down,left]
		move_name = [name['u'],name['r'],name['d'],name['l']]

		for i in range(4):
			if front_face[pair_front_f[i]] != front_face[4] and front_face[pair_front_s[i]] != front_face[4]:
				if back_face[pair_back_f[i]] != front_face[4] and back_face[pair_back_s[i]] != front_face[i]:
					back()
					back()
					self.ans.extend([name['b'],name['b']])
				
				move[i]()
				move[i]()
				self.ans.extend([move_name[i],move_name[i]])
		# self.print_cube_with_faces()




	def set_corners_acc_center(self):
		
		self.set_corner_of_face(self.front,self.back,self.u,self.d,self.l,self.r,self.f,self.b,{'u':'u','d':'d','l':'l','r':'r','f':'f','b':'b'})
		self.set_corner_of_face(self.right,self.left,self.u,self.d,self.f,self.b,self.r,self.l,{'u':'u','d':'d','l':'f','r':'b','f':'r','b':'l'})