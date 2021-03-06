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
- pytest, dbus, conftest, pytest.fixture https://github.com/Pelagicore/dbus-proxy/blob/6f8dfcefb83cee5513f4ffcc46f12dcf701598f5/component-test/conftest.py
- pulse, pulsevideo, pytest, integration, FrameCounter https://github.com/wmanley/pulsevideo/blob/d8259f2ce2f3951e380e319c80b9d124b47efdf2/tests/integration_test.py (Allows multiplexing access to webcams such that more than one application can read video from a single piece of hardware at a time.)
- dbus-python: https://cgit.freedesktop.org/dbus/dbus-python/


# Movement towards integration testing for scarlett_os

Make cover-debug = `py.test -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals`

Without Timeout = `pytest -p no:timeout -s --tb short --cov-config .coveragerc --cov scarlett_os tests --cov-report html --benchmark-skip --pdb --showlocals`

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

# dbus testing

```
$ DBUS_SESSION_BUS_ADDRESS=tcp:host=192.168.56.101,port=10010 dbus-send --print-reply --type=method_call --dest=com.example.Test /com/example/Test com.example.Test.TestMethod string:foo


dbus-send \
  --print-reply \
  --dest=org.scarlett \
  --type=mathod_call \
  /org/scarlett/Listener \
  org.scarlett.Listener.emitConnectedToListener \
  variant:string:"ScarlettEmitter"



dbus-send \
--print-reply \
--dest=org.scarlett \
/org/scarlett/Listener \
org.scarlett.Listener.emitConnectedToListener \
variant:string:"ScarlettEmitter"


DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-jDEVlaa4gH,guid=0731db7bb15b0f356987abe7587bf5f6 \


dbus-send \
--session \
--print-reply \
--dest='org.scarlett' \
'/org/scarlett/Listener' \
'org.scarlett.Listener.emitConnectedToListener' \
string:"ScarlettEmitter"


dbus-send \
--session \
--print-reply \
--dest=org.scarlett \
/org/scarlett/Listener \
org.scarlett.Listener1.emitConnectedToListener \
string:"ScarlettEmitter"



 dbus-send --dest=org.freedesktop.ExampleName               \
                       /org/freedesktop/sample/object/name              \
                       org.freedesktop.ExampleInterface.ExampleMethod   \
                       int32:47 string:'hello world' double:65.32       \
                       array:string:"1st item","next item","last item"  \
                       dict:string:int32:"one",1,"two",2,"three",3      \
                       variant:int32:-8                                 \
                       objpath:/org/freedesktop/sample/object/name
```

# sysdig for debugging

```
docker pull sysdig/sysdig

docker run -i -t --name sysdig --privileged -v /var/run/docker.sock:/host/var/run/docker.sock -v /dev:/host/dev -v /proc:/host/proc:ro -v /boot:/host/boot:ro -v /lib/modules:/host/lib/modules:ro -v /usr:/host/usr:ro sysdig/sysdig
```

```
# list process by top CPU inside container @ name
sysdig -pc -c topprocs_cpu container.name=7764d091cf0b

# Show all the interactive commands executed inside the container
sysdig -pc -c spy_users container.name=7764d091cf0b


sysdig evt.type=open and fd.name contains /etc
```

# Solid approach

Target: `multiple modules`

Sticking with main focus of porting everything from python2 to python3 from the `scarlett-dbus-poc` repo, even though it needs to be refactored ... HEAVILY.

Planning on using the `S.O.L.I.D` approach w/ python going forward.

Resources:

- https://github.com/dboyliao/SOLID
- http://www.slideshare.net/DrTrucho/python-solid
- https://www.reddit.com/r/learnpython/comments/4i6tw4/solid_principles_in_python/

Videos:

- https://www.youtube.com/watch?v=wf-BqAjZb8M
- https://www.youtube.com/watch?v=NfngrdLv9ZQ
- https://www.youtube.com/watch?v=TQgB9JFbui0

<img width="628" alt="screen shot 2016-12-23 at 7 05 51 pm" src="https://cloud.githubusercontent.com/assets/709872/21464154/34496f78-c943-11e6-8b22-eb2c493e1286.png">


# pygobject callbacks ! return true or return false

```
#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)

        # Here we connect the "destroy" event to a signal handler.
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Hello World")

        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.button.connect("clicked", self.hello, None)

        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        # This packs the button into the window (a GTK container).
        self.window.add(self.button)

        # The final step is to display this newly created widget.
        self.button.show()

        # and the window
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
```

Also see: https://en.wikibooks.org/wiki/PyGTK_For_GUI_Programming/Signals


# [EVENTS] Return values in pygobject/gtk+ events

**SOURCE:** https://en.wikibooks.org/wiki/PyGTK_For_GUI_Programming/Signals

GTK+ events are similar to signals: they are 'emitted' by specific widgets and can be handled by callback functions. The only differences as far as the PyGTK programmer is concerned are the arguments to a callback function and its return value. As an example, we'll use the 'button_pressed_event' emitted by the gtk.Button widget, which can be connected to a callback function the same way a signal is:

`button.connect('button_press_event', callback_func, callback_data)`

where button is an instance of the gtk.Button object. The callback_data argument, as explained in the previous chapter, is optional. The definition of the callback function contains three arguments: a reference to the widget that emitted the signal, the event and the callback data:

`def callback_func(widget, event, callback_data=None)`

The value returned from this function must be a boolean value (unlike callback functions for signals). This return value is an important message in the GTK+ event mechanism:

* False means that the event was not fully processed so GTK+ should continue doing whatever it usually does when this event occurs and the signal should propagate further.
* True means that the event was fully handled and GTK+ no longer needs to do any further processing in response to the event.

As an example, the 'delete_event' event is emitted from a gtk.Window when the user tries to close the window; if we connect a callback function to this and the function returns False, GTK+ will go on to close the window and emit the 'destroy' signal. If our callback function returns True, however, GTK+ does not close the window itself or emit the 'destroy' signal. This allows us to intervene when someone tries to close a window so we have to opportunity to ask them if, for example, they want to save their work, and then either instruct GTK+ to close the window or leave it open by returning the appropriate values from our callback function.


# pygobject / pygtk signals

