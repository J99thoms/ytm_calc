from datetime import datetime, timedelta
import math


"""
A bond object is used to store information about a bond.

A bond object has an issue date, a maturity date, and a coupon rate.

A bond object can also store a list of clean price(s).
	This list of clean price(s) is assumed to correspond to consecutive business day(s).
"""

class bond:
	
	# Constructor
	def __init__(self, issue_date, maturity, coupon, clean_prices):
		self.issue_date = issue_date
		self.maturity = maturity
		self.coupon = coupon
		self.clean_prices = clean_prices	# Clean prices should correspond to consecutive business days.
		
		
	# For debugging
	def __str__(self):
         return (f"issue date: {self.issue_date} \n" +
		 	f"maturity date: {self.maturity} \n" +
			f"coupon: {self.coupon} \n \n" +
			f"clean prices: {self.clean_prices}")
		
		
		
	#Take in a coupon date, add 6 months to it, and return the incremented date
	@staticmethod
	def incrementCoupon(couponDate):
		newYear = couponDate.year + ((couponDate.month + 6) // 12)
		newMonth = (couponDate.month + 6) % 12
		if newMonth == 0:
			newMonth = 12
		nextCouponDate = couponDate.replace(newYear, newMonth)
		return nextCouponDate
		
		
	#Take in a coupon date, subtract 6 months from it, and return the decremented date
	@staticmethod
	def decrementCoupon(couponDate):
		newMonth = (couponDate.month + 6) % 12
		if newMonth == 0:
			newMonth = 12
		newYear = couponDate.year
		if newMonth >= 7:
			newYear -= 1
		nextCouponDate = couponDate.replace(newYear, newMonth)
		return nextCouponDate
		
		
		
		
		
	
	#Given the current date, return the date of the most recent coupon payment for this bond
	def prevCouponDate(self, currentDate):
		couponDate = self.maturity
		while couponDate > currentDate:
			couponDate = bond.decrementCoupon(couponDate)
		return couponDate
		
		
	#Given the current date, return the date of the next upcoming coupon payment for this bond
	def nextCouponDate(self, currentDate):
		return bond.incrementCoupon(self.prevCouponDate(currentDate))
		
	
	#Given the current date, return the number of days since the most recent coupon payment for this bond
	def daysSinceCoupon(self, currentDate):
		couponDate = self.prevCouponDate(currentDate)
		days = (currentDate - couponDate).days
		return days
				
				
	#Given the current date, return the time (in years) until next upcoming coupon payment for this bond
	def timeToNextCoupon(self, currentDate):
		couponDate = self.nextCouponDate(currentDate)
		days = (couponDate - currentDate).days
		time = days/365
		return time
		
		
	#Given the current date, return the time (in years) until the maturity date of this bond
	def timeToMaturity(self, currentDate):
		days = (self.maturity - currentDate).days
		time = days/365
		#print(self.maturity)
		return time
		
		
		
		
	#Given a clean price and the date of that price, calculate the bond's YTM
	def calcYTM(self, cleanDate, cleanPrice):
	
		#Calculate the dirty price
		n = self.daysSinceCoupon(cleanDate)
		accruedInterest = n/365*self.coupon
		dirtyPrice = cleanPrice + accruedInterest
		
		#Setup cashflows
		couponFlow = self.coupon/2
		notional = 100
		
		#Calculate time until cashflows
		timeToMaturity = self.timeToMaturity(cleanDate)
		initialTimeToCoupon = self.timeToNextCoupon(cleanDate) 
		
		r=0	#Initial guess for yield is r=0
		
		#Each loop is one interation of Newton's method. Break when desired accuracy is achieved. 
		while True:
	
			#Reset loop variables
			timeToCoupon = initialTimeToCoupon
			date = self.nextCouponDate(cleanDate)
			DCF = 0
			deriv = 0
			
			#Add up coupon cashflows
			while date <= self.maturity:
				DCF += couponFlow*math.exp(-r*timeToCoupon)
				deriv += timeToCoupon*couponFlow*math.exp(-r*timeToCoupon)
				
				timeToCoupon += 0.5
				date = bond.incrementCoupon(date)
				
			#Add maturity cashflow to calculations
			DCF +=  notional*math.exp(-r*timeToMaturity)
			deriv += timeToMaturity*notional*math.exp(-r*timeToMaturity)
			
			
			#If desired accuracy is not achieved, perform another iteration of Newton's method. 
			#Else, break and return r (=YTM).
			if abs(DCF - dirtyPrice) > 0.0000001:
				r = r - (dirtyPrice - DCF)/deriv
			else:
				break
		return r
		
	
	
	#Assuming the bond object has a list of clean prices from consecutive business days,
	# and given the date of the first clean price in the list,
	# calculate the bond's YTM on each day.
	def calcYTMs(self, startDate):
	
		#Setup loop variables
		i = 0
		date = startDate
		YTMs = []
		prices = self.clean_prices
		
		#Calc YTMs
		while i < len(prices):
			YTMs.append(self.calcYTM(date, prices[i]))
			if (i%5)==4:
				date = date + timedelta(days=2)		#If the previous date was a Friday, add two extra days to the date
			date = date + timedelta(days=1)
			i+=1			
		return YTMs
				
	