import random
import time

class TicTacToe:
    """
    Tic-Tac-Toe game with AI opponent using Minimax algorithm.
    Features multiple difficulty levels and smart scoring.
    """
    
    def __init__(self, game_suite):
        self.game_suite = game_suite
        self.board = [' ' for _ in range(9)]  # 3x3 board as 1D array
        self.human_player = 'X'
        self.ai_player = 'O'
        self.current_player = 'X'
        self.game_mode = None
        self.difficulty = None
        
        # Difficulty settings
        self.difficulties = {
            '1': {'name': 'Easy', 'smart_moves': 0.3, 'score_multiplier': 1},
            '2': {'name': 'Medium', 'smart_moves': 0.7, 'score_multiplier': 2},
            '3': {'name': 'Hard', 'smart_moves': 1.0, 'score_multiplier': 3}
        }
    
    def display_game_header(self):
        """Display game header and rules"""
        print("\n" + "="*50)
        print("               ❌ TIC-TAC-TOE ⭕")
        print("="*50)
        print("🎯 Goal: Get 3 in a row (horizontal, vertical, or diagonal)")
        print("👤 You are X, AI is O")
        print("📍 Enter position 1-9 to place your mark")
        print("="*50)
    
    def display_board(self):
        """Display the current board state"""
        print("\n📋 Current Board:")
        print("   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   ")
        
        print("\n📍 Position Reference:")
        print("   |   |   ")
        print(" 1 | 2 | 3 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 4 | 5 | 6 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 7 | 8 | 9 ")
        print("   |   |   ")
    
    def reset_board(self):
        """Reset the board for a new game"""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
    
    def is_winner(self, board, player):
        """Check if the given player has won"""
        # Define winning combinations (indices)
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in win_combinations:
            if all(board[i] == player for i in combo):
                return True
        return False
    
    def is_board_full(self, board):
        """Check if the board is full (tie game)"""
        return ' ' not in board
    
    def get_available_moves(self, board):
        """Get list of available moves (empty positions)"""
        return [i for i, cell in enumerate(board) if cell == ' ']
    
    def make_move(self, board, position, player):
        """Make a move on the board"""
        if board[position] == ' ':
            board[position] = player
            return True
        return False
    
    def evaluate_board(self, board):
        """Evaluate board state for minimax algorithm"""
        if self.is_winner(board, self.ai_player):
            return 10
        elif self.is_winner(board, self.human_player):
            return -10
        else:
            return 0
    
    def minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm for optimal AI moves.
        Returns the best score for the current position.
        """
        score = self.evaluate_board(board)
        
        # Base cases
        if score == 10 or score == -10:
            return score
        
        if self.is_board_full(board):
            return 0
        
        if is_maximizing:
            # AI's turn - maximize score
            best_score = -1000
            for move in self.get_available_moves(board):
                # Make the move
                board[move] = self.ai_player
                # Recursively get the score
                score = self.minimax(board, depth + 1, False)
                # Undo the move
                board[move] = ' '
                # Update best score
                best_score = max(score, best_score)
            return best_score
        else:
            # Human's turn - minimize score
            best_score = 1000
            for move in self.get_available_moves(board):
                # Make the move
                board[move] = self.human_player
                # Recursively get the score
                score = self.minimax(board, depth + 1, True)
                # Undo the move
                board[move] = ' '
                # Update best score
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self, board):
        """Get the best move for AI using minimax"""
        best_score = -1000
        best_move = -1
        
        for move in self.get_available_moves(board):
            # Make the move
            board[move] = self.ai_player
            # Calculate score for this move
            score = self.minimax(board, 0, False)
            # Undo the move
            board[move] = ' '
            
            # Update best move if this is better
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_random_move(self, board):
        """Get a random available move"""
        available_moves = self.get_available_moves(board)
        return random.choice(available_moves) if available_moves else -1
    
    def get_ai_move(self, board):
        """Get AI move based on difficulty level"""
        if not self.difficulty:
            return self.get_best_move(board)
        
        smart_move_chance = self.difficulty['smart_moves']
        
        if random.random() < smart_move_chance:
            # Make smart move
            return self.get_best_move(board)
        else:
            # Make random move
            return self.get_random_move(board)
    
    def get_human_move(self):
        """Get human player's move with validation"""
        while True:
            try:
                move = input(f"\n{self.human_player}'s turn - Enter position (1-9): ").strip()
                
                if not move.isdigit():
                    print("❌ Please enter a number between 1-9.")
                    continue
                
                move_num = int(move)
                
                if move_num < 1 or move_num > 9:
                    print("❌ Please enter a number between 1-9.")
                    continue
                
                # Convert to 0-based index
                position = move_num - 1
                
                if self.board[position] != ' ':
                    print("❌ Position already taken. Choose another.")
                    continue
                
                return position
            
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def select_difficulty(self):
        """Let player choose AI difficulty"""
        print("\n🤖 SELECT AI DIFFICULTY:")
        for key, diff in self.difficulties.items():
            print(f"{key}. {diff['name']} - Smart moves: {int(diff['smart_moves']*100)}%")
        
        while True:
            choice = input("\nChoose difficulty (1-3): ").strip()
            if choice in self.difficulties:
                return self.difficulties[choice]
            print("❌ Invalid choice. Please select 1-3.")
    
    def calculate_score(self, result, moves_taken, difficulty_multiplier):
        """Calculate score based on game result"""
        base_scores = {
            'win': 1000,
            'tie': 500,
            'lose': 100
        }
        
        base_score = base_scores[result]
        
        # Bonus for fewer moves (faster win)
        if result == 'win':
            move_bonus = max(0, (9 - moves_taken) * 50)
        else:
            move_bonus = 0
        
        # Difficulty multiplier
        difficulty_bonus = difficulty_multiplier * 200
        
        total_score = base_score + move_bonus + difficulty_bonus
        return total_score
    
    def play_round(self):
        """Play one round of Tic-Tac-Toe"""
        self.reset_board()
        moves_taken = 0
        start_time = time.time()
        
        print(f"\n🎮 Starting new game! You are {self.human_player}")
        
        while True:
            self.display_board()
            
            try:
                if self.current_player == self.human_player:
                    # Human's turn
                    position = self.get_human_move()
                    self.make_move(self.board, position, self.human_player)
                    moves_taken += 1
                    
                else:
                    # AI's turn
                    print(f"\n🤖 AI ({self.ai_player}) is thinking...")
                    time.sleep(0.5)  # Dramatic pause
                    
                    position = self.get_ai_move(self.board)
                    if position != -1:
                        self.make_move(self.board, position, self.ai_player)
                        print(f"🤖 AI chose position {position + 1}")
                
                # Check for winner
                if self.is_winner(self.board, self.human_player):
                    self.display_board()
                    end_time = time.time()
                    time_taken = round(end_time - start_time, 1)
                    
                    print(f"\n🎉 CONGRATULATIONS! You won!")
                    print(f"⏱️ Time: {time_taken} seconds")
                    print(f"🎯 Moves: {moves_taken}")
                    
                    score = self.calculate_score('win', moves_taken, self.difficulty['score_multiplier'])
                    print(f"⭐ Your score: {score}")
                    self.game_suite.record_game_score("Tic-Tac-Toe", score)
                    return 'win'
                
                elif self.is_winner(self.board, self.ai_player):
                    self.display_board()
                    print(f"\n🤖 AI wins! Better luck next time!")
                    
                    score = self.calculate_score('lose', moves_taken, self.difficulty['score_multiplier'])
                    print(f"⭐ Your score: {score}")
                    self.game_suite.record_game_score("Tic-Tac-Toe", score)
                    return 'lose'
                
                elif self.is_board_full(self.board):
                    self.display_board()
                    print(f"\n🤝 It's a tie! Good game!")
                    
                    score = self.calculate_score('tie', moves_taken, self.difficulty['score_multiplier'])
                    print(f"⭐ Your score: {score}")
                    self.game_suite.record_game_score("Tic-Tac-Toe", score)
                    return 'tie'
                
                # Switch players
                self.current_player = self.ai_player if self.current_player == self.human_player else self.human_player
            
            except KeyboardInterrupt:
                print("\n❌ Game cancelled.")
                return 'cancelled'
    
    def play_game(self):
        """Main game loop"""
        self.display_game_header()
        
        # Select difficulty
        self.difficulty = self.select_difficulty()
        print(f"\n🤖 AI difficulty set to: {self.difficulty['name']}")
        
        wins = 0
        losses = 0
        ties = 0
        
        while True:
            # Play a round
            result = self.play_round()
            
            if result == 'cancelled':
                break
            elif result == 'win':
                wins += 1
                print("🏆 Victory!")
            elif result == 'lose':
                losses += 1
                print("😞 Defeat!")
            elif result == 'tie':
                ties += 1
                print("🤝 Draw!")
            
            # Show session stats
            print(f"\n📊 Session Stats: Wins: {wins}, Losses: {losses}, Ties: {ties}")
            
            # Ask to play again
            while True:
                play_again = input("\n🔄 Play again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print(f"👋 Thanks for playing Tic-Tac-Toe!")
                    print(f"🎯 Final Session: {wins} wins, {losses} losses, {ties} ties")
                    return
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
    
    def get_game_stats(self):
        """Get statistics for this game"""
        if not self.game_suite.current_player:
            return "No player logged in"
        
        player = self.game_suite.current_player
        high_score = player.high_scores.get("Tic-Tac-Toe", 0)
        return f"High Score: {high_score}"

# Integration with main game suite
def integrate_tictactoe(game_suite):
    """Integrate Tic-Tac-Toe with the main suite"""
    
    def run_tictactoe():
        if not game_suite.current_player:
            print("❌ Please login first (Menu option 5)")
            return
        
        game = TicTacToe(game_suite)
        game.play_game()
    
    # Update the games dictionary in game_suite
    game_suite.games['2']['class'] = run_tictactoe

# Example usage for testing
if __name__ == "__main__":
    # For standalone testing
    class MockGameSuite:
        def __init__(self):
            self.current_player = type('Player', (), {'name': 'Test Player'})()
        
        def record_game_score(self, game_name, score):
            print(f"Score recorded: {score} for {game_name}")
    
    mock_suite = MockGameSuite()
    game = TicTacToe(mock_suite)
    game.play_game()