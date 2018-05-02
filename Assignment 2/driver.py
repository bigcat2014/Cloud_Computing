#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 2
#

from shape import get_shape


class Driver:
	shapes = []
	
	
def main():
	driver = Driver()

	fileLines = []
	with open('shapes.txt', 'r') as f:
		fileLines = f.readlines()
	
	for line in fileLines:
		driver.shapes.append(get_shape(line))

	for shape in driver.shapes:
		print('Shape: %s;\tsides: %s;\t\tarea: %.2f' % (shape.name, str(shape.sides), shape.area()))
	
		
if __name__ == '__main__':
	main()