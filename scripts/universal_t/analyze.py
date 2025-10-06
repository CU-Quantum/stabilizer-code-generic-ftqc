from scripts.analyzer import Analyzer
from scripts.universal_t.universal_t import UniversalT

if __name__ == '__main__':
    Analyzer(filepath=__file__, was_successful=UniversalT.was_successful).analyze()
