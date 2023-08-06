import pkg_resources

from .eth_tools import EthTools

__version__ = pkg_resources.get_distribution("ethtools").version
__all__ = [
    "__version__",
    "EthTools",
]