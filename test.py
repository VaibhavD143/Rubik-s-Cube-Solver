# from color_resolver import color_resolver
from cube_solver import *
from solution import solution
from webcam import *

sc = scan_cube()
colors = sc.get_rgb_of_all_faces()
faces = ['f','b','l','r','u','d']
input = {}

for face in faces:
	input[face] = list(colors[face].values())


# input = {'f':['w','r','r','g','b','o','r','r','b'],
# 		 'b':['g','y','y','r','g','b','b','r','y'],
# 		 'u':['o','g','w','o','r','b','g','b','w'],
# 		 'd':['y','g','o','y','o','g','o','y','y'],
# 		 'l':['g','y','r','o','y','o','b','b','g'],
# 		 'r':['b','w','o','w','w','w','w','w','r']
# 		}
solver = cube_solver(input)
debug = True
ans = solver.solve(debug)
print("=============================RESULTS===============================")
print("Total steps to solve: ",ans.length)
print("Steps to folow: ",ans.ans)
print("Time taken by program to execute :",ans.time,"secs")
print("Yipee! SOLVED") if ans.status else print("Can't be solved")
