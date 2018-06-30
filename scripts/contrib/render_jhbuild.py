import argparse
import contextlib
import getpass
import os
import re
import shutil
import subprocess
import sys
import errno
import stat
import io
import select
import time

USERNAME = getpass.getuser()
USERHOME = os.path.expanduser("~")
PATH_TO_JHBUILDRC = os.path.join(USERHOME + ".config", "jhbuildrc")
PREFIX = os.path.join(USERHOME, "jhbuild")
CHECKOUTROOT = os.path.join(USERHOME, "gnome")
PROJECT_HOME = os.path.join(USERHOME, "dev")
PY_VERSION = '3.5'
PY_VERSION_FULL = "{}.2".format(PY_VERSION)
JHBUILD_GITHUB_URL = "https://github.com/GNOME/jhbuild.git"
JHBUILD_SHA = "86d958b6778da649b559815c0a0dbe6a5d1a8cd4"
PATH_TO_JHBUILD_BIN = os.path.join(USERHOME + ".local/bin", "jhbuild")

# JHBUILD_TEMPLATE = """
# import os
# prefix='{PREFIX}'
# checkoutroot='{CHECKOUTROOT}'
# moduleset = 'gnome-world'
# interact = False
# makeargs = '-j4'
# os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
# os.environ['PYTHON'] = 'python'
# os.environ['GSTREAMER'] = '1.0'
# os.environ['ENABLE_PYTHON3'] = 'yes'
# os.environ['ENABLE_GTK'] = 'yes'
# os.environ['PYTHON_VERSION'] = '3.5'
# os.environ['MAKEFLAGS'] = '-j4'
# os.environ['PREFIX'] = '{PREFIX}'
# os.environ['JHBUILD'] = '{CHECKOUTROOT}'
# os.environ['PATH'] = '/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/home/pi/.pyenv/shims:~/.pyenv/bin/:~/.bin:/home/pi/.local/bin:/home/pi/.rbenv/shims:/home/pi/.rbenv/bin:/home/pi/.nvm/versions/node/v8.7.0/bin:/usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/pi/.rvm/bin:/home/pi/.go/bin:/home/pi/go/bin'
# os.environ['LD_LIBRARY_PATH'] = '/home/pi/jhbuild/lib:/home/pi/jhbuild/lib:/usr/lib'
# os.environ['PYTHONPATH'] = '/home/pi/.pyenv/versions/3.5.2/lib/python3.5/site-packages:/home/pi/jhbuild/lib/python3.5/site-packages:/usr/lib/python3.5/site-packages'
# os.environ['PKG_CONFIG_PATH'] = '/home/pi/.pyenv/versions/3.5.2/lib/pkgconfig:/home/pi/jhbuild/lib/pkgconfig:/home/pi/jhbuild/share/pkgconfig:/usr/lib/pkgconfig'
# os.environ['XDG_DATA_DIRS'] = '/home/pi/jhbuild/share:/usr/share'
# os.environ['XDG_CONFIG_DIRS'] = '/home/pi/jhbuild/etc/xdg'
# os.environ['CC'] = 'gcc'
# os.environ['PROJECT_HOME'] = '/home/pi/dev'
# os.environ['PYTHONSTARTUP'] = '/home/pi/.pythonrc'
# """

JHBUILD_TEMPLATE = """
import os
prefix='{PREFIX}'
checkoutroot='{CHECKOUTROOT}'
moduleset = 'gnome-world'
interact = False
makeargs = '-j4'
os.environ['CFLAGS'] = '{CFLAGS}'
os.environ['PYTHON'] = 'python'
os.environ['GSTREAMER'] = '1.0'
os.environ['ENABLE_PYTHON3'] = 'yes'
os.environ['ENABLE_GTK'] = 'yes'
os.environ['PYTHON_VERSION'] = '{PYTHON_VERSION}'
os.environ['MAKEFLAGS'] = '-j4'
os.environ['PREFIX'] = '{PREFIX}'
os.environ['JHBUILD'] = '{CHECKOUTROOT}'
os.environ['PATH'] = '{PATH}'
os.environ['LD_LIBRARY_PATH'] = '{LD_LIBRARY_PATH}'
os.environ['PYTHONPATH'] = '{PYTHONPATH}'
os.environ['PKG_CONFIG_PATH'] = '{PKG_CONFIG_PATH}'
os.environ['XDG_DATA_DIRS'] = '{XDG_DATA_DIRS}'
os.environ['XDG_CONFIG_DIRS'] = '{XDG_CONFIG_DIRS}'
os.environ['CC'] = 'gcc'
os.environ['PROJECT_HOME'] = '{PROJECT_HOME}'
os.environ['PYTHONSTARTUP'] = '{PYTHONSTARTUP}'
"""

