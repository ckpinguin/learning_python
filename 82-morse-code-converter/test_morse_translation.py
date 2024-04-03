import pytest
from morse_translator import text_to_morse


@pytest.mark.parametrize("text, expected_morse_code", [
    ("Hello", ".... . .-.. .-.. ---"),
    ("Hello, World!", ".... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--"),
    ("12345", ".---- ..--- ...-- ....- ....."),
    ("@$&", ".--.-. ...-..- .-..."),
    ("Hello World", ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."),
    ("", ""),
    ("Hello123@", ".... . .-.. .-.. --- .---- ..--- ...-- .--.-.")
])
def test_text_to_morse(text, expected_morse_code):
    assert text_to_morse(text) == expected_morse_code
