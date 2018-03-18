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

	def check_algo1(self):
		face_edge_fun = { 'front':{1:self.u2,3:self.l2,5:self.r2,7:self.d2},
						  'back':{1:self.u2,3:self.r2,5:self.l2,7:self.d2},
						   'up':{1:self.b2,3:self.l2,5:self.r2,7:self.f2},
						  'down':{1:self.f2,3:self.l2,5:self.r2,7:self.b2},
						  'left':{1:self.u2,3:self.b2,5:self.f2,7:self.d2},
						  'right':{1:self.u2,3:self.f2,5:self.b2,7:self.d2},
						}
		faces = [self.front,self.back,self.left,self.right,self.up,self.down]
		faces2 = ['front','back','left','right','up','down']
		function_name = {self.f2:'f2',self.b2:'b2',self.l2:'l2',self.r2:'r2',self.u2:'u2',self.d2:'d2'}
		i=0
		for face in faces:
			bad_edges[i] = self.get_bad_edges_on_face(face)
			i+=1
		#well this for loop works for checking front-back and left-right but not up-down(for that below is the if conditoins)
		for i in range(0,4,2):
			if 1 in bad_edges[i] and 3 in bad_edges[i]:
				if 1 in bad_edges[i+1] and 5 in bad_edges[i+1]:
					up_function = face_edge_fun[faces2[i]][1]
					right_function = face_edge_fun[faces2[i]][3]
					up_function_name = function_name[up_function]
					right_function_name = function_name[right_function]
					self.algo1(up_function,right_function,up_function_name,right_function_name)
				elif 1 in bad_edges[i+1] and 3 in bad_edges[i+1]:
					up_function = face_edge_fun[faces2[i]][1]
					right_function = face_edge_fun[faces2[i]][3]
					up_function_name = function_name[up_function]
					right_function_name = function_name[right_function]
					self.algo1(up_function,right_function,up_function_name,right_function_name)
				elif 3 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					up_function = face_edge_fun[faces2[i]][1]
					right_function = face_edge_fun[faces2[i]][3]
					up_function_name = function_name[up_function]
					right_function_name = function_name[right_function]
					self.algo1(up_function,right_function,up_function_name,right_function_name)

			elif 1 in bad_edges[i] and 5 in bad_edges[i]:
				if 1 in bad_edges[i+1] and 3 in bad_edges[i+1]:
					up_function = face_edge_fun[faces2[i]][1]
					right_function = face_edge_fun[faces2[i]][5]
					up_function_name = function_name[up_function]
					right_function_name = function_name[right_function]
					self.algo1(up_function,right_function,up_function_name,right_function_name)
				elif 1 in bad_edges[i+1] and 5 in bad_edges[i+1]:
				elif 5 in bad_edges[i+1] and 7 in bad_edges[i+1]:
			elif 3 in bad_edges[i] and 7 in bad_edges[i] :
				if 5 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					up_function = face_edge_fun[faces2[i]][7]
					right_function = face_edge_fun[faces2[i]][3]
					up_function_name = function_name[up_function]
					right_function_name = function_name[right_function]
					self.algo1(up_function,right_function,up_function_name,right_function_name)
				elif 3 in bad_edges[i+1] and 7 in bad_edges[i+1]:
				elif 1 in bad_edges[i+1] and 5 in bad_edges[i+1]:
			elif 5 in bad_edges[i] and 7 in bad_edges[i] :
				if 3 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					up_function = face_edge_fun[faces2[i]][7]
					right_function = face_edge_fun[faces2[i]][5]
					up_function_name = function_name[up_function]
					right_function_name = function_name[right_function]
					self.algo1(up_function,right_function,up_function_name,right_function_name)
				elif 5 in bad_edges[i+1] and 7 in bad_edges[i+1]:
				elif 1 in bad_edges[i+1] and 3 in bad_edges[i+1]:

		if 1 in bad_edges[4] and 3 in bad_edges[4]:
			if 3 in bad_edges[5] and 7 in bad_edges[5]:
				up_function = face_edge_fun[faces2[4]][1]
				right_function = face_edge_fun[faces2[4]][3]
				up_function_name = function_name[up_function]
				right_function_name = function_name[right_function]
				self.algo1(up_function,right_function,up_function_name,right_function_name)
			elif 1 in bad_edges[5] and 3 in bad_edges[5]:
			elif 5 in bad_edges[5] and 7 in bad_edges[5]:
		elif 1 in bad_edges[4] and 5 in bad_edges[4] :
			if 5 in bad_edges[5] and 7 in bad_edges[5]:
				up_function = face_edge_fun[faces2[4]][1]
				right_function = face_edge_fun[faces2[4]][5]
				up_function_name = function_name[up_function]
				right_function_name = function_name[right_function]
				self.algo1(up_function,right_function,up_function_name,right_function_name)
			elif 1 in bad_edges[5] and 5 in bad_edges[5]:
			elif 3 in bad_edges[5] and 7 in bad_edges[5]:
		elif 3 in bad_edges[4] and 7 in bad_edges[4] :
			if 1 in bad_edges[5] and 3 in bad_edges[5]:
				up_function = face_edge_fun[faces2[i]][7]
				right_function = face_edge_fun[faces2[i]][3]
				up_function_name = function_name[up_function]
				right_function_name = function_name[right_function]
				self.algo1(up_function,right_function,up_function_name,right_function_name)
			elif 1 in bad_edges[5] and 5 in bad_edges[5]:
			elif 3 in bad_edges[5] and 7 in bad_edges[5]:
		elif 5 in bad_edges[4] and 7 in bad_edges[4] :
			if 1 in bad_edges[5] and 5 in bad_edges[5]:
				up_function = face_edge_fun[faces2[i]][7]
				right_function = face_edge_fun[faces2[i]][5]
				up_function_name = function_name[up_function]
				right_function_name = function_name[right_function]
				self.algo1(up_function,right_function,up_function_name,right_function_name)
			elif 5 in bad_edges[5] and 7 in bad_edges[5]:
			elif 1 in bad_edges[5] and 3 in bad_edges[5]:
	
	def check_algo2(self):
		edge_move = [{1:self.d2,3:self.r2},{1:self.d2,3:self.b2},{1:self.f2,3:self.r2}]
		face_function_name = {self.front:'f2',self.back:'b2',self.left:'l2',self.right:'r2',self.up:'u2',self.down:'d2'}
		edge_middle_move = [{1:1,3:3},{1:2,3:3},{1:1,3:2}]
		i = 0
		for f,b in face_pairs.items:
			if f[1] != face_color[f] and b[1] != face_color[b]:
				if f[7] != face_color[f] and b[7] != face_color[b]:
					self.algo2(edge_move[i][1],face_function_name[edge_move[i][1]],edge_middle_move[i][1])
			elif f[3] != face_color[f] and b[3] != face_color[b]:
				if f[5] != face_color[f] and b[5] != face_color[b]:
					self.algo2(edge_move[i][3],face_function_name[edge_move[i][3]],edge_middle_move[i][3])
	def check_algo4(self):

		if self.front[1]!=self.front[4]  and self.back[1]!=self.back[4]:
			if (self.right[1]!=self.right[4] and self.left[1]!=self.left[4]) or (self.right[7]!=self.right[4] and self.left[7]!=self.left[4]):
				self.algo4(self.u,'u',1)

		elif self.front[7]!=self.front[4] and self.back[7]!=self.back[4]:
			if  (self.right[7]!=self.right[4]  and self.left[7]!=self.left[4]) or (self.right[1]!=self.right[4]  and self.left[1]!=self.left[4]):
				self.algo4(self.d,'d',1)

		elif self.front[5]!=self.front[4]  and self.back[3]!=self.back[4] :
			if (self.up[5]!=self.up[4] and self.down[5]!=self.down[4]) or (self.up[3]!=self.up[4] and self.down[3]!=self.down[4]):
				self.algo4(self.r,'r',2)

		elif self.front[3]!=self.front[4]  and self.back[5]!=self.back[4] and self.down[3]!=self.down[4]:
			if (self.up[3]!=self.up[4] and self.down[3]!=self.down[4]) or (self.up[5]!=self.up[4] and self.down[5]!=self.down[4]):
				self.algo4(self.l,'l',2)
		
		elif self.right[3]!=self.right[4]  and self.left[5]!=self.left[4] :
			if (self.up[7]!=self.up[4] and self.down[1]!=self.down[4]) or (self.up[1]!=self.up[4] and self.down[7]!=self.down[4]):
				self.algo4(self.f,'f',3)
		
		elif self.right[5]!=self.right[4] and self.left[3]!=self.left[4] :
			if (self.up[1]!=self.up[4] and self.down[7]!=self.down[4]) or (self.up[7]!=self.up[4] and self.down[1]!=self.down[4]):
				self.algo4(self.f,'b',3)


	def algo1(self,up_fun,right_fun,up_fun_name,right_fun_name):
		for x in range(0,3):
			up_fun()
			self.ans.append(up_fun_name)
			right_fun()
			self.ans.append(right_fun_name)
	def algo2(self,front_fun,front_fun_name,middle_layer):
		for x in range(0,2):
			front_fun()
			self.ans.append(front_fun_name)
			
			if middle_layer == 1:
				self.mf2()
				self.ans.append('mf2')
			elif middle_layer == 2:
				self.mr2()
				self.ans.append('mr2')
			elif middle_layer == 3:
				self.mc2()
				self.ans.append('mc2')
	def algo3(self,front_fun,front_fun_name):
		front_fun()
		self.r1()
		self.l()
		front_fun()
		self.r()
		self.l1()
		self.ans.extend([front_fun_name,'r1','l',front_fun_name,'r','l1'])
		
	def algo4(self,up_fun,up_fun_name,middle_layer):
		middle_layer_fun = None
		if middle_layer == 1:
			middle_layer_fun = self.mf2()
			middle_layer_fun_name = 'mf2'
		elif middle_layer == 2:
			middle_layer_fun = self.mr2()
			middle_layer_fun_name = 'mr2'
		elif middle_layer == 3:
			middle_layer_fun = self.mc2()
			middle_layer_fun_name = 'mc2'

		middle_layer_fun()
		up_fun()
		middle_layer_fun()
		up_fun()
		up_fun()
		middle_layer_fun()
		up_fun()
		middle_layer_fun()
		self.ans.extend([middle_layer_fun_name,up_fun_name,middle_layer_fun_name,up_fun_name,up_fun_name,middle_layer_fun_name,up_fun_name,middle_layer_fun_name])


	def get_bad_edges_on_face(self,face):
		ans = []
		for i in [1,3,5,7]:
			if face[i] != face[4]
				ans.append(i)
