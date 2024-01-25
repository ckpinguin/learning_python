from art import logo
from menu import menu

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}


def print_menu():
    for drink in menu:
        print("- ", drink)


def prompt_user():
    print("\nWelcome! What would you like?\n")
    print_menu()
    return input("\nYour choice: ").lower()


def print_report():
    print("\n")
    for key, value in resources.items():
        if key == "water" or key == "milk":
            print(key.capitalize() + ": " + str(value) + "ml")
        elif key == "coffee":
            print(key.capitalize() + ": " + str(value) + "g")
        elif key == "money":
            print(key.capitalize() + ": $" + str(value))


def check_resources(drink):
    ingredients = get_ingredients(drink)
    for ingredient, amount in ingredients.items():
        if not check_enough_ingredient(ingredient, amount):
            print(
                f"Sorry there is not enough {ingredient}, maybe try something else?")
            return False
    return True


def get_ingredients(drink):
    return menu[drink.capitalize()]["ingredients"]


def check_enough_ingredient(ingredient, amount):
    if resources[ingredient] >= amount:
        return True
    else:
        return False


def get_price(drink):
    return menu[drink.capitalize()]["cost"]


def prompt_for_coins():
    quarter = int(input("How many quarters?: "))
    dime = int(input("How many dimes?: "))
    nickle = int(input("How many nickles?: "))
    penny = int(input("How many pennies?: "))

    coin_value = calculate_coins_value(quarter, dime, nickle, penny)
    return coin_value


def calculate_coins_value(quarter, dime, nickle, penny):
    return (quarter * 0.25) + (dime * 0.1) + (nickle * 0.05) + (penny * 0.01)


def check_transaction_success(coins_value, drink):
    drink_price = menu[drink.capitalize()]["cost"]
    if coins_value == drink_price:
        take_money(coins_value)
        return True
    elif coins_value > drink_price:
        print(f"You have put in ${coins_value:.2f}")
        take_money(drink_price)
        change_value = coins_value - drink_price
        give_change(change_value)
        return True
    else:
        return False


def take_money(amount):
    resources["money"] += amount


def give_change(value):
    coins = calculate_coins_from_amount(value)
    rounded_value = round(value, 2)
    print(f"Giving back change for ${rounded_value:.2f}:")
    print(f"Quarters: {coins[0]}")
    print(f"Dimes: {coins[1]}")
    print(f"Nickles: {coins[2]}")
    print(f"Pennies: {coins[3]}")


def calculate_coins_from_amount(value):
    quarters = int(value / 0.25)
    value = value % 0.25
    dimes = int(value / 0.1)
    value = value % 0.1
    nickles = int(value / 0.05)
    value = value % 0.05
    pennies = int(value / 0.01)
    return [quarters, dimes, nickles, pennies]


def make_coffee(drink):
    ingredients = get_ingredients(drink)
    for ingredient, amount in ingredients.items():
        resources[ingredient] -= amount
    print(f"Here is your {drink} ☕️. Enjoy!")


def refund(value):
    print(f"Money refunded: {value}")


def main_loop():
    print(logo)
    machine_running = True
    while machine_running:
        try:
            user_choice = prompt_user()
            if user_choice == "off":
                print("\nTurning off machine...\n")
                machine_running = False
            elif user_choice == "report":
                print_report()
            else:
                user_choice = user_choice.capitalize()
                if check_resources(user_choice):
                    price = f"{get_price(user_choice):.2f}"
                    print(f"{user_choice} costs ${price}.")
                    print("Please insert coins.")
                    coin_value = prompt_for_coins()
                    while not check_transaction_success(coin_value, user_choice):
                        print("Not enough money, please insert more coins.")
                        if input("Continue y/n?") == "n":
                            refund(coin_value)
                            break
                        coin_value += prompt_for_coins()
                    # check again, because after possible break we get here
                    if check_transaction_success(coin_value, user_choice):
                        make_coffee(user_choice)
                else:
                    continue
        except KeyError as e:
            key_causing_error = e.args[0]
            print(f"Unknown command: {key_causing_error}")
            continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_loop()
