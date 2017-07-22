`source: https://gist.github.com/oleq/24e09112b07464acbda1`
`source: https://forums.resin.io/t/pulseaudio-in-a-docker-container-on-rpi3/499/2`

## What is this all about?

This tutorial will turn your [Raspberry PI](https://www.raspberrypi.org/) into a simple Bluetooth audio receiver, which plays music through connected speakers. It's like a regular car audio system, but it can be used anywhere and it's a good value.

```
   Audio source (i.e. smartphone)
                |
                v
 (((  Wireless Bluetooth Channel  )))
                |
                v
           Raspberry PI
                |
                v
       USB Audio Interface
                |
                v
             Speakers
```

The Bluetooth profile which does the magic is called [A2DP](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#Advanced_Audio_Distribution_Profile_.28A2DP.29).

## Obtaining peripherals

```
pi@raspberrypi:~ $ lsusb
...
Bus 001 Device 008: ID 041e:30d3 Creative Technology, Ltd Sound Blaster Play!
...
Bus 001 Device 012: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)
...
```

### Audio interface

The on–board audio produces low–quality, noisy output, so I decided to use something better. I chose external USB **Creative Sound Blaster Play!** interface. It costs ~$20.

### Bluetooth dongle

As for Bluetooth dongle, I used **Digitus Tiny USB-Adapter**, which is discovered as `Cambridge Silicon Radio, Ltd Bluetooth Dongle`.

**Note**: I used another dongle (different manufacturer) also discovered as `Cambridge Silicon Radio` but unable to stream audio. So beware, because different manufacturers use the same hardware in a different way. Or they pretend to use the same hardware for some (compatibility?) reasons. This way or another, if you get garbled audio or no audio at all but everything else is alright, don't worry, just try another dongle – it's cheap.

See [RPi USB Bluetooth adapters](http://elinux.org/RPi_USB_Bluetooth_adapters) for buying recommendations. Trial and error is another option, since most devices cost below $10.

### USB Hub

Raspberry PI offers limited power to USB devices (and limited number of ports). You'll need some active (powered) **USB Hub** to keep USB devices stable and working (USB Audio, USB Bluettoth and optional USB WiFi).
Google to learn more, it's a very common topic when using Raspberry PI.

## Initial setup

I'm using [Raspberry PI 1 Model B](https://www.raspberrypi.org/products/model-b/), running [Raspbian Jessie](https://www.raspberrypi.org/downloads/raspbian/). Make sure your system is up–to–date first:

```
sudo apt-get update
sudo apt-get upgrade
```

**Note:** It usually takes a while. Get some tee and sandwiches.

Then install required packages ([related article](http://www.instructables.com/id/Enhance-your-Raspberry-Pi-media-center-with-Blueto/?ALLSTEPS)):

```
sudo apt-get install alsa-utils bluez bluez-tools pulseaudio-module-bluetooth python-gobject python-gobject-2
```

Not quite sure it's really needed (?), but it doesn't hurt:

```
sudo usermod -a -G lp pi
```

## Setup PulseAudio

Use the following configuration to get most of PulseAudio ([related article](http://www.crazy-audio.com/2014/09/pulseaudio-on-the-raspbery-pi/)):

```
pi@raspberrypi:~ $ cat /etc/pulse/daemon.conf
...
resample-method=ffmpeg
enable-remixing = no
enable-lfe-remixing = no
default-sample-format = s32le
default-sample-rate = 192000
alternate-sample-rate = 176000
default-sample-channels = 2
exit-idle-time = -1
...
```

Reboot PI:

```
sudo reboot
```

**Note:** PA is pretty CPU–consuming. With the following configuration it uses ~30% of my PI's CPU.
So if you expect PI to do something else beside A2DP and avoid sound glitches, reasearch different `resample-method`.

## Configure USB Audio

The problem is that on–board audio ouput is prefered over USB audio interface:

```
pi@raspberrypi:~ $ cat /proc/asound/modules
 0 snd_bcm2835
 1 snd_usb_audio
```

Some configuration does the trick ([related article](http://raspberrypi.stackexchange.com/questions/40831/how-do-i-configure-my-sound-for-jasper-on-raspbian-jessie)):

```
pi@raspberrypi:~ $ cat /etc/modprobe.d/alsa-base.conf
# This sets the index value of the cards but doesn't reorder.
options snd_usb_audio index=0
options snd_bcm2835 index=1

# Does the reordering.
options snd slots=snd-usb-audio,snd-bcm2835
```

Reboot PI:

```
sudo reboot
```

From now on RPI uses USB Audio as default:

```
pi@raspberrypi:~ $ cat /proc/asound/modules
 0 snd_usb_audio
 1 snd_bcm2835
```


## Setup Bluetooth

Make sure Bluetooth audio is working and discovered as a car audio system

```
pi@raspberrypi:~ $ cat /etc/bluetooth/audio.conf
[General]
Class = 0x20041C
Enable = Source,Sink,Media,Socket
```

I'm not quite sure if the following is also needed. But I added it anyway:

```
pi@raspberrypi:~ $ cat /etc/bluetooth/main.conf
[General]
...
Name = raspberrypi
Class = 0x20041C
...
```

Reboot PI:

```
sudo reboot
```

Pair devices (phones, tablets, PCs) with PI using `bluetoothctl` utility:

```
pi@raspberrypi:~ $ bluetoothctl
```

See that your USB dongle is here:

```
[bluetooth]# list
Controller 00:1A:7D:DA:71:06 raspberrypi [default]
```

Prepare for pairing:

```
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# discoverable on
[bluetooth]# scan on
```

Then, for each device:

```
pair XX:XX:XX:XX:XX:XX
...
    Go through pairing process.
...
trust XX:XX:XX:XX:XX:XX
```

`CTRL(CMD)+D` to exit `bluetoothctl`.

## Setup auto connecting

Given that your device is already paired and connected to PI, run the following:

```
pi@raspberrypi:~ $ pactl list sources short
0   alsa_output.0.analog-stereo.monitor module-alsa-card.c  s16le 2ch 48000Hz   IDLE
1   alsa_input.0.analog-mono    module-alsa-card.c  s16le 1ch 48000Hz   IDLE
4   bluez_source.A8_88_08_11_AB_4B  module-bluez5-device.c  s16le 2ch 44100Hz   RUNNING
```

and

```
pi@raspberrypi:~ $ pactl list sinks short
0   alsa_output.0.analog-stereo module-alsa-card.c  s16le 2ch 48000Hz   RUNNING
```

The whole trick is to redirect the right **source** (i.e. smartphone)  the right **sink** (ALSA) each time a new Bluetooth device is connected. In the above case, it would be `bluez_source.A8_88_08_11_AB_4B` to `alsa_output.0.analog-stereo`.

The good news that it can be automated. Add udev rule which executes [`a2dp-autoconnect`](#file-a2dp-autoconnect) script each time a Bluetooth device is connected:

```
pi@raspberrypi:~ $ cat /etc/udev/rules.d/99-input.rules
KERNEL=="input[0-9]*", RUN+="/home/pi/a2dp-autoconnect"
```

The script I used is an extended version of http://blog.mrverrall.co.uk/2013/01/raspberry-pi-a2dp-bluetooth-audio.html. It's pretty straightforward: it redirects a new Bluetooth audio source to the right sink and sets output volume level.

I located it in `/home/pi/a2dp-autoconnect`, then made it executable:

```
pi@raspberrypi:~ $ chmod +x a2dp-autoconnect
```

**Note**: Observe connection log "live" to debug connection issues:

```
pi@raspberrypi:~ $ tail -f /var/log/a2dp-autoconnect
```

## Auto–login

Some people complained that the whole configuration does not work after reboot, unless `pi` user is logged in.

Auto–login can be enabled using `raspi–config` utility

```
pi@raspberrypi:~ $ sudo raspi-config
```

in "Boot Options" -> "Console Auto–login".

## Enjoy!

If your device is already paired, simply connect it to Raspberry PI and select Bluetooth audio output. Enjoy your tunes!

Tested with iPhone, MacbookPro and Windows laptop.


### filename: a2dp-autoconnect

```
#!/bin/bash
# The original script: http://blog.mrverrall.co.uk/2013/01/raspberry-pi-a2dp-bluetooth-audio.html.

# Find the right sink with `pactl list sources short`.
PA_SINK="alsa_output.0.analog-stereo"
BT_MAC=$(echo "$NAME" | sed 's/:/_/g' | sed 's/\"//g')
BT_USER=pi

function log {
	echo "[$(date)]: $*" >> /var/log/a2dp-autoconnect
}

function checkSource {
	# Get the current sources
	local _sources=$(sudo su - "$BT_USER" -c "pactl list sources short")

	# Check if any sources are currently running and that our new device is valid.
	if [[ "$_sources" =~ RUNIING ]]; then
		log "Source is already RUNNING. Available sources:"
		log "$_sources"
		return
	fi

	if [[ ! "$_sources" =~ "$1" ]] ; then
		log "Unrecognized source. Available sources:"
		log "\n$_sources"
		return
	fi

	log "Validated new source: $1."
	echo "$1"
}

function setVolume {
	log "Setting volume levels."

	# Set our volume to max
	sudo su - "$BT_USER" -c "pacmd set-sink-volume 0 65537"
	sudo su - "$BT_USER" -c "amixer set Master 100%"
}

function connect {
	log "Connecting $1."

	# Connect source to sink
	sudo su - "$BT_USER" -c 'pactl load-module module-loopback source="$1" sink="$PA_SINK" rate=44100 adjust_time=0'
}

log "Change for device $BT_MAC detected, running $ACTION."

if [ "$ACTION" = "add" ]
then
	incoming=bluez_source."$BT_MAC"
	if [ ! -z $(checkSource "$incoming") ] ; then
		connect "$incoming"
		setVolume
	fi
fi
```