**SEE THE FOLLOWING:** https://en.wikibooks.org/wiki/PyGTK_For_GUI_Programming/First_Steps


# Testing ScarlettTasker in ipython

```
from scarlett_os.tasker import ScarlettTasker
from scarlett_os.tasker import player_cb
from scarlett_os.tasker import command_cb
from scarlett_os.tasker import connected_to_listener_cb

from scarlett_os.internal.gi import gi
from scarlett_os.internal.gi import GObject
from scarlett_os.internal.gi import GLib


loop = GLib.MainLoop()

st = ScarlettTasker()
st.prepare(player_cb, command_cb, connected_to_listener_cb)
st.configure()


loop.run()
```

# Patching tricks

```
class TestScarlettTasker(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """
        Method called to prepare the test fixture. This is called immediately before calling the test method; other than AssertionError or SkipTest, any exception raised by this method will be considered an error rather than a test failure. The default implementation does nothing.
        """
        # source: http://stackoverflow.com/questions/7667567/can-i-patch-a-python-decorator-before-it-wraps-a-function
        # Do cleanup first so it is ready if an exception is raised
        def kill_patches():  # Create a cleanup callback that undoes our patches
            mock.patch.stopall()  # Stops all patches started with start()
            imp.reload(tasker)  # Reload our UUT module which restores the original decorator
        self.addCleanup(kill_patches)  # We want to make sure this is run so we do this in addCleanup instead of tearDown

        self.old_glib_exception_error = GLib.GError
        # Now patch the decorator where the decorator is being imported from
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_abort_on_exception = mock.patch('scarlett_os.utility.gnome.abort_on_exception', lambda x: x).start()
        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gi = mock.patch('scarlett_os.internal.gi.gi', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_glib = mock.patch('scarlett_os.internal.gi.GLib', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gobject = mock.patch('scarlett_os.internal.gi.GObject', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_gio = mock.patch('scarlett_os.internal.gi.Gio', spec=True, create=True).start()

        # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        mock_pydbus_SessionBus = mock.patch('pydbus.SessionBus', spec=True, create=True).start()

        # mock_pydbus_SessionBus.return_value

        # mock_time = mock.patch('time.sleep', spec=True, create=True).start()  # The lambda makes our decorator into a pass-thru. Also, don't forget to call start()
        # mock_pydbus.get.side_effect = Exception('GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.scarlett was not provided by any .service files')

        # Exception Thrown from [/home/pi/.virtualenvs/scarlett_os/lib/python3.5/site-packages/pydbus/proxy.py] on line [40] via function [get]
        # Exception type Error:
        # GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name
        # org.scarlett was not provided by any .service files

        # HINT: if you're patching a decor with params use something like:
        # lambda *x, **y: lambda f: f
        imp.reload(tasker)  # Reloads the tasker.py module which applies our patched decorator
```

# Commented out tasker stuff we might care about

```

    # def run_mainloop(self):
    #     try:
    #         self.mainloop_init()
    #     except Exception:
    #         ss_failed_signal.disconnect()
    #         ss_rdy_signal.disconnect()
    #         ss_kw_rec_signal.disconnect()
    #         ss_cmd_rec_signal.disconnect()
    #         ss_cancel_signal.disconnect()
    #         ss_connect_signal.disconnect()
    #         loop.quit()
    #         self.bucket.put(sys.exc_info())
    #         raise

    ###################################################################################################################
    #  From dbus_runner
    ###################################################################################################################
    # def start(self):
    #     """
    #     Start the :func:`gi.MainLoop` to establish DBUS communications.
    #     """
    #     if self.__active:
    #         return
    #
    #     self.__active = True
    #
    #     self.__thread = threading.Thread(target=self.__runner)
    #     self.__thread.daemon = True
    #     self.__thread.start()
    #
    # def __runner(self):
    #     self.__gloop = GLib.MainLoop()
    #     try:
    #         self.__gloop.run()
    #         # Definition: GLib.MainLoop.get_context
    #
    #         # The GLib.MainContext with which the source is associated,
    #         # or None if the context has not yet been added to a source.
    #         # Return type: GLib.MainContext or None
    #
    #         # Gets the GLib.MainContext with which the source is associated.
    #         # You can call this on a source that has been destroyed,
    #         # provided that the GLib.MainContext it was attached to still
    #         # exists (in which case it will return that GLib.MainContext).
    #         # In particular, you can always call this function on the
    #         # source returned from GLib.main_current_source().
    #         # But calling this function on a source whose
    #         # GLib.MainContext has been destroyed is an error.
    #         context = self.__gloop.get_context()
    #         while self.__active:
    #             context.iteration(False)
    #             if not context.pending():
    #                 time.sleep(.1)
    #     except KeyboardInterrupt:
    #         self.__active = False
    #         # env = Environment.getInstance()
    #         # if hasattr(env, "active"):
    #         #     env.active = False
    #
    # def stop(self):
    #     """
    #     Stop the :func:`gobject.MainLoop` to shut down DBUS communications.
    #     """
    #     # Don't stop us twice
    #     if not self.__active:
    #         return
    #
    #     self.__active = False
    #     self.__gloop.quit()
    #     self.__thread.join(5)

    # # from mopidy
    # def mainloop_init(self):
    #     loop = GLib.MainLoop()
    #     context = loop.get_context()
    #     t = threading.Thread(target=self.__mainloop, args=(context,))
    #     t.daemon = True
    #     t.start()
    #
    # # from mopidy
    # def __mainloop(self, context):
    #     while 1:
    #         try:
    #             context.iteration(True)
    #         except Exception:
    #             pass
```


# Patch modules vs patch objects

**source:** http://stackoverflow.com/questions/24995466/assertionerror-altough-the-expected-call-looks-same-as-actual-call

```
AFAIK you can't use patch() like this. Patch target should be a string in the form package.module.ClassName. I don't know much about django but I suppose Note is a class so Note.objects.filter is not something you can import and hence use in patch(). Also I don't think patch() can handle attributes. Actually I don't quite understand why the patch works at all.

Try using patch.object() which is specifically designed to patch class attributes. It implies Note is already imported in your test module.

@mock.patch.object(Note, 'objects')
def test_get_all_notes(self, objects_mock):
    get_notes()
    objects_mock.filter.assert_called_once_with(number=2, new=1)
I've removed autospec because I'm not sure it will work correctly in this case. You can try putting it back if it works.

Another option might be to use patch() on whatever you get with type(Note.objects) (probably some django class).

As I've said I don't know much about django so I'm not sure if these things work.
```

