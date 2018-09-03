# install sphinx osx

**re: https://github.com/vscode-restructuredtext/vscode-restructuredtext/blob/master/docs/sphinx.md**

`ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include" pip3 install sphinx sphinx-autobuild restructuredtext-lint`


# try this

```
#!/usr/bin/with-contenv execlineb

# Import defaults from linked container.
# with-contenv

# # ================== Cron entry point ===============================================================
# # How to use:
# # /app/bin/cron_runner service.name [additional_args]
# #
# # Note - /init.sh will load environment variables, then the traditional `/app/bin/cron $@` cron runner
# # ====================================================================================================

# # Signal to init processes to avoid any webserver startup, really anything but `web` will be fine
# # export CONTAINER_ROLE='cron'

# # Begin startup/run.d sequence
# /init.sh

# STATUS=$?  # Captures exit code from script that was run

# # /app/bin/cron $@

# # /worker.sh 1 /app/bin/cron migration

# # if [[ $SCARLETT_BUILD_GNOME != true ]]; then
# #   echo " [run] SCARLETT_BUILD_GNOME not set, moving on ..."
# #   exit
# # fi

# # TODO this exit code detection is also present in run.sh, needs to be combined
# if [[ $STATUS == $SIGNAL_BUILD_STOP ]]
# then
#   echo "[worker] container exit requested"
#   exit # Exit cleanly
# fi

# if [[ $STATUS != 0 ]]
# then
#   echo "[scarlett_os] failed to init"
#   exit $STATUS
# fi


# # # Start process manager
# # echo "[run] starting process manager"
# # exec /init

# echo "\
# #!/usr/bin/execlineb -P

# with-contenv
# s6-setuidgid pi

# foreground {
#   s6-applyuidgid -u 1000 -g 1000
#   cd /home/pi/dev/bossjones-github/scarlett_os
#   make test-travis
# }
# s6-true" > '/tmp/ci.sh'

# exec s6-setuidgid pi /bin/bash -C '/tmp/ci.sh'

foreground { s6-echo " [run] multisubstitute for HOME and XDG_RUNTIME_DIR" }

# s6-envuidgid potentially sets the UID, GID and GIDLIST environment variables according to the options and arguments it is given; then it executes into another program.
s6-envuidgid pi
multisubstitute
{
  importas CURRENT_DIR CURRENT_DIR
  importas DEBIAN_FRONTEND DEBIAN_FRONTEND
  importas ENABLE_GTK ENABLE_GTK
  importas ENABLE_PYTHON3 ENABLE_PYTHON3
  importas GID GID
  importas GITHUB_BRANCH GITHUB_BRANCH
  importas GITHUB_REPO_NAME GITHUB_REPO_NAME
  importas GITHUB_REPO_ORG GITHUB_REPO_ORG
  importas GST_PLUGIN_PATH GST_PLUGIN_PATH
  importas GSTREAMER GSTREAMER
  importas HOME HOME
  importas JHBUILD JHBUILD
  importas LANG LANG
  importas LANGUAGE_ID LANGUAGE_ID
  importas LC_ALL LC_ALL
  importas LD_LIBRARY_PATH LD_LIBRARY_PATH
  importas MAIN_DIR MAIN_DIR
  importas NOT_ROOT_USER NOT_ROOT_USER
  importas NOTVISIBLE NOTVISIBLE
  importas PATH PATH
  importas PI_HOME PI_HOME
  importas PIP_DOWNLOAD_CACHE PIP_DOWNLOAD_CACHE
  importas PKG_CONFIG_PATH PKG_CONFIG_PATH
  importas PREFIX PREFIX
  importas PROJECT_HOME PROJECT_HOME
  importas PYTHON PYTHON
  importas PYTHON_VERSION PYTHON_VERSION
  importas PYTHON_VERSION_MAJOR PYTHON_VERSION_MAJOR
  importas PYTHONPATH PYTHONPATH
  importas PYTHONSTARTUP PYTHONSTARTUP
  importas PYTHONUNBUFFERED PYTHONUNBUFFERED
  importas SCARLETT_CONFIG SCARLETT_CONFIG
  importas SCARLETT_DICT SCARLETT_DICT
  importas SCARLETT_HMM SCARLETT_HMM
  importas SCARLETT_LM SCARLETT_LM
  importas SIGNAL_BUILD_STOP SIGNAL_BUILD_STOP
  importas SKIP_GOSS_TESTS_GTK_DEPS SKIP_GOSS_TESTS_GTK_DEPS
  importas SKIP_GOSS_TESTS_JHBUILD SKIP_GOSS_TESTS_JHBUILD
  importas SKIP_ON_TRAVIS SKIP_ON_TRAVIS
  importas SKIP_TRAVIS_CI_PYTEST SKIP_TRAVIS_CI_PYTEST
  importas STOP_AFTER_GOSS_GTK_DEPS STOP_AFTER_GOSS_GTK_DEPS
  importas STOP_AFTER_GOSS_JHBUILD STOP_AFTER_GOSS_JHBUILD
  importas TRAVIS_CI TRAVIS_CI
  importas TRAVIS_CI_PYTEST TRAVIS_CI_PYTEST
  importas UID UID
  importas UNAME UNAME
  importas USER USER
  importas USER_HOME USER_HOME
  importas USER_SSH_PUBKEY USER_SSH_PUBKEY
  importas VIRT_ROOT VIRT_ROOT
  importas VIRTUALENV_WRAPPER_SH VIRTUALENV_WRAPPER_SH
  importas VIRTUALENVWRAPPER_PYTHON VIRTUALENVWRAPPER_PYTHON
  importas VIRTUALENVWRAPPER_SCRIPT VIRTUALENVWRAPPER_SCRIPT
  importas VIRTUALENVWRAPPER_VIRTUALENV VIRTUALENVWRAPPER_VIRTUALENV
  importas WORKON_HOME WORKON_HOME
  importas XDG_CONFIG_DIRS XDG_CONFIG_DIRS
  importas XDG_DATA_DIRS XDG_DATA_DIRS
  importas XDG_RUNTIME_DIR XDG_RUNTIME_DIR
}

foreground { s6-echo " [run] TEST_PATH is ${TEST_PATH}" }
foreground { s6-echo " [run] HOME is ${HOME}" }
foreground { s6-echo " [run] XDG_RUNTIME_DIR is ${XDG_RUNTIME_DIR}" }
foreground { s6-echo " [run] PATH is ${PATH}" }

multisubstitute {
    import -D "1000" UID
    import -D "1000" GID
}

# Set uid to 1000 now
# NOTE: s6-env -i program
# -i Invoke utility with exactly the environment specified by the arguments; the inherited environment shall be ignored completely.
foreground {
    s6-env -i
    UID=$UID
    GID=$GID
    XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR
    s6-dumpenv -- /var/run/s6/container_environment
}
foreground { s6-echo " [run] AFTER s6-env -i" }
# foreground { s6-env }

# verify that we're the correct user, pi
foreground {
    s6-applyuidgid -u 1000 -g 1000 w
}
foreground {
    s6-applyuidgid -u 1000 -g 1000 id
}
foreground {
    s6-applyuidgid -u 1000 -g 1000 who
}
foreground {
    s6-echo " [run] Get env vars directly from pi user"
}

foreground {
    s6-applyuidgid -u 1000 -g 1000 env
}

foreground {
    s6-echo " [run] s6-envuidgid root mkdir -p ${XDG_RUNTIME_DIR}/env"
}

# NOTE: These guys are new and might break everything
foreground {
    s6-envuidgid root mkdir -p ${XDG_RUNTIME_DIR}/env
}

foreground {
    s6-echo " [run] s6-envuidgid pi s6-chown -U ${XDG_RUNTIME_DIR}"
}

foreground {
    s6-envuidgid pi s6-chown -U ${XDG_RUNTIME_DIR}
}

foreground {
    s6-echo " [run] s6-envuidgid pi s6-chown -U ${XDG_RUNTIME_DIR}/env"
}

foreground {
    s6-envuidgid pi s6-chown -U ${XDG_RUNTIME_DIR}/env
}

foreground {
    s6-echo " [run] s6-applyuidgid -u 1000 -g 1000 umask 022 s6-dumpenv -- ${XDG_RUNTIME_DIR}/env"
}

foreground {
    s6-applyuidgid -u 1000 -g 1000 umask 022 s6-dumpenv -- ${XDG_RUNTIME_DIR}/env
}

foreground {
    s6-echo " [run] cd /home/pi/dev/bossjones-github/scarlett_os"
}

# foreground {
#     cd /home/pi/dev/bossjones-github/scarlett_os
#     s6-applyuidgid -u 1000 -g 1000 umask 022 make -- test-travis
#     # s6-envuidgid pi
#     # s6-setuidgid pi /bin/bash -C 'cd /home/vagrant/dev/bossjones-github/scarlett_os && make test-travis'
#     # cd /home/vagrant/dev/bossjones-github/scarlett_os
#     # make test-travis
#     importas REXIT ?
#     foreground { s6-echo " [run] make test-travis exited ${REXIT}." }
#     foreground { s6-echo " [run] make test-travis ran succesfully fool" }
# }


foreground {
    # NOTE: if program
    # if [ -X ] [ -n ] [ -t | -x exitcode ] { prog1... } prog2...
    # if will exit if prog1... exits false. To use it in an execline script that must run prog3... no matter the result of the test, use a foreground wrapper:
    # foreground { if { prog1... } prog2... } prog3...
    # -X : treat a crash of prog1 as a non-zero ("false") exit.
    # -n : negate the test (exit on true, exec into prog2 on false)
    # -x exitcode : exit exitcode instead of 1 if the test fails.
    # -t : exit 0 instead of 1 if the test fails. This is equivalent to -x 0.
    if {
        if { s6-echo " [run] lets start these goss tests..." }
        # NOTE: verify that we're the correct user, pi
        ifelse { s6-test $SKIP_TRAVIS_CI_PYTEST = false }
        {
            foreground {
                s6-applyuidgid -u 1000 -g 1000
                cd /home/pi/dev/bossjones-github/scarlett_os
                make test-travis
            }
        } s6-true
        # NOTE: UNCOMMENT THIS LINE IF YOU NEED TO TEST THIS LOGIC WITHOUT RUNNING TESTS # foreground { s6-echo " [run] pretend we just ran s6-applyuidgid -u 1000 -g 1000 /usr/local/bin/goss -g /tests/goss.jhbuild.yaml validate --retry-timeout 30s --sleep 1s" }
        # foreground { s6-echo " [run] pretend we just ran s6-applyuidgid -u 1000 -g 1000 /usr/local/bin/goss -g /tests/goss.jhbuild.yaml validate --retry-timeout 30s --sleep 1s" }
        # NOTE: importas program
        # importas [ -i | -D default ] [ -u ] [ -s ] [ -C | -c ] [ -n ] [ -d delim ] variable envvar prog...
        # D default : If this option is given and envvar is undefined, substitute default for the value of variable instead of no word. For instance, to substitute the empty word, use -D "".
        # -i : Insist. If envvar is undefined, importas will not do anything; instead, it will exit 100 with an error message. This has precedence over any -D option.
        # -u : Unexport. envvar will be removed from the environment after the substitution. importas -u variable envvar is equivalent to importas variable envvar unexport envvar.
        # Other options are used to control the substitution mechanism.
        importas REXIT ?
        foreground { s6-echo " [run] pytest exited ${REXIT}." }
        foreground { s6-echo " [run] pytest tests ran succesfully fool" }
    }
}

if -t { s6-test $TRAVIS_CI_PYTEST = true }
foreground { s6-echo " [run] TRAVIS_CI_PYTEST: '${TRAVIS_CI_PYTEST}' ... sending signal build stop" }
exit ${SIGNAL_BUILD_STOP}

```


# pep8 Error code meaning and option

Below is the rough classification (extracted from source codes)

**SOURCE: https://blog.sideci.com/about-style-guide-of-python-and-linter-tool-pep8-pyflakes-flake8-haking-pyling-7fdbe163079d**

```
Error and warning
Starting with E … errors
Starting with W … warnings
100 type … indentation
200 type … whitespace
300 type … blank lines
400 type … imports
500 type … line length
600 type … deprecation
700 type … statements
900 type … syntax errors
```


# Flake8 Error code meaning

