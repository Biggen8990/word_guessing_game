import unittest
import random
import json
from word_game import is_guess_correct, get_hint
from word_game import load_word_list
from word_game import is_give_up
from word_game import update_score
from word_game import save_game_state, load_game_state
from word_game import WORD_HINTS
from word_game import play_game
from word_game import TIERS, get_user_tier

WORD_LIST = load_word_list()
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

    def test_load_word_list(self):
        filename = 'test_words.txt'
        with open(filename, 'w') as f:
            f.write('apple\nbanana\ncat\n\nDOG\n')
        result = load_word_list(filename)
        self.assertEqual(result, ['apple', 'banana', 'cat', 'DOG'])

    def test_give_up(self):
        self.assertTrue(is_give_up("give up"))
        self.assertTrue(is_give_up("GIVE UP"))
        self.assertFalse(is_give_up("notquit"))

    def test_score_update(self):
        scores = {'wins': 0, 'losses': 0}
        update_score(scores, True)
        self.assertEqual(scores['wins'], 1)
        self.assertEqual(scores['losses'], 0)

        update_score(scores, False)
        self.assertEqual(scores['wins'], 1)
        self.assertEqual(scores['losses'], 1)

    def test_save_load_game(self):
        state = {
            'secret_word': 'python',
            'tries': 2,
            'guessed': False,
            'previous_guesses': ['code', 'java'],
            'wins': 1,
            'losses': 0
        }
        filename = 'test_save.json'
        save_game_state(filename, state)
        loaded = load_game_state(filename)
        self.assertEqual(state, loaded)

    def test_hint_exists(self):
        self.assertEqual(WORD_HINTS["God"], "Who doesn't ever change?")
    def test_hint_fallback(self):
        self.assertEqual(WORD_HINTS.get("unknownword", "No hint available."), "No hint available.")

    def test_lose_after_max_tries(self):
        word_list = ["python"]
        inputs = iter(['wrong'] * 5)
        original_input = __builtins__.input
        __builtins__.input = lambda prompt='': next(inputs)
        try:
            guessed, tries = play_game(word_list, max_tries=5, secret_word="python")
            self.assertFalse(guessed)
            self.assertEqual(tries, 5)
        finally:
            __builtins__.input = original_input

    def test_multi_slot_save_load(self):
        state1 = {'secret_word': 'python', 'tries': 1, 'guessed': False, 'previous_guesses': [], 'wins': 2, 'losses': 1}
        state2 = {'secret_word': 'code', 'tries': 2, 'guessed': True, 'previous_guesses': ['fun'], 'wins': 3, 'losses': 0}
        save_game_state('1', state1)
        save_game_state('2', state2)
        loaded1 = load_game_state('1')
        loaded2 = load_game_state('2')
        self.assertEqual(state1, loaded1)
        self.assertEqual(state2, loaded2)

    def test_tiers(self):
        # Patch or simulate get_user_tier
        for tier, slots in TIERS.items():
            self.assertEqual(TIERS[tier], slots)

    def test_get_user_tier(self):
        #This will just test current hardcoded value.
        self.assertIn(get_user_tier(), TIERS)

    def setUp(self):
        with open('test_config_paid.json', 'w') as f:
            json.dump({"username": "testuser", "tier": "paid"}, f)
        with open('test_config_invalid.json', 'w') as f:
            f.write('not json')

    def test_get_user_tier_paid(self):
        self.assertEqual(get_user_tier('test_config_paid.json'), "paid")

    def test_get_user_tier_missing(self):
        self.assertEqual(get_user_tier('nonexistent_config.json'), "free")

    def test_get_user_tier_invalid(self):
        self.assertEqual(get_user_tier('test_config_invalid.json'), "free")

if __name__ == '__main__':
    unittest.main()
