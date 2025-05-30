#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient
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
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
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
    
    """Unit tests for the `memoize` decorator defined in utils.py."""

    def test_memoize(self):
        """
        Test that the `memoize` decorator caches the result of a method.

        The test defines a class with:
        - a method `a_method()` returning a constant value (42),
        - a memoized property `a_property()` which wraps the method call.

        The test checks that:
        - `a_property` returns the correct result,
        - `a_method` is called only once even though `a_property` is accessed twice.
        """

        class TestClass:
            """Test class to demonstrate memoization behavior."""

            def a_method(self):
                """Return a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """Return result of a_method (memoized)."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            # First access: triggers the actual method call
            self.assertEqual(obj.a_property, 42)
            # Second access: should return cached result, not call the method again
            self.assertEqual(obj.a_property, 42)
            # Ensure the method was called exactly once
            mock_method.assert_called_once()



class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of names"""
        test_payload = [
            {'name': 'repo1'},
            {'name': 'repo2'},
            {'name': 'repo3'}
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            client = GithubOrgClient("test_org")

            result = client.public_repos()
            expected = ['repo1', 'repo2', 'repo3']
            self.assertEqual(result, expected)

            # Ensure the mocks were called exactly once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")


if __name__ == "__main__":
    unittest.main()