from datetime import datetime
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import xlrd


from bond import bond
from spotCurve import spotCurve
from forwardCurve import forwardCurve
from plotter import plotter
from logReturner import logReturner as logr




#Open the excel spreadsheet with the bond data
loc = ("C:/Users/Jakob/Desktop/School Materials/Toronto/Winter 2022/MAT1856/Assignments/A1/bonds.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

#Read in the data for the 11 selected bonds, storing each as a bond object in the list 'bonds'
bonds = []
for i in range(11):
	issueDate = datetime.strptime(sheet.cell_value(i+1, 2), '%m/%d/%Y')
	maturityDate = datetime.strptime(sheet.cell_value(i+1, 3), '%m/%d/%Y')
	coupon = sheet.cell_value(i+1, 0)*100
	cleanPrices = []
	for j in range(5, 15):
		cleanPrices.append(sheet.cell_value(i+1, j))
	newBond = bond(issueDate, maturityDate, coupon, cleanPrices)
	bonds.append(newBond)
	
	

startDay = datetime(2022, 1, 10)	#Date that data collection began = Jan. 10, 2022








#Calculations for Q4(a):
print('\nQ4(a):\n')

#For each bond, calculate its YTM for each day of data,
#	and then store all the YTMs in a matrix.
YTMs = []	
for i in range(len(bonds)):
	YTMs.append(bonds[i].calcYTMs(startDay))
ytmMatrix = np.array(YTMs)		

#Output the YTM matrix
print('YTM matrix:\n')
print(ytmMatrix)			
print('Each row corresponds to a bond.\nEach column corresonds to a day of data.\n')


#Store the time to maturity of each bond (used when plotting the YTM curve)
times = []
for i in range(len(bonds)):
	times.append(bonds[i].timeToMaturity(startDay))





#Calculations for Q4(b):
print('\n\n\nQ4(b):\n')

#Generate a 3D matrix of point-estimates for spot curves for each day of data
spt = spotCurve(bonds, startDay)
spt.calcPoints()
spotMatrix = np.array(spt.getPointsArray())

#Output the spot curve point-estimate matrix
print('\nSpot curve point-estimate matrix:\n')
print(spotMatrix)
print('Each row corresonds to a bond.\nEach 2D matrix corresponds to a day of data.\nCol 1 = point-estimate for spot rate at time T, Col 2 = time T (in years)\n')





#Calculations for Q4(c):
print('\n\n\nQ4(c):\n')

#Generate a matrix of point-estimates for 1-year forward curves for each day of data
frwd = forwardCurve(spt.getPointsArray())
frwd.calcRates()
forwardMatrix = np.array(frwd.getForwardArray())

#Output the forward curve point-estimate matrix
print('\n1-year - T-year forward curve point-estimate matrix:\n')
print(forwardMatrix)
print('Each row corresponds to a day of data.')
print('Starting from T=2, each column corresonds to a year, T.\n')




#For quick debugging of the plotter:

#np.save('ytmMatrix', ytmMatrix)	
#np.save('times', times)	
#np.save('spotPoints', spotMatrix) 
#np.save('forwardPoints', forwardMatrix)

#ytmMatrix = np.load('ytmMatrix.npy') 
#times = np.load('times.npy')
#spotMatrix = np.load('spotPoints.npy')
#forwardMatrix = np.load('forwardPoints.npy')




#Plots for Q4:

#Generate plots for the YTM curve, spot curve, and 1-year forward curve, with each day of data superimposed on-top of each other
pltt = plotter(ytmMatrix, times, spotMatrix, forwardMatrix)
pltt.buildYTMPlot()
pltt.buildSpotPlot()
pltt.buildForwardPlot()









#Calculations for Q5:
print('\n\n\nQ5:\n')

ytmData = ytmMatrix[[1,3,5,7,9],:]	#Get YTM data for bonds with maturities in approximately 1, 2, 3, 4, and 5 years
ytmData = ytmData.T					#Transpose the matrix for use with the logReturner class

#Output the YTM data again (for debugging)
print('\nYTM data matrix:\n')
print(ytmData)
print('Each column corresponds to a bond.\nEach row corresonds to a day of data.')
print('With the leftmost column being column #1, the bond corresonding to column i matures in approximately i years.\n')

ytmLogReturns = logr.calcLogArray(ytmData)	#Calculate the daily log-returns of yield for bonds with maturities in approximately 1, 2, 3, 4, and 5 years

#Output the YTM log-return data
print('\nYTM daily log-return matrix:\n')
print(ytmLogReturns)
print('Each column corresponds to a bond.\nEach row corresonds to a day of data.')
print('With the leftmost column being column #1, the bond corresonding to column i matures in approximately i years.\n')


ytmCov = np.cov(ytmLogReturns, rowvar=False)	#Calculate the covariance matrix for the time series of daily log-returns of yields

#Output the YTM log-return covariance matrix
print('\nYTM daily log-return covariance matrix: \n')
print(ytmCov)
print('Starting from i=1, column/row i corresponds to a bond that matures in approximately i years.\n')



#Output the 1-year forward rate data again (for debugging)
print('\n\n\n1-year - T-year forward rate data matrix:\n')
print(forwardMatrix)
print('Each row corresponds to a day of data.')
print('Starting from T=2, each column corresonds to a year, T.\n')


forwardLogReturns = logr.calcLogArray(forwardMatrix)	#Calculate the daily log-returns of 1-year forward rate for 1yr-1yr, 1yr-2yr, 1yr-3yr, and 1yr-4yr

#Output the 1-year forward rate log-return data
print('\n1-year - T-year forward rate daily log-return matrix:\n')
print(forwardLogReturns)
print('Each row corresponds to a day of data.')
print('Starting from T=2, each column corresonds to a year, T.\n')

forwardCov = np.cov(forwardLogReturns, rowvar=False)	#Calculate the covariance matrix for the time series of daily log-returns of 1-year forward rates

#Output the 1-year forward rate log-return covariance matrix
print('\n1-year - T-year forward rate daily log-return covariance matrix: \n')
print(forwardCov)
print('Starting from i=1, column/row i corresponds the 1-year - (i+1)-year forward rate.\n')









#Calculations for Q6:
print('\n\n\nQ6:\n')

#Calculate and output the eigenvalues and eigenvectors of the covariance matrix for the time series of daily log-returns of yields
ytmEigVals, ytmEigVecs = LA.eig(ytmCov)	
print('YTM daily log-return covariance matrix eigenvalues and eigenvectors:')
for i in range(len(ytmEigVals)):
	print('\neigenvalue: ' + str(ytmEigVals[i]) + '\neigenvector: ' + str(ytmEigVecs[:,i]))


#Calculate and output the eigenvalues and eigenvectors of the covariance matrix for the time series of daily log-returns of of 1-year forward rates
forwardEigVals, forwardEigVecs = LA.eig(forwardCov)	
print('\n\n1-year - T-year forward rate daily log-return covariance matrix eigenvalues and eigenvectors:')
for i in range(len(forwardEigVals)):
	print('\neigenvalue: ' + str(forwardEigVals[i]) + '\neigenvector: ' + str(forwardEigVecs[:,i]))







