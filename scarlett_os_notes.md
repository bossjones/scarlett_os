### Folders:

# NOTE:

`ha = s`
`hass = ss`

```
scarlett_os/brain/
  - Store all commands asked of scarlett, command processing?
  - Register name of system
     - name is generated automatically based on SJ names in other movies
     - http://www.imdb.com/name/nm0424060/
     - Or you can specify a name yourself
  - StateMachine
  - CommandObject? - Jarvis
  - BinaryObject(CommandObject)? - Jarvis
  - ToggleObject(CommandObject)? - Jarvis

scarlett_os/database/
  - Create connection to db, eg. redis, sql-lite, etcd, whatever
  - Persistent info

scarlett_os/util/
  - (folder, see ha for examples)
  - url.py
  - yaml.py
  - temp.py
  - location.py
  - color.py
  - datetime.py
  - discover.py ( timeside)
  - dep.py
  - gi.py
  - dbus.py
  - jsonrpc.py
  - formatting.py

scarlett_os/audio/
  - listener logic
  - speaker logic
  - alsa device lookups
  - GST stuff
  - example: https://github.com/mopidy/mopidy/tree/develop/mopidy/audio

scarlett_os/configure/
  - Configuration for scarlett, yaml or environment variables
  - __init__.py
  - file_config.py
  - env_config.py
  - default_config.py
  - example: redpill

scarlett_os/static/speech
  - static assets, eg. .wav files for scarlett sounds
  - corpus etc

scarlett_os/static/ir_commands
  - text files full of IR codes

scarlett_os/automations/
  - AKA automations or features
  - hue lights
  - ir reciever / emitter
  - weather
  - wordnik
  - google
  - usb
  - window
  - robot remote control
  - tv
  - stock
  - spotify
  - motion sensor

scarlett_os/core/
  - see timeside, https://github.com/Parisson/TimeSide/tree/master/timeside/core

scripts/
  - scripts to do one off things, eg update corpus, lm, etc

tests/
tests/unit/
tests/integration/
  - all testing related stuff duh

docs/

bin/ - wrapper python scripts for calling everything via cli

```

### Modules:

```
__init__.py
  - Initalize everything as a python module

__main__.py
  - This wraps the entire program, leverages cli.py and starts the scarlett daemon
  - eg. https://github.com/home-assistant/home-assistant/blob/dev/scarlett_os/__main__.py
  - verifies mode(env/fileconfig)
  - verifies version of python
  - verifies version of gst/gtk

__version__.py
  - current version of code

bootstrap.py
  - returns instance of scarlett
  - must be started with environment variables or yaml config

exceptions.py
  - all exception handling

ext.py
  - contains Base class for extensions etc
  - see: https://github.com/mopidy/mopidy/blob/develop/mopidy/ext.py

remote.py
  - scarlett that forwards information to somewhere else, or listens to info from elsewhere
  - example: https://github.com/home-assistant/home-assistant/blob/dev/scarlett_os/remote.py

core.py - Where we define what the Scarlett System Object is.
  - https://github.com/home-assistant/home-assistant/blob/dev/scarlett_os/core.py
  - Similar to locustio, this is were we define what a master/slave/local scarlett system looks like ( Management Component )

consts.py
  - Simple constants we need

component.py
  - example: https://github.com/Parisson/TimeSide/blob/master/timeside/core/component.py
  - management class for all things in api.py

log.py
  - handle all scralett logging

task.py
  - task objects and things that scarlett needs to do

api.py
  - example: https://github.com/Parisson/TimeSide/blob/master/timeside/core/api.py
  - scarlett interfaces/base classes

cli.py
  - integrate with click cli framework


```

### Notes:

Looking at this example:

```
def setup_and_run_hass(config_dir: str,
                       args: argparse.Namespace) -> Optional[int]:
    """Setup HASS and run."""
    from scarlett_os import bootstrap
```

What does the -> mean?

A: http://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions

```
It's a function annotation.

In more detail, Python 2.x has docstrings, which allow you to attach a metadata string to various types of object. This is amazingly handy, so Python 3 extends the feature by allowing you to attach metadata to functions describing their parameters and return values.

There's no preconceived use case, but the PEP suggests several. One very handy one is to allow you to annotate parameters with their expected types; it would then be easy to write a decorator that verifies the annotations or coerces the arguments to the right type. Another is to allow parameter-specific documentation instead of encoding it into the docstring.
```

### Ansible roles to use going forward

