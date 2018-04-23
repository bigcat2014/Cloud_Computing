#!/usr/bin/python3
#
#	Logan Thomas
#	Cloud Computing
#	Assignment 2
#


# Capitalize the first letter of each word in the string and
# take the sum of all numbers, not contained in a word, and
# print the new string and the sum.
def main():
	total = 0.0
	user_input = input("Please enter a string\n>> ")
	user_input = user_input.split()
	output = []

	for word in user_input:
		try:
			total += float(word)
			output.append(word)
		except ValueError:
			output.append(word.capitalize())
	
	output = ' '.join(output)
	print('"%s", the sum of numbers is %.3f' % (output, total))

if __name__ == "__main__":
	main()