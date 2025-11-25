from cirq_experiments.scripts.analyzer import Analyzer
from cirq_experiments.scripts.universal_cnot.universal_cnot import UniversalCnot


if __name__ == '__main__':
    Analyzer(file=__file__, was_successful=UniversalCnot.was_successful).analyze()
