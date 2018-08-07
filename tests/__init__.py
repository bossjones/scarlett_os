#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ScarlettOS unit tests
"""

# NOTE: A bunch of this was borrowed from Pitivi

import glob
import os
import sys
import unittest


def get_scarlett_os_dir():
    """
    Gets the scarlett_os root directory.

    Example:

    pi@5068ced95719:~/dev/bossjones-github/scarlett_os/tests$ python try.py
    /home/pi/dev/bossjones-github/scarlett_os
    pi@5068ced95719:~/dev/bossjones-github/scarlett_os/tests$

    """
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    scarlett_os_dir = os.path.join(tests_dir, os.path.pardir)
    return os.path.abspath(scarlett_os_dir)


PROJECT_ROOT = get_scarlett_os_dir()


def setup():
    """Sets paths and initializes modules, to be able to run the tests."""
    res = True

    # # Make available to configure.py the top level dir.
    # scarlett_os_dir = get_scarlett_os_dir()
    # sys.path.insert(0, scarlett_os_dir)
    #
    # NOTE: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # SUPER IMPORTANT
    # CONFIGURE RELATES TO A SCRIPT THAT GENERATES Pitivi MAKEFILES ( Since they compile stuff as well )
    # IT IS NOT THE BASIC CONFIGURATION FOR THE APPLICATION
    # IF YOU NEED THAT YOU SHOULD BE LOOKING AT settings.py
    # from scarlett_os import configure
    #
    # # Make available the compiled C code.
    # sys.path.append(configure.BUILDDIR)
    # subproject_paths = os.path.join(configure.BUILDDIR, "subprojects", "gst-transcoder")
    #
    # _prepend_env_paths(LD_LIBRARY_PATH=subproject_paths,
    #                    GST_PLUGIN_PATH=subproject_paths,
    #                    GI_TYPELIB_PATH=subproject_paths,
    #                    GST_PRESET_PATH=[os.path.join(scarlett_os_dir, "data", "videopresets"),
    #                                     os.path.join(scarlett_os_dir, "data", "audiopresets")],
    #                    GST_ENCODING_TARGET_PATH=[os.path.join(scarlett_os_dir, "data", "encoding-profiles")])
    # os.environ.setdefault('SCARLETT_OS_TOP_LEVEL_DIR', scarlett_os_dir)
    #
    # # Make sure the modules are initialized correctly.
    # from scarlett_os import check
    # check.initialize_modules()
    # res = check.check_requirements()
    #
    # from scarlett_os.utils import loggable as log
    # log.init('SCARLETT_OS_DEBUG')

    return res


# TODO: Comment this in after we figure out best way to get some of this working
# if not setup():
#     raise ImportError("Could not setup testsuite")

TEST_LM_DATA = """
Language model created by QuickLM on Sat Jan  2 12:51:32 EST 2016
Copyright (c) 1996-2010 Carnegie Mellon University and Alexander I. Rudnicky

The model is in standard ARPA format, designed by Doug Paul while he was at MITRE.

The code that was used to produce this language model is available in Open Source.
Please visit http://www.speech.cs.cmu.edu/tools/ for more information

The (fixed) discount mass is 0.5. The backoffs are computed using the ratio method.
This model based on a corpus of 70 sentences and 80 words

\data\
ngram 1=80
ngram 2=155
ngram 3=128

