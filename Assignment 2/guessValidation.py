def get_guess():
	guess = input("Guess a letter\n>> ")
	if guess:
		return guess
	else:
		print("Please enter a guess.")
		return get_guess()


def correct_guess(word, guess):
	return word.count(guess)


def word_guessed(word, guessed_letters):
	count = 0
	for letter in guessed_letters:
		count += word.count(letter)

	return count == len(word)