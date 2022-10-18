from unittest import TestCase
from unittest.mock import patch, mock_open
from numpy import int64

from main import BanksInfo, ensure_and_get_bin

class TestMethods(TestCase):
    def test_ensure_and_get_bin(self):
        self.assertIsNone(ensure_and_get_bin('some_str_of_length_20'))
        self.assertIsNone(ensure_and_get_bin('123'))
        self.assertIsNone(ensure_and_get_bin('123456789012345678901'))
        self.assertIsNone(ensure_and_get_bin('123456789012345'))
        self.assertEqual(ensure_and_get_bin('1234567890123456'), int64(123456))
        self.assertEqual(ensure_and_get_bin('123456789012345678'), int64(123456))

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="bin,data\n123456,test_data"
    )
    def test_banks_info(self, mock_file):
        banks_info = BanksInfo("some_filename")
        self.assertEqual(
            banks_info.get_info_json_by_bin(int64(123456)),
            '[{"index":0,"bin":123456,"data":"test_data"}]'
        )
        self.assertEqual(
            banks_info.get_info_json_by_bin(int64(111111)),
            '[]'
        )
