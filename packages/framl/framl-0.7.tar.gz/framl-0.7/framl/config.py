import os
from typing import Union
import getpass
import yaml

class Config:

    def __init__(self, project_path):
        # cli params
        self.project_path = project_path
        self.user_config_path = os.environ['HOME'] + '/.framl'
        self._load_lib_config()
        self.skeleton_bucket: str
        self.skeleton_name: str
        self.skeleton_tag: str

        # project params
        self.project_params: dict = None
        self.gcp_project_id: str
        self.model_name: str
        self.env: str

    def _create_user_config(self):
        default = {
            'skeleton': {
                'bucket': 'framl-skeleton-artifact',
                'name': 'framl-skeleton-artifact',
                'tag': 'latest'
            },
            'environment': getpass.getuser()
        }

        with open(self.user_config_path, 'w') as outfile:
            yaml.dump(default, outfile, default_flow_style=False, sort_keys=False)

    def _load_lib_config(self) -> None:

        # if the user has no config file
        if not os.path.exists(self.user_config_path):
            self._create_user_config()

        config = yaml.safe_load(open(self.user_config_path))

        requirements = ['skeleton.bucket', 'skeleton.name', 'skeleton.tag']
        if not Config.keys_exist( requirements, config ):
            raise Exception( f'Cli config file is missing skeleton parameters')

        self.skeleton_bucket = config['skeleton']['bucket']
        self.skeleton_name = config['skeleton']['name']
        self.skeleton_tag = config['skeleton']['tag']
        self.env = os.environ['FRAML_ENV'] if 'FRAML_ENV' in os.environ else config['environment']

    def _load_project_config(func):
        def wrapper(self):
            if self.project_params is None:
                config = yaml.safe_load(open(self.project_path + '/config.yaml'))
                if 'name' not in config:
                    raise Exception(f'Config file is missing the algo name')
                if 'gcp_project_id' not in config:
                    raise Exception(f'Config file is missing the GCP project ID')
                self.project_params = config
                self.gcp_project_id = config['gcp_project_id']
                self.model_name = config['name']

            return func(self)
        return wrapper

    @_load_project_config
    def load_project_config(self):
        pass

    def get_env(self):
        return 'production'

    @_load_project_config
    def get_model_name(self):
        return self.model_name

    @_load_project_config
    def get_flags(self):
        if 'flags' not in self.project_params:
            raise Exception( f'No flags configuration in {self.project_path}/config.yaml')

        return self.project_params['flags']

    @staticmethod
    def keys_exist(needles: list, haystack: dict) -> bool:
        for key in needles:
            if not Config.get_key(key, haystack):
                return False
        return True

    @staticmethod
    def get_key(needle: str, haystack: dict) -> Union[bool, str, int]:
        pieces = needle.split('.')
        for piece in pieces:
            if piece not in haystack:
                return False
            haystack = haystack[piece]
        return haystack

    @staticmethod
    def value_match( needles: list, key:str, haystack: dict ) -> bool:
        value = Config.get_key(key, haystack)
        if not value:
            return False

        if value not in needles:
            return False

        return True
