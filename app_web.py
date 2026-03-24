from flask import Flask, session, render_template, request, redirect, url_for
from word_game import load_high_scores
import random
import json

DEMO_MODE = True

WORD_HINTS = { "god": "Who doesn't ever change?", 
              "lord": "He's the King of Kings and...", 
              "jesus": "The only name above all names.", 
              "love": "Opposite of hate?", 
              "joy": "... to the World, the Lord has come.", 
              "peace": "The Prince of...",
              "patience": "A fruit of the spirit, starts with the letter P.", 
              "kindness": "The opposite of not careing about others.", 
              "goodness": "I will sing of the ________ of God.", 
              "gentleness": "Non-agressive", 
              "faithfulness": "Fully trusting.", 
              "long-suffering": "Similar to Patience.", 
              "meekness": "... is not weakness.", 
              "faith": "_____, Hope, and Love...", 
              "grace": "Probably the only hymnal everyone knows. It's 'Amazing'.",                                                                                                                                                                              #JRM 12-23-2025 
              "redemption": "Your __________ draws near.", 
              "repent":"Acts 2:38 says to ______ and be baptized...", 
              "salvation": "The plan of _________." 
              }

WORD_LIST = ( "God",
             "Lord",
             "Jesus",
             "Love",
             "Joy",
             "Peace",
             "Patience", 
             "Kindness", 
             "Goodness", 
             "Gentleness", 
             "Faithfulness", 
             "Long-suffering", 
             "Meekness", 
             "Faith", 
             "Grace",                                                                                                                                                                              #JRM 12-23-2025 
             "Redemption", 
             "Repent", 
             "Salvation")

app = Flask(__name__)

import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def get_hint(secret_word, guess):
    guess = guess.lower()
    secret_word = secret_word.lower()
    if guess < secret_word:
        return "after"
    elif guess > secret_word:
        return "before"
    else:
        return "correct"
    
def clear_high_scores(filename="high_scores.json"):
    with open(filename, "w") as f:
        json.dump([], f)
    print(f"Leaderboard cleared from {filename}.")

def show_user_progress(filename="user_progress.json"):
    user_tier = session.get('user_tier', 'free')
    if user_tier != 'admin':
        return "Forbidden", 403
    try:
        with open(filename) as f:
            all_data = json.load(f)
        
    except FileNotFoundError:
        print("No progress log found.")

        all_data = []
    from collections import defaultdict
    summary = defaultdict(lambda: {"games": 0, "wins": 0, "losses": 0, "total_tries": 0})
    for entry in all_data:
        summary[entry["username"]]["games"] += 1
        if entry["result"] == "Win":
            summary[entry["username"]]["wins"] += 1
        else:
            summary[entry["username"]]["losses"] += 1
        summary[entry["username"]]["total_tries"] += entry["tries"]
    
    users = [
        {
            "username": user,
            "games": stats["games"],
            "wins": stats["wins"],
            "losses": stats["losses"],
            "avg_tries": stats["total_tries"] / stats["games"] if stats["games"] else 0
        }
        for user, stats in summary.items()
    ]
    return render_template("user_progress.html", users=users)

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

@app.route('/')
def main_menu():
    user_tier = session.get('user_tier', 'free')
    username = session.get('username', 'Guest')
    return render_template('main.html', user_tier=user_tier, username=username, demo_mode=DEMO_MODE)

@app.route('/')
def home():
    username = session.get('username', 'Guest')
    user_tier = session.get('user_tier', 'free')
    return render_template('main.html', user_tier=user_tier, username=username, demo_mode=DEMO_MODE)

def get_unique_user_count(filename="user_progress.json"):
    try:
        with open(filename) as f:
            data = json.load(f)
        usernames = {entry["username"] for entry in data}
        return len(usernames)
    except Exception:
        return 0
    
DEMO_MODE = get_unique_user_count() < 10

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Default values for GET/display
    user_tier = session.get('user_tier', 'free')
    username = session.get('username', 'Guest')

    if request.method == 'POST':
        entered_username = request.form['username'].strip()
        selected_tier = request.form['tier']
        # Tier locking: only allow upgrade if in demo mode or user picks 'free'
        if not DEMO_MODE and selected_tier != 'free':
            flash('Upgrades to paid/premium/admin are coming soon!')
            selected_tier = 'free'
        # Save to session for use in routes/templates
        session['username'] = entered_username
        session['user_tier'] = selected_tier
        return redirect(url_for('home')) 

    # Pass variables to pre-fill/display on the profile page
    return render_template(
        'profile.html',
        user_tier=user_tier,
        username=username,
        demo_mode=DEMO_MODE
    )

