import os
from art import logo

def get_highest_bidder(bids):
  max_bid = 0
  winner = ""
  for id in bids:
    bid_amount = bids[id]
    if bid_amount > max_bid:
      max_bid = bid_amount
      winner = id
  return winner 

print(logo)

bids = {}
bidding = True

while bidding:
  name = input("What is your name?: ")
  bid = int(input("What's your bid?: $"))
  os.system('clear')
  bids[name] = bid
  should_continue = input("Are there more bidders (yes/no)?:\n")
  if should_continue == "no":
    bidding = False

print(f"The highest bid of came from {get_highest_bidder(bids)}!")