# Anonymous functions

Lambda expressions (sometimes called lambda forms) are used to create anonymous functions. The expression lambda arguments: expression yields a function object.

The unnamed object behaves like a function object defined with:

```
def <lambda>(arguments):
    return expression
```

# next()
```
next(...)
    next(iterator[, default])

    Return the next item from the iterator. If default is given and the iterator
    is exhausted, it is returned instead of raising StopIteration.
```


# analyzing functions / classes using dis module

http://stackoverflow.com/questions/1995418/python-generator-expression-vs-yield


# envs

`DEBUG_CI_DISABLE_FAKESINK` - If set, disable fakesink so we can hear the sounds play


# Current Tasker Workerflow ( Pre Refactor )

Current Tasker workerflow

1. User: Says Scarlett
2. Listener: Gets a keyword match:
  a. call result() w/ struct['hypothesis'], set vars failed = 0, kw_found = 1, use dbus_proxy obj to call dbus_proxy.emitKeywordRecognizedSignal
    i. local var failed_temp = failed + 1
    ii. if failed > 4, use dbus_proxy obj to call dbus_proxy.emitSttFailedSignal(), then call scarlett_reset_listen()
  b. If kw_found == 1 and STT can be decoded, then call run_cmd() w/ struct['hypothesis']

3. Tasker: Go into tasker._keyword_recognized_signal_callback() aka player_cb()

  a. player_cb:
    1a. enumerate args, using i,v
    2a. find case when v is instance tuple
    3a. get length of tuple w/ len(v), set to variable tuple_args
    4a. find number of args based on length. msg, scarlett_sound, command
    5a. use scarlett_sound to construct wavefile path ( path to audio sound )
    6a. run no-op function run_player w/ arg player_generator_func which is CALLABLE. player_generator_func is your generator function.
    7a. player_generator_func gets called via a GObject.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_HIGH), yielding data till finished

  b. command_cb:
    1b. Follow everything from player_cb, playing new acknowledgement sound
    2b. Run commands.Command.check_cmd, passing in kwarg command_tuple=v), save results to command_run_results.
    3b. verify command_run_results is NOT a command NO_OP ... if it is, end callback by returning False.
    4b. Take value of command_run_results and put it into an array using staticmethod SpeakerType.speaker_to_array() w/ arg command_run_results
    5b. run no-op function run_speaker w/ arg speaker_generator_func which is CALLABLE. speaker_generator_func is your generator function, it calls s = speaker.ScarlettSpeaker w/ kargs text_to_speak, wavpath, and skip_player ... this useses Subprocess class to call espeak to a wav file in a temporary wav location.
    6b. run player.ScarlettPlayer w/ path to espeak temporary file _wavepath.
    7b. get instance of DBusRunner
    8b. via DBusRunner object, get_session_bus()
    9b. get dbus_proxy object of MPRIS
    10b. Sleep for 1 second, then call emitListenerCancelSignal()

# Dbus Signal Types

```
############################################################################
# EXAMPLE [ready signal]
# another arg through *arg : :1.0
# another arg through *arg : /org/scarlett/Listener
# another arg through *arg : org.scarlett.Listener
# another arg through *arg : ListenerReadySignal
# another arg through *arg : ('  ScarlettListener is ready', 'pi-listening')
############################################################################

#############################################################################
# EXAMPLE [failed]
# another arg through *arg : :1.0
# another arg through *arg : /org/scarlett/Listener
# another arg through *arg : org.scarlett.Listener
# another arg through *arg : SttFailedSignal
# another arg through *arg : ('  ScarlettListener hit Max STT failures', 'pi-response2')
#############################################################################

#############################################################################
# EXAMPLE [listener]
# another arg through *arg : :1.0
# another arg through *arg : /org/scarlett/Listener
# another arg through *arg : org.scarlett.Listener
# another arg through *arg : KeywordRecognizedSignal
# another arg through *arg : ('  ScarlettListener caught a keyword match', 'pi-listening')
#############################################################################

##############################################################################
# EXAMPLE [command]
# another arg through *arg : :1.0
# another arg through *arg : /org/scarlett/Listener
# another arg through *arg : org.scarlett.Listener
# another arg through *arg : CommandRecognizedSignal
# another arg through *arg : ('  ScarlettListener caught a command match', 'pi-response', 'what time is it')
##############################################################################

###############################################################################
# EXAMPLE [cancel]
# another arg through *arg : :1.0
# another arg through *arg : /org/scarlett/Listener
# another arg through *arg : org.scarlett.Listener
# another arg through *arg : ListenerCancelSignal
# another arg through *arg : ('  ScarlettListener cancel speech Recognition', 'pi-cancel')
###############################################################################

################################################################################
# EXAMPLE [connect]
# another arg through *arg : :1.0
# another arg through *arg : /org/scarlett/Listener
# another arg through *arg : org.scarlett.Listener
# another arg through *arg : ConnectedToListener
# another arg through *arg : ('ScarlettEmitter',)
################################################################################
```

# Testing Tasker

```
# NOTE: RUN THIS INSIDE OF IPYTHON

import os
import sys
import signal
import pytest
import builtins
import threading

import pydbus
import scarlett_os
import scarlett_os.exceptions

import time

from scarlett_os.internal import gi  # noqa
from scarlett_os.internal.gi import Gio  # noqa
from scarlett_os.internal.gi import GObject  # noqa
from scarlett_os.internal.gi import GLib

from scarlett_os import tasker

from scarlett_os.tasker import on_signal_recieved
from scarlett_os.tasker import call_speaker
from scarlett_os.tasker import call_espeak_subprocess
from scarlett_os.tasker import call_player

from scarlett_os.internal.debugger import dump

import scarlett_os.logger

# import faulthandler
# faulthandler.register(signal.SIGUSR2, all_threads=True)

from scarlett_os.internal.debugger import init_debugger
init_debugger()

# from scarlett_os.internal.debugger import enable_remote_debugging
# enable_remote_debugging()


loop = GLib.MainLoop()

tskr = tasker.ScarlettTasker()

# tskr.prepare(catchall_handler, catchall_handler, catchall_handler)

tskr.prepare(on_signal_recieved, on_signal_recieved, on_signal_recieved)

tskr.configure()

loop.run()
```

