"""
Utility module - shared helper functions for input validation
and formatting used across the Lost and Found Management System.
"""


def validate_input(data, required_fields):
    """
    Checks that all required fields are present and non-empty
    in the given data dictionary. Raises ValueError if not.
    """
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return True


def is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""


def format_item_summary(item_dict):
    """Returns a short, readable one-line summary of an item."""
    return (
        f"[{item_dict.get('item_id')}] "
        f"{item_dict.get('category', 'Unknown')} - "
        f"{item_dict.get('description', 'No description')} "
        f"({item_dict.get('status', 'unknown')})"
    )


def normalize_text(text):
    """Lowercases and strips whitespace for consistent comparisons."""
    return text.strip().lower() if isinstance(text, str) else text
