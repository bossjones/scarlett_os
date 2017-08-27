#!/bin/bash

# Entrypoint for utilizing as a scarlett-ci pool instead of a web server
# Based on configuration, can run multiple instances of a single scarlett-ci process

SUPERVISOR_CONF=/etc/supervisor/conf.d/scarlett-ci.conf
SERVICES_D=/etc/services.d

# Signal to init processes to avoid any webserver startup
export CONTAINER_ROLE='scarlett-ci'

# Begin startup sequence
/init.sh

STATUS=$?  # Captures exit code from script that was run

# TODO this exit code detection is also present in run.sh, needs to be combined
if [[ $STATUS == $SIGNAL_BUILD_STOP ]]
then
  echo "[scarlett-ci] container exit requested"
  exit # Exit cleanly
fi

if [[ $STATUS != 0 ]]
then
  echo "[scarlett-ci] failed to init"
  exit $STATUS
fi


CI_WORKER_QUANTITY=$1

# Rebuild scarlett-ci command as properly escaped parameters from shifted input args
# @see http://stackoverflow.com/questions/7535677/bash-passing-paths-with-spaces-as-parameters
shift
CI_WORKER_COMMAND="$@"

if [ -z "$CI_WORKER_COMMAND" ]
then
  echo "[scarlett-ci] command is required, exiting"
  exit 1
fi

echo "[scarlett-ci] command: '${CI_WORKER_COMMAND}' quantity: ${CI_WORKER_QUANTITY}"

for i in `seq 1 $CI_WORKER_QUANTITY`;
do
  SERVICE_FOLDER="${SERVICES_D}/scarlett-ci-${i}"
  mkdir $SERVICE_FOLDER
  echo "\
#!/usr/bin/execlineb -P
with-dynenv
cd /home/pi/dev/bossjones-github/scarlett_os
s6-envuidgid ${NOT_ROOT_USER}
s6-setuidgid ${NOT_ROOT_USER}
${CI_WORKER_COMMAND}" > "${SERVICE_FOLDER}/run"
done

# Start process manager
echo "[run] starting process manager"
exec /init

# # /worker.sh 1 /app/bin/cron migration
