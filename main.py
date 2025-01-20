import random
import os
import requests
from colorama import Fore, Style, init

init()

def fetch_words():
    global words
    url = "https://raw.githubusercontent.com/gaspertheghost0/hangman/refs/heads/main/words.py"
    response = requests.get(url)
    
    if response.status_code == 200:
        exec(response.text, globals())
    else:
        print(f"{Fore.RED}Failed to retrieve words.py from GitHub!{Style.RESET_ALL}")
        exit()

fetch_words()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_word(difficulty):
    return random.choice(words[difficulty])

def display_hangman(tries):
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        --------
        """
    ]

    if tries >= len(stages):
        tries = len(stages) - 1
    return stages[tries]

def ending_screen(message, word):
    clear_terminal()
    print(f"\n{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
    print(f"{Fore.GREEN if 'Congratulations' in message else Fore.RED}{message.center(40)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}The word was: {word.center(40)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
    input(f"\n{Fore.MAGENTA}Press Enter to return to the main menu.{Style.RESET_ALL}")
    clear_terminal()
    main_menu()

def hangman():
    clear_terminal()
    print(f"{Fore.CYAN}Welcome to Hangman!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Choose a difficulty level: easy, medium, hard, impossible.{Style.RESET_ALL}")
    
    while True:
        difficulty = input(f"{Fore.GREEN}Enter difficulty: {Style.RESET_ALL}").lower()
        if difficulty in ["easy", "medium", "hard", "impossible"]:
            break
        print(f"{Fore.RED}Invalid difficulty. Please choose easy, medium, hard, or impossible.{Style.RESET_ALL}")
    
    word = get_word(difficulty)
    max_tries = 8 if difficulty == "easy" else 6 if difficulty == "medium" else 5 if difficulty == "hard" else 3
    guessed_word = ["_"] * len(word)
    guessed_letters = set()
    tries = 0

    while True:
        clear_terminal()
        print(f"{Fore.CYAN}HANGMAN - Difficulty: {difficulty.capitalize()}{Style.RESET_ALL}")
        print(display_hangman(tries))
        print(f"\n{Fore.YELLOW}Word: {Style.RESET_ALL}{' '.join(guessed_word)}")
        print(f"{Fore.MAGENTA}Guessed letters: {Style.RESET_ALL}{', '.join(sorted(guessed_letters))}")
        print(f"{Fore.GREEN}Tries remaining: {max_tries - tries}{Style.RESET_ALL}")
        
        if tries >= max_tries:
            ending_screen(f"Game Over! You've run out of attempts. The correct word was: '{word}'.", word)
            return

        guess = input(f"\n{Fore.BLUE}Guess a letter or the full word: {Style.RESET_ALL}").lower()

        if len(guess) == 1:
            if not guess.isalpha():
                print(f"{Fore.RED}Please enter a valid letter!{Style.RESET_ALL}")
                continue
            if guess in guessed_letters:
                print(f"{Fore.RED}You already guessed that letter!{Style.RESET_ALL}")
                continue
            
            guessed_letters.add(guess)
            
            if guess in word:
                print(f"{Fore.GREEN}Good guess! The letter '{guess}' is in the word.{Style.RESET_ALL}")
                for i, letter in enumerate(word):
                    if letter == guess:
                        guessed_word[i] = guess
            else:
                print(f"{Fore.RED}Wrong guess! The letter '{guess}' is not in the word.{Style.RESET_ALL}")
                tries += 1
        
        elif len(guess) == len(word):
            if guess == word:
                ending_screen(f"Congratulations! You guessed the word!", word)
                return
            else:
                print(f"{Fore.RED}Wrong guess! The word is not '{guess}'.{Style.RESET_ALL}")
                tries += 1
        else:
            print(f"{Fore.RED}Invalid input. Guess a single letter or the full word.{Style.RESET_ALL}")
            continue

        if "_" not in guessed_word:
            ending_screen(f"Congratulations! You guessed the word!", word)
            return

def main_menu():
    print(f"{Fore.CYAN}Welcome to Hangman!{Style.RESET_ALL}")
    print("1. Start Game")
    print("2. Exit")
    
    while True:
        choice = input(f"\n{Fore.GREEN}Enter choice (1 or 2): {Style.RESET_ALL}")
        if choice == "1":
            hangman()
            break
        elif choice == "2":
            clear_terminal()
            print(f"{Fore.YELLOW}Thank you for playing!{Style.RESET_ALL}")
            exit()
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")

if __name__ == "__main__":
    main_menu()
