from notation import *
from second_phase import *
from third_phase import *
from datetime import datetime
from first_phase import *
from solution import solution
from cube_input_verifier import cube_input_verifier

class cube_solver():
	# this class is intended for controlling the solving process like creating objects for different phases and calling their solver methods 
	def __init__(self,input):
		self.input = input
		self.up = input['u']
		self.down = input['d']
		self.back = input['b']
		self.front = input['f']
		self.right = input['r']
		self.left = input['l']
	
	def ans_shortner(self,ans):
		final_ans = []
		if len(ans) > 0:
			current = self.get_current(ans[0])
			count = 0
			for move in ans:
				if self.get_current(move) == current:
					if move[len(move)-1] == '1':
						count+=3
					elif move[len(move)-1] == '2':
						count+=2
					else:
						count+=1
				else: 
					count = count%4
					if count == 1:
						final_ans.append(current)
					elif count == 2:
						final_ans.append(current+'2')
					elif count == 3:
						final_ans.append(current+'1')
					current = self.get_current(move)
					count = 0
					if move[len(move)-1] == 1:
						count+=3
					elif move[len(move)-1] == 2:
						count+=2
					else:
						count+=1
			
			count = count%4
			if count == 1:
				final_ans.append(current)
			elif count == 2:
				final_ans.append(current+'2')
			elif count == 3:
				final_ans.append(current+'1')
		return final_ans

	def solve(self):

		verifier = cube_input_verifier(self.input)

		if not verifier.full_verify():
			sol = solution()
			sol.status = 0
			return sol

		ans = []
		ini = datetime.now()

		cube = mycube(self.input)

		f =first_phase(cube)
		ans.extend(f.solve())
		
		s =second_phase(f)
		ans.extend(s.solve())
	
		t = third_phase(s)
		ans.extend(t.solve())
		
		end = datetime.now()
		exec_time = (end - ini).microseconds

		ans = self.ans_shortner(ans)

		sol = solution()
		sol.ans = ans
		sol.time = exec_time
		sol.length = len(ans)
		sol.status = 1

		return sol

	def get_current(self,move):
		if move[0] == 'm':
			return move[0]+move[1]
		else:
			return move[0]