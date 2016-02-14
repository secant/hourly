#functions to randomly generate a new start time, string, check if current time is within posting range
#what we need in main function: global variable to save the current theme and startime
import random
import datetime as dt

def time(old):
#takes in oldStartDT
#returns a datetime.time object for the start time of allowed range
#time range is two hours between 7am and 10pm
	current = dt.datetime.now()
	hr = random.randint(7,22)
	if current.day == old.day:
		current = dt.datetime(current.year,current.month,current.day + 1)
	start = dt.datetime(current.year,current.month,current.day,hour=hr,minute=0)
	return start

def timeAllowed(startDT):
	#returns true if current time allows for upload, false otherwise
	#takes dt.datetime object as the starttime
	
	current = dt.datetime.now()
	#checks that current time is in the valid range
	if current>=startDT and current <= startDT+dt.timedelta(hours=2) and current.day==startDT.day:
		return True
	return False 

def theme():
	#returns a random string for the food
	f = open('FlaskWebProject/foods.txt', 'r') 
	foods = list(f)
	select = random.choice(foods)
	return select[:-1]


def updateTimeTheme(start, curr_theme):
	current = dt.datetime.now()
	#checks if we've past today's upload date
	#returns a tuple with the newStartDT, newTheme

	#checks if we're past the current start time
	if not timeAllowed(start) and current.day != start.day - 1:
		#generates new start time and theme
		start = time(start)
		curr_theme = theme()
	return start, curr_theme

