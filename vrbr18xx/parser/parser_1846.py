from vrbr18xx.parser.abstract_base_parser import Parser18xx
import re


class Parser1846(Parser18xx):
    def parse(self, line: str) -> dict:
        pts = {
            'introduce_player': re.compile(self.patterns.introduce_player()),
        }

        for action, compiled in pts.items():
            result = compiled.match(line)
            if result:
                return {'action': action, 'player': result.group('player')}

        return None