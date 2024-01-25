from art import logo
import random
import os

############### Blackjack Project #####################

#Difficulty Normal 😎: Use all Hints below to complete the project.
#Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
#Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
#Difficulty Expert 🤯: Only use Hint 1 to complete the project.

############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.



##################### Hints #####################

#Hint 1: Go to this website and try out the Blackjack game: 
#   https://games.washingtonpost.com/games/blackjack/
#Then try out the completed Blackjack project here: 
#   http://blackjack-final.appbrewery.repl.run

DEALER_RISK_LIMIT=17
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def get_card():
  return random.choice(cards)

def get_starting_hand():
  return [get_card(), get_card()]

def get_cards_sum(card_list):
  sum = 0
  for card in card_list:
    # Ace can count as 1 or 11
    if card == 11 and sum < 11:
      card = 1
    sum += card
  return sum

def blackjack(cards_list):
  return get_cards_sum(cards_list) == 21

def busted(cards_list):
  return get_cards_sum(cards_list) > 21

def get_winner():
  sum1 = get_cards_sum(user_cards)
  sum2 = get_cards_sum(dealer_cards)
  busted1 = busted(user_cards)
  busted2 = busted(dealer_cards)
  
  if busted1 and busted2: return 0
  elif busted1: return 2
  elif busted2: return 1
  
  if sum1 > sum2: return 1
  elif sum1 < sum2: return 2
  else: return 0

def print_blackjack_winner():
  if blackjack(user_cards):
    if blackjack(dealer_cards):
      print("It's a Blackjack draw!!!")
      return True
    print("You win with Blackjack! 😎")
    return True
  else:
    if blackjack(dealer_cards):
      print("Dealer has Blackjack and you lose 😒")
      return True
    else:
      return False

def print_final_hands():
  print(f"Your final hand: {user_cards}, final score: {get_cards_sum(user_cards)}")
  print(f"Dealer's final hand: {dealer_cards}, final score: {get_cards_sum(dealer_cards)}")

def print_starting_hands():
  print(f"Your initial cards are: {user_cards[0]} and {user_cards[1]}, that makes {get_cards_sum(user_cards)} points.")
  print(f"Dealer's first card is {dealer_cards[0]}.")

def print_winner():
  winner = get_winner()
  if winner == 1:
    print("You win! 😊")
  elif winner == 2:
    print("Dealer wins, you lose! 😒")
  else:
    print("It's a draw! ❌")
    
continue_game = input("Do you want to play a round of Blackjack (y/n)? ") == "y"

while continue_game:
  os.system('clear')
  print(logo)
  
  user_cards = get_starting_hand()
  dealer_cards = get_starting_hand()
  print_starting_hands()

  if blackjack(user_cards) or blackjack(dealer_cards):
    print_blackjack_winner()
    round_ongoing = False
  else:
    round_ongoing = True

  round_ongoing = input("Do you want to get another card (y/n)? ") == "y"
  
  while round_ongoing:
    user_cards.append(get_card())
    user_sum = get_cards_sum(user_cards)
    print(f"Your cards: {user_cards}, current score: {user_sum}")
    if busted(user_cards):
      print(f"Busted! You got {user_sum} now 💥")
      round_ongoing = False
      break
    else:
      if blackjack(user_cards) or blackjack(dealer_cards):
        print_blackjack_winner()
        round_ongoing = False
    round_ongoing = input("Do you want to get another card (y/n)? ") == "y"
    
  while get_cards_sum(dealer_cards) < DEALER_RISK_LIMIT:
    dealer_cards.append(get_card())

   
  print_final_hands()
  print_winner()
    
  continue_game = input("\n\nDo you want to play a round of Blackjack (y/n)? ") == "y"

  
      
    
  
    
  
  

  
  



# Extra hints #

#Hint 2: Read this breakdown of program requirements: 
#   http://listmoz.com/view/6h34DJpvJBFVRlZfJvxF
#Then try to create your own flowchart for the program.

#Hint 3: Download and read this flow chart I've created: 
#   https://drive.google.com/uc?export=download&id=1rDkiHCrhaf9eX7u7yjM1qwSuyEk-rPnt

#Hint 4: Create a deal_card() function that uses the List below to *return* a random card.
#11 is the Ace.
#cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

#Hint 5: Deal the user and computer 2 cards each using deal_card() and append().
#user_cards = []
#computer_cards = []

#Hint 6: Create a function called calculate_score() that takes a List of cards as input 
#and returns the score. 
#Look up the sum() function to help you do this.

#Hint 7: Inside calculate_score() check for a blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in our game.

#Hint 8: Inside calculate_score() check for an 11 (ace). If the score is already over 21, remove the 11 and replace it with a 1. You might need to look up append() and remove().

#Hint 9: Call calculate_score(). If the computer or the user has a blackjack (0) or if the user's score is over 21, then the game ends.

#Hint 10: If the game has not ended, ask the user if they want to draw another card. If yes, then use the deal_card() function to add another card to the user_cards List. If no, then the game has ended.

#Hint 11: The score will need to be rechecked with every new card drawn and the checks in Hint 9 need to be repeated until the game ends.

#Hint 12: Once the user is done, it's time to let the computer play. The computer should keep drawing cards as long as it has a score less than 17.

#Hint 13: Create a function called compare() and pass in the user_score and computer_score. If the computer and user both have the same score, then it's a draw. If the computer has a blackjack (0), then the user loses. If the user has a blackjack (0), then the user wins. If the user_score is over 21, then the user loses. If the computer_score is over 21, then the computer loses. If none of the above, then the player with the highest score wins.

#Hint 14: Ask the user if they want to restart the game. If they answer yes, clear the console and start a new game of blackjack and show the logo from art.py.

