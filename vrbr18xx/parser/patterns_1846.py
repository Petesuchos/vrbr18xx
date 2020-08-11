from vrbr18xx.parser.abstract_base_pattern import Pattern18xx

import importlib.resources as pkg_resources

# __configfile = pkg_resources.open_text(__package__, 'companies_1846.json')
# __config = json.load(__configfile)

# pattern_companies = _build_pattern_from_list(__config['privates'], 'company')
# pattern_railroads = _build_pattern_from_list(__config['railroads'], 'railroad')

# pattern_extract_player = r'(?P<player>\w+) chooses a company'

# pattern_stock_round = r'-- Stock Round (?P<stock_round>\d+)'


class Patterns1846(Pattern18xx):

    def __init__(self):
        self.privates = [
            "Steamboat Company",
            "Michigan Central",
            "Meat Packing Company",
            "Mail Contract",
            "Michigan Southern",
            "Ohio & Indiana",
            "Lake Shore Line",
            "Tunnel Blasting Company",
            "Big 4",
            "Chicago and Western Indiana"
        ]

        self.railroads = [
            "PRR",
            "NYC",
            "B&O",
            "C&O",
            "ERIE",
            "GT",
            "IC"
        ]

    def introduce_player(self):
        return r'(?P<player>\w+) chooses a company'

    def railroad(self):
        return super()._build_pattern_from_list(lst=self.railroads, group_name='railroad')

    def par_company(self):
        pass

    def stock_round(self):
        return r'-- Stock Round (?P<stock_round>\d+)'

    def operation_round(self):
        pass

    def private_companies(self):
        return super()._build_pattern_from_list(lst=self.privates, group_name='private')

