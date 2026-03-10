from datetime import date
try:
    from tabulate import tabulate
except ModuleNotFoundError:
    tabulate = None


def print_table(rows: list[list], headers: list[str]) -> None:
    """Print a table with tabulate when available, else a simple fallback."""
    if tabulate is not None:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        return

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def make_line(sep: str = "-") -> str:
        return "+" + "+".join(sep * (w + 2) for w in widths) + "+"

    def make_row(values: list) -> str:
        padded = [str(v).ljust(widths[i]) for i, v in enumerate(values)]
        return "| " + " | ".join(padded) + " |"

    print(make_line("-"))
    print(make_row(headers))
    print(make_line("="))
    for row in rows:
        print(make_row(row))
    print(make_line("-"))


def add_expense(expenses: list[dict]) -> None:
    """Ask user details and add a new expense dictionary into the list."""
    print("\nAdd a new expense")

    amount_str = input("Amount (e.g., 120.50): ").strip()
    category = input("Category (e.g., Food/Travel/Rent): ").strip()
    description = input("Description (e.g., Uber Auto): ").strip()

    # Basic validation (beginner-friendly)
    if not amount_str:
        print("❌ Amount cannot be empty.")
        return

    try:
        amount = float(amount_str)
    except ValueError:
        print("❌ Amount must be a number.")
        return

    if amount <= 0:
        print("❌ Amount must be greater than 0.")
        return

    if not category:
        print("❌ Category cannot be empty.")
        return

    expense = {
        "date": str(date.today()),
        "amount": amount,
        "category": category,
        "description": description
    }

    expenses.append(expense)
    print("✅ Expense added successfully!")


def list_expenses(expenses: list[dict]) -> None:
    """Print all expenses in a table format."""
    print("\nAll expenses")

    if not expenses:
        print("No expenses found yet.")
        return

    rows = []
    for e in expenses:
        rows.append([e["date"], e["amount"], e["category"], e["description"]])

    print_table(rows, headers=["Date", "Amount", "Category", "Description"])


def show_total(expenses: list[dict]) -> None:
    """Print total spending."""
    total = 0.0
    for e in expenses:
        total += float(e["amount"])

    print(f"\nTotal spending: ₹{total:.2f}")


def show_category_summary(expenses: list[dict]) -> None:
    """Print spending summary by category."""
    print("\nCategory summary")

    if not expenses:
        print("No expenses found yet.")
        return

    summary = {}
    for e in expenses:
        cat = e["category"]
        amt = float(e["amount"])
        summary[cat] = summary.get(cat, 0.0) + amt

    rows = []
    for cat, amt in summary.items():
        rows.append([cat, f"₹{amt:.2f}"])

    print_table(rows, headers=["Category", "Total"])