```
The error code of flake8 are E***, W*** used in pep8 and F*** and C9**.

E***/W***: Error and warning of pep8
F***: Detection of PyFlakes
C9**: Detection of circulate complexity by McCabe
You can see the description of error code in this document.
```


# Debug GST Warning

Source: https://lists.freedesktop.org/archives/gstreamer-devel/2016-June/058941.html

### Example warning message

```
(process:77249): GLib-GObject-CRITICAL **: g_param_spec_boxed: assertion 'G_TYPE_IS_BOXED (boxed_type)' failed

(process:77249): GLib-GObject-CRITICAL **: g_object_class_install_property: assertion 'G_IS_PARAM_SPEC (pspec)' failed

(process:77249): GLib-GObject-WARNING **: gsignal.c:1681: return value of type '<invalid>' for signal "GstPlayBin::get_video_tags" is not a value type

(process:77249): GLib-GObject-WARNING **: gsignal.c:1681: return value of type '<invalid>' for signal "GstPlayBin::get_audio_tags" is not a value type

(process:77249): GLib-GObject-WARNING **: gsignal.c:1681: return value of type '<invalid>' for signal "GstPlayBin::get_text_tags" is not a value type

(process:77249): GLib-GObject-WARNING **: gsignal.c:1673: parameter 1 of type '<invalid>' for signal "GstPlayBin::convert_sample" is not a value type
```


Set the following:

`G_DEBUG=fatal_warnings`


EG.

```
 ⌁ pi@scarlett-ansible-manual1604-2  ⓔ scarlett_os  ⎇  master S:2 U:23 ?:120  ~/dev/bossjones-github/sc
arlett_os  G_DEBUG=fatal_warnings jhbuild run -- pylint -E scarlett_os/listener.py
Using config file /home/pi/dev/bossjones-github/scarlett_os/pylintrc
************* Module scarlett_os.listener
E:477, 8: Instance of 'ScarlettListenerI' has no 'play' member (no-member)
E:494,59: Instance of 'ScarlettListenerI' has no 'on_cancel_listening' member (no-member)

(process:29111): GLib-GObject-WARNING **: /home/pi/gnome/glib/gobject/gsignal.c:1675: parameter 1 of type '<invalid>' for signal "GstBus::sync_message" is not a value type
Trace/breakpoint trap (core dumped)
```

Based on this via https://lists.freedesktop.org/archives/gstreamer-devel/2016-June/058983.html:

```
The problem looks like it is using multiple versions of GStreamer
and/or other libraries in the same process, and they are conflicting
with each other then. So maybe also make sure that you did the
relocation correctly for all dynamic libraries that are used in the
process, and not some of them still try to load another version of some
library from the old place.
```


# Fakegir

fakegir: Bring autocompletion to your PyGObject code

https://github.com/strycore/fakegir

# Example output from Fakegir testing

```
Checking Atk.py
Checking Atspi.py
Checking Cally.py
Checking Clutter.py
Checking ClutterGdk.py
Checking ClutterGst.py
Checking ClutterX11.py
Checking Cogl.py
Checking CoglPango.py
Checking DBus.py
Checking DBusGLib.py
Checking GIRepository.py
Checking GL.py
Checking GLib.py
Checking GModule.py
Checking GObject.py
Checking GSSDP.py
Checking GUPnP.py
Checking GUPnPIgd.py
Checking GUdev.py
Checking Gdk.py
Checking GdkPixbuf.py
Checking GdkX11.py
Checking Gee.py
Traceback (most recent call last):
  File "Gee.py", line 2, in <module>
    import Gee
  File "/Users/malcolm/.cache/fakegir/gi/repository/Gee.py", line 93, in <module>
    class AbstractBidirList(Gee.AbstractList, Gee.BidirList):
AttributeError: module 'Gee' has no attribute 'AbstractList'
Checking Gio.py
Checking Gitg.py
Traceback (most recent call last):
  File "Gitg.py", line 3, in <module>
    import Gitg
  File "/Users/malcolm/.cache/fakegir/gi/repository/Gitg.py", line 4, in <module>
    import Ggit
ImportError: No module named 'Ggit'
Checking GitgExt.py
Checking Gst.py
Checking GstAllocators.py
Checking GstApp.py
Checking GstAudio.py
Checking GstBase.py
Checking GstCheck.py
Checking GstController.py
Checking GstFft.py
Checking GstGL.py
Checking GstInsertBin.py
Checking GstInterfaces.py
Checking GstMpegts.py
Checking GstNet.py
Checking GstNetbuffer.py
Traceback (most recent call last):
  File "GstNetbuffer.py", line 57, in <module>
    class NetBuffer(Gst.Buffer):
AttributeError: module 'Gst' has no attribute 'Buffer'
Checking GstPbutils.py
Checking GstPlayer.py
Checking GstRiff.py
Checking GstRtp.py
Checking GstRtsp.py
Checking GstSdp.py
Checking GstTag.py
Checking GstVideo.py
Checking Gtk.py
Checking GtkClutter.py
Checking GtkSource.py
Checking HarfBuzz.py
Checking JSCore.py
Checking JavaScriptCore.py
Checking Json.py
Checking Pango.py
Checking PangoCairo.py
Checking PangoFT2.py
Checking PangoXft.py
Checking Soup.py
Checking WebKit.py
Checking __init__.py
Checking cairo.py
Checking fontconfig.py
Checking freetype2.py
Checking libxml2.py
Checking win32.py
Checking xfixes.py
Checking xft.py
Checking xlib.py
Checking xrandr.py

 |2.4.2|  using virtualenv: scarlett-os-venv2   hyenatop in ~/dev/bossjones/scarlett_os/fakegir
± |master U:1 ?:1 ✗| →

```


# saving errors

```
 ⌁ pi@scarlett-ansible-manual1604-2  ⓔ scarlett_os  ⎇  master S:2 U:23 ?:119  ~/dev/bossjones-github/scarlett_os  make jhbuild-run-pylint-error
jhbuild run -- pylint -E scarlett_os
Using config file /home/pi/dev/bossjones-github/scarlett_os/pylintrc
************* Module scarlett_os.core
E:165,38: Undefined variable 'dt_util' (undefined-variable)
************* Module scarlett_os.loader
W: 13, 0: Unused import importlib (unused-import)
W: 15, 0: Unused import os (unused-import)
W: 16, 0: Unused import pkgutil (unused-import)
W: 17, 0: Unused import sys (unused-import)
W: 19, 0: Unused ModuleType imported from types (unused-import)
************* Module scarlett_os.listener
E:352,12: Raising NoneType while only classes or instances are allowed (raising-bad-type)
/usr/lib/python3.5/inspect.py:78: Warning: /home/pi/gnome/glib/gobject/gsignal.c:1675: parameter 1 of type '<invalid>' for signal "GstBus::sync_message" is not a value type
  return isinstance(object, type)
/usr/lib/python3.5/inspect.py:78: Warning: /home/pi/gnome/glib/gobject/gsignal.c:1675: parameter 1 of type '<invalid>' for signal "GstBus::message" is not a value type
  return isinstance(object, type)
/usr/lib/python3.5/inspect.py:78: Warning: g_param_spec_boxed: assertion 'G_TYPE_IS_BOXED (boxed_type)' failed
  return isinstance(object, type)
/usr/lib/python3.5/inspect.py:78: Warning: g_object_class_install_property: assertion 'G_IS_PARAM_SPEC (pspec)' failed
  return isinstance(object, type)
E:665,11: Access to member 'signed' before its definition line 671 (access-member-before-definition)
************* Module scarlett_os.log
E:190,26: isatty is not callable (not-callable)
************* Module scarlett_os.player
E:295,12: Raising NoneType while only classes or instances are allowed (raising-bad-type)
************* Module scarlett_os.compat
E: 34,10: Undefined variable 'itertools' (undefined-variable)
************* Module scarlett_os.internal.formatting
E: 57,25: Undefined variable 'text_type' (undefined-variable)
************* Module scarlett_os.internal.debugger
E: 98, 4: No name 'PythonLexer' in module 'pygments.lexers' (no-name-in-module)
E: 99, 4: No name 'Terminal256Formatter' in module 'pygments.formatters' (no-name-in-module)
************* Module scarlett_os.internal.path
E:440,31: Module 'scarlett_os.exceptions' has no 'FindError' member (no-member)
E:450,31: Module 'scarlett_os.exceptions' has no 'FindError' member (no-member)
E:452,31: Module 'scarlett_os.exceptions' has no 'FindError' member (no-member)
E:455,27: Module 'scarlett_os.exceptions' has no 'FindError' member (no-member)
************* Module scarlett_os.utility.dt
E:225,19: Undefined variable 'reduce' (undefined-variable)
E:290, 0: function already defined line 144 (function-redefined)
************* Module scarlett_os.utility.yaml
E:199, 4: Using variable 'logger' before assignment (used-before-assignment)
E:205,16: Instance of 'str' has no 'setLevel' member (no-member)
E:207,16: Instance of 'str' has no 'error' member (no-member)
************* Module scarlett_os.utility.gnome
E:284, 8: Raising NoneType while only classes or instances are allowed (raising-bad-type)
E:369,16: Raising NoneType while only classes or instances are allowed (raising-bad-type)
E:392,26: Undefined variable 'MainRunnerTimeoutError' (undefined-variable)
E:394,16: Raising NoneType while only classes or instances are allowed (raising-bad-type)
E:442,74: Instance of 'Exception' has no 'message' member (no-member)
E:491, 8: No name 'generator_player' in module 'scarlett_os.utility' (no-name-in-module)
************* Module scarlett_os.utility.file
E: 63,23: Undefined variable '_FSCODING' (undefined-variable)
************* Module scarlett_os.tools.package
E: 10, 4: Unable to import 'distutils.sysconfig' (import-error)
E: 56, 4: Unable to import 'distutils.sysconfig' (import-error)
Makefile:891: recipe for target 'jhbuild-run-pylint-er
```


# python typing-stubs

https://github.com/pygobject/pycairo/pull/101
https://github.com/pygobject/pycairo/issues/99
https://github.com/pygobject/pgi-docgen/issues/79


# pytpython debugging 3/8/2018

```
 |2.4.2|  using virtualenv: scarlett-os-venv2   hyenatop in ~/dev/bossjones/scarlett_os
± |feature-config-schema {7} U:10 ?:3 ✗| → ptpython
>>> from scarlett_os.internal.gi import gi

(gst-plugin-scanner:13321): GStreamer-WARNING **: Failed to load plugin '/usr/local/lib/gstreamer-1.0/libgstjpeg.so': dlopen(/usr/local/lib/gstreamer-1.0/libgstjpeg.so, 2): Library not loaded: /usr/local/opt/jpeg/lib/libjpeg.8.dylib
  Referenced from: /usr/local/lib/gstreamer-1.0/libgstjpeg.so
  Reason: image not found

(gst-plugin-scanner:13321): GStreamer-WARNING **: Failed to load plugin '/usr/local/lib/gstreamer-1.0/libgstopengl.so': dlopen(/usr/local/lib/gstreamer-1.0/libgstopengl.so, 2): Library not loaded: /usr/local/opt/jpeg/lib/libjpeg.8.dylib
  Referenced from: /usr/local/lib/gstreamer-1.0/libgstopengl.so
  Reason: image not found

** (gst-plugin-scanner:13321): CRITICAL **: pygobject initialization failed

>>>
```


# Environment variabls to use when debugging gnome

https://wiki.ubuntu.com/DebuggingGNOME


# Example jhbuildrc file

