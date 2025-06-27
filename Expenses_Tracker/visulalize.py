import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from collections import defaultdict
import calendar

class ExpenseVisualizer:
    def __init__(self, tracker):
        # Store the tracker instance
        self.tracker = tracker
        # Set up chart styling
        self.setup_style()
    
    def setup_style(self):
        # Configure matplotlib for better looking charts
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
    
    def create_category_pie_chart(self, save_path=None):
        # Get spending data by category
        category_totals = self.tracker.get_category_totals()
        
        if not category_totals:
            print("No data available for pie chart.")
            return False
        
        # Extract categories and amounts
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        # Create the pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Generate colors for each slice
        colors = plt.cm.Set3(range(len(categories)))
        
        # Create pie chart with percentages
        wedges, texts, autotexts = ax.pie(
            amounts, 
            labels=[cat.title() for cat in categories],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.05] * len(categories)  # Separate slices slightly
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Add title with total
        total_amount = sum(amounts)
        ax.set_title(f'Spending by Category - Total: ${total_amount:.2f}', 
                    fontsize=16, fontweight='bold')
        
        # Make the pie circular
        ax.axis('equal')
        
        # Save or show the chart
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            print(f"Pie chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
        return True
    
    def create_category_bar_chart(self, save_path=None):
        # Get category data
        category_totals = self.tracker.get_category_totals()
        
        if not category_totals:
            print("No data available for bar chart.")
            return False
        
        # Prepare data for plotting
        categories = [cat.title() for cat in category_totals.keys()]
        amounts = list(category_totals.values())
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create bars with different colors
        bars = ax.bar(categories, amounts, color=plt.cm.viridis(range(len(categories))))
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(amounts)*0.01,
                   f'${height:.2f}',
                   ha='center', va='bottom', fontweight='bold')
        
        # Style the chart
        ax.set_title('Spending by Category', fontsize=16, fontweight='bold')
        ax.set_xlabel('Category', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        
        # Rotate x-axis labels if needed
        if len(categories) > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Add grid for better readability
        ax.grid(axis='y', alpha=0.3)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save or show
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            print(f"Bar chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
        return True
    
    def create_monthly_spending_chart(self, save_path=None):
        # Get all expenses
        expenses = self.tracker.get_all_expenses()
        
        if not expenses:
            print("No data available for monthly chart.")
            return False
        
        # Group expenses by month
        monthly_totals = defaultdict(float)
        
        for expense in expenses:
            # Parse the date and create month key
            date_obj = datetime.strptime(expense.date, "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")  # Format: "2024-06"
            monthly_totals[month_key] += expense.amount
        
        # Sort months chronologically
        sorted_months = sorted(monthly_totals.keys())
        amounts = [monthly_totals[month] for month in sorted_months]
        
        # Create readable month labels
        month_labels = []
        for month in sorted_months:
            date_obj = datetime.strptime(month, "%Y-%m")
            month_labels.append(date_obj.strftime("%b %Y"))  # "Jun 2024"
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot line with markers
        ax.plot(month_labels, amounts, marker='o', linewidth=2, markersize=8, 
                color='#2E86AB', markerfacecolor='#A23B72')
        
        # Add value labels on points
        for i, amount in enumerate(amounts):
            ax.annotate(f'${amount:.0f}', 
                       (i, amount), 
                       textcoords="offset points", 
                       xytext=(0,10), 
                       ha='center',
                       fontweight='bold')
        
        # Style the chart
        ax.set_title('Monthly Spending Trend', fontsize=16, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save or show
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            print(f"Monthly chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
        return True
    
    def create_daily_spending_chart(self, days=30, save_path=None):
        # Get recent expenses
        recent_expenses = self.tracker.get_recent_expenses(days)
        
        if not recent_expenses:
            print(f"No data available for last {days} days.")
            return False
        
        # Group by date
        daily_totals = defaultdict(float)
        
        for expense in recent_expenses:
            daily_totals[expense.date] += expense.amount
        
        # Create date range for last N days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        dates = []
        amounts = []
        
        # Fill in all dates (including days with no expenses)
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            dates.append(current_date)
            amounts.append(daily_totals.get(date_str, 0))
            current_date += timedelta(days=1)
        
        # Create the chart
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Create bar chart
        bars = ax.bar(dates, amounts, color='#F18F01', alpha=0.7, edgecolor='#C73E1D')
        
        # Highlight non-zero days
        for i, (date, amount) in enumerate(zip(dates, amounts)):
            if amount > 0:
                bars[i].set_color('#C73E1D')
        
        # Format x-axis to show dates nicely
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
        
        # Style the chart
        ax.set_title(f'Daily Spending - Last {days} Days', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        
        # Rotate dates for better readability
        plt.xticks(rotation=45)
        
        # Add grid
        ax.grid(axis='y', alpha=0.3)
        
        # Add summary statistics
        total_spent = sum(amounts)
        avg_daily = total_spent / days
        ax.text(0.02, 0.98, f'Total: ${total_spent:.2f}\nDaily Average: ${avg_daily:.2f}', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        # Save or show
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            print(f"Daily chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
        return True
    
    def create_expense_summary_dashboard(self, save_path=None):
        # Create a dashboard with multiple charts
        expenses = self.tracker.get_all_expenses()
        
        if not expenses:
            print("No data available for dashboard.")
            return False
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Expense Summary Dashboard', fontsize=20, fontweight='bold')
        
        # Chart 1: Category pie chart
        category_totals = self.tracker.get_category_totals()
        if category_totals:
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            ax1.pie(amounts, labels=[cat.title() for cat in categories], autopct='%1.1f%%', startangle=90)
            ax1.set_title('Spending by Category')
        
        # Chart 2: Monthly trend
        monthly_totals = defaultdict(float)
        for expense in expenses:
            date_obj = datetime.strptime(expense.date, "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")
            monthly_totals[month_key] += expense.amount
        
        if monthly_totals:
            sorted_months = sorted(monthly_totals.keys())
            month_amounts = [monthly_totals[month] for month in sorted_months]
            month_labels = [datetime.strptime(month, "%Y-%m").strftime("%b") for month in sorted_months]
            ax2.plot(month_labels, month_amounts, marker='o', linewidth=2)
            ax2.set_title('Monthly Spending Trend')
            ax2.set_ylabel('Amount ($)')
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # Chart 3: Top expenses
        top_expenses = sorted(expenses, key=lambda x: x.amount, reverse=True)[:10]
        if top_expenses:
            descriptions = [exp.description[:15] + '...' if len(exp.description) > 15 
                           else exp.description for exp in top_expenses]
            expense_amounts = [exp.amount for exp in top_expenses]
            ax3.barh(range(len(descriptions)), expense_amounts, color='lightcoral')
            ax3.set_yticks(range(len(descriptions)))
            ax3.set_yticklabels(descriptions)
            ax3.set_title('Top 10 Expenses')
            ax3.set_xlabel('Amount ($)')
        
        # Chart 4: Statistics text
        stats = self.tracker.get_statistics()
        stats_text = f"""
        Total Expenses: {stats['total_expenses']}
        Total Amount: ${stats['total_amount']:.2f}
        Average: ${stats['average_expense']:.2f}
        Highest: ${stats['max_expense']:.2f}
        Lowest: ${stats['min_expense']:.2f}
        Categories: {stats['categories']}
        """
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax4.set_title('Statistics Summary')
        ax4.axis('off')
        
        plt.tight_layout()
        
        # Save or show
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            print(f"Dashboard saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
        return True
    
    def generate_all_charts(self, output_dir="charts"):
        # Create all charts and save them
        import os
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("Generating all charts...")
        
        # Generate each chart
        charts_created = 0
        
        if self.create_category_pie_chart(f"{output_dir}/category_pie.png"):
            charts_created += 1
        
        if self.create_category_bar_chart(f"{output_dir}/category_bar.png"):
            charts_created += 1
        
        if self.create_monthly_spending_chart(f"{output_dir}/monthly_trend.png"):
            charts_created += 1
        
        if self.create_daily_spending_chart(30, f"{output_dir}/daily_spending.png"):
            charts_created += 1
        
        if self.create_expense_summary_dashboard(f"{output_dir}/dashboard.png"):
            charts_created += 1
        
        print(f"Created {charts_created} charts in '{output_dir}' directory")
        return charts_created > 0