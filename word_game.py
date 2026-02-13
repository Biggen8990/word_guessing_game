import random
import json
from datetime import datetime

HIGH_SCORES_FILE = "high_scores.json"
TIERS = {"free": 1, "paid": 3, "premium": 5, "admin": 10}
player_roles = ["Player 1", "Player 2"]

WORD_HINTS = { "God": "Who doesn't ever change?", 
              "Lord": "He's the King of Kings and...", 
              "Jesus": "The only name above all names.", 
              "Love": "Opposite of hate?", 
              "Joy": "... to the World, the Lord has come.", 
              "Peace": "The Prince of...",
              "Patience": "A fruit of the spirit, starts with the letter P.", 
              "Kindness": "The opposite of not careing about others.", 
              "Goodness": "I will sing of the ________ of God.", 
              "Gentleness": "Non-agressive", 
              "Faithfulness": "Fully trusting.", 
              "Long-suffering": "Similar to Patience.", 
              "Meekness": "... is not weakness.", 
              "Faith": "_____, Hope, and Love...", 
              "Grace": "Probably the only hymnal everyone knows. It's 'Amazing'.",                                                                                                                                                                              #JRM 12-23-2025 
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

def save_high_score(name, word, tries, mode, filename=HIGH_SCORES_FILE):
    scores = []
    try:
        with open(filename) as f:
            scores = json.load(f)
    except FileNotFoundError:
        pass
    scores.append({"name": name, "word": word, "tries": tries, "mode": mode})
    scores.sort(key=lambda x: x["tries"])
    scores = scores[:5]
    with open(filename, "w") as f:
        json.dump(scores, f)

def load_high_scores(filename=HIGH_SCORES_FILE):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def show_high_scores(filename=HIGH_SCORES_FILE):
    try:
        with open(filename) as f:
            scores = json.load(f)
        print("Leaderboard — Best Games:")
        for s in scores:
            mode_label = s.get('mode', 'unknown').title()
            print(f"{s['name']} ({mode_label}) guessed '{s['word']}' in {s['tries']} tries")
    except FileNotFoundError:
        print("No high scores yet!")

def print_welcome_menu():
    print("="*40)
    print("Welcome to the Word Guessing game!")
    print("Controls:")
    print("- Guess the secret word by typing your guess.")
    print("- Type 'give up' to reveal the answer and quit the round.")
    print("- Type 'y' or 'n' for yes/no questions.")
    print("- In multiplayer, take turns as Player 1 and Player 2.")
    print("- After each game, you can save or change word list/theme.")
    print("="*40)

def preview_word_list(filename):
    try:
        with open(filename) as f:
            words = [line.strip() for line in f if line.strip()]
        preview = words[:5]
        print(f" '{filename}' contains {len(words)} words.")
        print("First few words:", ', '.join(preview) + ('...' if len(words) > 5 else ''))
        return words
    except FileNotFoundError:
        print(f"File '{filename}' not found. Using default list.")
        return load_word_list()

def select_word_list():
    print("Choose word list:")
    print("1. Default")
    print("2. Enter custom filename")
    choice = input("Your choice (1/2): ").strip()
    if choice == '2':
        filename = input("Enter filename (e.g., history_words.txt): ").strip()
        words = preview_word_list(filename)
        use_this = input("Use this list? (y/n): ").strip().lower()
        if use_this == 'y':
            return words
        else:
            print("Using default word list.")
    return load_word_list()

def clear_high_scores(filename=HIGH_SCORES_FILE):
    with open(filename, "w") as f:
         json.dump([], f)
    print(f"Leaderboard cleared from {filename}.")

def show_high_scores_by_mode(mode, filename=HIGH_SCORES_FILE):
    try:
        with open(filename) as f:
            scores = json.load(f)
        filtered = [s for s in scores if s.get('mode', '').lower() == mode.lower()]
        if not filtered:
            print(f"No high scores yet for {mode} mode!")
            return
        print(f"Leaderboard - {mode.title()} Mode:")
        for s in filtered:
            print(f"{s['name']} guessed '{s['word']}' in {s['tries']} tries.")
    except FileNotFoundError:
        print("No high scores yet!")

def run_game(mode, multiplayer, WORD_LIST, player_roles, player_scores, MAX_TRIES, user_tier):
    tries = 0
    guessed = False
    previous_guesses = set()
    early_quit = False

    if multiplayer == 'y':
        print(f"{player_roles[0]}, enter the secret word (Player 2, look away!):")
        secret_word = input("Secret word:").strip().lower()
    else:
        secret_word = random.choice(WORD_LIST)

    if user_tier != "free":
        print("Your premium hint:", WORD_HINTS.get(secret_word, "No hint available for this word."))

    print("\nGuess the secret word!")

    while not guessed and tries < MAX_TRIES:
        try:
            guess = input("Your guess (or type 'give up' to quit): ").strip()
            if not guess:
                raise ValueError("Input cannot be blank!")
            if is_give_up(guess):
                print(f"You gave up! The word was '{secret_word}'.")
                early_quit = True
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
    return guessed, tries, secret_word, early_quit, previous_guesses

def get_last_user(filename= "last_user.json"):
    try:
        with open(filename) as f:
            return json.load(f).get('username', None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
def save_last_user(username, filename="last_user.json"):
    with open(filename, 'w') as f:
        json.dump({"username": username}, f)

def log_session(username, secret_word, guesses, result, mode, filename="session_history.txt"):
    with open(filename, 'a') as f:
        f.write(
            f"User: {username}, Word: {secret_word}, Guesses: {guesses}, "
            f"Result: {result}, Mode: {mode}\n"
        )

def log_user_progress(username, mode, guessed, tries, filename="user_progress.json"):
    entry = {
        "username": username,
        "mode": mode,
        "result": "Win" if guessed else "Loss",
        "tries": tries,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(filename) as f:
            all_data = json.load(f)
    except Exception:
        all_data = []
    all_data.append(entry)
    with open(filename, "w") as f:
        json.dump(all_data, f, indent=2)

def show_user_progress(filename="user_progress.json"):
    try:
        with open(filename) as f:
            all_data = json.load(f)
        from collections import defaultdict
        summary = defaultdict(lambda: {"games": 0, "wins": 0, "losses": 0, "total_tries": 0})
        for entry in all_data:
            summary[entry["username"]]["games"] += 1
            if entry["result"] == "Win":
                summary[entry["username"]]["wins"] += 1
            else:
                summary[entry["username"]]["losses"] += 1
            summary[entry["username"]]["total_tries"] += entry["tries"]
        for user, stats in summary.items():
            wins = stats["wins"]
            losses = stats["losses"]
            games = stats["games"]
            avg_tries = stats["total_tries"] / wins if wins else 0
            print(f"\nUser: {user}")
            print(f"  Games played: {games}")
            print(f"  Wins: {wins}, Losses: {losses}")
            print(f"  Average tries per win: {avg_tries:.2f}")
    except FileNotFoundError:
        print("No progress log found.")

def export_user_progress_csv(json_file="user_progress.json", csv_file="user_progress.csv"):
    try:
        with open(json_file) as fin, open(csv_file, "w") as fout:
            data = json.load(fin)
            if data:
                headers = list(data[0].keys())
                fout.write(",".join(headers) + "\n")
                for entry in data:
                    row = [str(entry.get(h, "")) for h in headers]
                    fout.write(",".join(row) + "\n")
                print(f"User progress exported to {csv_file}.")
            else:
                print("No data to export.")
    except FileNotFoundError:
        print("No user progress history to export.")

def view_edit_profile(username, filename="last_user.json"):
    print(f"Username: {username}")

    action = input("Do you want to change your username? (y/n): ").strip().lower()
    if action == 'y':
        new_username = input("Enter a new username: ").strip()
        save_last_user(new_username, filename)
        print(f"Username updated to {new_username}. (Please restart the app to fully update session if needed.)")
    else:
        print("No changes made.")

def print_help_about(user_tier):
    print("="*40)
    print("Word Guessing Game — Help/About")
    print("\nHow to Play:")
    print("- Guess the secret word by typing your guess. Responses are not case-sensitive.")
    print("- Type 'give up' to reveal the answer and quit the round.")
    print("- Type 'y' or 'n' to answer yes/no prompts.")
    print("- Multiplayer: Take turns with Player 1 setting the word and Player 2 guessing.")

    print("\nFeature Tiers:")
    print("- Free: 1 save slot, default word list, essentials only.")
    if user_tier != "free":
        print("- Paid/Premium: Up to 3 (paid) or 5+ (premium) save slots, import custom word lists, advanced stats.")
    if user_tier == "admin":
        print("- Admin: All premium features, plus clear leaderboard, view user progress, export history, and manage word lists.")

    print("\nMain Menu Navigation:")
    print("- Play Game: Start a new round (set mode and multiplayer each time).")
    print("- View Leaderboard: Shows the top five scoring rounds.")
    print("- View Leaderboard by Mode: See best games by easy/hard difficulty.")
    if user_tier != "free":
        print("- Import Word List: Use a custom list of words (supports .txt files).")
    if user_tier == "admin":
        print("- Clear Leaderboard: Reset all high scores.")
        print("- View User Progress: See games played, wins/losses, average tries per user.")
    print("- Help/About: View instructions and feature info.")
    print("- Quit: Exit the game.")

    print("\nFAQ:")
    print("Q: How do I switch or import a word list?")
    print("A: Choose the 'Import Word List' menu option (paid/premium), then select or type the file name.")
    print("Q: What if I enter an invalid menu choice or word?")
    print("A: The app will give you another chance, always with a clear error message.")
    print("Q: How are wins/losses tracked?")
    print("A: By difficulty, and for both solo and multiplayer games. Premium users get personalized stats.")
    print("="*40)

def export_session_history_csv(txt_file="session_history.txt", csv_file="session_history.csv"):
    try:
        with open(txt_file) as fin, open(csv_file, "w") as fout:
            fout.write("username,word,guesses,result,mode,timestamp\n")
            for line in fin:
                # Example line: "User: Justin, Word: python, Guesses: ['code', 'java', 'python'], Result: Win, Mode: easy"
                try:
                    parts = {k.strip(): v.strip() for k, v in (field.split(":", 1) for field in line.split(",") if ":" in field)}
                    username = parts.get("User", "")
                    word = parts.get("Word", "")
                    guesses = parts.get("Guesses", "")
                    result = parts.get("Result", "")
                    mode = parts.get("Mode", "")
                    timestamp = parts.get("timestamp", "")  # Add if you save timestamps
                    fout.write(f"{username},{word},{guesses},{result},{mode},{timestamp}\n")
                except Exception:
                    continue
        print(f"Session history exported to {csv_file}.")
    except FileNotFoundError:
        print("No session history to export.")

def view_individual_user_log(filename="user_progress.json"):
    try:
        user = input("Enter username to view details: ").strip()
        with open(filename) as f:
            all_data = json.load(f)
        entries = [e for e in all_data if e["username"].lower() == user.lower()]
        if not entries:
            print(f"No games found for user {user}.")
        else:
            print(f"\nDetailed log for {user}:")
            for entry in entries:
                print(f"  {entry['datetime']} | {entry['mode']} | {entry['result']} | Tries: {entry['tries']}")
    except FileNotFoundError:
        print("No user progress found.")

if __name__ == '__main__':
    last_user = get_last_user()
    if last_user:
        print(f"Welcome back, {last_user}!")
        use_prev = input("Use this username? (y/n): ").strip().lower()
        if use_prev != 'y':
            username = input("Enter your username: ").strip()
            save_last_user(username)
        else:
            username = last_user
    else:
        username = input("Enter your username: ").strip()
        save_last_user(username)
    print_welcome_menu()
    WORD_LIST = select_word_list()
    if not WORD_LIST:
        print("Warning: Word list is empty. Exiting.")
        exit()
    user_tier = get_user_tier()
    MAX_SLOTS = TIERS[user_tier]
    print(f"Welcome {user_tier.title()} user! You have {MAX_SLOTS} save slot(s) available.")

    wins_easy = 0
    losses_easy = 0
    wins_hard = 0
    losses_hard = 0
    win_tries_easy = []
    win_tries_hard = []

    while True:
        print("\nMenu Options:")
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. View Leaderboard by Mode")
        print("4. Quit")
        print("5. Help/About")
        if user_tier != "free":
            print("6. Import word list")
        if user_tier == 'admin':
            print("7. Clear Leaderboard")
        if user_tier == 'admin':
            print("8. View User Progress")
        if user_tier == 'admin':
            print("9. Export User Progress History to CSV")
        if user_tier != 'admin':
            print("10. View/Edit Profile")
        if user_tier == 'admin':
            print("11. Export Session/Game History to CSV")
        if user_tier == 'admin':
            print("12. View Individual User Game Log")

        choice = input("Choose an option: ")

        if choice == '1':
            while True:
                mode = input("Select difficulty (easy/hard): ").strip().lower()
                if mode in ('easy', 'hard'):
                    break
                print("Invalid input. Please type 'easy' or 'hard'.")
            MAX_TRIES = 5 if mode == 'hard' else 10
            multiplayer = input("Multiplayer? (y/n): ").strip().lower()
            player_scores = {player_roles[0]: 0, player_roles[1]: 0} if multiplayer == 'y' else None

            guessed, tries, secret_word, early_quit, previous_guesses = run_game(
                mode, multiplayer, WORD_LIST, player_roles, player_scores, MAX_TRIES, user_tier
            )

            if early_quit:
                break

            # Update stats by mode
            if mode == 'hard':
                if guessed:
                    wins_hard += 1
                    win_tries_hard.append(tries)
                else:
                    losses_hard += 1
            else:
                if guessed:
                    wins_easy += 1
                    win_tries_easy.append(tries)
                else:
                    losses_easy += 1

            # Leaderboard
            if guessed:
                name = input("Enter your name for the leaderboard: ") if multiplayer == 'y' else username
                save_high_score(name, secret_word, tries, mode)
                show_high_scores()

            # Log session
            log_session(
                username, secret_word, list(previous_guesses),
                "Win" if guessed else "Loss", mode
            )
            log_user_progress(username, mode, guessed, tries)
            # Averages/stats
            if win_tries_easy:
                avg_easy = average_tries(win_tries_easy)
                print(f"Easy mode average tries: {avg_easy:.2f}")
            if win_tries_hard:
                avg_hard = average_tries(win_tries_hard)
                print(f"Hard mode average tries: {avg_hard:.2f}")
            if not win_tries_easy and not win_tries_hard:
                print("No wins yet, so no average guess.")

            print(f"Easy mode - Wins: {wins_easy}, Losses: {losses_easy}")
            print(f"Hard mode - Wins: {wins_hard}, Losses: {losses_hard}")
            print(f"Total games won: {wins_easy + wins_hard}, Total games lost: {losses_easy + losses_hard}")
            if multiplayer == 'y':
                print(f"Scores: {player_roles[0]}: {player_scores[player_roles[0]]}, {player_roles[1]}: {player_scores[player_roles[1]]}")

            # Option to save after each round
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
                    'wins_easy': wins_easy,
                    'losses_easy': losses_easy,
                    'wins_hard': wins_hard,
                    'losses_hard': losses_hard,
                    'win_tries_easy': win_tries_easy,
                    'win_tries_hard': win_tries_hard
                }
                save_game_state(slot, state)

            # Multiplayer role swap
            if multiplayer == 'y':
                swap = input("Swap roles for the next round? (y/n): ").strip().lower()
                if swap == 'y':
                    player_roles.reverse()

            # Option to change word list
            change = input("Change or import a new word list? (y/n): ").strip().lower()
            if change == 'y':
                WORD_LIST = select_word_list()

        elif choice == '2':
            show_high_scores()
        elif choice == '3':
            mode_choice = input("Mode? (easy/hard): ").strip().lower()
            show_high_scores_by_mode(mode_choice)
        elif choice == '4':
            print("Goodbye! Thanks for playing!")
            break
        elif choice == '5':
            print_help_about(user_tier)
        elif choice == '6' and user_tier != "free":
            WORD_LIST = select_word_list()
        elif choice == '7' and user_tier == 'admin':
            clear_high_scores()
        elif choice == '8' and user_tier == 'admin':
            show_user_progress()
        elif choice == '9' and user_tier == 'admin':
            export_user_progress_csv()
        elif choice == '10' and user_tier != 'free':
            view_edit_profile(username)
        elif choice == '11' and user_tier == 'admin':
            export_session_history_csv()
        elif choice == '12' and user_tier == 'admin':
            view_individual_user_log()