```
aab42dbfecb3:~# cat .jhbuildrc
import os
prefix='/home/pi/jhbuild'
checkoutroot='/home/pi/gnome'
moduleset = 'gnome-world'
interact = False
makeargs = '-j4 V=1'
module_autogenargs['gtk-doc'] = 'PYTHON=/usr/bin/python3'
os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
os.environ['PYTHON'] = 'python3'
os.environ['GSTREAMER'] = '1.0'
os.environ['ENABLE_PYTHON3'] = 'yes'
os.environ['ENABLE_GTK'] = 'yes'
os.environ['PYTHON_VERSION'] = '3.5'
os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
os.environ['MAKEFLAGS'] = '-j4 V=1'
os.environ['PREFIX'] = '/home/pi/jhbuild'
os.environ['JHBUILD'] = '/home/pi/gnome'
os.environ['PATH'] = '/usr/lib/ccache:/home/pi/bin:/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/usr/local/bin:/usr/local/sbin:/usr/lib/ccache:/home/pi/bin:/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
os.environ['LD_LIBRARY_PATH'] = '/home/pi/jhbuild/lib:/home/pi/.virtualenvs/scarlett_os/lib'
os.environ['PYTHONPATH'] = '/home/pi/jhbuild/lib/python3.5/site-packages:/usr/lib/python3.5/site-packages'
os.environ['PKG_CONFIG_PATH'] = '/home/pi/jhbuild/lib/pkgconfig:/home/pi/jhbuild/share/pkgconfig:/usr/lib/pkgconfig'
os.environ['XDG_DATA_DIRS'] = '/home/pi/jhbuild/share:/usr/share'
os.environ['XDG_CONFIG_DIRS'] = '/home/pi/jhbuild/etc/xdg'
os.environ['CC'] = 'gcc'
os.environ['WORKON_HOME'] = '/home/pi/.virtualenvs'
os.environ['PROJECT_HOME'] = '/home/pi/dev'
os.environ['VIRTUALENVWRAPPER_PYTHON'] = '/usr/local/bin/python3'
os.environ['VIRTUALENVWRAPPER_VIRTUALENV'] = '/usr/local/bin/virtualenv'
os.environ['PYTHONSTARTUP'] = '/home/pi/.pythonrc'
os.environ['PIP_DOWNLOAD_CACHE'] = '/home/pi/.pip/cache'
os.environ['CCACHE_DIR'] = '/ccache'
```

# d-feet example of flatpak manifest

**SOURCE: https://github.com/GNOME/d-feet/blob/2b4726ca8b67e24e3a7b3b2e62f4f9dcaab40b5a/org.gnome.dfeet.json**

```

{
    "id": "org.gnome.dfeet",
    "runtime": "org.gnome.Platform",
    "runtime-version": "master",
    "branch": "master",
    "sdk": "org.gnome.Sdk",
    "command": "d-feet",
    "tags": ["nightly"],
    "desktop-file-name-prefix": "(Nightly) ",
    "finish-args": [
        "--share=ipc", "--socket=x11",
        "--socket=wayland",
        "--socket=system-bus", "--socket=session-bus",
        "--filesystem=xdg-run/dconf", "--filesystem=~/.config/dconf:ro",
        "--talk-name=ca.desrt.dconf", "--env=DCONF_USER_CONFIG_DIR=.config/dconf"
    ],
    "modules": [
        {
            "name": "pycairo",
            "buildsystem": "simple",
            "build-commands": [
                "python2 setup.py install --prefix=/app"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/pygobject/pycairo.git"
                }
            ],
            "cleanup": [
                "/include",
                "/share/pkgconfig"
            ]
        },
        {
            "name": "pygobject",
            "build-options" : {
                "env": {
                    "PYTHON": "/usr/bin/python2"
                }
            },
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/pygobject.git"
                }
            ],
            "cleanup": [
                "/include",
                "/lib/pkgconfig",
                "/lib/python2.7/site-packages/gi/*.la"
            ]
        },
        {
            "name": "d-feet",
            "config-opts": [
                "--disable-tests"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/d-feet.git"
                }
            ]
        }
    ]
}

```


# meld flatpak manifest

```

{
  "app-id": "org.gnome.meld",
  "runtime": "org.gnome.Platform",
  "runtime-version": "master",
  "sdk": "org.gnome.Sdk",
  "command": "meld",
  "cleanup": [
    "/include",
    "/lib/pkgconfig",
    "/share/pkgconfig",
    "/share/aclocal",
    "/man",
    "/share/man",
    "/share/gtk-doc",
    "/share/vala",
    "*.la",
    "*.a",
    "*.pyc",
    "*.pyo"
  ],
  "build-options": {
    "cflags": "-O2 -g",
    "cxxflags": "-O2 -g",
    "env": {
      "V": "1"
    }
  },
  "rename-appdata-file": "meld.appdata.xml",
  "rename-desktop-file": "meld.desktop",
  "rename-icon": "meld",
  "finish-args": [
    /* X11 + XShm */
    "--share=ipc", "--socket=x11",
    /* Wayland */
    "--socket=wayland",
    /* Filesystem */
    "--filesystem=host",
    /* dconf */
    "--talk-name=ca.desrt.dconf", "--env=DCONF_USER_CONFIG_DIR=.config/dconf"
  ],
  "modules": [
    {
      "name": "gtksourceview",
      "sources": [
        {
          "type": "archive",
          "url": "http://ftp.gnome.org/pub/GNOME/sources/gtksourceview/3.18/gtksourceview-3.18.2.tar.xz",
          "sha256": "60f75a9f0039e13a2281fc595b5ef7344afa06732cc53b57d13234bfb0a5b7b2"
        }
      ]
    },
    {
      "name": "py2cairo",
      "rm-configure": true,
      "sources": [
        {
          "type": "archive",
          "url": "http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2",
          "sha256": "d30439f06c2ec1a39e27464c6c828b6eface3b22ee17b2de05dc409e429a7431"
        },
        {
          "type": "script",
          "commands": [
            "libtoolize --force",
            "aclocal",
            "autoheader",
            "automake --force-missing --add-missing --foreign",
            "autoconf"
          ],
          "dest-filename": "autogen.sh"
        }
      ]
    },
    {
      "name": "pygobject",
      "build-options" : {
        "env": {
          "PYTHON": "python2"
        }
      },
      "sources": [
        {
          "type": "archive",
          "url": "http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.18/pygobject-3.18.2.tar.xz",
          "sha256": "2a3cad1517916b74e131e6002c3824361aee0671ffb0d55ded119477fc1c2c5f"
        }
      ]
    },
    {
      "name": "meld",
      "no-autogen": true,
      "sources": [
        {
          "type": "git",
          "url": "git://git.gnome.org/meld"
        },
        {
          "type": "file",
          "path": "data/meld-Makefile",
          "dest-filename": "Makefile"
        }
      ]
    }
  ]
}
```


# gimp flatpak manifest

```

{
    "id": "org.gimp.GIMP",
    "branch": "dev",
    "base": "org.gimp.BaseApp",
    "base-version": "stable",
    "runtime": "org.gnome.Platform",
    "runtime-version": "3.28",
    "sdk": "org.gnome.Sdk",
    "command": "gimp-2.9",
    "rename-desktop-file": "gimp.desktop",
    "rename-icon": "gimp",
    "finish-args": ["--share=ipc", "--socket=x11", "--share=network",
                    "--filesystem=host", "--filesystem=xdg-config/GIMP",
                    "--filesystem=xdg-config/gtk-3.0",
                    "--talk-name=org.gtk.vfs", "--talk-name=org.gtk.vfs.*" ],
    "tags": ["dev"],
    "desktop-file-name-prefix": "(Dev) ",
    "build-options" : {
        "cflags": "-O2 -g",
        "cxxflags": "-O2 -g",
        "env": {
            "V": "1"
        }
    },
    "cleanup": ["/include", "/lib/pkgconfig", "/share/pkgconfig",
                "/share/aclocal", "/man", "/share/man", "/share/gtk-doc",
                "/share/vala", "*.la", "*.a", "/bin/wmf*", "/bin/libwmf-*",
                "/bin/pygtk*", "/bin/pygobject*"],
    "modules": [
        {
            "name": "lcms2",
            "config-opts": [ "--disable-static" ],
            "cleanup": [ "/bin", "/share" ],
            "sources": [
                {
                    "type": "archive",
                    "url": "http://download.sourceforge.net/lcms/lcms2-2.8.tar.gz",
                    "sha256": "66d02b229d2ea9474e62c2b6cd6720fde946155cd1d0d2bffdab829790a0fb22"
                }
            ]
	},
        {
            "name": "babl",
            "config-opts": [ "--disable-docs" ],
            "sources": [
                {
                    "type": "git",
                    "url": "git://git.gnome.org/babl",
                    "branch": "BABL_0_1_38",
                    "commit": "04cea9206deb0a6fb52b0a86012d70551b020205"
                }
            ]
        },
        {
            "name": "gegl",
            "config-opts": [ "--disable-docs", "--disable-introspection" ],
            "cleanup": [ "/bin" ],
            "sources": [
                {
                    "type": "git",
                    "url": "git://git.gnome.org/gegl",
                    "branch": "GEGL_0_3_24",
                    "commit": "e647c79dc6c6f1c9a3c12e79a1fd8e77847d61d9"
                }
            ]
        },
        {
            "name": "gimp",
            "config-opts": [ "--disable-docs", "--disable-gtk-doc", "--disable-gtk-doc-html", "--enable-vector-icons" ],
            "cleanup": [ "/bin/gimptool-2.0", "/bin/gimp-console-2.9" ],
            "sources": [
                {
                    "type": "git",
                    "url": "git://git.gnome.org/gimp",
                    "branch": "GIMP_2_9_8",
                    "commit": "18794a6ba2915ed58b82337edaba794d69f767b7"
                }
            ],
	    "post-install": [
                "rm -fr /app/include /app/lib/pkgconfig /app/share/pkgconfig",
                "rm -fr /app/share/gtk-doc/ /app/share/man/",
                "rm -fr /app/lib/*.la /app/lib/*.a",
                "rm -fr /app/share/ghostscript/9.20/doc/",
                "rm -fr /app/bin/wmf* /app/bin/libwmf-*",
                "rm -fr /app/bin/pygtk* /app/bin/pygobject* /app/bin/pygobject-codegen-2.0"
            ]
        }
    ]
}

```


# Gimp nightly flatpak build

```

{
    "id": "org.gimp.GIMP",
    "branch": "master",
    "base": "org.gimp.BaseApp",
    "base-version": "stable",
    "runtime": "org.gnome.Platform",
    "runtime-version": "3.28",
    "sdk": "org.gnome.Sdk",
    "command": "gimp-2.9",
    "rename-desktop-file": "gimp.desktop",
    "rename-icon": "gimp",
    "finish-args": ["--share=ipc", "--socket=x11", "--share=network",
                    "--filesystem=host", "--filesystem=xdg-config/GIMP",
                    "--filesystem=xdg-config/gtk-3.0",
                    "--talk-name=org.gtk.vfs", "--talk-name=org.gtk.vfs.*" ],
    "tags": ["nightly"],
    "desktop-file-name-prefix": "(Nightly) ",
    "build-options" : {
        "cflags": "-O2 -g",
        "cxxflags": "-O2 -g",
        "env": {
            "V": "1"
        }
    },
    "cleanup": ["/include", "/lib/pkgconfig", "/share/pkgconfig",
                "/share/aclocal", "/man", "/share/man", "/share/gtk-doc",
                "/share/vala", "*.la", "*.a", "/bin/wmf*", "/bin/libwmf-*",
                "/bin/pygtk*", "/bin/pygobject*", "/bin/pygobject-codegen-2.0",

                "/share/glib-2.0/codegen", "/bin/gdbus-codegen", "/bin/glib-*",
                "/bin/gobject-query", "/bin/gresource", "/bin/gtester*"],
    "modules": [
        {
            "name" : "glib2",
            "config-opts" : [
                "--with-pcre=system"
            ],
            "ensure-writable" : [
                "/share/glib-2.0/codegen/*.pyc"
            ],
            "sources" : [
                {
                    "url": "https://download.gnome.org/sources/glib/2.54/glib-2.54.2.tar.xz",
                    "sha256": "bb89e5c5aad33169a8c7f28b45671c7899c12f74caf707737f784d7102758e6c",
                    "type": "archive"
                }
            ]
        },
        {
            "name" : "glib-networking",
            "config-opts" : [
                "--disable-static"
            ],
            "sources" : [
                {
                    "url": "http://ftp.gnome.org/pub/gnome/sources/glib-networking/2.54/glib-networking-2.54.1.tar.xz",
                    "sha256": "eaa787b653015a0de31c928e9a17eb57b4ce23c8cf6f277afaec0d685335012f",
                    "type": "archive"
                }
            ]
        },
        {
            "name": "mypaint-brushes",
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/Jehan/mypaint-brushes.git",
                    "branch": "v1.3.0",
                    "commit": "fce9b5f23f658f15f8168ef5cb2fee69cf90addb"
                }
            ]
        },
        {
            "name": "lcms2",
            "config-opts": [ "--disable-static" ],
            "cleanup": [ "/bin", "/share" ],
            "sources": [
                {
                    "type": "archive",
                    "url": "http://download.sourceforge.net/lcms/lcms2-2.8.tar.gz",
                    "sha256": "66d02b229d2ea9474e62c2b6cd6720fde946155cd1d0d2bffdab829790a0fb22"
                }
            ]
        },
        {
            "name": "openjpeg",
            "cmake": true,
            "buildsystem": "cmake-ninja",
            "builddir": true,
            "cleanup": [ "/bin", "/lib/openjpeg-2.3" ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://github.com/uclouvain/openjpeg/archive/v2.3.0.tar.gz",
                    "sha256": "3dc787c1bb6023ba846c2a0d9b1f6e179f1cd255172bde9eb75b01f1e6c7d71a"
                }
            ]
        },
        {
            "name": "babl",
            "config-opts": [ "--disable-docs" ],
            "sources": [
                {
                    "type": "git",
                    "url": "git://git.gnome.org/babl",
                    "branch": "master"
                }
            ]
        },
        {
            "name": "gegl",
            "config-opts": [ "--disable-docs", "--disable-introspection" ],
            "cleanup": [ "/bin" ],
            "sources": [
                {
                    "type": "git",
                    "url": "git://git.gnome.org/gegl",
                    "branch": "master"
                }
            ]
        },
        {
            "name": "gimp",
            "config-opts": [ "--disable-docs", "--disable-gtk-doc", "--disable-gtk-doc-html", "--enable-vector-icons" ],
            "cleanup": [ "/bin/gimptool-2.0", "/bin/gimp-console-2.9" ],
            "sources": [
                {
                    "type": "git",
                    "url": "git://git.gnome.org/gimp",
                    "branch": "master"
                }
            ],
	    "post-install": [
                "rm -fr /app/include /app/lib/pkgconfig /app/share/pkgconfig",
                "rm -fr /app/share/gtk-doc/ /app/share/man/",
                "rm -fr /app/lib/*.la /app/lib/*.a",
                "rm -fr /app/share/ghostscript/9.20/doc/",
                "rm -fr /app/bin/wmf* /app/bin/libwmf-*",
                "rm -fr /app/bin/pygtk* /app/bin/pygobject* /app/bin/pygobject-codegen-2.0"
            ]
        }
    ]
}

```

