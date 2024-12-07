import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../solution"))
)

from logic import create_csv_report, gel_alphabet, get_count_animals_by_letter


class TestLogic(unittest.IsolatedAsyncioTestCase):

    @patch("logic.get_page_data")
    async def test_gel_alphabet_success(self, mock_get_page_data):
        mock_get_page_data.return_value = "<html><ul><li>A</li><li>B</li></ul></html>"

        with patch("logic.BeautifulSoup") as MockSoup:
            mock_soup = MagicMock()
            MockSoup.return_value = mock_soup
            mock_soup.select.return_value = [MagicMock(text="A"), MagicMock(text="B")]

            result = await gel_alphabet()
            self.assertEqual(result, ["A", "B"])

    @patch("logic.get_page_data")
    async def test_gel_alphabet_no_data(self, mock_get_page_data):
        mock_get_page_data.return_value = "<html></html>"

        with patch("logic.BeautifulSoup") as MockSoup:
            mock_soup = MagicMock()
            MockSoup.return_value = mock_soup
            mock_soup.select.return_value = []

            with self.assertRaises(ValueError) as context:
                await gel_alphabet()
            self.assertIn("Не удалось извлечь буквы", str(context.exception))

    @patch("logic.gel_alphabet")
    @patch("logic.get_page_data")
    async def test_get_count_animals_by_letter_success(
        self, mock_get_page_data, mock_gel_alphabet
    ):
        mock_gel_alphabet.return_value = ["A", "B"]

        mock_get_page_data.side_effect = [
            """
            <html>
                <div class="mw-category mw-category-columns">
                    <h3>A</h3>
                    <ul>
                        <li>Animal1</li>
                        <li>Animal2</li>
                    </ul>
                    <h3>B</h3>
                    <ul>
                        <li>Animal3</li>
                    </ul>
                </div>
                <div id="mw-pages">
                    <a href="/next_page">Следующая страница</a>
                </div>
            </html>
            """,
            """
            <html>
                <div class="mw-category mw-category-columns">
                    <h3>B</h3>
                    <ul>
                        <li>Animal4</li>
                    </ul>
                </div>
            </html>
            """,
        ]

        result = await get_count_animals_by_letter()
        print(result)
        self.assertEqual(result, {"A": 2, "B": 2})

    @patch("logic.gel_alphabet")
    @patch("logic.get_page_data")
    async def test_get_count_animals_by_letter_no_animals(
        self, mock_get_page_data, mock_gel_alphabet
    ):
        mock_gel_alphabet.return_value = ["A"]

        mock_get_page_data.return_value = """
            <html>
                <div class='mw-category mw-category-columns'>
                    <h3>A</h3>
                    <ul></ul>
                </div>
            </html>
        """

        result = await get_count_animals_by_letter()
        self.assertEqual(result, {"A": 0})

    def test_create_csv_report_success(self):
        test_data = {"A": 5, "B": 3}
        file_name = "test_report.csv"

        create_csv_report(test_data, file_name)
        self.assertTrue(os.path.exists(file_name))

        with open(file_name, "r") as f:
            content = f.read()
        self.assertIn("A,5", content)
        self.assertIn("B,3", content)

        os.remove(file_name)

    def test_create_csv_report_failure(self):
        test_data = {"A": 5, "B": 3}
        file_name = "/invalid_path/test_report.csv"
        with self.assertRaises(Exception) as context:
            create_csv_report(test_data, file_name)
        self.assertIn("Не удалось сохранить CSV-файл", str(context.exception))


if __name__ == "__main__":
    unittest.main()
