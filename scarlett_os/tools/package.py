# -*- coding: utf-8 -*-

from importlib import import_module
import warnings

# from ..exceptions import VampImportError


# def discover_modules(subpackage, package=None):
#     import pkgutil
#
#     if package:
#         try:
#             _pkg = import_module('.' + subpackage, package)
#         except ImportError as e:
#             raise e
#     else:
#         _pkg = import_module(subpackage)
#
#     pkg_path = _pkg.__path__
#     pkg_prefix = _pkg.__name__ + '.'
#
#     _list = [import_module_with_exceptions(modname)
#              for importer, modname, ispkg
#              in pkgutil.walk_packages(pkg_path, pkg_prefix)]
#
#     modules_list = [mod for mod in _list if mod is not None]
#     return modules_list


# def import_module_with_exceptions(name, package=None):
#     """Wrapper around importlib.import_module to import TimeSide subpackage
#     and ignoring ImportError if Aubio, Yaafe and Vamp Host are not available"""
#
#     # from timeside.core import _WITH_SPHINXBASE, _WITH_POCKETSPHINX, _WITH_GST_ESPEAK
#
#     # TODO: When we start organizing scarlett_os better again, we should break things into folders/components
#     if name.count('.server.'):
#         # TODO:
#         # Temporary skip all timeside.server submodules before check dependencies
#         return
#     try:
#         import_module(name, package)
#     except VampImportError:
#         # No Vamp Host
#         # if _WITH_VAMP:
#         #     raise VampImportError
#         if True:
#             print(' No Vamp Host')
#         else:
#             # Ignore Vamp ImportError
#             return
#     except ImportError as e:
#         # if str(e).count('yaafelib') and not _WITH_YAAFE:
#         #     # Ignore Yaafe ImportError
#         #     return
#         # elif str(e).count('aubio') and not _WITH_AUBIO:
#         #     # Ignore Aubio ImportError
#         #     return
#         if str(e).count('DJANGO_SETTINGS_MODULE'):
#             # Ignore module requiring DJANGO_SETTINGS_MODULE in environnement
#             return
#         else:
#             print (name, package)
#             raise e
#     return name


# # Check Availability of external Audio feature extraction librairies
# def check_aubio():
#     "Check Aubio availability"
#     try:
#         import aubio
#     except ImportError:
#         warnings.warn('Aubio librairy is not available', ImportWarning,
#                       stacklevel=2)
#         _WITH_AUBIO = False
#     else:
#         _WITH_AUBIO = True
#         del aubio
#
#     return _WITH_AUBIO
#
#
# def check_yaafe():
#     "Check Aubio availability"
#     try:
#         import yaafelib
#     except ImportError:
#         warnings.warn('Yaafe librairy is not available', ImportWarning,
#                       stacklevel=2)
#         _WITH_YAAFE = False
#     else:
#         _WITH_YAAFE = True
#         del yaafelib
#     return _WITH_YAAFE
#
#
# def check_vamp():
#     "Check Vamp host availability"
#
#     try:
#         from timeside.plugins.analyzer.externals import vamp_plugin
#     except VampImportError:
#         warnings.warn('Vamp host is not available', ImportWarning,
#                       stacklevel=2)
#         _WITH_VAMP = False
#     else:
#         _WITH_VAMP = True
#         del vamp_plugin
#
#     return _WITH_VAMP


def add_gstreamer_packages():
    import os
    import sys
    from distutils.sysconfig import get_python_lib

    dest_dir = get_python_lib()

    packages = ['gobject', 'glib', 'pygst', 'pygst.pyc', 'pygst.pth',
                'gst-0.10', 'pygtk.pth', 'pygtk.py', 'pygtk.pyc']

    python_version = sys.version[:3]
    global_path = os.path.join('/usr/lib', 'python' + python_version)
    global_sitepackages = [os.path.join(global_path,
                                        'dist-packages'),  # for Debian-based
                           os.path.join(global_path,
                                        'site-packages')]  # for others

    for package in packages:
        for pack_dir in global_sitepackages:
            src = os.path.join(pack_dir, package)
            dest = os.path.join(dest_dir, package)
            if not os.path.exists(dest) and os.path.exists(src):
                os.symlink(src, dest)


def check_gstreamer():
    try:
        import gobject
        import pygst
    except ImportError:
        add_gstreamer_packages()


def check_gi():
    try:
        import gi
    except ImportError:
        add_gi_packages()


def add_gi_packages():
    import os
    import sys
    from distutils.sysconfig import get_python_lib

    dest_dir = get_python_lib()

    packages = ['gi']

    # packages = ['gobject', 'glib', 'pygst', 'pygst.pyc', 'pygst.pth',
    #             'gst-0.10', 'pygtk.pth', 'pygtk.py', 'pygtk.pyc']
    python_version = sys.version[:3]
    global_path = os.path.join('/usr/lib', 'python' + python_version)
    global_sitepackages = [os.path.join(global_path,
                                        'dist-packages'),  # for Debian-based
                           os.path.join(global_path,
                                        'site-packages')]  # for others

    print('dest_dir', dest_dir)
    print('packages', packages)
    print('python_version', python_version)
    print('global_path', global_path)
    print('global_sitepackages', global_sitepackages)

    for package in packages:
        for pack_dir in global_sitepackages:
            src = os.path.join(pack_dir, package)
            dest = os.path.join(dest_dir, package)
            print('src', src)
            print('dest', dest)
            if not os.path.exists(dest) and os.path.exists(src):
                os.symlink(src, dest)


def create_gi_symlinks():
    import os
    import sys
    verbose = 1
    if not sys.executable.startswith('/usr/bin/python'):
        try:
            import gi
        except ImportError:
            if verbose > 0:
                print('--------------')
            import subprocess
            dirs = ['gi', ]
            imp = 'import os, gi; print(os.path.dirname(os.path.dirname(' \
                'gi.__file__)))'
            src_dir = subprocess.check_output([
                '/usr/bin/{}'.format(os.path.basename(sys.executable)),
                '-c',
                imp,
            ]).strip().decode('unicode_escape')
            for dst_base in sys.path:
                if dst_base.strip():
                    break
            if verbose > 0:
                print('src_dir', src_dir)
            for d in dirs:
                src = os.path.join(src_dir, d)
                dst = os.path.join(dst_base, d)
                if verbose > 1:
                    print('src', src)
                    print('dst', dst)
                if os.path.exists(src) and not os.path.exists(dst):
                    if verbose > 0:
                        print('linking', d, 'to', dst_base)
                    os.symlink(src, dst)

    # if len(sys.argv) > 1 and sys.argv[1] == 'sdist':
    #     assert full_package_name == os.path.abspath(os.path.dirname(
    #         __file__)).split('site-packages' + os.path.sep)[1].replace(
    #         os.path.sep, '.')
