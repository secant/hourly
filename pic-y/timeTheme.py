#functions to randomly generate a new start time, string, check if current time is within posting range
#what we need in main function: global variable to save the current theme and startime
import random
import datetime as dt

def time(old):
#takes in oldStartDT
#returns a datetime.time object for the start time of allowed range
#time range is two hours between 7am and 10pm
	
	hr = random.randint(7,22)
	minute = random.randint(0,60)
	start = dt.datetime(old.year,old.month,old.day,hour=hr,minute=minute)
	#increments the start by one day to get the next day's
	start+= dt.timedelta(days=1)
	return start

def timeAllowed(startDT):
	#returns true if current time allows for upload, false otherwise
	#takes dt.datetime object as the starttime
	
	current = dt.datetime.now()
	#checks that current time is in the valid range
	if current>=startDT and current <= startDT+dt.timedelta(hours=2):
		return True
	return False 

def theme():
	#returns a random string for the food
	f = open('foods.txt', 'r') 
	foods = list(f)
	select = random.choice(foods)
	print(select[:-1])


def updateTimeTheme(startDT):
	current = dt.datetime.now()
	#checks if we've past today's upload date
	#returns a tuple with the newStartDT, newTheme

	#checks if we're past the current start time
	if current>dt.time(start.time.hour+2,start.time.minute):
		#generates new start time and theme
		newStartDT = time(startDT)
		newTheme = theme()


# theme()
# print(time(dt.datetime.now()-dt.timedelta(days=1)))
# print(timeAllowed(dt.datetime()))