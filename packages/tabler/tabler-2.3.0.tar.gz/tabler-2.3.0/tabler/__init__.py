"""
Tabler package.

The tabler package provides the :class:`tabler.Table` class for simple and
intutive accessing, manipulation and writing of tablulated data.

    Basic Usage::

        >>> from tabler import Table
        >>> table = Table('somefile.csv')
        >>> table.open('Path/To/Input_File.csv')
        >>> table[0]['Price']
        '29.99'
        >>> table[0]['Price'] = 15.50
        >>> table[0]['Price']
        '15.5'
        >>> table.write('Path/To/Output_File')
        Writen 3 lines to file Path/To/Output_File.csv

"""

from .__version__ import __title__, __description__, __url__  # NOQA
from .__version__ import __version__, __author__, __author_email__  # NOQA
from .__version__ import __copyright__, __license__  # NOQA

from .table import Table  # NOQA
from .tabletypes import *  # NOQA
from .tohtml import ToHTML  # NOQA

Tabler = Table  # Backwards compatibility with v1.*
