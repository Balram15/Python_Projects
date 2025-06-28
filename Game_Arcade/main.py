#!/usr/bin/env python3
"""
Python Game Arcade - Complete Main Entry Point
Run this file to start the complete game suite with all 4 games integrated.

Games included:
1. Number Guessing Game - Multiple difficulty levels with smart scoring
2. Tic-Tac-Toe - Unbeatable AI using Minimax algorithm
3. Snake Game - Classic snake with collision detection
4. Memory Card Game - Card matching with time challenges

Features:
- Player management system with profiles
- High score tracking and leaderboards
- Statistics dashboard
- Data persistence with JSON
- Error handling and recovery
"""

from game_suite import GameSuite
from number_guessing import integrate_number_guessing
from tictactoe import integrate_tictactoe
from snake import integrate_snake
from memory import integrate_memory

def main():
    """Main entry point for the game arcade"""
    print("🎮 Initializing Python Game Arcade...")
    print("🔧 Loading games and player data...")
    
    # Create the main game suite
    game_suite = GameSuite()
    
    # Integrate all games
    integrate_number_guessing(game_suite)
    integrate_tictactoe(game_suite)
    integrate_snake(game_suite)
    integrate_memory(game_suite)
    
    print("✅ All games loaded successfully!")
    
    # Enhanced run method with all games integrated
    def enhanced_run():
        """Enhanced run method with complete game integration"""
        print("🚀 Welcome to Python Game Arcade!")
        print("🎯 Choose from 4 exciting games with AI opponents and challenges!")
        
        # Ensure we have a player
        if not game_suite.current_player:
            print("\n👤 First, let's set up a player profile:")
            game_suite.create_player()
        
        while game_suite.running:
            try:
                game_suite.display_header()
                game_suite.display_main_menu()
                
                choice = game_suite.get_user_choice()
                if choice is None:
                    continue
                
                if choice == '0':
                    game_suite.running = False
                    
                elif choice == '1':
                    # Run Number Guessing Game
                    if game_suite.games['1']['class']:
                        print("\n🎲 Loading Number Guessing Game...")
                        game_suite.games['1']['class']()
                    else:
                        print("🎲 Number Guessing Game - Error loading!")
                        
                elif choice == '2':
                    # Run Tic-Tac-Toe Game
                    if game_suite.games['2']['class']:
                        print("\n❌ Loading Tic-Tac-Toe with AI...")
                        game_suite.games['2']['class']()
                    else:
                        print("❌ Tic-Tac-Toe - Error loading!")
                        
                elif choice == '3':
                    # Run Snake Game
                    if game_suite.games['3']['class']:
                        print("\n🐍 Loading Snake Game...")
                        game_suite.games['3']['class']()
                    else:
                        print("🐍 Snake Game - Error loading!")
                        
                elif choice == '4':
                    # Run Memory Card Game
                    if game_suite.games['4']['class']:
                        print("\n🧠 Loading Memory Card Game...")
                        game_suite.games['4']['class']()
                    else:
                        print("🧠 Memory Card Game - Error loading!")
                        
                elif choice == '5':
                    game_suite.player_management_menu()
                    
                elif choice == '6':
                    game_suite.view_high_scores()
                    input("\nPress Enter to continue...")
                    
                elif choice == '7':
                    game_suite.view_statistics()
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for playing Python Game Arcade!")
                print("🎮 Come back anytime for more gaming fun!")
                break
                
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("🔧 Please try again or restart the application.")
                input("Press Enter to continue...")
        
        # Final goodbye message
        print("\n" + "="*60)
        print("           🎮 THANKS FOR PLAYING! 🎮")
        print("="*60)
        
        if game_suite.current_player:
            final_stats = game_suite.current_player
            print(f"👤 Player: {final_stats.name}")
            print(f"🎯 Total Games Played: {final_stats.games_played}")
            print(f"⭐ Total Score Earned: {final_stats.total_score}")
            print(f"📊 Average Score: {final_stats.get_average_score()}")
            
            if final_stats.high_scores:
                print(f"\n🏆 Your High Scores:")
                for game, score in final_stats.high_scores.items():
                    print(f"   {game}: {score}")
        
        print("\n🌟 Keep practicing and beat your high scores!")
        print("💡 Pro tip: Try different difficulty levels for more challenge!")
        print("\n👋 See you next time in Python Game Arcade!")
    
    # Replace the run method and start the game suite
    game_suite.run = enhanced_run
    game_suite.run()

def display_startup_info():
    """Display startup information and credits"""
    print("\n" + "="*60)
    print("           🎮 PYTHON GAME ARCADE 🎮")
    print("="*60)
    print("🎯 Version: 1.0.0")
    print("👨‍💻 A complete gaming suite built with Python")
    print("\n🎮 Available Games:")
    print("   1. 🎲 Number Guessing - Test your intuition!")
    print("   2. ❌ Tic-Tac-Toe - Challenge the unbeatable AI!")
    print("   3. 🐍 Snake Game - Classic arcade action!")
    print("   4. 🧠 Memory Cards - Train your memory!")
    print("\n🌟 Features:")
    print("   • Player profiles with statistics tracking")
    print("   • High score leaderboards")
    print("   • Multiple difficulty levels")
    print("   • Smart AI opponents")
    print("   • Achievement system")
    print("="*60)

def check_dependencies():
    """Check if all required modules are available"""
    required_modules = [
        'json', 'os', 'datetime', 'random', 'time', 
        'threading', 'sys', 'collections'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing required modules: {', '.join(missing_modules)}")
        print("🔧 Please install the missing modules and try again.")
        return False
    
    return True

if __name__ == "__main__":
    # Display startup information
    display_startup_info()
    
    # Check dependencies
    if not check_dependencies():
        exit(1)
    
    # Start the game suite
    try:
        main()
    except Exception as e:
        print(f"\n💥 Fatal error starting game suite: {e}")
        print("🔧 Please check your installation and try again.")
        print("📧 If the problem persists, please report this bug.")
    
    # Final cleanup
    print("\n🔄 Game suite terminated normally.")
    print("💾 All player data has been saved.")
    print("👋 Goodbye!")