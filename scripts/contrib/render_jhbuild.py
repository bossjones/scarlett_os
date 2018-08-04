import argparse
import contextlib
import errno
import getpass
import io
import os
import re
import select
import shutil
import stat
import subprocess
import sys
import time

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    from six.moves.urllib.parse import urlparse
elif PY3:
    from urllib.parse import urlparse

USERNAME = getpass.getuser()
USERHOME = os.path.expanduser("~")
PATH_TO_JHBUILDRC = os.path.join(USERHOME + "/.config", "jhbuildrc")
PREFIX = os.path.join(USERHOME, "jhbuild")
CHECKOUTROOT = os.path.join(USERHOME, "gnome")
PROJECT_HOME = os.path.join(USERHOME, "dev")
PY_VERSION = "3.5"
PY_VERSION_FULL = "{}.2".format(PY_VERSION)
JHBUILD_GITHUB_URL = "https://github.com/GNOME/jhbuild.git"
JHBUILD_SHA = "86d958b6778da649b559815c0a0dbe6a5d1a8cd4"
PATH_TO_JHBUILD_BIN = os.path.join(USERHOME + ".local/bin", "jhbuild")


BUILD_GTK_DOC = """
jhbuild buildone -n gtk-doc
"""

BUILD_GLIB = """
jhbuild buildone -n glib
"""

BUILD_GOBJECT_INTROSPECTION = """
jhbuild buildone -n gobject-introspection
"""

BUILD_PIXMAN = """
chmod +x ./autogen.sh; \
jhbuild run ./autogen.sh; \
jhbuild run ./configure --prefix={PREFIX}; \
jhbuild run make -j4; \
jhbuild run make install
"""

BUILD_CAIRO = """
chmod +x ./autogen.sh; \
jhbuild run ./autogen.sh; \
jhbuild run ./configure --prefix={PREFIX} --enable-xlib --enable-ft --enable-svg --enable-ps --enable-pdf --enable-tee --enable-gobject; \
jhbuild run make -j4 ; \
jhbuild run make install
"""

BUILD_PYCAIRO = """
jhbuild run python3 setup.py install
"""

BUILD_PYGOBJECT = """
jhbuild run ./autogen.sh --prefix={PREFIX} --with-python=$(pyenv which python3.5); \
jhbuild run make install
"""

BUILD_FRIBIDI = """
jhbuild run meson mesonbuild/ --prefix={PREFIX} -Ddocs=false --libdir=lib --includedir=include --bindir=bin --datadir=share --mandir=share/man; \
jhbuild run ninja -C mesonbuild/; \
jhbuild run ninja -C mesonbuild/ install
"""

BUILD_PANGO = """
jhbuild run meson mesonbuild/ --prefix={PREFIX} --libdir=lib --includedir=include --bindir=bin --datadir=share --mandir=share/man; \
ninja -C mesonbuild/ dist
"""

BUILD_GTK2 = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --disable-man --with-xinput=xfree; \
jhbuild run make clean all; \
jhbuild run make install
"""

BUILD_GTK3 = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --enable-xkb --enable-xinerama --enable-xrandr --enable-xfixes --enable-xcomposite --enable-xdamage
--enable-x11-backend; \
jhbuild run make clean all; \
jhbuild run make install
"""

BUILD_GSTREAMER = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --enable-introspection=yes --enable-gtk-doc=no --prefix={PREFIX}; \
jhbuild run make -j4; \
jhbuild run make install
"""

BUILD_ORC = """
export BOSSJONES_PATH_TO_PYTHON=$(pyenv which python3.5)
sed -i "s,#!python,#!$BOSSJONES_PATH_TO_PYTHON,g" {PREFIX}/bin/gtkdoc-rebase; \
jhbuild run ./configure --prefix={PREFIX}; \
jhbuild run make -j4 ; \
jhbuild run make install;
"""

BUILD_GST_PLUGINS_BASE = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --enable-orc --enable-introspection=yes --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no; \
jhbuild run make -j4; \
jhbuild run make install
"""

BUILD_GST_PLUGINS_GOOD = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --enable-orc --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no; \
jhbuild run make -j4; \
jhbuild run make install
"""

BUILD_GST_PLUGINS_UGLY = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --enable-orc --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no; \
jhbuild run make -j4; \
jhbuild run make install
"""


