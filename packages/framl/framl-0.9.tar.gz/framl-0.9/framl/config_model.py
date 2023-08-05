import yaml

from framl.config import Config


class ConfigModel(Config):

    def __init__(self, project_path):
        self._mc = yaml.safe_load(open(project_path + "/config.yaml"))

        # project
        self._gcp_project_id: str = None
        self._model_name: str = None

        # flags
        self._refresh_rate: str = None
        self._declared_flags: list = None

    def _load_main(func):
        def wrapper(self):
            if self._model_name is None:

                # gcp project id
                self._gcp_project_id = Config.get_key('gcp_project_id', self._mc)
                if self._gcp_project_id is None:
                    raise Exception(f'Config file is missing the GCP project ID. Check your config.yaml')

                self._model_name = Config.get_key('name', self._mc)
                if self._model_name is None:
                    raise Exception(f'Config file is missing the algo name. Check your config.yaml')

            return func(self)

        return wrapper

    def _load_flags(func):
        def wrapper(self):
            if self._declared_flags is None:

                if not Config.keys_exist(['flags', 'flags_refresh_rate'], self._mc):
                    raise Exception(f'Invalid flags configuration. Check your config.yaml')


                if len(self._mc['flags']) <= 0 or not isinstance(self._mc['flags'], list):
                    raise Exception(f"Wrong flag declaration: "
                                    f"{self._mc['flags']}, make sure you're using a list. Check your config.yaml")

                self._refresh_rate = Config.get_key('flags_refresh_rate', self._mc)
                self._declared_flags = Config.get_key('flags', self._mc)

            return func(self)

        return wrapper

    def _load_mandatory_params(self):
        pass

    @_load_main
    def get_gcp_project_id(self):
        return self._gcp_project_id

    @_load_main
    def get_model_name(self):
        return self._model_name

    @_load_flags
    def get_refresh_rate(self):
        return self._refresh_rate

    @_load_flags
    def get_declared_flags(self):
        return self._declared_flags