https://galaxy.ansible.com/angstwad/docker_ubuntu/
https://galaxy.ansible.com/thefinn93/letsencrypt/
https://galaxy.ansible.com/geerlingguy/git/
https://galaxy.ansible.com/geerlingguy/daemonize/
https://galaxy.ansible.com/geerlingguy/java/
https://galaxy.ansible.com/geerlingguy/
https://galaxy.ansible.com/geerlingguy/firewall/
https://galaxy.ansible.com/geerlingguy/nodejs/
https://galaxy.ansible.com/nickhammond/logrotate/
https://galaxy.ansible.com/geerlingguy/security/
https://galaxy.ansible.com/mattwillsher/sshd/
https://galaxy.ansible.com/rvm_io/rvm1-ruby/
https://galaxy.ansible.com/angstwad/docker_ubuntu/
https://galaxy.ansible.com/resmo/ntp/
https://galaxy.ansible.com/joshualund/golang/
https://galaxy.ansible.com/yatesr/timezone/
https://galaxy.ansible.com/tersmitten/limits/
https://galaxy.ansible.com/f500/dumpall/
https://galaxy.ansible.com/zzet/rbenv/
https://galaxy.ansible.com/williamyeh/oracle-java/
https://galaxy.ansible.com/mivok0/users/
https://galaxy.ansible.com/gaqzi/ssh-config/
https://galaxy.ansible.com/leonidas/nvm/
https://galaxy.ansible.com/bennojoy/network_interface/
https://galaxy.ansible.com/jdauphant/ssl-certs/
https://galaxy.ansible.com/dev-sec/os-hardening/


# brew install pygobject3

