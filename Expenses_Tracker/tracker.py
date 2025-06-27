import json
import os
from datetime import datetime, timedelta
from expense import Expense

class ExpenseTracker:
    """
    Main class that manages all expense operations.
    Handles data persistence, filtering, calculations, and CRUD operations.
    """
    
    def __init__(self, data_file='data.json'):
        """
        Initialize the expense tracker.
        
        Args:
            data_file (str): Path to JSON file for data storage
        """
        self.data_file = data_file
        self.expenses = []  # List to store all expense objects
        self.load_data()
    
    def load_data(self):
        """
        Load expenses from JSON file into memory.
        Creates empty list if file doesn't exist or is corrupted.
        
        Time Complexity: O(n) where n is number of expenses
        Space Complexity: O(n) - stores all expenses in memory
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Convert each dictionary back to Expense object
                    self.expenses = [Expense.from_dict(exp_data) for exp_data in data]
                print(f"Loaded {len(self.expenses)} expenses from {self.data_file}")
            except json.JSONDecodeError:
                print(f"Warning: {self.data_file} is corrupted. Starting fresh.")
                self.expenses = []
            except KeyError as e:
                print(f"Warning: Missing required field {e}. Starting fresh.")
                self.expenses = []
            except Exception as e:
                print(f"Error loading data: {e}. Starting fresh.")
                self.expenses = []
        else:
            print(f"No existing data file found. Will create {self.data_file} on first save.")
            self.expenses = []
    
    def save_data(self):
        """
        Save all expenses to JSON file.
        
        Time Complexity: O(n) where n is number of expenses
        Space Complexity: O(n) for JSON serialization
        """
        try:
            # Convert all expense objects to dictionaries
            data = [expense.to_dict() for expense in self.expenses]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)  # indent=2 makes it readable
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def add_expense(self, amount, category, description, date_str=None):
        """
        Add a new expense to the tracker.
        
        Args:
            amount (float): Expense amount
            category (str): Category name
            description (str): Expense description
            date_str (str, optional): Date in YYYY-MM-DD format
            
        Returns:
            tuple: (success: bool, message: str, expense_id: str or None)
        """
        try:
            expense = Expense(amount, category, description, date_str)
            self.expenses.append(expense)
            
            if self.save_data():
                return True, f"Added expense: {expense}", expense.id
            else:
                # Remove from memory if save failed
                self.expenses.pop()
                return False, "Failed to save expense", None
                
        except ValueError as e:
            return False, f"Invalid expense data: {e}", None
        except Exception as e:
            return False, f"Unexpected error: {e}", None
    
    def delete_expense(self, expense_id):
        """
        Delete an expense by its ID.
        
        Args:
            expense_id (str): ID of expense to delete
            
        Returns:
            tuple: (success: bool, message: str)
            
        Time Complexity: O(n) - linear search through expenses
        """
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                deleted_expense = self.expenses.pop(i)
                if self.save_data():
                    return True, f"Deleted: {deleted_expense}"
                else:
                    # Restore if save failed
                    self.expenses.insert(i, deleted_expense)
                    return False, "Failed to save after deletion"
        
        return False, f"Expense with ID '{expense_id}' not found"
    
    def update_expense(self, expense_id, amount=None, category=None, description=None, date_str=None):
        """
        Update an existing expense.
        
        Args:
            expense_id (str): ID of expense to update
            amount, category, description, date_str: New values (None to keep current)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        for expense in self.expenses:
            if expense.id == expense_id:
                try:
                    # Store original values in case we need to rollback
                    original_values = {
                        'amount': expense.amount,
                        'category': expense.category,
                        'description': expense.description,
                        'date': expense.date
                    }
                    
                    # Update the expense
                    expense.update(amount, category, description, date_str)
                    
                    if self.save_data():
                        return True, f"Updated expense: {expense}"
                    else:
                        # Rollback changes if save failed
                        expense.update(**original_values)
                        return False, "Failed to save updated expense"
                        
                except ValueError as e:
                    return False, f"Invalid update data: {e}"
        
        return False, f"Expense with ID '{expense_id}' not found"
    
    def update_expense(self, expense_id, amount=None, category=None, description=None, date=None):
        """
        Update an existing expense.
        
        Args:
            expense_id (str): ID of expense to update
            amount, category, description, date: New values (None to keep current)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        for expense in self.expenses:
            if expense.id == expense_id:
                try:
                    # Store original values in case we need to rollback
                    original_values = {
                        'amount': expense.amount,
                        'category': expense.category,
                        'description': expense.description,
                        'date': expense.date
                    }
                    
                    # Update the expense
                    expense.update(amount, category, description, date)
                    
                    if self.save_data():
                        return True, f"Updated expense: {expense}"
                    else:
                        # Rollback changes if save failed
                        expense.update(**original_values)
                        return False, "Failed to save updated expense"
                        
                except ValueError as e:
                    return False, f"Invalid update data: {e}"
        
        return False, f"Expense with ID '{expense_id}' not found"
    
    def get_all_expenses(self):
        """
        Get all expenses, sorted by date (most recent first).
        
        Returns:
            list: All expenses sorted by date
            
        Time Complexity: O(n log n) due to sorting
        """
        return sorted(self.expenses, key=lambda x: x.date, reverse=True)
    
    def get_expenses_by_category(self, category):
        """
        Filter expenses by category.
        
        Args:
            category (str): Category to filter by
            
        Returns:
            list: Expenses in the specified category
            
        Time Complexity: O(n) - linear scan
        Space Complexity: O(k) where k is number of matching expenses
        """
        category = category.lower().strip()
        return [exp for exp in self.expenses if exp.category == category]
    
    def get_expenses_by_date_range(self, start_date, end_date):
        """
        Get expenses within a date range.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            list: Expenses within the date range
            
        Time Complexity: O(n) - check each expense
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            result = []
            for expense in self.expenses:
                expense_date = datetime.strptime(expense.date, "%Y-%m-%d")
                if start <= expense_date <= end:
                    result.append(expense)
            
            return sorted(result, key=lambda x: x.date, reverse=True)
            
        except ValueError as e:
            print(f"Invalid date format: {e}")
            return []
    
    def get_recent_expenses(self, days=7):
        """
        Get expenses from the last N days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            list: Recent expenses
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        return self.get_expenses_by_date_range(cutoff_str, today_str)
    
    def get_category_totals(self):
        """
        Calculate total spending by category.
        
        Returns:
            dict: Category names mapped to total amounts
            
        Time Complexity: O(n) - single pass through expenses
        Space Complexity: O(k) where k is number of unique categories
        """
        totals = {}
        for expense in self.expenses:
            if expense.category in totals:
                totals[expense.category] += expense.amount
            else:
                totals[expense.category] = expense.amount
        
        # Sort by amount (highest first)
        return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))
    
    def get_total_spending(self):
        """
        Calculate total spending across all expenses.
        
        Returns:
            float: Total amount spent
        """
        return round(sum(expense.amount for expense in self.expenses), 2)
    
    def get_expense_by_id(self, expense_id):
        """
        Find a specific expense by its ID.
        
        Args:
            expense_id (str): ID to search for
            
        Returns:
            Expense or None: The expense if found, None otherwise
            
        Time Complexity: O(n) - linear search
        """
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None
    
    def get_statistics(self):
        """
        Get summary statistics about expenses.
        
        Returns:
            dict: Statistics including totals, averages, and counts
        """
        if not self.expenses:
            return {
                'total_expenses': 0,
                'total_amount': 0.0,
                'average_expense': 0.0,
                'max_expense': 0.0,
                'min_expense': 0.0,
                'categories': 0,
                'date_range': 'No expenses'
            }
        
        amounts = [exp.amount for exp in self.expenses]
        dates = [exp.date for exp in self.expenses]
        
        return {
            'total_expenses': len(self.expenses),
            'total_amount': self.get_total_spending(),
            'average_expense': round(sum(amounts) / len(amounts), 2),
            'max_expense': max(amounts),
            'min_expense': min(amounts),
            'categories': len(set(exp.category for exp in self.expenses)),
            'date_range': f"{min(dates)} to {max(dates)}"
        }
    
    def get_monthly_total(self, month=None, year=None):
        """
        Calculate total spending for a specific month.
        
        Args:
            month (int, optional): Month (1-12). Defaults to current month.
            year (int, optional): Year. Defaults to current year.
            
        Returns:
            float: Total spending for the month
        """
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year
        
        total = 0.0
        for expense in self.expenses:
            expense_date = datetime.strptime(expense.date, "%Y-%m-%d")
            if expense_date.month == month and expense_date.year == year:
                total += expense.amount
        
        return round(total, 2)
    
    def get_total_spending(self):
        """
        Calculate total spending across all expenses.
        
        Returns:
            float: Total amount spent
        """
        return round(sum(expense.amount for expense in self.expenses), 2)
    
    def get_expense_by_id(self, expense_id):
        """
        Find a specific expense by its ID.
        
        Args:
            expense_id (str): ID to search for
            
        Returns:
            Expense or None: The expense if found, None otherwise
            
        Time Complexity: O(n) - linear search
        """
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None
    
    def get_statistics(self):
        """
        Get summary statistics about expenses.
        
        Returns:
            dict: Statistics including totals, averages, and counts
        """
        if not self.expenses:
            return {
                'total_expenses': 0,
                'total_amount': 0.0,
                'average_expense': 0.0,
                'max_expense': 0.0,
                'min_expense': 0.0,
                'categories': 0,
                'date_range': 'No expenses'
            }
        
        amounts = [exp.amount for exp in self.expenses]
        dates = [exp.date for exp in self.expenses]
        
        return {
            'total_expenses': len(self.expenses),
            'total_amount': self.get_total_spending(),
            'average_expense': round(sum(amounts) / len(amounts), 2),
            'max_expense': max(amounts),
            'min_expense': min(amounts),
            'categories': len(set(exp.category for exp in self.expenses)),
            'date_range': f"{min(dates)} to {max(dates)}"
        }