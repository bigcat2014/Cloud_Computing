#!/usr/bin/python3
#
# Logan Thomas
# Clouf Computing
# Assignment 2
#

import random

GUESSES = 6


def print_welcome_message(points):
	print('Welcome to Hangman')
	print('Your Current Score is %d points' % points)


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


def print_word_picked():
	print('I have picked a word, please guess the letters')


def print_word(word, guessed_letters):
	length = len(word)
	return_string = ['_' for letter in range(length)]

	for letter in guessed_letters:
		index = word.find(letter)
		while index != -1:
			return_string[index] = letter
			index = word.find(letter, index + 1)
	
	print('Current Guess: %s' % ' '.join(return_string))


def print_guesses(guessed_letters):
	print('Guessed Letters: %s' % str(guessed_letters))


def print_tries(num_guesses):
	print("Number of tries left: %d" % num_guesses)


def correct_guess(word, guess):
	return word.count(guess), guess


def print_correct((isCorrect, guess)):
	if isCorrect:
		print("There are %d %s's in the word" % (isCorrect, guess))


def word_guessed(word, guessed_letters):
	count = 0
	for letter in guessed_letters:
		count += word.count(letter)

	return count == len(word)


def print_round(won, guesses, word, score):
	if won:
		print('Congratulations, you won this round!')
		print('It took you %d guesses to guess the word %s' % (GUESSES - guesses, word))
	else:
		print('Unfortunately, you lost this round.')
		print('The word was %s' % word)
	print('Your new Score is %d' % score)


def print_game(score):
	if score > 0:
		print('You won the game!')
	else:
		print('You lost. Try again next time.')
	print('Your final score was %d' % score)


def main():
	score = 500
	curr_guesses = GUESSES

	print_welcome_message(score)

	words = get_word_dictionary('dictionary.txt')

	while (score > 0 and score < 1000):
		guessed_letters = []
		curr_guesses = GUESSES
		word = pick_word(words)

		print_word_picked()
		print_tries(curr_guesses)
		print('\n')
		
		while curr_guesses > 0:
			print_word(word, guessed_letters)
			print_guesses(guessed_letters)
			print_tries(curr_guesses)
			print('\n')

			guess = raw_input("Guess a letter\n>> ")
			curr_guesses -= 1
			print('\n')

			print_correct(correct_guess(word, guess))
			guessed_letters.append(guess)

			if word_guessed(word, guessed_letters):
				score += words[word]
				print('\n')
				print_round(True, curr_guesses, word, score)
				print('\n')
				break
		else:
			score -= words[word]
			print('\n')
			print_round(False, curr_guesses, word, score)
			print('\n')
		
		del(words[word])
	
	print('\n')
	print_game(score)

if __name__ == "__main__":
	main()