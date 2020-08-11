import re


def _build_pattern_from_list(lst: list, group_name: str) -> str:
    escaped_list = map(re.escape, lst)
    escaped_list = map(lambda x: r'\b' + x + r'\b', escaped_list)
    return r'(?P<' + group_name + '>' + '|'.join(escaped_list) + ')'

