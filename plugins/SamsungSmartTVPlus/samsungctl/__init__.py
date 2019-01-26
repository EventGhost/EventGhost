"""Remote control Samsung televisions via TCP/IP connection"""

__title__ = "samsungctl"
__version__ = "0.7.1+1"
__url__ = "https://github.com/kdschlosser/samsungctl"
__author__ = "Lauri Niskanen, Kevin Schlosser"
__author_email__ = "kevin.g.schlosser@gmail.com"
__license__ = "MIT, GNUv2"


import logging
from logging import NullHandler

logger = logging.getLogger('samsungctl')
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=None)

logger.setLevel(logging.NOTSET)

from .remote import Remote # NOQA
from .config import Config # NOQA
from .discover import discover # NOQA

__all__ = (
    '__title__', '__version__', '__url__', '__author__', '__author_email__',
    '__license__', 'Remote', 'Config', 'discover'
)
