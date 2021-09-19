class Game:
    """
    Class for the game mechanics. All it does is it directs the piece-moving of the players.
    """
    def __init__(self, board, player1, player2):
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2

    @staticmethod
    def move(column, player):
        """
        Makes the given player move on the given column <column> (if the player is human), or tells the player
        to choose its move (if the player is the AI)
        :param column: The column where the move should be made; Integer
        :param player: The player making the move; Player class instance
        """
        player.move(column, player.symbol)
