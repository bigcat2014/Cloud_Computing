#!/usr/bin/python3
#
# Logan Thomas
# Clouf Computing
# Assignment 2
#

from printer import *
from dictManipulation import get_word_dictionary, pick_word
from guessValidation import *

GUESSES = 6

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

			if word_guessed(word, guessed_letters)[0]:
				score += words[word]
				print('\n')
				print_round(True, GUESSES - curr_guesses, word, score)
				print('\n')
				break
		else:
			score -= words[word]
			print('\n')
			print_round(False, GUESSES - curr_guesses, word, score)
			print('\n')
		
		del(words[word])
	
	print('\n')
	print_game(score)

if __name__ == "__main__":
	main()