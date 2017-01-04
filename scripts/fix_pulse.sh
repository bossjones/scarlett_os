#!/usr/bin/env bash

sudo apt-get update;sudo apt-get dist-upgrade;
sudo apt-get install pavucontrol linux-sound-base alsa-base alsa-utils lightdm ubuntu-desktop linux-image-`uname -r` libasound2;
sudo apt-get -y --reinstall install linux-sound-base alsa-base alsa-utils lightdm ubuntu-desktop linux-image-`uname -r` libasound2;
killall pulseaudio;
rm -r ~/.pulse*;
ubuntu-support-status;
sudo usermod -aG `cat /etc/group | grep -e '^pulse:' -e '^audio:' -e '^pulse-access:' -e '^pulse-rt:' -e '^video:' | awk -F: '{print $1}' | tr '\n' ',' | sed 's:,$::g'` `whoami`

# Support status summary of 'scarlett-ansible-manual1604-2':
#
# You have 198 packages (7.8%) supported until January 2017 (9m)
# You have 19 packages (0.7%) supported until December 2021 (5y)
# You have 1846 packages (72.8%) supported until April 2021 (5y)
# You have 84 packages (3.3%) supported until April 2019 (3y)
#
# You have 0 packages (0.0%) that can not/no-longer be downloaded
# You have 387 packages (15.3%) that are unsupported
#
# Run with --show-unsupported, --show-supported or --show-all to see more details
#  ⌁ pi@scarlett-ansible-manual1604-2  ⓔ scarlett_os  ⎇  master S:2 U:17 ?:77  ~/dev/bossjones-github/scarlett_os
