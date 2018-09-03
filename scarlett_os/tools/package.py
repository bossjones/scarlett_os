# -*- coding: utf-8 -*-

from importlib import import_module
import warnings

# How to deal w/ lazy imports and mocks? Move the import into a function, then mock it!
# NOTE: https://stackoverflow.com/questions/41873928/how-can-i-mock-a-module-that-is-imported-from-a-function-and-not-present-in-sys?rq=1


def get_gi_module():
    import gi

    return gi


def get_os_module():
    import os

    return os


def get_sys_module():
    import sys

    return sys

def get_distutils_module():
    import distutils

    return distutils


def get_distutils_sysconfig_function_get_python_lib():
    distutils = get_distutils_module()
    from distutils.sysconfig import get_python_lib

    return get_python_lib


def get_itertools_module():
    import itertools

    return itertools


def get_subprocess_module():
    import subprocess

    return subprocess


def check_gi():
    try:
        # NOTE: This is a lazy import
        # SOURCE: https://stackoverflow.com/questions/128478/should-import-statements-always-be-at-the-top-of-a-module
        gi = get_gi_module()
    except ImportError:
        warnings.warn("PyGI library is not available", ImportWarning, stacklevel=2)
        add_gi_packages()


def get_uniq_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def add_gi_packages():
    # NOTE: This is a lazy import
    # SOURCE: https://stackoverflow.com/questions/128478/should-import-statements-always-be-at-the-top-of-a-module
    os = get_os_module()
    sys = get_sys_module()
    # NOTE: Keep in mind this guy -
    # https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory
    # from distutils.sysconfig import get_python_lib  # pylint: disable=import-error
    get_python_lib = get_distutils_sysconfig_function_get_python_lib()

    dest_dir = get_python_lib()

    packages = ["gi"]

    # >>> sys.version
    # '3.6.5 (default, Apr 25 2018, 14:22:56) \n[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)]'
    python_version = sys.version[:3]
    # FIXME:
    # USECASES WE NEED TO ACCOUNT FOR
    # 1. brew python
    # 2. ubuntu python
    # 3. fedora python
    # 4. flatpak python
    # 5. jhbuild python
    # 6. pyenv python
    # 7. virtualenvs

    # INFO WE NEED TO USE
    # ---------------------
    # A list of prefixes for site-packages directories
    # In [2]: site.PREFIXES
    # Out[2]: ['/Users/malcolm/.pyenv/versions/3.6.5/envs/jupyter3']

    # Return a list containing all global site-packages directories (and possibly site-python).
    # In [3]: site.getsitepackages()
    # Out[3]: ['/Users/malcolm/.pyenv/versions/3.6.5/envs/jupyter3/lib/python3.6/site-packages']

    # In [4]: site.getuserbase()
    # Out[4]: '/Users/malcolm/.local'

    # In [5]: site.getusersitepackages()
    # Out[5]: '/Users/malcolm/.local/lib/python3.6/site-packages'

    # INFO: A string giving the site-specific directory prefix where the platform-dependent Python files are installed; by default, this is also '/usr/local'. This can be set at build time with the --exec-prefix argument to the configure script. Specifically, all configuration files (e.g. the pyconfig.h header file) are installed in the directory exec_prefix/lib/pythonX.Y/config, and shared library modules are installed in exec_prefix/lib/pythonX.Y/lib-dynload, where X.Y is the version number of Python, for example 3.2.
    # If a virtual environment is in effect, this value will be changed in site.py to point to the virtual environment. The value for the Python installation will still be available, via base_exec_prefix.
    # In[7]: sys.exec_prefix
    # Out[7]: '/Users/malcolm/.pyenv/versions/3.6.5/envs/jupyter3'

    # INFO: Set during Python startup, before site.py is run, to the same value as exec_prefix. If not running in a virtual environment, the values will stay the same; if site.py finds that a virtual environment is in use, the values of prefix and exec_prefix will be changed to point to the virtual environment, whereas base_prefix and base_exec_prefix will remain pointing to the base Python installation (the one which the virtual environment was created from).
    # In [8]: sys.base_exec_prefix
    # Out[8]: '/Users/malcolm/.pyenv/versions/3.6.5'

    # SYSTEM PYTHON ( OSX )
    #  |2.4.2|    hyenatop in ~
    # ○ → python
    # Python 2.7.15 (default, May  1 2018, 16:44:14)
    # [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
    # Type "help", "copyright", "credits" or "license" for more information.
    # >>> import sys
    # >>> import site
    # >>> site.PREFIXES
    # ['/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7']
    # >>>

    # python2
    # sys.path
    # ['', '/usr/local/lib/python2.7/site-packages/_pdbpp_path_hack', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python27.zip', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-old', '/usr/local/Cellar/python@2/2.7.15/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload', '/usr/local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/site-packages/gtk-2.0', '/usr/local/lib/python2.7/site-packages/gtk-2.0']

    # python3
    # ['', '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python36.zip', '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6', '/usr/local/Cellar/python/3.6.5/Frameworks/Python.framework/Versions/3.6/lib/python3.6/lib-dynload', '/usr/local/lib/python3.6/site-packages']

    global_path_system = os.path.join("/usr/lib", "python" + python_version)

    if os.environ.get("PYTHONPATH"):
        # INFO: PYTHONPATH=/usr/local/share/jhbuild/sitecustomize
        # FIXME: This looks prone to error, we should have it default to something sane if PYTHONPATH isn't set 7/3/2018
        py_path = os.environ.get("PYTHONPATH")
        py_paths = py_path.split(":")
    else:
        # else create an empty list
        py_paths = list()

    flatpak_site_packages = get_flatpak_site_packages()
    global_sitepackages = [
        os.path.join(global_path_system, "dist-packages"),  # for Debian-based
        os.path.join(global_path_system, "site-packages"),  # for others
    ]

    all_package_paths = [flatpak_site_packages, py_paths, global_sitepackages]
    package_list_with_dups = create_list_with_dups(all_package_paths)
    uniq_package_list = get_uniq_list(package_list_with_dups)

    print("dest_dir", dest_dir)
    print("packages", packages)
    print("python_version", python_version)
    print("global_path_system", global_path_system)
    print("global_sitepackages", global_sitepackages)
    print("all_package_paths", all_package_paths)
    print("package_list_with_dups", package_list_with_dups)
    print("uniq_package_list", uniq_package_list)
    ##########################################################
    # Example Output
    ##########################################################
    # dest_dir /home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages
    # packages ['gi']
    # python_version 3.5
    # global_path_system /usr/lib/python3.5
    # global_sitepackages ['/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']
    # all_package_paths [['/usr/local/share/jhbuild/sitecustomize'], ['/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']]
    # package_list_with_dups ['/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']
    # uniq_package_list ['/usr/local/share/jhbuild/sitecustomize', '/usr/lib/python3.5/dist-packages', '/usr/lib/python3.5/site-packages']
    # src /usr/local/share/jhbuild/sitecustomize/gi
    # dest /home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/gi
    # src /usr/lib/python3.5/dist-packages/gi
    # dest /home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/gi
    # src /usr/lib/python3.5/site-packages/gi
    # dest /home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/gi
    ##########################################################

    # FIXME: Delete this when we confirm everything works as expected. Moved the symlinking logic into a new function
    # 7/3/2018
    # for package in packages:
    #     for pack_dir in uniq_package_list:
    #         src = os.path.join(pack_dir, package)
    #         dest = os.path.join(dest_dir, package)
    #         print('src', src)
    #         print('dest', dest)
    #         if not os.path.exists(dest) and os.path.exists(src):
    #             os.symlink(src, dest)
    #             print('symlink made')
    create_package_symlinks(packages, uniq_package_list, dest_dir)


