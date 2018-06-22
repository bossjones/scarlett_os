import os
import sys
import re
import argparse

USERNAME = whoami()
USERHOME = os.path.expanduser("~")
PATH_TO_JHBUILDRC = os.path.join(USERHOME + ".config", "jhbuildrc")
PREFIX = os.path.join(USERHOME, "jhbuild")
CHECKOUTROOT = os.path.join(USERHOME, "gnome")
PROJECT_HOME = os.path.join(USERHOME, "dev")
PY_VERSION = '3.5'
PY_VERSION_FULL = "{}.2".format(PY_VERSION)


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

def _popen(cmd_arg):
    from subprocess import Popen, PIPE
    devnull = open('/dev/null')
    cmd = Popen(cmd_arg, stdout=PIPE, stderr=devnull, shell=True)
    retval = cmd.stdout.read().strip()
    err = cmd.wait()
    cmd.stdout.close()
    devnull.close()
    if err:
        raise RuntimeError, 'Failed to close %s stream' % cmd_arg
    return retval

def whoami():
    whoami = _popen('who')
    return whoami

# Some utility functions used here and in custom files:

def environ_append(key, value, separator=' '):
    old_value = os.environ.get(key)
    if old_value is not None:
        value = old_value + separator + value
    os.environ[key] = value

def environ_prepend(key, value, separator=' '):
    old_value = os.environ.get(key)
    if old_value is not None:
        value = value + separator + old_value
    os.environ[key] = value

def environ_remove(key, value, separator=':'):
    old_value = os.environ.get(key)
    if old_value is not None:
        old_value_split = old_value.split(separator)
        value_split = [x for x in old_value_split if x != value]
        value = separator.join(value_split)
    os.environ[key] = value

def path_append(value):
    if os.path.exists(value):
        environ_append("PATH", value, ":")

def path_prepend(value):
    if os.path.exists(value):
        environ_prepend("PATH", value, ":")

# Call either setup_debug or setup_release in your .jhbuildrc-custom
# or other customization file to get the compilation flags.
def setup_debug():
    environ_prepend('CFLAGS', '-O0 -g')
    environ_prepend('CXXFLAGS', '-O0 -g')
    environ_prepend('OBJCFLAGS', '-O0 -g')

def setup_path_env():
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
    path_prepend("{}/.pyenv/bin".format(USERHOME))
    path_prepend("{}/.pyenv/shims".format(USERHOME))
    path_prepend("{}/jhbuild/sbin".format(USERHOME))
    path_prepend("{}/jhbuild/bin".format(USERHOME))

def write_jhbuildrc():
    # path_to_main_yml = os.path.join(path_to_role_subdir, 'main.yml')
    # with open(path_to_main_yml, 'w+') as fp:
    #     fp.write(MAIN_YML_TEMPLATE.format(role_name=context['role']))
    pass

def dump_env_var(var):
    print("Env Var:{}={}".format(var,os.environ.get(var,"<EMPTY>")))


def main(context):
    # mkdir_role(context)
    # mkdirs_playbook(context)
    setup_path_env()
    dump_env_var(PATH)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="cmd to run. Options [render, list, dump_env]")

    args, extra_args = parser.parse_known_args()

    assert args.cmd != None

    context = {
        'cmd': args.cmd
    }

    main(context)
