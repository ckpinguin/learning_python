from words import word_list
import random


class TypingSpeedTest:
    def __init__(self, sentence=""):
        self.score = 0
        self.sentence = sentence

    def set_new_random_sentence(self, max_num_words=9):
        self.sentence = self._create_random_sentence(max_num_words)

    def _create_random_sentence(self, max_num_words):
        sentence_len: int = random.randint(3, max_num_words)
        sentence = ""
        for i in range(sentence_len):
            word: str = random.choice(word_list)
            sentence += f" {word}"
        sentence += "."
        return sentence

    def calculate_typing_speed(self, start_type_time, end_type_time):
        # Calculate typing speed in words per minute (WPM) and
        # types per minute (TPM)
        if start_type_time is not None and end_type_time is not None:
            elapsed_time = end_type_time - start_type_time
            if elapsed_time > 0:
                self.typing_speed_wpm = int(
                    (self.total_words_typed / elapsed_time) * 60)
                self.typing_speed_cpm = int(
                    (self.total_characters_typed / elapsed_time) * 60)

    def check_word_in_sentence(self, word) -> bool:
        if word in self.sentence:
            self.sentence = self.sentence.replace(word, "")
            return True
        return False

    def reset_stats(self):
        self.typing_speed_wpm = 0
        self.typing_speed_cpm = 0
        self.avg_typing_speed_wpm = 0
        self.avg_typing_speed_cpm = 0
        self.total_words_typed = 0
        self.total_characters_typed = 0
