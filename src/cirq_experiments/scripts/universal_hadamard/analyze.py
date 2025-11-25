from cirq_experiments.scripts.analyzer import Analyzer
from cirq_experiments.scripts.universal_hadamard.universal_hadamard import UniversalHadamard

if __name__ == '__main__':
    Analyzer(filepath=__file__, was_successful=UniversalHadamard.was_successful).analyze()
