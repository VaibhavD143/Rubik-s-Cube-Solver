class mycube():
	def __init__(self):
		self.front = ['w','w','b','y','b','b','r','b','r']
		self.back = ['g','y','b','r','g','r','g','g','g']
		self.left = ['r','w','o','g','y','r','w','b','b']
		self.right = ['y','y','o','y','w','b','y','w','o']
		self.up = ['y','g','w','o','r','o','b','g','o']
		self.down = ['w','o','g','w','o','r','r','o','y']


	def rotate(self,face,up,right,down,left,name):
		r_face = face
		r_up = up
		r_right = right
		r_down = down
		r_left = left
		
		
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
		r_face[4] = front[4]
		r_face[5] = front[1]
		r_face[6] = front[8]
		r_face[7] = front[5]
		r_face[8] = front[2]

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

if __name__ == '__main__':
	cube = mycube()
	cube.r()
	print(cube.front)

