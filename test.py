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


input = {'f':['y','b','y','w','b','o','o','g','y'],
		 'b':['g','g','w','y','g','b','b','o','g'],
		 'u':['o','w','r','w','r','r','r','r','o'],
		 'd':['y','y','b','y','o','g','w','g','r'],
		 'l':['b','r','g','w','y','o','o','o','b'],
		 'r':['g','y','w','b','w','b','r','r','w']
		}
solver = cube_solver(input)
debug = True
ans = solver.solve(debug)
print("=============================RESULTS===============================")
print("Total steps to solve: ",ans.length)
print("Steps to folow: ",ans.ans)
print("Time taken by program to execute :",ans.time,"secs")
print("Yipee! SOLVED") if ans.status else print("Can't be solved")
