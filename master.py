import sqlite3
import re

conn = sqlite3.connect('expenses.db')  # Connect to the SQLite database
cur = conn.cursor()  # Create a cursor object to interact with the database


def validate_date(date_str):
    """
    Checks if the provided string matches the YYYY-MM-DD date format.

    Args:
        date_str (str): The date string to validate.

    Returns:
        bool: True if the string matches the date format, False otherwise.
    """
    pattern = r'\d{4}-\d{2}-\d{2}'
    return bool(re.match(pattern, date_str))


def validate_price(price_str):
    """
    Checks if the provided string represents a numeric value.

    Args:
        price_str (str): The price string to validate.

    Returns:
        bool: True if the string is numeric, False otherwise.
    """
    return price_str.isdigit()


try:
    while True:
        print("Select an option:")
        print("1. Enter a new expense")
        print("2. View expenses summary")

        try:
            choice = int(input())  # Get user choice
        except ValueError:
            print("Invalid input. Please enter a valid option.")
            continue

        if choice == 1:
            date = input("Enter the date of the expense(YYYY-MM-DD): ")
            if not validate_date(date):
                print(
                    "Invalid date format. Please enter the date in the format YYYY-MM-DD.")
                continue

            description = input("Enter the description of the expense: ")

            cur.execute("SELECT DISTINCT category FROM expenses")
            categories = cur.fetchall()

            print("Select a category by number:")
            for idx, category in enumerate(categories):
                print(f"{idx + 1}. {category[0]}")
            print(f"{len(categories) + 1}. Create a new category")

            try:
                category_choice = int(input())  # Get user category choice
            except ValueError:
                print("Invalid input. Please enter a valid category number.")
                continue

            category = (
                input("Enter the new category name: ")
                if category_choice == len(categories) + 1
                else categories[category_choice - 1][0]
            )

            price = input("Enter the price of the expense: ")
            if not validate_price(price):
                print("Invalid price. Please enter a numeric value.")
                continue

            # Insert the new expense entry into the database
            cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                        (date, description, category, price))

            conn.commit()  # Commit changes to the database

        elif choice == 2:
            print("Select an option:")
            print("1. View all expenses")
            print("2. View monthly expenses by category")
            print("3. View all expenses by category")

            try:
                view_choice = int(input())  # Get user view choice
            except ValueError:
                print("Invalid input. Please enter a valid view option.")
                continue

            if view_choice == 1:
                # Fetch and display all expenses from the database
                cur.execute("SELECT * FROM expenses")
                expenses = cur.fetchall()
                for expense in expenses:
                    print(expense)

            elif view_choice == 2:
                month = input("Enter the month (MM): ")
                year = input("Enter the year (YYYY): ")
                # Fetch and display expenses grouped by category for the specified month and year
                cur.execute(
                    """SELECT category, SUM(price) FROM expenses
                    WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                    GROUP BY category""", (month, year))
                expenses = cur.fetchall()
                for expense in expenses:
                    print(f"Category: {expense[0]}, Total: {expense[1]}")

            elif view_choice == 3:
                cur.execute("SELECT DISTINCT category FROM expenses")
                categories = cur.fetchall()

                print("Select a category by number:")
                for idx, category in enumerate(categories):
                    print(f"{idx + 1}. {category[0]}")
                try:
                    category_choice = int(input())  # Get user category choice
                except ValueError:
                    print("Invalid input. Please enter a valid category number.")
                    continue

                selected_category = categories[category_choice - 1][0]
                # Fetch and display all expenses for the selected category
                cur.execute("SELECT * FROM expenses WHERE category = ?",
                            (selected_category,))
                expenses = cur.fetchall()
                for expense in expenses:
                    print(expense)

        else:
            print("Invalid option. Please enter a valid option.")
            continue

        repeat = input("Would you like to do something else (y/n)?\n")
        if repeat.lower() != 'y':
            break

except Exception as e:
    print(f"An unexpected error occurred: {e}")  # Print any errors
finally:
    conn.close()  # Close the database connection