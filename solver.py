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
	
	# def move_edge_to_front(self,no,pos):
		
	# 	if(no in [10,12]):
	# 		self.r2()
	# 		ans.append('r2')
	# 	elif(no in [5,6,9]):
	# 		while not self.is_bad_edge(1):
	# 			self.u()
	# 			ans.append('u')
	# 	elif(no in [7,8,11]):
	# 		while not self.is_bad_edge(3):
	# 			self.d()
	# 			ans.append('d')
		

	# def move_bad_edges_to_front(self,bad_edges):
	# 	cnt = 0
	# 	while bad_edges[cnt] in front_edges:
	# 		cnt+=1

		
	#solve bad edges of the cube
	def solve_bad_edges(self):
		bad_edges = self.get_bad_edges()
		len_bad_edges = len(bad_edges)
		if  len_bad_edges % 2:
			print(bad_edges)
			print("Invalid State")
			return
		elif len_bad_edges == 2 :
			self.from_two_bad_edges_to_four(bad_edges)

		self.move_bad_edges_to_front(bad_edges)

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
		else:
			while (self.down[b] =='o' or self.down[b] =='r'): #rotate until it sets the blank(!r !o) in that place
				self.d()
				ans.append('d')	

	#It will set red orange edges to top and down faces
	#there can be only four posibilities as shown below in conditions
	def make_ro_cross(self):
		if(self.front[5]=='r' or self.front[5]=='o'):
			self.set_opposite_to_ro(1,7)
			if ans[-1] == 'u':
				self.r()
				self.u()
				self.r1()
				ans.append(['r','u','r1'])
			elif ans[-1] == 'd':
				self.r1()
				self.d1()
				self.r()
				ans.append(['r1','d1','r'])

		if self.front[3]=='r' or self.front[3]=='o':
			self.set_opposite_to_ro(1,7)
			if ans[-1] == 'u':
				self.l1()
				self.u1()
				self.l()
				ans.append(['l1','u1','l'])
			elif ans[-1] == 'd':
				self.l()
				self.d()
				self.l1()
				ans.append(['l','d','l1'])
		if (self.back[3]=='r' or self.back[3]=='o'):
			self.set_opposite_to_ro(7,1)	
			if ans[-1] == 'u':
				self.r1()
				self.u1()
				self.r()
				ans.append(['r1','u1','r'])
			elif ans[-1] == 'd':
				self.r()
				self.d()
				self.r1()
				ans.append(['r','d','r1'])
		if self.back[5]=='r' or self.back[5]=='o':
			# print('in',ans)
			self.set_opposite_to_ro(7,1)
			if ans[-1] == 'u':
				self.l()
				self.u()
				self.l1()
				ans.append(['l','u','l1'])
			elif ans[-1] == 'd':
				self.l1()
				self.u1()
				self.l()
				ans.append(['r1','d1','r'])
		
		def set_ro_corners(self):
			while(!self.check_ro_corners()):
				flag_down = flag_up = 0
				falg = 0
				ro = ['r','o'] 
				if self.up[0] in ro or self.right[0] in ro



				for i in [self.front,self.right,self.back,self.left]:
					if i[0] in ro:
						flag_up = 1
					if i[6] in ro:
						flag_down = 1
				if flag_down  :
					while self.front[6] not in ro:
						self.d()
						ans.append('d')
					if flag_up:
						while self.right[0] not in ro:
							self.u()
							ans.append('u')
					else : 
						while self.right[2] not in ro:
							self.u()
							ans.append('u')

					self.l()
					self.d1()
					self.r2()
					self.d()
					self.l1()
					ans.append(['l','d1','r2','d','l1'])

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
					ans.append(['r1','d','l2','d1','r'])
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
					ans.append(['l','d1','r2','d','l1'])



if __name__ == '__main__':
	ans = []
	# cube = mycube()
	f =first_phase()
	f.make_ro_cross()
	print(ans)
	# print(f.get_bad_edges())
	# f.l1()
	# f.d()
	# f.r1()

	# print(f.get_bad_edges())
	# f.print_cube()
	# print(f.solve_bad_edges())
	# while(len(f.get_bad_edges())):
	# 	f.solve_bad_edges()