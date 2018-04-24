def print_welcome_message(points):
	print('Welcome to Hangman')
	print('Your Current Score is %d points' % points)


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


def print_already_guessed(guess):
	print("%s has already been guessed, try again." % guess)


def print_correct((isCorrect, guess)):
	if isCorrect:
		print("There are %d %s's in the word" % (isCorrect, guess))


def print_round(won, guesses, word, score):
	if won:
		print('Congratulations, you won this round!')
		print('It took you %d guesses to guess the word %s' % (guesses, word))
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


