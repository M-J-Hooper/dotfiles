import math
import queue
import string

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
            misses.append((char, i))
    
    return exact, inexact, misses


# Use the hits and misses to reduce the set of possible words
# - Hits intersect the set with words that contain that char at that position
# - Misses substract the words that contain that char at any position
# - Inexact hits intersect the set with the set of words that contain that char
#   at any position except the guessed position or any that are already exactly known
# - (Special care taken with regards to duplicate chars in guess or target)
def refine_possibilities(possible, feedback):
    refined = possible
    for char, _ in feedback[2]: # Misses
        for i in range(5):
            refined = refined - lookup[char][i]

    for char, i in feedback[0]: # Exact hits
        refined = refined & lookup[char][i]
    
    for char, i in feedback[1]: # Inexact hits
        refined = refined - lookup[char][i]
        temp = set()
        for j in range(5):
            if i != j:
                temp = temp | lookup[char][j]
        refined = refined & temp

    return refined


# For a given word produce the 3^5 permutations of feedback
def feedback_permutations(guess):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    for m in range(3):
                        entry = ([], [], [])
                        entry[i].append((guess[0], 0))
                        entry[j].append((guess[1], 1))
                        entry[k].append((guess[2], 2))
                        entry[l].append((guess[3], 3))
                        entry[m].append((guess[4], 4))
                        yield entry


def refine_chars_with_info(chars_with_info, feedback):
    result = chars_with_info
    for char, _ in feedback[0] + feedback[1] + feedback[2]:
        result.add(char)
    return result


# Calculate the expected value of information for each possibility and return the optimal word
def make_guess(possible, chars_with_info):
    info_queue = queue.PriorityQueue()

    extra = set()
    if len(possible) > 10: # Magic number when extra becomes less useful
        extra = set(words)
        for char in chars_with_info:
            for i in range(5):
                extra = extra - lookup[char][i]
        print('Using extra ' + str(len(extra)) + ' outside of actual possibilities')

    print('Calculating guess from ' + str(len(possible)) + ' actual possibilities')
    for i, guess in enumerate(possible | extra):
        info = 0
        for feedback in feedback_permutations(guess):
            refined = refine_possibilities(possible, feedback)
            prob = len(refined) / len(possible)
            if prob > 0:
                info += prob * math.log(prob, 2)

        info_queue.put((info, guess))

    return info_queue.get()[1]


# Pretty printing on the terminal
def pretty_print(guess, feedback):
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    END = '\033[0m'
    prefixes = [''] * 5

    for char, i in feedback[2]: # No colour
        prefixes[i] = END

    for char, i in feedback[1]: # Yellow
        prefixes[i] = YELLOW

    for char, i in feedback[0]: # Green
        prefixes[i] = GREEN
    
    result = ''
    for i, char in enumerate(guess):
        result += prefixes[i] + char
    return result + END


# Since there is no prior info it will always be the same
# Use `make_guess(set(words))` to do the full calculation
first_guess = 'tries'

# Try to guess every possible target
results = [0] * 30
for target in words:
    tries = 0
    history = []
    guess = ''
    possible = set(words)
    chars_with_info = set()

    print(f'\nTarget: {target}')
    while True:
        tries += 1
        print(f'Try: {tries}')

        if tries == 1:
            guess = first_guess
        else:
            guess = make_guess(possible, chars_with_info)

        print(f'Guess: {guess}')
        if guess == target:
            break    

        feedback = get_feedback(guess, target)
        history.append(pretty_print(guess, feedback))
        
        chars_with_info = refine_chars_with_info(chars_with_info, feedback)
        possible = refine_possibilities(possible, feedback)

    results[tries] = results[tries] + 1
    history.append(pretty_print(target, get_feedback(target, target)))
    print('\n' + '\n'.join(history))

# Print the distribution of tries
print()
for i, n in enumerate(results):
    if n > 0:
        print(f'{i}: {n}')