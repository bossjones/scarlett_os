#!/usr/bin/env python3

import json as jsonlib
import requests
import os
import hashlib
import argparse

# SOURCE: https://github.com/AdrianKoshka/flatpak-tools/blob/master/org.mozilla.Thunderbird/genman.py

# Setup arguments to be parsed
parser = argparse.ArgumentParser(description="Auto generates ScarlettOS' flatpak manifest")
parser.add_argument("-r", "--release", help="ScarlettOS release version")
parser.add_argument("-o", "--output", help="File to write to", default="org.scarlett.ScarlettOS.updated.json")
args = parser.parse_args()

# File to output the JSON to
output_file = args.output

# Version of the GNOME runtime to use
gnome_runtime = "3.24"
python_vers = "3.5.2"

# Take the thunderbird release from the '-r' or --release' argument
release = args.release

# A function which takes a URL, requests the content, and makes a sha256 hash
# of it, and then returns said hash
def hashsrc(url):
    print("Getting " + url)
    r = requests.get(url)
    sha256 = hashlib.sha256()
    sha256.update(r.content)
    filechecksum = sha256.hexdigest()
    return(filechecksum)


fin_args = [
    # / * Allow access to developer tools * /
    "--allow=devel",
    "--talk-name=org.freedesktop.Flatpak",
    # / * X11 + XShm access * /
    "--socket=x11",
    "--share=ipc",
    # /* OpenGL */
    "--device=dri",
    # /* Wayland access */
    "--socket=wayland",
    # /* Audio output */
    "--socket=pulseaudio",

    # /* We want full fs access */
    "--filesystem=host",
    "--filesystem=home",


    # /* Allow communication with network */
    "--share=network",
    "--talk-name=org.gtk.vfs.*",

    # /* Needed for dconf to work (+ host or homedir read access from above) */
    "--filesystem=xdg-run/dconf",
    "--filesystem=~/.config/dconf:ro",
    "--talk-name=ca.desrt.dconf",
    "--env=DCONF_USER_CONFIG_DIR=.config/dconf",

    #  /* We need access to auth agents */
    "--talk-name=org.freedesktop.secrets",
    "--filesystem=xdg-run/keyring",

    # / * Needed for various SSL certificates to work * /
    "--env=SSL_CERT_DIR=/etc/ssl/certs",
    "--filesystem=/etc/ssl:ro",
    "--filesystem=/etc/pki:ro",
    "--filesystem=/etc/ca-certificates:ro",

    # / * Keep system terminal mappings * /
    "--filesystem=/etc/inputrc:ro",

    # / * Chromium uses a socket in tmp for its singleton check * /
    "--filesystem=/tmp",

    "--own-name=org.scarlett.Listener",
    "--own-name=org.scarlett.Listener.*",

    # Bunch of dbus session bus stuff
    "--talk-name=org.freedesktop.DBus.Proprieties",
    "--talk-name=org.freedesktop.IBus",
    "--talk-name=org.freedesktop.Notifications",

    # Applications sometimes need to interact with the desktop's file manager.
    # SOURCE: https://www.freedesktop.org/wiki/Specifications/file-manager-interface/
    "--talk-name=org.freedesktop.FileManager1",

    # Gnome settings daemon
    "--talk-name=org.gnome.SettingsDaemon.Color",
    "--talk-name=org.freedesktop.PackageKit",

    # Ability to talk to polkit
    "--system-talk-name=org.freedesktop.PolicyKit1",

    # Sysprof kernel based performance profiler for Linux
    # SOURCE: https://github.com/GNOME/sysprof
    "--system-talk-name=org.gnome.Sysprof2",

    # gnome-code-assistance is a project which aims to provide common code assistance
    # services for code editors(simple editors as well as IDEs). It is an effort to
    # provide a centralized code - assistance as a service for the GNOME platform
    # instead of having every editor implement their own solution.

    # SOURCE: https://github.com/GNOME/gnome-code-assistance
    "--talk-name=org.gnome.CodeAssist.v1.*",

    "--system-talk-name=org.freedesktop.login1",

    "--socket=session-bus",
    "--system-talk-name=org.freedesktop.Avahi",

    "--filesystem=~/.local/share/flatpak",
    "--filesystem=/var/lib/flatpak",
    "--filesystem=xdg-data/meson"

]

