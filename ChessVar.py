# Author: Tal Nguyen
# GitHub Username: talietport
# Date: 11/28/2023
# Description: create a pseudo-chess game for two players.
# The player who capture all pieces of the same kind of the opponent wins the game.
# Movement of each piece is the same as the regular chess rules

class ChessVar:
    """
    a class that initializes the game-board and methods to play the game and checks for winner
    """
    def __init__(self):
        """
        initialize chess board, current player and piece counter for each player
        """
        self.board = self.setup_board()
        self.current_player = 1
        self.player_pieces = {1: {"pawn": 8, "rook": 2, "knight": 2, "bishop": 2, "king": 1, "queen": 1},
                              -1: {"pawn": 8, "rook": 2, "knight": 2, "bishop": 2, "king": 1, "queen": 1}}
    def setup_board(self):
        """
        Initialize a 8x8 board with pieces in their starting positions
        """
        board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        return board

    def display_board(self):
        """
        Display the current state of the chess board
        """
        for row in self.board:
            print(" ".join(row))
        print()
    PIECE_NAMES = {'pawn', 'rook', 'knight', 'bishop', 'king', 'queen'}

    def make_move(self, move):
        """
        Method that allows the player to make a move, update piece counts,
        checks validity, captures pieces, updates the board, then switches to the next player
        """
        start_col, start_row, end_col, end_row = self.parse_move(move)

        # Validate the move
        if not self.is_valid_move(start_col, start_row, end_col, end_row):
            return False

        # Check if there's a piece at the destination, if there's a piece on the destination, capture piece
        destination_piece = self.board[end_row][end_col]
        if destination_piece != ' ':
            self.capture_piece(destination_piece)

        # Move piece from one position on the board to another
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' '

        # Update piece counts to reflect any captured pieces
        self.update_piece_count(start_col, start_row, end_col, end_row)

        # Check for a winner
        winner = self.check_for_winner()
        if winner is not None:
            return True

        # Switch to the next player
        self.current_player *= -1
        return True

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if move is valid based on current player and piece type
        """
        player_piece = self.board[start_row][start_col]

        if self.current_player == 1 and player_piece not in ['P', 'R', 'N', 'B', 'Q', 'K']:
            return False
        elif self.current_player == -1 and player_piece not in ['p', 'r', 'n', 'b', 'q', 'k']:
            return False
        return True

    def is_valid_direction(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is in a valid direction: horizontal, vertical, diagonal
        """
        # test for distance between starting pos and ending pos to check if piece moves correctly
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        return dx == dy or dx == 0 or dy == 0      # check: diagonal or vertical or horizontal

    def capture_piece(self, piece):
        """
        Decrease the piece count for the opposing player
        """
        if piece.isupper():                 # white pieces
            opposing_player = -1            # opponent: black player
        else:
            opposing_player = 1             # if opponent is black player
        piece_name = piece.lower()
        self.player_pieces[opposing_player][piece_name] -= 1           # decrement piece count for opponent

    def update_piece_count(self, start_col, start_row, end_col, end_row):
        """
        update piece count after a move (current player and opponent)
        """
        player = self.current_player                            # current player
        start_piece = self.board[start_row][start_col].lower()  # piece name (starting pos)
        end_piece = self.board[end_row][end_col].lower()        # piece name (ending pos)

        # check if the piece exist in dictionary
        if start_piece not in self.player_pieces[player]:
            return "Error updating piece count: Invalid piece {start_piece} for player {player}"

        # if a piece was moved, decrement it
        self.player_pieces[player][start_piece] -= 1

        # decrement opponent' piece count for chess pieces (except pawn)
        if start_piece != 'p':
            if start_piece not in self.player_pieces[-player]:          # exception
                return "Error updating piece count: Invalid piece {start_piece} for player {-player}"
            self.player_pieces[-player][start_piece] -= 1

        # If a piece is captured at the destination, decrement opponents' count
        if end_piece != ' ':                                    # check if piece is captured
            if end_piece not in self.player_pieces[-player]:    # check type of captured piece
                return "Error updating piece count: Invalid piece {end_piece} for player {-player}"
            self.player_pieces[-player][end_piece] -= 1         # decrement piece for the opponent

    def check_for_winner(self):
        """
        Check if a player has lost all their pieces
        """
        for player, pieces in self.player_pieces.items():   # Loop through each player and their pieces
            has_pieces_left = False             # placeholder to check if the player has any pieces left
            for count in pieces.values():         # Check each count of pieces for the player
                if count != 0:                  # If any piece count is not 0, set the flag to True
                    has_pieces_left = True
                    break

            # If the player has no pieces left, return the winning player (positive for white, negative for black)
            if not has_pieces_left:
                return -player

        # If no player has lost all their pieces, return 0 (game still ongoing)
        return 0

    def get_game_state(self):
        """
        calls check_for_winner to determines a winner
        """
        winner = self.check_for_winner()
        if winner > 0:
            return 'WHITE_WON'
        elif winner < 0:
            return 'BLACK_WON'
        else:
            return 'UNFINISHED'

    def parse_move(self, move):
        """
        Convert algebraic notation to board indices
        """
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])
        return start_col, start_row, end_col, end_row

    def position_to_tuple(self, position):
        """
        convert position string to column and row
        """
        col, row = position[0], int(position[1])
        return col, row


