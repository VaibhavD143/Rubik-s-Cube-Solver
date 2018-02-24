from notation import *


class first_phase(mycube):

	global ans #answer variable containing all the steps
	front_edges = [1,2,3,4] #edges those are in front face 	

	#To convert two bad edges to four bad edges 
	def from_two_bad_edges_to_four(self,bad_edges):
		#When both bad edges are in front face
		if bad_edges[0] in self.front_edges and bad_edges[1] in self.front_edges:
			if bad_edges[0] == 1:
				self.u()
				ans.append('u')
			elif bad_edges[0] == 2:
				self.r()
				ans.append('r')
			elif bad_edges[0] == 3:
				self.d()
				ans.append('d')
			elif bad_edges[0] == 4:
				self.l()
				ans.append('l')
			self.f()
			ans.append('f')

		#when any one bad edge is in front
		elif (bad_edges[0] in self.front_edges and bad_edges[1] not in self.front_edges) or (bad_edges[0] not in self.front_edges and bad_edges[1] in self.front_edges):
			self.f()
			ans.append('f')

		#when both bad edges are not in front then call one in front and rotate fron
		elif (bad_edges[0] not in self.front_edges and bad_edges[1] not in self.front_edges):
			
			if(bad_edges[0] in [10,12] and bad_edges[1] in [10,12]):
				self.r2()
				ans.append('r2')
			elif(bad_edges[0] in [5,6,9] or bad_edges[1] in [5,6,9]):
				while not self.is_bad_edge(1):
					self.u()
					ans.append('u')
			elif(bad_edges[0] in [7,8,11] or bad_edges[1] in [7,8,11]):
				while not self.is_bad_edge(3):
					self.d()
					ans.append('d')
			self.f()
			ans.append('f')

	def move_bad_edges_to_front(self,edge_no):
		if edge_no == 1:
			moves = {'u':self.u,'d':self.d,'r':self.r,'l':self.l,'f':self.f,'b':self.b}
			move_name = {'u':'u','d':'d','r':'r','l':'l','f':'f','b':'b'}
		elif edge_no == 2:
			moves = {'u':self.r,'d':self.l,'r':self.d,'l':self.u,'f':self.f,'b':self.b}
			move_name = {'u':'r','d':'l','r':'d','l':'u','f':'f','b':'b'}
		elif edge_no == 3:
			moves = {'u':self.d,'d':self.u,'r':self.l,'l':self.r,'f':self.f,'b':self.b}
			move_name = {'u':'d','d':'u','r':'l','l':'r','f':'f','b':'b'}
		elif edge_no == 4:
			moves = {'u':self.l,'d':self.r,'r':self.u,'l':self.d,'f':self.f,'b':self.b}
			move_name = {'u':'l','d':'r','r':'u','l':'d','f':'f','b':'b'}

		back_edge = edge_no + 8

		bottom_edges = {1:[7,8],2:[5,8],3:[5,6],4:[6,7]}

		for i in range(4):
			if self.is_bad_edge(edge_no):
				try:
					ans.extend([move_name['u']]*(i))
				except:
					pass
				return 'first'
			moves['u']()
		
		for i in range(4):
			print("====================================== here",self.get_bad_edges(),back_edge)
			self.print_cube_with_faces()
			if self.is_bad_edge(back_edge):
				try:
					ans.extend([move_name['b']]*(i))
				except:
					pass
				moves['u']()
				moves['u']()
				ans.append(move_name['u'])
				ans.append(move_name['u'])
				return 'Second'
			moves['b']()

		if is_bad_edge(bottom_edges[edge_no][0]):
			moves['r']()
			moves['r']()
			moves['u']()
			moves['r']()
			moves['r']()
			ans.extend([move_name['r'],move_name['r'],move_name['u'],move_name['r'],move_name['r']])
			return 'Third'

		if is_bad_edge(bottom_edges[edge_no][1]):
			moves['l']()
			moves['l']()
			moves['u']()
			moves['u']()
			moves['u']()
			moves['l']()
			moves['l']()
			ans.extend([move_name['l'],move_name['l'],move_name['u'],move_name['u'],move_name['u'],move_name['l'],move_name['l']])
			return 'Fourth'
	#solve bad edges of the cube
	def solve_bad_edges(self):
		t=3
		while t:
			bad_edges = self.get_bad_edges()
			len_bad_edges = len(bad_edges)
			if  len_bad_edges % 2:
				print(bad_edges)
				print("Invalid State")
				return False
			elif len_bad_edges == 0:
				return True
			elif len_bad_edges == 2 :
				print("======================================",t,self.get_bad_edges())
				self.print_cube_with_faces()
				self.from_two_bad_edges_to_four(bad_edges)
				self.print_cube_with_faces()
				print("======================================",t,self.get_bad_edges())
			for i in range(4):
				self.move_bad_edges_to_front(i+1)
			self.f()
			ans.append('f')
			t-=1


	#to set upper or down layer for setting cross on top and down 
	def set_opposite_to_ro(self,a,b): #a is index of upper face and b is index of down face where we need to set blank
		flag = False
		for i in range(1,9,2):	#checks if there is any space in upper face
			if self.up[i] != 'r' and self.up[i] != 'o':
				flag = True
				break
		if flag:
			while (self.up[a] == 'o' or self.up[a] == 'r'):	#rotate until it sets the blank(!r !o) in that place
				self.u()
				ans.append('u')
			return 'u'
		else:
			while (self.down[b] =='o' or self.down[b] =='r'): #rotate until it sets the blank(!r !o) in that place
				self.d()
				ans.append('d')	
			return 'd'

	#It will set red orange edges to top and down faces
	#there can be only four posibilities as shown below in conditions
	def make_ro_cross(self):
		if(self.front[5]=='r' or self.front[5]=='o'):
			face_set = self.set_opposite_to_ro(1,7)
			if face_set == 'u':
				self.r()
				self.u()
				self.r1()
				ans.extend(['r','u','r1'])
			elif face_set == 'd':
				self.r1()
				self.d1()
				self.r()
				ans.extend(['r1','d1','r'])

		if self.front[3]=='r' or self.front[3]=='o':
			face_set = self.set_opposite_to_ro(1,7)
			if face_set == 'u':
				self.l1()
				self.u1()
				self.l()
				ans.extend(['l1','u1','l'])
			elif face_set == 'd':
				self.l()
				self.d()
				self.l1()
				ans.extend(['l','d','l1'])
		if (self.back[3]=='r' or self.back[3]=='o'):
			face_set = self.set_opposite_to_ro(7,1)	
			if face_set == 'u':
				self.r1()
				self.u1()
				self.r()
				ans.extend(['r1','u1','r'])
			elif face_set == 'd':
				self.r()
				self.d()
				self.r1()
				ans.extend(['r','d','r1'])
		if self.back[5]=='r' or self.back[5]=='o':
			face_set = self.set_opposite_to_ro(7,1)
			if face_set == 'u':
				self.l()
				self.u()
				self.l1()
				ans.extend(['l','u','l1'])
			elif face_set == 'd':
				self.l1()
				self.d1()
				self.l()
				ans.extend(['l1','d1','l'])
		
	def set_ro_corners(self):
		while(not self.check_ro_corners()):
			# print('--------------------------------------------')
			# print(ans)
			# self.print_cube_with_faces()
			flag_upper_line = flag_down_line = flag_up = flag_down =0
			ro = ['r','o'] 
			for i in [self.front,self.right,self.back,self.left]:
				if i[0] in ro or i[2] in ro:
					flag_upper_line = 1
				if i[6] in ro or i[8] in ro:
					flag_down_line = 1
			# print(flag_down_line,flag_upper_line)
			if flag_down_line and flag_upper_line:
				# print("here")
				for i in [self.front,self.right,self.back,self.left]:
					if i[0] in ro:
						flag_up = 1
					if i[6] in ro:
						flag_down = 1
				if flag_down :
					while self.front[6] not in ro:
						self.d()
						ans.append('d')
					if flag_up:
						while self.right[0] not in ro:
							self.u()
							ans.append('u')
					else : 
						while self.front[2] not in ro:
							self.u()
							ans.append('u')

					self.l()
					self.d1()
					self.r2()
					self.d()
					self.l1()
					ans.extend(['l','d1','r2','d','l1'])
				elif not flag_down and flag_up:
					while self.front[0] not in ro:
						self.u()
						ans.append('u')
					while self.front[8] not in ro:
						self.d()
						ans.append('d')

					self.r1()
					self.d()
					self.l2()
					self.d1()
					self.r()
					ans.extend(['r1','d','l2','d1','r'])
				else:
					while self.front[2] not in ro:
						self.u()
						ans.append('u')
					while self.front[8] not in ro:
						self.d()
						ans.append('d')
					self.r2()
					ans.append('r2')
					while self.front[6] not in ro:
						self.d()
						ans.append('d')
					while self.right[0] not in ro:
						self.u()
						ans.append('u')					
					self.l()
					self.d1()
					self.r2()
					self.d()
					self.l1()
					ans.extend(['l','d1','r2','d','l1'])
			else:
				unset_corners = self.give_unset_corners()
				if flag_down_line:
					unset_corners = sorted(unset_corners['down'])
				else:
					unset_corners = sorted(unset_corners['up'])

				if len(unset_corners) >= 3:
					self.f2()
					ans.append('f2')
				elif len(unset_corners) == 2:
					if unset_corners[0] == 0:
						if unset_corners[1] in [2,7]:
							self.r2()
							ans.append('r2')
						elif unset_corners[1] == 6:
							self.f2()
							ans.append('f2')
					elif unset_corners[0] == 2:
						self.f2()
						ans.append('f2')
					elif unset_corners[0] == 3:
						self.r2()
						ans.append('r2')
			
if __name__ == '__main__':
	ans = []
	# cube = mycube()
	f =first_phase()
	# f.print_cube_with_faces()
	f.solve_bad_edges()
	print("------------------------------------------------solved bad edges--------------------------")
	print(f.get_bad_edges())
	f.print_cube_with_faces()
	# print(f.get_bad_edges())

	# f.make_ro_cross()
	# print("------------------------------------------------ro cross-----------------------------------")
	# f.print_cube_with_faces()
	# f.set_ro_corners()
	# print("------------------------------------------------Up and down side settled--------------------------")
	# f.print_cube_with_faces()
	# print(ans)
	# print ()
	# f.make_ro_cross()
	# f.print_cube_with_faces()