# # Define the finish-args
# fin_args = [
#     "--share=ipc",
#     "--socket=x11",
#     "--device=dri",
#     "--share=network",
#     "--socket=pulseaudio",
#     "--filesystem=~/.cache/thunderbird:create",
#     "--filesystem=~/.thunderbird:create",
#     "--filesystem=home:ro",
#     "--filesystem=xdg-download:rw",
#     "--filesystem=xdg-run/dconf",
#     "--filesystem=~/.config/dconf:ro",
#     "--talk-name=ca.desrt.dconf",
#     "--env=DCONF_USER_CONFIG_DIR=.config/dconf",
#     "--talk-name=org.a11y.*",
#     "--talk-name=org.freedesktop.Notifications"
# ]

# Define the files/directories to cleanup
# clnup = [
#     "/include",
#     "/lib/pkgconfig",
#     "/share/pkgconfig",
#     "/share/aclocal",
#     "/man",
#     "/share/man",
#     "*.la",
#     "*.a"
# ]
clnup = []

# Define the structure for the build-options section
build_opts = {}
build_opts["cflags"] = "-O2 -g"
build_opts["cxxflags"] = "-O2 -g"
build_opts["env"] = {
    "V": "1",
    "BASH_COMPLETIONSDIR": "/app/share/bash-completion/completions",
    "MOUNT_FUSE_PATH": "../tmp/"
}

# Define the modules section
mdles = []

#########################################################
# Autoconf sources
#########################################################
acsrcs = []
acsrc = {}
acsrc["type"] = "archive"
acsrc["url"] = "http://ftp.gnu.org/gnu/autoconf/autoconf-2.13.tar.gz"
acsrc["sha256"] = hashsrc(acsrc["url"])
acsrcs.append(acsrc)

# Autoconf module
ac = {}
ac["name"] = "autoconf-2.13"
# ac["cleanup"] = ["*"]
ac["sources"] = acsrcs
ac["post-install"] = ["ln -s /app/bin/autoconf /app/bin/autoconf-2.13"]
mdles.append(ac)
#########################################################



#########################################################
# icu sources
#########################################################
icusrcs = []
icusrc = {}
icusrc["type"] = "archive"
icusrc["url"] = "http://download.icu-project.org/files/icu4c/60.1/icu4c-60_1-src.tgz"
icusrc["sha256"] = hashsrc(icusrc["url"])
icusrcs.append(icusrc)

# icu module
icu = {}
icu["name"] = "icu"
icu["cleanup"] = ["/bin/*", "/sbin/*"]
icu["sources"] = icusrc
icu["subdir"] = {"subdir": "source"}
mdles.append(icu)
#########################################################


#########################################################
# cpython sources
#########################################################
cpython_sources = []
cpythonsrc = {}
cpythonsrc["type"] = "archive"
cpythonsrc["url"] = "https://www.python.org/ftp/python/${python_vers}/Python-${python_vers}.tar.xz".format(python_vers=python_vers)
cpythonsrc["sha256"] = hashsrc(cpythonsrc["url"])
cpython_sources.append(cpythonsrc)

# pip source
pipsrc = {}
pipsrc["type"] = "file"
pipsrc["url"] = "https://files.pythonhosted.org/packages/ae/e8/2340d46ecadb1692a1e455f13f75e596d4eab3d11a57446f08259dee8f02/pip-10.0.1.tar.gz"
pipsrc["sha256"] = hashsrc(pipsrc["url"])
cpython_sources.append(pipsrc)
#########################################################

#########################################################
# setuptools source
#########################################################
stsrc = {}
stsrc["type"] = "file"
stsrc["url"] = "https://files.pythonhosted.org/packages/a6/5b/f399fcffb9128d642387133dc3aa9bb81f127b949cd4d9f63e5602ad1d71/setuptools-39.1.0.zip"
stsrc["sha256"] = hashsrc(stsrc["url"])
cpython_sources.append(stsrc)

# wheel source
wheelsrc = {}
wheelsrc["type"] = "file"
wheelsrc["url"] = "https://files.pythonhosted.org/packages/5d/c1/45947333669b31bc6b4933308dd07c2aa2fedcec0a95b14eedae993bd449/wheel-0.31.0.tar.gz"
wheelsrc["sha256"] = hashsrc(wheelsrc["url"])
cpython_sources.append(wheelsrc)

# cpython module
cpython = {}
cpython["name"] = "cpython"
# cpython["cleanup"] = ["*"]
cpython["sources"] = cpython_sources
cpython["post-install"] = [
    "ls -lta `pwd`",
    "/app/bin/python3 -m pip install --no-index --find-links=\"file://${PWD}\" --prefix=${FLATPAK_DEST} pip setuptools wheel"
]
cpython["build-options"] = {
    "build-args": [
        "--share=network",
        "--allow=devel"
    ],
    "config-opts": [
        "--with-pydebug"
    ],
    "cflags": "-O0 -g",
    "cxxflags": "-O0 -g",
    "strip": False,
    "no-debuginfo": False
}

