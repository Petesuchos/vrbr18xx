import re
from abc import ABC, abstractmethod


class Pattern18xx(ABC):

    def _build_pattern_from_list(self, lst: list, group_name: str) -> str:
        escaped_list = map(re.escape, lst)
        escaped_list = map(lambda x: r'\b' + x + r'\b', escaped_list)
        return r'(?P<' + group_name + '>' + '|'.join(escaped_list) + ')'

    @abstractmethod
    def introduce_player(self):
        pass

    @abstractmethod
    def par_company(self):
        pass

    @abstractmethod
    def stock_round(self):
        pass

    @abstractmethod
    def operation_round(self):
        pass

    @abstractmethod
    def railroad(self):
        pass

    @abstractmethod
    def private_companies(self):
        pass

    # Todo: buy, sell shares