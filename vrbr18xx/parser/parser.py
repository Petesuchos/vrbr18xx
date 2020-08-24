import re


class Match:
    def __init__(self, action: str, results: dict, sentence: str):
        self.action = action
        self.results = results
        self.sentence = sentence


class SentenceMatcher:
    def __init__(self, pattern: str, groups: list, action: str, coordinator=None):
        self.pattern = pattern
        self.compiled_regex = re.compile(pattern)
        self.groups = groups
        self.action = action
        self.coordinator = coordinator

    def match(self, sentence: str):
        result = self.compiled_regex.match(sentence)
        if result:
            match = Match(action=self.action,
                          results={group: result.group(group) for group in self.groups},
                          sentence=sentence)
            if self.coordinator is not None:
                self.coordinator.notify(match)
            return match
        return None


class SentenceMatcherFabric:
    def __init__(self, interpreter_coordinator=None):
        self.interpreter_coordinator = interpreter_coordinator
        self.patterns = {
            'player': r'(?P<player>\w+)',
            'stock_round': r'(?P<stock_round>\d+)',
            'operation_round': r'(?P<operation_round>\d+\.\d+)',
            'corporation': r'(?P<corporation>\bPRR\b|\bNYC\b|\bB\&O\b|\bC\&O\b|\bERIE\b|\bGT\b|\bIC\b)',
            'value': r'\$(?P<value>\d+)',
            'shares': r'(?P<shares>\d{2})\%',
            'number_of_shares': r'(?P<number_of_shares>\d)',
            'no_corporation': r'(?!\bPRR\b|\bNYC\b|\bB\&O\b|\bC\&O\b|\bERIE\b|\bGT\b|\bIC\b)',
            'chat': r'\w+\: ',
            'private': r'(?P<private>\bSteamboat Company\b|\bMichigan Central\b|\bMeat Packing Company\b|\bMail '
                       r'Contract\b|\bMichigan Southern\b|\bOhio \& Indiana\b|\bLake Shore Line\b|\bTunnel Blasting '
                       r'Company\b|\bBig 4\b|\bChicago and Western Indiana\b)'
        }

    def add_player_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['player'] + ' chooses a company',
            groups=['player'],
            action='add_player',
            coordinator=self.interpreter_coordinator
        )

    def stock_round_matcher(self):
        return SentenceMatcher(
            pattern=r'-- Stock Round ' + self.patterns['stock_round'],
            groups=['stock_round'],
            action='stock_round',
            coordinator=self.interpreter_coordinator
        )

    def operation_round_matcher(self):
        return SentenceMatcher(
            pattern=r'-- Operating Round ' + self.patterns['operation_round'],
            groups=['operation_round'],
            action='operation_round',
            coordinator=self.interpreter_coordinator
        )

    def par_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['player'] + ' pars ' + self.patterns['corporation'] + ' at ' + self.patterns['value'],
            groups=['player', 'corporation', 'value'],
            action='par',
            coordinator=self.interpreter_coordinator
        )

    def buy_shares_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['player'] + ' buys a ' +
                    self.patterns['shares'] + ' share of ' +
                    self.patterns['corporation'] + ' .+ ' + self.patterns['value'],
            groups=['player', 'shares', 'corporation', 'value'],
            action='buy_shares',
            coordinator=self.interpreter_coordinator
        )

    def sell_shares_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['player'] + ' sells ' + self.patterns['number_of_shares'] + ' shares? ' +
                    self.patterns['corporation'] + ' and receives ' + self.patterns['value'],
            groups=['player', 'number_of_shares', 'corporation', 'value'],
            action='sell_shares',
            coordinator=self.interpreter_coordinator
        )

    def corporation_price_change_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['corporation'] + r'\'s share price changes from \$\d+ to ' +
                    self.patterns['value'],
            groups=['corporation', 'value'],
            action='corporation_share_price_change',
            coordinator=self.interpreter_coordinator
        )

    def player_receives_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['no_corporation'] +
                    self.patterns['player'] + ' receives ' + self.patterns['value'],
            groups=['player', 'value'],
            action='player_receives',
            coordinator=self.interpreter_coordinator
        )

    def player_buys_private_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['player'] + ' buys ' + self.patterns['private'] + ' for ' + self.patterns['value'],
            groups=['player', 'private', 'value'],
            action='player_buys_private_matcher',
            coordinator=self.interpreter_coordinator
        )

    def player_collects_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['no_corporation'] +
                    self.patterns['player'] + ' collects ' + self.patterns['value'] + ' from ' +
                    self.patterns['private'],
            groups=['player', 'value', 'private'],
            action='player_collects',
            coordinator=self.interpreter_coordinator
        )

    def chat_matcher(self):
        return SentenceMatcher(
            pattern=self.patterns['chat'],
            groups=[],
            action='chat',
            coordinator=self.interpreter_coordinator
        )


class InterpreterCoordinator:

    def __init__(self, game: str):
        self.game = game

    def notify(self, match: Match):
        print(match.action)
        print(match.results.items())
