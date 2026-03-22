from flask import Flask, session, render_template, request, redirect, url_for
from word_game import load_high_scores

DEMO_MODE = True

WORD_LIST = [
    "God", "Lord", "Jesus", "Love", "Joy", "Peace",
    "Patience", "Kindness", "Goodness", "Gentleness",
    "Faithfulness", "Long-suffering", "Meekness", "Faith", "Grace", 
    "Redemption", "Repent", "Salvation"
]

app = Flask(__name__)

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
    import random
    if 'secret_word' not in session:
        session['secret_word'] = random.choice(WORD_LIST)
        session['tries'] = 0
        session['guessed'] = False
        session['previous_guesses'] = []

    message = ""
    hint = None
    game_over = False

    if request.method == 'POST':
        guess = request.form['guess'].strip()
        session['tries'] += 1
        if not guess:
            message = "Input cannot be blank."
        elif guess.lower() == session['secret_word']:
            message = f"Congratulations! You guessed the word: {session['secret_word']}"
            session['guessed'] = True
            game_over = True
        else:
            if guess in session['previous_guesses']:
                message = "You already guessed that!"
            else:
                session['previous_guesses'].append(guess)
                message = "Not the right word, try again!"
                hint = f"Hint: The word comes {'after' if guess.lower() < session['secret_word'] else 'before'} your guess alphabetically."

    if session.get('guessed') or session['tries'] >= 10:
        game_over = True

    return render_template(
        'play.html',
        message=message,
        hint=hint,
        game_over=game_over
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

if __name__ == "__main__":
    app.run(debug=True)