# gnome-ostree/manifest.json

https://github.com/GNOME/gnome-ostree/blob/edd9828d72753f14aa6ad69ae0093ea00ad4205b/manifest.json

# org.gnome.SDK.json from gnome-sdk-images

source: https://github.com/GNOME/gnome-sdk-images/blob/master/org.gnome.Sdk.json.in

```

{
    "build-runtime": true,
    "id": "org.gnome.Sdk",
    "id-platform": "org.gnome.Platform",
    "branch": "@@SDK_BRANCH@@",
    "runtime": "org.freedesktop.Platform",
    "sdk": "org.freedesktop.Sdk",
    "runtime-version": "@@SDK_RUNTIME_VERSION@@",
    "sdk-extensions": ["org.freedesktop.Sdk.Debug", "org.freedesktop.Sdk.Locale", "org.freedesktop.Sdk.Docs"],
    "platform-extensions": [ "org.freedesktop.Platform.Locale"],
    "inherit-extensions": [
        "org.freedesktop.Platform.GL",
        "org.freedesktop.Platform.Timezones",
        "org.freedesktop.Platform.GStreamer",
        "org.freedesktop.Platform.Icontheme",
        "org.freedesktop.Platform.VAAPI.Intel",
        "org.freedesktop.Platform.ffmpeg",
        "org.freedesktop.Sdk.Extension",
        "org.gtk.Gtk3theme"
    ],
    "add-extensions": {
        "org.gnome.Sdk.Docs" : {
            "directory": "share/runtime/docs",
            "bundle": true,
            "autodelete": true,
            "no-autodownload": true
        }
    },
    "finish-args": [
        "--env=GI_TYPELIB_PATH=/app/lib/girepository-1.0",
        "--env=GST_PLUGIN_SYSTEM_PATH=/app/lib/gstreamer-1.0:/usr/lib/extensions/gstreamer-1.0:/usr/lib/gstreamer-1.0",
        "--env=XDG_DATA_DIRS=/app/share:/usr/share:/usr/share/runtime/share:/run/host/share",
        "--sdk=org.gnome.Sdk//@@SDK_BRANCH@@",
        "--runtime=org.gnome.Platform//@@SDK_BRANCH@@"
    ],
    "cleanup": [ "/man",
                 "/share/man",
                 "/share/gtk-doc/html",
                 "/lib/systemd",
                 "*.la", "*.a"],
    "cleanup-commands": [ "update-desktop-database",
                          "/usr/libexec/freedesktop-post.sh"
                        ],
    "cleanup-platform": [ "/share/runtime/docs",
                          "/include",
                          "/share/aclocal",
                          "/share/pkgconfig",
                          "/lib/pkgconfig",
                          "/share/gir-1.0",
                          "/share/vala"
                        ],
    "cleanup-platform-commands": [  "/usr/libexec/freedesktop-post.sh" ],
    "build-options" : {
        "cflags": "-O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2",
        "cxxflags": "-O2 -g -fstack-protector-strong -D_FORTIFY_SOURCE=2",
        "ldflags": "-fstack-protector-strong -Wl,-z,relro,-z,now",
        "env": {
            "V": "1"
        }
    },
    "modules": [
        {
            "name": "gnome-common",
            "cleanup-platform": [ "*" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/gnome-common"
                }
            ]
        },
        {
            "name": "yelp-xsl",
            "config-opts": ["--disable-doc"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/yelp-xsl"
                }
            ]
        },
        {
            "name": "yelp-tools",
            "cleanup-platform": [ "*" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/yelp-tools"
                }
            ]
        },
        {
            "name": "cantarell-fonts",
            "config-opts": [ "--disable-source-rebuild"],
            "post-install": [
                "ln -s /usr/share/fontconfig/conf.avail/31-cantarell.conf /etc/fonts/conf.d/31-cantarell.conf"
            ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://download.gnome.org/sources/cantarell-fonts/0.0/cantarell-fonts-0.0.25.tar.xz",
                    "sha256": "14a228aa0b516dfc367b434a850f955a00c57fc549cbb05348e2b150196a737f"
                }
            ]
        },
        {
            "name": "glib",
            "config-opts": [ "--with-pcre=system", "--with-python=python3" ],
            "ensure-writable": [ "/share/glib-2.0/codegen/*.pyc" ],
            "cleanup-platform": [ "/share/glib-2.0/codegen",
                                  "/bin/gdbus-codegen",
                                  "/bin/glib-*",
                                  "/bin/gobject-query",
                                  "/bin/gresource",
                                  "/bin/gtester*"
                               ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/glib.git"
                }
            ]
        },
        {
            "name": "gobject-introspection",
            "config-opts": ["--disable-static" ],
            "ensure-writable": [ "/lib/gobject-introspection/giscanner/*.pyc",
                                 "/lib/gobject-introspection/giscanner/*/*.pyc" ],
            "cleanup-platform": ["/lib/gobject-introspection/giscanner",
                                 "/share/gobject-introspection/giscanner",
                                 "/bin"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/gobject-introspection.git"
                }
            ]
        },
        {
            "name": "gsettings-desktop-schemas",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/gsettings-desktop-schemas"
                }
            ]
        },
        {
            "name": "glib-networking",
            "buildsystem": "meson",
            "ensure-writable": [
                "/share/locale/*/LC_MESSAGES/*.mo",
                "/share/runtime/locale/*/share/*/LC_MESSAGES/*.mo"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/glib-networking"
                }
            ]
        },
        {
            "name": "vala-bootstrap",
            "cleanup": [ "/bin/*-0.16",
                         "/lib/*-0.16*",
                         "/lib/pkgconfig/*",
                         "/include/vala-0.16",
                         "/share/vala-0.16" ],
            "cleanup-platform": [ "*" ],
            "config-opts": [ "--disable-build-from-vala",
                             "--disable-vapigen" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/vala-bootstrap"
                }
            ]
        },
        {
            "name": "vala",
            "cleanup-platform": [ "*" ],
            "config-opts": [ "--enable-vapigen", "--enable-unversioned" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/vala",
                    "branch": "0.36"
                }
            ]
        },
        {
            "name": "dconf",
            "buildsystem": "meson",
            "cleanup": [ "/libexec/dconf-service", "/share/dbus-1/services/*" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/dconf"
                },
                {
                    "type": "patch",
                    "path": "dconf-override.patch"
                }
            ]
        },
        {
            "name": "libsoup",
            "config-opts": ["--disable-static"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/libsoup"
                }
            ]
        },
        {
            "name": "dbus-glib",
            "config-opts": [ "--disable-static" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/dbus/dbus-glib.git"
                }
            ]
        },
        {
            "name": "json-glib",
            "buildsystem": "meson",
            "builddir": true,
            "ensure-writable": [
                "/share/locale/*/LC_MESSAGES/json-glib-1.0.mo",
                "/share/runtime/locale/*/share/*/LC_MESSAGES/json-glib-*.mo"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/json-glib.git"
                }
            ]
        },
        {
            "name": "libdatrie",
            "config-opts": ["--disable-static"],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://linux.thai.net/pub/thailinux/software/libthai/libdatrie-0.2.10.tar.xz",
                    "sha256": "180eff7b0309ca19a02d5864e744185d715f021398a096fec6cf960f8ebfaa2b"
                }
            ]
        },
        {
            "name": "libthai",
            "config-opts": ["--disable-static"],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://linux.thai.net/pub/thailinux/software/libthai/libthai-0.1.27.tar.xz",
                    "sha256": "1659fa1b7b1d6562102d7feb8c8c3fd94bb2dc5761ed7dbaae4f300e1c03eff6"
                }
            ]
        },
        {
            "name": "wayland-updated",
            "config-opts": ["--disable-static", "--disable-documentation"],
            "cleanup-platform": [ "/bin/wayland-scanner" ],
            "sources": [
                 {
                     "type": "archive",
                     "url": "https://wayland.freedesktop.org/releases/wayland-1.14.0.tar.xz",
                     "sha256": "ed80cabc0961a759a42092e2c39aabfc1ec9a13c86c98bbe2b812f008da27ab8"
                 }
            ]
        },
        {
            "name": "wayland-protocols-updated",
            "cleanup-platform": [ "*" ],
            "sources": [
                 {
                     "type": "archive",
                     "url": "https://wayland.freedesktop.org/releases/wayland-protocols-1.13.tar.xz",
                     "sha256": "0758bc8008d5332f431b2a84fea7de64d971ce270ed208206a098ff2ebc68f38"
                 }
            ]
        },
        {
            "name": "fribidi",
            "buildsystem": "meson",
            "config-opts": [ "-Ddocs=false" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/fribidi/fribidi.git"
                }
            ]
        },
        {
            "name": "pango",
            "buildsystem": "meson",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/pango"
                }
            ]
        },
        {
            "name": "atk",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/atk"
                }
            ]
        },
        {
            "name": "at-spi2-core",
            "sources": [
                {
                    "type": "archive",
                    "url": "https://download.gnome.org/sources/at-spi2-core/2.26/at-spi2-core-2.26.2.tar.xz",
                    "sha256": "c80e0cdf5e3d713400315b63c7deffa561032a6c37289211d8afcfaa267c2615"
                }
            ]
        },
        {
            "name": "at-spi2-atk",
            "sources": [
                {
                    "type": "archive",
                    "url": "https://download.gnome.org/sources/at-spi2-atk/2.26/at-spi2-atk-2.26.1.tar.xz",
                    "sha256": "b4f0c27b61dbffba7a5b5ba2ff88c8cee10ff8dac774fa5b79ce906853623b75"
                }
            ]
        },
        {
            "name": "gdk-pixbuf",
            "ensure-writable": ["/lib/gdk-pixbuf-2.0/*/loaders.cache"],
            "config-opts": ["--disable-static",
                            "--without-x11",
                            "--without-libjasper",
                            "--with-included-loaders=png,jpeg" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/gdk-pixbuf"
                },
                {
                    "type": "shell",
                    /* Temporary workaround until fixed in fd.o sdk (81b7e21a0) */
                    "commands": ["update-mime-database /usr/share/mime"]
                }
            ]
        },
        {
            "name": "libcroco",
            "config-opts": ["--disable-static"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/libcroco"
                }
            ]
        },
        {
            "name": "librsvg",
            "config-opts": ["--disable-static"],
            "ensure-writable": ["/lib/gdk-pixbuf-2.0/*/loaders.cache"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/librsvg.git",
                    "branch": "librsvg-2-40"
                }
            ]
        },
        {
            "name": "gtk2",
            "config-opts": ["--disable-man",
                            "--with-xinput=xfree"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/gtk.git",
                    "branch": "gtk-2-24"
                }
            ]
        },
        {
            "name": "gtk3",
            "config-opts": [ "--enable-xkb",
                             "--enable-xinerama",
                             "--enable-xrandr",
                             "--enable-xfixes",
                             "--enable-xcomposite",
                             "--enable-xdamage",
                             "--enable-x11-backend",
                             "--enable-wayland-backend" ],
            "cleanup-platform": [
                "/bin/gtk3-*",
                "/bin/gtk-builder-tool",
                "/bin/gtk-encode-symbolic-svg"
            ],
            "ensure-writable": ["/lib/gtk-3.0/*/immodules.cache"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/gtk.git",
                    "branch": "gtk-3-22"
                }
            ]
        },
        {
            "name": "adwaita-icon-theme",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/adwaita-icon-theme"
                }
            ]
        },
        {
            "name": "gstreamer",
            "config-opts": ["--enable-debug", "--disable-examples", "--disable-fatal-warnings" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/gstreamer/gstreamer.git"
                }
            ],
            "build-commands": [
                /* We delete all the 1.10 plugins to avoid version mismatches with renamed or removed plugins */
                "rm -rf /usr/lib/gstreamer-1.0"
            ]
        },
        {
            "name": "opus",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.xiph.org/opus.git"
                }
            ]
        },
        {
            "name": "gstreamer-plugins-base",
            "config-opts": ["--enable-experimental", "--enable-orc" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/gstreamer/gst-plugins-base.git"
                }
            ]
        },
        {
            "name": "cogl",
            "config-opts": [  "--enable-cairo=yes",
                              "--enable-cogl-pango=yes",
                              "--enable-gdk-pixbuf=yes",
                              "--enable-glx=yes",
                              "--enable-introspection=yes",
                              "--enable-kms-egl-platform",
                              "--enable-wayland-egl-platform",
                              "--enable-wayland-egl-server",
                              "--enable-xlib-egl-platform",
                              "--enable-cogl-gst" ],
            "sources": [
                {
                    "type": "git",
                    "branch": "cogl-1.22",
                    "url": "https://git.gnome.org/browse/cogl"
                }
            ]
        },
        {
            "name": "clutter",
            "config-opts": ["--enable-gdk-backend",
                            "--enable-xinput",
                            "--enable-evdev-input" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/clutter"
                }
            ]
        },
        {
            "name": "clutter-gst",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/clutter-gst",
                    "branch": "clutter-gst-3.0"
                }
            ]
        },
        {
            "name": "clutter-gtk",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/clutter-gtk"
                }
            ]
        },
        {
            "name": "gstreamer-plugins-good",
            "build-options" : {
                "arch" : {
                    "i386" : {
                        "config-opts" : [
                            "--build=i586-unknown-linux-gnu"
                        ]
                    },
                    "arm" : {
                        "config-opts" : [
                            "--build=arm-unknown-linux-gnueabi"
                        ]
                    }
                }
            },
            "config-opts": ["--enable-experimental", "--enable-orc" ,
                            "--disable-monoscope",
                            "--disable-aalib",
                            "--enable-cairo",
                            "--disable-libcaca",
                            "--disable-jack",
                            "--with-default-visualizer=autoaudiosink" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/gstreamer/gst-plugins-good.git"
                }
            ]
        },
        {
            "name": "gstreamer-plugins-bad",
            "build-options" : {
                "arch" : {
                    "i386" : {
                        "config-opts" : [
                            "--build=i586-unknown-linux-gnu"
                        ]
                    },
                    "arm" : {
                        "config-opts" : [
                            "--build=arm-unknown-linux-gnueabi"
                        ]
                    }
                }
            },
            "config-opts": ["--enable-experimental", "--enable-orc", "--disable-fatal-warnings" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/gstreamer/gst-plugins-bad.git"
                }
            ]
        },
        {
            "name": "gstreamer-libav",
            "build-options" : {
                "arch" : {
                    "i386" : {
                        "config-opts" : [
                            "--build=i586-unknown-linux-gnu"
                        ]
                    },
                    "arm" : {
                        "config-opts" : [
                            "--build=arm-unknown-linux-gnueabi"
                        ]
                    }
                }
            },
            "config-opts": ["--with-system-libav" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/gstreamer/gst-libav.git"
                }
            ]
        },
        {
            "name": "libcanberra",
            "sources": [
                {
                    "type": "git",
                    "url": "http://git.0pointer.net/clone/libcanberra.git" /* No HTTPS unfortunately */
                }
            ]
        },
        {
            "name": "libsecret",
            "config-opts": ["--disable-static", "--disable-manpages"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/libsecret"
                }
            ]
        },
        {
            "name": "libnotify",
            "config-opts": ["--disable-static"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/libnotify"
                }
            ]
        },
        {
            "name": "gvfs",
            "cleanup": [ "/libexec/*", "/share/dbus-1/services/*", "/share/gvfs/mounts" ],
            "config-opts": [ "--disable-hal", "--disable-gdu", "--disable-gcr", "--disable-obexftp",
                             "--disable-avahi", "--disable-documentation", "--disable-admin" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/gvfs"
                }
            ]
        },
        {
            "name": "enchant",
            "config-opts": ["--disable-static", "--with-myspell-dir=/usr/share/hunspell"],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://www.abisource.com/downloads/enchant/1.6.0/enchant-1.6.0.tar.gz",
                    "sha256": "2fac9e7be7e9424b2c5570d8affe568db39f7572c10ed48d4e13cddf03f7097f"
                },
                {
                    "type": "shell",
                    "commands": [
                        "cp -f /usr/share/gnu-config/config.sub .",
                        "cp -f /usr/share/gnu-config/config.guess ."
                    ]
                }
            ]
        },
        {
            "name": "gcab",
            "buildsystem": "meson",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/gcab"
                }
            ]
        },
        {
            "name": "gnome-themes-extra",
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/gnome-themes-extra.git"
                }
            ]
        },
        {
            "name": "mozjs52",
            "build-options": {
                "arch" : {
                    "i386" : {
                        "config-opts" : [
                            "--host=i586-unknown-linux-gnu"
                        ]
                    },
                    "arm" : {
                        /* Workaround for bug seebugzilla.gnome.org, bug 790097 */
                        "cflags": "-fno-schedule-insns",
                        "cxxflags": "-fno-schedule-insns",
                        "config-opts" : [
                            "--host=arm-unknown-linux-gnueabi"
                        ]
                    }
                }
            },
            "config-opts": [  "--enable-posix-nspr-emulation",
                              "--with-system-zlib",
                              "--without-system-icu",
                              "--with-intl-api",
                              "AUTOCONF=autoconf"],
            "subdir": "js/src",
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/ptomato/mozjs.git",
                    "branch": "mozjs52"
                }
            ],
            "post-install": [
                "cp -p js/src/js-config.h /usr/include/mozjs-52",
                "rm /usr/lib/libjs_static.ajs"
            ]
        },
        {
            "name": "gjs",
            "config-opts": [  "--disable-Werror"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/gjs.git"
                }
            ]
        },
        /* VTE needs pcre2 */
        {
            "name": "pcre2",
            "config-opts": ["--enable-jit",
                            "--enable-pcre2grep-jit",
                            "--disable-bsr-anycrlf",
                            "--disable-coverage",
                            "--disable-ebcdic",
                            "--disable-never-backslash-C",
                            "--enable-newline-is-lf",
                            "--enable-pcre2-8",
                            "--enable-pcre2-16",
                            "--enable-pcre2-32",
                            "--disable-pcre2test-libedit",
                            "--enable-pcre2test-libreadline",
                            "--enable-pcre2grep-callout",
                            "--disable-pcre2grep-libbz2",
                            "--disable-pcre2grep-libz",
                            "--disable-rebuild-chartables",
                            "--enable-shared",
                            "--enable-stack-for-recursion",
                            "--disable-static",
                            "--enable-unicode",
                            "--disable-valgrind"],
            "sources": [
                {
                    "type": "archive",
                    "url": "http://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre2-10.22.tar.gz",
                    "sha256": "7627f93f2763ee6e11ac58558d8cfbf29e1070757b45571c0ba30ce9e096505c"
                }
            ]
        },
        {
            "name": "vte",
            "build-options" : {
                "cflags": "-fPIE -DPIE",
                "cxxflags": "-fPIE -DPIE",
                "ldflags": "-pie -lssp"
            },
            "config-opts": ["--disable-gnome-pty-helper",
                            "--disable-static",
                            "--with-gtk=3.0",
                            "--enable-introspection",
                            "--without-pcre2"],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/vte"
                }
            ]
        },
        {
            "name": "brotli",
            "buildsystem": "cmake",
            "config-opts": [
                "-DCMAKE_INSTALL_PREFIX:PATH=/usr",
                "-DCMAKE_INSTALL_LIBDIR:PATH=/usr/lib"
            ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://github.com/google/brotli/archive/v1.0.1.tar.gz",
                    "sha256": "6870f9c2c63ef58d7da36e5212a3e1358427572f6ac5a8b5a73a815cf3e0c4a6"
                }
            ]
        },
        {   "name": "woff2",
            "buildsystem": "cmake",
            "config-opts": [
                "-DCMAKE_INSTALL_PREFIX:PATH=/usr",
                "-DCMAKE_INSTALL_LIBDIR:PATH=/usr/lib"
            ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://github.com/google/woff2/archive/v1.0.2/woff2-1.0.2.tar.gz",
                    "sha256": "add272bb09e6384a4833ffca4896350fdb16e0ca22df68c0384773c67a175594"
                }
            ]
        },
        {
            "name": "WebKitGTK+",
            "cleanup-platform": [ "/libexec/webkit2gtk-4.0/MiniBrowser" ],
            "buildsystem": "cmake",
            "build-options" : {
                "cflags": "-g1",
                "cxxflags": "-g1",
                "arch" : {
                    "i386" : {
                        "config-opts" : [
                            "-DCMAKE_SYSTEM_PROCESSOR=i586"
                        ]
                    },
                    "arm" : {
                        "config-opts" : [
                            "-DCMAKE_SYSTEM_PROCESSOR=arm",
                            "-DENABLE_JIT=OFF"
                        ]
                    }
                }
            },
            "config-opts": [
                "-DPORT=GTK",
                "-DCMAKE_BUILD_TYPE=Release",
                "-DCMAKE_INSTALL_PREFIX:PATH=/usr",
                "-DLIB_INSTALL_DIR:PATH=/usr/lib",
                "-DSYSCONF_INSTALL_DIR:PATH=/usr/etc",
                "-DSHARE_INSTALL_PREFIX:PATH=/usr/share",
                "-DINCLUDE_INSTALL_DIR:PATH=/usr/include",
                "-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON",
                "-DENABLE_MINIBROWSER=ON"
            ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://webkitgtk.org/releases/webkitgtk-2.20.0.tar.xz",
                    "sha256": "57f640f720bd9a8a7207f3321cf803a15c2f207b4e7b75ff1be17bc1eeb00a3c"
                }
            ]
        },
        {
            "name": "yelp",
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/yelp"
                },
                {
                    "type": "patch",
                    "path": "yelp-use-in-sandbox.patch"
                }
            ]
        },
        {
            "name": "pycairo",
            "build-options" : {
                "env": {
                    "PYTHON": "/usr/bin/python3"
                }
            },
            "buildsystem": "simple",
            "build-commands": [
                "python3 ./setup.py build",
                "python3 ./setup.py install"
            ],
            "sources": [
                {
                    "type": "archive",
                    "url": "https://github.com/pygobject/pycairo/releases/download/v1.14.1/pycairo-1.14.1.tar.gz",
                    "sha256": "0d13a0a6eeaf0c357db04392943eb9b25767445608d31dde1307f003f68c5754"
                }
            ]
        },
        {
            "name": "pygobject",
            "config-opts": ["--enable-compile-warnings=minimum"],
            "build-options" : {
                "env": {
                    "PYTHON": "/usr/bin/python3"
                }
            },
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/pygobject.git"
                }
            ]
        },
        {
            "name": "python-gstreamer",
            "build-options" : {
                "env": {
                    "PYTHON": "/usr/bin/python3"
                }
            },
            "sources": [
                {
                    "type": "git",
                    "url": "https://anongit.freedesktop.org/git/gstreamer/gst-python.git"
                }
            ]
        },
        {
            "name": "gcr",
            "cleanup": [ "/share/GConf" ],
            "cleanup-platform": [ "/libexec", "/bin", "/share/applications", "/share/dbus-1/services" ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://git.gnome.org/browse/gcr"
                }
            ]
        },
        {
            "name": "ibus",
            "config-opts": ["--disable-xim", "--disable-static", "--disable-dconf", "--disable-schemas-compile",
                            "--disable-setup", "--disable-ui", "--disable-engine", "--disable-libnotify", "--disable-emoji-dict",
                            "--disable-appindicator", "--disable-tests"],
            "cleanup": [
                "/bin", "/libexec", "/share/bash-completion", "/share/dbus-1",
                "/share/icons", "/share/man", "/share/ibus" ],
            "post-install": [ "gtk-query-immodules-3.0 --update-cache",
                              "gtk-query-immodules-2.0 --update-cache" ],

            "sources": [
                {
                    "type": "archive",
                    "url": "https://github.com/ibus/ibus/releases/download/1.5.16/ibus-1.5.16.tar.gz",
                    "sha256": "36b57bfbe4f92e3281fb535cae65794b6f25164b2a3288e73e6d06b4a409fe1e"
                },
                {
                    "type": "patch",
                    "path": "ibus-portal.patch"
                }
            ]
        },
        {
            "name": "os-release",
            "sources": [
                {
                    "type": "file",
                    "path": "os-release"
                },
                {
                    "type": "file",
                    "path": "issue"
                },
                {
                    "type": "file",
                    "path": "issue.net"
                },
                {
                    "type": "file",
                    "path": "org.gnome.Sdk.appdata.xml"
                },
                {
                    "type": "file",
                    "path": "org.gnome.Platform.appdata.xml"
                },
                {
                    "type": "file",
                    "path": "os-release-configure",
                    "dest-filename": "configure"
                }
            ]
        }
    ]
}

```


