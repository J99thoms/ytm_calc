import numpy as np
import matplotlib.pyplot as plt



#plotter is a utility class.
#
#A plotter object is used to plot various matrices of data obtained from other classes:
#
#	-Given a matrix 'ytmMatrix' of various bonds' YTM(s) over consecutive business day(s)
#		together with a matrix 'times' of those bonds' timeToMaturity (in years),
#		a plotter object can generate a plot with the YTM curve from each day
#		superimposed on-top of each other.
#
#	-Given a matrix 'spotPoints' of point-estimates for spot curve(s) over consecutive business day(s)
#		(assumed to be obtained from the spotCurve class), 
#		a plotter object can generate a plot with the spot curve from each day
#		superimposed on-top of each other.
#
#	-Given a matrix 'forwardPoints' of point-estimates over consecutive business day(s) for 1-year forward curve(s)
#		with terms range from 2-5 years	(assumed to be obtained from the forwardCurve class), 
#		a plotter object can generate a plot with the forward curve from each day
#		superimposed on-top of each other.
#
#All the plots above are drawn using linear interpolation between points.



class plotter:
	
	#Constructor
	def __init__(self, ytmMatrix, times, spotPoints, forwardPoints):
		self.ytmMatrix = ytmMatrix
		self.times = times
		self.spotPoints = spotPoints
		self.forwardPoints = forwardPoints
		

	
	#Getter methods:
	
	def getYTMs(self):
		return self.ytmMatrix
		
	def getTimes(self):
		return self.times
		
	def getSpotMatrix(self):
		return self.spotPoints
		
	def getForwardMatrix(self):
		return self.forwardPoints
		
		
		

	#Using ytmMatrix and times, generate a plot with the YTM curve from from each day superimposed on-top of each other.
	def buildYTMPlot(self):
		ytmMatrix = self.getYTMs()
		times = self.getTimes()
		for i in range(len(ytmMatrix[0,:])):
			plt.plot(times,  ytmMatrix[:,i]*100, linestyle=':', linewidth=2.0, marker='o', label='Day '+str(i+1))
		plt.xlabel('Time to maturity (years)', fontsize=15)
		plt.xticks(times, fontsize=13)
		plt.yticks(fontsize=13)
		plt.ylabel('YTM', fontsize=15)
		plt.title('5-year YTM curves from 10 days of data', fontsize=25)
		plt.legend(loc=2, prop={'size': 13})
		plt.show()
		
		
	#Using spotPoints, generate a plot with the spot curve from each day superimposed on-top of each other.
	def buildSpotPlot(self):
		spotPoints = self.getSpotMatrix()
		for i in range(len(spotPoints)):
			plt.plot(spotPoints[i,:,1], spotPoints[i,:,0]*100, linestyle=':', linewidth=2.0, marker='o', label='Day '+str(i+1))
		plt.xlabel('Time to maturity, T (years)', fontsize=15)
		plt.xticks(np.arange(0.0, 5.5, 0.5), fontsize=13)
		plt.yticks(fontsize=13)
		plt.ylabel('Spot rate, r(T)', fontsize=15)
		plt.title('5-year spot curves from 10 days of data', fontsize=25)
		plt.legend(loc=2, prop={'size': 13})
		plt.show()
	
	#Using forwardPoints, generate a plot with the 1-year forward curve from each day superimposed on-top of each other.	
	def buildForwardPlot(self):
		forwardPoints = self.getForwardMatrix()
		for i in range(len(forwardPoints)):
			plt.plot(range(1,5), forwardPoints[i,:]*100, linestyle=':', linewidth=2.0, marker='o', label='Day '+str(i+1))
		plt.xlabel('T (years)', fontsize=15)
		plt.ylabel('1year-Tyear forward rate', fontsize=15)
		plt.xticks(range(1,5), fontsize=13)
		plt.yticks(fontsize=13)
		plt.title('1-year forward curves from 10 days of data', fontsize=25)
		plt.legend(loc=2, prop={'size': 13})
		plt.show()
		
		