```
 |2.1.7|   Malcolms-MBP-3 in /usr/local/Cellar/pygobject3/3.18.2/lib/python2.7/site-packages/gi
± |master ✓| → brew info pygobject3
pygobject3: stable 3.20.1 (bottled)
GNOME Python bindings (based on GObject Introspection)
https://live.gnome.org/PyGObject
/usr/local/Cellar/pygobject3/3.18.2 (61 files, 2M) *
  Poured from bottle on 2016-02-27 at 10:16:05
From: https://github.com/Homebrew/homebrew-core/blob/master/Formula/pygobject3.rb
==> Dependencies
Build: xz ✔, pkg-config ✔
Required: glib ✔, py2cairo ✔, gobject-introspection ✘
Optional: libffi ✔
==> Options
--universal
       	Build a universal binary
--with-libffi
       	Build with libffi support
--with-python3
       	Build with python3 support
--without-python
       	Build without python2 support

 |2.1.7|   Malcolms-MBP-3 in /usr/local/Cellar/pygobject3/3.18.2/lib/python2.7/site-packages/gi
± |master ✓| → brew reinstall pygobject3 --with-python3
==> Reinstalling pygobject3 with --with-python3
==> Installing dependencies for pygobject3: sqlite, homebrew/dupes/tcl-tk, python3, libpng, freetype, fontconfig, py3cairo, gobject-introspection
==> Installing pygobject3 dependency: sqlite
==> Downloading https://homebrew.bintray.com/bottles/sqlite-3.14.1.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring sqlite-3.14.1.el_capitan.bottle.tar.gz
==> Caveats
This formula is keg-only, which means it was not symlinked into /usr/local.

OS X provides an older sqlite3.

Generally there are no consequences of this for you. If you build your
own software and it requires this formula, you'll need to add to your
build variables:

    LDFLAGS:  -L/usr/local/opt/sqlite/lib
    CPPFLAGS: -I/usr/local/opt/sqlite/include

==> Summary
🍺  /usr/local/Cellar/sqlite/3.14.1: 10 files, 2.9M
==> Installing pygobject3 dependency: homebrew/dupes/tcl-tk
==> Downloading https://homebrew.bintray.com/bottles-dupes/tcl-tk-8.6.6.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring tcl-tk-8.6.6.el_capitan.bottle.tar.gz
==> Caveats
This formula is keg-only, which means it was not symlinked into /usr/local.

Tk installs some X11 headers and OS X provides an (older) Tcl/Tk.

Generally there are no consequences of this for you. If you build your
own software and it requires this formula, you'll need to add to your
build variables:

    LDFLAGS:  -L/usr/local/opt/tcl-tk/lib
    CPPFLAGS: -I/usr/local/opt/tcl-tk/include

==> Summary
🍺  /usr/local/Cellar/tcl-tk/8.6.6: 2,846 files, 29.2M
==> Installing pygobject3 dependency: python3
==> Using the sandbox
==> Downloading https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
######################################################################## 100.0%
==> Downloading https://bugs.python.org/file30805/issue10910-workaround.txt
######################################################################## 100.0%
==> Patching
==> Applying issue10910-workaround.txt
patching file Include/pyport.h
Hunk #1 succeeded at 688 (offset -11 lines).
Hunk #2 succeeded at 711 (offset -11 lines).
patching file setup.py
Hunk #1 succeeded at 1749 (offset 50 lines).
Hunk #2 succeeded at 1794 (offset 50 lines).
Hunk #3 succeeded at 1817 (offset 50 lines).
==> ./configure --prefix=/usr/local/Cellar/python3/3.5.2_1 --enable-ipv6 --datarootdir=/usr/local/Cellar/python3/3.5.2_1/share --datadir=/usr/local/Cellar/python3/3.5.2_1/share --en
==> make
==> make install PYTHONAPPSDIR=/usr/local/Cellar/python3/3.5.2_1
==> make frameworkinstallextras PYTHONAPPSDIR=/usr/local/Cellar/python3/3.5.2_1/share/python3
==> Downloading https://files.pythonhosted.org/packages/9f/32/81c324675725d78e7f6da777483a3453611a427db0145dfb878940469692/setuptools-25.2.0.tar.gz
######################################################################## 100.0%
==> Downloading https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz
######################################################################## 100.0%
==> Downloading https://pypi.python.org/packages/source/w/wheel/wheel-0.29.0.tar.gz
######################################################################## 100.0%
==> /usr/local/Cellar/python3/3.5.2_1/bin/python3 -s setup.py --no-user-cfg install --force --verbose --install-scripts=/usr/local/Cellar/python3/3.5.2_1/bin --install-lib=/usr/loca
==> /usr/local/Cellar/python3/3.5.2_1/bin/python3 -s setup.py --no-user-cfg install --force --verbose --install-scripts=/usr/local/Cellar/python3/3.5.2_1/bin --install-lib=/usr/loca
==> /usr/local/Cellar/python3/3.5.2_1/bin/python3 -s setup.py --no-user-cfg install --force --verbose --install-scripts=/usr/local/Cellar/python3/3.5.2_1/bin --install-lib=/usr/loca
==> Caveats
Pip, setuptools, and wheel have been installed. To update them
  pip3 install --upgrade pip setuptools wheel

You can install Python packages with
  pip3 install <package>

They will install into the site-package directory
  /usr/local/lib/python3.5/site-packages

See: https://github.com/Homebrew/brew/blob/master/share/doc/homebrew/Homebrew-and-Python.md

.app bundles were installed.
Run `brew linkapps python3` to symlink these to /Applications.
==> Summary
🍺  /usr/local/Cellar/python3/3.5.2_1: 7,719 files, 109.5M, built in 2 minutes 46 seconds
==> Installing pygobject3 dependency: libpng
==> Downloading https://homebrew.bintray.com/bottles/libpng-1.6.24.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring libpng-1.6.24.el_capitan.bottle.tar.gz
🍺  /usr/local/Cellar/libpng/1.6.24: 26 files, 1.2M
==> Installing pygobject3 dependency: freetype
==> Downloading https://homebrew.bintray.com/bottles/freetype-2.6.5.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring freetype-2.6.5.el_capitan.bottle.tar.gz
🍺  /usr/local/Cellar/freetype/2.6.5: 61 files, 2.5M
==> Installing pygobject3 dependency: fontconfig
==> Downloading https://homebrew.bintray.com/bottles/fontconfig-2.12.1.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring fontconfig-2.12.1.el_capitan.bottle.tar.gz
==> Regenerating font cache, this may take a while
==> /usr/local/Cellar/fontconfig/2.12.1/bin/fc-cache -frv
🍺  /usr/local/Cellar/fontconfig/2.12.1: 468 files, 3M
==> Installing pygobject3 dependency: py3cairo
==> Downloading https://homebrew.bintray.com/bottles/py3cairo-1.10.0_2.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring py3cairo-1.10.0_2.el_capitan.bottle.tar.gz
🍺  /usr/local/Cellar/py3cairo/1.10.0_2: 10 files, 153.8K
==> Installing pygobject3 dependency: gobject-introspection
==> Downloading https://homebrew.bintray.com/bottles/gobject-introspection-1.48.0.el_capitan.bottle.tar.gz
######################################################################## 100.0%
==> Pouring gobject-introspection-1.48.0.el_capitan.bottle.tar.gz
🍺  /usr/local/Cellar/gobject-introspection/1.48.0: 170 files, 9.5M
==> Installing pygobject3
==> Downloading https://download.gnome.org/sources/pygobject/3.20/pygobject-3.20.1.tar.xz
==> Downloading from https://mirror.umd.edu/gnome/sources/pygobject/3.20/pygobject-3.20.1.tar.xz
######################################################################## 100.0%
==> ./configure --prefix=/usr/local/Cellar/pygobject3/3.20.1_1 PYTHON=python
==> make install
==> make clean
==> ./configure --prefix=/usr/local/Cellar/pygobject3/3.20.1_1 PYTHON=python3
==> make install
==> make clean
🍺  /usr/local/Cellar/pygobject3/3.20.1_1: 164 files, 3.4M, built in 47 seconds
shell-init: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
pwd: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
```

