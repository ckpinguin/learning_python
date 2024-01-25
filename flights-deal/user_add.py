from user_manager import UserManager

user_manager = UserManager()

print("""Welcome to the Flight Club
      where we find the best flight deals and email you!""")
first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")
email = input("What is your email?\n")
email2 = input("Please type your email again for confirmation\n")


if (email == email2):
    result = user_manager.register_user(first_name, last_name, email)

if result:
    print("You're in the club!")
