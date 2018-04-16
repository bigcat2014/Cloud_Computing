#!usr/bin/python3

import random

num = int(random.uniform(5, 15))
guesses = 0

while True:
    guess = int(input("Please enter your guess\n> "))
    guesses += 1

    diff = abs(num - guess)

    if diff == 0:
        break
    elif diff <= 3:
        print('HOT')
    else:
        print('COLD')

print('MATCH\nNumber of guesses: %s' % guesses)
