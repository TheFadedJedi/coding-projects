#Expense Tracker
class Expenses:
    def __init__(self, date, description, amount):
        self.date=date
        self.description=description
        self.amount=amount

#---------------------------------------------------
class ExpenseTracker:
    def __init__(self):
        self.expenses=[]

    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, index):
        if 0<=index<len(self.expenses):
            del self.expenses[index]
            print("Expense removed successfully.")
        else:
            print("Invalid expense index.")
    
    def view_expenses(self):
        if len(self.expenses)==0:
            print("No expenses found.")
        else:
            print("Expense list:")
            for i, expense in enumerate(self.expenses, start=1):
                print(f"{i}. Date:{expense.date}, Description: {expense.description}, Amount: ${expense.amount:.2f}")
            
    def total_expenses(self):
        total=sum(expense.amount for expense in self.expenses)
        print(f"Total Expenses: ${total:.2f}")

    def save_expenses_to_file(self):
        filename="Daily Expenses.txt"
        try:
            with open(filename, 'a') as file:
                for expense in self.expenses:
                    file.write(f"{expense.date},{expense.description},{expense.amount:.2f}\n")
            print(f"Expenses saved to {filename} successfully.")
        except Exception as e:
            print(f"Error saving to file: {e}")

#---------------------------------------------------
def main():
    tracker=ExpenseTracker()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. View Expenses")
        print("4. Total Expenses")
        print("5. Save Expenses to File")
        print("6. Exit")

        choice=input("Enter your choice(1-6): ")

        if choice=="1":
            date=input("Enter the date YYYY-MM-DD: ")
            print("Select a description:")
            print("1. Gas")
            print("2. Groceries")
            print("3. Food")
            print("4. Custom Description")

            description_choice=input("Enter your choice (1-4): ")

            if description_choice=="1":
                description="Gas"
            elif description_choice=="2":
                description="Groceries"
            elif description_choice=="3":
                description="Food"
            elif description_choice=="4":
                description=input("Enter the custom description: ")
            else:
                print("Invalid choice. Using 'Other' as default.")
                description="Other"
                        
            amount=float(input("Enter the amount: "))
            expense=Expenses(date, description, amount)
            tracker.add_expense(expense)
            print("Expense added successfully.")
        elif choice=="2":
            index=int(input("Enter the expence index to remove: "))-1
            tracker.remove_expense(index)
        elif choice=="3":
            tracker.view_expenses()
        elif choice=="4":
            tracker.total_expenses()
        elif choice=="5":
            tracker.save_expenses_to_file()
        elif choice=="6":
            while True:
                print("\nHave all expenses been saved?")
                print("1. Yes")
                print("2. No")
                saved_choice = input("Enter your choice (1 or 2): ").strip()

                if saved_choice=="1":
                    print("Exiting Tracker.")
                    break
                elif saved_choice=="2":
                    while True:
                        print("\nWould you like to save now?")
                        print("1. Yes")
                        print("2. No")
                        save_now_choice = input("Enter your choice (1 or 2): ").strip()

                        if save_now_choice=="1":
                            tracker.save_expenses_to_file()
                            print("Exiting Tracker.")
                            break
                        elif save_now_choice=="2":
                            print("Exiting Tracker without saving.")
                            break
                        else:
                            print("Invalid choice. Please enter 1 or 2.")
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            if saved_choice in ["1", "2"]:
                break
        else:
            print("Invalid choice. Please try again.")
#---------------------------------------------------
if __name__=='__main__':
    main()