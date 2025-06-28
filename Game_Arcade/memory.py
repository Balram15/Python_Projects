import random
import time

class MemoryCardGame:
    """
    Memory Card Matching Game with different grid sizes.
    Player flips cards to find matching pairs within time limit.
    """
    
    def __init__(self, game_suite):
        self.game_suite = game_suite
        self.grid = []
        self.revealed = []
        self.matched = []
        self.grid_size = 4  # 4x4 default
        self.total_pairs = 0
        self.attempts = 0
        self.matches_found = 0
        self.start_time = None
        
        # Card symbols for different difficulties
        self.card_symbols = [
            '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼',
            '🐨', '🐯', '🦁', '🐸', '🐵', '🐔', '🐧', '🐦',
            '🦆', '🦅', '🦉', '🐺', '🐗', '🐴', '🦄', '🐝',
            '🐛', '🦋', '🐌', '🐞', '🐜', '🕷️', '🦂', '🐢'
        ]
        
        # Difficulty levels
        self.difficulties = {
            '1': {'name': 'Easy', 'grid_size': 4, 'time_limit': 120, 'score_multiplier': 1},
            '2': {'name': 'Medium', 'grid_size': 6, 'time_limit': 180, 'score_multiplier': 2},
            '3': {'name': 'Hard', 'grid_size': 8, 'time_limit': 240, 'score_multiplier': 3}
        }
    
    def display_game_header(self):
        """Display game header and rules"""
        print("\n" + "="*60)
        print("              🧠 MEMORY CARD GAME 🧠")
        print("="*60)
        print("🎯 Goal: Find all matching pairs by flipping cards")
        print("🎮 Enter row,col coordinates (e.g., 1,2) to flip a card")
        print("⏰ Complete within time limit for bonus points!")
        print("🧠 Fewer attempts = higher score")
        print("="*60)
    
    def select_difficulty(self):
        """Let player choose difficulty level"""
        print("\n🎚️ SELECT DIFFICULTY:")
        for key, diff in self.difficulties.items():
            grid_size = diff['grid_size']
            total_cards = grid_size * grid_size
            pairs = total_cards // 2
            print(f"{key}. {diff['name']} - {grid_size}x{grid_size} grid, "
                  f"{pairs} pairs, {diff['time_limit']}s time limit")
        
        while True:
            choice = input("\nChoose difficulty (1-3): ").strip()
            if choice in self.difficulties:
                return self.difficulties[choice]
            print("❌ Invalid choice. Please select 1-3.")
    
    def create_grid(self, difficulty):
        """Create game grid with card pairs"""
        self.grid_size = difficulty['grid_size']
        total_cards = self.grid_size * self.grid_size
        self.total_pairs = total_cards // 2
        
        # Select random symbols for this game
        selected_symbols = random.sample(self.card_symbols, self.total_pairs)
        
        # Create pairs
        cards = selected_symbols * 2
        random.shuffle(cards)
        
        # Create 2D grid
        self.grid = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                card_index = i * self.grid_size + j
                row.append(cards[card_index])
            self.grid.append(row)
        
        # Initialize tracking arrays
        self.revealed = [[False for _ in range(self.grid_size)] 
                        for _ in range(self.grid_size)]
        self.matched = [[False for _ in range(self.grid_size)] 
                       for _ in range(self.grid_size)]
        
        self.attempts = 0
        self.matches_found = 0
    
    def display_grid(self, show_cards=None):
        """Display the current grid state"""
        print(f"\n🧠 Memory Grid ({self.grid_size}x{self.grid_size}):")
        
        # Print column headers
        print("   ", end="")
        for j in range(self.grid_size):
            print(f" {j+1:2}", end="")
        print()
        
        # Print rows
        for i in range(self.grid_size):
            print(f"{i+1:2} ", end="")
            for j in range(self.grid_size):
                if self.matched[i][j]:
                    # Matched cards stay revealed
                    print(f" {self.grid[i][j]} ", end="")
                elif self.revealed[i][j] or (show_cards and (i, j) in show_cards):
                    # Currently revealed cards
                    print(f" {self.grid[i][j]} ", end="")
                else:
                    # Hidden cards
                    print(" ❓ ", end="")
            print()
        
        # Game status
        time_elapsed = time.time() - self.start_time if self.start_time else 0
        print(f"\n📊 Pairs found: {self.matches_found}/{self.total_pairs} | "
              f"Attempts: {self.attempts} | Time: {int(time_elapsed)}s")
    
    def get_card_choice(self):
        """Get player's card choice with validation"""
        while True:
            try:
                choice = input(f"\nEnter card position (row,col) 1-{self.grid_size}: ").strip()
                
                if ',' not in choice:
                    print("❌ Please use format: row,col (e.g., 1,2)")
                    continue
                
                row_str, col_str = choice.split(',')
                row = int(row_str.strip()) - 1  # Convert to 0-based
                col = int(col_str.strip()) - 1
                
                if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
                    print(f"❌ Please enter numbers between 1 and {self.grid_size}")
                    continue
                
                if self.revealed[row][col] or self.matched[row][col]:
                    print("❌ Card already revealed or matched. Choose another.")
                    continue
                
                return row, col
            
            except ValueError:
                print("❌ Please enter valid numbers (e.g., 1,2)")
            except KeyboardInterrupt:
                raise KeyboardInterrupt
    
    def flip_card(self, row, col):
        """Flip a card and return its symbol"""
        self.revealed[row][col] = True
        return self.grid[row][col]
    
    def hide_card(self, row, col):
        """Hide a card again"""
        self.revealed[row][col] = False
    
    def mark_matched(self, pos1, pos2):
        """Mark two cards as matched"""
        row1, col1 = pos1
        row2, col2 = pos2
        self.matched[row1][col1] = True
        self.matched[row2][col2] = True
        self.matches_found += 1
    
    def calculate_score(self, difficulty, time_taken, attempts):
        """Calculate final score based on performance"""
        base_score = 1000 * difficulty['score_multiplier']
        
        # Time bonus (faster = better)
        time_limit = difficulty['time_limit']
        time_remaining = max(0, time_limit - time_taken)
        time_bonus = int(time_remaining * 5)
        
        # Efficiency bonus (fewer attempts = better)
        optimal_attempts = self.total_pairs + 2  # Theoretical minimum
        efficiency_bonus = max(0, (optimal_attempts * 2 - attempts) * 10)
        
        # Perfect game bonus
        perfect_bonus = 500 if attempts == optimal_attempts else 0
        
        total_score = base_score + time_bonus + efficiency_bonus + perfect_bonus
        return max(total_score, 100)  # Minimum score
    
    def show_score_breakdown(self, difficulty, time_taken, attempts, total_score):
        """Show detailed score breakdown"""
        print(f"\n📊 SCORE BREAKDOWN:")
        print(f"Base Score: {1000 * difficulty['score_multiplier']}")
        
        time_limit = difficulty['time_limit']
        time_remaining = max(0, time_limit - time_taken)
        time_bonus = int(time_remaining * 5)
        print(f"Time Bonus: {time_bonus} ({time_remaining:.1f}s remaining)")
        
        optimal_attempts = self.total_pairs + 2
        efficiency_bonus = max(0, (optimal_attempts * 2 - attempts) * 10)
        print(f"Efficiency Bonus: {efficiency_bonus} ({attempts} attempts)")
        
        perfect_bonus = 500 if attempts == optimal_attempts else 0
        if perfect_bonus > 0:
            print(f"Perfect Game Bonus: {perfect_bonus}")
        
        print(f"⭐ TOTAL SCORE: {total_score}")
    
    def play_round(self, difficulty):
        """Play one round of the memory game"""
        self.create_grid(difficulty)
        self.start_time = time.time()
        time_limit = difficulty['time_limit']
        
        print(f"\n🎮 Starting {difficulty['name']} difficulty!")
        print(f"⏰ You have {time_limit} seconds to find all {self.total_pairs} pairs")
        
        # Show grid briefly at start
        print("\n👀 Memorize the cards! (3 seconds)")
        all_positions = [(i, j) for i in range(self.grid_size) 
                        for j in range(self.grid_size)]
        self.display_grid(show_cards=all_positions)
        time.sleep(3)
        
        # Clear and start game
        print("\n" + "="*50)
        print("🎯 Game started! Find the matching pairs!")
        
        while self.matches_found < self.total_pairs:
            # Check time limit
            elapsed_time = time.time() - self.start_time
            if elapsed_time > time_limit:
                print(f"\n⏰ TIME'S UP! Game over after {time_limit} seconds")
                return False
            
            try:
                self.display_grid()
                
                # Get first card
                print(f"\n🎯 Turn {self.attempts + 1}")
                print("Choose first card:")
                row1, col1 = self.get_card_choice()
                card1 = self.flip_card(row1, col1)
                
                # Show first card
                self.display_grid()
                print(f"First card: {card1} at ({row1+1},{col1+1})")
                
                # Get second card
                print("Choose second card:")
                row2, col2 = self.get_card_choice()
                card2 = self.flip_card(row2, col2)
                
                # Show both cards
                self.display_grid()
                print(f"Second card: {card2} at ({row2+1},{col2+1})")
                
                self.attempts += 1
                
                # Check for match
                if card1 == card2:
                    print("🎉 MATCH! Great memory!")
                    self.mark_matched((row1, col1), (row2, col2))
                    time.sleep(1)
                else:
                    print("❌ No match. Try to remember where these cards are!")
                    time.sleep(2)
                    # Hide both cards
                    self.hide_card(row1, col1)
                    self.hide_card(row2, col2)
            
            except KeyboardInterrupt:
                print("\n❌ Game cancelled.")
                return False
        
        # Victory!
        end_time = time.time()
        time_taken = end_time - self.start_time
        
        print(f"\n🎉 CONGRATULATIONS! You found all pairs!")
        print(f"⏱️ Time taken: {time_taken:.1f} seconds")
        print(f"🎯 Total attempts: {self.attempts}")
        
        # Calculate and show score
        score = self.calculate_score(difficulty, time_taken, self.attempts)
        self.show_score_breakdown(difficulty, time_taken, self.attempts, score)
        
        # Record score
        self.game_suite.record_game_score("Memory Cards", score)
        
        return True
    
    def play_game(self):
        """Main game loop"""
        self.display_game_header()
        
        while True:
            # Select difficulty
            difficulty = self.select_difficulty()
            
            # Play the round
            completed = self.play_round(difficulty)
            
            if not completed:
                print("😞 Better luck next time!")
            
            # Ask to play again
            while True:
                play_again = input("\n🔄 Play again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("👋 Thanks for playing Memory Cards!")
                    return
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
    
    def get_game_stats(self):
        """Get statistics for this game"""
        if not self.game_suite.current_player:
            return "No player logged in"
        
        player = self.game_suite.current_player
        high_score = player.high_scores.get("Memory Cards", 0)
        return f"High Score: {high_score}"

# Integration with main game suite
def integrate_memory(game_suite):
    """Integrate Memory Card game with the main suite"""
    
    def run_memory():
        if not game_suite.current_player:
            print("❌ Please login first (Menu option 5)")
            return
        
        game = MemoryCardGame(game_suite)
        game.play_game()
    
    # Update the games dictionary in game_suite
    game_suite.games['4']['class'] = run_memory

# Example usage for testing
if __name__ == "__main__":
    # For standalone testing
    class MockGameSuite:
        def __init__(self):
            self.current_player = type('Player', (), {'name': 'Test Player'})()
        
        def record_game_score(self, game_name, score):
            print(f"Score recorded: {score} for {game_name}")
    
    mock_suite = MockGameSuite()
    game = MemoryCardGame(mock_suite)
    game.play_game()