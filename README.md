Word Guessing Game (Python Edition)

A versatile, menu-based word guessing game supporting multi-slot saves, custom themes, user profiles, multiplayer, tiered features, statistics, and admin/teacher reporting—built for fun, learning, and real classroom use.
 
 Features 

Flexible word lists: Choose from defaults, import custom lists, or switch lists anytime
Hints: Contextual and alphabetical hints for every word (with premium early/extra hints)
Single-player and hotseat multiplayer (PvP), with score tracking and optional role swaps
Difficulty modes and stat tracking per mode
Multi-slot save/resume (slots/tier: 1/3/5+/admin)
User login/profile saving (auto-remembers last user)
Leaderboard: per-mode high scores, displayed after each win
Session/game history logging for parental/teacher review (saved to .txt and .json)
Admin controls: clear leaderboard, view/export user progress/history, and CSV export for audits
Fully tested with automated test suite
 
 How To Play

Choose your username/profile (auto-remembers last user)
Pick your tier (“free”, “paid”, “premium”, “admin”)
Pick an optional custom word list (for themes, lessons, or fun)
Set difficulty (easy/hard) and choose single or multiplayer
Try to guess the secret word!
Enter your guess, or type give up to reveal the answer and end the round.
Get hints and see win/loss stats, leaderboards, and your average guess count
Save and resume on any slot (more slots unlocked for paid/pro/admin)
Admins/teachers can view and export user progress/stats/reports
 
 Menu Navigation 

Play Game: Start a new round (single/multiplayer, mode selection)
View Leaderboard: View top scores
View Leaderboard by Mode: See scores for easy/hard
Help/About: See instructions, feature guide, FAQ
Import Word List (paid+): Add or switch to a custom list (.txt)
Clear Leaderboard (admin): Resets scores
View User Progress (admin): See per-user stats/logs, export CSV
Quit: Exit app
 
 Tier Features 

Tier	Save Slots	Custom Word List	Advanced Stats	Admin Controls
Free	1	        No	                Basic	        No
Paid	3	        Yes	                Yes	            No
Premium	5+	        Yes	                Yes         	No
Admin	10	        Yes	                Full	        Yes
 
 Testing

Automated test scripts included:
 
Validates word list loading, hint logic, multi-slot saves, search/guess correctness, tiered access, PvP scoring, high scores, windowing, and session history.
 
Run with:
 
1python3 word_game_test.py
 
 Quick FAQ

Q: How do I switch word lists?
 A: Choose "Import Word List" from the menu and preview/choose any .txt file (one word per line).
 
Q: Why are some menu options hidden or locked?
 A: Some advanced features (multi-slot, import/export, admin) require a non-free or admin tier.
 
 Author

Justin McVey | GitHub: Biggen8990 | Feb. 13th, 2026
