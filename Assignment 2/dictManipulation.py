import random

def get_word_dictionary(filename):
	wordDict = {}
	content = []
	with open(filename, 'r') as f:
		content = f.readlines()
	
	for curr_line in content:
		line = curr_line.split()
		wordDict[line[0]] = int(line[1])

	return wordDict


def pick_word(words):
	return random.choice(words.keys())