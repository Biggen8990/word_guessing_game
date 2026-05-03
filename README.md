Word Guessing Game (Web Edition) 
A user-friendly, customizable word guessing game for students, teachers, and casual players. Play solo or multiplayer, import your own word lists, and unlock advanced features with higher-level tiers. Includes leaderboard, stats logging, and teacher/admin tools for the classroom or group competitions.
 
 Features 
🎮 Interactive gameplay: guess the secret word with contextual and alphabetical hints
🔄 Multi-slot save/resume (slots unlocked by tier)
👥 Multiplayer support (PvP hotseat with score tracking)
🏆 High scores and average tries tracker by mode and user
🗂️ Import/preview custom word lists for endless content
🛡️ Profile and tier selection for users and admins
📋 Session/game logging, admin stats/reporting, and session export (CSV)
💡 Contextual hints from built-in or custom lists
✅ Full test suite for every main feature
 
 How to Play 
Log in or create a user profile (stored locally).
Choose a word list (default, import your own, or switch at any time).
Pick difficulty mode (easy/hard) and single or multiplayer.
Guess the word! Use hints, save games, and see your stats.
Teachers/admins can view/monitor all users and export session reports.
 
 Tiered Features 
Tier	Save Slots	Custom Lists	Advanced Stats	Admin Tools
Free	1	No	Basic	No
Paid	3	Yes	Yes	No
Premium	5+	Yes	Yes	No
Admin	10	Yes	Yes	All
 
 Menu Navigation 
Play Game: Start a new round and guess the word!
View Leaderboard: Top scores overall and by mode.
Help/About: Game instructions, FAQ, and tier info.
Profile: View or change your username and tier.
Import Word List/Manage Words (Paid+): Upload or switch custom lists.
Admin: Clear leaderboard, view/export user progress, and more.
Save/Resume: Multi-slot support based on your tier.
 
 Tech Stack 
Python 3.x
Flask (for web UI and routing)
HTML/CSS (templating)
JSON (for save files, logs, and progress)
Automated testing: unittest
 
 Getting Started 
Clone/download this repo.
Install Flask with pip3 install flask.
Run with python3 app_web.py.
Open a browser to http://localhost:5000
Use built-in or custom word lists (.txt, one word per line).
 
 Testing 
Test all features and logic with:
 
python3 word_game_test.py
 
 Author 
Justin McVey | 03/22/2026 | GitHub: Biggen8990
