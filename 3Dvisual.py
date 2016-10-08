""" 3Dvisual.py
    
    Usage:
        3Dvisual.py -h
		3Dvisual.py (-f <filename>) [(--draw-axes) (--draw-reference) (--draw-ref-labels) (--sizeX=<number>) (--sizeY=<number>) (--sizeZ=<number>) (--draw-X-values) (--draw-Y-values) (--draw-Z-values)]

		
	  

	Options:
		-h,--help : This is the help message. Provide the file name as the first argument, followed by the other command to be run by the user.
		-f : specify the filename or the file path. i.e -f filename.csv 
		--draw-axes       : draw axes of plot
		--draw-reference  : draw reference of plot
		--draw-ref-labels : draw reference labels
		--draw-X-values   : draw X values on reference plot
		--draw-Y-values   : draw Y values on reference plot		
		--draw-Z-values   : draw Z values on reference plot
		--sizeX=<number>  : Scale X by number 
		--sizeY=<number>  : Scale Y by number
		--sizeZ=<number>  : Scale Z by number
	
"""
import matplotlib.delaunay as triang  #import Delaunay triangulation from Matplotlib
import matplotlib.text as textlabel
import matplotlib.colors as cl
import pylab
import random
import numpy
import numpy  as np  #import numpy library 
import matplotlib.pyplot as plt
from docopt import docopt  #import docopt; the library to process CLI functions

class Draw(object):
	
	def __init__(self):
		self.xList = [] #This list holds the values corresponding to X from the CSV
		self.yList = [] #This list holds values corresponding to Y from the CSV
		self.zList = [] #This list holds values corresponding to Z from the CSV
		self.colourList = [] #This list holds values corresponding to hex values of colour from the CSV file
		input_file = args['<filename>'] # Get the file name from the command line
		with open(input_file, 'r') as input: #open the CSV file and read through it
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
		self.len_xList = len(self.xList)
		self.len_yList = len(self.yList)
		self.len_zList = len(self.zList)
		self.len_colourList = len(self.colourList)
		x_min = int(min(self.xList)) #Min x value from CSV data
		y_min = int(min(self.yList)) #Min y value from CSV  data
		z_min = int(min(self.zList)) #Min z value from CSV  data
		x_max = int(max(self.xList)) #Max x value from CSV  data
		y_max = int(max(self.yList)) #Max y value from CSV  data
		z_max = int(max(self.zList)) #Max z value from CSV  data
		self.min_xyz_values = (x_min,y_min,z_min) #Tuple holding the minimum values of x, y and z respectively
		self.max_xyz_values = (x_max,y_max,z_max) #Tuple holding the maximum values of x, y and z respectively
		self.xyzcolour_len = (self.len_xList,self.len_yList,self.len_zList,self.len_colourList) #Tuple holding the size of the list of x,y,z and colour respectively
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
			#For performance sake, we reuse the xList, yList, zList and colourList(holding original CSV data) instead of creating and using a new lists 
			self.xList.append(x)
			self.yList.append(y)
			self.zList.append(z)
			self.colourList.append(colourhex)
		#Update the content of xList,yList,zList and colourList to the new data needed for triangulation
		self.xList[:self.len_xList] = [] #Remove all X values original appended from the CSV file 
		self.yList[:self.len_yList] = [] #Remove all Y values original appended from the CSV file
		self.zList[:self.len_zList] = [] #Remove all Z values original appended from the CSV file
		self.colourList[:self.len_colourList] = [] #Remove all hex values original appended from the CSV

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
		#Remember on lines #101 through #104 we updated self.xList,self.yList,self.zList and self.colourList from the CSV data values to the data needed for triangulation/plotting
		
		while (col<len(self.xList)): #Starting at the first index, iterate through the entire length of  xList
			#Access lists values column by column
			#Swap y and Z values for the purpose of our plot
			xcol = self.xList[col] #Get all values corresponding to x from xList
			zcol = self.yList[col] #Get all values corresponding to y from yList
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
			#Increament col to further to the next column on next iteration
			col = col + 1
			i = 0
			#Render our plot using the triangulation points 
			#Aurora-VR Mod understands understands this print command to generate our plot
			print "line", x1,y1,z1,x2,y2,z2,thickness,R,G,B,gamma
			print "line", x2,y2,z2,x3,y3,z3,thickness,R,G,B,gamma
			print "line", x3,y3,z3,x1,y1,z1,thickness,R,G,B,gamma
			print "text", 0,y1,0,"ffffff", y1 #Draw y values 
			print "text", 0,y2,0,"ffffff", y2 #Draw y values 
			print "text", 0,y3,0,"ffffff", y3 #Draw y values 
			print "text", x1,0,0,"ffffff", x1 #Draw x values 
			print "text", x2,0,0,"ffffff", x2 #Draw x values 
			print "text", x3,0,0,"ffffff", x3 #Draw x values 
			print "text", 0,0,z1,"ffffff", z1 #Draw z values 
			print "text", 0,0,z2,"ffffff", z2 #Draw Z values 
			print "text", 0,0,z3,"ffffff", z3 #Draw z values

	
