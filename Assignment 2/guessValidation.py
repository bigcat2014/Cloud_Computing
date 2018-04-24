def get_guess():
	return raw_input("Guess a letter\n>> ")[:1]

def correct_guess(word, guess):
	return word.count(guess), guess


def word_guessed(word, guessed_letters):
	count = 0
	for letter in guessed_letters:
		count += word.count(letter)

	return count == len(word)