# Meson.build files using python (examples )

- General search: https://github.com/search?q=org%3AGNOME+meson.build+python&type=Code
- https://github.com/GNOME/grilo/blob/4538c07aafae1d23211335ecfd51fb97e4f4d96d/tools/grilo-inspect/meson.build
- https://github.com/GNOME/baobab/blob/884fb555173c46fcb4a80a5cc9cbd32bad8186ba/meson.build
- https://github.com/GNOME/gnome-clocks/blob/b501c0defa9bf02341907d557621908293c4fad9/snap/plugins/x-meson.py
- https://github.com/GNOME/gnome-dictionary/blob/42b3f0afe085ef266af7c3905ef716e0764824a3/README.md
- https://github.com/GNOME/gnome-clocks/blob/57a9ea019209695532f92ad633fb55b51990b0b0/meson.build
- https://github.com/GNOME/libgd/blob/44f7d2673d4ba19be99dfe6a775b18e67bc4b56e/meson_readme.md
- https://github.com/GNOME/gnome-settings-daemon/blob/c343f5de1d53ce1c0e0634e73684939a1f2cc530/.gitlab-ci.yml
- https://github.com/GNOME/pitivi/blob/b8b22123966cff0ba513300ef2b4fd3dec624c5a/meson.build
- https://github.com/GNOME/gnome-music/blob/88ca0fb55d5c3a035929c5d8a39c2808c27b58bd/meson.build
- https://github.com/GNOME/gtk/blob/1b62d28cbb561c12f43f08819e1714c8bf068ef7/build-aux/flatpak/org.gtk.WidgetFactory.json
- https://github.com/flathub ( LOOK AT ME FOR ALL MANIFESTS )
- https://github.com/flathub/im.srain.Srain/blob/f98b0427fdc5e20f270adf46928ebd963f8e6f24/im.srain.Srain.json
- https://github.com/flathub/org.blender.Blender/blob/00ca9787a8c8f05b9a40abaea9e7b8906b74a7f9/org.blender.Blender.json
- https://github.com/flathub/work.openpaper.Paperwork/blob/8ea2466ac39150de0d61177de6f9f49934e8cb50/work.openpaper.Paperwork.json


