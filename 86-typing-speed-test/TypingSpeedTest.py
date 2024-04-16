from words import word_list
import random


class TypingSpeedTest:
    def __init__(self, test_sequence: str = ""):
        self.score = 0
        self.test_sequence = test_sequence

    def create_random_sentence(self):
        sentence_len: int = random.randint(3, 10)
        sentence = ""
        for i in range(sentence_len):
            word: str = random.choice(word_list)
            sentence += f" {word}"
        sentence += "."
        return sentence