BUILD_GST_PLUGINS_BAD = """
export BOSSJONES_PATH_TO_PYTHON=$(pyenv which python3.5)
sed -i "s,#!python3,#!$BOSSJONES_PATH_TO_PYTHON,g" {PREFIX}/bin/gdbus-codegen; \
sed -i "s,#!python,#!$BOSSJONES_PATH_TO_PYTHON,g" {PREFIX}/bin/gdbus-codegen; \
cat {PREFIX}/bin/gdbus-codegen; \
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --enable-orc --enable-gtk-doc=no --disable-examples --enable-gtk-doc-html=no; \
jhbuild run make -j4; \
jhbuild run make install
"""

BUILD_GST_LIBAV = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --enable-orc --enable-gtk-doc=no --enable-gtk-doc-html=no; \
jhbuild run make -j4; \
jhbuild run make install
"""


BUILD_GST_PYTHON = """
jhbuild run ./autogen.sh --prefix={PREFIX} --enable-shared=no; \
jhbuild run ./configure --prefix={PREFIX} --enable-shared=no; \
jhbuild run make -j4; \
jhbuild run make install
"""

BUILD_GST_PLUGINS_ESPEAK = """
for i in `grep -irH "-lespeak-ng" * | cut -d ':' -f1`; do
    sed -i 's,-lespeak-ng,-lespeak,g' $i
done
jhbuild run ./configure --prefix={PREFIX}; \
jhbuild run make; \
jhbuild run make install
"""

BUILD_SPHINXBASE = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX}; \
jhbuild run make clean all; \
jhbuild run make install
"""

BUILD_POCKETSPHINX = """
jhbuild run ./autogen.sh --prefix={PREFIX}; \
jhbuild run ./configure --prefix={PREFIX} --with-python; \
jhbuild run make clean all; \
jhbuild run make install
"""

repo_git_dicts = {
    "gtk-doc": {
        "repo": "https://github.com/GNOME/gtk-doc.git",
        "branch": "master",
        "compile-commands": BUILD_GTK_DOC,
        "folder": "gtk-doc",
    },
    "glib": {
        "repo": "https://github.com/GNOME/glib.git",
        "branch": "eaca4f4116801f99e30e42a857559e19a1e6f4ce",
        "compile-commands": BUILD_GLIB,
        "folder": "glib",
    },
    "gobject-introspection": {
        "repo": "https://github.com/GNOME/gobject-introspection.git",
        "branch": "cee2a4f215d5edf2e27b9964d3cfcb28a9d4941c",
        "compile-commands": BUILD_GOBJECT_INTROSPECTION,
        "folder": "gobject-introspection",
    },
    "pixman": {
        "repo": "git://anongit.freedesktop.org/git/pixman",
        "branch": "pixman-0.33.6",
        "compile-commands": BUILD_PIXMAN,
        "folder": "pixman",
    },
    "cairo": {
        "repo": "git://anongit.freedesktop.org/git/cairo",
        "branch": "1.14.6",
        "compile-commands": BUILD_CAIRO,
        "folder": "cairo",
    },
    "pycairo": {
        "repo": "git://anongit.freedesktop.org/git/pycairo",
        "branch": "master",
        "compile-commands": BUILD_PYCAIRO,
        "folder": "pycairo",
    },
    "pygobject": {
        "repo": "https://github.com/GNOME/pygobject.git",
        "branch": "fb1b8fa8a67f2c7ea7ad4b53076496a8f2b4afdb",
        "compile-commands": BUILD_PYGOBJECT,
        "folder": "pygobject",
    },
    "fribidi": {
        "repo": "https://github.com/fribidi/fribidi.git",
        "branch": "master",
        "compile-commands": BUILD_FRIBIDI,
        "folder": "fribidi",
    },
    "pango": {
        "repo": "https://gitlab.gnome.org/GNOME/pango.git",
        "branch": "1.42.1",
        "compile-commands": BUILD_PANGO,
        "folder": "pango",
    },
    "gtk2": {
        "repo": "https://gitlab.gnome.org/GNOME/gtk.git",
        "branch": "gtk-2-24",
        "compile-commands": BUILD_GTK2,
        "folder": "gtk2",
    },
    "gtk3": {
        "repo": "https://gitlab.gnome.org/GNOME/gtk.git",
        "branch": "gtk-3-22",
        "compile-commands": BUILD_GTK3,
        "folder": "gtk3",
    },
    "gst-python": {
        "repo": "https://github.com/GStreamer/gst-python",
        "branch": "1.8.2",
        "compile-commands": BUILD_GST_PYTHON,
        "folder": "gst-python",
    },
    "sphinxbase": {
        "repo": "https://github.com/cmusphinx/sphinxbase.git",
        "branch": "74370799d5b53afc5b5b94a22f5eff9cb9907b97",
        "compile-commands": BUILD_SPHINXBASE,
        "folder": "sphinxbase",
    },
    "pocketsphinx": {
        "repo": "https://github.com/cmusphinx/pocketsphinx.git",
        "branch": "68ef5dc6d48d791a747026cd43cc6940a9e19f69",
        "compile-commands": BUILD_POCKETSPHINX,
        "folder": "pocketsphinx",
    },
}

