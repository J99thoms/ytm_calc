from datetime import datetime, timedelta
import math
import numpy as np



#spotCurve is a utility class.
#
#A spotCurve object stores a list of bond objects, together with a start date.
#
#It assumes that each bond has a list of clean price(s) corresponding to consecutive business day(s).
#Each bond should have the same number of clean price(s), and the clean price(s) should all start from the same start date.
#
#A spotCurve object is used to perform the boot-strapping process and can return an array of point-estimates for spot curve(s).
#The boot-strapping process is done using linear interpolation.



class spotCurve:
	
	#Constructor
	def __init__(self, bonds, startDate):
		self.bonds = bonds
		self.startDate = startDate
		self.currentDate = startDate
		self.pointsArray = []			#stores point-estimates for the spot curve(s)
		self.weekDay = 0				#used for tracking day of week
		


	#Getter methods:
	
	def getBonds(self):
		return self.bonds
		
	def getStartDate(self):
		return self.startDate
		
	def getCurrentDate(self):
		return self.currentDate
		
	def getPointsArray(self):
		return self.pointsArray
		
		
		
	#Setter methods:
	
	def setCurrentDate(self, date):
		self.currentDate = date
		
		
		
	


	#Take in a coupon date, add 6 months to it, and return the incremented date
	@staticmethod
	def incrementCoupon(couponDate):
		newYear = couponDate.year + ((couponDate.month + 6) // 12)
		newMonth = (couponDate.month + 6) % 12
		if newMonth == 0:
			newMonth = 12
		nextCouponDate = couponDate.replace(newYear, newMonth)
		return nextCouponDate
		
				
				
				
		
	#Increment the value of currentDay by one business day
	def incrementDate(self):
		if (self.weekDay%5)==4:	#If it's currently a Friday, add 2 extra days to the current date
			self.setCurrentDate(self.getCurrentDate() + timedelta(days=2))
		self.setCurrentDate(self.getCurrentDate() + timedelta(days=1))
		self.weekDay += 1
		


		
		
		
	#Calculate the array of point-estimates for the spot curve(s)
	def calcPoints(self):
		numPoints = len(self.getBonds())	#One point-estimate is gained from each bond
		
		#Loop through the cleanPrices (assumed to be consecutive business days)
		for i in range(len(self.getBonds()[0].getCleanPrices())):	#Assumes that each bond in self.bonds has the same number of cleanPrices
			self.calcFirstPoint(i)	
			while len(self.getPointsArray()[-1]) < numPoints:
				self.calcNextPoint(i)
			self.incrementDate()
		
		
	#Calculate the first point-estimate for a spot curve on a given day
	def calcFirstPoint(self, day):
		currentDate = self.getCurrentDate()
		self.pointsArray.append([])
		
		firstBond = self.getBonds()[0]
		
		#Calc dirty price
		n = firstBond.daysSinceCoupon(currentDate)
		accruedInterest = n/365*firstBond.getCoupon()
		cleanPrice = firstBond.getCleanPrice(day)
		dirtyPrice = cleanPrice + accruedInterest
		
		#Setup cashflows
		couponFlow = firstBond.getCoupon()/2
		finalFlow = 100 + couponFlow
		
		#Calc time until cashflows
		timeToMaturity = firstBond.timeToMaturity(currentDate)
		
		#Calc yield
		r = -np.log(dirtyPrice/finalFlow)/timeToMaturity	# r = -ln(P/N)/T
		
		self.pointsArray[-1].append([r, timeToMaturity])
		
		
	#Calculate a point-estimate for a spot curve on a given day
	def calcNextPoint(self, day):
		currentDate = self.getCurrentDate()
		i = len(self.getPointsArray()[-1])
		
		nextBond = self.getBonds()[i]
		
		#Calc dirty price
		n = nextBond.daysSinceCoupon(currentDate)
		accuredInterest = n/365*nextBond.getCoupon()
		cleanPrice = nextBond.getCleanPrice(day)
		dirtyPrice = cleanPrice + accuredInterest
		
		#Setup cashflows
		couponFlow = nextBond.getCoupon()/2
		finalFlow = 100 + couponFlow
		
		#Calc time until cashflows
		timeToMaturity = nextBond.timeToMaturity(currentDate)
		initialTimeToCoupon = nextBond.timeToNextCoupon(currentDate) 
		
		#Initialize loop variables:
		DCF = 0
		timeToCoupon = initialTimeToCoupon
		loopDate = nextBond.nextCouponDate(currentDate)
		j=1
			
		#Sum up coupon cash flows (using interpolated yield values from boot-strapping)
		while loopDate < nextBond.getMaturity():
		
			#Get nearby spot curve point-estimates (for linear interpolation)
			rPrev = 0
			tPrev = 0
			if j!=1:
				rPrev = self.getPointsArray()[-1][j-2][0]
				tPrev = self.getPointsArray()[-1][j-2][1]
			rNext = self.getPointsArray()[-1][j-1][0]
			tNext = self.getPointsArray()[-1][j-1][1]	
			
			#Interpolate yield at time = loopDate
			rTime = rPrev + (rNext - rPrev)/(tNext - tPrev)*(timeToCoupon-tPrev)
		
			#Add discounted coupon cash flow
			DCF += couponFlow*math.exp(-rTime*timeToCoupon)	
			
			#Increment loop variables:
			timeToCoupon += 0.5
			loopDate = spotCurve.incrementCoupon(loopDate)
			j += 1

		#Calc yield
		r = -np.log((dirtyPrice - DCF)/finalFlow)/timeToMaturity	
		
		self.pointsArray[-1].append([r, timeToMaturity])
		
		
		
		