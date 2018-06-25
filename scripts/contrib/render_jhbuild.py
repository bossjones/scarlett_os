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


JHBUILD_TEMPLATE = """
import os
prefix='{PREFIX}'
checkoutroot='{CHECKOUTROOT}'
moduleset = 'gnome-world'
interact = False
makeargs = '-j4'
os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
os.environ['PYTHON'] = 'python'
os.environ['GSTREAMER'] = '1.0'
os.environ['ENABLE_PYTHON3'] = 'yes'
os.environ['ENABLE_GTK'] = 'yes'
os.environ['PYTHON_VERSION'] = '3.5'
os.environ['MAKEFLAGS'] = '-j4'
os.environ['PREFIX'] = '{PREFIX}'
os.environ['JHBUILD'] = '{CHECKOUTROOT}'
os.environ['PATH'] = '/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/home/pi/.pyenv/shims:~/.pyenv/bin/:~/.bin:/home/pi/.local/bin:/home/pi/.rbenv/shims:/home/pi/.rbenv/bin:/home/pi/.nvm/versions/node/v8.7.0/bin:/usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/pi/.rvm/bin:/home/pi/.go/bin:/home/pi/go/bin'
os.environ['LD_LIBRARY_PATH'] = '/home/pi/jhbuild/lib:/home/pi/jhbuild/lib:/usr/lib'
os.environ['PYTHONPATH'] = '/home/pi/.pyenv/versions/3.5.2/lib/python3.5/site-packages:/home/pi/jhbuild/lib/python3.5/site-packages:/usr/lib/python3.5/site-packages'
os.environ['PKG_CONFIG_PATH'] = '/home/pi/.pyenv/versions/3.5.2/lib/pkgconfig:/home/pi/jhbuild/lib/pkgconfig:/home/pi/jhbuild/share/pkgconfig:/usr/lib/pkgconfig'
os.environ['XDG_DATA_DIRS'] = '/home/pi/jhbuild/share:/usr/share'
os.environ['XDG_CONFIG_DIRS'] = '/home/pi/jhbuild/etc/xdg'
os.environ['CC'] = 'gcc'
os.environ['PROJECT_HOME'] = '/home/pi/dev'
os.environ['PYTHONSTARTUP'] = '/home/pi/.pythonrc'
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
            remove(PREFIX)
            # clone it
            jhbuild_clone_cmd = "git clone {repo} {dest}".format(repo=JHBUILD_GITHUB_URL,
                                                                            dest=PREFIX)
            _retval_clone = _popen(jhbuild_clone_cmd)
            Console.message("_retval_clone: {}".format(_retval_clone))

            # CD to directory
            with cd(PREFIX):
                jhbuild_checkout_cmd = "git checkout {sha}".format(sha=JHBUILD_SHA)
                _retval_checkout = _popen(jhbuild_checkout_cmd)
                Console.message("_retval_checkout: {}".format(_retval_checkout))

    return PREFIX

def compile_jhbuild():
    # First check if folder exists
    if not os.path.exists(PREFIX):
        # check if folder is a git repo
        if scm(PREFIX) != 'git':
            with cd(PREFIX):
                _autogen_cmd = "./autogen.sh --prefix={}/.local".format(USERHOME)
                _autogen_retval = _popen(_autogen_cmd)
                Console.message(_autogen_retval)

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
    os.environ.get(key)

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

def write_jhbuildrc():
    # path_to_main_yml = os.path.join(path_to_role_subdir, 'main.yml')
    # with open(path_to_main_yml, 'w+') as fp:
    #     fp.write(MAIN_YML_TEMPLATE.format(role_name=context['role']))
    pass

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