def main(docopt_args):
	#Create an object of the Draw class
	obj = Draw()
	#swap the minimum and maximum values of z and y from the list
	x_min = obj.min_xyz_values[0]
	z_min = obj.min_xyz_values[1] #y_min value is now swapped for z_min value
	y_min = obj.min_xyz_values[2] #z_min value is now swapped for y_min value
	x_max = obj.max_xyz_values[0]
	#Swap also the values of z_max and y_max
	z_max = obj.max_xyz_values[1] 
	y_max = obj.max_xyz_values[2]
	R = obj.R
	G = obj.G
	B = obj.B
	gamma = 1.0
	range_x= x_max - x_min #Range of x values
	range_y= y_max - y_min #Range of y values
	range_z= z_max - z_min #Range of y values
	#Calculate our triangulation data
	obj.calc_triangulation()
	#in order to scale our plot, we need to check for the following parameters
	#and apply accordingly
	#Scale X plot by the value provided at CLI
	if docopt_args["--sizeX"]: 
		number = docopt_args.get("--sizeX")
		scale_x = (int(number)/range_x)
		obj.xList = np.multiply(obj.xList,int(scale_x)) #Scale the values in xList by scale_x value
		x_min = np.amin(obj.xList) #Min x value after scaling X
		x_max = np.amax(obj.xList) #Max x value after scaling X
	#Scale Y plot by the value provided at CLI
	if docopt_args["--sizeY"]: 
		number = docopt_args.get("--sizeY")
		scale_y = (int(number)/range_y)
		obj.zList = np.multiply(obj.zList,int(scale_y)) #Scale elements contained in zList, these will will use as y values
		y_min = np.amin(obj.zList) #Min y value after scaling
		y_max = np.amax(obj.zList)  #Max y value after scaling
		print "damn y min", y_min
	#Scale Z plot by the value provided at CLI
	if docopt_args["--sizeZ"]: 
		number = docopt_args.get("--sizeZ")
		scale_z = (int(number)/range_z)
		obj.yList = np.multiply(obj.yList,int(scale_z))
		z_min = np.amin(obj.yList) #Min z value after scaling
		z_max = np.amax(obj.yList)  #Max z value after scaling
	#After all scaling is done, draw triangulation plot
	obj.draw_triangulation()
	
	#Draw triangulation axes
	if docopt_args["--draw-axes"]:
	#Draw X, Y and Z axis
		print "line", x_min,y_min,z_min, x_max,y_min,z_min,"4",R,G,"0",gamma #Draw x-axis
		print "line", x_min,y_min,z_min, x_min,y_max,z_min,"4",R,G,"0",gamma #Draw y axis.
		print "line", x_min,y_min,z_min, x_min,y_min,z_max,"4",R,G,"0",gamma #Draw z-axis
	
	#Draw reference labels for plot
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
		#Draw y values on plot
		for i in range(0,y_max+1,1):
			print "text", 0,i,0,"ffffff", i #Draw values of y
			
	if docopt_args["--draw-Z-values"]:
		#Draw z values on plot
		for i in range(0,z_max+1,1):
			print "text", 0,0,i,"ffffff", i #Draw values of z
	
	if docopt_args["--draw-reference"]:	
			#Draw y and x lines for Grid
		for i in range(y_min,y_max+1,1):
			print "line", x_min,i,z_min,x_max,i,z_min,"1",R,G,"0",gamma #Draw x line on the y-axis
			print "text", 0,i,0,"ffffff", i #Draw values of y on y-axis
		#Draw z and x lines for Grid
		for i in range(z_min,z_max+1,1):
			print "line", x_min,y_min,i,x_max,y_min,i,"1",R,G,"0",gamma #Draw x line on the z-axis
			print "text", 0,0,i,"ffffff", i #Draw values of z on x axis
		for i in range(x_min,x_max+1,1):
			print "line", i,y_min,z_min,i,y_min,z_max,"1",R,G,"0",gamma  #Draw z line on x-axis
			print "line", i,y_min,z_min,i,y_max,z_min,"1",R,G,"0",gamma #Draw y line on x-axis
			print "text", i,0,0,"ffffff", i #Draw vlaues of x on x axis
	
if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
	