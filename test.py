from color_resolver import color_resolver
"""from cube_solver import *
from solution import solution
input = {'f':['b','y','y','r','b','b','o','w','b'],
		 'b':['b','g','g','b','g','r','o','w','g'],
		 'u':['w','y','w','w','r','o','o','o','o'],
		 'd':['w','b','r','y','o','o','y','r','y'],
		 'l':['r','g','w','g','y','b','r','r','g'],
		 'r':['g','w','r','y','w','o','y','g','b']
		}
solver = cube_solver(input)
ans = solver.solve()
print(ans.length)
print(ans.ans)
print(ans.time)
print(ans.status)"""
cr = color_resolver()
h,s,v = cr.rgb2hsv(255,100,0)
print(h,s,v)
print(cr.resolve_color(h,s,v))