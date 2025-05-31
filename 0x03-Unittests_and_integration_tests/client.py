#!/usr/bin/env python3
"""Client module"""

import requests
from typing import Dict, List
from utils import get_json, memoize


class GithubOrgClient:
    """GitHub organization client"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str):
        self.org_name = org_name

    @memoize
    def org(self) -> Dict:
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        return self.org.get("repos_url")

    def public_repos(self, license: str = None) -> List[str]:
        repo_list = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repo_list]
        return [
            repo["name"]
            for repo in repo_list
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        try:
            return repo["license"]["key"] == license_key
        except Exception:
            return False