# SOURCE: https://github.com/ARMmbed/mbed-cli/blob/f168237fabd0e32edcb48e214fc6ce2250046ab3/test/util.py
# Process execution
class ProcessException(Exception):
    pass

class Console:  # pylint: disable=too-few-public-methods

    quiet = False

    @classmethod
    def message(cls, str_format, *args):
        if cls.quiet:
            return

        if args:
            print(str_format % args)
        else:
            print(str_format)

        # Flush so that messages are printed at the right time
        # as we use many subprocesses.
        sys.stdout.flush()

def pquery(command, stdin=None, **kwargs):
    # SOURCE: https://github.com/ARMmbed/mbed-cli/blob/f168237fabd0e32edcb48e214fc6ce2250046ab3/test/util.py
    # Example:
    print(' '.join(command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    stdout, _ = proc.communicate(stdin)

    if proc.returncode != 0:
        raise ProcessException(proc.returncode)

    return stdout.decode("utf-8")

# Directory navigation
@contextlib.contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)

def scm(dir=None):
    if not dir:
        dir = os.getcwd()

    if os.path.isdir(os.path.join(dir, '.git')):
        return 'git'
    elif os.path.isdir(os.path.join(dir, '.hg')):
        return 'hg'

def _popen(cmd_arg):
    devnull = open('/dev/null')
    cmd = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=devnull, shell=True)
    retval = cmd.stdout.read().strip()
    err = cmd.wait()
    cmd.stdout.close()
    devnull.close()
    if err:
        raise RuntimeError('Failed to close %s stream' % cmd_arg)
    return retval

def _popen_stdout(cmd_arg, cwd=None):
    # if passing a single string, either shell mut be True or else the string must simply name the program to be executed without specifying any arguments
    cmd = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, bufsize=4096, shell=True)
    Console.message("BEGIN: {}".format(cmd_arg))
    # output, err = cmd.communicate()

    for line in iter(cmd.stdout.readline, b''):
        # Print line
        _line = line.rstrip()
        Console.message(">>> {}".format(_line.decode("utf-8")))

    Console.message("END: {}".format(cmd_arg))

# Higher level functions
def remove(path):
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, onerror=remove_readonly)

def move(src, dst):
    shutil.move(src, dst)

def copy(src, dst):
    shutil.copytree(src, dst)

def clone_jhbuild():
    # First check if folder exists
    if not os.path.exists(PREFIX):
        # check if folder is a git repo
        if scm(PREFIX) != 'git':
            # nuke folder
            # remove(PREFIX)
            # clone it
            jhbuild_clone_cmd = "git clone {repo} {dest}".format(repo=JHBUILD_GITHUB_URL,
                                                                            dest=PREFIX)
            _popen_stdout(jhbuild_clone_cmd)

            # CD to directory
            with cd(PREFIX):
                jhbuild_checkout_cmd = "git checkout {sha}".format(sha=JHBUILD_SHA)
                _popen_stdout(jhbuild_checkout_cmd)

    return PREFIX

def compile_jhbuild():
    Console.message('First check if folder exists')
    Console.message("if not os.path.exists(PREFIX) = {}".format(PREFIX))
    if os.path.exists(PREFIX):
        Console.message('check if folder is a git repo')
        if scm(PREFIX) == 'git':
            with cd(PREFIX):
                _autogen_cmd = "./autogen.sh --prefix={}/.local".format(USERHOME)
                _popen_stdout(_autogen_cmd, cwd=PREFIX)
                _make_cmd = "make"
                _popen_stdout(_make_cmd, cwd=PREFIX)
                _make_install_cmd = "make install"
                _popen_stdout(_make_install_cmd, cwd=PREFIX)
                _test_jhbuild = "~/.local/bin/jhbuild --help"
                _popen_stdout(_test_jhbuild, cwd=PREFIX)

def whoami():
    whoami = _popen('who')
    return whoami

# Some utility functions used here and in custom files:

def environ_append(key, value, separator=' ', force=False):
    old_value = os.environ.get(key)
    if old_value is not None:
        value = old_value + separator + value
    os.environ[key] = value

def environ_prepend(key, value, separator=' ', force=False):
    old_value = os.environ.get(key)
    if old_value is not None:
        value = value + separator + old_value
    os.environ[key] = value

def environ_remove(key, value, separator=':', force=False):
    old_value = os.environ.get(key)
    if old_value is not None:
        old_value_split = old_value.split(separator)
        value_split = [x for x in old_value_split if x != value]
        value = separator.join(value_split)
    os.environ[key] = value

