from art import logo


def add(n1, n2):
  return n1 + n2

def sub(n1, n2):
  return n1 - n2

def mul(n1, n2):
  return n1 * n2

def div(n1, n2):
  return n1 / n2

operations = {
  "+": add,
  "-": sub,
  "*": mul,
  "/": div,
  }

def calculator():
  print(logo)

  num1 = float(input("What is the first number? "))
  for symbol in operations:
    print(symbol)
    
    
  should_continue = True

  while should_continue:
    op = input("Pick an operation: ")
    num2 = float(input("What's the next number? "))
    calculation_function = operations[op]
    result = calculation_function(num1, num2)

    print(f"{num1} {op} {num2} = {result}")

    if input(f"Type 'y' to continue calculating with {result}, or 'n' to exit: ") == "y":
      num1 = result
    else:
      should_continue = False
      calculator()
      
calculator()