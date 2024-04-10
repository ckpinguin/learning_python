
class TicTacToe:
    def __init__(self):
        self.fields: list[str] = [' ' for i in range(9)]
        self.actual_field: int
        self.actual_player = "X"

    def print_sep_line(self):
        for i in range(11):
            print('-', end='')
        print()

    def print_introduction_board(self):
        print('Introduction Board')
        print(' 1 | 2 | 3 ')
        self.print_sep_line()
        print(' 4 | 5 | 6 ')
        self.print_sep_line()
        print(' 7 | 8 | 9 ')
        self.print_sep_line()

    def print_board(self):
        for i in range(3):  # lines
            for j in range(3):  # columns
                separator = '|' if j < 2 else ''
                print(f' {self.fields[i*3 + j]} {separator}', end='')
            print()
            self.print_sep_line() if i < 2 else None

    def check_winner(self):
        # Check rows
        for i in [0, 3, 6]:
            if self.fields[i] == self.fields[i+1] == self.fields[i+2] != ' ':
                print(f'Player {self.actual_player} wins!')
                exit(0)

        # Check columns
        for i in range(3):
            if self.fields[i] == self.fields[i+3] == self.fields[i+6] != ' ':
                print(f'Player {self.actual_player} wins!')
                exit(0)

        # Check the two diagonals
        if self.fields[0] == self.fields[4] == self.fields[8] != ' ' or \
                self.fields[2] == self.fields[4] == self.fields[6] != ' ':
            print(f'Player {self.actual_player} wins!')
            exit(0)

    def process_input(self, user_input: str) -> bool:
        field = int(user_input)
        if field < 1 or field > 9:
            print("ERROR: Field number is out of range (1-9)")
            return False
        self.actual_field = field - 1
        return True

    def set_field(self, field: int, symbol: str):
        if self.fields[field] != ' ':
            print("ERROR: This field is already set")
            return
        self.fields[field] = symbol

    def switch_player(self):
        self.actual_player = 'X' if self.actual_player == 'O' else 'O'

    def game_loop(self):
        self.print_introduction_board()
        print('''Example input: "3" for field 3.
Starting with Player "X"''')
        while True:
            user_input = input(
                f'Player {self.actual_player}, enter your move: ')
            if user_input == 'q':
                return
            if self.process_input(user_input):
                self.set_field(self.actual_field, self.actual_player)
                self.print_board()
                self.check_winner()
                self.switch_player()


def main():
    print("Tic Tac Toe!")
    print("Press 'q' to quit anytime")
    game = TicTacToe()
    game.game_loop()


if __name__ == '__main__':
    main()