# How to display info about wav file

```
 ⌁ pi@scarlett-ansible-manual1604-2  ⓔ scarlett_os  ⎇  master S:2 U:19 ?:89  ~/dev/bossjones-github/scarlett_os  soxi fixture_scarlett.wav

Input File     : 'fixture_scarlett.wav'
Channels       : 1
Sample Rate    : 16000
Precision      : 16-bit
Duration       : 18:38:26.82 = 1073709056 samples ~ 5.03301e+06 CDDA sectors
File Size      : 149k
Bit Rate       : 17.8
Sample Encoding: 16-bit Signed Integer PCM

 ⌁ pi@scarlett-ansible-manual1604-2  ⓔ scarlett_os  ⎇  master S:2 U:19 ?:89  ~/dev/bossjones-github/scarlett_os
```

# HOW to make fixture sounds

```
gst-launch-1.0 alsasrc device=plughw:CARD=Device,DEV=0 ! \
                                                queue name=capsfilter_queue \
                                                      leaky=2 \
                                                      max-size-buffers=0 \
                                                      max-size-time=0 \
                                                      max-size-bytes=0 ! \
                                                capsfilter caps='audio/x-raw,format=(string)S16LE,rate=(int)16000,channels=(int)1,layout=(string)interleaved' ! \
                                                audioconvert ! \
                                                audioresample ! \
                                                wavenc ! \
                                                filesink location=fixture_what_time_is_it-riff-little-endian-16bit-16kh-wave-file.wav
```

# HOW to test fixture sounds

```


export SCARLETT_FILE_LOCATION=/home/pi/dev/bossjones-github/scarlett_os/tests/data/samples/fixture_scarlett-riff-little-endian-16bit-16kh-wave-file.wav

gst-launch-1.0 filesrc location="${SCARLETT_FILE_LOCATION}" ! \
                                                queue name=capsfilter_queue \
                                                      leaky=2 \
                                                      max-size-buffers=0 \
                                                      max-size-time=0 \
                                                      max-size-bytes=0 ! \
                                                capsfilter caps='audio/x-raw,format=(string)S16LE,rate=(int)16000,channels=(int)1,layout=(string)interleaved' ! \
                                                audioconvert ! \
                                                audioresample ! \
                                                pocketsphinx \
                                                name=asr \
                                                lm=~/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm \
                                                dict=~/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic \
                                                hmm=~/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us \
                                                bestpath=true ! \
                                                queue name=capsfilter_queue \
                                                      leaky=2 \
                                                      max-size-buffers=0 \
                                                      max-size-time=0 \
                                                      max-size-bytes=0 ! \
                                                fakesink sync=false


# Use this inside of integration testing

gst-launch-1.0 uridecodebin uri="file://${SCARLETT_FILE_LOCATION}" ! \
                                                audioconvert ! \
                                                audioresample ! \
                                                pocketsphinx \
                                                name=asr \
                                                lm=~/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm \
                                                dict=~/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic \
                                                hmm=~/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us \
                                                bestpath=true ! \
                                                fakesink sync=false
```


# Todo list for Scarlett Listener to make it more testable 3/20/2017

- Turn gst_pipeline into a property w/ getter/setter ( Might need to use gobject property instead )
- GstPipeline should be a property instead of part of an array ( I think ) ... maybe dictionary would work too
- Make calls to get pipeline thread safe, use a lock
- make several of the elements properties eg, asr(self.pipeline.get_by_name ), "running" ( returns self._pipeline ).
- create clean functions for start_listening, pause_listening, unpause_listening, stop_listening, reset and close. See Listener_CMU for example. pipeline.py
- add call back member functions. on_level_cb
- use a queue to pass messages back and forth ?
- create a bunch of init_* functions, make sure the complexity isn't too tightly coupled
- ensure that we have the ability to override gst_parse command for testing, and add a timeout
- create a handler to deal with all event related stuff
- borrow logic from ThreadMaster in pitivi especially :

```
        assert issubclass(threadclass, Thread)
        self.log("Adding thread of type %r", threadclass)
        thread = threadclass(*args)
        thread.connect("done", self._threadDoneCb)
```

- move or fix up `ListenerDemo`

- Figure out if we are using the right number of arguments in the following callback member functions:

```

    def thread_finished(self, thread):
        logger.debug("thread_finished.")

    def thread_progress(self, thread):
        logger.debug("thread_progress.")
```

- add a member function to perform a join on get_loop_thread(), that might help w/ cleaning it up
- turn `bus = self._pipeline.get_bus()` into a property as well
- make listener take source as a kwarg eg `source=self.HELLO_WORLD`
- ( long term ) think about using a queue to pass along the messages decoded by pocketsphinx, eg:

```
def test_pipeline_creation( self ):
        p = self.pipeline = pipeline.QueuePipeline(
            context=self.context,
            source=self.HELLO_WORLD
        )
        p.start_listening()
        t = time.time()
        TIMEOUT = t + 20
        result = None
        while time.time() < TIMEOUT:
            message = p.queue.get( True, TIMEOUT-time.time() )
            if message['type'] == 'final':
                result = message
                break
        assert result, "No result message received in 20s"
        assert result['text']
        assert 'hello world' in result['text'], result

    def test_pipeline_default_source_is_alsa( self ):
        self.pipeline = pipeline.QueuePipeline(context=self.context)
        assert self.pipeline.source.continuous
        fragment = self.pipeline.source.gst_fragment()
        assert 'alsasrc' in fragment, fragment

        self.pipeline.source = None
        assert self.pipeline._source is None
```
- gst_bus_stack should be a property!


- it's possible that I broke tests because we're now using these guys:

https://github.com/bossjones/scarlett_os/pull/43/files

