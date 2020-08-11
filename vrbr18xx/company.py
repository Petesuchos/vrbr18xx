class OpenCompanies(object):
    def __init__(self):
        self.open_companies = {}

    def par(self, company_name: str, price: int):
        if company_name in self.open_companies.keys():
            raise ValueError('Cannot par an already opened company.')

        if price < 0:
            raise ValueError('Price cannot be a negative quantity.')

        self.open_companies[company_name] = price

    def set_price(self, company_name: str, new_price: int):
        if company_name not in self.open_companies.keys():
            raise ValueError('Cannot change share price of company that is not open.')

        if new_price < 0:
            raise ValueError('Price cannot be a negative value.')

        self.open_companies[company_name] = new_price

    def __getattr__(self, company_name):
        return self.open_companies[company_name]

    def __getitem__(self, company_name):
        return self.open_companies[company_name]

    def __contains__(self, company_name):
        return company_name in self.open_companies