\1-grams:
-0.9301 </s> -0.3010
-0.9301 <s> -0.2393
-2.7752 ALL -0.2892
-2.7752 APPLE -0.2468
-2.7752 ARE -0.2915
-2.7752 BACKWARD -0.2468
-2.4742 BATHROOM -0.2334
-2.7752 BLUE -0.2468
-2.7752 BRIGHTER -0.2468
-2.7752 BUTTON -0.2468
-2.7752 CANCEL -0.2468
-1.9971 CHANGE -0.2915
-2.4742 CHANNEL -0.2944
-2.7752 CIRCLE -0.3003
-2.7752 CLOSE -0.2915
-2.7752 DARKER -0.2468
-2.1732 DOWN -0.2468
-2.7752 EIGHT -0.2468
-2.7752 ENTER -0.2468
-2.4742 FAMILY -0.2996
-2.7752 FIVE -0.2468
-2.7752 FORWARD -0.2468
-2.7752 FOUR -0.2468
-2.7752 FRIZZY -0.2468
-2.4742 GET -0.2988
-2.7752 GIVE -0.3003
-2.7752 GO -0.2468
-2.7752 GREEN -0.2468
-2.7752 HALLWAY -0.2468
-2.7752 HBO -0.2468
-2.7752 IDS -0.2468
-2.2981 IN -0.2974
-2.7752 INPUT -0.2468
-2.7752 IS -0.3003
-2.7752 IT -0.2468
-2.2981 LEFT -0.2468
-2.2981 LIGHT -0.2981
-1.5711 LIGHTS -0.2393
-2.7752 ME -0.2988
-2.7752 MENU -0.2468
-2.7752 MTV -0.2468
-2.7752 MUTE -0.2468
-2.7752 MY -0.2892
-2.2981 NAMES -0.2459
-2.7752 NEGATIVE -0.2468
-2.7752 NINE -0.2468
-2.7752 OF -0.3003
-2.7752 OFF -0.2915
-1.8722 ON -0.2747
-2.7752 ONE -0.2468
-2.7752 PAUSE -0.2468
-2.7752 PLAY -0.2468
-2.7752 POWER -0.2468
-2.7752 RECALL -0.2468
-2.7752 RED -0.2468
-2.2981 RIGHT -0.2468
-2.4742 ROOM -0.2334
-2.7752 SCARLETT -0.2468
-2.1732 SELECT -0.2922
-2.7752 SEVEN -0.2468
-2.7752 SEXY -0.2996
-2.7752 SHADES -0.2468
-2.7752 SIX -0.2468
-2.7752 STOP -0.2468
-1.6613 THE -0.2832
-2.7752 THREE -0.2468
-2.4742 TIME -0.2459
-2.4742 TO -0.2996
-2.7752 TOSHIBA -0.2468
-1.7339 TURN -0.2847
-2.2981 TV -0.2451
-2.7752 TWO -0.2468
-2.0763 UP -0.2468
-2.4742 VOLUME -0.2944
-2.7752 WEATHER -0.2468
-2.4742 WHAT -0.2988
-2.7752 WHATS -0.2915
-2.7752 WHITE -0.2468
-2.7752 WINDOW -0.2892
-2.7752 ZERO -0.2468

