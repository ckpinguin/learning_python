from art import logo
import os
import random

HARD_LEVEL_TURNS = 5
EASY_LEVEL_TURNS = 10


def check_user_guess_success(guess, rand_num):
    if guess == rand_num:
        print(f"You got it! The answer was {rand_num} 🏆.")
        return True
    elif guess > rand_num:
        print("Too high 🚀.")
        return False
    elif guess < rand_num:
        print("Too low 📉.")
        return False
    else:
        raise Exception("Invalid input.")


def set_difficulty():
    difficulty = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
    if difficulty == "easy":
        return EASY_LEVEL_TURNS
    elif difficulty == "hard":
        return HARD_LEVEL_TURNS
    else:
        raise Exception("Invalid input.")


def game():
    finished = False
    number_of_attempts = 0

    while not finished:
        print(logo)
        print("Welcome to the Number Guessing Game!")
        number_of_attempts = set_difficulty()
        print("I'm thinking of a number between 1 and 100.")
        rand_num = random.randint(1, 100)
        # Debug: print(f"Pssst, the correct answer is {rand_num}")

        while number_of_attempts > 0:
            guess = int(input("Make a guess: "))
            if check_user_guess_success(guess, rand_num):
                break
            number_of_attempts -= 1

            if number_of_attempts == 0:
                print("You've run out of guesses, you lose 🙀.")
                break
            print(
                f"You have {number_of_attempts} attempts remaining to guess the number.")
        more = input("Another round? (y/n): ").lower()
        if more == "n":
            finished = True
            print("Goodbye 👋.")
        elif more == "y":
            os.system("clear")
        else:
            raise Exception("Invalid input.")


game()
