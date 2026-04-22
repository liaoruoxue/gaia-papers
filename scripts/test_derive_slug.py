import unittest

from derive_slug import derive_slug


class DeriveSlugTests(unittest.TestCase):
    def test_simple_pdf(self):
        self.assertEqual(derive_slug("attention.pdf"), "attention")

    def test_spaces_and_capitals(self):
        self.assertEqual(
            derive_slug("Attention Is All You Need.pdf"),
            "attention-is-all-you-need",
        )

    def test_runs_of_non_alnum_collapse(self):
        self.assertEqual(
            derive_slug("Foo  ---  Bar__baz.md"),
            "foo-bar-baz",
        )

    def test_leading_and_trailing_separators_trimmed(self):
        self.assertEqual(derive_slug("---hello---.txt"), "hello")

    def test_unicode_letters_preserved_lowercase(self):
        # Unicode letters are kept (lowercased); non-letters collapse.
        self.assertEqual(derive_slug("Café Noir.pdf"), "café-noir")

    def test_numbers_preserved(self):
        self.assertEqual(derive_slug("GPT-4 Technical Report.pdf"), "gpt-4-technical-report")

    def test_multiple_extensions_only_final_stripped(self):
        # We only strip the final suffix; intermediate dots collapse like any non-alnum.
        self.assertEqual(derive_slug("paper.v2.final.pdf"), "paper-v2-final")

    def test_html_and_txt_extensions(self):
        self.assertEqual(derive_slug("arxiv-2401.00001.html"), "arxiv-2401-00001")
        self.assertEqual(derive_slug("link.txt"), "link")

    def test_empty_stem_raises(self):
        with self.assertRaises(ValueError):
            derive_slug("---.pdf")


if __name__ == "__main__":
    unittest.main()
