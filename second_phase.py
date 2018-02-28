from notation import *

class second_phase(mycube):
	global ans

	def get_conflicting_corners(self,face):
		#returns conflicting corners of up face if face=0 else returns conflicting corners of down face
		count = 0
		conflicting_corner=[]
		if face == 0:
			for i in range(0,3,2):
			if self.up[i] == 'o':
				conflicting_corner.append(i)
				count+=1
			if self.up[i+6] == 'o':
				count+=1
				conflicting_corner.append(i+6)
		else:
			for i in range(0,3,2):
				if self.up[i] == 'r':
					conflicting_corner.append(i)
					count+=1
				if self.up[i+6] == 'r':
					count+=1
					conflicting_corner.append(i+6)

		return count,conflicting_corner

	def set_conflicting_corners(self):
		adjacent_corner = {0:2,2:0,6:8,8:6}
		while True:
			n_conflicting_corners,conflicting_corners = get_conflicting_corners(0)
			#no conflicting corners
			if n_conflicting_corners==0:
				break
			elif n_conflicting_corners==1:
				#rotate down face till upper conflicting corner is in cross-opposite of down-conflicting corner
				while self.down[adjacent_corner[conflicting_corners[0]]] != 'r':
					self.d()
					ans.append('d')
				#rotate face having upper-conflicting corner but down-conflicting twice
				if conflicting_corners[0] in [0,6]:
					self.l2()
					ans.append('l2')
				elif conflicting_corners[0] in [2,8]:
					self.r2()
					ans.append('r2')
			elif n_conflicting_corners==2:
				up_conf_corners = conflicting_corners
				down_conf_corners = get_conflicting_corners(1)

				if (is_adjacent(up_conf_corners[0],up_conf_corners[1])) and (is_adjacent(down_conf_corners[0],down_conf_corners[1])):
					d1 = get_down_corner(up_conf_corners[0])
					d2 = get_down_corner(up_conf_corners[1])
					#rotate to set set conflicting corners of down face to down of conflicting upper corners
					while self.down[d1] != 'r' and self.down[d2] != 'r':
						self.d()
						ans.append('d')
					#rotate face having  all conflicting corners
					if (up_conf_corners[0] in [0,2]) and (up_conf_corners[1] in [0,2]):
						self.b2()
						ans.append('b2')
					elif (up_conf_corners[0] in [2,8]) and (up_conf_corners[1] in [2,8]):
						self.r2()
						ans.append('r2')
					elif (up_conf_corners[0] in [6,8]) and (up_conf_corners[1] in [6,8]):
						self.f2()
						ans.append('f2')
					elif (up_conf_corners[0] in [0,6]) and (up_conf_corners[1] in [0,6]):
						self.l2()
						ans.append('l2')
					break	
				elif (is_adjacent(up_conf_corners[0],up_conf_corners[1])) and (not is_adjacent(down_conf_corners[0],down_conf_corners[1])):
					#rotate face having two upper-conflicting corners
					if (up_conf_corners[0] in [0,2]) and (up_conf_corners[1] in [0,2]):
						self.b2()
						ans.append('b2')
					elif (up_conf_corners[0] in [2,8]) and (up_conf_corners[1] in [2,8]):
						self.r2()
						ans.append('r2')
					elif (up_conf_corners[0] in [6,8]) and (up_conf_corners[1] in [6,8]):
						self.f2()
						ans.append('f2')
					elif (up_conf_corners[0] in [0,6]) and (up_conf_corners[1] in [0,6]):
						self.l2()
						ans.append('l2')
				elif (not is_adjacent(up_conf_corners[0],up_conf_corners[1])) and  (is_adjacent(down_conf_corners[0],down_conf_corners[1])):
					#rotate face having two down-conflicting corners
					if (up_conf_corners[0] in [0,2]) and (up_conf_corners[1] in [0,2]):
						self.f2()
						ans.append('f2')
					elif (up_conf_corners[0] in [2,8]) and (up_conf_corners[1] in [2,8]):
						self.r2()
						ans.append('r2')
					elif (up_conf_corners[0] in [6,8]) and (up_conf_corners[1] in [6,8]):
						self.b2()
						ans.append('b2')
					elif (up_conf_corners[0] in [0,6]) and (up_conf_corners[1] in [0,6]):
						self.l2()
						ans.append('l2')
				elif (not is_adjacent(up_conf_corners[0],up_conf_corners[1])) and  (not is_adjacent(down_conf_corners[0],down_conf_corners[1])):
					#make upper conflicting diagonal perpendicular to down conflicting diagonal
					#then rotate face having one upper-conflicting to get case 1 of this else-if ladder
					if up_conf_corners[0] in [0,8]:
						
						if down_conf_corners[0] not in [0,8]:
							self.d()
							ans.append('d')
						
						self.r1()
						ans.append('r1')

					elif up_conf_corners[0] in [2,6]
						
						if down_conf_corners[0] not in [2,6]:
							self.d()
							ans.append('d')

						self.l1()
						ans.append('l1')

			elif n_conflicting_corners==3:
				#get 2 down-conflicting corners opposite to upper conflicting corner
				if (0 not in conflicting_corners) or (6 not in conflicting_corners):
					down_edges = [2,8]
				elif (2 not in conflicting_corners) or (8 not in conflicting_corners):
					down_edges = [0,6]
				#rotate till down corners are conflicting
				while self.down[down_edges[0]] != 'r' and self.down[down_edges[1]] != 'r':
					self.d()
					ans.append('d')
				#rotate face having 2 conflicting corners
				if down_edges[0]==2:
					self.r2()
					ans.append('r2')
				elif down_edges[0]==0:
					self.l2()
					ans.append('l2')
			elif n_conflicting_corners==4:
				self.r2() 
				self.l2()
				ans.extend(['r2','l2'])
				break

	def is_adjacent(self,a,b):
		adjacent_list = {0:[2,6] , 2:[0,8] , 6:[0,8] , 8:[2,6]}
		return a in adjacent_list[b] 
	def get_down_corner(self,a):
		down_dic = {0:6,2:8,6:0,8:2}
		return down_dic[a]