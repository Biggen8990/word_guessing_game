Word Guessing Game (Python Console)

A simple replayable word guessing game built in Python. Users guess a randomly selected secret word from a list, with hints, guess limits, and automated checks for repeated or blank inputs. Easily extendable for new features like scoring, word lists, or mobile apps.

# Word Guessing Game (v1.1)

Version 1.1 adds:
- Load secret words from a customizable file
- "Give up" option to reveal the answer
- Guess limit and replay scoring (wins/losses)
- Functional test scripts for automated logic testing

## Features
- Random word selection from a preset list
- Guess limit with automatic loss message
- Input validation (no blanks; prevents repeated guesses)
- Alphabetical “before/after” hints after wrong guesses
 Option to replay after each round
- Clean, testable codebase with functions suitable for unit testing

## How to Play
Run: `python3 word_game.py`
Guess the word, or type 'give up' to reveal. Your win/loss stats are tracked per session.

## How to Test
Run: `python3 word_game_test.py`
All key logic and features are validated automatically.

## Requirements
- Python 3.x

## Future Plans
- Add high score tracking and leaderboard
- Build a mobile app (iOS/Android)
- Optional multiplayer and additional word packs

## Author
Justin McVey | [GitHub](https://github.com/Biggen8990)
