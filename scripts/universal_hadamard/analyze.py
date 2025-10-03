from scripts.analyzer import Analyzer
from scripts.universal_hadamard.universal_hadamard import UniversalHadamard

if __name__ == '__main__':
    Analyzer(filepath=__file__, was_successful=UniversalHadamard.was_successful).analyze()
