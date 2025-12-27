import random
import json

TIERS = {
    "free": 1,
    "paid": 3,
    "premium": 5
}

WORD_HINTS = {
    "God": "Who doesn't ever change?",
    "Lord": "He's the King of Kings and...",
    "Jesus": "The only name above all names.",
    "Love": "Opposite of hate?",
    "Joy": "... to the World, the Lord has come.",
    "Peace": "The Prince of...",
    "Patience": "A fruit of the spirit, starts with the lette P.",
    "Kindness": "The opposite of not careing about others.",
    "Goodness": "I will sing of the ________ of God.",
    "Gentleness": "Non-agressive",
    "Faithfulness": "Fully trusting.",
    "Long-suffering": "Similar to Patience.",
    "Meekness": "... is not weakness.",
    "Faith": "_____, Hope, and Love...",
    "Grace": "Probably the only hymnal everyone knows. It's 'Amazing'.",                                                                                                             #JRM 12-23-2025
    "Redemption": "Your __________ draws near.",
    "Repent":"Acts 2:38 says to ______ and be baptized...",
    "Salvation": "The plan of _________."

}

def get_user_tier(config_file='user_config.json'):
    try:
        with open(config_file) as f:
            config = json.load(f)
        tier = config.get("tier", "free")
        if tier not in TIERS:
            print("Warning: Unknow tier in config, defaulting to free.")
            return "free"
        return tier
    except (FileNotFoundError, json.JSONDecodeError):
        print("User config not found or invalid, using free tier.")
        return "free"

def save_game_state(slot, state):
    filename = f"savegame{slot}.json"
    with open(filename, 'w') as f:
        json.dump(state, f)
    print(f"Game saved to {filename}.")

def load_game_state(slot):
    filename = f"savegame{slot}.json"
    with open(filename) as f:
        state = json.load(f)
    print(f"Game loaded from {filename}.")
    return state

def is_guess_correct(secret_word, guess):
    return guess.lower() == secret_word.lower()

def is_give_up(guess):
    return guess.strip().lower() == "give up"

def get_hint(secret_word, guess):
    guess = guess.lower()
    secret_word = secret_word.lower()
    if guess < secret_word:
        return "after"
    elif guess > secret_word:
        return "before"
    else:
        return "correct"
    
def load_word_list(filename='words.txt'):
    """
    Returns a list of non-empty words from a test file.
    Each word should appear on it's own line.
    """
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def update_score(scores, won):
    """
    Update the scoreboard.
    :param scores: dict with keys 'wins' and 'losses'
    :param won: bool, True if player won the round
    """
    if won:
        scores['wins'] += 1
    else:
        scores['losses'] += 1

def play_game(word_list, max_tries=10, secret_word=None):
    """
    Play a full round of the guessing game.
    Returns: did_win (True/False), number_of_tries
    """
    import random
    if secret_word is None:
        secret_word = random.choice(word_list)
    tries = 0
    guessed = False
    previous_guesses = set()
    while not guessed and tries < max_tries:
        guess = input("Your guess (or type 'give up' to quit): ").strip()
        if guess.lower() == "give up":
            print(f"You gave up! Teh word was '{secret_word}'.")
            break
        if not guess:
            print("Input cannot be blank!")
            continue
        if guess in previous_guesses:
            print("You already guessed that!")
        previous_guesses.add(guess)
        tries += 1
        if is_guess_correct(secret_word, guess):
            print(f"Congratulations! You guessed the word in {tries} tries!")
        else:
            print("Not the right word, try again!")
    if not guessed and tries >= max_tries:
        print(f"Sorry! The word was '{secret_word}'.")
    return guessed, tries


if __name__ == '__main__':
    user_tier = get_user_tier()
    MAX_SLOTS = TIERS[user_tier]
    print(f"Welcome {user_tier.title()} user! You have {MAX_SLOTS} save slot(s) available.")

    mode = input("Select difficulty (easy/hard): ").strip().lower()
    if mode == 'hard':
        MAX_TRIES = 5
    else:
        MAX_TRIES = 10
    resume = input("Load saved game? (y/n): ").strip().lower()
    if resume == 'y':
        slot = input("Which slot? (1): ").strip() or "1"
        try:
            state = load_game_state(slot)
            secret_word = state['secret_word']
            tries = state['tries']
            guessed = state['guessed']
            previous_guesses = set(state['previous_guesses'])
            wins = state.get('wins', 0)
            losses = state.get('losses', 0)
        except FileNotFoundError:
            print("No save file for that slot. Starting new game.")
            secret_word = random.choice(WORD_LIST)
            tries = 0
            guessed = False
            previous_guesses = set()
    else:
        WORD_LIST = load_word_list()
        secret_word = random.choice(WORD_LIST)
        tries = 0
        guessed = False
        previous_guesses = set()
    
    
    WORD_LIST = load_word_list()
    MAX_TRIES = 10
    wins = 0
    losses = 0
    while True:
        secret_word = random.choice(WORD_LIST)
        tries = 0
        guessed = False
        previous_guesses = set()
        print("\nGuess the secret word!")

        while not guessed and tries < MAX_TRIES:
            try:
                guess = input("Your guess: (or type 'give up' to guit): ").strip()
                if not guess:
                    raise ValueError("Input cannot be blank!")
                if guess.lower() == "give up":
                    print(f"You gave up! The word was '{secret_word}'.")
                    break
                if guess in previous_guesses:
                    print("You already guessed that!")
                    continue
                previous_guesses.add(guess)
                tries += 1
                if is_guess_correct(secret_word, guess):
                    print(f"Congratulations! You guessed the word in {tries} tries!")
                    guessed = True
                else:
                    print("Not the right word, try again!")
                    print("Hint:", WORD_HINTS.get(secret_word, "No hint available."))
                    if guess < secret_word:
                        print("Hint: The word comes after your guess alphabetically.")
                    elif guess > secret_word:
                        print("Hint: The word comes before your guess alphabetically.")
            except ValueError as e:
                print("Error:", e)
        if guessed:
            wins += 1
        else:
            losses += 1
            

        if not guessed:
            print(f"Sorry, out of tries! The word was {secret_word}")
        print(f"Games won: {wins}, Games lost: {losses}")

        save = input("Would you like to save your game? (y/n)")
        if save.lower() == 'y':
            slot = input("save to slot (1): ").strip() or "1"
            state = {
                'secret_word': secret_word,
                'tries': tries,
                'guessed': guessed,
                'previous_guesses': list(previous_guesses),
                'wins': wins,
                'losses': losses
            }
            save_game_state(slot, state)
        again = input("Play again? (y/n): ")
        if again.lower() != 'y':
            break