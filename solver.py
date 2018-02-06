class mycube():
	def __init__(self):
		self.front = ['g','w','o','g','b','y','g','r','o']
		self.back = ['b','b','y','o','g','o','b','b','y']
		self.left = ['b','o','w','g','y','w','g','r','w']
		self.right = ['y','r','w','b','w','y','y','g','w']
		self.up = ['r','o','o','w','r','w','r','b','g']
		self.down = ['o','g','b','y','o','y','r','r','r']


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
		self.front,self.up,self.right,self.down,self.left=rotate(self.front,self.up,self.right,self.down,self.left,'f')
		
	def f1(self):
		self.front,self.up,self.right,self.down,self.left=rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=rotate(self.front,self.up,self.right,self.down,self.left,'f')
		
	def f2():
		self.front,self.up,self.right,self.down,self.left=rotate(self.front,self.up,self.right,self.down,self.left,'f')
		self.front,self.up,self.right,self.down,self.left=rotate(self.front,self.up,self.right,self.down,self.left,'f')
		
	def u():
		self.up,self.back,self.right,self.front,self.left=rotate(self.up,self.back,self.right,self.front,self.left,'t')
		
	def u1():
		self.up,self.back,self.right,self.front,self.left=rotate(self.up,self.back,self.right,self.front,self.left,'t')
		self.up,self.back,self.right,self.front,self.left=rotate(self.up,self.back,self.right,self.front,self.left,'t')
		self.up,self.back,self.right,self.front,self.left=rotate(self.up,self.back,self.right,self.front,self.left,'t')
		
	def u2():
		self.up,self.back,self.right,self.front,self.left=rotate(self.up,self.back,self.right,self.front,self.left,'t')
		self.up,self.back,self.right,self.front,self.left=rotate(self.up,self.back,self.right,self.front,self.left,'t')
		
	def b():
		self.back,self.up,self.left,self.down,self.right=rotate(self.back,self.up,self.left,self.down,self.right,'b')
		
	def b1():
		self.back,self.up,self.left,self.down,self.right=rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=rotate(self.back,self.up,self.left,self.down,self.right,'b')
		
	def b2():
		self.back,self.up,self.left,self.down,self.right=rotate(self.back,self.up,self.left,self.down,self.right,'b')
		self.back,self.up,self.left,self.down,self.right=rotate(self.back,self.up,self.left,self.down,self.right,'b')
		
	def d(self):
		self.down,self.front,self.right,self.back,self.left=rotate(self.down,self.front,self.right,self.back,self.left,'d')

	def d1(self):
		self.down,self.front,self.right,self.back,self.left=rotate(self.down,self.front,self.right,self.back,self.left,'d')
		self.down,self.front,self.right,self.back,self.left=rotate(self.down,self.front,self.right,self.back,self.left,'d')
		self.down,self.front,self.right,self.back,self.left=rotate(self.down,self.front,self.right,self.back,self.left,'d')

	def d2(self):
		self.down,self.front,self.right,self.back,self.left=rotate(self.down,self.front,self.right,self.back,self.left,'d')
		self.down,self.front,self.right,self.back,self.left=rotate(self.down,self.front,self.right,self.back,self.left,'d')

	def l(self):
		self.left,self.up,self.front,self.down,self.back=rotate(self.left,self.up,self.front,self.down,self.back,'l')

	def l1(self):
		self.left,self.up,self.front,self.down,self.back=rotate(self.left,self.up,self.front,self.down,self.back,'l')
		self.left,self.up,self.front,self.down,self.back=rotate(self.left,self.up,self.front,self.down,self.back,'l')
		self.left,self.up,self.front,self.down,self.back=rotate(self.left,self.up,self.front,self.down,self.back,'l')

	def l2(self):
		self.left,self.up,self.front,self.down,self.back=rotate(self.left,self.up,self.front,self.down,self.back,'l')
		self.left,self.up,self.front,self.down,self.back=rotate(self.left,self.up,self.front,self.down,self.back,'l')

	def r(self):
		self.right,self.up,self.back,self.down,self.front=rotate(self.right,self.up,self.back,self.down,self.front,'r')

	def r1(self):
		self.right,self.up,self.back,self.down,self.front=rotate(self.right,self.up,self.back,self.down,self.front,'r')
		self.right,self.up,self.back,self.down,self.front=rotate(self.right,self.up,self.back,self.down,self.front,'r')
		self.right,self.up,self.back,self.down,self.front=rotate(self.right,self.up,self.back,self.down,self.front,'r')

	def r2(self):
		self.right,self.up,self.back,self.down,self.front=rotate(self.right,self.up,self.back,self.down,self.front,'r')
		self.right,self.up,self.back,self.down,self.front=rotate(self.right,self.up,self.back,self.down,self.front,'r')

if __name__ == '__main__':
	cube = mycube()
	cube.print_cube()
	cube.r()
	cube.print_cube()
	# print(cube.right)

