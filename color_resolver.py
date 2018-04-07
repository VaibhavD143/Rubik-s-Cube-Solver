class color_resolver():
	
		
	def rgb2hsv(self,r,g,b):
		v = max(r,g,b)
		m = min(r,g,b)
		h = None
		s = None
		delta = v - m
		if v == m and v <127:
			return 0,0,0
		if v == m and v >=127:
			return 0,0,100
		if v != 0:
			s = delta / (v*1.0)
		else:
			s = 0
			h = -1
			return h,s,v

		if r == v:
			h = (g-b)/(delta*1.0)
		elif g == v:
			h = 2 + (b-r)/(delta*1.0)
		elif b == v:
			h = 4 + (r-g)/(delta*1.0)
		h *= 60	
		if h<0:
			h+=360
		return h,s*100,(v/255.0)*100
	def resolve_color(self,h,s,v):
		if s <= 10 and v >= 80:
			return 'w'
		if s >= 60 and v >= 60:
			return self.hue_to_color_approx(h)
		else:
			return -1
	def hue_to_color_approx(self,hue):
		if (hue >= 0 and hue <12) or (hue > 348 and hue < 360):
			return 'r'
		elif hue < 165 and hue > 75:
			return 'g'
		elif hue < 270 and hue > 200:
			return 'b'
		elif hue < 70 and hue > 50:
			return 'y'
		elif hue < 40 and hue > 15:
			return 'o'