CLEAN UP UNIT TESTS, Add same setup as test_tasker and make sure you mock all of the items in there as well.

```
self._handler = DbusSignalHandler()

# Get a dbus proxy and check if theres a service registered called 'org.scarlett.Listener'
# if not, then we can skip all further processing. (The scarlett-os-mpris-dbus seems not to be running)
self.__dr = DBusRunner.get_instance()
```

# PEP 3156 -- Asynchronous IO Support Rebooted: the "asyncio" Module

https://www.python.org/dev/peps/pep-3156/


# borrowed from gbulb

https://github.com/m-labs/gbulb/blob/5631d56eeeb4de7eb1ea883981e7640d204d1684/README.md

```
gbulb - a PEP 3156 event loop based on GLib
Gbulb is a python library that implements a PEP 3156 interface for the GLib main event loop. It is designed to be used together with the tulip reference implementation.

The code needs to be thoroughly tested, it should be considered as unstable for the moment.

Anthony Baire
```

## Divergences with PEP 3156

In GLib, the concept of event loop is split in two classes: GLib.MainContext
and GLib.MainLoop.

The thing is mostly implemented by MainContext. MainLoop is just a wrapper
that implements the run() and quit() functions. MainLoop.run() atomically
acquires a MainContext and repeatedly calls MainContext.iteration() until
MainLoop.quit() is called.

A MainContext is not bound to a particular thread, however is cannot be used
by multiple threads concurrently. If the context is owned by another thread,
then MainLoop.run() will block until the context is released by the other
thread.

MainLoop.run() may be called recursively by the same thread (this is mainly
used for implementing modal dialogs in Gtk).


The issue: given a context, GLib provides no ways to know if there is an
existing event loop running for that context. It implies the following
divergences with PEP 3156:

 - .run_forever() and .run_until_complete() are not guaranteed to run
   immediatly. If the context is owned by another thread, then they will
   block until the context is released by the other thread.

 - .stop() is relevant only when the currently running Glib.MainLoop object
   was created by this asyncio object (i.e. by calling .run_forever() or
   .run_until_complete()). The event loop will quit only when it regains
   control of the context. This can happen in two cases:
    1. when multiple event loop are enclosed (by creating new MainLoop
       objects and calling .run() recursively)
    2. when the event loop has not even yet started because it is still
       trying to acquire the context

It should be wiser not to use any recursion at all. GLibEventLoop will
actually prevent you from doing that (in accordance with PEP 3156). However
you should keep in mind that enclosed loops may be started at any time by
third-party code calling directly GLib's primitives.


# __repr__ and recursive_repr

- https://github.com/RazerM/represent/blob/c7db3d5b9554f170c7324bc410e77de5ee25687f/represent/core.py
- https://github.com/RazerM/represent/blob/d6b90468ff67333ce8ae33980d4201a25df88563/tests/test_helper.py
- https://docs.python.org/3.2/library/reprlib.html

# Visual Studio Code Remote Debug Docker

## install steps

```
# on os x
pip3 install ptvsd
```

# testing ad-hoc notes ( leaks etc )

```
--benchmark-skip -R :


pytest test_mod.py::TestClass::test_method  # run a single method in
                                             # a single class

pytest -k test_player.py --benchmark-skip -R :

from scarlett_os.internal.debugger import dump
from scarlett_os.internal.debugger import pprint_color

py.test --pdb --showlocals -v -R : -k test_speaker.py

py.test --pdb --showlocals -v -R : -k test_integration_threadmanager.py

py.test --pdb --showlocals -v -R : -k test_subprocess.py

py.test --trace-config --debug -p no:pytestipdb -p no:leaks -p no:pbdinvoke --showlocals -v -k test_integration_threadmanager.py

py.test --trace-config --debug --pdb --showlocals -v -R : -k test_subprocess_check_command_type
```


# traceback in pytest

```
 tests/test_subprocess.py::TestScarlettSubprocess.test_subprocess_map_type_to_command ✓                                  80% ████████
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> traceback >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

self = <tests.test_subprocess.TestScarlettSubprocess object at 0x7fcb6508ca80>
mocker = <pytest_mock.MockFixture object at 0x7fcb6508cd58>

    def test_subprocess_check_command_type(self, mocker):
        """Using the mock.patch decorator (removes the need to import builtins)"""

        test_command = ["who", "-b"]
        test_name = 'test_who'
        test_fork = False

        # Mock logger right off the bat
        mocker.patch('scarlett_os.subprocess.logging.Logger.debug')

        # Create instance of Subprocess, disable all checks
        sub = scarlett_os.subprocess.Subprocess(test_command,
                                                name=test_name,
                                                fork=test_fork,
                                                run_check_command=False)

        # Mock instance member functions
        mock_map_type_to_command = mocker.patch.object(sub, 'map_type_to_command')
        mocker.patch.object(sub, 'fork')

        # Set mock return types
        mock_map_type_to_command.return_value = int

        # action
        with pytest.raises(TypeError) as excinfo:
>           sub.check_command_type(test_command)
E           Failed: DID NOT RAISE <class 'TypeError'>

excinfo    = <[AttributeError("'ExceptionInfo' object has no attribute 'typename'") raised in repr()] ExceptionInfo object at 0x7fcb650b7ae8>
mock_map_type_to_command = <MagicMock name='map_type_to_command' id='140511550299064'>
mocker     = <pytest_mock.MockFixture object at 0x7fcb6508cd58>
self       = <tests.test_subprocess.TestScarlettSubprocess object at 0x7fcb6508ca80>
sub        = <subprocess.Subprocess object at 0x7fcb718882b0 (Subprocess at 0x332d580)>
test_command = ['who', '-b']
test_fork  = False
test_name  = 'test_who'

tests/test_subprocess.py:180: Failed
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> entering PDB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
```

# info on how we're running pytest

