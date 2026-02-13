import unittest
import random
import json
import os
from word_game import (
    is_guess_correct,
    get_hint,
    load_word_list,
    is_give_up,
    save_game_state,
    load_game_state,
    WORD_HINTS,
    TIERS,
    get_user_tier,
    save_high_score,
    load_high_scores,
    log_session,
    log_user_progress,
)
WORD_LIST = load_word_list()
HIGH_SCORES_FILE = "high_scores.json"

def test_save_load_last_user(self):
    save_last_user("TestUser")
    self.assertEqual(get_last_user(), "TestUser")

def test_load_word_list(self):
    filename = "test_import.text"
    with open(filename, "W") as f:
        f.write("alpha\nbeta\ngamma\n")
    words = load_word_list(filename)
    self.assertEqual(words, ["alpha", "beta", "gama"])
    os.remove(filename)

# Helper function for PvP scoring
def update_pvp_scores(scores, setter, guesser, setter_win):
    if setter_win:
        scores[setter] += 1
    else:
        scores[guesser] += 1

# Helper function for average tries
def average_tries(win_tries):
    if win_tries:
        return sum(win_tries) / len(win_tries)
    return 0

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
        for tier, slots in TIERS.items():
            self.assertEqual(TIERS[tier], slots)

    def test_get_user_tier(self):
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

    def test_log_session(self):
        log_session("Tester", "python", ["guess1", "python"], "Win", "easy", filename="test_session_history.txt")
        with open("test_session_history.txt") as f:
            content = f.read()
        self.assertIn("Tester", content)
        os.remove("test_session_history.txt")

    def test_log_user_progress(self):
        log_user_progress("Tester", "easy", True, 4, filename="test_user_progress.json")
        with open("test_user_progress.json") as f:
            data = json.load(f)
        self.assertEqual(data[-1]["username"], "Tester")
        os.remove("test_user_progress.json")


class TestPvPScore(unittest.TestCase):
    def test_guesser_win(self):
        scores = {"Player 1": 0, "Player 2": 0}
        update_pvp_scores(scores, "Player 1", "Player 2", setter_win=False)
        self.assertEqual(scores, {"Player 1": 0, "Player 2": 1})

    def test_setter_win(self):
        scores = {"Player 1": 0, "Player 2": 0}
        update_pvp_scores(scores, "Player 1", "Player 2", setter_win=True)
        self.assertEqual(scores, {"Player 1": 1, "Player 2": 0})

class TestAverageTries(unittest.TestCase):
    def test_average_tries(self):
        tries_list = [3, 4, 5]
        self.assertAlmostEqual(average_tries(tries_list), 4.0)
        self.assertEqual(average_tries([]), 0)

class TestHighScores(unittest.TestCase):
    TEST_FILE = "test_high_scores.json"

    def setUp(self):
        # Remove the test file if it exists
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_save_high_score_and_top_5(self):
        # Add six scores
        save_high_score("Alice", "python", 4, "easy", filename=self.TEST_FILE)
        save_high_score("Bob", "code", 2, "hard", filename=self.TEST_FILE)
        save_high_score("Carol", "fun", 5, "easy", filename=self.TEST_FILE)
        save_high_score("Dave", "test", 1, "hard", filename=self.TEST_FILE)
        save_high_score("Eve", "guess", 3, "easy", filename=self.TEST_FILE)
        save_high_score("Frank", "logic", 10, "hard", filename=self.TEST_FILE)  # Should not appear (worst score)

        scores = load_high_scores(filename=self.TEST_FILE)
        self.assertEqual(len(scores), 5)
        self.assertEqual(scores[0]['name'], "Dave")   # Best score
        self.assertEqual(scores[-1]['name'], "Carol") # Fifth best score

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

if __name__ == '__main__':
    unittest.main()