def create_package_symlinks(packages, uniq_package_list, dest_dir):
    os = get_os_module()

    for package in packages:
        for pack_dir in uniq_package_list:
            src = os.path.join(pack_dir, package)
            dest = os.path.join(dest_dir, package)
            print("src", src)
            print("dest", dest)
            if not os.path.exists(dest) and os.path.exists(src):
                os.symlink(src, dest)
                print("symlink made")


def create_list_with_dups(all_package_paths):
    itertools = get_itertools_module()

    return list(itertools.chain.from_iterable(all_package_paths))


def get_flatpak_site_packages():
    os = get_os_module()
    sys = get_sys_module()
    if os.environ.get("SCARLETT_OS_FLATPAK_PYTHON_LIBDIR_PATH"):
        return [os.environ.get("SCARLETT_OS_FLATPAK_PYTHON_LIBDIR_PATH")]
    else:
        return [os.path.join("/app/lib/", "python" + sys.version[:3], "site-packages")]


def create_gi_symlinks():
    os = get_os_module()
    sys = get_sys_module()
    verbose = 1
    if not sys.executable.startswith("/usr/bin/python"):
        try:
            gi = get_gi_module()
        except ImportError:
            if verbose > 0:
                print("--------------")
            subprocess = get_subprocess_module()
            dirs = ["gi"]
            imp = "import os, gi; print(os.path.dirname(os.path.dirname(" "gi.__file__)))"

            python_bin = "{}".format(sys.executable)

            src_dir = (
                subprocess.check_output([python_bin, "-c", imp])
                .strip()
                .decode("unicode_escape")
            )
            # NOTE: This is the old implementation
            # 7/3/2018
            # src_dir = subprocess.check_output(['/usr/bin/{}'.format(os.path.basename(sys.executable)),
            #                                    '-c',
            #                                    imp,
            #                                    ]).strip().decode('unicode_escape')
            for dst_base in sys.path:
                if dst_base.strip():
                    print("dst_base", dst_base)
                    break
            if verbose > 0:
                print("src_dir", src_dir)
            for d in dirs:
                src = os.path.join(src_dir, d)
                dst = os.path.join(dst_base, d)
                if verbose > 1:
                    print("src", src)
                    print("dst", dst)
                if os.path.exists(src) and not os.path.exists(dst):
                    if verbose > 0:
                        print("linking", d, "to", dst_base)
                    os.symlink(src, dst)
