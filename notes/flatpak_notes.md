http://docs.flatpak.org/en/latest/sandbox-permissions.html

```
"finish-args": [
        "--share=ipc", "--socket=x11",
        "--share=network",
        "--socket=wayland",
        "--talk-name=org.freedesktop.Tracker1",
        "--env=TRACKER_SPARQL_BACKEND=bus",
        "--talk-name=org.gnome.OnlineAccounts",
        "--filesystem=xdg-run/dconf", "--filesystem=~/.config/dconf:ro",
        "--talk-name=ca.desrt.dconf", "--env=DCONF_USER_CONFIG_DIR=.config/dconf",
        "--talk-name=com.intel.dleyna-server",
        "--socket=pulseaudio",
        "--filesystem=xdg-music",
        "--filesystem=xdg-cache/media-art"
    ],
```

http://docs.flatpak.org/en/latest/manifests.html
http://docs.flatpak.org/en/latest/flatpak-builder-command-reference.html


```
1.2.2 Using Flatpak
This page provides an introduction to the flatpak command line tool, including the most common commands
needed to use Flatpak.
The flatpak command
flatpak is the primary Flatpak command, to which specific commands are appended. For example, the command
to install something is flatpak install and the command to uninstall is flatpak uninstall.
Identifiers
Flatpak identifies each application and runtime using a unique three-part identifier, such as com.company.App.
The final segment of this address is the object’s name, and the preceding part identifies the developer, so that the same
developer can have multiple applications, like com.company.App1 and com.company.App2.
Developers should follow the standard D-Bus naming conventions when creating their own IDs. If an application
provides a D-Bus service, the D-Bus service name is expected to be the same as the application ID.
Identifier triples
Typically it is sufficient to refer to objects using their ID. However, in some situations it is necessary to refer to a
specific version of an object, or to a specific architecture. For example, some applications might be available as a
stable and a testing version, in which case it is necessary to specify which one you want to install.
Flatpak allows architectures and versions to be specified using an object’s identifier triple. This takes the form of
name/architecture/branch, such as com.company.App/i386/stable. (Branch is the term used to
refer to versions of the same object.) The first part of the triple is the ID, the second part is the architecture, and the
third part is the branch.
The Flatpak CLI provides feedback if an identifier triple is required, instead of the standard object ID.
System versus user
Flatpak commands can be run either system-wide or per-user. Applications and runtimes that are installed systemwide
are available to all users on the system. Applications and runtimes that are installed per-user are only available
to the users that installed them.
The same principle applies to repositories - repositories that have been added system-wide are available to all users,
whereas per-user repositories can only be used by a particular user.
Flatpak commands are run system-wide by default. If you are installing applications for day-to-day usage, it is recommended
to stick with this default behavior.
However, running commands per-user can be useful for testing and development purposes, since objects that are
installed in this way won’t be available to other users on the system. To do this, use the --user option, which can be
used in combination with most flatpak commands.
Commands behave in exactly the same way if they are run per-user rather than system-wide.
```


https://steemit.com/utopian-io/@tingping/create-script-to-generate-flatpak-manifest-from-pip-packages

https://github.com/flatpak/flatpak/wiki/Tips-&-Tricks

https://github.com/flatpak/flatpak/issues/178

http://docs.flatpak.org/en/latest/flatpak-builder.html
