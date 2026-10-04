def get_book_status(copies):
    """Determine whether the book is available."""
    if copies > 0:
        return "Available"
    else:
        return "Out of Stock"