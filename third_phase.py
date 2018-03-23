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
		"""This will solve third phase in two step"""
		#this is to solve corners of all edges
		self.set_corners_acc_center()
		print('-------------------------------------------- All corner set -------------------------------------------------')
		self.print_cube_with_faces()

		#3B start
		checking_functions = [self.check_algo1,self.check_algo2,self.check_algo3,self.check_algo4,self.check_algo5,self.check_algo6]
		# checking_functions = [self.check_algo1,self.check_algo5,self.check_algo6]
		while True:
			if self.is_solved():
				break
			else:
				for fun in checking_functions:
					if fun() == True:
						break
		
		return(self.ans)

	def get_bad_edges_on_face(self,face):
		ans = []
		for i in [1,3,5,7]:
			if face[i] != face[4]:
				ans.append(i)
		return ans
	
	def set_corner_of_face(self,front_face,back_face,up,down,left,right,front,back,name):
		
		""" This lists are pairs of possible mismatch in front and back"""
		pair_front_f = [0,2,8,6]
		pair_front_s = [2,8,6,0]
		pair_back_f = [2,0,6,8]
		pair_back_s = [0,6,8,2]

		#move to get proper corner according to number
		#0- pair in upper layer, 1-pair in right side .... 
		move = [up,right,down,left]
		move_name = [name['u'],name['r'],name['d'],name['l']]

		for i in range(4):
			#if corners are not set in front at ith pair
			if front_face[pair_front_f[i]] != front_face[4] and front_face[pair_front_s[i]] != front_face[4]:
				#if corners are not present as front in ith pair then it must be in opposite side as only rotation of 180* allowed
				if back_face[pair_back_f[i]] != front_face[4] and back_face[pair_back_s[i]] != front_face[4]:
					# make pair in front and back at same layer
					back()
					back()
					self.ans.extend([name['b'],name['b']])
				
				move[i]()
				move[i]()
				self.ans.extend([move_name[i],move_name[i]])
		# print('in---------------------------')
		# self.print_cube_with_faces()
		# print(self.ans)




	def set_corners_acc_center(self):
	
		self.set_corner_of_face(self.front,self.back,self.u,self.d,self.l,self.r,self.f,self.b,{'u':'u','d':'d','l':'l','r':'r','f':'f','b':'b'})
		self.set_corner_of_face(self.right,self.left,self.u,self.d,self.f,self.b,self.r,self.l,{'u':'u','d':'d','l':'f','r':'b','f':'r','b':'l'})

	def check_algo1(self):
		return_value = False
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
		bad_edges = [0]*len(faces)
		for face in faces:
			bad_edges[i] = self.get_bad_edges_on_face(face)
			i+=1

		a=b=0
		flag = False
		#well this for loop works for checking front-back and left-right but not up-down(for that below is the if conditoins)
		for i in range(0,4,2):
			flag = False
			if 1 in bad_edges[i] and 3 in bad_edges[i]:
				if 1 in bad_edges[i+1] and 5 in bad_edges[i+1]:
					a=1
					b=3
					flag = True

			elif 1 in bad_edges[i] and 5 in bad_edges[i]:
				if 1 in bad_edges[i+1] and 3 in bad_edges[i+1]:
					a=1
					b=5
					flag = True
				
			elif 3 in bad_edges[i] and 7 in bad_edges[i] :
				if 5 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					a=7
					b=3
					flag = True
				
			elif 5 in bad_edges[i] and 7 in bad_edges[i] :
				if 3 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					a=7
					b=5
					flag = True
			
			if flag:
				up_function = face_edge_fun[faces2[i]][a]
				right_function = face_edge_fun[faces2[i]][b]
				up_function_name = function_name[up_function]
				right_function_name = function_name[right_function]
				self.algo1(up_function,right_function,up_function_name,right_function_name)
				return_value = True
				

		if 1 in bad_edges[4] and 3 in bad_edges[4]:
			if 3 in bad_edges[5] and 7 in bad_edges[5]:
				a=1
				b=3
				flag = True
			
		elif 1 in bad_edges[4] and 5 in bad_edges[4] :
			if 5 in bad_edges[5] and 7 in bad_edges[5]:
				a = 1
				b = 5
				flag = True
			
		elif 3 in bad_edges[4] and 7 in bad_edges[4] :
			if 1 in bad_edges[5] and 3 in bad_edges[5]:
				a = 7
				b = 3
				flag = True
			
		elif 5 in bad_edges[4] and 7 in bad_edges[4] :
			if 1 in bad_edges[5] and 5 in bad_edges[5]:
				a = 7
				b = 5
				flag = True
		
		if flag:
			up_function = face_edge_fun[faces2[4]][a]
			right_function = face_edge_fun[faces2[4]][b]
			up_function_name = function_name[up_function]
			right_function_name = function_name[right_function]
			self.algo1(up_function,right_function,up_function_name,right_function_name)
			return_value = True
		return return_value

	def check_algo6(self):
		#line 240function for edge 4 remaining
		return_value = False
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
		bad_edges = [0]*len(faces)

		for face in faces:
			bad_edges[i] = self.get_bad_edges_on_face(face)
			i+=1

		a=b=0
		flag = False
		#TODO USE a,b
		for i in range(0,4,2):
			if 1 in bad_edges[i] and 3 in bad_edges[i]:
				
				if (1 in bad_edges[i+1] and 3 in bad_edges[i+1]):
					a = 1
					b = 4
					flag = True
					
				elif 5 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					a = 3
					b = 4
					flag = True

			elif 1 in bad_edges[i] and 5 in bad_edges[i]:
				
				if (1 in bad_edges[i+1] and 5 in bad_edges[i+1]):
					a = 1
					b = 4
					flag = True
				elif 3 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					a = 5
					b = 4
					flag = True

			elif 3 in bad_edges[i] and 7 in bad_edges[i] :
				
				if (1 in bad_edges[i+1] and 5 in bad_edges[i+1]):
					a = 3
					b = 4
					flag = True
					
				elif 3 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					a = 7
					b = 4
					flag = True

			elif 5 in bad_edges[i] and 7 in bad_edges[i] :

				if (1 in bad_edges[i+1] and 3 in bad_edges[i+1]):
					a = 5
					b = 4
					flag = True

				elif 5 in bad_edges[i+1] and 7 in bad_edges[i+1]:
					a = 7
					b = 4
					flag = True

			if flag:
				up_function = face_edge_fun[faces2[i]][a]
				right_function = face_edge_fun[faces2[i]][b]
				up_function_name = function_name[up_function]
				right_function_name = function_name[right_function]
				self.algo1(up_function,right_function,up_function_name,right_function_name)
				return_value = True

		if 1 in bad_edges[4] and 3 in bad_edges[4]:
			
			if 1 in bad_edges[5] and 3 in bad_edges[5]:
				a = 3
				b = 4
				flag = True
				
			elif 5 in bad_edges[5] and 7 in bad_edges[5]:
				a = 1
				b = 4
				flag = True

		elif 1 in bad_edges[4] and 5 in bad_edges[4] :
			
			if 1 in bad_edges[5] and 5 in bad_edges[5]:
				a = 5
				b = 4
				flag = True
				
			elif 3 in bad_edges[5] and 7 in bad_edges[5]:
				a = 1
				b = 4
				flag = True
				
		elif 3 in bad_edges[4] and 7 in bad_edges[4] :
			
			if 1 in bad_edges[5] and 5 in bad_edges[5]:
				a = 7
				b = 4
				flag = True
				
			elif 3 in bad_edges[5] and 7 in bad_edges[5]:
				a = 3
				b = 4
				flag = True
				
		elif 5 in bad_edges[4] and 7 in bad_edges[4] :
			
			if 5 in bad_edges[5] and 7 in bad_edges[5]:
				a = 5
				b = 4
				flag = True
				
			elif 1 in bad_edges[5] and 3 in bad_edges[5]:
				a = 7
				b = 4
				flag = True
				

		if flag:
			up_function = face_edge_fun[faces2[4]][a]
			right_function = face_edge_fun[faces2[4]][b]
			up_function_name = function_name[up_function]
			right_function_name = function_name[right_function]
			self.algo1(up_function,right_function,up_function_name,right_function_name)
			return_value = True
		return return_value

	def check_algo2(self):
		#change key of dict
		return_value = False
		edge_move = [{1:self.d2,3:self.r2},{1:self.d2,3:self.b2},{1:self.f2,3:self.r2}]
		face_function_name = {self.front:'f2',self.back:'b2',self.left:'l2',self.right:'r2',self.up:'u2',self.down:'d2'}
		edge_middle_move = [{1:1,3:3},{1:2,3:3},{1:1,3:2}]
		i = 0
		for f,b in face_pairs.items:
			if f[1] != face_color[f] and b[1] != face_color[b]:
				if f[7] != face_color[f] and b[7] != face_color[b]:
					self.algo2(edge_move[i][1],face_function_name[edge_move[i][1]],edge_middle_move[i][1])
					return_value = True
			elif f[3] != face_color[f] and b[3] != face_color[b]:
				if f[5] != face_color[f] and b[5] != face_color[b]:
					self.algo2(edge_move[i][3],face_function_name[edge_move[i][3]],edge_middle_move[i][3])
					return_value = True
		return return_value

	def check_algo3(self):

		return_value = False
		if (self.front[7] != self.front[4] and self.down[1] != self.down[4] and self.back[1] != self.back[4]  and self.up[7] != self.up[4]):
			self.algo3(self.f2,self.mf1,self.mf,['f2','mf1','mf'])
			return_value = True
		
		elif (self.front[7] != self.front[4] and self.down[1] != self.down[4] and self.back[7] != self.back[4] and self.up[1] != self.up[4]):
			self.algo3(self.d2,self.mf,self.mf1,['d2','mf','mf1'])
			return_value = True

		elif (self.front[1] != self.front[4] and self.up[7] != self.up[4] and self.down[1] != self.down[4] and self.back[7] != self.back[4]):
			self.algo3(self.f2,self.mf,self.mf1,['f2','mf','mf1'])
			return_value = True

		elif (self.front[1] != self.front[4] and self.up[7] != self.up[4] and  self.down[7] != self.down[4] and self.back[1] != self.back[4]):
			self.algo3(self.u2,self.mf1,self.mf,['u2','mf1','mf'])
			return_value = True

		elif (self.up[1] != self.up[4] and self.back[1] != self.back[4] and self.front[7] != self.front[4] and self.down[7] != self.down[4]):
			self.algo3(self.b2,self.mf1,self.mf,['u2','mf1','mf'])
			return_value = True
		
		elif (self.up[1] != self.up[4] and self.back[1] != self.back[4] and self.front[1] != self.front[4] and self.down[1] != self.down[4]):
			self.algo3(self.u2,self.mf,self.mf1,['u2','mf','mf1'])
			return_value = True
		
		elif (self.down[7] != self.down[4] and self.back[7] != self.back[4] and self.front[7] != self.front[4] and self.up[7] != self.up[4]):
			self.algo3(self.d2,self.mf1,self.mf,['d2','mf1','mf'])
			return_value = True

		elif (self.down[7] != self.down[4] and self.back[7] != self.back[4] and self.front[1] != self.front[4] and self.up[1] != self.up[4]):
			self.algo3(self.b2,self.mf,self.mf1,['b2','mf','mf1'])
			return_value = True

		elif (self.right[7] != self.right[4] and self.down[5] != self.down[4] and self.up[5] != self.up[4] and self.left[1] != self.left[4]):
			self.algo3(self.r2,self.mr1,self.mr,['r2','mr1','mr'])
			return_value = True

		elif (self.right[7] != self.right[4] and self.down[5] != self.down[4] and self.up[3] != self.up[4] and self.left[7] != self.left[4]):
			self.algo3(self.d2,self.mr,self.mr1,['d2','mr','mr1'])
			return_value = True

		elif (self.right[1] != self.right[4] and self.up[5] != self.up[4] and self.left[1] != self.left[4] and self.down[3] != self.down[4]):
			self.algo3(self.u2,self.mr1,self.mr,['u2','mr1','mr'])
			return_value = True	

		elif (self.right[1] != self.right[4] and self.up[5] != self.up[4] and self.left[7] != self.left[4] and self.down[5] != self.down[4]):
			self.algo3(self.r2,self.mr,self.mr1,['u2','mr','mr1'])
			return_value = True

		elif (self.left[1] != self.left[4] and self.up[3] != self.up[4] and self.right[7] != self.right[4] and self.down[3] != self.down[4]):
			self.algo3(self.l2,self.mr1,self.mr,['l2','mr1','mr'])
			return_value = True

		elif (self.left[1] != self.left[4] and self.up[3] != self.up[4] and self.right[1] != self.right[4] and self.down[5] != self.down[4]):
			self.algo3(self.u2,self.mr,self.mr1,['u2','mr','mr1'])
			return_value = True

		elif (self.left[7] != self.left[4] and self.down[3] != self.down[4] and self.right[7] != self.right[4] and self.up[5] != self.up[4]):
			self.algo3(self.d2,self.mr1,self.mr,['d2','mr1','mr'])
			return_value = True
		
		elif (self.left[7] != self.left[4] and self.down[3] != self.down[4] and self.up[3] != self.right[4] and self.right[1] != self.up[4]):
			self.algo3(self.l2,self.mr,self.mr1,['l2','mr','mr1'])
			return_value = True

		elif (self.front[5] != self.front[4] and self.right[3] != self.right[4] and self.left[5] != self.left[4] and self.back[5] != self.back[4]):
			self.algo3(self.f2,self.mc,self.mc1,['f2','mc','mc1'])
			return_value = True

		elif (self.front[5] != self.front[4] and self.right[3] != self.right[4] and self.back[3] != self.back[4] and self.left[3] != self.left[4]):
			self.algo3(self.r2,self.mc1,self.mc,['r2','mc1','mc'])
			return_value = True

		elif (self.front[3] != self.front[4] and self.left[5] != self.left[4] and self.back[5] != self.back[4] and self.right[5] != self.right[4]):
			self.algo3(self.l2,self.mc,self.mc1,['l2','mc','mc1'])
			return_value = True
		
		elif (self.front[3] != self.front[4] and self.left[5] != self.left[4] and self.back[3] != self.back[4] and self.right[3] != self.right[4]):
			self.algo3(self.f2,self.mc1,self.mc,['f2','mc1','mc'])
			return_value = True

		elif (self.left[3] != self.left[4] and self.back[5] != self.back[4] and self.right[5] != self.right[5] and self.front[5] != self.front[4]):
			self.algo3(self.b2,self.mc,self.mc1,['b2','mc','mc1'])
			return_value = True

		elif (self.left[3] != self.left[4] and self.back[5] != self.back[4] and self.right[3] != self.right[5] and self.front[3] != self.front[4]):
			self.algo3(self.l2,self.mc1,self.mc,['l2','mc1','mc'])
			return_value = True

		elif (self.right[5] != self.right[4] and self.back[3] != self.back[4] and self.front[5] != self.front[5] and self.left[5] != self.left[5]):
			self.algo3(self.r2,self.mc,self.mc1,['r2','mc','mc1'])
			return_value = True

		elif (self.right[5] != self.right[4] and self.back[3] != self.back[4] and self.front[3] != self.front[5] and self.left[3] != self.left[5]):
			self.algo3(self.b2,self.mc1,self.mc,['b2','mc1','mc'])
			return_value = True
		return return_value

	def check_algo4(self):
		return_value = False
		if self.front[1]!=self.front[4]  and self.back[1]!=self.back[4]:
			if (self.right[1]!=self.right[4] and self.left[1]!=self.left[4]) or (self.right[7]!=self.right[4] and self.left[7]!=self.left[4]):
				self.algo4(self.u,'u',1)
				return_value = True

		elif self.front[7]!=self.front[4] and self.back[7]!=self.back[4]:
			if  (self.right[7]!=self.right[4]  and self.left[7]!=self.left[4]) or (self.right[1]!=self.right[4]  and self.left[1]!=self.left[4]):
				self.algo4(self.d,'d',1)
				return_value = True

		elif self.front[5]!=self.front[4]  and self.back[3]!=self.back[4] :
			if (self.up[5]!=self.up[4] and self.down[5]!=self.down[4]) or (self.up[3]!=self.up[4] and self.down[3]!=self.down[4]):
				self.algo4(self.r,'r',2)
				return_value = True

		elif self.front[3]!=self.front[4]  and self.back[5]!=self.back[4] and self.down[3]!=self.down[4]:
			if (self.up[3]!=self.up[4] and self.down[3]!=self.down[4]) or (self.up[5]!=self.up[4] and self.down[5]!=self.down[4]):
				self.algo4(self.l,'l',2)
				return_value = True
		
		elif self.right[3]!=self.right[4]  and self.left[5]!=self.left[4] :
			if (self.up[7]!=self.up[4] and self.down[1]!=self.down[4]) or (self.up[1]!=self.up[4] and self.down[7]!=self.down[4]):
				self.algo4(self.f,'f',3)
				return_value = True
		
		elif self.right[5]!=self.right[4] and self.left[3]!=self.left[4] :
			if (self.up[1]!=self.up[4] and self.down[7]!=self.down[4]) or (self.up[7]!=self.up[4] and self.down[1]!=self.down[4]):
				self.algo4(self.f,'b',3)
				return_value = True
		return return_value
	def check_algo5(self):
		
		return_value = False
		bad_edges = self.get_bad_edges()
		bad_edges = set(bad_edges)
		all_edges = set(range(1,13))
		loop_through = list(all_edges - bad_edges)
		# bad_edges = sorted(bad_edges)
		#if key=1 then 1 is mismatched and others are set,there can be two posibilities for this,given face is face on which it makes tri set. 
		possible_faces = {1:[[2,3,4],'f',[5,8,9],'u'],2:[[1,3,4],'f',[5,6,10],'r'],3:[[1,2,4],'f',[6,7,11],'d'],4:[[1,2,3],'f',[7,8,12],'l'],5:[[2,6,10],'r',[1,8,9],'u'],6:[[7,11,3],'d',[5,2,10],'r'],7:[[4,8,12],'l',[3,6,11],'d'],8:[[1,5,9],'u',[4,7,12],'l'],9:[[10,11,12],'b',[1,5,8],'u'],10:[[9,11,12],'b',[2,5,6],'r'],11:[[9,10,12],'b',[3,6,7],'d'],12:[[9,10,11],'b',[4,7,8],'l']}
		#possible fourth edge for mismatch number of key
		fourth_edge ={1:{'f':[9,11],'u':[3,11]},2:{'f':[10,12],'r':[4,12]},3:{'f':[11,9],'d':[1,9]},4:{'f':[12,10],'l':[2,10]},5:{'r':[8,7],'u':[6,7]},6:{'d':[5,8],'r':[7,8]},7:{'l':[6,5],'d':[8,5]},8:{'u':[7,6],'l':[5,6]},9:{'b':[1,3],'u':[11,3]},10:{'b':[2,4],'r':[12,4]},11:{'b':[3,1],'d':[9,1]},12:{'b':[4,2],'l':[10,2]}}
		#required moves to perform to set four mismatch in single side
		moves ={1:{'f':[self.u2,self.b2],'u':[self.f2,self.d2]},2:{'f':[self.r2,self.b2],'r':[self.f2,self.l2]},3:{'f':[self.d2,self.d2],'d':[self.f2,self.u2]},4:{'f':[self.l2,self.b2],'l':[self.f2,self.r2]},5:{'r':[self.u2,self.l2],'u':[self.r2,self.d2]},6:{'d':[self.r2,self.u2],'r':[self.d2,self.l2]},7:{'l':[self.d2,self.r2],'d':[self.l2,self.u2]},8:{'u':[self.l2,self.d2],'l':[self.u2,self.r2]},9:{'b':[self.u2,self.f2],'u':[self.b2,self.d2]},10:{'b':[self.r2,self.f2],'r':[self.b2,self.l2]},11:{'b':[self.d2,self.f2],'d':[self.b2,self.u2]},12:{'b':[self.l2,self.f2],'l':[self.b2,self.r2]}}
		move_name ={1:{'f':['u2','b2'],'u':['f2','d2']},2:{'f':['r2','b2'],'r':['f2','l2']},3:{'f':['d2','d2'],'d':['f2','u2']},4:{'f':['l2','b2'],'l':['f2','r2']},5:{'r':['u2','l2'],'u':['r2','d2']},6:{'d':['r2','u2'],'r':['d2','l2']},7:{'l':['d2','r2'],'d':['l2','u2']},8:{'u':['l2','d2'],'l':['u2','r2']},9:{'b':['u2','f2'],'u':['b2','d2']},10:{'b':['r2','f2'],'r':['b2','l2']},11:{'b':['d2','f2'],'d':['b2','u2']},12:{'b':['l2','f2'],'l':['b2','r2']}}

		for edge in list():
			if set(possible_faces[edge][0]).issubset(bad_edges):
				if fourth_edge[edge][possible_faces[edge][1]][0] in bad_edges:
					moves[edge][possible_faces[edge][1]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][1]][0])

					moves[edge][possible_faces[edge][1]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][1]][0])
					return_value = True
				elif fourth_edge[edge][possible_faces[edge][1]][1] in bad_edges:
					moves[edge][possible_faces[edge][1]][1]()
					self.ans.append(move_name[edge][possible_faces[edge][1]][1])
					moves[edge][possible_faces[edge][1]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][1]][0])

					moves[edge][possible_faces[edge][1]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][1]][0])
					moves[edge][possible_faces[edge][1]][1]()
					self.ans.append(move_name[edge][possible_faces[edge][1]][1])
					return_value = True

			elif set(possible_faces[edge][2]).issubset(bad_edges):
				
				if fourth_edge[edge][possible_faces[edge][3]][0] in bad_edges:
					moves[edge][possible_faces[edge][3]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][3]][0])

					moves[edge][possible_faces[edge][3]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][3]][0])
					return_value = True
				elif fourth_edge[edge][possible_faces[edge][3]][1] in bad_edges:
					moves[edge][possible_faces[edge][3]][1]()
					self.ans.append(move_name[edge][possible_faces[edge][3]][1])
					moves[edge][possible_faces[edge][1]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][3]][0])

					moves[edge][possible_faces[edge][1]][0]()
					self.ans.append(move_name[edge][possible_faces[edge][3]][0])
					moves[edge][possible_faces[edge][1]][1]()
					self.ans.append(move_name[edge][possible_faces[edge][3]][1])
					return_value = True
		return return_value

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
		
	def algo3(self,front2,middle_layer1,middle_layer,move_names):
		front2()
		middle_layer1()
		front2()
		middle_layer()
		self.ans.extend([move_names[0],move_names[1],move_names[0],move_names[2]])

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