```
pi@99c42ce46358:~/dev/bossjones-github/scarlett_os$ py.test --pdb --showlocals -v -R : -k test_subprocess.py
/usr/local/lib/python3.5/site-packages/_pdbpp_path_hack/pdb.py:4: ResourceWarning: unclosed file <_io.TextIOWrapper name='/usr/local/lib/python3.5/site-packages/pdb.py' mode='r' encoding='UTF-8'>
  os.path.dirname(os.path.dirname(__file__)), 'pdb.py')).read(), os.path.join(
Test session starts (platform: linux, Python 3.5.2, pytest 3.0.7, pytest-sugar 0.8.0)
cachedir: .cache
benchmark: 3.1.0a2 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /home/pi/dev/bossjones-github/scarlett_os, inifile: setup.cfg
plugins: flakefinder-0.1.0, mock-1.6.0, ipdb-0.1.dev2, ordering-0.5, leaks-0.2.2, xdist-1.15.0, interactive-0.1.1, catchlog-1.2.2, sugar-0.8.0, cov-2.4.0, benchmark-3.1.0a2, timeout-1.2.0, rerunfailures-2.1.0
timeout: 60.0s method: signal
[DBUS_SESSION_BUS_ADDRESS]: unix:path=/tmp/dbus_proxy_outside_socket

 tests/test_subprocess.py::TestScarlettSubprocess.test_check_pid_os_error ✓                                              20% ██
 tests/test_subprocess.py::TestScarlettSubprocess.test_check_pid ✓                                                       40% ████
 tests/test_subprocess.py::TestScarlettSubprocess.test_subprocess_init ✓                                                 60% ██████
 tests/test_subprocess.py::TestScarlettSubprocess.test_subprocess_map_type_to_command ✓                                  80% ██████
```

# python 3.5.2 unittest.mock vs mock ( THEY ARE DIFFERENT )

https://mock.readthedocs.io/en/latest/

IS IT WORKING:
https://travis-ci.org/testing-cabal/mock

```
mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions about how they have been used.

mock is now part of the Python standard library, available as unittest.mock in Python 3.3 onwards. However, if you are writing code that runs on multiple versions of Python the mock package is better, as you get the newest features from the latest release of Python available for all Pythons.

The mock package contains a rolling backport of the standard library mock code compatible with Python 2.6 and up, and 3.3 and up. Python 3.2 is supported by mock 1.3.0 and below - with pip no longer supporting 3.2, we cannot test against that version anymore.

Please see the standard library documentation for usage details.
```

# pytest-mock, python 3.5.2, unittest, and why we need to keep running stopall()

### This was the first working commit I had w/ the technologies above working correctly together
https://github.com/bossjones/scarlett_os/pull/47/commits/2b7d190db9276f6f37b67ab2f5c092c1a7061dd3

### How to get the error to come back?
- Remove mocker.stopall() from either the beginning of each test, or the end of each test.
- Switch back to using mock instead of unittest.mock on python 3.5.2 when `mock_use_standalone_module = True` inside of setup.cfg ( or tox.ini, pytest.ini )
- Seems like it only works on instance objects, and possibly their method functions
- command we used: `py.test --pdb --showlocals -v -R : -k test_subprocess.py`

```
NOTE:
source: https://github.com/ryanhiebert/tox-travis/blob/master/tox.ini#L5
# mock is required to allow mock_use_standalone_module
# Coverage doesn't work on PyPy or Python 3.2
```


### Resources used to debug issue
- "unittest.mock small gotcha - a humbling tale of failure 2017 article" - https://allanderek.github.io/posts/unittestmock-small-gotcha/
- https://github.com/pytest-dev/pytest-mock/blob/master/pytest_mock.py#L13 ( _get_mock_module )
- https://github.com/pytest-dev/pytest-mock/commit/891ee7e6daaec99fffa0ab5db34e3bfe044c3dd6 this version of above ^
- This gave me the hint that this wasn't actually working on all python versions out there: https://github.com/pytest-dev/pytest-mock/blob/master/test_pytest_mock.py#L11
- dump() and pprint_color() functions
- https://github.com/search?p=3&q=%22yield+mpatch%22&type=Code&utf8=%E2%9C%93
- pattern! Everything in pytest 3.5.2 seems to be dealing with some sort of weird issue isolated to THAT version of python! https://github.com/pytest-dev/pytest/issues/2180
- python 3.5.2 monkeypatcing issues again https://github.com/pytest-dev/pytest/issues/1938
- Started to give me the idea that we might need to undo manually on each test run https://github.com/pytest-dev/pytest/commit/5eaac194164ed09f55ee6578860ceeb0797fdae0#diff-b7f6c224f9e3b3dd1ed445e9b2f0fa55
- This guy gave a good hint on proper locations to mock from, etc.. ( originally found him in gitter in a russian chat about the same issue ) https://github.com/pytest-dev/pytest-mock/issues/60

https://gitter.im/dev-ua/python/archives/2016/08/24

```
@pytest.mark.asyncio
async def test_async_func2(mocker):
    mock_async_func2 = mocker.patch(__name__ + '.async_func2')
    async def return_async_value(val):
        return val
    mock_async_func2.return_value = return_async_value('something')
    res = await async_func1()
    mock_async_func2.assert_called_once_with()
    assert res == 'something'
```

- More github searchs this time on `mocker.patch(__name__` - https://github.com/search?p=2&q=mocker.patch%28__name__&type=Code&utf8=%E2%9C%93
- githun search `"yield mpatch"` - https://github.com/search?p=3&q=%22yield+mpatch%22&type=Code&utf8=%E2%9C%93
- "I need to mock a function and all references which point to this function." - http://widequestion.com/question/mock-function-and-references-to-this-function/
- "How to patch a module's internal functions with mock? [Resolved]" - http://blogs.candoerz.com/question/185650/how-to-patch-a-module39s-internal-functions-with-mock.aspx
- "Python - Mocking chained function calls" - https://stackoverflow.com/questions/34308511/python-mocking-chained-function-calls
- "PYTEST: MORE ADVANCED FEATURES FOR EASIER TESTING" - http://programeveryday.com/post/pytest-more-advanced-features-for-easier-testing/
- "WHERE TO PATCH: Mocks and Monkeypatching in Python" https://semaphoreci.com/community/tutorials/mocks-and-monkeypatching-in-python
- https://github.com/ryanhiebert/tox-travis/blob/master/tox.ini#L5


# pytest 3.0.7 monkeypath busted?

### Workaround:

```
# source: https://github.com/pytest-dev/pytest/issues/363
@pytest.fixture(scope="session")
def monkeysession(request):
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
```