repo_tar_dicts = {
    "gstreamer": {
        "tar": "https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.8.2.tar.xz",
        "folder": "gstreamer-1.8.2",
        "compile-commands": BUILD_GSTREAMER,
    },
    "orc": {
        "tar": "https://gstreamer.freedesktop.org/src/orc/orc-0.4.25.tar.xz",
        "folder": "orc-0.4.25",
        "compile-commands": BUILD_ORC,
    },
    "gst-plugins-base": {
        "tar": "http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.8.2.tar.xz",
        "folder": "gst-plugins-base-1.8.2",
        "compile-commands": BUILD_GST_PLUGINS_BASE,
    },
    "gst-plugins-good": {
        "tar": "http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-1.8.2.tar.xz",
        "folder": "gst-plugins-good-1.8.2",
        "compile-commands": BUILD_GST_PLUGINS_GOOD,
    },
    "gst-plugins-bad": {
        "tar": "http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-1.8.2.tar.xz",
        "folder": "gst-plugins-bad-1.8.2",
        "compile-commands": BUILD_GST_PLUGINS_BAD,
    },
    "gst-plugins-ugly": {
        "tar": "http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-1.8.2.tar.xz",
        "folder": "gst-plugins-ugly-1.8.2",
        "compile-commands": BUILD_GST_PLUGINS_UGLY,
    },
    "gst-libav": {
        "tar": "http://gstreamer.freedesktop.org/src/gst-libav/gst-libav-1.8.2.tar.xz",
        "folder": "gst-libav-1.8.2",
        "compile-commands": BUILD_GST_LIBAV,
    },
    "gst-plugins-espeak": {
        "tar": "https://github.com/bossjones/bossjones-gst-plugins-espeak-0-4-0/archive/v0.4.1.tar.gz",
        "folder": "bossjones-gst-plugins-espeak-0-4-0-0.4.1",
        "compile-commands": BUILD_GST_PLUGINS_ESPEAK,
    },
}

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
    print(" ".join(command))
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )
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

    if os.path.isdir(os.path.join(dir, ".git")):
        return "git"
    elif os.path.isdir(os.path.join(dir, ".hg")):
        return "hg"


def _popen(cmd_arg):
    devnull = open("/dev/null")
    cmd = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, stderr=devnull, shell=True)
    retval = cmd.stdout.read().strip()
    err = cmd.wait()
    cmd.stdout.close()
    devnull.close()
    if err:
        raise RuntimeError("Failed to close %s stream" % cmd_arg)
    return retval


def _popen_stdout(cmd_arg, cwd=None):
    # if passing a single string, either shell mut be True or else the string must simply name the program to be executed without specifying any arguments
    cmd = subprocess.Popen(
        cmd_arg,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        bufsize=4096,
        shell=True,
    )
    Console.message("BEGIN: {}".format(cmd_arg))
    # output, err = cmd.communicate()

    for line in iter(cmd.stdout.readline, b""):
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


def clone_all():
    for k, v in repo_git_dicts.items():
        k_full_path = os.path.join(CHECKOUTROOT, k)
        git_clone(v["repo"], k_full_path, sha=v["branch"])


def get_tar_files():
    for k, v in repo_tar_dicts.items():
        _a_url = urlparse(v["tar"])
        _file_name = os.path.basename(_a_url.path)
        with cd(CHECKOUTROOT):
            _cmd = "curl -L '{tar}' > {archive_file}".format(
                tar=v["tar"], archive_file=_file_name
            )
            _popen_stdout(_cmd)


