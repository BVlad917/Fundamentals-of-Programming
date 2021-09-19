class UI:
    def __init__(self, players_service):
        self.__players_service = players_service
        self.__commands = {
            '1': self.__ui_display_all_players,
            '2': self.__ui_start_tournament,
        }

    @staticmethod
    def __print_menu():
        print("1 - Display all players\n"
              "2 - Start\n"
              "x - Exit\n")

    def __ui_display_all_players(self):
        all_players = self.__players_service.get_all_players()
        for player in all_players:
            print(player)

    def __ui_start_tournament(self):
        no_players = len(self.__players_service.get_all_players())
        if not ((no_players & (no_players-1) == 0) and no_players != 0):
            print("Qualifying round.")
            qualifying_players = self.__players_service.get_lowest_players()
            self.__make_players_play(qualifying_players)
            print("Remaining players: ")
            self.__ui_display_all_players()

        print("\nKnock-out stage.")
        while len(self.__players_service.get_all_players()) != 1:
            print(f"\nLast {len(self.__players_service.get_all_players())}.")
            player_pairs = self.__players_service.get_random_player_pairs()
            self.__make_players_play(player_pairs)

        print("\nThe winner is:")
        print(self.__players_service.get_all_players()[0])

    def __make_players_play(self, pairs_of_players_list):
        for player1, player2 in pairs_of_players_list:
            print()
            print(player1)
            print("plays with")
            print(player2)
            winner_id = int(input("Give the ID of the winner: "))
            if winner_id == player1.id:
                player1 = self.__players_service.increase_player_strength(player1)
                self.__players_service.add_player(player1)
            else:
                player2 = self.__players_service.increase_player_strength(player2)
                self.__players_service.add_player(player2)

    def run(self):
        while True:
            self.__print_menu()
            cmd = input("Please give a command: ").strip()
            if cmd == 'x':
                break
            elif cmd == '1':
                self.__commands['1']()
            elif cmd == '2':
                self.__commands['2']()
                print("Tournament over. Bye!")
                break
            else:
                print("Invalid command.")
