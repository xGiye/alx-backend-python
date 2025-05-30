#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
            
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))
        
        
class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function in utils.py."""

    @parameterized.expand([
        ("example_com", "http://example.com", {"payload": True}),
        ("holberton_io", "http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """
        Test that get_json returns the correct JSON response
        and that requests.get is called with the correct URL.
        """
        # mock_response = Mock()
        # mock_response.json.return_value = test_payload

        # with patch("utils.requests.get",new_callable=PropertyMock, return_value=mock_response) as mock_get:
        #     result = get_json(test_url)
        #     mock_get.assert_called_once_with(test_url)
        #     self.assertEqual(result, test_payload)
        

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator in utils.py."""

    def test_memoize(self):
        """
        Test that memoize caches the result of a method
        so the method is only called once, even on multiple accesses.
        """
        class TestClass:
            def a_method(self):
                """Returns a fixed value (42)."""
                return 42

            @memoize
            def a_property(self):
                """Returns result of a_method, memoized."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock.assert_called_once()