\2-grams:
-2.1461 <s> APPLE 0.0000
-2.1461 <s> BACKWARD 0.0000
-2.1461 <s> CANCEL 0.0000
-1.3680 <s> CHANGE 0.0000
-1.8451 <s> CHANNEL 0.0000
-2.1461 <s> CIRCLE 0.0000
-2.1461 <s> CLOSE 0.0000
-1.8451 <s> DOWN 0.0000
-2.1461 <s> EIGHT 0.0000
-2.1461 <s> FIVE 0.0000
-2.1461 <s> FORWARD 0.0000
-2.1461 <s> FOUR 0.0000
-2.1461 <s> FRIZZY 0.0000
-1.8451 <s> GET 0.0000
-2.1461 <s> GIVE 0.0000
-2.1461 <s> GO 0.0000
-2.1461 <s> INPUT 0.0000
-1.8451 <s> LEFT 0.0000
-2.1461 <s> MENU 0.0000
-2.1461 <s> MUTE 0.0000
-2.1461 <s> NEGATIVE 0.0000
-2.1461 <s> NINE 0.0000
-2.1461 <s> ONE 0.0000
-2.1461 <s> PAUSE 0.0000
-2.1461 <s> PLAY 0.0000
-2.1461 <s> POWER 0.0000
-2.1461 <s> RECALL 0.0000
-1.8451 <s> RIGHT 0.0000
-2.1461 <s> SCARLETT 0.0000
-1.5441 <s> SELECT 0.0000
-2.1461 <s> SEVEN 0.0000
-2.1461 <s> SEXY 0.0000
-2.1461 <s> SIX 0.0000
-2.1461 <s> STOP 0.0000
-2.1461 <s> THREE 0.0000
-2.1461 <s> TOSHIBA 0.0000
-1.1047 <s> TURN 0.0000
-2.1461 <s> TV -0.2218
-2.1461 <s> TWO 0.0000
-1.8451 <s> UP 0.0000
-1.8451 <s> VOLUME 0.0000
-1.8451 <s> WHAT 0.0000
-2.1461 <s> WHATS 0.0000
-2.1461 <s> ZERO 0.0000
-0.3010 ALL LIGHTS -0.1938
-0.3010 APPLE </s> -0.3010
-0.3010 ARE THE -0.2840
-0.3010 BACKWARD </s> -0.3010
-0.6021 BATHROOM </s> -0.3010
-0.6021 BATHROOM LIGHTS -0.1938
-0.3010 BLUE </s> -0.3010
-0.3010 BRIGHTER </s> -0.3010
-0.3010 BUTTON </s> -0.3010
-0.3010 CANCEL </s> -0.3010
-0.3010 CHANGE THE -0.0902
-0.6021 CHANNEL DOWN 0.0000
-0.6021 CHANNEL UP 0.0000
-0.3010 CIRCLE BUTTON 0.0000
-0.3010 CLOSE THE -0.2840
-0.3010 DARKER </s> -0.3010
-0.3010 DOWN </s> -0.3010
-0.3010 EIGHT </s> -0.3010
-0.3010 ENTER </s> -0.3010
-0.3010 FAMILY ROOM 0.0000
-0.3010 FIVE </s> -0.3010
-0.3010 FORWARD </s> -0.3010
-0.3010 FOUR </s> -0.3010
-0.3010 FRIZZY </s> -0.3010
-0.3010 GET LIGHT 0.0000
-0.3010 GIVE ME 0.0000
-0.3010 GO </s> -0.3010
-0.3010 GREEN </s> -0.3010
-0.3010 HALLWAY </s> -0.3010
-0.3010 HBO </s> -0.3010
-0.3010 IDS </s> -0.3010
-0.7782 IN BATHROOM -0.1761
-0.7782 IN FAMILY 0.0000
-0.7782 IN HALLWAY 0.0000
-0.3010 INPUT </s> -0.3010
-0.3010 IS IT 0.0000
-0.3010 IT </s> -0.3010
-0.3010 LEFT </s> -0.3010
-0.7782 LIGHT IDS 0.0000
-0.4771 LIGHT NAMES -0.1249
-0.6601 LIGHTS </s> -0.3010
-1.5051 LIGHTS BLUE 0.0000
-1.5051 LIGHTS BRIGHTER 0.0000
-1.5051 LIGHTS DARKER 0.0000
-1.5051 LIGHTS GREEN 0.0000
-1.0280 LIGHTS IN 0.0000
-1.5051 LIGHTS RED 0.0000
-1.5051 LIGHTS WHITE 0.0000
-0.3010 ME LIGHT -0.1249
-0.3010 MENU </s> -0.3010
-0.3010 MTV </s> -0.3010
-0.3010 MUTE </s> -0.3010
-0.3010 MY LIGHTS -0.1938
-0.4771 NAMES </s> -0.3010
-0.7782 NAMES OF 0.0000
-0.3010 NEGATIVE </s> -0.3010
-0.3010 NINE </s> -0.3010
-0.3010 OF MY 0.0000
-0.3010 OFF THE -0.1413
-1.2041 ON ALL 0.0000
-1.2041 ON BATHROOM -0.1761
-1.2041 ON FAMILY 0.0000
-0.7270 ON LIGHTS -0.2583
-1.2041 ON THE -0.1413
-1.2041 ON WINDOW 0.0000
-0.3010 ONE </s> -0.3010
-0.3010 PAUSE </s> -0.3010
-0.3010 PLAY </s> -0.3010
-0.3010 POWER </s> -0.3010
-0.3010 RECALL </s> -0.3010
-0.3010 RED </s> -0.3010
-0.3010 RIGHT </s> -0.3010
-0.6021 ROOM </s> -0.3010
-0.6021 ROOM LIGHTS -0.1938
-0.3010 SCARLETT </s> -0.3010
-0.9031 SELECT ENTER 0.0000
-0.9031 SELECT LEFT 0.0000
-0.9031 SELECT RIGHT 0.0000
-0.9031 SELECT UP 0.0000
-0.3010 SEVEN </s> -0.3010
-0.3010 SEXY TIME -0.1761
-0.3010 SHADES </s> -0.3010
-0.3010 SIX </s> -0.3010
-0.3010 STOP </s> -0.3010
-0.5119 THE LIGHTS -0.0746
-1.4150 THE NAMES -0.2218
-1.4150 THE SHADES 0.0000
-1.1139 THE TV -0.1249
-1.4150 THE WEATHER 0.0000
-0.3010 THREE </s> -0.3010
-0.6021 TIME </s> -0.3010
-0.6021 TIME IS 0.0000
-0.6021 TO HBO 0.0000
-0.6021 TO MTV 0.0000
-0.3010 TOSHIBA </s> -0.3010
-1.3424 TURN OFF 0.0000
-0.4393 TURN ON 0.0000
-1.0414 TURN THE -0.1413
-0.7782 TV </s> -0.3010
-0.4771 TV TO 0.0000
-0.3010 TWO </s> -0.3010
-0.3010 UP </s> -0.3010
-0.6021 VOLUME DOWN 0.0000
-0.6021 VOLUME UP 0.0000
-0.3010 WEATHER </s> -0.3010
-0.6021 WHAT ARE 0.0000
-0.6021 WHAT TIME -0.1761
-0.3010 WHATS THE -0.2840
-0.3010 WHITE </s> -0.3010
-0.3010 WINDOW LIGHTS -0.1938
-0.3010 ZERO </s> -0.3010

