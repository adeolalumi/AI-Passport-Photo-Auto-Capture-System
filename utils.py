from datetime import datetime


def get_timestamp():
    """
    Returns a safe timestamp string for filenames.
    Example: 20260424_143522
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")