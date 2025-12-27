import random
import json

TIERS = {"free": 1, "paid": 3, "premium": 5}
player_roles = ["Player 1", "Player 2"]
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
    "Grace": "Probably the only hymnal everyone knows. It's 'Amazing'.",                                                                                                                                               #JRM 12-23-2025 
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
            print("Warning: Unknown tier in config, defaulting to free.")
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
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def update_pvp_scores(scores, setter, guesser, setter_win):
    if setter_win:
        scores[setter] += 1
    else:
        scores[guesser] += 1

def average_tries(win_tries):
    return sum(win_tries) / len(win_tries) if win_tries else 0

if __name__ == '__main__':
    user_tier = get_user_tier()
    MAX_SLOTS = TIERS[user_tier]
    print(f"Welcome {user_tier.title()} user! You have {MAX_SLOTS} save slot(s) available.")

    WORD_LIST = load_word_list()

    wins = 0
    losses = 0
    win_tries = []

    mode = input("Select difficulty (easy/hard): ").strip().lower()
    MAX_TRIES = 5 if mode == 'hard' else 10

    multiplayer = input("Multiplayer? (y/n): ").strip().lower()
    player_scores = None
    if multiplayer == 'y':
        player_scores = {player_roles[0]: 0, player_roles[1]: 0}

    WORD_LIST = load_word_list()
    user_tier = get_user_tier()

    resume = input("Load savved game: (y/n): ").strip().lower()
    if resume == 'y':
        slot = input(f"Which slot? 1-{MAX_SLOTS}): ").strip() or "1"
        if not slot.isdigit() or not (1 <= int(slot) <= MAX_SLOTS):
            print("Invalid slot; using slot 1.")
            slot = "1"

        try:
            state = load_game_state(slot)
            secret_word = state['secret_word']
            tries = state['tries']
            guessed = state['guessed']
            previous_guesses = set(state['previous_guesses'])
            wins = state.get('wins', 0)
            losses = state.get('losses', 0)
            win_tries = state.get('win_tries', [])

        except FileNotFoundError:
            print(f"No save file for slot {slot}. Statring a new game.")
            secret_word = random.choice(WORD_LIST)
            tries = 0
            guessed = False
            previous_guesses = set()
    while True:
        if multiplayer == 'y':
            print(f"{player_roles[0]}, enter the secret word (Player 2, look away!):")
            secret_word = input("Secret word: ").strip().lower()
        else:
            secret_word = random.choice(WORD_LIST)

        tries = 0
        guessed = False
        previous_guesses = set()
        early_quit = False
        print("\nGuess the secret word!")

        while not guessed and tries < MAX_TRIES:
            try:
                guess = input("Your guess (or type 'give up' to quit): ").strip()
                if not guess:
                    raise ValueError("Input cannot be blank!")
                if is_give_up(guess):
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
                    alpha_hint = get_hint(secret_word, guess)
                    if alpha_hint in ("before", "after"):
                        print(f"Hint: The word comes {alpha_hint} your guess alphabetically.")
            except ValueError as e:
                print("Error:", e)
                
        if early_quit:
            break

        if guessed:
            wins += 1
            win_tries.append(tries)
            if multiplayer == 'y':
                player_scores[player_roles[1]] += 1  # Guesser wins
        else:
            losses += 1
        if tries >= MAX_TRIES:
            print(f"Sorry, out of tries! The word was {secret_word}")
        if multiplayer == 'y':
            player_scores[player_roles[0]] +=1 # Word-setter wins
        
        if win_tries:
            avg = sum(win_tries) / len(win_tries)
            print(f"Average guesses per win: {avg:.2f}")
        else:
            print("No wins yet, so no average guess.")

        # Show scores
        print(f"Games won: {wins}, Games lost: {losses}")
        if multiplayer == 'y':
            print(f"Scores: {player_roles[0]}: {player_scores[player_roles[0]]}, {player_roles[1]}: {player_scores[player_roles[1]]}")

        # Option to save
        save = input("Would you like to save your game? (y/n): ").strip().lower()
        if save == 'y':
            slot = input(f"Save to slot (1-{MAX_SLOTS}): ").strip() or "1"
            if not slot.isdigit() or not (1 <= int(slot) <= MAX_SLOTS):
                slot = "1"
            state = {
                'secret_word': secret_word,
                'tries': tries,
                'guessed': guessed,
                'previous_guesses': list(previous_guesses),
                'wins': wins,
                'win_tries': win_tries,
                'losses': losses
            }
            save_game_state(slot, state)

        # Multiplayer role swap
        if multiplayer == 'y':
            swap = input("Swap roles for the next round? (y/n): ").strip().lower()
            if swap == 'y':
                player_roles.reverse()

        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            break