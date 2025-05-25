from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode


class ConfigurationErrorCorrectingCodeManager:
    _configuration = None

    @classmethod
    def get_configuration(cls) -> ConfigurationErrorCorrectingCode:
        if cls._configuration is None:
            cls._configuration = ConfigurationErrorCorrectingCode()
        return cls._configuration
