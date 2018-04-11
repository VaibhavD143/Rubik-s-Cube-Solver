# from color_resolver import color_resolver
from cube_solver import *
from solution import solution
from webcam import *

# sc = scan_cube()
# colors = sc.get_rgb_of_all_faces()
# faces = ['f','b','l','r','u','d']
# input = {}

# for face in faces:
# 	input[face] = list(colors[face].values())


input = {'f':['b','r','g','b','b','g','w','r','w'],
		 'b':['b','o','g','b','g','g','y','y','y'],
		 'u':['o','b','r','o','r','w','o','w','r'],
		 'd':['r','y','r','r','o','r','o','o','o'],
		 'l':['w','g','w','w','y','w','b','g','g'],
		 'r':['y','o','y','y','w','y','b','b','g']
		}

solver = cube_solver(input)
debug = True
ans = solver.solve(debug)
print("=============================RESULTS===============================")
print("Total steps to solve: ",ans.length)
print("Steps to folow: ",ans.ans)
print("Time taken by program to execute :",ans.time,"secs")
print("Yipee! SOLVED") if ans.status else print("Can't be solved")
