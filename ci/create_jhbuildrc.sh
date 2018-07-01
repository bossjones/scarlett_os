# FIXME:
# FIXME:
# FIXME:
# FIXME:
# FIXME:

# THIS IS TAKEN FROM avengers-tower server. Automate the creation of this

import os
prefix='/home/pi/jhbuild'
checkoutroot='/home/pi/gnome'
moduleset = 'gnome-world'
interact = False
makeargs = '-j4'
os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
os.environ['PYTHON'] = 'python'
os.environ['GSTREAMER'] = '1.0'
os.environ['ENABLE_PYTHON3'] = 'yes'
os.environ['ENABLE_GTK'] = 'yes'
os.environ['PYTHON_VERSION'] = '3.5'
os.environ['CFLAGS'] = '-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer'
os.environ['MAKEFLAGS'] = '-j4'
os.environ['PREFIX'] = '/home/pi/jhbuild'
os.environ['JHBUILD'] = '/home/pi/gnome'
os.environ['PATH'] = '/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/home/pi/jhbuild/bin:/home/pi/jhbuild/sbin:/home/pi/.pyenv/shims:~/.pyenv/bin/:~/.bin:/home/pi/.local/bin:/home/pi/.rbenv/shims:/home/pi/.rbenv/bin:/home/pi/.nvm/versions/node/v8.7.0/bin:/usr/lib64/ccache:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/pi/.rvm/bin:/home/pi/.go/bin:/home/pi/go/bin'
os.environ['LD_LIBRARY_PATH'] = '/home/pi/jhbuild/lib:/home/pi/jhbuild/lib:/usr/lib'
os.environ['PYTHONPATH'] = '/home/pi/.pyenv/versions/3.5.2/lib/python3.5/site-packages:/home/pi/jhbuild/lib/python3.5/site-packages:/usr/lib/python3.5/site-packages'
os.environ['PKG_CONFIG_PATH'] = '/home/pi/.pyenv/versions/3.5.2/lib/pkgconfig:/home/pi/jhbuild/lib/pkgconfig:/home/pi/jhbuild/share/pkgconfig:/usr/lib/pkgconfig'
os.environ['XDG_DATA_DIRS'] = '/home/pi/jhbuild/share:/usr/share'
os.environ['XDG_CONFIG_DIRS'] = '/home/pi/jhbuild/etc/xdg'
os.environ['CC'] = 'gcc'
os.environ['PROJECT_HOME'] = '/home/pi/dev'
os.environ['PYTHONSTARTUP'] = '/home/pi/.pythonrc'

# FIXME:
# it needs to live in ~/.config/jhbuildrc
