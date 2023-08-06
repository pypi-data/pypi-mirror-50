from docshund import Docshund
import unittest


TEST_FILE = '''

class Blah:
    """
    This is a class.
    """

    def __init__(self):
        """
        Create a new Blah.

        Endow it with all of the qualities that a good Blah should
        have, and then set it free.
        """
        pass

    def engage(self, friend=None):
        """
        Engage the blah to a friend.

        Arguments:
            friend (Blah: None): The friend to whom this Blah should be engaged

        Returns:
            Blah: The new combined blah
        """
        pass

'''


class TestDocshund(unittest.TestCase):
    def test_clean_linebreaks(self):
        ds = """\
        This is a docstring.

        Here is a long description that
        spans many lines.
        """

        D = Docshund()
        self.assertEqual(
            D._clean_docstring(ds),
            [
                "This is a docstring.",
                "",
                "Here is a long description that spans many lines.",
                "",
            ],
        )

    def test_description_only_docstring(self):
        ds = """\
        This is a single-line description.

        It even spans multiple lines, which is great. I
        love that.

        But there's another part.

        Arguments:
            test (int: 1): Frogs!
        """

        D = Docshund()
        self.assertEqual(
            D.parse_docstring(ds),
            "This is a single-line description.\n"
            "\n"
            "It even spans multiple lines, which is great. I love that.\n"
            "\n"
            "But there's another part.\n"
            "\n"
            "# Arguments\n"
            "\t- test (`int`: `1`): Frogs!\n",
        )

    def test_parse_document(self):
        D = Docshund()
        parsed_doc = D.parse_document(TEST_FILE)
        self.assertIn("Create a new Blah", parsed_doc)
