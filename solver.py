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
<<<<<<< HEAD
		
=======

>>>>>>> 7829c3ef2687ce531149f12f2db6e21105e74207
	def f1(self):
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
<<<<<<< HEAD
		
	def f2(self):
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=self.rotate(self.front,self.up,self.right,self.down,self.left,'f')
		
	def u(self):
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'t')
		
	def u1(self):
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'t')
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'t')
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'t')
		
	def u2(self):
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'t')
		self.up,self.back,self.right,self.front,self.left=self.rotate(self.up,self.back,self.right,self.front,self.left,'t')
		
	def b(self):
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		
=======

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

>>>>>>> 7829c3ef2687ce531149f12f2db6e21105e74207
	def b1(self):
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
<<<<<<< HEAD
		
	def b2():
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		
=======

	def b2(self):
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=self.rotate(self.back,self.up,self.left,self.down,self.right,'b')

>>>>>>> 7829c3ef2687ce531149f12f2db6e21105e74207
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

<<<<<<< HEAD
	#status return methods

	def get_edge(self,edgeNum):
		if(edgeNum==1):
			return [-1,self.up[7],self.front[1]]
		if(edgeNum==2):
			return [self.right[3],-1,self.front[5]]
		if(edgeNum==3):
			return [-1,self.down[1],self.front[7]]
		if(edgeNum==4):
			return [self.left[5],-1,self.front[3]]
		if(edgeNum==5):
			return [self.left[1],self.up[3],-1]
		if(edgeNum==6):
			return [self.right[1],self.up[5],-1]
		if(edgeNum==7):
			return [self.right[7],self.down[5],-1]
		if(edgeNum==8):
			return [self.left[7],self.down[3],-1]
		if(edgeNum==9):
			return [-1,self.up[1],self.back[1]]
		if(edgeNum==10):
			return [self.right[5],-1,self.back[3]]
		if(edgeNum==11):
			return [-1,self.down[7],self.back[7]]
		if(edgeNum==12):
			return [self.left[3],-1,self.back[5]]
if __name__ == '__main__':
	cube = mycube()
	cube.print_cube()
	#cube.f2()
	for i in range(1,13):
		print i,cube.get_edge(i)
	#cube.print_cube()
=======
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

# class first_phase(mycube):
	

		

if __name__ == '__main__':
	cube = mycube()
	cube.print_cube()
	# cube.d()
	# cube.print_cube()
	for i in range(1,9):
		print(cube.get_corner(i))
>>>>>>> 7829c3ef2687ce531149f12f2db6e21105e74207
	# print(cube.right)

