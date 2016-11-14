"""Debug module using ipython."""

from __future__ import with_statement, division

import logging
import sys

from IPython.core.debugger import Tracer  # NOQA
from IPython.core import ultratb

sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                     color_scheme='Linux',
                                     call_pdb=True,
                                     ostream=sys.__stdout__)

logger = logging.getLogger(__name__)
