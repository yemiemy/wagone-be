from django.core.exceptions import ImproperlyConfigured

import json

with open("/etc/wagone_be_config.json") as config_file:
    config = json.load(config_file)

ENV_SETTING = "ENVIRONMENT_SETTING"

current_env = config.get(ENV_SETTING)

if current_env == "PROD":
    from wagone_be.settings.prod import *
elif current_env == "TESTING":
    from wagone_be.settings.testing import *
elif current_env == "DEV":
    from wagone_be.settings.dev import *
else:
    raise ImproperlyConfigured(
        "Set {} environment variable.".format(ENV_SETTING)
    )