# org.gtk.WidgetFactory.json
```

{
    "app-id": "org.gtk.WidgetFactory",
    "runtime": "org.gnome.Platform",
    "runtime-version": "master",
    "sdk": "org.gnome.Sdk",
    "command": "gtk4-widget-factory",
    "tags": ["devel", "development", "nightly"],
    "rename-desktop-file": "gtk4-widget-factory.desktop",
    "rename-icon": "gtk4-widget-factory",
    "desktop-file-name-prefix": "(Development) ",
    "finish-args": [
        "--device=dri",
        "--share=ipc",
        "--socket=x11",
        "--socket=wayland",
        "--talk-name=org.gtk.vfs", "--talk-name=org.gtk.vfs.*",
        "--talk-name=ca.desrt.conf", "--env=DCONF_USER_CONFIG_DIR=.config/dconf"
    ],
    "cleanup": [
        "/include",
        "/lib/pkgconfig", "/share/pkgconfig",
        "/share/aclocal",
        "/man", "/share/man", "/share/gtk-doc",
        "*.la", ".a",
        "/lib/girepository-1.0",
        "/share/gir-1.0",
        "/share/doc"
    ],
    "modules": [
        {
            "name": "graphene",
            "buildsystem": "meson",
            "builddir": true,
            "config-opts": [
                "--libdir=/app/lib"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/ebassi/graphene.git"
                }
            ]
        },
        {
            "name": "gtk",
            "buildsystem": "meson",
            "builddir": true,
            "config-opts": [
                "--libdir=/app/lib"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://gitlab.gnome.org/GNOME/gtk.git"
                }
            ]
        }
    ]
}

```

# Flatpak-builder steps

Now that the app has a manifest, flatpak-builder can be used to build it. This is done by specifying the manifest file and a target directory:

`$ flatpak-builder app-dir org.flatpak.Hello.json`

```
[developer@dev-experimental flatpak-demo]$ flatpak-builder app-dir org.flatpak.Hello.json
Downloading sources
Initializing build dir
Committing stage init to cache
Starting build of org.flatpak.Hello
========================================================================
Building module hello in /home/developer/Projects/flatpak-demo/.flatpak-builder/build/hello-1
========================================================================
Running: install -D hello.sh /app/bin/hello.sh
Committing stage build-hello to cache
Cleaning up
Committing stage cleanup to cache
Finishing app
Please review the exported files and the metadata
Committing stage finish to cache
Pruning cache
[developer@dev-experimental flatpak-demo]$
```

This command will build each module that is listed in the manifest and install it to the /app subdirectory, inside the
app-dir directory.

5. Test the build
To verify that the build was successful, run the following:

`$ flatpak-builder --run app-dir org.flatpak.Hello.json hello.sh`



# os x virtualenv artifacts ( old shit before updating things with brew )

```
l
 |2.4.2|  using virtualenv: scarlett-os-venv2   hyenatop in ~/.virtualenvs/scarlett-os-venv2/lib/python3.5/site-packages/gi
○ → ls -lta
total 1072
drwxr-xr-x  284 malcolm  staff    9656 Mar  8 12:18 ..
drwxr-xr-x   21 malcolm  staff     714 Sep  5  2016 .
-rwxr-xr-x    1 malcolm  staff  412772 Sep  5  2016 _gi.cpython-35m-darwin.so
-rwxr-xr-x    1 malcolm  staff    1214 Sep  5  2016 _gi.la
-rwxr-xr-x    1 malcolm  staff   16148 Sep  5  2016 _gi_cairo.cpython-35m-darwin.so
-rwxr-xr-x    1 malcolm  staff    1249 Sep  5  2016 _gi_cairo.la
drwxr-xr-x    4 malcolm  staff     136 Sep  5  2016 _gobject
drwxr-xr-x   12 malcolm  staff     408 Sep  5  2016 overrides
-rw-r--r--    1 malcolm  staff    4605 Sep  5  2016 __init__.py
drwxr-xr-x   24 malcolm  staff     816 Sep  5  2016 __pycache__
-rw-r--r--    1 malcolm  staff    2078 Sep  5  2016 _constants.py
-rw-r--r--    1 malcolm  staff    2080 Sep  5  2016 _error.py
-rw-r--r--    1 malcolm  staff   13249 Sep  5  2016 _option.py
-rw-r--r--    1 malcolm  staff   15175 Sep  5  2016 _propertyhelper.py
-rw-r--r--    1 malcolm  staff    9860 Sep  5  2016 _signalhelper.py
-rw-r--r--    1 malcolm  staff    6688 Sep  5  2016 docstring.py
-rw-r--r--    1 malcolm  staff    5288 Sep  5  2016 importer.py
-rw-r--r--    1 malcolm  staff   10037 Sep  5  2016 module.py
-rw-r--r--    1 malcolm  staff     766 Sep  5  2016 pygtkcompat.py
drwxr-xr-x    4 malcolm  staff     136 Sep  5  2016 repository
-rw-r--r--    1 malcolm  staff   13801 Sep  5  2016 types.py

 |2.4.2|  using virtualenv: scarlett-os-venv2   hyenatop in ~/.virtualenvs/scarlett-os-venv2/lib/python3.5/site-packages/gi
○ →
```


# Example of ninja file ( generated by meson by default, found in mesonbuild/ folder )