def environ_set(key, value):
    os.environ[key] = value

def environ_get(key):
    return os.environ.get(key)

def path_append(value):
    if os.path.exists(value):
        environ_append("PATH", value, ":")

def path_prepend(value, force=False):
    if os.path.exists(value):
        environ_prepend("PATH", value, ":", force)

# Call either setup_debug or setup_release in your .jhbuildrc-custom
# or other customization file to get the compilation flags.
def setup_debug():
    environ_set('CFLAGS', '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer')
    environ_set('CXXFLAGS', '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer')
    # environ_prepend('CFLAGS', '-O0 -g')
    # environ_prepend('CXXFLAGS', '-O0 -g')

def setup_path_env():
    # print("before")
    # dump_env_var("PATH")
    # /home/pi/jhbuild/bin
    # /home/pi/jhbuild/sbin
    # /home/pi/jhbuild/bin
    # /home/pi/jhbuild/sbin
    # /home/pi/.pyenv/shims
    # ~/.pyenv/bin/
    # ~/.bin
    # /home/pi/.local/bin
    # /home/pi/.rbenv/shims
    # /home/pi/.rbenv/bin
    # /home/pi/.nvm/versions/node/v8.7.0/bin
    # /usr/lib64/ccache
    # /usr/local/bin
    # /usr/bin
    # /usr/local/sbin
    # /usr/sbin
    # /home/pi/.rvm/bin
    # /home/pi/.go/bin
    # /home/pi/go/bin
    path_prepend("/usr/sbin")
    path_prepend("/usr/local/sbin")
    path_prepend("/usr/bin")
    path_prepend("/usr/local/bin")
    path_prepend("/usr/lib64/ccache")
    path_prepend("{}/.rbenv/bin".format(USERHOME))
    path_prepend("{}/.rbenv/shims".format(USERHOME))
    path_prepend("{}/.local/bin".format(USERHOME))
    path_prepend("{}/.bin".format(USERHOME))
    path_prepend("{}/.pyenv/bin".format(USERHOME), True)
    path_prepend("{}/.pyenv/shims".format(USERHOME), True)
    path_prepend("{}/jhbuild/sbin".format(USERHOME), True)
    path_prepend("{}/jhbuild/bin".format(USERHOME), True)
    Console.message("AFTER")
    dump_env_var("PATH")

def setup_python_version():
    environ_set("PYTHON_VERSION", PY_VERSION)


def setup_ld_library_path():
    # /home/pi/jhbuild/lib
    # /home/pi/jhbuild/lib
    # /usr/lib
    environ_prepend("LD_LIBRARY_PATH", "/usr/lib", ":")
    environ_prepend("LD_LIBRARY_PATH", "{}/jhbuild/lib".format(USERHOME), ":")
    Console.message("AFTER")
    dump_env_var("LD_LIBRARY_PATH")

def setup_pythonpath():
    # /home/pi/.pyenv/versions/3.5.2/lib/python3.5/site-packages
    # /home/pi/jhbuild/lib/python3.5/site-packages
    # /usr/lib/python3.5/site-packages
    environ_prepend("PYTHONPATH", "/usr/lib/python{}/site-packages".format(PY_VERSION), ":")
    environ_prepend("PYTHONPATH", "{}/jhbuild/lib/python{}/site-packages".format(USERHOME, PY_VERSION), ":")
    environ_prepend("PYTHONPATH", "{}/.pyenv/versions/{}/lib/python{}/site-packages".format(USERHOME, PY_VERSION_FULL, PY_VERSION), ":")
    Console.message("AFTER")
    dump_env_var("PYTHONPATH")


def setup_prefix():
    environ_set("PREFIX", PREFIX)
    Console.message("AFTER")
    dump_env_var("PREFIX")

def setup_checkoutroot():
    environ_set("CHECKOUTROOT", CHECKOUTROOT)
    Console.message("AFTER")
    dump_env_var("CHECKOUTROOT")

def setup_pkg_config_path():
    # /home/pi/.pyenv/versions/3.5.2/lib/pkgconfig
    # /home/pi/jhbuild/lib/pkgconfig
    # /home/pi/jhbuild/share/pkgconfig
    # /usr/lib/pkgconfig
    environ_prepend("PKG_CONFIG_PATH", "/usr/lib/pkgconfig", ":")
    environ_prepend("PKG_CONFIG_PATH", "{}/jhbuild/share/pkgconfig".format(USERHOME), ":")
    environ_prepend("PKG_CONFIG_PATH", "{}/jhbuild/lib/pkgconfig".format(USERHOME), ":")
    environ_prepend("PKG_CONFIG_PATH", "{}/.pyenv/versions/{}/lib/pkgconfig".format(USERHOME, PY_VERSION_FULL), ":")
    Console.message("AFTER")
    dump_env_var("PKG_CONFIG_PATH")

