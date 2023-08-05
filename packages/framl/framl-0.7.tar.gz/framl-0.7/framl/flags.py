import time
import warnings
from google.cloud import firestore
from google.cloud.firestore_v1 import ArrayUnion
from framl.config import Config


class Flags:

    def __init__(self, config: Config):

        # config params
        self.config_ob = config
        self._load_config()
        self.env = config.get_env()
        self.model_name = config.model_name
        self.authorized_flags: list
        self.location: str
        self.refresh_rate: int = 0
        self.default_values: dict

        # lifecycle
        self.flags: dict = {}

        # remote flags configuration
        if self.location == "remote":
            self.fs_client = firestore.Client(project=config.gcp_project_id)
            self.fs_doc = self.fs_client.collection(self.model_name).document(self.env)
            self.last_reload: int = 0
            self.load_flags()

    def _load_config(self):
        config_params = self.config_ob.get_flags()

        if not Config.get_key('options', config_params):
            raise Exception(f'Invalid flags "options" configuration. Check your config.yaml')

        if not Config.value_match(['remote', 'local'], 'options.location', config_params):
            raise Exception(f'Invalid flags location. Can be "remote" or "local". Check your config.yaml')

        if config_params["options"]["location"] == "remote" and "refresh_rate" not in config_params["options"]:
            raise Exception(f"Remote flags need to have a refresh rate. Check your config.yaml")

        if not Config.get_key('flags', config_params):
            raise Exception(f'You need to declare flags. Check your config.yaml')

        if len(config_params['flags']) <= 0 or not isinstance(config_params['flags'], dict):
            raise Exception(f"Wrong flag declaration: "
                            f"{config_params['flags']}, make sure you're using a dict. Check your config.yaml")

        self.refresh_rate = config_params["options"]["refresh_rate"]
        self.location = config_params["options"]["location"]
        self.authorized_flags = list(config_params["flags"].keys())
        self.default_values = config_params["flags"]
        if self.location == 'local':
            self.flags = config_params["flags"]

    def load_flags(self):
        if self.location != "remote":
            raise Exception("You can't reload flags with a local declaration")

        self.last_reload = int(time.time())
        res = self.fs_doc.get().to_dict()
        if not res or "flags" not in res:
            return {}
            raise Exception(f"Can't find any remote flags for {self.model_name} model in {self.env} environment")

        last_flags = res['flags'][-1]
        validity: bool = self._validate_remote_flags(last_flags)
        if validity is True:
            self.flags = last_flags

    def _validate_remote_flags(self, flags) -> bool:
        for mandatory_flag in self.authorized_flags:
            if mandatory_flag not in flags:
                warnings.warn(f'Loaded an undeclared flag from remote: {mandatory_flag}')
                return False

        return True

    def get(self, name: str):
        if int(time.time()) - self.last_reload > self.refresh_rate \
                and self.location == 'remote':
            self.load_flags()

        if name not in self.flags:
            return None

        return self.flags.get(name)

    def set(self, name: str, value) -> None:
        if name not in self.flags:
            raise Exception( f'Flag {name} does not exit. Please declare it first in config.yaml')

        self.flags[name] = value

    def save(self) -> None:
        if self.flags == {}:
            self.flags = self.default_values

        # if there is no doc for the env we need to create it
        if not self.fs_doc.get().to_dict():
            self.fs_doc.set({u'flags': [self.flags]}, merge=False)
        else:
             self.fs_doc.update({u'flags': ArrayUnion([self.flags])})

    def compare_current_with_config(self):
        dec = self.authorized_flags
        print(dec)
        cur = list(self.flags.keys())
        print(cur)
        all_flags = dec + list(set(cur) - set(dec))
        res = []
        for flag in all_flags:
            if flag in dec and flag in cur:
                value = self.flags[flag]
                line = [flag,flag, value,' ']
            elif flag in dec:
                value = self.default_values[flag]
                line = [flag, '', value, '+']
            elif flag in cur:
                value = self.flags[flag]
                line = ['', flag, value, '-']
            else:
                raise Exception( f'{flag} not supported in {all_flags}')
            res.append(line)

        return res
