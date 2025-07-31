import random

# A simplified but functional Ludo logic representation
# In a real-world scenario, this would be much more complex.

class LudoGame:
    def __init__(self, players, win_condition):
        self.players = players  # List of telegram_ids [player1, player2]
        self.win_condition = win_condition
        self.current_player_idx = 0
        self.board_state = self._create_initial_state()
        self.dice_roll = 0
        self.roll_count = 0

    def _create_initial_state(self):
        # A simple representation. Key: player_id, Value: list of 4 token positions
        # 0 = in yard, 1-52 = on path, 100+ = in home column, 999 = finished
        return {
            self.players[0]: [0, 0, 0, 0],
            self.players[1]: [0, 0, 0, 0]
        }

    def roll_dice(self):
        roll = random.randint(1, 6)
        self.dice_roll = roll
        if roll == 6:
            self.roll_count += 1
        else:
            self.roll_count = 0

        if self.roll_count == 3:
            self.dice_roll = 0 # Forfeit turn
            self.next_turn()
            return 0 # Signifies a forfeited roll

        return roll

    def get_movable_tokens(self, player_id):
        # Simplified: returns token indices that can move
        tokens = self.board_state[player_id]
        movable = []
        for i, pos in enumerate(tokens):
            if self.dice_roll == 6 and pos == 0:
                movable.append(i) # Can move out of yard
            elif pos > 0 and pos < 999:
                movable.append(i) # Can move on board
        return movable

    def move_token(self, player_id, token_index):
        # This is a placeholder for the complex movement logic.
        # It should handle:
        # 1. Moving from yard (pos 0) to start.
        # 2. Moving along the 52-step path.
        # 3. Knocking out opponent tokens.
        # 4. Landing on safe zones.
        # 5. Creating blocks.
        # 6. Moving into the home column.
        # 7. Finishing with an exact roll.
        
        pos = self.board_state[player_id][token_index]
        if pos == 0 and self.dice_roll == 6:
             self.board_state[player_id][token_index] = 1 # Move to start
        elif pos > 0:
            self.board_state[player_id][token_index] += self.dice_roll

        # After move, check for win condition
        winner = self.check_win()
        return winner

    def check_win(self):
        for player_id, tokens in self.board_state.items():
            finished_tokens = sum(1 for pos in tokens if pos == 999)
            if finished_tokens >= self.win_condition:
                return player_id
        return None

    def next_turn(self):
        if self.dice_roll != 6 or self.roll_count == 3:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.dice_roll = 0
        self.roll_count = 0

    def get_current_player(self):
        return self.players[self.current_player_idx]