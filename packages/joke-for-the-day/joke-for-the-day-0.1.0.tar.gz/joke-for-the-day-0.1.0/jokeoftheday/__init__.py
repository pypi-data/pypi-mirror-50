import random
import os

name = "joke-of-the-day"

def joke():
	jokes=[]
	fullPath = os.path.realpath(__file__).rsplit(os.sep, 1)[0]
	with open(fullPath+'/jokes.txt','r') as fileHandler:
		jokes.extend([eachJoke.strip("\n") for eachJoke in fileHandler.readlines()])
	randomInt = random.randint(0,len(jokes)-1)
	return jokes[randomInt]