# docker-machine

```
 |2.1.7|   Malcolms-MBP-3 in ~/dev/bossjones/scarlett-ansible
? |featutre-1604 U:2 ?| ? docker-machine create -d generic \
>  --generic-ssh-user pi \
>  --generic-ssh-key /Users/malcolm/dev/bossjones/scarlett_os/keys/vagrant_id_rsa \
>  --generic-ssh-port 2222 \
>  --generic-ip-address 127.0.0.1 \
>  --engine-install-url "https://test.docker.com" \
>  scarlett-1604-packer
Running pre-create checks...
Creating machine...
(scarlett-1604-packer) Importing SSH key...
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with ubuntu(systemd)...
Installing Docker...
Copying certs to the local machine directory...
Copying certs to the remote machine...
Setting Docker configuration on the remote daemon...
Checking connection to Docker...
Docker is up and running!
To see how to connect your Docker Client to the Docker Engine running on this virtual machine, run: docker-machine env scarlett-1604-packer
```

# Debug python3 and PyGObject Setup
- `python3 -c "from gi.repository import Gtk; print(Gtk._overrides_module)"`

Source:
  - https://bugs.launchpad.net/ubuntu/+source/gexiv2/+bug/1277894
  - http://stackoverflow.com/questions/21380202/using-python3-gexiv2

```
A few debugging tips:
You can verify introspection overrides are brought in by looking at the private "_overrides_module" attribute of a library:

(this is on Fedora so Ubuntu will give a different location)
python3 -c "from gi.repository import Gtk; print(Gtk._overrides_module)"
<module 'gi.overrides.Gtk' from '/usr/lib64/python3.3/site-packages/gi/overrides/Gtk.py'>

If you do the same thing with GExiv2, you should get a similar result in terms of output. It may also be a good idea to look at the result of Gtk.py to ensure the directory GExiv2.py found with "locate" is in the same place:
python3 -c "from gi.repository import GExiv2; print(GExiv2._overrides_module)"
<module 'gi.overrides.GExiv2' from '/usr/lib64/python3.3/site-packages/gi/overrides/GExiv2.py'>

Also note Python2 and 3 will require separate installs of the overrides to their respective site-packages/dist-packages directory.
```


# rfoo

rfoo: Add this so we can see what's happening when code gets locked up in python.

rconsole: rconsole is a remote Python console with auto completion, which can be used to inspect and modify the namespace of a running script.


```
 1646  pip install Cython
 1647  ls -lta
 1648  ls
 1649  cd ..
 1650  ls
 1651  gcl git@github.com:aaiyer/rfoo.git
 1652  gcl https://github.com/aaiyer/rfoo.git
 1653  cd rfoo/
 1654  ls
 1655  python setup.py install
 1656  history
```

# pulseaudio debugging

- https://bugs.launchpad.net/ubuntu/+source/pulseaudio/+bug/1596344

- https://bugs.launchpad.net/ubuntu/+source/pulseaudio/+bug/1604497

- https://wiki.ubuntu.com/Audio/UpgradingAlsa/DKMS

- https://wiki.ubuntu.com/PulseAudio/Log

- https://wiki.archlinux.org/index.php/NetworkManager

- https://bbs.archlinux.org/viewtopic.php?id=188287

- https://wiki.archlinux.org/index.php/PulseAudio/Troubleshooting

- https://wiki.archlinux.org/index.php/PulseAudio/Configuration

- http://askubuntu.com/questions/70560/why-am-i-getting-this-connection-to-pulseaudio-failed-error

- https://lists.freedesktop.org/archives/pulseaudio-discuss/2013-December/019344.html

- http://askubuntu.com/questions/5866/what-terminal-command-will-dump-all-gconf-keys-and-values-ie-the-ones-seen-in-g

- https://wiki.archlinux.org/index.php/PulseAudio/Examples

- https://mail.gnome.org/archives/gtk-devel-list/2012-June/msg00000.html

- https://mail.gnome.org/archives/commits-list/2011-May/msg07614.html


# pystuck and remote debugging

