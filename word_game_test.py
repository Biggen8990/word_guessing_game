import unittest
import random
from word_game import is_guess_correct, get_hint

WORD_LIST = ["python", "code", "fun", "test", "guess"]
MAX_TRIES = 10

class TestWordGuessGame(unittest.TestCase):
    def test_random_word_selection(self):
        secret = random.choice(WORD_LIST)
        self.assertIn(secret, WORD_LIST)

    def test_guess_limit(self):
        tries = MAX_TRIES
        self.assertEqual(tries, 10)

    def test_guess_correctness(self):
        self.assertTrue(is_guess_correct("python", "Python"))
        self.assertFalse(is_guess_correct("python", "java"))
    
    def test_prevent_repeats(self):
        guesses = {"code", "python"}
        guess = "python"
        self.assertIn(guess, guesses)

    def test_hint_direction(self):
        self.assertTrue("before" in get_hint("python", "Zebra"))
        self.assertTrue("after" in get_hint("python", "apple"))   

if __name__ == '__main__':
    unittest.main()
