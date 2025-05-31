#!/usr/bin/env python3
# """Unit & integration tests for client.py"""

# import unittest
# from unittest.mock import patch, PropertyMock
# from parameterized import parameterized, parameterized_class
# from client import GithubOrgClient
# from fixtures import TEST_PAYLOAD


# class TestGithubOrgClient(unittest.TestCase):
#     """Unit tests for GithubOrgClient"""

#     @parameterized.expand([
#         ("google",),
#         ("abc",)
#     ])
#     @patch("client.get_json")
#     def test_org(self, org_name, mock_get_json):
#         mock_get_json.return_value = {"login": org_name}
#         client = GithubOrgClient(org_name)
#         self.assertEqual(client.org, {"login": org_name})
#         mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

#     def test_public_repos_url(self):
#         with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
#             mock_org.return_value = {"repos_url": "http://fake-url.com/repos"}
#             client = GithubOrgClient("test")
#             self.assertEqual(client._public_repos_url, "http://fake-url.com/repos")

#     @patch("client.get_json")
#     def test_public_repos(self, mock_get_json):
#         mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
#         with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
#             mock_url.return_value = "http://fake-url.com/repos"
#             client = GithubOrgClient("test")
#             self.assertEqual(client.public_repos(), ["repo1", "repo2"])
#             mock_url.assert_called_once()
#             mock_get_json.assert_called_once()

#     @parameterized.expand([
#         ({"license": {"key": "my_license"}}, "my_license", True),
#         ({"license": {"key": "other_license"}}, "my_license", False),
#     ])
#     def test_has_license(self, repo, license_key, expected):
#         self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


