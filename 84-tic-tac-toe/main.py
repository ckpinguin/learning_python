
class TicTacToe:
    def __init__(self):
        self.fields = [' ' for _ in range(9)]

    def print_field(self, field):
        print(field)

    def print_sep_line(self):
        for i in range(3):
            print('---')

    def print_board(self):
        for i in range(3):
            self.print_field(self.fields[i*3:i*3+3])
            self.print_sep_line()

    def check_winner(self):
        pass

    def process_input(self, user_input):
        pass

    def game_loop(self):
        while True:
            user_input = input()
            if user_input == 'q':
                return
            self.process_input(user_input)


def main():
    print("Tic Tac Toe!")
    print("Press 'q' to quit anytime")
    game = TicTacToe()
    game.game_loop()


if __name__ == '__main__':
    main()
