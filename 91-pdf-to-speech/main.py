import PyPDF2
import pyttsx3
import argparse


def pdf_to_text(pdf_path: str) -> str:
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text


def write_text_to_file(text: str, output_txt: str) -> None:
    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


def speak_text(text: str) -> None:
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Speak the text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert PDF to text.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file.')
    parser.add_argument('output_txt', type=str,
                        help='Path to the output text file.')

    args = parser.parse_args()

    text = pdf_to_text(args.pdf_path)
    write_text_to_file(text, args.output_txt)
    speak_text(text)
