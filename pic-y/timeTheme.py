#functions to randomly generate a new start time, string, check if current time is within posting range
import random
import datetime as dt

def time():
#returns a datetime.time object for the start time of allowed range
#time range is two hours between 7am and 10pm
	current = dt.datetime.now()
	hr = random.randint(7,22)
	minute = random.randint(0,60)
	start = dt.datetime(hr,minute)

	return start

def timeAllowed(start):
	#returns true if current time allows for upload, false otherwise
	#takes dt.time object as the starttime
	current = dt.datetime.now().time()
	#checks that current time is in the valid range
	if current>=start and current <= dt.time(start.hour+2,start.minute):
		return True
	return False 

def theme():
	#returns a random string for the food
	f = open('foods.txt', 'r') 
	foods = list(f)
	select = random.choice(foods)
	print(select[:-1])


# theme()
# time()
# print(timeAllowed(dt.time(12,30)))