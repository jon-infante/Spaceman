import random
import os
import sys
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letters_guessed = list()
counter = 0
#Variables to make readability easier for print text
line = '~'
header = f'''|{line*78}|'''

#Makes a global counter, had issues with local counters and wanted a fix.
#Know this kind of practice in the long run isn't the cleanest.
def increment():
    global counter
    counter += 1

def load_word():
    '''
    A function that reads a text file of words and randomly selects one to use as the secret word
        from the list.
    Returns:
           string: The secret word to be used in the spaceman guessing game
    '''
    f = open('words.txt', 'r')
    words_list = f.readlines()
    f.close()

    words_list = words_list[0].split(' ') #comment this line out if you use a words.txt file with each word on a new line
    secret_word = random.choice(words_list)
    return secret_word

def is_word_guessed(secret_word, letters_guessed):
    '''
    A function that checks if all the letters of the secret word have been guessed.
    Args:
        secret_word (string): the random word the user is trying to guess.
        letters_guessed (list of strings): list of letters that have been guessed so far.
    Returns:
        bool: True only if all the letters of secret_word are in letters_guessed, False otherwise
    '''
    #Checks to see if all the letters have been guessed in the word.
    for i in secret_word:
            if i not in letters_guessed:
                return True
    return False

def get_guessed_word(secret_word, letters_guessed):
    '''
    A function that is used to get a string showing the letters guessed so far in the secret word and underscores for letters that have not been guessed yet.
    Args:
        secret_word (string): the random word the user is trying to guess.
        letters_guessed (list of strings): list of letters that have been guessed so far.
    Returns:
        string: letters and underscores.  For letters in the word that the user has guessed correctly, the string should contain the letter at the correct position.  For letters in the word that the user has not yet guessed, shown an _ (underscore) instead.
    '''
    #Loops through the secret word and adds the letter guessed if it is in
    #the secret word, if not it adds an underscore.
    guessed_word = list()
    gap = '_'
    for i in secret_word:
        if i in letters_guessed:
            guessed_word.append(i)
        else:
            guessed_word.append(gap)
    print('| ' + ' '.join(guessed_word) + '\n|')
    return guessed_word

def is_guess_in_word(guess, secret_word):
    '''
    A function to check if the guessed letter is in the secret word
    Args:
        guess (string): The letter the player guessed this round
        secret_word (string): The secret word
    Returns:
        bool: True if the guess is in the secret_word, False otherwise
    '''
    if guess in secret_word:
        print('| You guessed a letter!')
        return True
    else:
        print('| Incorrect guess.')
        increment()
        return False

#Loops through the the lists alphabet and letters_guessed and checks if the
#input is in them in order for the lists to be updated. Also checks if the input
#given is a alphabetical character.
def guess_input():
    valid = True
    while valid:
        guess = input('| Guess a letter: ').lower()
        print(header)
        if len(guess) > 1:
            print('| Only guess one letter a time!')
        else:
            if guess in alphabet or guess in letters_guessed:
                if guess in letters_guessed:
                    print('| Letter already guessed!')
                else:
                    alphabet.remove(guess)
                    letters_guessed.append(guess)
                    valid = False
                    is_guess_in_word(guess, secret_word)
                    return True
            else:
                print('| Guess is not a letter!')

#Restarting the game
#Reference: https://stackoverflow.com/questions/48129942/python-restart-program
def restart():
        choice = input('| Would you like to play again? y/n\n| ')
        if choice == 'y':
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        elif choice == 'n':
            print('| Thanks for playing!')
            sys.exit(0)
        else:
            pass

def spaceman(secret_word):
    '''
    A function that controls the game of spaceman. Will start spaceman in the command line.
    Args:
      secret_word (string): the secret word to guess.
    '''

    intro = f'''\n\n{header}\n| Welcome to Spaceman.\n|\n| You will have up to 7 attempts to guess letters in the secret word.\n| Guess one letter at a time per round.\n|\n| The word to guess contains {len(secret_word)} letters.\n{header}\n|'''
    print(intro)
    #Guess Counter
    #This block runs the guess_input function over and over until you are up to
    #7 guesses or the game is won by guessing all the letters.
    while is_word_guessed(secret_word, letters_guessed) and counter < 7:
            if counter == 6:
                print(f'| You have 1 guess left.')
            else:
                print(f'| You have {7 - counter} guesses left.')
            guess_input()

            #Joins the letters in the list and puts them together with a comma
            print('| Letters Guessed: ' + ', '.join(letters_guessed))
            get_guessed_word(secret_word, letters_guessed)
    #Adds breaks in code to show distinction between lines
    print(f'{header}\n|\n|\n{header}')
    #Checks again if you guess the word after you exit the loop
    if not is_word_guessed(secret_word, letters_guessed):
        print('| You Win!')
    else:
        print(f'| Sorry you lost. The word was {secret_word} \n| Try again in another game!')

    restart()

'''
    Test Functions

    When running the tests by themselves it passes, however when the
    spaceman function is enabled it gives an error. All the tests run fine
    with the spaceman function commented out.

'''

def test_is_word_guessed():
    #Logic is Reversed, this doesn't give an error.
    assert is_word_guessed(('ghost'),['g', 'h', 'o', 's', 't']) is False
    assert is_word_guessed(('toast'),['a', 'h', 'o', 's', 't']) is False
    assert is_word_guessed(('battle'),['a', 'b', 'o', 's', 't', 'l', 'e']) is False


def test_get_guessed_word():
     assert get_guessed_word(('basket'),['b', 's', 'k', 'e']) == ['b', '_', 's', 'k', 'e', '_']
     assert get_guessed_word(('broccoli'),['b', 't', 'o', 'e', 'c', 'i']) == ['b', '_', 'o', 'c', 'c', 'o', '_', 'i']
     assert get_guessed_word(('child'),['c', 'i', 'l', 'e', 'o']) == ['c', '_', 'i', 'l', '_']

def test_is_guess_in_word():
    assert is_guess_in_word(('b'), ('basket')) is True
    assert is_guess_in_word(('t'), ('trampoline')) is True
    assert is_guess_in_word(('c'), ('space')) is True

if __name__ == "__main__":
    #These function calls that will start the game
    secret_word = load_word()
    spaceman(secret_word)
