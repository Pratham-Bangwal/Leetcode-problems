"""Reusable functions for the MIET campus library assignment (Milestone 4)."""


def calculate_fine(days_kept, allowed_days, rate=5.0):
    """Calculate an overdue fine; rate is a default/keyword parameter."""
    if days_kept < 0 or allowed_days < 0 or rate < 0:
        raise ValueError("Days and fine rate cannot be negative")
    overdue = max(0, days_kept - allowed_days)
    return round(overdue * rate, 2)


def is_available(book, catalogue):
    """Check a book against the catalogue dictionary passed as an argument."""
    return catalogue.get(book, 0) > 0


def prepare_summary(borrowed_books):
    """Make a readable summary from a collection of borrowed books."""
    return ", ".join(borrowed_books) if borrowed_books else "None"