def untar_files():
    for k, v in repo_tar_dicts.items():
        _a_url = urlparse(v["tar"])
        _file_name = os.path.basename(_a_url.path)
        with cd(CHECKOUTROOT):
            _cmd = "tar xvf {archive_file}".format(archive_file=_file_name)
            _popen_stdout(_cmd)


# Clone everything that doesnt exist
def git_clone(repo_url, dest, sha="master"):
    # First check if folder exists
    if not os.path.exists(dest):
        # check if folder is a git repo
        if scm(dest) != "git":
            clone_cmd = "git clone {repo} {dest}".format(repo=repo_url, dest=dest)
            _popen_stdout(clone_cmd)

            # CD to directory
            with cd(dest):
                checkout_cmd = "git checkout {sha}".format(sha=sha)
                _popen_stdout(checkout_cmd)


def clone_jhbuild():
    # First check if folder exists
    if not os.path.exists(PREFIX):
        # check if folder is a git repo
        if scm(PREFIX) != "git":
            # nuke folder
            # remove(PREFIX)
            # clone it
            jhbuild_clone_cmd = "git clone {repo} {dest}".format(
                repo=JHBUILD_GITHUB_URL, dest=PREFIX
            )
            _popen_stdout(jhbuild_clone_cmd)

            # CD to directory
            with cd(PREFIX):
                jhbuild_checkout_cmd = "git checkout {sha}".format(sha=JHBUILD_SHA)
                _popen_stdout(jhbuild_checkout_cmd)

    return PREFIX


def compile_jhbuild():
    Console.message("First check if folder exists")
    Console.message("if not os.path.exists(PREFIX) = {}".format(PREFIX))
    if os.path.exists(PREFIX):
        Console.message("check if folder is a git repo")
        if scm(PREFIX) == "git":
            with cd(PREFIX):
                _autogen_cmd = "./autogen.sh --prefix={}/.local".format(USERHOME)
                _popen_stdout(_autogen_cmd, cwd=PREFIX)
                _make_cmd = "make"
                _popen_stdout(_make_cmd, cwd=PREFIX)
                _make_install_cmd = "make install"
                _popen_stdout(_make_install_cmd, cwd=PREFIX)
                _test_jhbuild = "~/.local/bin/jhbuild --help"
                _popen_stdout(_test_jhbuild, cwd=PREFIX)


def get_package_dict(package_to_build):
    if package_to_build in repo_git_dicts:
        return repo_git_dicts
    elif package_to_build in repo_tar_dicts:
        return repo_tar_dicts


def compile_one(package_to_build):
    pkg_dict = get_package_dict(package_to_build)
    path_to_folder = os.path.join(CHECKOUTROOT, pkg_dict[package_to_build]["folder"])
    with cd(path_to_folder):
        _rendered_command = pkg_dict[package_to_build]["compile-commands"].format(
            PREFIX=PREFIX
        )
        _popen_stdout(_rendered_command, cwd=path_to_folder)


def compile_all():
    compile_one("gtk-doc")
    compile_one("glib")
    compile_one("gobject-introspection")
    compile_one("pygobject")
    compile_one("gstreamer")
    compile_one("orc")
    compile_one("gst-plugins-base")
    compile_one("gst-plugins-good")
    compile_one("gst-plugins-ugly")
    compile_one("gst-plugins-bad")
    compile_one("gst-libav")
    compile_one("gst-python")
    compile_one("gst-plugins-espeak")
    compile_one("sphinxbase")
    compile_one("pocketsphinx")


def pip_install_meson():
    _cmd = "python3 -m pip install meson"
    _popen_stdout(_cmd, cwd=PREFIX)


def whoami():
    whoami = _popen("who")
    return whoami


# Some utility functions used here and in custom files:


def environ_append(key, value, separator=" ", force=False):
    old_value = os.environ.get(key)
    if old_value is not None:
        value = old_value + separator + value
    os.environ[key] = value


def environ_prepend(key, value, separator=" ", force=False):
    old_value = os.environ.get(key)
    if old_value is not None:
        value = value + separator + old_value
    os.environ[key] = value


