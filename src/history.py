from datetime import datetime

class HistoryEntry:
    def __init__(self, date: int, duration: int, moves: int, win: bool, width: int, height: int, mines: int, remaining_mines: int):
        self.date = datetime.fromtimestamp(date)
        self.duration = duration
        self.moves = moves
        self.win = win
        self.width = width
        self.height = height
        self.mines = mines
        self.remaining_mines = remaining_mines
    
    def __str__(self):
        return f"{int(self.date.timestamp())}, {self.duration}, {self.moves}, {self.win}, {self.width}, {self.height}, {self.mines}, {self.remaining_mines}"
    
    @staticmethod
    def from_string(s):
        date, duration, moves, win, width, height, mines, remaining_mines = s.split(", ")
        return HistoryEntry(int(date), int(duration), int(moves), win == "True", int(width), int(height), int(mines), int(remaining_mines))


history_singleton = None
class History:
    def __init__(self):
        try:
            with open("history.txt", "r") as f:
                self._history = [HistoryEntry.from_string(entry) for entry in f.readlines()]
        except FileNotFoundError:
            self._history = []
    
    @staticmethod
    def get_instance():
        global history_singleton
        if history_singleton is None:
            history_singleton = History()
        return history_singleton

    # cant be bothered to support paging or anything, the history will never get that large
    def get_history(self):
        return self._history
    
    def add_entry(self, entry: HistoryEntry):
        self._history.append(entry)
        with open("history.txt", "a") as f:
            f.write(str(entry) + "\n")
