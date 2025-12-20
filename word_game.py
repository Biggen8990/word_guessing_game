import random

WORD_LIST = ["python", "code", "fun", "test", "guess"]
MAX_TRIES = 10

def is_guess_correct(secret_word, guess):
    return guess.lower() == secret_word.lower()

def get_hint(secret_word, guess):
    guess = guess.lower()
    secret_word = secret_word.lower()
    if guess < secret_word:
        return "after"
    elif guess > secret_word:
        return "before"
    else:
        return "correct"

if __name__ == '__main__':
    while True:
        secret_word = random.choice(WORD_LIST)
        tries = 0
        guessed = False
        previous_guesses = set()
        print("\nGuess the secret word!")

        while not guessed and tries < MAX_TRIES:
            try:
                guess = input("Your guess: ").strip()
                if not guess:
                    raise ValueError("Input cannot be blank!")
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
                    if guess < secret_word:
                        print("Hint: The word comes after your guess alphabetically.")
                    elif guess > secret_word:
                        print("Hint: The word comes before your guess alphabetically.")
            except ValueError as e:
                print("Error:", e)

        if not guessed:
            print(f"Sorry, out of tries! The word was {secret_word}")
        again = input("Play again? (y/n): ")
        if again.lower() != 'y':
            break