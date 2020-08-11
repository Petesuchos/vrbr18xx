class Player(object):

    def __init__(self, name: str, initial_cash: int):
        self.name = name
        self.cash = initial_cash
        self.shares = {}
        self.valuation = {}

    def buy_shares(self, company_name: str, price: int, quantity: int = 1):
        if company_name in self.shares:
            self.shares[company_name] += quantity
        else:
            self.shares[company_name] = quantity
        self.cash -= price * quantity

    def sell_shares(self, company_name: str, price: int, quantity: int = 1):
        if company_name not in self.shares:
            raise ValueError(f'Cannot sell a company that a player do not own {company_name}')
        if quantity > self.shares[company_name]:
            raise ValueError(f'Cannot sell more shares ({quantity}) than a player have ({self.shares[company_name]}).')
        self.shares[company_name] -= quantity
        self.cash += price * quantity

    def store_valuation(self, round_phase: str, valuation: int):
        self.valuation[round_phase] = valuation

    def __getattr__(self, company_name):
        return self.shares[company_name]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.name == other.name
        )

    def __contains__(self, company_name):
        return company_name in self.shares
