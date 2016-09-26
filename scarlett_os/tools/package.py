# -*- coding: utf-8 -*-

from importlib import import_module
import warnings


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


def get_uniq_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def add_gi_packages():
    import os
    import sys
    from distutils.sysconfig import get_python_lib
    import itertools

    dest_dir = get_python_lib()

    packages = ['gi']

    python_version = sys.version[:3]
    global_path = os.path.join('/usr/lib', 'python' + python_version)

    if os.environ.get('PYTHONPATH'):
        py_path = os.environ.get('PYTHONPATH')
        py_paths = py_path.split(':')

    global_sitepackages = [os.path.join(global_path,
                                        'dist-packages'),  # for Debian-based
                           os.path.join(global_path,
                                        'site-packages')]  # for others

    all_package_paths = [py_paths, global_sitepackages]
    package_list_with_dups = list(itertools.chain.from_iterable(all_package_paths))
    uniq_package_list = get_uniq_list(package_list_with_dups)

    print('dest_dir', dest_dir)
    print('packages', packages)
    print('python_version', python_version)
    print('global_path', global_path)
    print('global_sitepackages', global_sitepackages)
    print('all_package_paths', all_package_paths)
    print('package_list_with_dups', package_list_with_dups)
    print('uniq_package_list', uniq_package_list)

    for package in packages:
        for pack_dir in uniq_package_list:
            src = os.path.join(pack_dir, package)
            dest = os.path.join(dest_dir, package)
            print('src', src)
            print('dest', dest)
            if not os.path.exists(dest) and os.path.exists(src):
                os.symlink(src, dest)
                print('symlink made')


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
