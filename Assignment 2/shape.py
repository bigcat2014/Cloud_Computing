#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 2
#

from math import sqrt


class Shape:
	sides = []
	name = ''

	def __init__(self):
		self.name = 'Shape'
	
	def area(self):
		pass


class Rectangle(Shape):
	def __init__(self, x, y):
		super().__init__()
		self.name = 'Rectangle'
		self.sides = [x, y]
	
	def area(self):
		return self.sides[0] * self.sides[1]


class Triangle(Shape):

	def __init__(self, s1, s2, s3):
		super().__init__()
		self.name = 'Triangle'
		self.sides = [s1, s2, s3]
	
	def area(self):
		p = (self.sides[0] + self.sides[1] + self.sides[2]) / 2
		return sqrt(p * (p - self.sides[0]) * (p - self.sides[1]) * (p - self.sides[2]))


def get_shape(line):
	line = line.split()
	shape_type = line[0]
	if shape_type == 'T':
		return Triangle(float(line[1]), float(line[2]), float(line[3]))
	else:
		return Rectangle(float(line[1]), float(line[2]))
