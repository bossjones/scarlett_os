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
