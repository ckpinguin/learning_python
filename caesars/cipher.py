import art

art.print_title()

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']




def caesar(start_text, shift_amount, cypher_direction):

  result = ""
  
  if cypher_direction == "decode":
    shift_amount = shift * -1
      
  for char in start_text:
    if char not in alphabet:
      result += char
      continue
    position= alphabet.index(char)
   
    new_position = (position + shift_amount) % len(alphabet)
    result += alphabet[new_position]
    
  print(f"The {cypher_direction}d text is {result}")

is_finished = False
while not is_finished:
  direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
  text = input("Type your message:\n").lower()
  shift = int(input("Type the shift number:\n"))
  caesar(start_text=text, shift_amount=shift, cypher_direction=direction)
  want_continue = input("Do you want to continue (yes / no)?")
  if want_continue == "no":
    is_finished = True

exit(0)