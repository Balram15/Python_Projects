import random
import time
import threading
import sys
from collections import deque

class SnakeGame:
    """
    Classic Snake Game with real-time movement.
    Snake grows when eating food, game ends on collision.
    """
    
    def __init__(self, game_suite):
        self.game_suite = game_suite
        self.width = 20
        self.height = 10
        self.snake = deque([(self.height//2, self.width//2)])  # Start in center
        self.direction = (0, 1)  # Start moving right
        self.food = None
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.3  # Seconds between moves
        self.level = 1
        
        # Game input handling
        self.input_buffer = []
        self.input_lock = threading.Lock()
        
        # Directions mapping
        self.directions = {
            'w': (-1, 0),  # Up
            's': (1, 0),   # Down
            'a': (0, -1),  # Left
            'd': (0, 1),   # Right
        }
    
    def display_game_header(self):
        """Display game header and controls"""
        print("\n" + "="*60)
        print("                  🐍 SNAKE GAME 🐍")
        print("="*60)
        print("🎯 Goal: Eat food (🍎) to grow and score points!")
        print("🎮 Controls: W=Up, S=Down, A=Left, D=Right")
        print("⏸️  Press P to pause, Q to quit")
        print("⚡ Snake speeds up as you grow!")
        print("="*60)
    
    def reset_game(self):
        """Reset game state for new game"""
        self.snake = deque([(self.height//2, self.width//2)])
        self.direction = (0, 1)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.3
        self.level = 1
        self.generate_food()
    
    def generate_food(self):
        """Generate food at random position not occupied by snake"""
        while True:
            food_pos = (random.randint(0, self.height-1), 
                       random.randint(0, self.width-1))
            if food_pos not in self.snake:
                self.food = food_pos
                break
    
    def display_board(self):
        """Display the current game state"""
        # Clear screen (simplified version)
        print("\n" * 2)
        
        # Create board
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place snake
        for i, (row, col) in enumerate(self.snake):
            if i == 0:  # Head
                board[row][col] = '🐍'
            else:  # Body
                board[row][col] = '█'
        
        # Place food
        if self.food:
            board[self.food[0]][self.food[1]] = '🍎'
        
        # Print board with border
        print("┌" + "─" * (self.width * 2) + "┐")
        for row in board:
            print("│" + "".join(f"{cell} " for cell in row) + "│")
        print("└" + "─" * (self.width * 2) + "┘")
        
        # Print game info
        print(f"🏆 Score: {self.score} | 📏 Length: {len(self.snake)} | 🚀 Level: {self.level}")
        print(f"🎮 Controls: WASD to move, P to pause, Q to quit")
        
        if self.paused:
            print("⏸️  GAME PAUSED - Press P to continue")
    
    def get_input_async(self):
        """Get user input in a non-blocking way"""
        try:
            # Simple input system (works on most terminals)
            print("Enter command (W/A/S/D/P/Q): ", end="", flush=True)
            
            # For this simplified version, we'll use blocking input
            # In a real game, you'd use keyboard libraries like 'keyboard' or 'getch'
            user_input = input().strip().lower()
            
            with self.input_lock:
                if user_input:
                    self.input_buffer.append(user_input)
        except:
            pass
    
    def process_input(self):
        """Process user input"""
        with self.input_lock:
            while self.input_buffer:
                key = self.input_buffer.pop(0)
                
                if key == 'q':
                    self.game_over = True
                    return
                elif key == 'p':
                    self.paused = not self.paused
                    print("⏸️  Game paused" if self.paused else "▶️  Game resumed")
                    return
                elif key in self.directions:
                    new_direction = self.directions[key]
                    # Prevent reversing into itself
                    if (new_direction[0] + self.direction[0] != 0 or 
                        new_direction[1] + self.direction[1] != 0):
                        self.direction = new_direction
    
    def move_snake(self):
        """Move snake in current direction"""
        if self.paused or self.game_over:
            return
        
        # Calculate new head position
        head_row, head_col = self.snake[0]
        new_head = (head_row + self.direction[0], 
                   head_col + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.height or 
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10 * self.level
            self.generate_food()
            
            # Increase speed/level every 5 food items
            if len(self.snake) % 5 == 0:
                self.level += 1
                self.speed = max(0.1, self.speed - 0.02)  # Faster, min 0.1 seconds
            
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def calculate_final_score(self):
        """Calculate final score with bonuses"""
        base_score = self.score
        length_bonus = len(self.snake) * 5
        level_bonus = self.level * 50
        
        total_score = base_score + length_bonus + level_bonus
        return total_score
    
    def play_turn_based_version(self):
        """
        Turn-based version of Snake (easier to implement in console)
        Player enters move each turn instead of real-time
        """
        print("\n🎮 Playing turn-based Snake!")
        print("💡 Enter your move each turn (W/A/S/D)")
        
        self.display_board()
        
        while not self.game_over:
            try:
                # Get player input
                self.get_input_async()
                self.process_input()
                
                if self.game_over:
                    break
                
                if not self.paused:
                    # Move snake
                    self.move_snake()
                    
                    # Display updated board
                    self.display_board()
                    
                    # Small delay for better experience
                    time.sleep(0.1)
            
            except KeyboardInterrupt:
                print("\n❌ Game cancelled.")
                return False
        
        return True
    
    def play_auto_version(self):
        """
        Auto-moving version - snake moves automatically
        Player can change direction during movement
        """
        print("\n🎮 Playing auto-moving Snake!")
        print("💡 Snake moves automatically. Enter direction to change course.")
        print("⚡ Game speed increases as you grow!")
        
        move_count = 0
        last_move_time = time.time()
        
        while not self.game_over:
            current_time = time.time()
            
            try:
                # Check for input periodically
                if move_count % 3 == 0:  # Every 3rd iteration
                    print("\nDirection (W/A/S/D) or P=pause, Q=quit: ", end="")
                    # Use a timeout for input (simplified)
                    self.get_input_async()
                
                self.process_input()
                
                if self.game_over:
                    break
                
                # Move snake based on speed
                if current_time - last_move_time >= self.speed and not self.paused:
                    self.move_snake()
                    self.display_board()
                    last_move_time = current_time
                    move_count += 1
                
                time.sleep(0.05)  # Small delay to prevent CPU spinning
            
            except KeyboardInterrupt:
                print("\n❌ Game cancelled.")
                return False
        
        return True
    
    def select_game_mode(self):
        """Let player choose game mode"""
        print("\n🎮 SELECT GAME MODE:")
        print("1. Turn-based - Enter move each turn (Recommended)")
        print("2. Auto-moving - Snake moves automatically (Advanced)")
        
        while True:
            choice = input("\nChoose mode (1-2): ").strip()
            if choice == '1':
                return 'turn_based'
            elif choice == '2':
                return 'auto'
            else:
                print("❌ Invalid choice. Please select 1 or 2.")
    
    def play_game(self):
        """Main game loop"""
        self.display_game_header()
        
        while True:
            # Reset for new game
            self.reset_game()
            
            # Select game mode
            mode = self.select_game_mode()
            
            # Play the game
            if mode == 'turn_based':
                completed = self.play_turn_based_version()
            else:
                completed = self.play_auto_version()
            
            if not completed:
                break
            
            # Game over - show results
            print(f"\n💀 GAME OVER!")
            print(f"🏆 Final Score: {self.score}")
            print(f"📏 Snake Length: {len(self.snake)}")
            print(f"🚀 Level Reached: {self.level}")
            
            # Calculate and record final score
            final_score = self.calculate_final_score()
            print(f"⭐ Total Score (with bonuses): {final_score}")
            self.game_suite.record_game_score("Snake Game", final_score)
            
            # Play again?
            while True:
                play_again = input("\n🔄 Play again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("👋 Thanks for playing Snake!")
                    return
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
    
    def get_game_stats(self):
        """Get statistics for this game"""
        if not self.game_suite.current_player:
            return "No player logged in"
        
        player = self.game_suite.current_player
        high_score = player.high_scores.get("Snake Game", 0)
        return f"High Score: {high_score}"

# Integration with main game suite
def integrate_snake(game_suite):
    """Integrate Snake game with the main suite"""
    
    def run_snake():
        if not game_suite.current_player:
            print("❌ Please login first (Menu option 5)")
            return
        
        game = SnakeGame(game_suite)
        game.play_game()
    
    # Update the games dictionary in game_suite
    game_suite.games['3']['class'] = run_snake

# Example usage for testing
if __name__ == "__main__":
    # For standalone testing
    class MockGameSuite:
        def __init__(self):
            self.current_player = type('Player', (), {'name': 'Test Player'})()
        
        def record_game_score(self, game_name, score):
            print(f"Score recorded: {score} for {game_name}")
    
    mock_suite = MockGameSuite()
    game = SnakeGame(mock_suite)
    game.play_game()