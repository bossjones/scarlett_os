# pulseaudio minimal setup for travis and testing

```
FIXME: Implement this!
```

source: https://unix.stackexchange.com/questions/105964/launch-a-fake-minimal-x-session-for-pulseaudio-dbus


You can use Xvfb, which is X server with a virtual framebuffer, i.e. an X server that displays only in memory and doesn't connect to any hardware. You don't need to run any client you don't want on that server, and in particular no desktop environment or window manager.

```
Xvfb :1 -screen 0 1x1x8 &
```

After this:

```
DISPLAY=:1 dbus-launch
DISPLAY=:1 pulseaudio --start
```

You need to wait a little after starting Xvfb for the display to be available. You can use xinit to start an X server and then start clients when it's ready. Put the commands you want to run in a script (note that when the script exits, the X server exits):

```
#!/bin/sh
dbus-launch
pulseaudio --start
sleep 99999999
```

Start the virtual X server with

`xinit /path/to/client.script -- /usr/bin/Xvfb :1 -screen 0 1x1x8`

If you want to run it at boot time, you can start it from cron. Run crontab -e (as your user, not as root) and add the line

`@reboot xinit /path/to/client.script -- Xvfb :1 -screen 0 1x1x8`

If you want to kill this session, kill the xinit process.


# Another thing to try?

https://github.com/mk-fg/pulseaudio-mixer-cli/issues/17

# Excellent example

https://github.com/LABSN/expyfun/blob/master/.travis.yml

# Another example ... from 2015, specifically for continuious integration

https://github.com/coala/coala/commit/76284149fefc30e6edfb96d21ad180987e0810f5