# 💰 Personal Expense Tracker

A comprehensive command-line expense tracking application built with Python. Track your spending, visualize patterns, and gain insights into your financial habits.



## 🌟 Features

- **💰 Expense Management**: Add, edit, delete, and view expenses with ease
- **🏷️ Category Organization**: Organize expenses by categories (food, transport, entertainment, etc.)
- **📊 Data Visualization**: Generate beautiful charts and graphs of your spending patterns
- **📅 Time-based Analysis**: View expenses by date ranges, monthly trends, and daily patterns
- **📈 Statistics Dashboard**: Get comprehensive insights into your spending habits
- **💾 Data Persistence**: Automatic JSON-based data storage
- **📋 Export Functionality**: Export data to CSV for external analysis
- **🔍 Search & Filter**: Find expenses by category, date range, or amount

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install matplotlib numpy
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
expense-tracker/
├── main.py           # Main CLI interface
├── expense.py        # Expense data model
├── tracker.py        # Core business logic
├── visualizer.py     # Data visualization module
├── data.json         # Data storage (auto-generated)
├── charts/           # Generated charts directory
├── README.md         # Project documentation
└── .gitignore        # Git ignore rules
```

## 🚀 Usage

### Quick Start
1. Run `python main.py`
2. Choose option **1** to add your first expense
3. Enter amount, category, and description
4. Explore other menu options to view and analyze your data

### Main Menu Options
- **➕ Add Expense**: Record new expenses
- **📖 View All Expenses**: See complete expense history
- **🔍 View by Category**: Filter expenses by category
- **📅 View by Date Range**: Analyze spending within specific periods
- **✏️ Edit Expense**: Modify existing expense records
- **🗑️ Delete Expense**: Remove unwanted expense entries
- **📊 View Statistics**: Get comprehensive spending insights
- **📈 View Category Totals**: See spending breakdown by category
- **💾 Export to CSV**: Export data for external analysis

### Example Usage
```bash
💰 Enter amount ($): 25.50
🏷️ Enter category: food
📝 Enter description: lunch at cafe
📅 Enter date (YYYY-MM-DD) or press Enter for today: 

✅ Added expense: [abc12345] $25.50 - Food - lunch at cafe (2025-06-27)
```

## 📊 Visualizations

The application generates several types of charts:

- **📊 Category Pie Chart**: Visual breakdown of spending by category
- **📈 Category Bar Chart**: Compare spending across categories
- **📉 Monthly Trend Line**: Track spending patterns over time
- **📅 Daily Spending Chart**: See daily expense patterns
- **🎛️ Summary Dashboard**: Comprehensive overview with multiple visualizations

### Generate Charts
```python
from visualizer import ExpenseVisualizer
from tracker import ExpenseTracker

tracker = ExpenseTracker()
viz = ExpenseVisualizer(tracker)

# Generate all charts
viz.generate_all_charts()
```

## 🏗️ Architecture

### Core Components

#### **Expense Class** (`expense.py`)
- Represents individual expense entries
- Handles data validation and serialization
- Unique ID generation for each expense

#### **ExpenseTracker Class** (`tracker.py`)
- Manages collection of expenses
- Handles CRUD operations
- JSON persistence and data aggregation

#### **ExpenseTrackerCLI Class** (`main.py`)
- User interface and interaction
- Input validation and error handling
- Menu system and program flow

#### **ExpenseVisualizer Class** (`visualizer.py`)
- Data visualization and chart generation
- Multiple chart types and styling
- Export functionality for charts

### Data Flow
```
User Input → CLI → ExpenseTracker → Expense Objects → JSON Storage
                ↓
            Visualizer → Charts & Analytics
```

## 🧮 Technical Features

### Data Persistence
- **JSON Storage**: Human-readable data format
- **Automatic Backups**: Data saved after each operation
- **Error Recovery**: Graceful handling of corrupted data

### Input Validation
- **Amount Validation**: Ensures positive numeric values
- **Date Parsing**: Flexible date input with validation
- **Category Normalization**: Consistent category formatting

### Performance
- **Time Complexity**: O(n) for most operations
- **Memory Efficient**: Loads all data in memory for fast access
- **Scalable**: Handles thousands of expense records efficiently

## 📈 Example Data Analysis

### Monthly Spending Trend
```
Jan 2024: $1,234.56
Feb 2024: $1,456.78
Mar 2024: $1,123.45
```

### Category Breakdown
```
Food:          $456.78 (35.2%)
Transport:     $234.56 (18.1%)
Entertainment: $123.45 (9.5%)
Shopping:      $345.67 (26.7%)
Other:         $134.89 (10.4%)
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 🐛 Known Issues & Limitations

- **Concurrent Access**: Single-user application, no multi-user support
- **Data Size**: Optimized for personal use (<10,000 expenses)
- **Currency**: Single currency support (USD)
- **Platform**: Tested on Windows, macOS, and Linux

## 🔮 Future Enhancements

- [ ] **Web Interface**: Browser-based UI
- [ ] **Database Support**: PostgreSQL/SQLite integration
- [ ] **Multi-currency**: Support for different currencies
- [ ] **Budget Planning**: Set and track budgets
- [ ] **Recurring Expenses**: Handle subscription and recurring payments
- [ ] **Data Import**: Import from bank statements
- [ ] **Mobile App**: React Native or Flutter app
- [ ] **Cloud Sync**: Synchronization across devices

## 📚 Learning Resources

This project demonstrates:

- **Object-Oriented Programming**: Classes, inheritance, encapsulation
- **File I/O**: JSON serialization and data persistence
- **Error Handling**: Exception management and recovery
- **Data Visualization**: Matplotlib charts and graphs
- **CLI Development**: User interface design and interaction
- **Software Architecture**: Modular design and separation of concerns

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- LinkedIn: [Your Name](https://linkedin.com/in/yourname)

## 🙏 Acknowledgments

- **Python Community** for excellent documentation and libraries
- **Matplotlib** for powerful visualization capabilities
- **JSON** for simple and effective data storage
- **Open Source Community** for inspiration and best practices

---

⭐ **Star this repository if you found it helpful!** ⭐

*Built with ❤️ and Python*