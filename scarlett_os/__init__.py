# -*- coding: utf-8 -*-


from __future__ import absolute_import

# from . import api
# from . import processor
#
# from .processor import Processor, get_processor, list_processors
# from .component import implements, interfacedoc, abstract

__author__ = 'Malcolm Jones'
__email__ = 'bossjones@theblacktonystark.com'
__version__ = '0.1.0'


# source: timeside

from .tools import package as ts_package

# Check Availability of Gstreamer python bindings
ts_package.check_gi()

# Check Availability of sphinxbase, pocketsphinx, gst-plugins-espeak
# _WITH_SPHINXBASE = ts_package.check_sphinxbase()
# _WITH_POCKETSPHINX = ts_package.check_pocketsphinx()
# _WITH_GST_ESPEAK = ts_package.check_gst_espeak()

# __all__ = ['api', 'processor']

# ts_package.discover_modules('plugins', 'scarlett_os') #__name__)

# Clean-up
del ts_package
del absolute_import
