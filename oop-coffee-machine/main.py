from art import logo
from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()


def main_loop():
    running = True
    while running:
        choice = input(
            f"Welcome! Please choose drink from {menu.get_items()}: ")
        if choice == "off":
            running = False
            break
        elif choice == "report":
            coffee_maker.report()
            money_machine.report()
            continue
        drink = menu.find_drink(choice)
        if not drink:
            print("Invalid choice")
            continue
        if coffee_maker.is_resource_sufficient(drink):
            money_machine.make_payment(drink.cost)
            coffee_maker.make_coffee(drink)
        else:
            print("Insufficient resources: ")
            coffee_maker.report()

    print("Turning machine off...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(logo)
    main_loop()