class Queen:
    """
    queen chess piece rules
    """
    def __init__(self, chess_var):
        self.chess_var = chess_var

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is a valid queen move
        """
        return self.chess_var.is_valid_direction(start_col, start_row, end_col, end_row)

    def generate_queen_moves(self, current_position):
        """
        possible moves for queen
        """
        col, row = current_position
        col_index = ord(col) - ord('a') + 2  # Convert column to board index
        row_index = 10 - row  # Convert row to board index

        possible_moves = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for move in moves:  # iterate over possible directions
            for step in range(1, 8):  # iterate over number of steps
                new_x = col_index + step * move[0]  # calculate new position
                new_y = row_index + step * move[1]

                # check if the move is valid
                if self.is_valid_move(col_index, row_index, new_x, new_y):
                    new_col = chr(new_x - 2 + ord('a'))  # Convert back to column character
                    new_row = 10 - new_y  # Convert back to row index
                    destination_piece = self.chess_var.board[new_row][new_col]

                    # Check if the destination square is empty or contains an opponent's piece
                    if destination_piece == ' ' or (destination_piece.isupper() != self.chess_var.current_player == 1):
                        possible_moves.append((new_col, new_row))

                        # Stop extending moves in this direction if capturing a piece
                        if destination_piece != ' ':
                            break
        return possible_moves


class King:
    """
    king chess piece rules
    """
    def __init__(self, chess_var):
        self.chess_var = chess_var

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is a valid king move
        """
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        return (dx == 1 or dx == 0) and (dy == 1 or dy == 0)

    def generate_king_moves(self, current_position):
        """
        generate possible moves for the king based on its current position
        """
        col, row = current_position
        col_index = ord(col) - ord('a') + 2
        row_index = 10 - row

        possible_moves = []
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for move in moves:
            new_x = col_index + move[0]
            new_y = row_index + move[1]

            if self.is_valid_move(col_index, row_index, new_x, new_y):
                new_col = chr(new_x - 2 + ord('a'))  # Convert back to column character
                new_row = 10 - new_y  # Convert back to row index
                destination_piece = self.chess_var.board[new_row][new_col]

                # Check if the destination square is empty or contains an opponent's piece
                if destination_piece == ' ' or (destination_piece.isupper() != self.chess_var.current_player == 1):
                    possible_moves.append((new_col, new_row))

        return possible_moves


