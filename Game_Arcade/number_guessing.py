import random
import time

class NumberGuessingGame:
    """
    Number Guessing Game with multiple difficulty levels.
    Player tries to guess a random number with hints.
    """
    
    def __init__(self, game_suite):
        self.game_suite = game_suite
        self.difficulties = {
            '1': {'name': 'Easy', 'range': (1, 50), 'max_attempts': 10},
            '2': {'name': 'Medium', 'range': (1, 100), 'max_attempts': 8},
            '3': {'name': 'Hard', 'range': (1, 200), 'max_attempts': 6},
            '4': {'name': 'Expert', 'range': (1, 500), 'max_attempts': 5}
        }
    
    def display_game_header(self):
        """Display game header and rules"""
        print("\n" + "="*50)
        print("           🎲 NUMBER GUESSING GAME 🎲")
        print("="*50)
        print("🎯 Goal: Guess the secret number!")
        print("💡 You'll get hints: Higher or Lower")
        print("⭐ Score: Based on attempts remaining")
        print("="*50)
    
    def select_difficulty(self):
        """Let player choose difficulty level"""
        print("\n🎚️ SELECT DIFFICULTY:")
        for key, diff in self.difficulties.items():
            range_min, range_max = diff['range']
            print(f"{key}. {diff['name']} - Range: {range_min}-{range_max}, "
                  f"Max Attempts: {diff['max_attempts']}")
        
        while True:
            choice = input("\nChoose difficulty (1-4): ").strip()
            if choice in self.difficulties:
                return self.difficulties[choice]
            print("❌ Invalid choice. Please select 1-4.")
    
    def calculate_score(self, attempts_used, max_attempts, difficulty_multiplier):
        """Calculate score based on performance"""
        # Base score starts at 1000
        base_score = 1000
        
        # Bonus for fewer attempts
        attempts_remaining = max_attempts - attempts_used
        attempt_bonus = attempts_remaining * 100
        
        # Difficulty multiplier
        difficulty_bonus = difficulty_multiplier * 200
        
        # Total score
        total_score = base_score + attempt_bonus + difficulty_bonus
        return max(total_score, 100)  # Minimum score of 100
    
    def play_round(self, difficulty):
        """Play one round of the guessing game"""
        range_min, range_max = difficulty['range']
        max_attempts = difficulty['max_attempts']
        difficulty_multiplier = list(self.difficulties.values()).index(difficulty) + 1
        
        # Generate secret number
        secret_number = random.randint(range_min, range_max)
        attempts_used = 0
        start_time = time.time()
        
        print(f"\n🎯 I'm thinking of a number between {range_min} and {range_max}")
        print(f"🎫 You have {max_attempts} attempts")
        print("-" * 40)
        
        while attempts_used < max_attempts:
            try:
                # Get player's guess
                guess = input(f"\nAttempt {attempts_used + 1}/{max_attempts} - Enter your guess: ").strip()
                
                # Validate input
                if not guess.isdigit():
                    print("❌ Please enter a valid number.")
                    continue
                
                guess_num = int(guess)
                attempts_used += 1
                
                # Check if guess is in valid range
                if guess_num < range_min or guess_num > range_max:
                    print(f"❌ Please guess between {range_min} and {range_max}.")
                    continue
                
                # Check the guess
                if guess_num == secret_number:
                    # Winner!
                    end_time = time.time()
                    time_taken = round(end_time - start_time, 1)
                    
                    print(f"\n🎉 CONGRATULATIONS! You guessed it!")
                    print(f"✅ The number was {secret_number}")
                    print(f"⏱️ Time taken: {time_taken} seconds")
                    print(f"🎯 Attempts used: {attempts_used}/{max_attempts}")
                    
                    # Calculate and record score
                    score = self.calculate_score(attempts_used, max_attempts, difficulty_multiplier)
                    print(f"⭐ Your score: {score}")
                    
                    # Record the score
                    self.game_suite.record_game_score("Number Guessing", score)
                    
                    return True
                
                elif guess_num < secret_number:
                    remaining = max_attempts - attempts_used
                    if remaining > 0:
                        print(f"📈 Too low! Try higher. ({remaining} attempts left)")
                    
                else:  # guess_num > secret_number
                    remaining = max_attempts - attempts_used
                    if remaining > 0:
                        print(f"📉 Too high! Try lower. ({remaining} attempts left)")
                
            except KeyboardInterrupt:
                print("\n❌ Game cancelled.")
                return False
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Game over - no more attempts
        print(f"\n💥 GAME OVER!")
        print(f"🎯 The number was {secret_number}")
        print(f"😢 You used all {max_attempts} attempts")
        
        # Give consolation score
        consolation_score = 50 * difficulty_multiplier
        print(f"⭐ Consolation score: {consolation_score}")
        self.game_suite.record_game_score("Number Guessing", consolation_score)
        
        return False
    
    def play_game(self):
        """Main game loop"""
        self.display_game_header()
        
        while True:
            # Select difficulty
            difficulty = self.select_difficulty()
            print(f"\n🎚️ Selected: {difficulty['name']} difficulty")
            
            # Play the round
            won = self.play_round(difficulty)
            
            if won:
                print("\n🌟 Excellent guessing!")
            else:
                print("\n🎯 Better luck next time!")
            
            # Ask if player wants to play again
            while True:
                play_again = input("\n🔄 Play again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("👋 Thanks for playing Number Guessing!")
                    return
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
    
    def get_game_stats(self):
        """Get statistics for this game"""
        if not self.game_suite.current_player:
            return "No player logged in"
        
        player = self.game_suite.current_player
        high_score = player.high_scores.get("Number Guessing", 0)
        return f"High Score: {high_score}"

# Integration with main game suite
def integrate_number_guessing(game_suite):
    """Integrate the number guessing game with the main suite"""
    
    def run_number_guessing():
        if not game_suite.current_player:
            print("❌ Please login first (Menu option 5)")
            return
        
        game = NumberGuessingGame(game_suite)
        game.play_game()
    
    # Update the games dictionary in game_suite
    game_suite.games['1']['class'] = run_number_guessing

# Example usage for testing
if __name__ == "__main__":
    # For standalone testing
    class MockGameSuite:
        def __init__(self):
            self.current_player = type('Player', (), {'name': 'Test Player'})()
        
        def record_game_score(self, game_name, score):
            print(f"Score recorded: {score} for {game_name}")
    
    mock_suite = MockGameSuite()
    game = NumberGuessingGame(mock_suite)
    game.play_game()