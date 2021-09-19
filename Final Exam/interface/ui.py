from errors.exceptions import BoardException, GameOverException


class Console:
    def __init__(self, game):
        self.__game = game

    def __print_board(self):
        print(self.__game.get_board())

    def __ui_move(self, params):
        if len(params) >= 2:
            print("Invalid number of parameters")
        elif len(params) == 0:
            self.__game.move()
        else:
            steps = int(params[0])
            self.__game.move(steps)

    def __ui_change_dir(self, direction):
        direction = direction[0]
        self.__game.change_direction(direction)

    def start(self):
        game_over = False
        while not game_over:
            self.__print_board()
            cmd = input(">>>")
            cmd = cmd.strip()
            if cmd == "":
                continue
            cmd, params = self.__ui_process_command(cmd)
            if cmd == 'move':
                try:
                    self.__ui_move(params)
                except BoardException as be:
                    print(str(be))
                except IndexError:
                    print("Game over.")
                    return
                except GameOverException as ge:
                    print(str(ge))
                    return
            elif cmd in ('left', 'right', 'up', 'down'):
                try:
                    self.__ui_change_dir(cmd)
                except BoardException as be:
                    print(str(be))
                except IndexError:
                    print("Game over.")
                    return
                except GameOverException as ge:
                    print(str(ge))
                    return
            else:
                print("Invalid command.")

    @staticmethod
    def __ui_process_command(cmd):
        parts = cmd.split()
        return parts[0], parts[1:]
