import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch, MagicMock, ANY

from parameterized import parameterized
from zadanie_2.app import (
    is_correct_email,
    compute_rectangle_area,
    process_sequence,
    is_palindrome,
    convert_datetime,
    write_file,
)


class TestIsCorrectEmail(TestCase):
    @parameterized.expand(
        [
            "test@example.com",  # normal email
            "12345@domain.org",  # numbers in email
            "a.kowalski@example.com",  # dots in email
            "a_kowalski@example.com",  # underscore in email
            "test@example.longertld",  # longer TLD
            "test@mail.example.com",  # mail on a subdomain
        ]
    )
    def test_returns_true_for_valid_emails(self, email: str):
        self.assertTrue(is_correct_email(email), f"{email} should be a valid email")

    @parameterized.expand(
        [
            "",  # empty
            "      ",  # whitespace only
            "test",  # no @ sign
            "test@",  # no domain
            "test@example",  # no dot
            "test@example.",  # no TLD
            "ęśąćż@mbank.pl",  # special characters in username
            "test@ęśąćż.com",  # special characters in domain
        ]
    )
    def test_returns_false_for_invalid_emails(self, email: str):
        self.assertFalse(
            is_correct_email(email), f"{email} should not be a valid email"
        )

    @patch("re.match", return_value=())
    def test_strips_whitespace_from_email(self, mock_match: MagicMock):
        self.assertTrue(is_correct_email("   test@example.com   "))
        mock_match.assert_called_once_with(ANY, "test@example.com")

    def test_raises_if_email_is_not_a_string(self):
        with self.assertRaises(TypeError, msg="Email must be a string"):
            is_correct_email(["test@example.com"])  # noqa


class TestComputeRectangleArea(TestCase):
    @parameterized.expand([(2.0, 2.0, 4.0), (2.5, 2, 5.0), (5, 0, 0), (0, 5, 0)])
    def test_returns_correct_area(self, width: int, height: int, expected: float):
        self.assertEqual(compute_rectangle_area(width, height), expected)

    @parameterized.expand(
        [
            (2, 2),
            (1, 2.0),
            (2.0, 1),
            (2.0, 2.0),
        ]
    )
    def test_always_returns_float(self, width, height):
        self.assertIsInstance(compute_rectangle_area(width, height), float)

    @parameterized.expand(
        [("abc", 1), (1, "abc"), ("abc", "abc"), (None, 1), (1, None)]
    )
    def test_raises_if_args_are_not_int_or_float(self, width, height):
        with self.assertRaises(
            TypeError, msg="Width and height must be integers or floats"
        ):
            compute_rectangle_area(width, height)

    @parameterized.expand([(1, -1), (-1, 1), (1.0, -1.0), (-1.0, 1), (1, -1.0)])
    def test_raises_if_args_are_negative(self, width, height):
        with self.assertRaises(ValueError, msg="Width and height must be positive"):
            compute_rectangle_area(width, height)


class TestProcessList(TestCase):
    @parameterized.expand(
        [
            ([5, 4, 3, 2, 1, 0], [0, 2, 4]),
            ([-5, -4, -3, -2, -1, 0], [-4, -2, 0]),
            ([-2, -1, 0, 1, 2], [-2, 0, 2]),
        ]
    )
    def test_returns_list_sorted_without_odd_numbers(self, sequence, expected):
        self.assertSequenceEqual(process_sequence(sequence), expected)

    @parameterized.expand(["test", {"test": "test"}, 1, 1.0, True, False, None])
    def test_raises_if_argument_is_not_a_sequence(self, input_sequence):
        with self.assertRaises(
            TypeError,
            msg="Processed list must be a valid Sequence (list, tuple, set, ...)",
        ):
            process_sequence(input_sequence)

    @parameterized.expand([[1, 2, 3, "test"], {3, 2, 1, 3.14}, (2, 1, 3, None)])
    def test_raises_if_argument_it_not_a_sequence_of_integers(self, *input_sequence):
        with self.assertRaises(
            TypeError,
            msg="Processed list must be a sequence of integers",
        ):
            process_sequence(input_sequence)


class TestConvertDatetime(TestCase):
    @parameterized.expand(
        [
            ("2024-12-31", "%Y-%m-%d", "%d/%m/%Y", "31/12/2024"),
            ("31/12/2024", "%d/%m/%Y", "%Y-%m-%d", "2024-12-31"),
            ("2024-02-29", "%Y-%m-%d", "%m-%d-%Y", "02-29-2024"),
        ]
    )
    def test_correctly_converts_datetime(
        self, date, input_format, output_format, expected
    ):
        self.assertEqual(convert_datetime(date, input_format, output_format), expected)

    def test_raises_if_date_invalid(self):
        with self.assertRaises(ValueError):
            convert_datetime("2024-12-40", "%Y-%m-%d", "%d/%m/%Y")

    def test_raises_if_input_format_invalid(self):
        with self.assertRaises(ValueError):
            convert_datetime("2024-12-40", "invalid", "%d/%m/%Y")

    def test_raises_if_output_format_invalid(self):
        with self.assertRaises(ValueError):
            convert_datetime("2024-12-40", "%Y-%m-%d", "invalid")


class TestIsPalindrome(TestCase):
    @parameterized.expand(
        [
            "abba",
            "ala",
            "kajak",
        ]
    )
    def test_returns_true_if_text_is_a_palindrome(self, text):
        self.assertTrue(is_palindrome(text))

    @parameterized.expand(["test", "hello", "world"])
    def test_returns_false_if_text_is_not_a_palindrome(self, text):
        self.assertFalse(is_palindrome(text))

    def test_removes_whitespace_before_checking(self):
        self.assertTrue(is_palindrome("race car"))

    def test_checks_in_a_case_insensitive_way(self):
        self.assertTrue(is_palindrome("Kajak"))


class TestWriteFile(TestCase):
    def setUp(self):
        # create a temporary file for writing
        self.out_file = NamedTemporaryFile()

    def tearDown(self):
        # close the file handle, in case of temporary file will also delete the file
        self.out_file.close()

    def test_writes_contents_to_file(self):
        test_content = "test test test test test"
        ret = write_file(self.out_file.name, test_content)
        self.assertIsNone(ret)

        content = Path(self.out_file.name).read_text()
        self.assertEqual(content, test_content)


if __name__ == "__main__":
    unittest.main()