@app.route('/play', methods=['GET', 'POST'])
def play():
    user_tier = session.get('user_tier', 'free')
    if request.args.get('new'):
        session.pop('secret_word', None)
        session.pop('guessed', None)
        session.pop('tries', None)
        session.pop('previous_guesses', None)

    if 'secret_word' not in session:
        session['secret_word'] = random.choice(WORD_LIST).strip().lower()
        session['tries'] = 0
        session['guessed'] = False
        session['previous_guesses'] = []

    message = ""
    hint = WORD_HINTS.get(session['secret_word'], "No hint available.")
    game_over = False
    guessed = session.get('guessed', False)
    tries = session.get('tries', 0)

    if request.method == 'POST':
        guess = request.form['guess'].strip()
        session['tries'] += 1
        tries = session['tries']
        if not guess:
            message = "Input cannot be blank."
        elif guess.lower() == session['secret_word']:
            message = f"Congratulations! You guessed the word: {session['secret_word']}"
            session['guessed'] = True
            guessed = True
            game_over = True
            hint = None
        else:
            if guess in session['previous_guesses']:
                message = "You already guessed that!"
            else:
                session['previous_guesses'].append(guess)
                message = "Not the right word, try again!"
            hint = WORD_HINTS.get(session['secret_word'], "No hint available.")
            alpha_hint = get_hint(session['secret_word'], guess)
            if alpha_hint in ("before", "after"):
                hint += f" The word comes {alpha_hint} your guess alphabetically."

    if session.get('guessed', False) or session['tries'] >= 10:
        game_over = True
        hint = None

    return render_template(
        'play.html',
        message=message,
        hint=hint,
        game_over=game_over,
        guessed=guessed
    )

@app.route('/leaderboard')
def leaderboard():
    user_tier = session.get('user_tier', 'free')
    scores = load_high_scores()
    return render_template('leaderboard.html', scores=scores)

@app.route('/import-word-list', methods=['GET', 'POST'])
def import_word_list():
    user_tier = session.get('user_tier', 'free')
    if request.method == 'POST':
        new_words = []
        filename = request.form['filename']
        with open(filename) as f:
            new_words = [line.strip() for line in f if line.strip()]
        if new_words:
            global WORD_LIST
            WORD_LIST = new_words
        return redirect('/play')
    return render_template('import_word_list.html')

@app.route('/leaderboard-by-mode', methods=['GET', 'POST'])
def leaderboard_by_mode():
    user_tier = session.get('user_tier', 'free')
    mode = None
    scores = []
    if request.method == 'POST':
        mode = request.form['mode'].strip().lower()
        all_scores = load_high_scores()
        # Filter scores for the chosen mode (easy or hard)
        scores = [s for s in all_scores if s.get('mode', '').lower() == mode]
    return render_template('leaderboard_by_mode.html', scores=scores)

@app.route('/help')
def help_page():
    user_tier = session.get('user_tier', 'free')
    return render_template('help.html', user_tier=user_tier)

@app.route('/clear-leaderboard')
def clear_leaderboard_route():
    user_tier = session.get('user_tier', 'free')
    if user_tier != 'admin':
        return "Forbidden", 403
    clear_high_scores()
    return redirect(url_for('main_menu'))

@app.route('/user-progress')
def user_progress():
    user_tier = session.get('user_tier', 'free')
    if user_tier != 'admin':
        return "Forbidden", 403
    # Show user progress as HTML, or redirect/print it
    # You might render a new template here for prettiness:
    show_user_progress()
    return redirect(url_for('main_menu'))

@app.route('/export-history')
def export_history():
    user_tier = session.get('user_tier', 'free')
    if user_tier != 'admin':
        return "Forbidden", 403
    export_user_progress_csv()  # Or your function to create CSV
    # You can redirect to a download or just confirm export
    return redirect(url_for('main_menu'))

if __name__ == "__main__":
    app.run(debug=True)