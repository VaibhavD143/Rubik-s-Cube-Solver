class mycube():
	def __init__(self):
		self.front = ['w','b','y','w','b','r','y','g','o']
		self.back = ['g','y','o','w','g','o','b','b','y']
		self.left = ['b','r','g','g','y','o','g','b','g']
		self.right = ['b','y','w','g','w','g','b','o','w']
		self.up = ['y','b','r','w','r','r','o','o','r']
		self.down = ['o','y','w','w','o','y','r','r','r']


	def rotate(self,face,up,right,down,left,name):
		r_face = face[:]
		r_up = up[:]
		r_right = right[:]
		r_down = down[:]
		r_left = left[:]
		
		
		index = { 'f' : [[6,7,8],[0,3,6],[2,1,0],[8,5,2]],
				  'b' : [[2,1,0],[0,3,6],[6,7,8],[8,5,2]],
				  'l' :	[[0,3,6],[0,3,6],[0,3,6],[8,5,2]],
				  'r' : [[8,5,2],[0,3,6],[8,5,2],[8,5,2]],
				  'u' : [[2,1,0],[2,1,0],[2,1,0],[2,1,0]],
				  'd' : [[6,7,8],[6,7,8],[6,7,8],[6,7,8]]
				}

		#update face side of rotation 
		r_face[0] = face[6]
		r_face[1] = face[3]
		r_face[2] = face[0]
		r_face[3] = face[7]
		r_face[4] = face[4]
		r_face[5] = face[1]
		r_face[6] = face[8]
		r_face[7] = face[5]
		r_face[8] = face[2]
		# print(face)
		# print(r_face)
		#update other four sides
		if name == 'b':
			loop = index['b']
		elif name == 'f':
			loop = index['f']
		elif name == 'r':
			loop = index['r']
		elif name == 'l':
			loop = index['l']
		elif name == 'u':
			loop = index['u']
		elif name == 'd':
			loop = index['d']

		r_up[loop[0][0]] = left[loop[3][0]] 
		r_up[loop[0][1]] = left[loop[3][1]] 
		r_up[loop[0][2]] = left[loop[3][2]]

		r_right[loop[1][0]] = up[loop[0][0]] 
		r_right[loop[1][1]] = up[loop[0][1]] 
		r_right[loop[1][2]] = up[loop[0][2]]

		r_down[loop[2][0]] = right[loop[1][0]]
		r_down[loop[2][1]] = right[loop[1][1]]
		r_down[loop[2][2]] = right[loop[1][2]]

		r_left[loop[3][0]] = down[loop[2][0]]
		r_left[loop[3][1]] = down[loop[2][1]]
		r_left[loop[3][2]] = down[loop[2][2]]

		return r_face,r_up,r_right,r_down,r_left

	def r(self):
		# print(self.right)
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')
		# print(self.right)

	def print_cube(self):
		print('Current State of cube:')
		print('front:',self.front)
		print('Back: ',self.back)
		print('left: ',self.left)
		print('right:',self.right)
		print('up:   ',self.up)
		print('down: ',self.down)

	def f(self):
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')

	def f1(self):
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')

	def f2(self):
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')

	def u(self):
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'u')

	def u1(self):
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'u')
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'u')
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'u')

	def u2(self):
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'u')
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'u')

	def b(self):
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')

	def b1(self):
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')

	def b2(self):
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')

	def d(self):
		self.down,self.front,self.right,self.back,self.left=self.rotate(self.down,self.front,self.right,self.back,self.left,'d')

	def d1(self):
		self.down,self.front,self.right,self.back,self.left=self.rotate(self.down,self.front,self.right,self.back,self.left,'d')
		self.down,self.front,self.right,self.back,self.left=self.rotate(self.down,self.front,self.right,self.back,self.left,'d')
		self.down,self.front,self.right,self.back,self.left=self.rotate(self.down,self.front,self.right,self.back,self.left,'d')

	def d2(self):
		self.down,self.front,self.right,self.back,self.left=self.rotate(self.down,self.front,self.right,self.back,self.left,'d')
		self.down,self.front,self.right,self.back,self.left=self.rotate(self.down,self.front,self.right,self.back,self.left,'d')

	def l(self):
		self.left,self.up,self.front,self.down,self.back=self.rotate(self.left,self.up,self.front,self.down,self.back,'l')

	def l1(self):
		self.left,self.up,self.front,self.down,self.back=self.rotate(self.left,self.up,self.front,self.down,self.back,'l')
		self.left,self.up,self.front,self.down,self.back=self.rotate(self.left,self.up,self.front,self.down,self.back,'l')
		self.left,self.up,self.front,self.down,self.back=self.rotate(self.left,self.up,self.front,self.down,self.back,'l')

	def l2(self):
		self.left,self.up,self.front,self.down,self.back=self.rotate(self.left,self.up,self.front,self.down,self.back,'l')
		self.left,self.up,self.front,self.down,self.back=self.rotate(self.left,self.up,self.front,self.down,self.back,'l')

	def r(self):
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')

	def r1(self):
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')

	def r2(self):
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')
		self.right,self.up,self.back,self.down,self.front=self.rotate(self.right,self.up,self.back,self.down,self.front,'r')

	def get_corner(self,no):
		if no == 1:
			return self.left[2],self.up[6],self.front[0]
		elif no == 2:
			return self.right[0],self.up[8],self.front[2]
		elif no == 3:
			return self.right[6],self.down[2],self.front[8]
		elif no == 4:
			return self.left[8],self.down[0],self.front[6]
		elif no == 5:
			return self.left[0],self.up[0],self.back[2]
		elif no == 6:
			return self.right[2],self.up[2],self.back[0]
		elif no == 7:
			return self.right[8],self.down[8],self.back[6]
		elif no == 8:
			return self.left[6],self.down[6],self.back[8]
		else:
			return False,False,False

	def is_bad_edge(self,no):
		
		x,y,z = self.get_edges(no)
		
		if no == 1 and (y == 'y' or y == 'w' or z == 'o' or z == 'r'):
			return True
		elif no == 2 and (z == 'y' or z == 'w' or x == 'o' or x == 'r'):
			return True
		elif no == 3 and (y == 'y' or y == 'w' or z == 'o' or z == 'r'):
			return True
		elif no == 4 and (z == 'y' or z == 'w' or x == 'o' or x == 'r'):
			return True
		elif no == 5 and (x == 'o' or x == 'r' or y == 'w' or y == 'y'):
			return True
		elif no == 6 and (x == 'o' or x == 'r' or y == 'w' or y == 'y'):
			return True
		elif no == 7 and (x == 'o' or x == 'r' or y == 'y' or y == 'w'):
			return True
		elif no == 8 and (x == 'o' or x == 'r' or y == 'y' or y == 'w'):
			return True
		elif no == 9 and (z == 'o' or z == 'r' or y == 'y' or y == 'w'):
			return True
		elif no == 10 and (z == 'w' or z == 'y' or x == 'o' or x == 'r'):
			return True
		elif no == 11 and (z == 'o' or z == 'r' or y == 'y' or y == 'w'):
			return True
		elif no == 12 and (z == 'w' or z == 'y' or x == 'o' or x == 'r'):
			return True




class first_phase(mycube):
	
	def get_bad_edges(self):
		bad_edges = []
		for i in range(1,13):
			if self.is_bad_edge(i):
				bad_edges.append(i)
		print(bad_edges)
		return bad_edges

		

if __name__ == '__main__':
	cube = mycube()
	# cube.print_cube()
	# cube.d()
	# cube.print_cube()
	# for i in range(1,9):
		# print(cube.get_corner(i))
	# print(cube.right)
	f =first_phase()
	print(f.get_bad_edges())

