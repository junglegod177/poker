class Player:
    def __init__(self) -> None:
        self._is_sitting = False

    def get_is_sitting(self):
        return self._is_sitting
    
    def set_is_sitting(self, bool) -> None:
        self._is_sitting = bool