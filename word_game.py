secret_word = "python"
tries = 0
guessed = False

print("Guess the secret word!")

while not guessed:
    try:
        guess = input("Your guess: ").strip()
        tries += 1
        if not guess:
            raise ValueError("Input cannot be blank!")
        if guess.lower() == secret_word:
            print(f"Congratulations! You guessed the word in {tries} tries!")
            guessed = True
        else:
            print("Not the right word, try again!")
    except ValueError as e:
        print("Error:", e)