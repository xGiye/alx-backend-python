from utils import access_nested_map

nested = {"a": {"b": {"c": 42}}}
path = ["a", "b", "c"]
print("Value from nested map:", access_nested_map(nested, path))  # Output: 42