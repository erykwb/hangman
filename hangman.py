##!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

"""
Create a guess a word game - also known as Hangman game.
* Please write in Python and specify which version of Python you are using.
* Please include instructions on how to run.
* Please don't spend more than 30 minutes on this even if it is incomplete.

Rules:
1) When the game starts the player can see how many characters the word has.
2) The player can guess up to 9 times if a letter appears in the secret word.
   If the letter is in the word then the place of the character is shown to the player.
   Over the span of the game the incomplete word will appear to the player.
3) At any stage the player can propose a word. Each proposal reduces the number of attempts by one.
4) The player wins if he can find the secret word within the guess limit. Otherwise the game is lost.


The method of interaction is up to you, you can do it via the Puthon shell, as a command line game, or as Django app
or anything else (but Python!).

Where the initial word comes from is up to you. 

Requested by Essence (2018-06-14).

Written to target Python 3.5.2 and above. No attempt made at Python 2.x compatibility.

To run unit and integration tests:
    >>> python -m unittest
"""

DEFAULT_WORDS_FILE = '/usr/share/dict/words'
DEFAULT_MAX_TRIES = 9
PLACEHOLDER_CHAR = '*'

BANNER = ['Welcome to 30 minute Hangman. A word will be chosen at random and',
           'you must try to guess the word correctly, letter by letter.',
           'If you think you know the answer, you may type the whole word.']


class WordList(object):
    """
    A list of words for use in the game
    
    Args:
        word_file (str): Path to a file containing a `\n` delimited list of words
        word_length (int): Length of words desired
    
    Todo:
        There is no allowance made for character sets, punctuation or diacritics etc.
        so some words may be unguessable. This depends on the semantics of isalpha() and
        runtime environment sensing which there isn't time to deal with or construct test
        cases for in the allocated timeframe. This should probably also be an ABC to 
        improve testability and DI for the game class.
    """

    def __init__(self, word_length = DEFAULT_MAX_TRIES, word_file = DEFAULT_WORDS_FILE):
        self.word_length = word_length or DEFAULT_MAX_TRIES
        self.word_file = word_file
        self.word_list = self.load_word_list()

    def __repr__(self):
        # I usually use attrs `http://www.attrs.org/en/stable/` for dunder functions
        return "<WordList object for: `{}`>".format(self.word_file)
    
    def load_word_list(self):
        # Return a list of words of the desired length
        # str.strip() the trailing `\n`. Real version might str.translate() and/or
        # unicodedata.normalize() accents/diacritics. Also, watch the eval order when
        # calling strip() and len() in the same comprehension.
        with open(self.word_file) as f:
            return [word for word in (word.strip() for word in f.readlines()) 
                if len(word) == self.word_length]

    def get_target_word(self):
        # Todo: Shift to base class
        return random.choice(self.word_list).lower()

class Hangman(object):
    def __init__(self, target_word = None, word_list = None, max_tries = DEFAULT_MAX_TRIES):
        self.max_tries = max_tries or DEFAULT_MAX_TRIES
        self.tries = 0
        self.letters_tried = []
        self.letters_matched = []
        self.word_list = word_list
        if not target_word and not word_list:
            raise Exception('Neither a target word nor a word list were specified')
        self.target_word = target_word or self.word_list.get_target_word()
        self.current_state = list(PLACEHOLDER_CHAR * self.max_tries)

    def __repr__(self):
        return "<Hangman object for: `{}`>".format(self.target_word)
    
    # def load_words_list(self):
    #     return [word for word in (word.strip() for word in open(DEFAULT_WORDS_FILE).readlines()) 
    #             if len(word) == self.max_tries]

    # def get_target_word(self):
    #     return random.choice(self.load_words_list()).lower()

    @staticmethod # No reason besides demonstrating that it exists.
    def print_banner(text):
        for line in text:
            print(line, sep='\n')

    @property # As above.
    def playing(self):
        return self.tries_remaining and PLACEHOLDER_CHAR in self.current_state

    @property
    def tries_remaining(self):
        return self.max_tries - self.tries

    def check_guess(self, guess):
        for index, letter in enumerate(self.target_word):
            if guess == letter:
                self.current_state[index] = guess
        if guess not in self.target_word:
            # A correct guess does not traditionally use up a try, but the spec is ambiguous on this.
            # Move the increment out of the conditional to change the logic.
            self.tries += 1
            return False
        return True

    def run(self):
        # Todo: Bounce this out into a game runner class to make the game engine more testable (time...)
        self.print_banner(BANNER)
        while self.playing:
            try:
                guess = input('\nPlease select a letter between a-z' + '\n> ').lower()
            except (KeyboardInterrupt, SystemExit):
                break
            except:
                print('Looks like something went wrong, sorry!')
                raise
            else:
                if not guess.isalpha(): 
                    # Check the input is a letter(s)
                    print('That is not a valid character. Please try again.')
                    continue
                elif len(guess) > 1:
                    if guess == self.target_word:
                        self.current_state = guess
                        break
                    else:
                        self.tries += 1
                        print('That is not the correct answer. Please try again.')
                        continue
                elif guess in self.letters_tried: 
                    # Check that the letter hasn't been tried already. Alternatively, we could just make
                    # self.letters_tried a set and catch the exception.
                    print("You have already guessed that letter. Please try again.")
                    continue
                else:
                    pass

            if not self.check_guess(guess):
                print('Letter `{}` is not present. {} guesses remaining'.
                      format(guess.lower(), self.tries_remaining))

            print(''.join(self.current_state))
            self.letters_tried.append(guess)

        # EndWhile
        if PLACEHOLDER_CHAR not in self.current_state:
            print(("\nCongratulations! `{}` is correct!").format(self.target_word))
        else:
            print(("\nBad luck! The word was `{}`.").format(self.target_word))

if __name__ == "__main__":
    game = Hangman(word_list=WordList())
    game.run()