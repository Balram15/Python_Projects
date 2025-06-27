from datetime import datetime
import uuid

class Expense:
    """
    Represents a single expense entry with amount, category, description, and date.
    Each expense gets a unique ID for easy tracking and modification.
    """
    
    def __init__(self, amount, category, description, date_str=None):
        """
        Initialize a new expense.
        
        Args:
            amount (float): The expense amount
            category (str): Category like 'food', 'transport', 'entertainment'
            description (str): Brief description of the expense
            date_str (str, optional): Date in YYYY-MM-DD format. Defaults to today.
        """
        self.id = str(uuid.uuid4())[:8]  # Generate unique 8-character ID
        self.amount = self._validate_amount(amount)
        self.category = category.lower().strip()  # Normalize category
        self.description = description.strip()
        self.date = date_str if date_str else datetime.now().strftime("%Y-%m-%d")
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _validate_amount(self, amount):
        """
        Validate and convert amount to float.
        
        Args:
            amount: Amount to validate (can be string or number)
            
        Returns:
            float: Validated amount
            
        Raises:
            ValueError: If amount is invalid
        """
        try:
            amount_float = float(amount)
            if amount_float < 0:
                raise ValueError("Amount cannot be negative")
            return round(amount_float, 2)  # Round to 2 decimal places
        except (ValueError, TypeError):
            raise ValueError(f"Invalid amount: {amount}")
    
    def to_dict(self):
        """
        Convert expense to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the expense
        """
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create an Expense object from dictionary data.
        This is a factory method - it creates instances in a different way.
        
        Args:
            data (dict): Dictionary containing expense data
            
        Returns:
            Expense: New expense instance
        """
        expense = cls(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date_str=data['date']
        )
        # Preserve original ID and timestamp
        expense.id = data['id']
        expense.created_at = data['created_at']
        return expense
    
    def update(self, amount=None, category=None, description=None, date_param=None):
        """
        Update expense fields.
        
        Args:
            amount (float, optional): New amount
            category (str, optional): New category
            description (str, optional): New description
            date_param (str, optional): New date
        """
        if amount is not None:
            self.amount = self._validate_amount(amount)
        if category is not None:
            self.category = category.lower().strip()
        if description is not None:
            self.description = description.strip()
        if date_param is not None:
            self.date = date_param
    
    def __str__(self):
        """String representation of the expense for display."""
        return f"[{self.id}] ${self.amount:.2f} - {self.category.title()} - {self.description} ({self.date})"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"Expense(id='{self.id}', amount={self.amount}, category='{self.category}', date='{self.date}')"