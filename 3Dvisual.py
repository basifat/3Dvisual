""" 3Dvisual.py
    
    Usage:
        3Dvisual.py -h
		3Dvisual.py [(--draw-axes) (--draw-reference) (--draw-ref-labels) (--sizeX=<number>) (--sizeY=<number>) (--sizeZ=<number>) (--draw-X-values) (--draw-Y-values) (--draw-Z-values)]
	
        

    Options:
		-h,--help              : show this help message
		--draw-axes            : example flag #1
		-dr,--draw-reference   : draw reference of plot
		-drf,--draw-ref-labels : draw reference labels
		-dxv,--draw-X-values   : draw X values on reference plot
		-dyv,--draw-Y-values   : draw Y values on reference plot		
		-dzv,--draw-Z-values   : draw Z values on reference plot
		-sxn,--sizeX=<number>  : Scale X by number 
		-syn,--sizeY=<number>  : Scale Y by number
		-szn,--sizeZ=<number>  : Scale Z by number
	
"""
import matplotlib.delaunay as triang
import matplotlib.text as textlabel
import matplotlib.colors as cl
import pylab
import random
import numpy
import numpy  as np 
import matplotlib.pyplot as plt
from docopt import docopt

class Draw(object):
	
	def __init__(self):
		self.xList = [] #This list holds the values corresponding to X from the CSV
		self.yList = [] #This list holds values corresponding to Y from the CSV
		self.zList = [] #This list holds values corresponding to Z from the CSV
		self.colourList = [] #This list holds values corresponding to colour from the CSV
		input_file = "test3.csv"
		with open(input_file, 'r') as input:
			lines = input.readlines()[1:]
			for line in lines:
				line = line.strip()
				if line:
					line = line.split("\t")
					x = line[0]
					y = line[1]
					z = line[2]
					colourhex = line[3]
					self.xList.append(x)
					self.yList.append(y)
					self.zList.append(z)
					self.colourList.append("#"+colourhex)
		len_xList = len(self.xList)
		len_yList = len(self.yList)
		len_zList = len(self.zList)
		len_colourList = len(self.colourList)
		x_min = int(min(self.xList)) #Min x value from csv data
		y_min = int(min(self.yList)) #Min y value from csv data
		z_min = int(min(self.zList)) #Min z value from csv data
		x_max = int(max(self.xList)) #Max x value from csv data
		y_max = int(max(self.yList)) #Max y value from csv data
		z_max = int(max(self.zList)) #Max z value from csv data
		#X,Y,Z min tuple
		self.min_xyz_values = (x_min,y_min,z_min) #Tuple holding the x,y, and z minimum values respectively
		self.max_xyz_values = (x_max,y_max,z_max) #Tuple holding the x,y and z maximum values respectively
		self.xyzcolour_len = (len_xList,len_yList,len_zList,len_colourList) #Tuple holding the len of x,y,z and colour list respectively
		colour = cl.hex2color(self.colourList[0])
		self.R = colour[0]
		self.G = colour[1]
		self.B = colour[2]
		
		
	def calc_triangulation(self):
		cens,edg,tri,neig = triang.delaunay(self.xList,self.yList)
		tri = numpy.array([tri])
		tri = tri[0]
		for t in tri:
		# t[0], t[1], t[2] are the points indexes of the triangle
		#Now we want to extract a complete triangle from each index
			t_i = [t[0], t[1], t[2], t[0]]
			#t_i = [t[0], t[1], t[2]]
			x = [self.xList[i] for i in t_i]
			y = [self.yList[i] for i in t_i]
			z = [self.zList[i] for i in t_i]
			colourhex = [self.colourList[i] for i in t_i]
			#Retrieve only the first item of the colour value since all the 3 points have same colour
			colourhex = colourhex[:1]
			#Convert to string so we can add to a new list and extract later on
			colourhex = "".join(colourhex)
			#Convert string values of triangle to int
			x = [int(i) for i in x]
			y = [int(i) for i in y]
			z = [int(i) for i in z]
			#For performance sake, we reuse the xList, yList, zList and colourList holding data from the
			#csv (insead of a new list lst_x e.t.c)
			#-----SWAP Z and Y in the plane of the plot----#
			self.xList.append(x)
			self.yList.append(y)
			self.zList.append(z)
			self.colourList.append(colourhex)
		#Update self.xList,self.yList,self.zList and self.colourList to the new data needed for triangulation
		self.xList[:100] = [] #Remove all values corresponding to X that was appended from csv
		self.yList[:100] = [] #Remove all values corresponding to Y that was appended from csv
		self.zList[:100] = [] #Remove all values corresponding to Z that was appended from csv
		self.colourList[:100] = [] #Remove all values corresponding to colour that was appended from csv

	def draw_triangulation(self):
		col = 0 #Start at column 0
		i = 0
		j = 1
		k = 2
		#colour = cl.hex2color(self.colourList[i])
		#R = colour[i]
		#G = colour[j]
		#B = colour[k]
		print "#gl_cmds="  #Before a new plot, clear the previous plot
		#Remember that we updated self.xList,self.yList,self.zList and self.colourList from the csv data values now to the data needed for triangulation or plotting
		
		while (col<len(self.xList)): #Iterate through the entire len of  xList
			#Access lists column after column
			#Swap y and Z for the plot plane
			xcol = self.xList[col] #Get all values corresponding to x from updated xList
			zcol = self.yList[col] #Get all values corresponding to y from updated yList
			ycol = self.zList[col] #Get all values corresponding to z from zList
			#Get out each individual items in the columns
			x1 = xcol[i] 
			x2 = xcol[j]
			x3 = xcol[k]
			y1 = ycol[i]
			y2 = ycol[j]
			y3 = ycol[k]
			z1 = zcol[i]
			z2 = zcol[j]
			z3 = zcol[k]
			gamma = 1.0
			thickness = 1.0
			R = self.R
			B = self.B
			G = self.G
			#Increament col by 1 after every iteration so that we can go on to the next column
			col = col + 1
			i = 0
			#The right traingulation plot
			print "line", x1,y1,z1,x2,y2,z2,thickness,R,G,B,gamma
			print "line", x2,y2,z2,x3,y3,z3,thickness,R,G,B,gamma
			print "line", x3,y3,z3,x1,y1,z1,thickness,R,G,B,gamma
			print "text", 0,y1,0,"ffffff", y1 #Draw x values 
			print "text", 0,y2,0,"ffffff", y2 #Draw x values 
			print "text", 0,y3,0,"ffffff", y3 #Draw x values 
			print "text", x1,0,0,"ffffff", x1 #Draw y values 
			print "text", x2,0,0,"ffffff", x2 #Draw y values 
			print "text", x3,0,0,"ffffff", x3 #Draw y values 
			print "text", 0,0,z1,"ffffff", z1 #Draw z values 
			print "text", 0,0,z2,"ffffff", z2 #Draw Z values 
			print "text", 0,0,z3,"ffffff", z3 #Draw Z values
				
			#print "text", x2,y2,z2,"ffffff", x1,y1,z1 #Draw vlaues of y on y axis
			#print "text", x3,y3,z3,"ffffff", x1,y1,z1 #Draw vlaues of y on y axis
		#y_max = 9
		#for i in range(0,y_max+1,1):
			#print "text", 0,i,0,"ffffff", i #Draw vlaues of y on y axis

	
