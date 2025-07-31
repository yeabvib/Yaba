# A simple visualizer. More advanced versions could draw a full grid.

PLAYER_EMOJIS = ["🔴", "🔵", "🟡", "🟢"]

def generate_board_string(game, players_map):
    """
    Generates a text representation of the current game state.
    """
    player1_id = game.creator_id
    player2_id = game.opponent_id
    
    p1_emoji = PLAYER_EMOJIS[0]
    p2_emoji = PLAYER_EMOJIS[1]

    p1_name = players_map[player1_id]
    p2_name = players_map[player2_id]

    board_state = game.board_state
    
    def get_token_status(player_id):
        tokens = board_state.get(str(player_id), [])
        yard = tokens.count(0)
        finished = tokens.count(999)
        on_board = 4 - yard - finished
        return f"Yard: {yard}, On Board: {on_board}, Home: {finished}"

    p1_status = get_token_status(player1_id)
    p2_status = get_token_status(player2_id)
    
    current_player_id = game.current_turn_id
    current_player_name = players_map[current_player_id]
    
    status_text = (
        f"**🏆 Win Condition: {game.win_condition} Token(s) Home**\n"
        f"**💰 Pot: {game.pot} ETB**\n\n"
        f"{p1_emoji} **{p1_name}**: {p1_status}\n"
        f"{p2_emoji} **{p2_name}**: {p2_status}\n\n"
        f"-----------------------------------\n"
        f"It's **{current_player_name}'s** turn!"
    )
    
    return status_text