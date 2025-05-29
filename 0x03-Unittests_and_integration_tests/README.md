# 0x03. Unittests and Integration Tests

## Description

This project focuses on understanding and applying **unit testing**, **integration testing**, **mocking**, and **parameterization** techniques in Python using the `unittest` framework. The tasks emphasize writing clean, effective tests that verify both individual components and the interaction between them, with a particular focus on ensuring that code functions as expected when isolated and integrated.

## Learning Objectives

By the end of this project, you should be able to:

- Explain the difference between **unit** and **integration tests**
- Understand and apply **mocking**, **parameterization**, and **fixtures**
- Use Python’s built-in `unittest` and `unittest.mock` modules
- Mock external calls like **HTTP requests**, **file I/O**, and **database I/O**
- Perform **memoization** testing
- Mock **properties and methods**
- Apply **parameterized tests** with different input scenarios

## Requirements

- Python 3.7
- Ubuntu 18.04 LTS
- Follow `pycodestyle` (PEP8) version 2.5
- All files must be executable and end with a new line
- All modules, classes, and functions must be documented
- All functions and coroutines must be type-annotated

## Setup

To run the tests, use the command:

```bash
$ python3 -m unittest path/to/test_file.py


## Files

- `utils.py` - Contains helper functions like `access_nested_map`, `get_json`, and `memoize`.
- `client.py` - Contains the `GithubOrgClient` class.
- `fixtures.py` - Contains example payloads for integration testing.
- `test_utils.py` - Contains unit tests for utility functions.
- `test_client.py` - Contains unit and integration tests for the GitHub client.
```
