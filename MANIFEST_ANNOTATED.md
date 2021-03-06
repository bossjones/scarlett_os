```

{
    "app-id": "org.scarlett.Listener",
    "runtime": "org.gnome.Platform",
    "runtime-version": "3.22",
    "sdk": "org.gnome.Sdk",
    "command": "python -c 'import gi'",
    "tags": ["nightly"],
    "desktop-file-name-prefix": "(Nightly) ",
    "finish-args": [
        /* X11 + XShm access */
        "--socket=x11", "--share=ipc",

        /* Wayland access */
        "--socket=wayland",

        /* Needs network, obviously */
        "--share=network",

        /* Our client name */
        "--own-name=org.scarlett.Listener",
        "--own-name=org.scarlett.Listener.*",

        /* Keyring */
        "--talk-name=org.freedesktop.secrets",

        /* Audio Access */
        "--socket=pulseaudio",

        /* Dbus Access */
        "--socket=session-bus",

        /* SOURCE: https://github.com/flathub/org.gnome.Builder/blob/master/org.gnome.Builder.json */
        "--filesystem=home",
        "--filesystem=host",
        "--system-talk-name=org.freedesktop.Avahi",
        "--talk-name=org.freedesktop.secrets",
        "--filesystem=xdg-run/keyring",
        "--env=SSL_CERT_DIR=/etc/ssl/certs",
        "--filesystem=/etc/ssl:ro",
        "--filesystem=/etc/pki:ro",
        "--filesystem=/etc/ca-certificates:ro",
        "--filesystem=~/.local/share/flatpak",
        "--filesystem=/var/lib/flatpak",

        /* dconf */
        "--filesystem=xdg-run/dconf",
        "--filesystem=~/.config/dconf:ro",
        "--talk-name=ca.desrt.dconf",
        "--env=DCONF_USER_CONFIG_DIR=.config/dconf",

        "--filesystem=host"
    ],
    "build-options" : {
        "cflags": "-fPIC -O0 -ggdb -fno-inline -fno-omit-frame-pointer",
        "cxxflags": "-O2 -g",
        "env": {
            "V": "1"
        }
    },
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
        "/lib/girepository-1.0",
        "/share/doc",
        "/share/gir-1.0",
        "/lib/python*",
        "/share/dbus-1/services/org.freedesktop*",
        "/share/info",
        "/share/man"
    ],
    "modules": [
        {
            "name": "scarlett_os",
            "buildsystem": "simple",
            "ensure-writable": [
                "easy-install.pth"
            ],
            "build-options": {
                "build-args": ["--share=network"],
                "cflags": "-O0 -g",
                "cxxflags": "-O0 -g",
                "env": {
                    "PYTHON": "python3",
                    "GST_PLUGIN_SYSTEM_PATH": "/app/lib/gstreamer-1.0/",
                    "FREI0R_PATH": "/app/lib/frei0r-1/",
                    "GSTREAMER": "1.0",
                    "ENABLE_PYTHON3": "yes",
                    "ENABLE_GTK": "yes",
                    "PYTHON_VERSION": "3.5",
                    "MAKEFLAGS": "-j4 V=1",
                    "CC": "gcc",
                    "V": "1"
                },
                "strip": false,
                "no-debuginfo": false
            },
            "build-commands": [
                "mkdir -p /app/lib/python3.5/site-packages",
                "CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -r requirements.txt",
                "CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -r requirements_dev.txt",
                "CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ python3.5 setup.py install --prefix=/app --root=/",
                "CFLAGS='-L/usr/lib -Lbuild/temp.linux-x86_64-3.4 -I/usr/include -I/usr/include/python3.5m/' CXX=/usr/bin/g++ CC=/usr/bin/gcc PYTHONUSERBASE=/app/ pip3.5 install --target=/app --root=/ -e .[test]"
            ],
            "sources": [
                {
                    "type": "git",
                    "url": "https://github.com/bossjones/scarlett_os.git",
                    "branch": "feature-config-schema"
                }
            ],
            "cleanup": [
                "/include",
                "/lib/pkgconfig",
                "/lib/python3.5/site-packages/gi/*.la"
            ]
        }
    ]
}

```