\3-grams:
-0.3010 <s> APPLE </s>
-0.3010 <s> BACKWARD </s>
-0.3010 <s> CANCEL </s>
-0.3010 <s> CHANGE THE
-0.6021 <s> CHANNEL DOWN
-0.6021 <s> CHANNEL UP
-0.3010 <s> CIRCLE BUTTON
-0.3010 <s> CLOSE THE
-0.3010 <s> DOWN </s>
-0.3010 <s> EIGHT </s>
-0.3010 <s> FIVE </s>
-0.3010 <s> FORWARD </s>
-0.3010 <s> FOUR </s>
-0.3010 <s> FRIZZY </s>
-0.3010 <s> GET LIGHT
-0.3010 <s> GIVE ME
-0.3010 <s> GO </s>
-0.3010 <s> INPUT </s>
-0.3010 <s> LEFT </s>
-0.3010 <s> MENU </s>
-0.3010 <s> MUTE </s>
-0.3010 <s> NEGATIVE </s>
-0.3010 <s> NINE </s>
-0.3010 <s> ONE </s>
-0.3010 <s> PAUSE </s>
-0.3010 <s> PLAY </s>
-0.3010 <s> POWER </s>
-0.3010 <s> RECALL </s>
-0.3010 <s> RIGHT </s>
-0.3010 <s> SCARLETT </s>
-0.9031 <s> SELECT ENTER
-0.9031 <s> SELECT LEFT
-0.9031 <s> SELECT RIGHT
-0.9031 <s> SELECT UP
-0.3010 <s> SEVEN </s>
-0.3010 <s> SEXY TIME
-0.3010 <s> SIX </s>
-0.3010 <s> STOP </s>
-0.3010 <s> THREE </s>
-0.3010 <s> TOSHIBA </s>
-1.3424 <s> TURN OFF
-0.4393 <s> TURN ON
-1.0414 <s> TURN THE
-0.3010 <s> TV </s>
-0.3010 <s> TWO </s>
-0.3010 <s> UP </s>
-0.6021 <s> VOLUME DOWN
-0.6021 <s> VOLUME UP
-0.6021 <s> WHAT ARE
-0.6021 <s> WHAT TIME
-0.3010 <s> WHATS THE
-0.3010 <s> ZERO </s>
-0.3010 ALL LIGHTS </s>
-0.3010 ARE THE NAMES
-0.3010 BATHROOM LIGHTS </s>
-0.4771 CHANGE THE LIGHTS
-0.7782 CHANGE THE TV
-0.3010 CHANNEL DOWN </s>
-0.3010 CHANNEL UP </s>
-0.3010 CIRCLE BUTTON </s>
-0.3010 CLOSE THE SHADES
-0.6021 FAMILY ROOM </s>
-0.6021 FAMILY ROOM LIGHTS
-0.6021 GET LIGHT IDS
-0.6021 GET LIGHT NAMES
-0.3010 GIVE ME LIGHT
-0.3010 IN BATHROOM </s>
-0.3010 IN FAMILY ROOM
-0.3010 IN HALLWAY </s>
-0.3010 IS IT </s>
-0.3010 LIGHT IDS </s>
-0.3010 LIGHT NAMES </s>
-0.3010 LIGHTS BLUE </s>
-0.3010 LIGHTS BRIGHTER </s>
-0.3010 LIGHTS DARKER </s>
-0.3010 LIGHTS GREEN </s>
-0.7782 LIGHTS IN BATHROOM
-0.7782 LIGHTS IN FAMILY
-0.7782 LIGHTS IN HALLWAY
-0.3010 LIGHTS RED </s>
-0.3010 LIGHTS WHITE </s>
-0.3010 ME LIGHT NAMES
-0.3010 MY LIGHTS </s>
-0.3010 NAMES OF MY
-0.3010 OF MY LIGHTS
-0.3010 OFF THE LIGHTS
-0.3010 ON ALL LIGHTS
-0.3010 ON BATHROOM LIGHTS
-0.3010 ON FAMILY ROOM
-0.3010 ON LIGHTS IN
-0.3010 ON THE LIGHTS
-0.3010 ON WINDOW LIGHTS
-0.3010 ROOM LIGHTS </s>
-0.3010 SELECT ENTER </s>
-0.3010 SELECT LEFT </s>
-0.3010 SELECT RIGHT </s>
-0.3010 SELECT UP </s>
-0.3010 SEXY TIME </s>
-0.9031 THE LIGHTS </s>
-1.2041 THE LIGHTS BLUE
-1.2041 THE LIGHTS BRIGHTER
-1.2041 THE LIGHTS DARKER
-1.2041 THE LIGHTS GREEN
-1.2041 THE LIGHTS RED
-1.2041 THE LIGHTS WHITE
-0.3010 THE NAMES OF
-0.3010 THE SHADES </s>
-0.3010 THE TV TO
-0.3010 THE WEATHER </s>
-0.3010 TIME IS IT
-0.3010 TO HBO </s>
-0.3010 TO MTV </s>
-0.3010 TURN OFF THE
-1.2041 TURN ON ALL
-1.2041 TURN ON BATHROOM
-1.2041 TURN ON FAMILY
-0.7270 TURN ON LIGHTS
-1.2041 TURN ON THE
-1.2041 TURN ON WINDOW
-0.3010 TURN THE LIGHTS
-0.6021 TV TO HBO
-0.6021 TV TO MTV
-0.3010 VOLUME DOWN </s>
-0.3010 VOLUME UP </s>
-0.3010 WHAT ARE THE
-0.3010 WHAT TIME IS
-0.3010 WHATS THE WEATHER
-0.3010 WINDOW LIGHTS </s>