See https://github.com/pytest-dev/pytest/issues/363


# aufs bug
### AKA: Permission denied for directories created automatically by Dockerfile ADD command

Taken from https://github.com/moby/moby/issues/1295

I'm going to lock the discussion on this issue, because it has become a kitchensink for anything related to "permissions".

The original issue reported here was fixed more than 3 years ago in docker#1316. Some issues
remained due to an issue in aufs; issue (#783), and are resolved by newer aufs versions. To quote jpetazzo again on that issue:

```
When a directory has a given permission mask in a lower layer, the upper layers cannot have a broader mask.
I was able to work around the Permission denied error by switching to devicemapper instead of aufs, since changing the image was not a practical solution to me.
Note that that only applies to those that run aufs and run an old version of it.
```

For other issues discussed here;

- When ADD-ing or COPY-ing files to an image, those files are always owned by root. If you have a USER instruction in your Dockerfile, that may result in that user not being able to read, chown or chmod those files. This is expected behavior. A pull request for changing this behavior through a --user flag is currently reviewed; docker#28499

- When bind-mounting files from your host to the container at runtime and on a Linux host, permissions of the files on the host are maintained. This can result in the process in the container not being able to access them (i.e., because the process is not running as "your personal account on the host"). Change permissions of the files to match the uid/gid of the process in the container, also see my answer on StackOverflow for some hints.

- When bind-mounting files from your host to the container at runtime on a Mac or Windows machine, and docker runs in a VirtualBox VM; those files are always owned by uid:gid 1000:1000. You cannot change permissions on those files, which is due to limitations in VirtualBox guest additions. Use an actual volume (docker volume create) for those files, or run the process inside the container as 1000:1000, but this may require changes to your Dockerfile / image. Read the discussion on issue #581 in the boot2docker issue tracker for more information

- When bind-mounting files from your host to the container on a Mac running Docker for Mac, there is some "magic" built-in to ignore ownership; the process inside the container always gets access. Read the troubleshooting section for Docker for Mac or Docker for Windows if you're running into issues.

For other issues; open a new bug report if you suspect there's a bug, but please make sure there's no existing issue, or if your problem falls in one of those mentioned above.



# Config research

### Check this guy out

https://github.com/bvujicic/yml-to-env/blob/ed0e4b61ac0c9ca356084c1820db30312c3e05f7/yml_config/__init__.py

dot notation on yaml configs: https://stackoverflow.com/questions/39463936/python-accessing-yaml-values-using-dot-notation


### Make sure you are using the latest setuptools

`pip3 install --upgrade pip setuptools wheel`

### dumping a dictionary to a YAML file while preserving order ( ruamel.yaml )

**Source: https://stackoverflow.com/questions/31605131/dumping-a-dictionary-to-a-yaml-file-while-preserving-order**

```
DEFAULT_CONFIG = """
scarlett:
  # Omitted values in this section will be auto detected using freegeoip.io

  # Name for Scarlett to call user
  owners_name: 'Hair Ron Jones'

  pocketsphinx:
      hmm: /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
      lm: /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
      dict: /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
      silprob: 0.1
      wip: 1e-4
      bestpath: 0

  keywords_list:
  - 'scarlett'
  - 'SCARLETT'

  features:
  - time
  - help
  - party
"""

# Out[19]:
# CommentedMap([('scarlett',
#                CommentedMap([('owners_name', 'Hair Ron Jones'),
#                              ('pocketsphinx',
#                               CommentedMap([('hmm',
#                                              '/home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us'),
#                                             ('lm',
#                                              '/home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm'),
#                                             ('dict',
#                                              '/home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic'),
#                                             ('silprob', 0.1),
#                                             ('wip', 0.0001),
#                                             ('bestpath', 0)])),
#                              ('keywords_list', ['scarlett', 'SCARLETT']),
#                              ('features', ['time', 'help', 'party'])]))])

# In [20]:

data = ruamel.yaml.load(DEFAULT_CONFIG, Loader=ruamel.yaml.RoundTripLoader)
print(data)
ruamel.yaml.dump(data, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper)
```


# s6 related stuff ( Taken from docker-base )

### Tools

- [S6](https://github.com/just-containers/s6-overlay) process supervisor is used for `only` for zombie reaping (as PID 1), boot coordination, and termination signal translation
- [Goss](https://github.com/aelsabbahy/goss) is used for build-time testing
- [Dgoss](https://github.com/aelsabbahy/goss/tree/master/extras/dgoss) is used for run-time testing.

### Expectations

To add a service to be monitored, simply create a service script: https://github.com/just-containers/s6-overlay#writing-a-service-script
For programmatic switches, create the service in `/etc/services-available`, and symlink to `/etc/services.d` to enable


### Advanced Modification

More advanced changes can take effect using the `run.d` system. Similar to the `/etc/cont-init.d/` script system, any shell scripts (ending in .sh) in the `/run.d/` folder will be executed ahead of the S6 initialization.

- If a `run.d` script terminates with a non-zero exit code, container will stop, terminating with the script's exit code, unless...
- If script terminates with exit code of $SIGNAL_BUILD_STOP (99), this will signal the container to stop cleanly. This can be used for a multi-stage build process


### Long-running processes (workers + crons)

This container image can be used with multiple entrypoints (not to be confused with Docker entrypoints).
For example, a codebase that runs a web service, but also requires crons and background workers. These processes should not run inside the same container (like a VM would), but can be executed separately from the same image artifact by adding arguments to the `run` command.

`docker run {image_id} /worker.sh 3 /bin/binary -parameters -that -binary -receives`

Runs `3` copies of `/bin/binary` that receives the parameters `-parameters -that -binary -receives`


### Container Organization

Besides the instructions contained in the Dockerfile, the majority of this
container's use is in configuration and process. The `./container/root` repo directory is overlayed into a container during build. Adding additional files to the folders in there will be present in the final image. All paths from the following explanation are assumed from the repo's `./root/` base:

Directory | Use
--- | ---
`/etc/cont-init.d/` | startup scripts that run ahead of services booting: https://github.com/just-containers/s6-overlay#executing-initialization-andor-finalization-tasks
`/etc/fix-attrs.d/` | scripts that may fix permissions at runtime: https://github.com/just-containers/s6-overlay#fixing-ownership--permissions
`/etc/services.d/` |  services that will be supervised by S6: https://github.com/just-containers/s6-overlay#writing-a-service-script
`/etc/services-available/` | same as above, but must be symlinked into `/etc/services.d/` to take effect
`/run.d/` | shell scripts (ending in .sh) that make runtime modifications ahead of S6 initialization
`/scripts` | convenience scripts that can be leveraged in derived images

----------------------------

# Broken pip + setuptools
## AKA ( _NamespacePath object has no attribute sort (31.0.0) )

Links to git issues:

- https://github.com/pypa/setuptools/issues/885
- https://github.com/pypa/pip/issues/4216
- https://github.com/yougov/pmxbot/commit/c227caf3794d840f992151d1749302f7097a896f
- https://github.com/pypa/pip/commit/eaccb88674beff75bb98a1d1e2d53a26a9c63890
- https://github.com/pypa/setuptools/commit/d9c9284e19ce475c2366b279dd4db82a2751a571

### Error in question

```
pi@70acac127862:~/dev/bossjones-github/scarlett_os$ pip install cryptography
Traceback (most recent call last):
  File "/usr/local/bin/pip", line 7, in <module>
    from pip import main
  File "/usr/local/lib/python3.5/site-packages/pip/__init__.py", line 14, in <module>
    from pip.utils import get_installed_distributions, get_prog
  File "/usr/local/lib/python3.5/site-packages/pip/utils/__init__.py", line 27, in <module>
    from pip._vendor import pkg_resources
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2927, in <module>
    @_call_aside
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2913, in _call_aside
    f(*args, **kwargs)
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2952, in _initialize_master_working_set
    add_activation_listener(lambda dist: dist.activate())
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 956, in subscribe
    callback(dist)
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2952, in <lambda>
    add_activation_listener(lambda dist: dist.activate())
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2515, in activate
    declare_namespace(pkg)
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2097, in declare_namespace
    _handle_ns(packageName, path_item)
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2047, in _handle_ns
    _rebuild_mod_path(path, packageName, module)
  File "/usr/local/lib/python3.5/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2066, in _rebuild_mod_path
    orig_path.sort(key=position_in_sys_path)
AttributeError: '_NamespacePath' object has no attribute 'sort'
```

### Debugging: Determine what's in python path

Based on this [observation](https://github.com/pypa/setuptools/issues/885#issuecomment-266606086):

[@jaraco](https://github.com/jaraco) The bug happens trying to import `setuptools`/`pkg_resources` in an environment where a namespace package is installed, but where there is more than one directory in the path of the namespace package (e.g., one package in a "development install" vs. dependencies installed into `site-packages`).

In [@jkbbwr](https://github.com/jkbbwr)'s case above, what would cause `zope.__path__` to be an instance of `_NamespacePath` rather than the plain list that the code in `pkg_resources._rebuild_mod_path` clearly expects? That class appears only to be instantiated by the stdlib's import machinery under Python 3.5+:

*   `importlib._bootstrap_external._NamespaceLoader.__init__`
*   `importlib._bootstrap_external.PathFinder.find_spec`.

As a hackaround, one might add monkeypatch a `sort` method onto `importlib._bootstrap_external._NamespacePath`. ;)


`....`

So, first up, lets list what's in our python path currently:

`python -c "import sys; print('\n'.join(sys.path))"`

```
pi@91c2236d8a47:~/dev/bossjones-github/scarlett_os$ python -c "import sys; print('\n'.join(sys.path))"

/home/pi/jhbuild/lib/python3.5/site-packages
/usr/lib/python3.5/site-packages
/usr/local/lib/python35.zip
/usr/local/lib/python3.5
/usr/local/lib/python3.5/plat-linux
/usr/local/lib/python3.5/lib-dynload
/usr/local/lib/python3.5/site-packages
pi@91c2236d8a47:~/dev/bossjones-github/scarlett_os$

pi@91c2236d8a47:~/dev/bossjones-github/scarlett_os$ jhbuild run -- python -c "import sys; print('\n'.join(sys.path))"
I: Modulesets were edited locally but JHBuild is configured to get them from the network, perhaps you need to add use_local_modulesets = True to your /home/pi/.jhbuildrc.

/usr/local/share/jhbuild/sitecustomize
/home/pi/jhbuild/lib/python3.5/site-packages
/usr/lib/python3.5/site-packages
/usr/local/lib/python35.zip
/usr/local/lib/python3.5
/usr/local/lib/python3.5/plat-linux
/usr/local/lib/python3.5/lib-dynload
/usr/local/lib/python3.5/site-packages
pi@91c2236d8a47:~/dev/bossjones-github/scarlett_os$
```

`...`

via [jaraco](https://github.com/pypa/setuptools/issues/885#issuecomment-266921037):

`Working with the google-auth library, I find that if I set usedevelop = True in the tox settings, the issue doesn't occur. This behavior indicates to me that the issue lies in part with a package which is duplicately installed. In any case, I was able to use it to create a test case that captures the error.`


### Tried downgrading for a second, no luck:

`pip3 install --no-cache-dir --upgrade --force-reinstall "setuptools==31.0.1"`


### What does vendoring mean?

https://gist.github.com/datagrok/8577287

```
Vendoring is the moving of all 3rd party items such as plugins, gems and even rails into the /vendor directory. This is one method for ensuring that all files are deployed to the production server the same as the dev environment.
```

### This is the soluton that ended up working

Seems like issue https://github.com/pypa/pip/issues/4216 is halted at the moment ... most likely because the devs are busy or they're working on rolling out version 10 of pip instead which will fix this problem w/ 9.0.1. For now, decided to use the patch that `pradyunsg ` put together that involves installing pip like this: `pip install --ignore-installed --pre "https://github.com/pradyunsg/pip/archive/hotfix/9.0.2.zip#egg=pip"`. We locked it to our own fork just to prevent any other changes from happening after today 7/22/2017 ... just in case. But will keep an eye on things.

# ssh to container

example repo: https://github.com/jeroenpeeters/docker-ssh