mdles.append(cpython)
#########################################################


# Thunderbird build-options
# app_data_and_icons_bopt = {}
# app_data_and_icons_bopt["clfags"] = "-fno-delete-null-pointer-checks -fno-lifetime-dse -fno-schedule-insns2"
# app_data_and_icons_bopt["cxxflags"] = "-fno-delete-null-pointer-checks -fno-lifetime-dse -fno-schedule-insns2"
# app_data_and_icons_bopt["env"] = {"VERSION": release}

# Thunderbird build-commands
app_data_and_icons_bc = [
    "ls -lta",
    "env",
    "mkdir -p /app/share/metainfo/",
    "mkdir -p /app/share/appdata/",
    "mkdir -p /app/share/applications/",
    "mkdir -p /app/cache/scarlett/",
    "mkdir -p /app/share/icons/hicolor/64x64/apps/",
    "cp org.scarlett.ScarlettOS.appdata.xml /app/share/metainfo/org.scarlett.ScarlettOS.appdata.xml",
    "cp scarlettOS.png /app/share/icons/hicolor/64x64/apps/org.scarlett.ScarlettOS.png",
    "cp org.scarlett.ScarlettOS.desktop /app/share/applications/org.scarlett.ScarlettOS.desktop"
]

# Thunderbird sources
appdata_and_icons_src = []

# mozconfig source
icons_install_src = {}
icons_install_src["type"] = "file"
icons_install_src["path"] = "../../data/icons-install.sh"
icons_install_src["dest-filename"] = "icons-install.sh"
appdata_and_icons_src.append(icons_install_src)

# .desktop file
dsk_install_shell_script = {}
dsk_install_shell_script["type"] = "file"
dsk_install_shell_script["path"] = "../../data/install-desktop-file.sh"
dsk_install_shell_script["dest-filename"] = "install-desktop-file.sh"
appdata_and_icons_src.append(dsk_install_shell_script)

# AppData source
png_data = {}
png_data["type"] = "file"
png_data["path"] = "../../data/icons/64x64/scarlettOS.png"
appdata_and_icons_src.append(png_data)

# AppData source
desktop_data = {}
desktop_data["type"] = "file"
desktop_data["path"] = "../../data/ScarlettOS.desktop"
desktop_data["dest-filename"] = "org.scarlett.ScarlettOS.desktop"
appdata_and_icons_src.append(desktop_data)

appdata_xml = {}
appdata_xml["type"] = "file"
appdata_xml["path"] = "../../data/ScarlettOS.appdata.xml"
appdata_xml["dest-filename"] = "org.scarlett.ScarlettOS.appdata.xml"
appdata_and_icons_src.append(appdata_xml)

# URL formation
# burl = "https://ftp.mozilla.org/pub/thunderbird/releases/"
# srcdir = "/source/"
# srctar = "thunderbird-" + release + ".source.tar.xz"
# full_url = burl + release + srcdir + srctar

# Thunderbird source tar
# tbtarsrc = {}
# tbtarsrc["type"] = "archive"
# tbtarsrc["url"] = full_url
# tbtarsrc["sha256"] = hashsrc(tbtarsrc["url"])
# appdata_and_icons_src.append(tbtarsrc)

# appdata_and_icons module
appdata_and_icons_module = {}
appdata_and_icons_module["name"] = "appdata_and_icons"
appdata_and_icons_module["buildsystem"] = "simple"
# appdata_and_icons_module["build-options"] = app_data_and_icons_bopt
appdata_and_icons_module["build-commands"] = app_data_and_icons_bc
appdata_and_icons_module["sources"] = appdata_and_icons_src
mdles.append(appdata_and_icons_module)

# Define the basic structure
base = {}
base["app-id"] = "org.scarlett.ScarlettOS"
base["runtime"] = gnome_runtime
base["sdk"] = "org.gnome.Sdk"
base["command"] = "/usr/bin/bash"
base["tags"] = ["nightly"]
base["finish-args"] = fin_args
base["build-options"] = build_opts
base["cleanup"] = clnup
base["modules"] = mdles
base["desktop-file-name-prefix"] = "(Nightly) "
base["copy-icon"] = True
json_data = jsonlib.dumps(base, indent=4, default=str)

# Spit out the JSON
with open(output_file, 'w') as f:
    f.write(json_data)
