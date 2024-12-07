import sys
import os
import unittest
from unittest.mock import AsyncMock, patch
from aiohttp import ClientError

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../solution"))
)

from async_requests import get_page_data


class TestAsyncRequests(unittest.IsolatedAsyncioTestCase):
    @patch("async_requests.ClientSession")
    async def test_get_page_data_success(self, mock_client_session):
        mock_session = AsyncMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_session.get.return_value.text = AsyncMock(return_value="<html>Test</html>")

        result = await get_page_data("http://example.com")
        self.assertEqual(result, "<html>Test</html>")

    @patch("async_requests.ClientSession")
    async def test_get_page_data_failure(self, mock_client_session):
        mock_session = AsyncMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session
        mock_session.get.side_effect = ClientError("Failed to connect")

        with self.assertRaises(ClientError):
            await get_page_data("http://example.com")


if __name__ == "__main__":
    unittest.main()
