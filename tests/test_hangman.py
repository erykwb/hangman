from unittest import TestCase
from unittest.mock import MagicMock as MMock
from unittest.mock import patch
import hangman

class TestWordList(TestCase):
    def test_01_create_word_list_from_defaults(self):
        words = hangman.WordList()
        word = words.get_target_word()
        self.assertEqual(9, len(word))

    def test_02_create_word_list_with_custom_word_length(self):
        words = hangman.WordList(7)
        word = words.get_target_word()
        self.assertEqual(7, len(word))

    def test_03_create_word_list_from_bogus_file(self):
        with self.assertRaises(FileNotFoundError):
            words = hangman.WordList(word_file = 'bogosity.txt')
            word = words.get_target_word()
            self.assertIsNone(word)

        #Code is not protected against errors such as these.
        # words = hangman.WordList(0)
        # word = words.get_target_word()
        # self.assertEqual(2, len(word))

        # words = hangman.WordList(200)
        # word = words.get_target_word()
        # self.assertEqual(200, len(word))

    def test_04_word_list_default_identity(self):
        words = hangman.WordList()
        self.assertEqual('<WordList object for: `/usr/share/dict/words`>', words.__repr__())

class TestHangman(TestCase):
    def test_01_create_with_defined_word(self):
        game = hangman.Hangman(target_word='essence')
        self.assertEqual('essence',game.target_word)
        game.current_state = 'essence'
        self.assertFalse(game.playing) # Check we won the game. Should really be it's own test

    def test_02_create_with_mock_word_list(self):
        # Not useful as it stands, just a start on mocking the word list dependency injection
        words = MMock()
        words.get_target_word.return_value = 'essence'
        game = hangman.Hangman(word_list=words)
        self.assertEqual('essence', game.target_word)
        self.assertTrue(game.playing)

    def test_03_create_with_no_word_or_list(self):
        # Should use custom exceptions, but no time to define them
        with self.assertRaises(Exception):
            _ = hangman.Hangman()

    def test_04_play_the_game(self):
        """ 
        Insufficient time to implement, but `@patch('builtins.input', return_value='a')` can
        emulate user input so the actual game logic could be tested, as can popen to drive the UI 
        """
        game = hangman.Hangman(target_word='essence')
        self.assertEqual('essence',game.target_word)
        game.current_state = 'essence'
        self.assertFalse(game.playing)
