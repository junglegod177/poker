class Table:
    def __init__(self, num_seats=7) -> None:
        self.num_seats = num_seats
        self.seats = [None] * num_seats
        self.dealer = None
        self.players = []
        self.deck = Deck()  # Assuming you have a Deck class for managing cards

    def sit_down(self, player, seat_num):
        if self.seats[seat_num] is None:
            self.seats[seat_num] = player
            return True
        else:
            print("Seat is already taken.")
            return False

    def start_game(self):
        # Start the game by dealing cards, setting up blinds, etc.
        # You can implement this method based on your game rules.
        pass

    def end_game(self):
        # End the game and distribute winnings, if any.
        # You can implement this method based on your game rules.
        pass

    def __str__(self):
        table_info = f"Table with {self.num_seats} seats:\n"
        for i, player in enumerate(self.seats):
            if player is not None:
                table_info += f"Seat {i+1}: {player}\n"
            else:
                table_info += f"Seat {i+1}: Empty\n"
        return table_info
    

class Player:
    def __init__(self) -> None:
        pass