def main(docopt_args):
	#Create an object of the Draw class
	obj = Draw()
	#swap the minimum and maximum values of z and y from the list
	x_min = obj.min_xyz_values[0]
	z_min = obj.min_xyz_values[1] #y_min value is now swapped for z_min value
	y_min = obj.min_xyz_values[2] #z_min value is now swapped for y_min value
	x_max = obj.max_xyz_values[0]
	#Same swapping for both z_max and y_max
	z_max = obj.max_xyz_values[1] 
	y_max = obj.max_xyz_values[2]
	R = obj.R
	G = obj.G
	B = obj.B
	gamma = 1.0
	range_x= x_max - x_min #Range of x values
	range_y= y_max - y_min #Range of y values
	range_z= z_max - z_min #Range of y values
	#Calculate the triangulation data
	obj.calc_triangulation()
	
	#Check for scaling parameters and apply accordingly
	if docopt_args["--sizeX"]: #If the is a value, scale X for this value
		number = docopt_args.get("--sizeX")
		scale_x = (int(number)/range_x)
		obj.xList = np.multiply(obj.xList,int(scale_x)) #Scale the values in xList by scale_x value
		x_min = np.amin(obj.xList) #Min x value after scaling X
		x_max = np.amax(obj.xList) #Max x values after scaling X
	if docopt_args["--sizeY"]: #if there is a value, scale Y for this value
		number = docopt_args.get("--sizeY")
		scale_y = (int(number)/range_y)
		obj.zList = np.multiply(obj.zList,int(scale_y)) #Scale elements contained in zList, these will will use as y values
		y_min = np.amin(obj.zList) #Max y values after scaling
		y_max = np.amax(obj.zList)  #Max y values after scaling
		print "damn y min", y_min
	if docopt_args["--sizeZ"]: #if there is a value, scale Z for this value
		number = docopt_args.get("--sizeZ")
		scale_z = (int(number)/range_z)
		obj.yList = np.multiply(obj.yList,int(scale_z))
		z_min = np.amin(obj.yList) #Min z value after scaling
		z_max = np.amax(obj.yList)  #Max z values after scaling
	#After all scaling is done, print triangulation plot
	obj.draw_triangulation()
	
	#Draw triangulation axes
	if docopt_args["--draw-axes"]:
	#Draw X, Y and Z axis
		print "line", x_min,y_min,z_min, x_max,y_min,z_min,"4",R,G,"0",gamma #Draw x-axis
		print "line", x_min,y_min,z_min, x_min,y_max,z_min,"4",R,G,"0",gamma #Draw y axis.Remember that we interchanged z and y
		print "line", x_min,y_min,z_min, x_min,y_min,z_max,"4",R,G,"0",gamma #Draw z-axis
	
	#Draw reference lables for plot
	if docopt_args["--draw-ref-labels"]:
		#Draw X, Y and Z Axes label
		print "text", x_max+1,0,0,"ffffff", "X-axis" 
		print "text", 0,y_max+1,0,"ffffff", "Z-axis" 
		print "text", 0,0,z_max+1,"ffffff", "Y-axis" 
		
	if docopt_args["--draw-X-values"]:
		#Draw x values on plot
		for i in range(0,x_max+1,1):
			print "text", i,0,0,"ffffff", i #Draw values of x
			
	if docopt_args["--draw-Y-values"]:
		#Draw x values on plot
		for i in range(0,y_max+1,1):
			print "text", 0,i,0,"ffffff", i #Draw values of x
			
	if docopt_args["--draw-Z-values"]:
		#Draw x values on plot
		for i in range(0,z_max+1,1):
			print "text", 0,0,i,"ffffff", i #Draw values of x
	
	if docopt_args["--draw-reference"]:	
			#Draw y and x lines for Grid
		for i in range(y_min,y_max+1,1):
			print "line", x_min,i,z_min,x_max,i,z_min,"1",R,G,"0",gamma #Draw x line on the y axis
			print "text", 0,i,0,"ffffff", i #Draw vlaues of y on y axis
		#Draw z and x lines for Grid
		for i in range(z_min,z_max+1,1):
			print "line", x_min,y_min,i,x_max,y_min,i,"1",R,G,"0",gamma #Draw x line on the z axis
			print "text", 0,0,i,"ffffff", i #Draw vlaues of z on x axis
		for i in range(x_min,x_max+1,1):
			print "line", i,y_min,z_min,i,y_min,z_max,"1",R,G,"0",gamma  #Draw z line on x axis
			print "line", i,y_min,z_min,i,y_max,z_min,"1",R,G,"0",gamma #Draw vertical y line on X axis
			print "text", i,0,0,"ffffff", i #Draw vlaues of x on x axis
	
if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
	