def setup_xdg_data_dirs():
    # /home/pi/jhbuild/share
    # /usr/share
    environ_prepend("XDG_DATA_DIRS", "/usr/share", ":")
    environ_prepend("XDG_DATA_DIRS", "{}/jhbuild/share".format(USERHOME), ":")
    Console.message("AFTER")
    dump_env_var("XDG_DATA_DIRS")

def setup_xdg_config_dirs():
    # /home/pi/jhbuild/etc/xdg
    environ_prepend("XDG_CONFIG_DIRS", "{}/jhbuild/etc/xdg".format(USERHOME), ":")
    Console.message("AFTER")
    dump_env_var("XDG_CONFIG_DIRS")

def setup_project_home():
    # /home/pi/dev
    environ_prepend("PROJECT_HOME", "{}/dev".format(USERHOME), ":")
    Console.message("AFTER")
    dump_env_var("PROJECT_HOME")

def setup_pythonstartup():
    # /home/pi/.pythonrc
    environ_prepend("PYTHONSTARTUP", "{}/.pythonrc".format(USERHOME), ":")
    Console.message("AFTER")
    dump_env_var("PYTHONSTARTUP")

def setup_all_envs():
    setup_debug()
    setup_path_env()
    setup_python_version()
    setup_ld_library_path()
    setup_pythonpath()
    setup_pkg_config_path()
    setup_xdg_data_dirs()
    setup_xdg_config_dirs()
    setup_project_home()
    setup_pythonstartup()
    setup_prefix()
    setup_checkoutroot()


def write_jhbuildrc():
    rendered_jhbuild = render_jhbuildrc_dry_run()
    with open(PATH_TO_JHBUILDRC, 'w+') as fp:
        fp.write(rendered_jhbuild)

def render_jhbuildrc_dry_run():
    rendered_jhbuild = JHBUILD_TEMPLATE.format(PREFIX=environ_get('PREFIX'),
                                               CHECKOUTROOT=environ_get('CHECKOUTROOT'),
                                               CFLAGS=environ_get('CFLAGS'),
                                               PYTHON_VERSION=environ_get('PYTHON_VERSION'),
                                               PATH=environ_get('PATH'),
                                               LD_LIBRARY_PATH=environ_get('LD_LIBRARY_PATH'),
                                               PYTHONPATH=environ_get('PYTHONPATH'),
                                               PKG_CONFIG_PATH=environ_get('PKG_CONFIG_PATH'),
                                               XDG_DATA_DIRS=environ_get('XDG_DATA_DIRS'),
                                               XDG_CONFIG_DIRS=environ_get('XDG_CONFIG_DIRS'),
                                               PROJECT_HOME=environ_get('PROJECT_HOME'),
                                               PYTHONSTARTUP=environ_get('PYTHONSTARTUP')
                                              )
    Console.message('----------------[render_jhbuildrc_dry_run]----------------')
    Console.message(rendered_jhbuild)

    return rendered_jhbuild

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def dump_env_var(var):
    Console.message("Env Var:{}={}".format(var, os.environ.get(var, "<EMPTY>")))

def mkdir_user_bin_dirs():
    _local_bin_path = "{}/.local/bin".format(USERHOME)
    _dot_bin_path = "{}/.bin".format(USERHOME)
    # mkdir ~/.local/bin
    if not os.path.exists(_local_bin_path):
        mkdir_p(_local_bin_path)
    # mkdir ~/.bin
    if not os.path.exists(_dot_bin_path):
        mkdir_p(_dot_bin_path)

def bootstrap():
    mkdir_user_bin_dirs()
    clone_jhbuild()
    compile_jhbuild()

def main(context):
    if context['cmd'] == 'bootstrap':
        bootstrap()
    elif context['cmd'] == 'dump_env':
        setup_path_env()
        dump_env_var("PATH")
    elif context['cmd'] == 'compile':
        compile_jhbuild()
    elif context['cmd'] == 'render-dry-run':
        setup_all_envs()
        render_jhbuildrc_dry_run()
    elif context['cmd'] == 'render':
        setup_all_envs()
        render_jhbuildrc_dry_run()
        write_jhbuildrc()
    else:
        Console.message('you picked something else weird, please try again')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="cmd to run. Options [render, list, dump_env, bootstrap]")

    args, extra_args = parser.parse_known_args()

    assert args.cmd != None

    context = {
        'cmd': args.cmd
    }

    main(context)
