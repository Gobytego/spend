import datetime
import time  
import pickle  
import os 

class SpendingCalculator:
    """
    A simple console-based application to track spending.  It allows the user to
    input expenses, categorize them, and view a summary.
    """
    def __init__(self):
        """
        Initializes the data structures.
        """
        self.expenses = []
        self.categories = ["Food", "Housing", "Transportation", "Entertainment", "Utilities", "Other"]
        self.balance = 0  
        self.transaction_history = []  
        self.history_length = 5  
        self.budget = 0  
        self.budget_interval = "Month"  
        self.data_file = "spending_data.pkl"  
        self.budget_intervals = ["Day", "Week", "Bi-Weekly", "Month", "Year"] 
        self.category_budgets = {}  

        self.load_data()  
        self.initialize_category_budgets() 

    def initialize_category_budgets(self):
        """Initializes the category budgets to 0."""
        for category in self.categories:
            if category not in self.category_budgets:
                self.category_budgets[category] = 0

    def load_data(self):
        """Loads data from a file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "rb") as f:
                    data = pickle.load(f)
                    self.expenses = data.get("expenses", [])
                    self.categories = data.get("categories", ["Food", "Housing", "Transportation", "Entertainment", "Utilities", "Other"])
                    self.balance = data.get("balance", 0)
                    self.transaction_history = data.get("transaction_history", [])
                    self.budget = data.get("budget", 0)
                    self.budget_interval = data.get("budget_interval", "Month")
                    self.category_budgets = data.get("category_budgets", {}) # Load category budgets
            except Exception as e:
                print(f"Error loading data: {e}")
                print("Starting with default data.")

    def save_data(self):
        """Saves data to a file."""
        try:
            with open(self.data_file, "wb") as f:
                data = {
                    "expenses": self.expenses,
                    "categories": self.categories,
                    "balance": self.balance,
                    "transaction_history": self.transaction_history,
                    "budget": self.budget,
                    "budget_interval": self.budget_interval,
                    "category_budgets": self.category_budgets, 
                }
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_expense(self):
        """
        Adds a new expense to the list, validating the input data.
        """
        while True:
            try:
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue  
                break  
            except ValueError:
                print("Invalid amount. Please enter a number.")
            except EOFError:
                print("No input provided. Exiting input for amount.")
                return

        while True:
            try:
                print("Categories:")
                for i, category in enumerate(self.categories):
                    print(f"{i+1}. {category}")
                category_input = input("Enter category number or name: ")
                if not category_input:
                    print("No input provided for category. Exiting category input.")
                    return

                if category_input.isdigit():
                    category_index = int(category_input) - 1
                    if 0 <= category_index < len(self.categories):
                        category = self.categories[category_index]
                        break
                    else:
                        print("Invalid category number. Please choose from the list.")
                        continue
                elif category_input in self.categories:
                    category = category_input
                    break
                else:
                    print("Invalid category name. Please choose from the list or enter the number.")
                    continue
            except EOFError:
                print("No input provided for category. Exiting category input.")
                return

        while True:
            try:
                date_str = input("Enter date (YYYY-MM-DD): ")
                if not date_str:
                    date = datetime.datetime.now()
                    break
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use ȲYYY-MM-DD.")
            except EOFError:
                print("No input provided for date. Exiting date input.")
                return

        self.expenses.append((date, category, amount))
        self.balance -= amount  
        self.transaction_history.append(("Expense", date, category, amount))  
        if len(self.transaction_history) > self.history_length:
            self.transaction_history.pop(0)  
        print("Expense added successfully!")

    def update_summary(self):
        """
        Prints a summary of the current expenses.
        """
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        total_spending = 0
        category_totals = {}
        # Sort expenses by date
        sorted_expenses = sorted(self.expenses, key=lambda x: x[0])

        print("\n--- Expense Summary ---")
        for date, category, amount in sorted_expenses:
            print(f"Date: {date.strftime('%Y-%m-%d')}, Category: {category}, Amount: ${amount:.2f}")
            total_spending += amount
            category_totals[category] = category_totals.get(category, 0) + amount

        print("\n--- Category Totals ---")
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f}")
        print(f"\nTotal Spending: ${total_spending:.2f}")

    def clear_input_fields(self):
        """
        There are no input fields to clear in a console application.
        This method is kept for consistency with the GUI version.
        """
        pass

    def add_category(self):
        """Adds a new category to the list of categories."""
        while True:
            try:
                new_category = input("Enter the new category name: ")
                if not new_category:
                    print("No input provided. Exiting category addition.")
                    return
                if new_category in self.categories:
                    print("Category already exists.")
                    continue
                self.categories.append(new_category)
                self.category_budgets[new_category] = 0  
                print(f"Category '{new_category}' added successfully!")
                break
            except EOFError:
                print("No input provided. Exiting category addition.")
                return

    def delete_category(self):
        """Deletes a category from the list of categories."""
        while True:
            try:
                category_to_delete = input(f"Enter the category to delete ({', '.join(self.categories)}): ")
                if not category_to_delete:
                    print("No input provided. Exiting category deletion.")
                    return
                if category_to_delete not in self.categories:
                    print("Category not found.")
                    continue
                self.categories.remove(category_to_delete)
                if category_to_delete in self.category_budgets:
                    del self.category_budgets[category_to_delete]  
                print(f"Category '{category_to_delete}' deleted successfully!")
                break
            except EOFError:
                print("No input provided. Exiting category deletion.")
                return

    def list_categories(self):
        """Lists all categories."""
        if not self.categories:
            print("No categories defined.")
            return
        print("\n--- Categories ---")
        for category in self.categories:
            print(category)

    def add_money(self):
        """Adds money to the balance."""
        while True:
            try:
                amount = float(input("Enter amount to add: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                self.balance += amount
                self.transaction_history.append(("Deposit", datetime.datetime.now(), "Deposit", amount))  
                if len(self.transaction_history) > self.history_length:
                    self.transaction_history.pop(0)  
                print(f"${amount:.2f} added to balance. New balance: ${self.balance:.2f}")
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
            except EOFError:
                print("No input provided. Exiting adding money.")
                return

    def display_status(self):
        """Displays the current balance and the last few transactions."""
        print("\n--- Current Balance and Recent Transactions ---")
        print(f"Current Balance: ${self.balance:.2f}")
        if self.budget > 0:
            print(f"Total Budget ({self.budget_interval}): ${self.budget:.2f}")
            now = datetime.datetime.now()
            if self.budget_interval.lower() == "month":
                month_start = now.replace(day=1)
                month_expenses = sum(expense[2] for expense in self.expenses if month_start <= expense[0] <= now)
                print(f"Spending this month: ${month_expenses:.2f}")
                print(f"Remaining budget: ${self.budget - month_expenses:.2f}")
            elif self.budget_interval.lower() == "year":
                year_start = now.replace(month=1, day=1)
                year_expenses = sum(expense[2] for expense in self.expenses if year_start <= expense[0] <= now)
                print(f"Spending this year: ${year_expenses:.2f}")
                print(f"Remaining budget: ${self.budget - year_expenses:.2f}")
            elif self.budget_interval.lower() == "day":
                day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                day_expenses = sum(expense[2] for expense in self.expenses if day_start <= expense[0] <= now)
                print(f"Spending today: ${day_expenses:.2f}")
                print(f"Remaining budget: ${self.budget - day_expenses:.2f}")
            elif self.budget_interval.lower() == "week":
                week_start = now - datetime.timedelta(days=now.weekday())
                week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                week_expenses = sum(expense[2] for expense in self.expenses if week_start <= expense[0] <= now)
                print(f"Spending this week: ${week_expenses:.2f}")
                print(f"Remaining budget: ${self.budget - week_expenses:.2f}")
            elif self.budget_interval.lower() == "bi-weekly":
                # Calculate the start of the bi-weekly period.  This assumes the bi-weekly period starts on a Monday
                days_since_monday = now.weekday()
                weeks_since_start = (now - datetime.datetime(1970, 1, 5)).days // 7  # 1970-01-05 was a Monday
                if weeks_since_start % 2 != 0:
                    days_since_monday += 7
                bi_weekly_start = now - datetime.timedelta(days=days_since_monday)
                bi_weekly_start = bi_weekly_start.replace(hour=0, minute=0, second=0, microsecond=0)
                bi_weekly_expenses = sum(expense[2] for expense in self.expenses if bi_weekly_start <= expense[0] <= now)
                print(f"Spending this bi-weekly period: ${bi_weekly_expenses:.2f}")
                print(f"Remaining budget: ${self.budget - bi_weekly_expenses:.2f}")

        if self.category_budgets:
            print("\n--- Category Budgets ---")
            category_expenses = {}
            for expense in self.expenses:
                category = expense[1]
                amount = expense[2]
                category_expenses[category] = category_expenses.get(category, 0) + amount

            for category, budget in self.category_budgets.items():
                expense = category_expenses.get(category, 0)
                remaining = budget - expense
                print(f"{category}: Budget = ${budget:.2f}, Spent = ${expense:.2f}, Remaining = ${remaining:.2f}")

        if self.transaction_history:
            print("\n--- Last Transactions ---")
            for transaction_type, date, category, amount in reversed(self.transaction_history):
                print(f"{transaction_type}: {date.strftime('%Y-%m-%d %H:%M:%S')}, Category: {category}, Amount: ${amount:.2f}")
        else:
            print("No recent transactions.")

    def set_budget(self):
        """Sets the budget."""
        while True:
            try:
                budget = float(input("Enter your total budget: "))
                if budget <= 0:
                    print("Budget must be greater than zero.")
                    continue
                self.budget = budget
                print(f"Total budget set to: ${self.budget:.2f}")
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
            except EOFError:
                print("No input provided. Exiting setting budget.")
                return

    def set_category_budget(self):
        """Sets the budget for a specific category."""
        while True:
            try:
                print("\nAvailable Categories:")
                for i, category in enumerate(self.categories):
                    print(f"{i+1}. {category}")
                category_input = input("Enter category number or name: ")
                if not category_input:
                    print("No input provided. Exiting category budget setting.")
                    return

                if category_input.isdigit():
                    category_index = int(category_input) - 1
                    if 0 <= category_index < len(self.categories):
                        category = self.categories[category_index]
                        break
                    else:
                        print("Invalid category number. Please choose from the list.")
                        continue
                elif category_input in self.categories:
                    category = category_input
                    break
                else:
                    print("Invalid category name. Please choose from the list or enter the number.")
                    continue
            except EOFError:
                print("No input provided. Exiting category budget setting.")
                return

        while True:
            try:
                budget = float(input(f"Enter budget for {category}: "))
                if budget <= 0:
                    print("Budget must be greater than zero.")
                    continue
                self.category_budgets[category] = budget
                print(f"Budget for {category} set to: ${budget:.2f}")
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
            except EOFError:
                print("No input provided. Exiting setting category budget.")
                return

    def set_budget_interval(self):
        """Sets the budget interval."""
        while True:
            try: # added try
                interval = input(f"Enter budget interval ({', '.join(self.budget_intervals)}): ").title()
                if interval not in self.budget_intervals:
                    print("Invalid interval. Please choose from the list.")
                    continue
                self.budget_interval = interval
                print(f"Budget interval set to: {self.budget_interval}")
                break
            except EOFError:
                print("No input provided. Exiting setting budget interval")
                return

    def category_menu(self):
        """Manages categories."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("\n--- Category Menu ---")
            self.list_categories()
            print("\nOptions:")
            print("1. Add Category")
            print("2. Delete Category")
            print("x. Exit to Main Menu") 
            try:
                choice = input("Enter your choice: ")
            except EOFError:
                print("\nNo input provided. Exiting to main menu...")
                return

            if choice == '1':
                self.add_category()
            elif choice == '2':
                self.delete_category()
            elif choice.lower() == 'x': 
                return  
            else:
                print("Invalid choice. Please try again.")
            time.sleep(1)

    def budget_menu(self):
        """Manages budget and budget interval."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("\n--- Budget Menu ---")
            print(f"Total Budget: ${self.budget:.2f}")
            print(f"Current Budget Interval: {self.budget_interval}")
            print("\nCategory Budgets:")
            category_expenses = {}
            for expense in self.expenses:
                category = expense[1]
                amount = expense[2]
                category_expenses[category] = category_expenses.get(category, 0) + amount
            for category, budget in self.category_budgets.items():
                expense = category_expenses.get(category, 0)
                remaining = budget - expense
                print(f"  {category}: Budget = ${budget:.2f}, Spent = ${expense:.2f}, Remaining = ${remaining:.2f}")

            # Calculate total expenses
            total_expenses = sum(expense[2] for expense in self.expenses)
            print(f"\nTotal Expenses: ${total_expenses:.2f}")

            # Calculate remaining budget
            remaining_budget = self.budget - total_expenses
            print(f"Remaining Budget: ${remaining_budget:.2f}")

            print("\nOptions:")
            print("1. Set Total Budget")
            print("2. Set Category Budget")
            print("3. Set Budget Interval")
            print("x. Exit to Main Menu") 
            try:
                choice = input("Enter your choice: ")
            except EOFError:
                print("\nNo input provided. Exiting to main menu...")
                return

            if choice == '1':
                self.set_budget()
            elif choice == '2':
                self.set_category_budget()
            elif choice == '3':
                self.set_budget_interval()
            elif choice.lower() == 'x': 
                return  
            else:
                print("Invalid choice. Please try again.")
            time.sleep(1)

    def clear_all_data(self):
        """Clears all data: expenses, balance, history, budget, and category budgets."""
        while True:
            confirmation = input("Are you sure you want to clear all data? (yes/no): ").lower()
            if confirmation == 'yes':
                self.expenses = []
                self.balance = 0
                self.transaction_history = []
                self.budget = 0
                self.category_budgets = {}
                self.save_data()  
                print("All data cleared successfully!")
                break
            elif confirmation == 'no':
                print("Data clearing cancelled.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def run(self):
        """
        Runs the main loop of the application.
        """
        print("Welcome to the Spending Calculator!")
        while True:
            # os.system('cls' if os.name == 'nt' else 'clear') 
            self.display_status()  
            print("\nOptions:")
            print("1. Add Expense")
            print("2. Add Money")
            print("3. View Summary")
            print("4. Budget") 
            print("5. Categories") 
            print("6. Clear All Data")
            print("x. Exit")  
            try:
                choice = input("Enter your choice: ")
            except EOFError:
                print("\nNo input provided. Exiting...")
                break

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.add_money()
            elif choice == '3':
                self.update_summary()
            elif choice == '4':
                self.budget_menu()
            elif choice == '5':
                self.category_menu()
            elif choice == '6':
                self.clear_all_data()
            elif choice.lower() == 'x': 
                print("Exiting...")
                self.save_data()  
                break
            else:
                print("Invalid choice. Please try again.")
            time.sleep(1)  

if __name__ == "__main__":
    calculator = SpendingCalculator()
    calculator.run()

