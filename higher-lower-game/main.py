from art import logo, vs
from game_data import data
import random
import os


print(logo)
data_len = len(data)
taken_choices = []


def get_random_choice():
    choice = random.choice(data)
    # taken_choices.append(choiceA)
    return choice


def compare_followers(choiceA, choiceB):
    if choiceA['follower_count'] > choiceB['follower_count']:
        return 'a'
    else:
        return 'b'


def format_choice(choice):
    return f"{choice['name']}, a {choice['description']}, from {choice['country']}"


def get_guess():
    return input("Who has more followers? Type 'A' or 'B': ").lower()


choiceA = get_random_choice()
score = 0

while True:
    choiceB = get_random_choice()
    # Prevent duplicate comparisons
    if choiceA == choiceB:
        choiceB = get_random_choice()

    print(format_choice(choiceA))
    print(vs)
    print(format_choice(choiceB))

    guess = get_guess()

    if guess == compare_followers(choiceA, choiceB):
        score += 1
        print(f"You are right! 🎉 Your score now is {score}\n")
        input("Press enter to continue")
        os.system('clear')
        print(logo)
        choiceA = choiceB
    else:
        print(f"You are wrong! Game over...😭 Final score is {score}")
        break
