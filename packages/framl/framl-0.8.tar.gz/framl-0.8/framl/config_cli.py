import os
import yaml
import getpass

from framl.config import Config


class ConfigFraml(Config):
    user_config_path = os.environ['HOME'] + '/.framl'

    def __init__(self):

        self.skeleton_bucket: str
        self.skeleton_name: str
        self.skeleton_tag: str

        # if the user has no config file
        if not os.path.exists(ConfigFraml.user_config_path):
            self._create_user_config()

        self._fc = yaml.safe_load(open(ConfigFraml.user_config_path))

    def _create_user_config(self):
        default = {
            'skeleton':    {
                'bucket': 'framl-skeleton-artifact',
                'name':   'framl-skeleton-artifact',
                'tag':    'latest'
            },
            'environment': getpass.getuser()
        }
        with open(ConfigFraml.user_config_path, 'w') as outfile:
            yaml.dump(default, outfile, default_flow_style=False, sort_keys=False)

    def _load_lib_config(self) -> None:

        requirements = ['skeleton.bucket', 'skeleton.name', 'skeleton.tag']
        if not Config.keys_exist(requirements, self._fc):
            raise Exception(f'Framl config is missing skeleton parameters. Check {ConfigFraml.user_config_path}')

        self.skeleton_bucket = Config.get_key('skeleton.bucket', self._fc)
        self.skeleton_name = Config.get_key('skeleton.name', self._fc)
        self.skeleton_tag = Config.get_key('skeleton.tag', self._fc)

    @staticmethod
    def get_env() -> str:
        conf = yaml.safe_load(open(ConfigFraml.user_config_path))
        if 'FRAML_ENV' in os.environ:
            return os.environ['FRAML_ENV']
        elif "environment" in conf:
            return os.environ['FRAML_ENV']
        else:
            raise Exception(f"Can't determine Framl environment. "
                            f"Please specify it in {ConfigFraml.user_config_path} or as environment variable with 'FRAML_ENV'")