\end\
"""


TEST_DIC_DATA = """
ALL	AO L
APPLE	AE P AH L
ARE	AA R
ARE(2)	ER
BACKWARD	B AE K W ER D
BATHROOM	B AE TH R UW M
BLUE	B L UW
BRIGHTER	B R AY T ER
BUTTON	B AH T AH N
CANCEL	K AE N S AH L
CHANGE	CH EY N JH
CHANNEL	CH AE N AH L
CIRCLE	S ER K AH L
CLOSE	K L OW S
CLOSE(2)	K L OW Z
DARKER	D AA R K ER
DOWN	D AW N
EIGHT	EY T
ENTER	EH N T ER
ENTER(2)	EH N ER
FAMILY	F AE M AH L IY
FAMILY(2)	F AE M L IY
FIVE	F AY V
FORWARD	F AO R W ER D
FOUR	F AO R
FRIZZY	F R IH Z IY
GET	G EH T
GET(2)	G IH T
GIVE	G IH V
GO	G OW
GREEN	G R IY N
HALLWAY	HH AO L W EY
HBO	EY CH B IY OW
IDS	AY D IY Z
IDS(2)	IH D Z
IN	IH N
INPUT	IH N P UH T
IS	IH Z
IT	IH T
LEFT	L EH F T
LIGHT	L AY T
LIGHTS	L AY T S
ME	M IY
MENU	M EH N Y UW
MTV	EH M T IY V IY
MUTE	M Y UW T
MY	M AY
NAMES	N EY M Z
NEGATIVE	N EH G AH T IH V
NINE	N AY N
OF	AH V
OFF	AO F
ON	AA N
ON(2)	AO N
ONE	W AH N
ONE(2)	HH W AH N
PAUSE	P AO Z
PLAY	P L EY
POWER	P AW ER
RECALL	R IY K AO L
RECALL(2)	R IH K AO L
RED	R EH D
RIGHT	R AY T
ROOM	R UW M
SCARLETT	S K AA R L IH T
SELECT	S AH L EH K T
SEVEN	S EH V AH N
SEXY	S EH K S IY
SHADES	SH EY D Z
SIX	S IH K S
STOP	S T AA P
THE	DH AH
THE(2)	DH IY
THREE	TH R IY
TIME	T AY M
TO	T UW
TO(2)	T IH
TO(3)	T AH
TOSHIBA	T OW SH IY B AH
TURN	T ER N
TV	T IY V IY
TV(2)	T EH L AH V IH ZH AH N
TWO	T UW
UP	AH P
VOLUME	V AA L Y UW M
WEATHER	W EH DH ER
WHAT	W AH T
WHAT(2)	HH W AH T
WHATS	W AH T S
WHATS(2)	HH W AH T S
WHITE	W AY T
WHITE(2)	HH W AY T
WINDOW	W IH N D OW
ZERO	Z IY R OW
"""


COMMON_MOCKED_CONFIG = """
# Omitted values in this section will be auto detected using freegeoip.io

