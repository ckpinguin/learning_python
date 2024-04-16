from words import word_list
import random


class TypingSpeedTest:
    def __init__(self, sentence=""):
        self.score = 0
        self.sentence = sentence

    def set_new_random_sentence(self, max_num_words=9):
        self.sentence = self._create_random_sentence(max_num_words)
        print(f"new sentence: {self.sentence}")

    def _create_random_sentence(self, max_num_words) -> str:
        sentence_len: int = random.randint(3, max_num_words)
        words = [random.choice(word_list) for _ in range(sentence_len)]
        sentence = ' '.join(words)
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
        print(f"Checking word {word}")
        if word in self.sentence:
            return True
        return False

    def remove_word_from_sentence(self, word):
        self.sentence = self.sentence.replace(word, '', 1).strip()
        print(f"New sentence: {self.sentence}")

    def is_sentence_finished(self) -> bool:
        return len(self.sentence) == 0

    def update_stats(self, word):
        self.total_words_typed += 1
        self.total_characters_typed += len(word)

    def reset_stats(self):
        self.typing_speed_wpm = 0
        self.typing_speed_cpm = 0
        self.avg_typing_speed_wpm = 0
        self.avg_typing_speed_cpm = 0
        self.total_words_typed = 0
        self.total_characters_typed = 0
