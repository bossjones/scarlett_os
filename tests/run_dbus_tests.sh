#!/bin/sh
set -e

# Create a temporary file or directory, safely, and print its name.
ADDRESS_FILE=$(mktemp /tmp/scarlettos.XXXXXXXXX)
PID_FILE=$(mktemp /tmp/scarlettos.XXXXXXXXX)

# --session: Use the standard configuration file for the per-login-session message bus.

# --print-address=0: Print the address of the message bus to standard output,
# or to the given file descriptor. This is used by programs that launch the message bus.

# --print-pid=1: Print the process ID of the message bus to standard output, or to the given file descriptor. This is used by programs that launch the message bus.

# --fork: -Force the message bus to fork and become a daemon, even if the configuration file does not specify that it should. In most contexts the configuration file already gets this right, though.

dbus-daemon \
     --session \
     --print-address=0 \
     --print-pid=1 \
     --fork 0>"$ADDRESS_FILE" 1>"$PID_FILE"

export DBUS_SESSION_BUS_ADDRESS=$(cat "$ADDRESS_FILE")
PID=$(cat "$PID_FILE")

# If any type of exit happens, send term signal to dbus
trap 'kill -TERM $PID' EXIT

rm "$ADDRESS_FILE" "$PID_FILE"

# 'if $1 is set to any value except the empty string, use it; otherwise, use python instead'.
# source: http://stackoverflow.com/questions/14152534/variable-expansion-in-curly-braces
PYTHON=${1:-python}

# pidof - find pid of running process

"$PYTHON" -m pydbus.tests.context
"$PYTHON" -m pydbus.tests.identifier
if [ "$2" != "dontpublish" ]
then
	"$PYTHON" -m pydbus.tests.publish
	"$PYTHON" -m pydbus.tests.publish_properties
	"$PYTHON" -m pydbus.tests.publish_multiface
fi