# @parameterized_class(
#     ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
#     [
#         (
#             TEST_PAYLOAD["org_payload"],
#             TEST_PAYLOAD["repos_payload"],
#             TEST_PAYLOAD["expected_repos"],
#             TEST_PAYLOAD["apache2_repos"],
#         )
#     ],
# )
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration test class"""

#     @classmethod
#     def setUpClass(cls):
#         cls.get_patcher = patch("requests.get")
#         mock_get = cls.get_patcher.start()
#         mock_get.side_effect = [
#             Mock(json=lambda: cls.org_payload),
#             Mock(json=lambda: cls.repos_payload)
#         ]

#     @classmethod
#     def tearDownClass(cls):
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         client = GithubOrgClient("google")
#         self.assertEqual(client.public_repos(), self.expected_repos)

#     def test_public_repos_with_license(self):
#         client = GithubOrgClient("google")
#         self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import expand, parameterized_class
from typing import Dict, List, Any
import client
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the GithubOrgClient class.
    """

    @expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        # Define the expected payload for the mocked get_json call
        expected_payload = {"login": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient
        github_client = client.GithubOrgClient(org_name)

        # Call the org method
        result = github_client.org()

        # Assert that get_json was called exactly once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result is the expected payload
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """
        Unit-test GithubOrgClient._public_repos_url property.
        Patches GithubOrgClient.org to return a known payload.
        """
        # Define the mock payload for client.org
        mock_org_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        # Patch GithubOrgClient.org using patch as a context manager
        # new_callable=PropertyMock is essential for mocking properties
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_org_payload

            # Create an instance of GithubOrgClient
            github_client = client.GithubOrgClient("test_org")

            # Access the _public_repos_url property
            # Note: No parentheses because it's a property
            result_url = github_client._public_repos_url

            # Assert that GithubOrgClient.org was called exactly once
            mock_org.assert_called_once()

            # Assert that the returned URL is the expected one
            self.assertEqual(result_url, mock_org_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock):
        """
        Unit-test GithubOrgClient.public_repos.
        Mocks get_json and GithubOrgClient._public_repos_url.
        """
        # Define mock payloads and URLs
        mock_repos_payload = [{"name": "repo1"}, {"name": "repo2", "license": {"key": "mit"}}]
        mock_public_repos_url = "https://mock.url/repos"
        expected_repo_names = ["repo1", "repo2"]

        # Configure the mocked get_json to return our mock_repos_payload
        mock_get_json.return_value = mock_repos_payload

        # Patch GithubOrgClient._public_repos_url as a context manager
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url_prop:
            # Configure the mocked _public_repos_url property
            mock_public_repos_url_prop.return_value = mock_public_repos_url

            # Create an instance of GithubOrgClient
            github_client = client.GithubOrgClient("test_org")

            # Call the public_repos method
            result_repos = github_client.public_repos()

            # Assert that _public_repos_url property was accessed once
            mock_public_repos_url_prop.assert_called_once()

            # Assert that get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(mock_public_repos_url)

            # Assert that the list of repo names is what we expect
            self.assertEqual(result_repos, expected_repo_names)

    @expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False), # Test case for license being None
        ({}, "my_license", False), # Test case for no license key
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected_result: bool):
        """
        Unit-test GithubOrgClient.has_license with parameterized inputs.
        """
        # Call the static method has_license directly from the class
        result = client.GithubOrgClient.has_license(repo, license_key)

        # Assert that the result matches the expected value
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test suite for GithubOrgClient.public_repos.
    Mocks external HTTP requests using fixtures.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up class-level mocks for integration tests.
        Mocks requests.get to return example payloads from fixtures.
        """
        # Create a patcher for client.get_json (as it's used by GithubOrgClient)
        cls.get_patcher = patch('client.get_json')
        cls.mock_get = cls.get_patcher.start()

        def side_effect_func(url: str):
            """
            Custom side effect function to return different payloads
            based on the URL requested by get_json.
            """
            if url == cls.org_payload["url"]:
                # Return the org_payload when the org URL is requested
                return cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                # Return the repos_payload when the repos URL is requested
                return cls.repos_payload
            # Add more conditions if other URLs are expected in future tests
            # For now, raise an error if an unexpected URL is called
            raise ValueError(f"Unexpected URL in mock: {url}")

        # Assign the side effect function to the mocked get_json
        cls.mock_get.side_effect = side_effect_func

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher after all integration tests are done.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test GithubOrgClient.public_repos in an integration setting.
        Verifies that the list of repos matches the expected fixture.
        """
        # Create an instance of GithubOrgClient using the org_payload's login
        github_client = client.GithubOrgClient(self.org_payload["login"])

        # Call the public_repos method
        result_repos = github_client.public_repos()

        # Assert that the returned list of repos matches the expected_repos fixture
        self.assertEqual(result_repos, self.expected_repos)

        # Assert that the mocked get_json was called with the correct URLs
        # We expect two calls: one for org() and one for _public_repos_url
        calls = self.mock_get.call_args_list
        self.assertEqual(len(calls), 2)
        self.mock_get.assert_any_call(self.org_payload["url"])
        self.mock_get.assert_any_call(self.org_payload["repos_url"])

    def test_public_repos_with_license(self):
        """
        Test GithubOrgClient.public_repos and then filter by license.
        This tests the integration of public_repos with has_license.
        """
        # Create an instance of GithubOrgClient
        github_client = client.GithubOrgClient(self.org_payload["login"])

        # Call public_repos to get the list of all repos (mocked via side_effect)
        all_repos = github_client.public_repos()

        # Filter the repos for those with an "apache-2.0" license
        apache2_licensed_repos = [
            repo["name"] for repo in self.repos_payload # Use the raw repos_payload here
            if client.GithubOrgClient.has_license(repo, "apache-2.0")
        ]

        # Assert that the filtered list matches the expected apache2_repos names
        # Note: apache2_repos fixture contains the full repo dicts,
        # so we extract names for comparison with the public_repos output.
        expected_apache2_repo_names = [repo["name"] for repo in self.apache2_repos]
        self.assertEqual(apache2_licensed_repos, expected_apache2_repo_names)

        # Ensure that get_json was called twice for the public_repos call
        self.assertEqual(self.mock_get.call_count, 2)


if __name__ == '__main__':
    unittest.main()