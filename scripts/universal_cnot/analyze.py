from scripts.analyzer import Analyzer
from scripts.universal_cnot.universal_cnot import UniversalCnot


if __name__ == '__main__':
    Analyzer(file=__file__, was_successful=UniversalCnot.was_successful).analyze()
