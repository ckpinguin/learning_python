# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".

# Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
# Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
# Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp


def read_template(template):
    with open(template) as file:
        content = file.read()
    return content


def replace_content(content: str, name_to_insert):
    placeholder = '[name]'
    return content.replace(placeholder, name_to_insert)


def write_letter(content, name):
    with open(f"./Output/ReadyToSend/letter_for_{name}.txt", "w") as letter:
        letter.write(content)


def main():
    template_content = read_template('./Input/Letters/starting_letter.txt')

    with open("./Input/Names/invited_names.txt") as file:
        for line in file:
            name = line.strip()
            new_content = replace_content(template_content, name)
            write_letter(new_content, name)


main()
