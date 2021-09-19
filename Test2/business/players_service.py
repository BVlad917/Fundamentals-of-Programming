import random


class PlayersService:
    def __init__(self, players_repo):
        self.__players_repo = players_repo

    def get_all_players(self):
        """
        Method that returns all the players in the repository
        """
        return self.__players_repo.elems

    def sort_players_by_strength(self):
        """
        Method that sorts the players in the repository (in ascending order)
        """
        all_players = self.__players_repo.elems
        all_players.sort(key=lambda x: x.strength)
        self.__players_repo.elems = all_players

    def get_lowest_players(self):
        """
        Method that selects the players with the lowest strengths and returns a list of random pairs of these
        players. It selects as many players as it is needed for the repository to have the number of players be
        a power of 2. It also modifies the repository itself, keeping only the players that will not be included
        in the qualification round.
        :return: The list of random player pairs that will play in the qualification round.
        """
        self.sort_players_by_strength()
        no_players = len(self.__players_repo.elems)
        qualification_no_players = (no_players - self.__highest_power_of_2(no_players)) * 2
        qualification_players = self.__players_repo.elems[:qualification_no_players]
        non_qualification_players = self.__players_repo.elems[qualification_no_players:]
        player_pairs = self.__form_player_pairs(qualification_players)
        self.__players_repo.elems = non_qualification_players
        return player_pairs

    def add_player(self, player):
        """
        Method that adds a player to the repository
        :param player: The player to be added
        """
        self.__players_repo.add_player(player)
        # self.__players_repo.elems.append(player)

    def get_random_player_pairs(self):
        """
        Method that returns pairs of players (chosen randomly) out of the currently available players in the
        repository. This function should be used only once we know that the number of players in the repository
        is a power of 2.
        :return: List of random players pairs (player1, player2) made with the players from the repository.
        """
        return self.__form_player_pairs(self.__players_repo.elems)

    def __form_player_pairs(self, players_list):
        """
        Given a list of players, it returns a list of randomly formed player pairs (player1, player2).
        :param players_list: The list of players out of which we form the player pairs
        :return: The list of randomly formed player pairs
        """
        player_pairs = []
        while players_list:
            rand1 = self.__pop_random(players_list)
            rand2 = self.__pop_random(players_list)
            pair = rand1, rand2
            player_pairs.append(pair)
        return player_pairs

    @staticmethod
    def increase_player_strength(player):
        """
        Method that increases the strength of a player by 1
        :param player: The player whose strength we want increased
        :return: The same player, but with an increased strength (by 1)
        """
        player.strength = player.strength + 1
        return player

    @staticmethod
    def __pop_random(lst):
        """
        Method that takes in a list as parameter and returns a random element from this list, removing said element
        from the list
        :param lst: The list from which we want to get a random element from
        :return: The random element from the function
        """
        idx = random.randrange(0, len(lst))
        return lst.pop(idx)

    @staticmethod
    def __highest_power_of_2(n):
        res = 0
        for i in range(n, 0, -1):
            if (i & (i - 1)) == 0:
                res = i
                break
        return res