```
pi@420148cf9f29:~/dev/bossjones-github/scarlett_os$ pystuck
Welcome to the pystuck interactive shell.
Use the 'modules' dictionary to access remote modules (like 'os', or '__main__')
Use the `%show threads` magic to display all thread stack traces.

In [1]: %show threads
<_MainThread(MainThread, started 140438333286144)>
  File "/usr/local/lib/python3.5/runpy.py", line 184, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/local/lib/python3.5/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/home/pi/dev/bossjones-github/scarlett_os/scarlett_os/mpris.py", line 456, in <module>
    loop.run()
  File "/home/pi/jhbuild/lib/python3.5/site-packages/gi/overrides/GLib.py", line 574, in run
    super(MainLoop, self).run()

<Thread(Thread-1, started daemon 140438198179584)>
  File "/usr/local/lib/python3.5/threading.py", line 882, in _bootstrap
    self._bootstrap_inner()
  File "/usr/local/lib/python3.5/threading.py", line 914, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.5/threading.py", line 862, in run
    self._target(*self._args, **self._kwargs)
  File "/usr/local/lib/python3.5/site-packages/rpyc/utils/server.py", line 241, in start
    self.accept()
  File "/usr/local/lib/python3.5/site-packages/rpyc/utils/server.py", line 128, in accept
    sock, addrinfo = self.listener.accept()
  File "/usr/local/lib/python3.5/socket.py", line 195, in accept
    fd, addr = self._accept()

<HistorySavingThread(IPythonHistorySavingThread, started 140438080890624)>
  File "/usr/local/lib/python3.5/threading.py", line 882, in _bootstrap
    self._bootstrap_inner()
  File "/usr/local/lib/python3.5/threading.py", line 914, in _bootstrap_inner
    self.run()
  File "<decorator-gen-23>", line 2, in run
  File "/usr/local/lib/python3.5/site-packages/IPython/core/history.py", line 60, in needs_sqlite
    return f(self, *a, **kw)
  File "/usr/local/lib/python3.5/site-packages/IPython/core/history.py", line 834, in run
    self.history_manager.save_flag.wait()
  File "/usr/local/lib/python3.5/threading.py", line 549, in wait
    signaled = self._cond.wait(timeout)
  File "/usr/local/lib/python3.5/threading.py", line 293, in wait
    waiter.acquire()

<Thread(Thread-2, started daemon 140438058526464)>
  File "/usr/local/lib/python3.5/site-packages/pystuck/thread_probe.py", line 15, in thread_frame_generator
    yield (thread_, frame)


In [2]: modules['sys']._current_frames()
Out[2]: {140438058526464: <frame object at 0x7fba3c009a08>, 140438080890624: <frame object at 0x1f127b8>, 140438333286144: <frame object at 0x2651fc8>, 140438198179584: <frame object at 0x7fba44003428>}

In [3]: _[140438333286144]
Out[3]: <frame at 0x7f4bfcf18988>

In [4]: _.f_locals
Out[4]: {'__class__': <class 'gi.overrides.GLib.MainLoop'>, 'self': <GLib.MainLoop object at 0x7fba523c0cb8 (GMainLoop at 0x1e2dfe0)>}
```


# example of gui docker instance
```
export distribution=ubuntu
export version=16.04
export python=3.5

# docker run --rm -it \
# -v /etc/machine-id:/etc/machine-id:ro \
# -v /etc/localtime:/etc/localtime:ro \
# -v /tmp/.X11-unix:/tmp/.X11-unix \
# -e DISPLAY=unix$DISPLAY \
# --device /dev/snd:/dev/snd \
# -v /var/run/dbus:/var/run/dbus \
# -v $HOME/.scudcloud:/home/user/.config/scudcloud \
# --name scudcloud \
# jess/scudcloud
```

# Good projects to follow

- pytest, python3.5, python-dbus, travis: https://github.com/peuter/gosa


# Movement towards integration testing for scarlett_os

Make cover-debug = `py.test -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals`

`py.test -s --tb short tests --benchmark-skip --pdb --showlocals`


# Garbage collection problem in travis test

Test: https://travis-ci.org/bossjones/scarlett_os/builds/191936999

```
tests/test_mpris.py [   <Gio.DBusConnection object at 0x7fc1681c6238 (GDBusConnection at 0x1fa0050)>,
    '/org/scarlett/Listener']
<Gio.DBusConnection object at 0x7fc1681c6238 (GDBusConnection at 0x1fa0050)>
.python3.5: Modules/gcmodule.c:441: visit_reachable: Assertion `gc_refs > 0 || gc_refs == GC_REACHABLE || gc_refs == GC_UNTRACKED' failed.
Makefile:119: recipe for target 'test-travis' failed
make: *** [test-travis] Aborted (core dumped)
```
