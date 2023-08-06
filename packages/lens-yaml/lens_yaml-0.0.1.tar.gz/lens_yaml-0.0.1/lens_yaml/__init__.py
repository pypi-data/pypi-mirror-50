import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pygments.lexers.data import YamlLexer

from lens.parsers.base import LensParser

class Parser(LensParser):
    lexer = YamlLexer

    def treat(self, inpt, keys):
        loaded = yaml.load(bytes(inpt, "utf-8"), Loader=Loader)

        for key in keys:
            loaded = loaded[key]

        return yaml.dump(loaded, Dumper=Dumper, explicit_start=True)
