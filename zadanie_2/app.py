import re
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Sequence

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+\.[a-zA-Z0-9_-]+$")


def is_correct_email(email: str) -> bool:
    """
    Validate given email with a simplified regex: `*@*.*`
    """
    if not isinstance(email, str):
        raise TypeError("Email must be a string")

    return re.match(EMAIL_REGEX, email.strip()) is not None


def compute_rectangle_area(width: int | float, height: int | float) -> float:
    """
    Compute the area of a rectangle with given width and height.
    """
    if not isinstance(width, (int, float)) or not isinstance(height, (int, float)):
        raise TypeError("Width and height must be integers or floats")

    if width < 0 or height < 0:
        raise ValueError("Width and height must be positive")

    return float(width * height)


def process_sequence(sequence: Sequence[int]) -> list[int]:
    """
    Dummy processing: remove odd integers from the `sequence` and return it sorted.
    """
    if not isinstance(sequence, Sequence):
        raise TypeError(
            "Processed list must be a valid Sequence (list, tuple, set, ...)"
        )

    if not all(map(lambda n: isinstance(n, int), sequence)):
        raise TypeError("Processed list must be a sequence of integers")

    even_only = [n for n in sequence if n % 2 == 0]
    return list(sorted(even_only))


def convert_datetime(
    date: str, input_format: str = "%Y-%m-%d", output_format: str = "%Y-%m-%d"
) -> str:
    """
    Convert the given `date` to `output_format` using `input_format` to parse it.
    Will raise a value error if either format is invalid.
    """
    # do not catch the exception if it occurs - we want this to error in that case
    return datetime.strptime(date, input_format).strftime(output_format)


def is_palindrome(text: str) -> bool:
    """
    Validate whether `text` is palindrome or not, case and whitespace insensitive.
    """
    text = text.replace(" ", "").lower()
    return text[::-1] == text


def write_file(path: PathLike[str] | Path, contents: str) -> None:
    if not isinstance(path, Path):
        path = Path(path)

    path.write_text(contents)
