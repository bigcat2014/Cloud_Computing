#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 2
#

import random


def get_word_dictionary(filename):
	word_dict = {}
	with open(filename, 'r') as f:
		content = f.readlines()
	
	for curr_line in content:
		line = curr_line.split()
		word_dict[line[0]] = int(line[1])

	return word_dict


def pick_word(words):
	return random.choice(list(words.keys()))