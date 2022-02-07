import string
import random

# Words sourced from the Unix dictionary
# `cat /usr/share/dict/words > words.txt`
words = []
with open('./words.txt') as file:
    words = [line.rstrip() for line in file]

# Allow quick lookup of words that contain a char in a specific position
lookup = {}
for char in string.ascii_lowercase:
    inner = {}
    lookup[char] = inner
    for i in range(5):
        inner[i] = set()

for word in words:
    for i, char in enumerate(word):
        lookup[char][i].add(word)


# Compare chars of guess with target to get the hits and misses
def get_feedback(guess, target):
    exact = []
    inexact = []
    misses = []

    hits = []
    for i, char in enumerate(guess):
        other = target[i]
        if char == other:
            exact.append((char, i))
            hits.append(i)
    
    for i, char in enumerate(guess):
        j = target.find(char)
        if j >= 0:
            if i not in hits:
                inexact.append((char, i))
        else:
            misses.append(char)
    
    return exact, inexact, misses


# Use the hits and misses to reduce the set of possible words
# - Hits intersect the set with words that contain that char at that position
# - Misses substract the words that contain that char at any position
# - Inexact hits intersect the set with the set of words that contain that char
#   at any position except the guessed position or any that are already exactly known
# - (Special care taken with regards to duplicate chars in guess or target)
def refine_possibilities(possible, feedback):
    refined = possible
    for char in feedback[2]: # Misses
        for i in range(5):
            refined = refined - lookup[char][i]
        print(f'After missed {char}: ', len(refined))

    for char, i in feedback[0]: # Exact hits
        refined = refined & lookup[char][i]
        print(f'After exact {char} at {i}: ', len(refined))
    
    for char, i in feedback[1]: # Inexact hits
        refined = refined - lookup[char][i]
        temp = set()
        for j in range(5):
            if i != j:
                temp = temp | lookup[char][j]
        refined = refined & temp
        print(f'After inexact {char} at {i}: ', len(refined))


    if len(refined) < 50:
        print(refined)
    return refined


# Try to guess every possible target and print the distribution of tries
results = [0] * 30
for target in set(words):
    tries = 0
    guess = ''
    possible = set(words)

    print(f'\nTarget: {target}')
    while True:
        tries += 1
        guess = random.choice(tuple(possible))

        print(f'Try: {tries}')
        print(f'Guess: {guess}')
        if guess == target:
            break    

        feedback = get_feedback(guess, target)
        possible = refine_possibilities(possible, feedback)

    results[tries] = results[tries] + 1
    print(f'Guessed {target} after {tries} tries!')

for i, n in enumerate(results):
    if n > 0:
        print(f'{i}: {n}')