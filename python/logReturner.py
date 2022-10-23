import numpy as np


#logReturner is a utility class.
#It can take in an array of data and return a corresonding array of log-returns for that data.




class logReturner:
	
	@staticmethod
	def calcLogArray(array):
		logArray = array[0:-1,:]
		for j in range(len(array)-1):
			for i in range(len(array[0])):
				logArray[j][i] = np.log(array[j+1][i]/array[j][i])
		return logArray