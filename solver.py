from notation import *


class first_phase(mycube):

	global ans
	front_edges = [1,2,3,4]

	def solve_two_bad_edges(self,bad_edges):
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


		elif (bad_edges[0] in self.front_edges and bad_edges[1] not in self.front_edges) or (bad_edges[0] not in self.front_edges and bad_edges[1] in self.front_edges):
			self.f()
			ans.append('f')

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

		

	def solve_bad_edges(self):
		bad_edges = self.get_bad_edges()
		len_bad_edges = len(bad_edges)
		if  len_bad_edges % 2:
			print(bad_edges)
			print("Invalid State")
			return
		elif len_bad_edges == 2 :
			self.solve_two_bad_edges(bad_edges)

		self.move_bad_edges_to_front(bad_edges)

	def set_opposite_to_ro(self,a,b):
		flag = False
		for i in range(1,9,2):
			if self.up[i] != 'r' and self.up[i] != 'o':
				flag = True
				break
		if flag:
			while (self.up[a] == 'o' or self.up[a] == 'r'):
				self.u()
				ans.append('u')
		else:
			while (self.down[b] =='o' or self.down[b] =='r'):
				self.d()
				ans.append('d')	

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

if __name__ == '__main__':
	ans = []
	# cube = mycube()
	f =first_phase()
	f.u1()
	f.r()
	f.u()
	f.r1()
	f.u1()
	f.l1()
	f.u1()
	f.l()
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