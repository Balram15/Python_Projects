import json
import os
from datetime import datetime

class Player:
    """Represents a player with profile and statistics"""
    
    def __init__(self, name):
        self.name = name
        self.games_played = 0
        self.total_score = 0
        self.high_scores = {}  # game_name -> best_score
        self.achievements = []
        self.created_date = datetime.now().strftime("%Y-%m-%d")
    
    def add_score(self, game_name, score):
        """Add a new score for a specific game"""
        self.games_played += 1
        self.total_score += score
        
        # Update high score if this is better
        if game_name not in self.high_scores or score > self.high_scores[game_name]:
            self.high_scores[game_name] = score
            return True  # New high score!
        return False
    
    def get_average_score(self):
        """Calculate average score across all games"""
        if self.games_played == 0:
            return 0
        return round(self.total_score / self.games_played, 2)
    
    def to_dict(self):
        """Convert player to dictionary for saving"""
        return {
            'name': self.name,
            'games_played': self.games_played,
            'total_score': self.total_score,
            'high_scores': self.high_scores,
            'achievements': self.achievements,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create player from dictionary data"""
        player = cls(data['name'])
        player.games_played = data.get('games_played', 0)
        player.total_score = data.get('total_score', 0)
        player.high_scores = data.get('high_scores', {})
        player.achievements = data.get('achievements', [])
        player.created_date = data.get('created_date', datetime.now().strftime("%Y-%m-%d"))
        return player

class GameSuite:
    """Main game suite manager"""
    
    def __init__(self):
        self.current_player = None
        self.players_file = "players.json"
        self.players = self.load_players()
        self.running = True
        
        # Available games
        self.games = {
            '1': {'name': 'Number Guessing Game', 'class': None},
            '2': {'name': 'Tic-Tac-Toe', 'class': None},
            '3': {'name': 'Snake Game', 'class': None},
            '4': {'name': 'Memory Card Game', 'class': None}
        }
    
    def load_players(self):
        """Load player data from file"""
        if os.path.exists(self.players_file):
            try:
                with open(self.players_file, 'r') as f:
                    data = json.load(f)
                    return {name: Player.from_dict(player_data) 
                           for name, player_data in data.items()}
            except (json.JSONDecodeError, KeyError):
                print("Warning: Could not load player data. Starting fresh.")
                return {}
        return {}
    
    def save_players(self):
        """Save player data to file"""
        try:
            data = {name: player.to_dict() for name, player in self.players.items()}
            with open(self.players_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving player data: {e}")
            return False
    
    def display_header(self):
        """Display the main header"""
        print("\n" + "="*60)
        print("           🎮 PYTHON GAME ARCADE 🎮")
        print("="*60)
        if self.current_player:
            print(f"Player: {self.current_player.name}")
            print(f"Games Played: {self.current_player.games_played}")
            print(f"Average Score: {self.current_player.get_average_score()}")
        print("="*60)
    
    def display_main_menu(self):
        """Display the main menu options"""
        print("\n🎯 MAIN MENU:")
        print("1. 🎲 Number Guessing Game")
        print("2. ❌ Tic-Tac-Toe")
        print("3. 🐍 Snake Game")
        print("4. 🧠 Memory Card Game")
        print("5. 👤 Player Management")
        print("6. 🏆 High Scores")
        print("7. 📊 Statistics")
        print("0. ❌ Exit")
        print("-" * 40)
    
    def get_user_choice(self):
        """Get and validate user menu choice"""
        try:
            choice = input("Enter your choice (0-7): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6', '7']:
                return choice
            else:
                print("❌ Invalid choice. Please enter a number between 0-7.")
                return None
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return '0'
    
    def player_management_menu(self):
        """Handle player management"""
        while True:
            print("\n👤 PLAYER MANAGEMENT")
            print("-" * 20)
            print("1. Login/Switch Player")
            print("2. Create New Player")
            print("3. Delete Player")
            print("4. View All Players")
            print("0. Back to Main Menu")
            
            choice = input("Enter choice (0-4): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.login_player()
            elif choice == '2':
                self.create_player()
            elif choice == '3':
                self.delete_player()
            elif choice == '4':
                self.view_all_players()
            else:
                print("❌ Invalid choice.")
    
    def login_player(self):
        """Login or switch to a player"""
        if not self.players:
            print("📭 No players found. Create a player first.")
            return
        
        print("\nAvailable players:")
        for i, name in enumerate(self.players.keys(), 1):
            player = self.players[name]
            print(f"{i}. {name} (Games: {player.games_played}, Avg Score: {player.get_average_score()})")
        
        try:
            choice = int(input(f"\nSelect player (1-{len(self.players)}): "))
            if 1 <= choice <= len(self.players):
                player_name = list(self.players.keys())[choice - 1]
                self.current_player = self.players[player_name]
                print(f"✅ Logged in as {player_name}")
            else:
                print("❌ Invalid player selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def create_player(self):
        """Create a new player"""
        name = input("Enter player name: ").strip()
        if not name:
            print("❌ Player name cannot be empty.")
            return
        
        if name in self.players:
            print(f"❌ Player '{name}' already exists.")
            return
        
        player = Player(name)
        self.players[name] = player
        self.current_player = player
        self.save_players()
        print(f"✅ Created and logged in as {name}")
    
    def delete_player(self):
        """Delete a player"""
        if not self.players:
            print("📭 No players to delete.")
            return
        
        print("\nSelect player to delete:")
        for i, name in enumerate(self.players.keys(), 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input(f"Select player (1-{len(self.players)}): "))
            if 1 <= choice <= len(self.players):
                player_name = list(self.players.keys())[choice - 1]
                
                confirm = input(f"Are you sure you want to delete '{player_name}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    del self.players[player_name]
                    if self.current_player and self.current_player.name == player_name:
                        self.current_player = None
                    self.save_players()
                    print(f"✅ Deleted player '{player_name}'")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def view_all_players(self):
        """Display all players and their stats"""
        if not self.players:
            print("📭 No players found.")
            return
        
        print("\n📊 ALL PLAYERS")
        print("-" * 50)
        print(f"{'Name':<15} {'Games':<8} {'Total Score':<12} {'Avg Score':<10} {'Created'}")
        print("-" * 50)
        
        for player in self.players.values():
            print(f"{player.name:<15} {player.games_played:<8} {player.total_score:<12} "
                  f"{player.get_average_score():<10} {player.created_date}")
    
    def view_high_scores(self):
        """Display high scores for all games"""
        print("\n🏆 HIGH SCORES")
        print("-" * 30)
        
        if not self.players:
            print("📭 No scores recorded yet.")
            return
        
        # Collect all high scores by game
        game_scores = {}
        for player in self.players.values():
            for game_name, score in player.high_scores.items():
                if game_name not in game_scores:
                    game_scores[game_name] = []
                game_scores[game_name].append((player.name, score))
        
        # Display top scores for each game
        for game_name, scores in game_scores.items():
            print(f"\n🎮 {game_name}:")
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
            for i, (player_name, score) in enumerate(sorted_scores, 1):
                print(f"  {i}. {player_name}: {score}")
    
    def view_statistics(self):
        """Display overall statistics"""
        if not self.players:
            print("📭 No statistics available.")
            return
        
        print("\n📊 GAME SUITE STATISTICS")
        print("-" * 30)
        
        total_games = sum(player.games_played for player in self.players.values())
        total_players = len(self.players)
        
        if total_games > 0:
            avg_games_per_player = total_games / total_players
            total_score = sum(player.total_score for player in self.players.values())
            overall_avg_score = total_score / total_games
            
            print(f"Total Players: {total_players}")
            print(f"Total Games Played: {total_games}")
            print(f"Average Games per Player: {avg_games_per_player:.1f}")
            print(f"Overall Average Score: {overall_avg_score:.2f}")
            
            # Most active player
            most_active = max(self.players.values(), key=lambda p: p.games_played)
            print(f"Most Active Player: {most_active.name} ({most_active.games_played} games)")
            
            # Highest scoring player
            highest_scorer = max(self.players.values(), key=lambda p: p.get_average_score())
            print(f"Highest Average Score: {highest_scorer.name} ({highest_scorer.get_average_score():.2f})")
    
    def record_game_score(self, game_name, score):
        """Record a score for the current player"""
        if not self.current_player:
            print("❌ No player logged in. Score not recorded.")
            return False
        
        is_high_score = self.current_player.add_score(game_name, score)
        self.save_players()
        
        if is_high_score:
            print(f"🎉 NEW HIGH SCORE for {game_name}: {score}!")
        else:
            print(f"Score recorded: {score}")
        
        return is_high_score