import sqlite3
import re

conn = sqlite3.connect('expenses.db')
cur = conn.cursor()


def validate_date(date_str):
    pattern = r'\d{4}-\d{2}-\d{2}'
    return bool(re.match(pattern, date_str))


def validate_price(price_str):
    return price_str.isdigit()


try:
    while True:
        print("Select an option:")
        print("1. Enter a new expense")
        print("2. View expenses summary")

        try:
            choice = int(input())
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
                category_choice = int(input())
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

            cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                        (date, description, category, price))

            conn.commit()

        elif choice == 2:
            print("Select an option:")
            print("1. View all expenses")
            print("2. View monthly expenses by category")
            print("3. View all expenses by category")

            try:
                view_choice = int(input())
            except ValueError:
                print("Invalid input. Please enter a valid view option.")
                continue

            if view_choice == 1:
                cur.execute("SELECT * FROM expenses")
                expenses = cur.fetchall()
                for expense in expenses:
                    print(expense)

            elif view_choice == 2:
                month = input("Enter the month (MM): ")
                year = input("Enter the year (YYYY): ")
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
                    category_choice = int(input())
                except ValueError:
                    print("Invalid input. Please enter a valid category number.")
                    continue

                selected_category = categories[category_choice - 1][0]
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
    print(f"An unexpected error occurred: {e}")
finally:
    conn.close()
