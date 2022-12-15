try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

try:
    __version__ = version("xfftspy")
except:
    __version__ = "0.0.0"


from .data_consumer import data_consumer
from .udp_client import udp_client


