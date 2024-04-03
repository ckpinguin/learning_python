from art import logo
from translation_table import morse_code_dict
import argparse


def text_to_morse(text: str):
    morse = ''.join(morse_code_dict.get(char.upper(), '') +
                    ' ' for char in text).strip()
    return morse


def main():
    parser = argparse.ArgumentParser(
        description="Simple text to python translator")
    parser.add_argument('input_string', type=str,
                        help="Input string to be translated to Morse code")
    args = parser.parse_args()

    input_string: str = args.input_string

    print(logo)
    print(text_to_morse(input_string))


if __name__ == '__main__':
    main()
