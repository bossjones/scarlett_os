### Folders:

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
  - AKA components or features
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
  - eg. https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/__main__.py
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
  - example: https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/remote.py

core.py - Where we define what the Scarlett System Object is.
  - https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/core.py
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
    from homeassistant import bootstrap
```

What does the -> mean?

A: http://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions

```
It's a function annotation.

In more detail, Python 2.x has docstrings, which allow you to attach a metadata string to various types of object. This is amazingly handy, so Python 3 extends the feature by allowing you to attach metadata to functions describing their parameters and return values.

There's no preconceived use case, but the PEP suggests several. One very handy one is to allow you to annotate parameters with their expected types; it would then be easy to write a decorator that verifies the annotations or coerces the arguments to the right type. Another is to allow parameter-specific documentation instead of encoding it into the docstring.
```