```

~/dev/scarlett_os-dev/scarlett_os/mesonbuild $ cat build.ninja
# This is the build file for project "scarlett-os"
# It is autogenerated by the Meson build system.
# Do not edit by hand.

ninja_required_version = 1.5.1

# Rules for compiling.

rule c_COMPILER
 command = ccache gcc $ARGS  -MD -MQ $out -MF '$DEPFILE' -o $out -c $in
 deps = gcc
 depfile = $DEPFILE
 description = Compiling C object $out.

rule c_PCH
 command = ccache gcc $ARGS  -MD -MQ $out -MF '$DEPFILE' -o $out -c $in
 deps = gcc
 depfile = $DEPFILE
 description = Precompiling header $in.


# Rules for linking.

rule STATIC_LINKER
 command =  rm -f $out && ar $LINK_ARGS $out $in
 description = Linking static target $out.

rule c_LINKER
 command = ccache gcc $ARGS -o $out $in $LINK_ARGS  $aliasing
 description = Linking target $out.


rule SHSYM
 command = /app/bin/python3.5 /app/bin/meson --internal symbolextractor $in $out $CROSS
 restat = 1
 description = Generating symbol file $out.

# Other rules

rule CUSTOM_COMMAND
 command = $COMMAND
 description = $DESC
 restat = 1

rule CUSTOM_COMMAND_DEP
 command = $COMMAND
 description = $DESC
 deps = gcc
 depfile = $DEPFILE
 restat = 1

rule REGENERATE_BUILD
 command = /app/bin/python3.5 /app/bin/meson --internal regenerate /home/pi/dev/scarlett_os-dev/scarlett_os /home/pi/dev/scarlett_os-dev/scarlett_os/mesonbuild --backend ninja
 description = Regenerating build files.
 generator = 1


# Phony build target, always out of date
build PHONY: phony

# Build rules for targets

# Test rules

build meson-test: CUSTOM_COMMAND all PHONY
 COMMAND = /app/bin/python3.5 -u /app/bin/meson test --no-rebuild --print-errorlogs
 DESC = Running$ all$ tests.
 pool = console

build test: phony meson-test

build meson-benchmark: CUSTOM_COMMAND all PHONY
 COMMAND = /app/bin/python3.5 -u /app/bin/meson test --benchmark --logbase benchmarklog --num-processes=1 --no-rebuild
 DESC = Running$ benchmark$ suite.
 pool = console

build benchmark: phony meson-benchmark

# Install rules

build meson-install: CUSTOM_COMMAND PHONY | all
 DESC = Installing$ files.
 COMMAND = /app/bin/python3.5 /app/bin/meson --internal install /home/pi/dev/scarlett_os-dev/scarlett_os/mesonbuild/meson-private/install.dat
 pool = console

build install: phony meson-install

build meson-dist: CUSTOM_COMMAND PHONY
 DESC = Creating$ source$ packages
 COMMAND = /app/bin/python3.5 /app/bin/meson --internal dist /home/pi/dev/scarlett_os-dev/scarlett_os /home/pi/dev/scarlett_os-dev/scarlett_os/mesonbuild /app/bin/python3.5 /app/bin/meson
 pool = console

build dist: phony meson-dist

# Suffix

build meson-scan-build: CUSTOM_COMMAND PHONY
 COMMAND = /app/bin/python3.5 /app/bin/meson --internal scanbuild /home/pi/dev/scarlett_os-dev/scarlett_os /home/pi/dev/scarlett_os-dev/scarlett_os/mesonbuild /app/bin/python3.5 /app/bin/meson -Ddisable-help=false
 pool = console

build scan-build: phony meson-scan-build

build meson-uninstall: CUSTOM_COMMAND PHONY
 COMMAND = /app/bin/python3.5 /app/bin/meson --internal uninstall
 pool = console

build uninstall: phony meson-uninstall

build all: phony

default all

build clean: phony meson-clean

build meson-clean: CUSTOM_COMMAND PHONY
 COMMAND = ninja -t clean
 description = Cleaning.

build build.ninja: REGENERATE_BUILD ../meson.build ../data/meson.build ../data/icons/meson.build ../getenvvar.py ../scarlett_os/shim.py.in ../mesonbuild/shim.py ../bin/meson.build ../bin/scarlett.in ../mesonbuild/bin/scarlett ../tests/meson.build meson-private/coredata.dat ../meson_options.txt
 pool = console

build reconfigure: REGENERATE_BUILD PHONY
 pool = console

build ../meson.build ../data/meson.build ../data/icons/meson.build ../getenvvar.py ../scarlett_os/shim.py.in ../mesonbuild/shim.py ../bin/meson.build ../bin/scarlett.in ../mesonbuild/bin/scarlett ../tests/meson.build meson-private/coredata.dat ../meson_options.txt: phony

(scarlett-flatpak) (pyvenv) [pi@avengers-tower, load: 0.11] (Mon Jun 11 - 00:52:47)
~/dev/scarlett_os-dev/scarlett_os/mesonbuild $

```

# Look at these paths, inside flatpak sandbox env

```
Installing /home/pi/dev/scarlett_os-dev/scarlett_os/mesonbuild/shim.py to /app/lib/scarlett_os/python/scarlett_os
Installing /home/pi/dev/scarlett_os-dev/scarlett_os/mesonbuild/bin/scarlett to /app/bin
```

# OSX Python Environment Isolated virtualenv w/ pyenv

https://stackoverflow.com/questions/22771204/virtualenv-that-can-find-relocated-libraires-like-mysqlclient-lib-for-mysqldb

### Example 1. (nteract: LD_LIBRARY_PATH and DYLD_LIBRARY_PATH not imported on OS X )

https://github.com/nteract/nteract/issues/1523#issuecomment-301623519

```
For what it's worth, rather than disable SIP, I've resorted to linking the .dylib objects into /usr/local/lib. E.g., ln -s $ORACLE_HOME/*.dylib* /usr/local/lib
```

### Example 2. https://github.com/splashkit/splashkit-core/issues/100

```
from ctypes import *
from enum import Enum

cdll.LoadLibrary("/Users/Alex/.splashkit/lib/libSplashKit.dylib")
sklib = CDLL("/Users/Alex/.splashkit/lib/libsplashkit.dylib")
```

### Example 3. https://kb.iu.edu/d/aonm

```
Change your LD_LIBRARY_PATH environment variable (to make the new Python available); for example, add the following line to the bottom of your ~/.bashrc file:
  export LD_LIBRARY_PATH=~/pythonbuild/lib:$LD_LIBRARY_PATH
```


# Virtualenv's bin/activate is Doing It Wrong

https://gist.github.com/datagrok/2199506

Implementations based on this ^ :
- https://github.com/berdario/pew
- https://github.com/sashahart/vex


```
 |2.4.2|    hyenatop in /usr/local/Cellar
○ → find . -name "*pkgconfig" -print
```


# The most basic jhbuildrc( used on vagrant 16.04 instance )

```
import os
prefix='/home/pi/jhbuild'
checkoutroot='/home/pi/gnome'
moduleset = 'gnome-world'
interact = False
makeargs = '-j4'
os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
os.environ['PYTHON'] = '/usr/bin/python3'
os.environ['PROMPT_COMMAND'] = ''
```


# GstPocketSphinx object. dump()

```
obj.__class__ = <class '__gi__.GstPocketSphinx'>
obj.__copy__ = <built-in method __copy__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__deepcopy__ = <built-in method __deepcopy__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__delattr__ = <method-wrapper '__delattr__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__dict__ = {}
obj.__dir__ = <built-in method __dir__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__doc__ = Object GstPocketSphinx

Properties from GstPocketSphinx:
  hmm -> gchararray: HMM Directory
    Directory containing acoustic model parameters
  lm -> gchararray: LM File
    Language model file
  lmctl -> gchararray: LM Control File
    Language model control file (for class LMs)
  dict -> gchararray: Dictionary File
    Dictionary File
  fsg -> gchararray: FSG File
    Finite state grammar file
  fwdflat -> gboolean: Flat Lexicon Search
    Enable Flat Lexicon Search
  bestpath -> gboolean: Graph Search
    Enable Graph Search
  maxhmmpf -> gint: Maximum HMMs per frame
    Maximum number of HMMs searched per frame
  maxwpf -> gint: Maximum words per frame
    Maximum number of words searched per frame
  beam -> gdouble: Beam width applied to every frame in Viterbi search
    Beam width applied to every frame in Viterbi search
  wbeam -> gdouble: Beam width applied to word exits
    Beam width applied to phone transitions
  pbeam -> gdouble: Beam width applied to phone transitions
    Beam width applied to phone transitions
  dsratio -> gint: Frame downsampling ratio
    Evaluate acoustic model every N frames
  latdir -> gchararray: Lattice Directory
    Output Directory for Lattices
  lmname -> gchararray: LM Name
    Language model name (to select LMs from lmctl)
  decoder -> PSDecoder: Decoder object
    The underlying decoder

Signals from GstElement:
  pad-added (GstPad)
  pad-removed (GstPad)
  no-more-pads ()

Signals from GstObject:
  deep-notify (GstObject, GParam)

Properties from GstObject:
  name -> gchararray: Name
    The name of the object
  parent -> GstObject: Parent
    The parent of the object

Signals from GObject:
  notify (GParam)


obj.__eq__ = <method-wrapper '__eq__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__format__ = <built-in method __format__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__gdoc__ = Object GstPocketSphinx

Properties from GstPocketSphinx:
  hmm -> gchararray: HMM Directory
    Directory containing acoustic model parameters
  lm -> gchararray: LM File
    Language model file
  lmctl -> gchararray: LM Control File
    Language model control file (for class LMs)
  dict -> gchararray: Dictionary File
    Dictionary File
  fsg -> gchararray: FSG File
    Finite state grammar file
  fwdflat -> gboolean: Flat Lexicon Search
    Enable Flat Lexicon Search
  bestpath -> gboolean: Graph Search
    Enable Graph Search
  maxhmmpf -> gint: Maximum HMMs per frame
    Maximum number of HMMs searched per frame
  maxwpf -> gint: Maximum words per frame
    Maximum number of words searched per frame
  beam -> gdouble: Beam width applied to every frame in Viterbi search
    Beam width applied to every frame in Viterbi search
  wbeam -> gdouble: Beam width applied to word exits
    Beam width applied to phone transitions
  pbeam -> gdouble: Beam width applied to phone transitions
    Beam width applied to phone transitions
  dsratio -> gint: Frame downsampling ratio
    Evaluate acoustic model every N frames
  latdir -> gchararray: Lattice Directory
    Output Directory for Lattices
  lmname -> gchararray: LM Name
    Language model name (to select LMs from lmctl)
  decoder -> PSDecoder: Decoder object
    The underlying decoder

Signals from GstElement:
  pad-added (GstPad)
  pad-removed (GstPad)
  no-more-pads ()

Signals from GstObject:
  deep-notify (GstObject, GParam)

Properties from GstObject:
  name -> gchararray: Name
    The name of the object
  parent -> GstObject: Parent
    The parent of the object

Signals from GObject:
  notify (GParam)


obj.__ge__ = <method-wrapper '__ge__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__getattribute__ = <method-wrapper '__getattribute__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__gpointer__ = <capsule object NULL at 0x7efe63156b70>
obj.__grefcount__ = 2
obj.__gsignals__ = {}
obj.__gt__ = <method-wrapper '__gt__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__gtype__ = <GType GstPocketSphinx (139630796424528)>
obj.__hash__ = <method-wrapper '__hash__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__info__ = ObjectInfo(Element)
obj.__init__ = <method-wrapper '__init__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__le__ = <method-wrapper '__le__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__lt__ = <method-wrapper '__lt__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__module__ = __gi__
obj.__ne__ = <method-wrapper '__ne__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__new__ = <built-in method __new__ of _GObjectMetaBase object at 0x7efe6f92a2a0>
obj.__reduce__ = <built-in method __reduce__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__reduce_ex__ = <built-in method __reduce_ex__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__repr__ = <method-wrapper '__repr__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__setattr__ = <method-wrapper '__setattr__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__sizeof__ = <built-in method __sizeof__ of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__str__ = <method-wrapper '__str__' of GstPocketSphinx object at 0x7efe628dd8b8>
obj.__subclasshook__ = <built-in method __subclasshook__ of GObjectMeta object at 0x7efe5406ca18>
obj._force_floating = gi.FunctionInfo(force_floating)
obj._gst_reserved = [0, 0, 0]
obj._ref = gi.FunctionInfo(ref)
obj._ref_sink = gi.FunctionInfo(ref_sink)
obj._unref = gi.FunctionInfo(unref)
obj._unsupported_data_method = <bound method Object._unsupported_data_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj._unsupported_method = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.abort_state = gi.FunctionInfo(abort_state)
obj.add_control_binding = gi.FunctionInfo(add_control_binding)
obj.add_metadata = <bound method add_metadata of <class '__gi__.GstPocketSphinx'>>
obj.add_pad = gi.FunctionInfo(add_pad)
obj.add_pad_template = <bound method add_pad_template of <class '__gi__.GstPocketSphinx'>>
obj.add_static_metadata = <bound method add_static_metadata of <class '__gi__.GstPocketSphinx'>>
obj.add_static_pad_template = <bound method add_static_pad_template of <class '__gi__.GstPocketSphinx'>>
obj.base_time = 0
obj.bind_property = <built-in method bind_property of GstPocketSphinx object at 0x7efe628dd8b8>
obj.bind_property_full = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.bus = <Gst.Bus object at 0x7efe628dd990 (GstBus at 0x7efe54016970)>
obj.chain = <built-in method chain of GstPocketSphinx object at 0x7efe628dd8b8>
obj.change_state = gi.FunctionInfo(change_state)
obj.check_uniqueness = gi.FunctionInfo(check_uniqueness)
obj.clock = None
obj.compat_control = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.connect = <built-in method connect of GstPocketSphinx object at 0x7efe628dd8b8>
obj.connect_after = <built-in method connect_after of GstPocketSphinx object at 0x7efe628dd8b8>
obj.connect_data = <bound method Object.connect_data of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.connect_object = <built-in method connect_object of GstPocketSphinx object at 0x7efe628dd8b8>
obj.connect_object_after = <built-in method connect_object_after of GstPocketSphinx object at 0x7efe628dd8b8>
obj.contexts = []
obj.continue_state = gi.FunctionInfo(continue_state)
obj.control_bindings = []
obj.control_rate = 100000000
obj.create_all_pads = gi.FunctionInfo(create_all_pads)
obj.current_state = <enum GST_STATE_NULL of type Gst.State>
obj.default_deep_notify = gi.FunctionInfo(default_deep_notify)
obj.default_error = gi.FunctionInfo(default_error)
obj.disconnect = <bound method _signalmethod.<locals>.meth of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.disconnect_by_func = <built-in method disconnect_by_func of GstPocketSphinx object at 0x7efe628dd8b8>
obj.do_change_state = gi.VFuncInfo(change_state)
obj.do_deep_notify = gi.VFuncInfo(deep_notify)
obj.do_get_state = gi.VFuncInfo(get_state)
obj.do_no_more_pads = gi.VFuncInfo(no_more_pads)
obj.do_pad_added = gi.VFuncInfo(pad_added)
obj.do_pad_removed = gi.VFuncInfo(pad_removed)
obj.do_post_message = gi.VFuncInfo(post_message)
obj.do_provide_clock = gi.VFuncInfo(provide_clock)
obj.do_query = gi.VFuncInfo(query)
obj.do_release_pad = gi.VFuncInfo(release_pad)
obj.do_request_new_pad = gi.VFuncInfo(request_new_pad)
obj.do_send_event = gi.VFuncInfo(send_event)
obj.do_set_bus = gi.VFuncInfo(set_bus)
obj.do_set_clock = gi.VFuncInfo(set_clock)
obj.do_set_context = gi.VFuncInfo(set_context)
obj.do_set_state = gi.VFuncInfo(set_state)
obj.do_state_changed = gi.VFuncInfo(state_changed)
obj.emit = <built-in method emit of GstPocketSphinx object at 0x7efe628dd8b8>
obj.emit_stop_by_name = <bound method Object.stop_emission of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.find_property = <bound method find_property of <class '__gi__.GstPocketSphinx'>>
obj.flags = 0
obj.force_floating = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.freeze_notify = <bound method Object.freeze_notify of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.g_type_instance = <GObject.TypeInstance object at 0x7efe628de3b8 (void at 0x7efe54010150)>
obj.get_base_time = gi.FunctionInfo(get_base_time)
obj.get_bus = gi.FunctionInfo(get_bus)
obj.get_clock = gi.FunctionInfo(get_clock)
obj.get_compatible_pad = gi.FunctionInfo(get_compatible_pad)
obj.get_compatible_pad_template = gi.FunctionInfo(get_compatible_pad_template)
obj.get_context = gi.FunctionInfo(get_context)
obj.get_context_unlocked = gi.FunctionInfo(get_context_unlocked)
obj.get_contexts = gi.FunctionInfo(get_contexts)
obj.get_control_binding = gi.FunctionInfo(get_control_binding)
obj.get_control_rate = gi.FunctionInfo(get_control_rate)
obj.get_data = <bound method Object._unsupported_data_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.get_factory = gi.FunctionInfo(get_factory)
obj.get_g_value_array = gi.FunctionInfo(get_g_value_array)
obj.get_metadata = <bound method get_metadata of <class '__gi__.GstPocketSphinx'>>
obj.get_name = gi.FunctionInfo(get_name)
obj.get_pad_template = <bound method get_pad_template of <class '__gi__.GstPocketSphinx'>>
obj.get_pad_template_list = <bound method get_pad_template_list of <class '__gi__.GstPocketSphinx'>>
obj.get_parent = gi.FunctionInfo(get_parent)
obj.get_path_string = gi.FunctionInfo(get_path_string)
obj.get_properties = <built-in method get_properties of GstPocketSphinx object at 0x7efe628dd8b8>
obj.get_property = <built-in method get_property of GstPocketSphinx object at 0x7efe628dd8b8>
obj.get_qdata = <bound method Object._unsupported_data_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.get_request_pad = gi.FunctionInfo(get_request_pad)
obj.get_start_time = gi.FunctionInfo(get_start_time)
obj.get_state = gi.FunctionInfo(get_state)
obj.get_static_pad = gi.FunctionInfo(get_static_pad)
obj.get_value = gi.FunctionInfo(get_value)
obj.get_value_array = gi.FunctionInfo(get_value_array)
obj.handler_block = <bound method signal_handler_block of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.handler_block_by_func = <built-in method handler_block_by_func of GstPocketSphinx object at 0x7efe628dd8b8>
obj.handler_disconnect = <bound method _signalmethod.<locals>.meth of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.handler_is_connected = <bound method _signalmethod.<locals>.meth of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.handler_unblock = <bound method _signalmethod.<locals>.meth of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.handler_unblock_by_func = <built-in method handler_unblock_by_func of GstPocketSphinx object at 0x7efe628dd8b8>
obj.has_active_control_bindings = gi.FunctionInfo(has_active_control_bindings)
obj.has_ancestor = gi.FunctionInfo(has_ancestor)
obj.has_as_ancestor = gi.FunctionInfo(has_as_ancestor)
obj.has_as_parent = gi.FunctionInfo(has_as_parent)
obj.install_properties = <bound method install_properties of <class '__gi__.GstPocketSphinx'>>
obj.install_property = <bound method install_property of <class '__gi__.GstPocketSphinx'>>
obj.interface_find_property = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.interface_install_property = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.interface_list_properties = <bound method Object._unsupported_method of <__gi__.GstPocketSphinx object at 0x7efe628dd8b8 (GstPocketSphinx at 0x7efe54010150)>>
obj.is_floating = gi.FunctionInfo(is_floating)
obj.is_locked_state = gi.FunctionInfo(is_locked_state)
obj.iterate_pads = gi.FunctionInfo(iterate_pads)
obj.iterate_sink_pads = gi.FunctionInfo(iterate_sink_pads)
obj.iterate_src_pads = gi.FunctionInfo(iterate_src_pads)
obj.last_return = <enum GST_STATE_CHANGE_SUCCESS of type Gst.StateChangeReturn>
obj.last_sync = 18446744073709551615
obj.link = gi.FunctionInfo(link)
obj.link_filtered = gi.FunctionInfo(link_filtered)
obj.link_pads = gi.FunctionInfo(link_pads)
obj.link_pads_filtered = gi.FunctionInfo(link_pads_filtered)
obj.link_pads_full = gi.FunctionInfo(link_pads_full)
obj.list_properties = <bound method list_properties of <class '__gi__.GstPocketSphinx'>>
2018-08-08 23:43:47,099 scarlett_os.utility.gnome (Thread #748) ERROR    (wrapper) Exception Thrown from [/home/pi/dev/bossjones-github/scarlett_os/scarlett_os/internal/debugger.py] on line [162] via function [dump]
2018-08-08 23:43:47,099 scarlett_os.utility.gnome (Thread #748) ERROR    (wrapper) Exception type NotImplementedError: getting an union is not supported yet
emit ('aborted', (<class 'NotImplementedError'>, NotImplementedError('getting an union is not supported yet',), <traceback object at 0x7efe628df3c8>))
```

