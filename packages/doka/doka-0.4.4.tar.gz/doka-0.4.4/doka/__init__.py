import fire
from doka.commands import *

__version__ = "0.4.3"


def main():
    fire.Fire({
        'version': __version__,
        'project': Project,
        'unit': Unit,
        "stack": Stack,
        "inspect": Inspect,
        "portainer": Portainer,
        "config": Config,
        "nginx": Nginx
    })