class Pawn:
    """
    Pawn chess piece rules
    """
    def __init__(self, chess_var):
        self.chess_var = chess_var

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is a valid pawn move
        """
        dx = abs(end_col - start_col)
        dy = end_row - start_row

        direction = 1 if self.chess_var.current_player == 1 else -1

        if dx == 0:
            # Moving forward
            if dy == direction and self.chess_var.board[end_row][end_col] == ' ':
                return True

            # Moving two squares forward from the starting position
            if dy == 2 * direction and start_row == (7 if direction == 1 else 2) and self.chess_var.board[end_row][end_col] == ' ':
                return True
        elif dx == 1 and dy == direction:
                                                                    # Capturing diagonally
            destination_piece = self.chess_var.board[end_row][end_col]
            if destination_piece != ' ' and destination_piece.isupper() != self.chess_var.current_player == 1:
                return True
        return False

    def generate_pawn_moves(self, current_position):
        """
        generate possible moves for the pawn based on its current position
        """
        col, row = current_position
        col_index = ord(col) - ord('a') + 2
        row_index = 10 - row

        possible_moves = []
        direction = 1 if self.chess_var.current_player == 1 else -1

        # Move forward one square
        new_x = col_index
        new_y = row_index + direction
        if self.is_valid_move(col_index, row_index, new_x, new_y):
            possible_moves.append((chr(new_x - 2 + ord('a')), 10 - new_y))

        # Move forward two squares from the starting position
        if row_index == 2 and self.chess_var.current_player == 1:
            new_y = row_index + 2 * direction
            if self.is_valid_move(col_index, row_index, col_index, new_y):
                possible_moves.append((chr(new_x - 2 + ord('a')), 10 - new_y))

        # Capture diagonally
        capture_moves = [(1, direction), (-1, direction)]
        for move in capture_moves:
            new_x = col_index + move[0]
            new_y = row_index + move[1]
            if self.is_valid_move(col_index, row_index, new_x, new_y):
                destination_piece = self.chess_var.board[new_y][new_x]
                if destination_piece != ' ' and destination_piece.isupper() != self.chess_var.current_player == 1:
                    possible_moves.append((chr(new_x - 2 + ord('a')), 10 - new_y))

        return possible_moves


class Rook:
    """
    rook piece chess rules
    """
    def __init__(self, chess_var):
        self.chess_var = chess_var

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is a valid rook move
        """
        return self.is_valid_direction(start_col, start_row, end_col, end_row)

    def is_valid_direction(self, start_col, start_row, end_col, end_row):
        """
        implement valid direction
        """
        return start_col == end_col or start_row == end_row

    def generate_rook_moves(self, current_position):
        """
        generate possible moves for the rook based on its current position
        """
        col, row = current_position
        col_index = ord(col) - ord('a') + 2
        row_index = 10 - row

        possible_moves = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            for step in range(1, 8):
                new_x = col_index + step * move[0]
                new_y = row_index + step * move[1]

                if self.is_valid_move(col_index, row_index, new_x, new_y):
                    new_col = chr(new_x - 2 + ord('a'))
                    new_row = 10 - new_y
                    destination_piece = self.chess_var.board[new_row][new_col]

                    # Check if the destination square is empty or contains an opponent's piece
                    if destination_piece == ' ' or (destination_piece.isupper() != self.chess_var.current_player == 1):
                        possible_moves.append((new_col, new_row))

                        # Stop extending moves in this direction if capturing a piece
                        if destination_piece != ' ':
                            break

        return possible_moves

class Bishop:
    """
    Bishop chess piece rules
    """
    def __init__(self, chess_var):
        self.chess_var = chess_var

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is a valid bishop move
        """
        return self.is_valid_direction(start_col, start_row, end_col, end_row)

    def is_valid_direction(self, start_col, start_row, end_col, end_row):
        """
        Implement valid direction for bishop
        """
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        return dx == dy

    def generate_bishop_moves(self, current_position):
        """
        Generate possible moves for the bishop
        """
        col, row = current_position
        col_index = ord(col) - ord('a') + 2
        row_index = 10 - row

        possible_moves = []
        moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for move in moves:
            for step in range(1, 8):
                new_x = col_index + step * move[0]
                new_y = row_index + step * move[1]

                if self.is_valid_move(col_index, row_index, new_x, new_y):
                    new_col = chr(new_x - 2 + ord('a'))
                    new_row = 10 - new_y
                    destination_piece = self.chess_var.board[new_row][new_col]

                    # Check if the destination square is empty or contains an opponent's piece
                    if destination_piece == ' ' or (destination_piece.isupper() != self.chess_var.current_player == 1):
                        possible_moves.append((new_col, new_row))

                        # Stop extending moves in this direction if capturing a piece
                        if destination_piece != ' ':
                            break

        return possible_moves


class Knight:
    """
    knight chess piece rules
    """
    def __init__(self, chess_var):
        self.chess_var = chess_var

    def is_valid_move(self, start_col, start_row, end_col, end_row):
        """
        Check if the move is an L-shaped knight move
        """
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    def generate_knight_moves(self, current_position):
        """
        generate possible moves for knight
        """
        col, row = current_position
        col_index = ord(col) - ord('a') + 2
        row_index = 10 - row

        possible_moves = []
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for move in moves:
            new_x = col_index + move[0]
            new_y = row_index + move[1]

            if self.is_valid_move(col_index, row_index, new_x, new_y):
                new_col = chr(new_x - 2 + ord('a'))
                new_row = 10 - new_y
                destination_piece = self.chess_var.board[new_row][new_col]

                # Knights can move 2 squares in one direction and 1 square in the other
                if abs(move[0]) + abs(move[1]) == 3:
                    if destination_piece == ' ' or (destination_piece.isupper() != self.chess_var.current_player == 1):
                        possible_moves.append((new_col, new_row))

        return possible_moves


def print_board(chess_var):
    """
    Helper function to print the chess board.
    """
    chess_var.display_board()


# Main game loop
def play_chess_game():
    game = ChessVar()

    print("Initial Board:")
    print_board(game)

    # Example moves
    moves = ['e2e4']
    for move in moves:
        move_result = game.make_move(move)
        print_board(game)

    # Get the game state
    game_state = game.get_game_state()
    print(f"Game State: {game_state}")

# Run the chess game
if __name__ == "__main__":
    play_chess_game()
