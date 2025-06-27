#!/usr/bin/env python3
"""
Personal Expense Tracker - Command Line Interface
A user-friendly CLI for managing personal expenses with data visualization.
"""

import sys
from datetime import datetime, timedelta
from tracker import ExpenseTracker

class ExpenseTrackerCLI:
    """
    Command Line Interface for the Expense Tracker.
    Handles user interaction, input validation, and display formatting.
    """
    
    def __init__(self):
        """Initialize the CLI with a tracker instance."""
        self.tracker = ExpenseTracker()
        self.running = True
    
    def display_header(self):
        """Display a nice header for the application."""
        print("\n" + "="*60)
        print("           💰 PERSONAL EXPENSE TRACKER 💰")
        print("="*60)
        stats = self.tracker.get_statistics()
        print(f"Total Expenses: {stats['total_expenses']} | ")
        print(f"Total Amount: ${stats['total_amount']:.2f}")
        if stats['total_expenses'] > 0:
            print(f"Date Range: {stats['date_range']}")
        print("="*60)
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n📋 MAIN MENU:")
        print("1. ➕ Add Expense")
        print("2. 📖 View All Expenses")
        print("3. 🔍 View by Category")
        print("4. 📅 View by Date Range")
        print("5. ✏️  Edit Expense")
        print("6. 🗑️  Delete Expense")
        print("7. 📊 View Statistics")
        print("8. 📈 View Category Totals")
        print("9. 💾 Export to CSV")
        print("0. ❌ Exit")
        print("-" * 40)
    
    def get_user_choice(self):
        """
        Get and validate user menu choice.
        
        Returns:
            str: Valid menu choice or None for invalid input
        """
        try:
            choice = input("Enter your choice (0-9): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return choice
            else:
                print("❌ Invalid choice. Please enter a number between 0-9.")
                return None
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return '0'
    
    def add_expense_interactive(self):
        """Interactive expense addition with input validation."""
        print("\n➕ ADD NEW EXPENSE")
        print("-" * 20)
        
        try:
            # Get amount with validation
            while True:
                amount_str = input("💰 Enter amount ($): ").strip()
                if not amount_str:
                    print("❌ Amount cannot be empty.")
                    continue
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("❌ Amount must be positive.")
                        continue
                    break
                except ValueError:
                    print("❌ Please enter a valid number.")
            
            # Get category with suggestions
            print("\n💡 Suggested categories: food, transport, entertainment, shopping, utilities, healthcare, other")
            while True:
                category = input("🏷️  Enter category: ").strip()
                if category:
                    break
                print("❌ Category cannot be empty.")
            
            # Get description
            while True:
                description = input("📝 Enter description: ").strip()
                if description:
                    break
                print("❌ Description cannot be empty.")
            
            # Get date (optional)
            print(f"\n📅 Enter date (YYYY-MM-DD) or press Enter for today ({datetime.now().strftime('%Y-%m-%d')}):")
            date_str = input("Date: ").strip()
            
            if date_str:
                try:
                    # Validate date format
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    print("⚠️  Invalid date format. Using today's date.")
                    date_str = None
            
            # Add the expense
            success, message, expense_id = self.tracker.add_expense(amount, category, description, date_str)
            
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")
        
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled.")
    
    def view_all_expenses(self):
        """Display all expenses in a formatted table."""
        print("\n📖 ALL EXPENSES")
        print("-" * 20)
        
        expenses = self.tracker.get_all_expenses()
        
        if not expenses:
            print("📭 No expenses found. Add some expenses first!")
            return
        
        # Display in table format
        print(f"{'ID':<10} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("-" * 70)
        
        for expense in expenses:
            print(f"{expense.id:<10} {expense.date:<12} {expense.category.title():<15} "
                  f"${expense.amount:<9.2f} {expense.description}")
        
        print(f"\n📊 Total: {len(expenses)} expenses, ${sum(exp.amount for exp in expenses):.2f}")
    
    def view_by_category(self):
        """View expenses filtered by category."""
        print("\n🔍 VIEW BY CATEGORY")
        print("-" * 20)
        
        # Show available categories
        category_totals = self.tracker.get_category_totals()
        if not category_totals:
            print("📭 No expenses found.")
            return
        
        print("Available categories:")
        for i, (category, total) in enumerate(category_totals.items(), 1):
            print(f"{i}. {category.title()} (${total:.2f})")
        
        category = input("\nEnter category name: ").strip().lower()
        if not category:
            print("❌ Category cannot be empty.")
            return
        
        expenses = self.tracker.get_expenses_by_category(category)
        
        if not expenses:
            print(f"📭 No expenses found for category '{category}'.")
            return
        
        print(f"\n💰 Expenses in category '{category.title()}':")
        print(f"{'ID':<10} {'Date':<12} {'Amount':<10} {'Description'}")
        print("-" * 50)
        
        total = 0
        for expense in sorted(expenses, key=lambda x: x.date, reverse=True):
            print(f"{expense.id:<10} {expense.date:<12} ${expense.amount:<9.2f} {expense.description}")
            total += expense.amount
        
        print(f"\n📊 Total in {category.title()}: ${total:.2f}")
    
    def view_by_date_range(self):
        """View expenses within a date range."""
        print("\n📅 VIEW BY DATE RANGE")
        print("-" * 20)
        
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            if not start_date:
                print("❌ Start date cannot be empty.")
                return
            
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            if not end_date:
                print("❌ End date cannot be empty.")
                return
            
            # Validate dates
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD.")
                return
            
            expenses = self.tracker.get_expenses_by_date_range(start_date, end_date)
            
            if not expenses:
                print(f"📭 No expenses found between {start_date} and {end_date}.")
                return
            
            print(f"\n💰 Expenses from {start_date} to {end_date}:")
            print(f"{'ID':<10} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
            print("-" * 70)
            
            total = 0
            for expense in expenses:
                print(f"{expense.id:<10} {expense.date:<12} {expense.category.title():<15} "
                      f"${expense.amount:<9.2f} {expense.description}")
                total += expense.amount
            
            print(f"\n📊 Total: {len(expenses)} expenses, ${total:.2f}")
        
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled.")
    
    def edit_expense(self):
        """Edit an existing expense."""
        print("\n✏️  EDIT EXPENSE")
        print("-" * 15)
        
        # Show recent expenses for reference
        recent = self.tracker.get_recent_expenses(7)
        if recent:
            print("\nRecent expenses:")
            for exp in recent[:5]:  # Show only first 5
                print(f"  {exp.id}: {exp}")
        
        expense_id = input("\nEnter expense ID to edit: ").strip()
        if not expense_id:
            print("❌ Expense ID cannot be empty.")
            return
        
        # Find the expense
        expense = self.tracker.get_expense_by_id(expense_id)
        if not expense:
            print(f"❌ No expense found with ID '{expense_id}'.")
            return
        
        print(f"\nCurrent expense: {expense}")
        print("\nEnter new values (press Enter to keep current value):")
        
        # Get new values
        amount_str = input(f"Amount (${expense.amount:.2f}): ").strip()
        new_amount = None
        if amount_str:
            try:
                new_amount = float(amount_str)
                if new_amount <= 0:
                    print("❌ Amount must be positive. Keeping current value.")
                    new_amount = None
            except ValueError:
                print("❌ Invalid amount. Keeping current value.")
                new_amount = None
        
        new_category = input(f"Category ({expense.category}): ").strip() or None
        new_description = input(f"Description ({expense.description}): ").strip() or None
        
        date_str = input(f"Date ({expense.date}): ").strip()
        new_date = None
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                new_date = date_str
            except ValueError:
                print("❌ Invalid date format. Keeping current value.")
        
        # Update the expense
        success, message = self.tracker.update_expense(
            expense_id, new_amount, new_category, new_description, new_date
        )
        
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n❌ {message}")
    
    def delete_expense(self):
        """Delete an expense interactively."""
        print("\n🗑️  DELETE EXPENSE")
        print("-" * 17)
        
        # Show recent expenses for reference
        recent = self.tracker.get_recent_expenses(7)
        if recent:
            print("\nRecent expenses:")
            for exp in recent[:5]:
                print(f"  {exp.id}: {exp}")
        
        expense_id = input("\nEnter expense ID to delete: ").strip()
        if not expense_id:
            print("❌ Expense ID cannot be empty.")
            return
        
        # Find and show the expense
        expense = self.tracker.get_expense_by_id(expense_id)
        if not expense:
            print(f"❌ No expense found with ID '{expense_id}'.")
            return
        
        print(f"\nExpense to delete: {expense}")
        confirm = input("Are you sure? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            success, message = self.tracker.delete_expense(expense_id)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")
        else:
            print("❌ Deletion cancelled.")
    
    def view_statistics(self):
        """Display comprehensive statistics."""
        print("\n📊 EXPENSE STATISTICS")
        print("-" * 22)
        
        stats = self.tracker.get_statistics()
        
        if stats['total_expenses'] == 0:
            print("📭 No expenses to analyze.")
            return
        
        print(f"📈 Total Expenses: {stats['total_expenses']}")
        print(f"💰 Total Amount: ${stats['total_amount']:.2f}")
        print(f"📊 Average Expense: ${stats['average_expense']:.2f}")
        print(f"⬆️  Highest Expense: ${stats['max_expense']:.2f}")
        print(f"⬇️  Lowest Expense: ${stats['min_expense']:.2f}")
        print(f"🏷️  Categories: {stats['categories']}")
        print(f"📅 Date Range: {stats['date_range']}")
        
        # Monthly breakdown
        current_month_total = self.tracker.get_monthly_total()
        print(f"\n📅 This Month: ${current_month_total:.2f}")
        
        # Recent activity
        recent = self.tracker.get_recent_expenses(7)
        recent_total = sum(exp.amount for exp in recent)
        print(f"📅 Last 7 Days: ${recent_total:.2f} ({len(recent)} expenses)")
    
    def view_category_totals(self):
        """Display spending by category."""
        print("\n📈 SPENDING BY CATEGORY")
        print("-" * 25)
        
        totals = self.tracker.get_category_totals()
        
        if not totals:
            print("📭 No expenses to analyze.")
            return
        
        total_spending = sum(totals.values())
        
        print(f"{'Category':<15} {'Amount':<12} {'Percentage'}")
        print("-" * 40)
        
        for category, amount in totals.items():
            percentage = (amount / total_spending) * 100
            print(f"{category.title():<15} ${amount:<11.2f} {percentage:.1f}%")
        
        print("-" * 40)
        print(f"{'TOTAL':<15} ${total_spending:<11.2f} 100.0%")
    
    def export_to_csv(self):
        """Export expenses to CSV file."""
        print("\n💾 EXPORT TO CSV")
        print("-" * 16)
        
        expenses = self.tracker.get_all_expenses()
        if not expenses:
            print("📭 No expenses to export.")
            return
        
        filename = input("Enter filename (or press Enter for 'expenses.csv'): ").strip()
        if not filename:
            filename = "expenses.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            import csv
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Date', 'Category', 'Amount', 'Description', 'Created At'])
                
                for expense in expenses:
                    writer.writerow([
                        expense.id,
                        expense.date,
                        expense.category,
                        expense.amount,
                        expense.description,
                        expense.created_at
                    ])
            
            print(f"✅ Exported {len(expenses)} expenses to '{filename}'")
        
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def run(self):
        """Main application loop."""
        print("🚀 Starting Personal Expense Tracker...")
        
        while self.running:
            try:
                self.display_header()
                self.display_menu()
                
                choice = self.get_user_choice()
                if choice is None:
                    continue
                
                # Handle menu choices
                if choice == '0':
                    self.running = False
                elif choice == '1':
                    self.add_expense_interactive()
                elif choice == '2':
                    self.view_all_expenses()
                elif choice == '3':
                    self.view_by_category()
                elif choice == '4':
                    self.view_by_date_range()
                elif choice == '5':
                    self.edit_expense()
                elif choice == '6':
                    self.delete_expense()
                elif choice == '7':
                    self.view_statistics()
                elif choice == '8':
                    self.view_category_totals()
                elif choice == '9':
                    self.export_to_csv()
                
                if self.running:
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using Personal Expense Tracker!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Please try again.")
        
        print("\n💰 Final Statistics:")
        stats = self.tracker.get_statistics()
        print(f"Total Expenses Tracked: {stats['total_expenses']}")
        print(f"Total Amount: ${stats['total_amount']:.2f}")
        print("\n👋 Goodbye!")

def main():
    """Entry point of the application."""
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
        print(f"Using data file: {data_file}")
        # You could modify ExpenseTracker to accept custom file
    
    cli = ExpenseTrackerCLI()
    cli.run()

if __name__ == "__main__":
    main()