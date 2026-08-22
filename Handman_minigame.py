import random

def choose_word():
    words = ["PYTHON", "C", "PROGRAMMING", "DEVELOPER", "COMPUTER", "ALGORITHM"]
    return random.choice(words)

def display_hangman(tries):
    stages = [
        """
           +---+
           |   |
               |
               |
               |
               |
         =========""",
        """
           +---+
           |   |
           O   |
               |
               |
               |
         =========""",
        """
           +---+
           |   |
           O   |
           |   |
               |
               |
         =========""",
        """
           +---+
           |   |
           O   |
          /|   |
               |
               |
         =========""",
        """
           +---+
           |   |
           O   |
          /|\\  |
               |
               |
         =========""",
        """
           +---+
           |   |
           O   |
          /|\\  |
          /    |
               |
         =========""",
        """
           +---+
           |   |
           O   |
          /|\\  |
          / \\  |
               |
         ========="""
    ]
    return stages[tries]

def play():
    word_to_guess = choose_word()
    guessed_letters = set()
    used_letters = set()
    errors = 0
    max_errors = 6

    print("=== HANGMAN GAME ===")

    while errors < max_errors:
        print(display_hangman(errors))
        
        word_display = " ".join([letter if letter in guessed_letters else "_" for letter in word_to_guess])
        print(f"\nWord to guess: {word_display}")
        print(f"Guessed letters: {', '.join(sorted(used_letters))}")

        if set(word_to_guess) == guessed_letters:
            print(f"\n Congratulations! You found the word: {word_to_guess}")
            return True

        guess = input("Guess a letter: ").strip().upper()

        if len(guess) != 1 or not guess.isalpha():
            print(" Error: Please enter a single valid letter.")
            continue

        if guess in used_letters:
            print(" You already tried that letter!")
            continue

        used_letters.add(guess)

        if guess in word_to_guess:
            guessed_letters.add(guess)
            print(" Good job!")
        else:
            errors += 1
            print(" Sorry, that letter is not in the word.")

    print(display_hangman(errors))
    print(f"\n Game Over! The word was: {word_to_guess}")
    return False

def main():
    while True:
        play()
        choice = input("\nDo you want to play again? (y/n): ").strip().lower()
        if choice != 'y':
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
