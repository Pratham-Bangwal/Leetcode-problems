# MIET Campus Library Borrowing and Fine Management System

**Python Programming (COM-501) — Group 2**

This is **one console application** developed through all five assignment milestones. No third-party packages needed.

## Run

Keep `main.py` and `library_utils.py` in this directory. Run:

```bash
python main.py
```

The application generates `library_records.txt` when a borrow or return succeeds; restarting the app restores recorded loans and stock.

## Milestone coverage

| Q | Requirements | Evidence |
|---|---|---|
| Q1 | Student name, roll, book, days, allowed days, rate; numeric types, string formatting, fine | Menu **1**, test Riya Sharma / 2023A1R015 / Learning Python / 18 / 14 / 5 → **4 days, Rs. 20** |
| Q2 | Catalogue dictionary (2,1,2,0), loops, DONE/3-book limit, reject unknown/unavailable, update copies | Menu **2**, borrow 3 books and separately test Operating Systems and an unknown title |
| Q3 | `LibraryAccount` attributes and class variable, constructor, borrow/return/display methods, `__str__`, 2 objects | Menu **6**, Riya and Aman, borrow and return |
| Q4 | `library_utils.py` functions, collection parameter, default/keyword rate, imported by `main.py`, time | `library_utils.py`, menu **1**, **3**, and **6** |
| Q5 | Append records; read records; handle `ValueError` and `FileNotFoundError` | Menus **2**, **3**, **5** and invalid numeric input in **1** |

## Sample output (reproduce using the menu)

```text
Student: Riya Sharma (2023A1R015) | Book: Learning Python
Types: days=<class 'int'>, rate=<class 'float'>
Overdue: 4 days | Fine: Rs. 20.00

Borrowed: Python Basics
Borrowed: Data Structures
Borrowed: Computer Networks
Borrowed books: Python Basics, Data Structures, Computer Networks
Updated catalogue: {'Python Basics': 1, 'Data Structures': 0, 'Computer Networks': 1, 'Operating Systems': 0}

Rejected: book unavailable.
Rejected: unknown book.
Handled ValueError: enter valid non-negative numbers.
Handled FileNotFoundError: library_records.txt does not exist yet.
```

A generated records-file line looks like:

```text
2026-11-12 09:30:00|2023A1R015|Riya Sharma|BORROW|Python Basics|0.00
```

Dates are illustrative; actual runs print the runtime timestamp.

## Short explanations

**OOP:** `LibraryAccount` represents each student's library account, using a constructor to initialize member details and an empty loans list. Instance methods borrow, return and display books. The shared `library_name` and readable `__str__()` complete the class design.

**Debugging:** `ValueError` is handled for invalid or negative numeric input; users should supply valid nonnegative numbers. `FileNotFoundError` is handled when the records file is missing; the program creates it at the first successful transaction.

## Submission

Capture real output screenshots for all five milestones. Include this individual GitHub URL in your report. The report and source-code ZIP are submitted separately on CAMU as required by the assignment.
