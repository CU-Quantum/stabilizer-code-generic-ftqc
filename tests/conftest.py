import pytest

from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


@pytest.fixture(autouse=True)
def reset_configuration():
    ConfigurationErrorCorrectingCodeManager.reset_configuration()