# pocketsphinx_continuous

```

/home/pi/dev/bossjones-github/scarlett_os/scarlett_os/listener.py:202: PyGIDeprecationWarning: GObject.MainLoop is deprecated; use GLib.MainLoop instead
  self.__loop = GObject.MainLoop()
Running <ScarlettListenerI(Thread #276, started 140638293059328)>
Current configuration:
[NAME]                  [DEFLT]         [VALUE]
-agc                    none            none
-agcthresh              2.0             2.000000e+00
-allphone
-allphone_ci            no              no
-alpha                  0.97            9.700000e-01
-ascale                 20.0            2.000000e+01
-aw                     1               1
-backtrace              no              no
-beam                   1e-48           1.000000e-48
-bestpath               yes             yes
-bestpathlw             9.5             9.500000e+00
-ceplen                 13              13
-cmn                    current         current
-cmninit                8.0             40,3,-1
-compallsen             no              no
-debug                                  0
-dict                                   /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
-dictcase               no              no
-dither                 no              no
-doublebw               no              no
-ds                     1               1
-fdict
-feat                   1s_c_d_dd       1s_c_d_dd
-featparams
-fillprob               1e-8            1.000000e-08
-frate                  100             100
-fsg
-fsgusealtpron          yes             yes
-fsgusefiller           yes             yes
-fwdflat                yes             yes
-fwdflatbeam            1e-64           1.000000e-64
-fwdflatefwid           4               4
-fwdflatlw              8.5             8.500000e+00
-fwdflatsfwin           25              25
-fwdflatwbeam           7e-29           7.000000e-29
-fwdtree                yes             yes
-hmm                                    /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
-input_endian           little          little
-jsgf
-keyphrase
-kws
-kws_delay              10              10
-kws_plp                1e-1            1.000000e-01
-kws_threshold          1               1.000000e+00
-latsize                5000            5000
-lda
-ldadim                 0               0
-lifter                 0               22
-lm                                     /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
-lmctl
-lmname
-logbase                1.0001          1.000100e+00
-logfn
-logspec                no              no
-lowerf                 133.33334       1.300000e+02
-lpbeam                 1e-40           1.000000e-40
-lponlybeam             7e-29           7.000000e-29
-lw                     6.5             6.500000e+00
-maxhmmpf               30000           3000
-maxwpf                 -1              -1
-mdef
-mean
-mfclogdir
-min_endfr              0               0
-mixw
-mixwfloor              0.0000001       1.000000e-07
-mllr
-mmap                   yes             yes
-ncep                   13              13
-nfft                   512             512
-nfilt                  40              25
-nwpen                  1.0             1.000000e+00
-pbeam                  1e-48           1.000000e-48
-pip                    1.0             1.000000e+00
-pl_beam                1e-10           1.000000e-10
-pl_pbeam               1e-10           1.000000e-10
-pl_pip                 1.0             1.000000e+00
-pl_weight              3.0             3.000000e+00
-pl_window              5               5
-rawlogdir
-remove_dc              no              no
-remove_noise           yes             yes
-remove_silence         yes             yes
-round_filters          yes             yes
-samprate               16000           1.600000e+04
-seed                   -1              -1
-sendump
-senlogdir
-senmgau
-silprob                0.005           5.000000e-03
-smoothspec             no              no
-svspec                                 0-12/13-25/26-38
-tmat
-tmatfloor              0.0001          1.000000e-04
-topn                   4               4
-topn_beam              0               0
-toprule
-transform              legacy          dct
-unit_area              yes             yes
-upperf                 6855.4976       6.800000e+03
-uw                     1.0             1.000000e+00
-vad_postspeech         50              50
-vad_prespeech          20              20
-vad_startspeech        10              10
-vad_threshold          2.0             2.000000e+00
-var
-varfloor               0.0001          1.000000e-04
-varnorm                no              no
-verbose                no              no
-warp_params
-warp_type              inverse_linear  inverse_linear
-wbeam                  7e-29           7.000000e-29
-wip                    0.65            6.500000e-01
-wlen                   0.025625        2.562500e-02

```

# Pocketsphinx how do I make it fast

```
How do I make it fast?

The default settings are not enough to achieve sub-realtime performance on most tasks. Here are some command-line flags you should experiment with:

-beam: Beam width applied to every frame in Viterbi search (smaller values mean wider beam)"

-pbeam: Beam width applied to phone transitions

-wbeam: Beam width applied to word exits

Main parameters to configure search width and thus accuracy-performance balance.

-ds

This is the dsratio. In most cases -ds 2 gives the best performance, though accuracy suffers a bit. (Frame GMM computation downsampling ratio) Thus lower should be better and higher should be less accurate.

-topn

The default value is 4, the fastest value is 2, but accuracy can suffer a bit depending on your acoustic model.

-lpbeam

This beam is quite important for performance, however the default setting is pretty narrow already. Run pocketsphinx_batch with no arguments to see what it is.

-lponlybeam

Likewise here as with -lpbeam. If you are finding it hard to get enough accuracy, you can widen these beams.

-maxwpf

This can be set quite low and still give you reasonable performance - try 5.

-maxhmmpf

Depending on the acoustic and language model this can be very helpful. Try 3000.

-pl_window

Phonetic lookahead is a specific technique which is used to speedup decoding by reducing the amount of computation. Basically everything is decoded with phonetic decoder first and then detailed search is restricted by the results of the fast phonetic search. It’s also called “Fast match”. For details and evaluations see the chapter “4.5 Phonetic Fast Match” in Efficient Algorithms for Speech Recognition Mosur K. Ravishankar

pl_window specifies lookahead distance in frames. Typical values are from 0 (don’t use lookahead) to 10 (decode 10 frames ahead). Bigger values give faster decoding but reduced accuracy.
```