def environ_remove(key, value, separator=":", force=False):
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
    environ_set("CFLAGS", "-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer")
    environ_set("CXXFLAGS", "-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer")
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
    environ_prepend(
        "PYTHONPATH", "/usr/lib/python{}/site-packages".format(PY_VERSION), ":"
    )
    environ_prepend(
        "PYTHONPATH",
        "{}/jhbuild/lib/python{}/site-packages".format(USERHOME, PY_VERSION),
        ":",
    )
    environ_prepend(
        "PYTHONPATH",
        "{}/.pyenv/versions/{}/lib/python{}/site-packages".format(
            USERHOME, PY_VERSION_FULL, PY_VERSION
        ),
        ":",
    )
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
    environ_prepend(
        "PKG_CONFIG_PATH", "{}/jhbuild/share/pkgconfig".format(USERHOME), ":"
    )
    environ_prepend("PKG_CONFIG_PATH", "{}/jhbuild/lib/pkgconfig".format(USERHOME), ":")
    environ_prepend(
        "PKG_CONFIG_PATH",
        "{}/.pyenv/versions/{}/lib/pkgconfig".format(USERHOME, PY_VERSION_FULL),
        ":",
    )
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
    with open(PATH_TO_JHBUILDRC, "w+") as fp:
        fp.write(rendered_jhbuild)


def render_jhbuildrc_dry_run():
    rendered_jhbuild = JHBUILD_TEMPLATE.format(
        PREFIX=environ_get("PREFIX"),
        CHECKOUTROOT=environ_get("CHECKOUTROOT"),
        CFLAGS=environ_get("CFLAGS"),
        PYTHON_VERSION=environ_get("PYTHON_VERSION"),
        PATH=environ_get("PATH"),
        LD_LIBRARY_PATH=environ_get("LD_LIBRARY_PATH"),
        PYTHONPATH=environ_get("PYTHONPATH"),
        PKG_CONFIG_PATH=environ_get("PKG_CONFIG_PATH"),
        XDG_DATA_DIRS=environ_get("XDG_DATA_DIRS"),
        XDG_CONFIG_DIRS=environ_get("XDG_CONFIG_DIRS"),
        PROJECT_HOME=environ_get("PROJECT_HOME"),
        PYTHONSTARTUP=environ_get("PYTHONSTARTUP"),
    )
    Console.message("----------------[render_jhbuildrc_dry_run]----------------")
    Console.message(rendered_jhbuild)

    return rendered_jhbuild


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


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


def mkdir_checkoutroot():
    if not os.path.exists(CHECKOUTROOT):
        mkdir_p(CHECKOUTROOT)


def bootstrap():
    mkdir_checkoutroot()
    mkdir_user_bin_dirs()
    clone_jhbuild()
    compile_jhbuild()
    pip_install_meson()


def main(context):
    if context["cmd"] == "bootstrap":
        bootstrap()
    elif context["cmd"] == "dump_env":
        setup_path_env()
        dump_env_var("PATH")
    elif context["cmd"] == "compile":
        compile_jhbuild()
    elif context["cmd"] == "render-dry-run":
        setup_all_envs()
        render_jhbuildrc_dry_run()
    elif context["cmd"] == "render":
        setup_all_envs()
        render_jhbuildrc_dry_run()
        write_jhbuildrc()
    elif context["cmd"] == "pip-install-meson":
        pip_install_meson()
    elif context["cmd"] == "compile-gtk-doc":
        print("compile-gtk-doc")
    elif context["cmd"] == "clone-all":
        clone_all()
    elif context["cmd"] == "get-all-tar-files":
        get_tar_files()
    elif context["cmd"] == "untar-files":
        untar_files()
    elif context["cmd"] == "build":
        compile_one(context["pkg"])
    elif context["cmd"] == "compile-all":
        compile_all()
    else:
        Console.message("you picked something else weird, please try again")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd",
        help="cmd to run. Options [bootstrap, dump_env, compile, render-dry-run, render, pip-install-meson, compile-gtk-doc, clone-all, get-all-tar-files, untar-files, build, compile-all]",
    )
    parser.add_argument("--pkg", type=str, required=False, help="Package name.")

    args, extra_args = parser.parse_known_args()

    assert args.cmd != None

    context = {"cmd": args.cmd, "pkg": args.pkg}

    main(context)