# Location required to calculate the time the sun rises and sets.
# Coordinates are also used for location for weather related automations.
# Google Maps can be used to determine more precise GPS coordinates.
latitude: 40.7056308
longitude: -73.9780034

pocketsphinx:
    hmm: /home/pi/.virtualenvs/scarlett_os/share/pocketsphinx/model/en-us/en-us
    lm: /home/pi/dev/bossjones-github/scarlett_os/static/speech/lm/1473.lm
    dict: /home/pi/dev/bossjones-github/scarlett_os/static/speech/dict/1473.dic
    # Silence word transition probability
    silprob: 0.1
    # ********************************************************
    # FIXME: ????? THIS IS THE ORIG VALUE, do we need too set it back? 8/5/2018 # wip: 1e-4
    # Enable Graph Search | Boolean. Default: true
    # ********************************************************
    # Word insertion penalty
    wip: 0.0001
    device: plughw:CARD=Device,DEV=0
    # ********************************************************
    # FIXME: ????? THIS IS THE ORIG VALUE, do we need too set it back? 8/5/2018 # bestpath: 0
    # Enable Graph Search | Boolean. Default: true
    # ********************************************************
    bestpath: True
    # Enable Flat Lexicon Search | Default: true
    fwdflat: True
    # Evaluate acoustic model every N frames |  Integer. Range: 1 - 10 Default: 1
    dsratio: 1
    # Maximum number of HMMs searched per frame | Integer. Range: 1 - 100000 Default: 30000
    maxhmmpf: 3000


# Impacts weather/sunrise data
elevation: 665

# 'metric' for Metric System, 'imperial' for imperial system
unit_system: metric

# Pick yours from here:
# http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
time_zone: America/New_York

# Name of the location where ScarlettOS Assistant is running
name: ScarlettOS

owner: "Hair Ron Jones"

keywords_list:
- 'scarlett'
- 'SCARLETT'

features:
- time

graphviz_debug_dir: /home/pi/dev/bossjones-github/scarlett_os/_debug
"""
