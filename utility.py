"""
utility.py

Simple utility functions. These functions behavior are simple enough
the name explains the behavior. Including these in sim.py would clutter
the code.
"""
import os


def get_unique_filename(filepath):
    """
    If filepath exists, append a number to make it unique.
    Example: file.txt -> file_1.txt -> file_2.txt, etc.
    """
    if not os.path.exists(filepath):
        return filepath

    # Split into base name and extension
    base, ext = os.path.splitext(filepath)

    counter = 1
    while True:
        new_filepath = f"{base}_{counter}{ext}"
        if not os.path.exists(new_filepath):
            return new_filepath
        counter += 1
