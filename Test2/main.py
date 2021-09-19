from business.players_service import PlayersService
from persistency.file_players_repo import FilePlayersRepo
from presentation.ui import UI

if __name__ == "__main__":
    players_repo = FilePlayersRepo("players.txt")
    players_service = PlayersService(players_repo)
    ui = UI(players_service)
    ui.run()
