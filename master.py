import sqlite3
import datetime

conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

while True:
    # Display the main menu options to the user
    print("Select an option:")
    print("1. Enter a new expense")
    print("2. View expenses summary")

    choice = int(input())

    # Option 1: Enter a new expense
    if choice == 1:
        # Collect expense details from user
        date = input("Enter the date of the expense(YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        # Fetch unique categories from the database
        cur.execute("SELECT DISTINCT category FROM expenses")

        categories = cur.fetchall()

        # Display categories for user to choose or create a new one
        print("Select a category by number:")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}. {category[0]}")
        print(f"{len(categories) + 1}. Create a new category")

        # Determine if a new category needs to be created or an existing one selected
        category_choice = int(input())
        category = (
            input("Enter the new category name: ")
            if category_choice == len(categories) + 1
            else categories[category_choice - 1][0]
        )
        price = input("Enter the price of the expense: ")

        # Insert the new expense into the database
        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                    (date, description, category, price))

        # Commit changes to the database
        conn.commit()

    # Option 2: View expenses summary
    elif choice == 2:
        # Provide user with viewing options
        print("Select an option:")
        print("1. View all expenses")
        print("2. View montly expenses by category")
        print("3. View all expenses by category")
        view_choice = int(input())

        # View choice 1: Display all expenses
        if view_choice == 1:
            cur.execute("SELECT * FROM expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)

        # View choice 2: Display monthly expenses by category
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            cur.execute(
                """SELECT category, SUM(price) FROM expenses
                WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                GROUP BY category""", (month, year))

        # View choice 3: Display expenses filtered by a specific category
        elif view_choice == 3:
            print("View all expenses by category")
            cur.execute("SELECT DISTINCT category FROM expenses")
            categories = cur.fetchall()

            # Allow user to select a category to filter expenses
            print("Select a category by number:")
            for idx, category in enumerate(categories):
                print(f"{idx + 1}. {category[0]}")
            category_choice = int(input())
            selected_category = categories[category_choice - 1][0]
            cur.execute("SELECT * FROM expenses WHERE category = ?",
                        (selected_category,))
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)

        # Fetch and display expenses after filtering
        expenses = cur.fetchall()
        for expense in expenses:
            print(f"Category: {expense[0]}, Total: {expense[1]}")
        else:
            exit()
    else:
        # Terminate the program if the user enters an invalid option
        exit()

    # Ask user if they want to perform another action
    repeat = input("Would you like to do something else (y/n)?\n")
    if repeat.lower() != 'y':
        break

# Close database connection
conn.close()
