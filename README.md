# Hangman

Create a guess a word game - also known as Hangman game.
* Please write in Python and specify which version of Python you are using.
* Please include instructions on how to run.
* Please don't spend more than 30 minutes on this even if it is incomplete.

## Rules:
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
    ```>>> python -m unittest```

To play:
    ```python hangman.py```

