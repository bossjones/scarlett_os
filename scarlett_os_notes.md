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
