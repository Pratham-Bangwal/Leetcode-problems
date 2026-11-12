"""COM-501, Group 2: one console application covering all five milestones."""

import csv
import time
from pathlib import Path

from library_utils import calculate_fine, is_available, prepare_summary

INITIAL_CATALOGUE = {
    "Python Basics": 2,
    "Data Structures": 1,
    "Computer Networks": 2,
    "Operating Systems": 0,
}
RECORD_FILE = Path(__file__).with_name("library_records.txt")


def save_transaction(member_id, student_name, action, book, fine=0.0):
    """Milestone 5: append every successful borrow/return to a text file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with RECORD_FILE.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file, delimiter="|").writerow(
            [timestamp, member_id, student_name, action, book, f"{fine:.2f}"]
        )
    return timestamp


class LibraryAccount:
    """Milestone 3: an account represents one student's library borrowing."""

    library_name = "MIET Campus Library"  # class variable

    def __init__(self, member_id, student_name, catalogue):
        self.member_id = member_id
        self.student_name = student_name.title()  # string operation
        self.borrowed_books = []
        self.catalogue = catalogue

    def borrow_book(self, book, persist=True):
        if len(self.borrowed_books) >= 3:
            return "Rejected: limit of 3 borrowed books reached."
        if book not in self.catalogue:
            return "Rejected: unknown book."
        if not is_available(book, self.catalogue):
            return "Rejected: book unavailable."
        if persist:
            save_transaction(self.member_id, self.student_name, "BORROW", book)
        self.borrowed_books.append(book)
        self.catalogue[book] -= 1
        return f"Borrowed: {book}"

    def return_book(self, book, days_kept=0, allowed_days=14, rate=5.0, persist=True):
        if book not in self.borrowed_books:
            return "Rejected: this member has not borrowed that book."
        fine = calculate_fine(days_kept, allowed_days, rate=rate)
        if persist:
            save_transaction(self.member_id, self.student_name, "RETURN", book, fine)
        self.borrowed_books.remove(book)
        self.catalogue[book] += 1
        return f"Returned: {book} | Overdue fine: Rs. {fine:.2f}"

    def display_account(self):
        print(f"{self.library_name} | {self}")

    def __str__(self):
        return (f"{self.student_name} ({self.member_id}) - "
                f"Borrowed: {prepare_summary(self.borrowed_books)}")


def normalize_book(text):
    """Match catalogue titles without requiring exact uppercase/lowercase."""
    for title in INITIAL_CATALOGUE:
        if title.lower() == text.strip().lower():
            return title
    return text.strip()


def load_state():
    """Rebuild catalogue and accounts from existing transaction history."""
    catalogue = INITIAL_CATALOGUE.copy()
    accounts = {}
    try:
        with RECORD_FILE.open("r", newline="", encoding="utf-8") as file:
            for row in csv.reader(file, delimiter="|"):
                if len(row) != 6:
                    continue
                _, member_id, student_name, action, book, _ = row
                if book not in catalogue or not member_id:
                    continue
                if member_id not in accounts:
                    accounts[member_id] = LibraryAccount(member_id, student_name, catalogue)
                account = accounts[member_id]
                if action == "BORROW":
                    account.borrow_book(book, persist=False)
                elif action == "RETURN":
                    account.return_book(book, persist=False)
    except FileNotFoundError:
        pass  # Normal on first launch; the file is created on first transaction.
    return catalogue, accounts


def get_account(accounts, catalogue):
    member_id = input("Roll/member ID: ").strip()
    if not member_id:
        print("Member ID cannot be blank.")
        return None
    if member_id not in accounts:
        name = input("Student name: ").strip()
        if not name:
            print("Student name cannot be blank.")
            return None
        accounts[member_id] = LibraryAccount(member_id, name, catalogue)
    return accounts[member_id]


def fine_calculator():
    """Milestone 1: data types, arithmetic, string formatting and fixed test data."""
    try:
        name = input("Student name: ").strip().title()
        roll = input("Roll number: ").strip()
        book = input("Book title: ").strip().title()
        days = int(input("Days kept: "))
        allowed = int(input("Allowed days: "))
        rate = float(input("Fine rate (Rs/day): "))
        fine = calculate_fine(days, allowed, rate=rate)
        print(f"Student: {name} ({roll}) | Book: {book}")
        print(f"Types: days={type(days)}, rate={type(rate)}")
        print(f"Overdue: {max(0, days - allowed)} days | Fine: Rs. {fine:.2f}")
    except ValueError:
        print("Handled ValueError: enter valid non-negative numbers.")


def borrow_flow(accounts, catalogue):
    """Milestone 2: dictionary, decisions, loop, DONE and three-book limit."""
    account = get_account(accounts, catalogue)
    if account is None:
        return
    while len(account.borrowed_books) < 3:
        book = input("Book title (or DONE): ").strip()
        if book.upper() == "DONE":
            break
        print(account.borrow_book(normalize_book(book)))
    print("Borrowed books:", prepare_summary(account.borrowed_books))
    print("Updated catalogue:", catalogue)


def return_flow(accounts, catalogue):
    account = get_account(accounts, catalogue)
    if account is None:
        return
    book = normalize_book(input("Book to return: "))
    if book not in account.borrowed_books:
        print("Rejected: this member has not borrowed that book.")
        return
    try:
        days = int(input("Days kept: "))
        allowed = int(input("Allowed days [14]: ") or "14")
        rate = float(input("Fine rate [5]: ") or "5")
        print(account.return_book(book, days, allowed, rate=rate))
        print("Transaction time:", time.strftime("%Y-%m-%d %H:%M:%S"))
    except ValueError:
        print("Handled ValueError: enter valid non-negative numbers.")


def show_records():
    """Milestone 5: show records and handle a missing file safely."""
    try:
        with RECORD_FILE.open("r", encoding="utf-8") as file:
            print(file.read() or "No saved records.")
    except FileNotFoundError:
        print("Handled FileNotFoundError: library_records.txt does not exist yet.")


def oop_demo():
    """Demonstrate two objects without changing the live catalogue or saved file."""
    sample_catalogue = INITIAL_CATALOGUE.copy()
    riya = LibraryAccount("2023A1R015", "Riya Sharma", sample_catalogue)
    aman = LibraryAccount("2023A1R016", "Aman", sample_catalogue)
    print(riya.borrow_book("Python Basics", persist=False))
    print(aman.borrow_book("Data Structures", persist=False))
    print(riya.return_book("Python Basics", 18, 14, rate=5, persist=False))
    riya.display_account()
    aman.display_account()
    print("Transaction time:", time.strftime("%Y-%m-%d %H:%M:%S"))


def main():
    catalogue, accounts = load_state()
    while True:
        print("\nMIET CAMPUS LIBRARY | COM-501 GROUP 2")
        print("1. Book-loan fine (Q1)")
        print("2. Borrow books (Q2)")
        print("3. Return book (Q3)")
        print("4. Show accounts and catalogue")
        print("5. Show saved records (Q5)")
        print("6. Demonstrate two OOP objects (Q3/Q4)")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            fine_calculator()
        elif choice == "2":
            borrow_flow(accounts, catalogue)
        elif choice == "3":
            return_flow(accounts, catalogue)
        elif choice == "4":
            for account in accounts.values():
                account.display_account()
            print("Catalogue:", catalogue)
        elif choice == "5":
            show_records()
        elif choice == "6":
            oop_demo()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
