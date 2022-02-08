import wordler

def interactive_feedback(guess, _):
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    END = '\033[0m'

    feedback = ([], [], [])
    str = input(f'Feedback ({GREEN}g{YELLOW}y{END}x): ')
    if len(str) > 5:
        exit(f'Invalid feedback: Must be 5 characters')

    for i, marker in enumerate(str):
        j = -1
        if marker == 'g':
            j = 0
        elif marker == 'y':
            j = 1
        elif marker == 'x':
            j = 2
        else:
            exit(f'Invalid feedback: Unexpected {marker}')
            
        feedback[j].append((guess[i], i))
    
    print(' ' * 15, wordler.pretty_print(guess, feedback))
    return feedback


if __name__ == '__main__':
    wordler.main('?????', interactive_feedback)