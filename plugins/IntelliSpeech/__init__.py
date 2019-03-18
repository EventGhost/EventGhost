# -*- coding: utf-8 -*-
version = "0.7"

# Plugins/IntelliSpeech/__init__.py
#
# Copyright (C)  2014-2016 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.7 by Pako 2016-10-31 08:32 UTC+1
#       - bugfix
# 0.6 by Pako 2016-10-29 18:11 UTC+1
#       - adjustments forced by changing "API":
#       - Text To Speech fixed
#       - Speech To Text fixed
# 0.5 by Pako 2016-03-18 09:30 UTC+1
#       - adjustments forced by changing "API":
#       - method speakIt() fixed (thanks TVBig !) http://www.eventghost.net/forum/viewtopic.php?f=9&t=6315&p=39275#p39275
#       - method Detect() fixed
# 0.4 by Pako 2015-08-07 10:11 UTC+1
#       - adjustments forced by changing "API"
# 0.3 by Pako 2014-11-11 05:49 UTC+1
#       - bugfix
# 0.2 by Pako 2014-11-09 10:16 UTC+1
#       - added two actions "Speech to text" (from microphone or file)
#       - added options to select audio output and audio input
# 0.1 by Pako 2014-09-23 11:13 UTC+1
#     - added option to select a folder for storing temporary audio files
# 0.0 by Pako 2014-09-22 11:19 UTC+1
#     - initial version

eg.RegisterPlugin(
    name="IntelliSpeech",
    author="Pako",
    version=version,
    kind="other",
    guid="{D741593B-422E-417A-8FB7-58F4DCD97D25}",
    canMultiLoad=False,
    createMacrosOnAdd=True,
    description=ur'''<rst>
This plugin is designed for automated translation, speech and recognition of
any texts. 
 
| Translation, Speech and Recognition powered by **Google Translate**. 
| Plugin uses the libraries speech_recognition_, pyAudio_ and Requests_.
| For conversion audio and video files is used command-line utility FFmpeg_.

Busy indicator (animated gif image) is obtained from the page 
`http://www.mytreedb.com/`__.

A **good internet connection** is required for a proper functioning. 

Plugin version: %s

.. _pyAudio:  http://people.csail.mit.edu/hubert/pyaudio/
.. _speech_recognition:  https://github.com/Uberi/speech_recognition
.. _FFmpeg:   https://www.ffmpeg.org/
.. _Requests: http://www.python-requests.org/en/latest/
__ http://www.mytreedb.com/blog/a-33-high_quality_ajax_loader_images.html
''' % version,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=6315",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAD70lEQVRYw82XT2hcVRTG"
        "f/fNTKZNMqPxJVGTbISEbMYGNYMtUUwq1JWmhUBXRcZFp2bRlmK67KY7dVHBBOkiIY3F"
        "CtqCBaFiEERSmLRI2qLtRLDaFBuTBjPGtIl5uS56XubN5P0bjOCBgbnz5t7vnO+c893z"
        "FJVZC5AGWoGngWr5fRn4DfgJmARmwh6oQvxnO5AB+oBGYBWwXPZqIAJUAb8DnwEjwIN/"
        "48A7wJvAiguYVXKQIqr1pv1xYBR4v1IHWoFhB8Ultn8/j507R2uZA5OA4XHeMvCWpKjE"
        "3DZ0AxeEejdbP3SIBq0pibe/n3phxiuNF4CeIAZeAj6SvLmyYxhgWbxQkg+NvnqVpXSa"
        "mz4saHGkH/jWjYEmYMgPHNADAzRsikKhOjtJmCaxgHp7AHwoWJscOC3F5leY65kM9fZi"
        "dZV158Njx3zTYDuxIlglDrwBNAd1RUsL8fb2YmEODXFverrYZtksT0KpUx5ONAvmhgNv"
        "A2sBG/Xx4zQ6fxgdZWFsjHl7bZrE0mlqQ2jLmmCigGeAi8DDgE1WocDziQRRgIUF/jZN"
        "vk8miS0u8pxdjOfPc7+vj9shNGYb8LoBvBwCnJ4eEjY4wMgIc4BRKLCWy/Gn1milUPv2"
        "YQbUgW0PgVcMoC3EBn3kCI3O3j91ijmJUp05w7xSjyI2DNSBAzwRwgENtBpAXQi6dG8v"
        "pg2Sz7M8M7Mhz2pwkPtOTchmaQhZjHVRKNLqZQcPYjrXly+ztHs3SUc76qkp/urooEYp"
        "VFcXydpaIktLgcxGFfCem0Q6e39igvadO0kohbJzHeT0iRPcOXmS2QB2vzGA234HJZNE"
        "d+0iaYOGARdNaAyRhl8MGSC8JFQfPVpUvvILyHWD/Ke5mXgq5X6bisWASTuaK169f/cu"
        "HU1NxB26n/Pqmh07qJmaIrWh7aeZzWa545OGTlsJz7o9TaWotsG1Ro+P84ccFnX7XLvG"
        "8uJiUVEzGd80nHVK8Qfy3RmZPny4ePMphRoeZt7nugUwxsaY2+A4hurt5XGX/jcEs4Sa"
        "16QjVu3q15p02bWbk7nP09raqMrnedZeT0xQ6OrilsPxKmAAuESZBlwCXgT2AuvxOJE9"
        "e7hpyeRXKGAFRA/A9DQr3d38GIk8Cs6y0I5ADeBzG9xrJnwXeDWknldiEeBrid53KK0B"
        "ckHjdAWmZbgdAgY3SaHb0BvmdgwJHAXmZbT/IcxYvh34bgvo3wb8LKPXRd/LoGz9qfSt"
        "8oioCpgVFXuq7Pk9IC/K+hXwayWvZtXyKtXgAq4konHgY6mPLTMF1ANfSFTKwUwcuAF8"
        "CXyyRXXhmgJTQOocb7nXhcr/BPR/Zf8AgqMap2oQw88AAAAASUVORK5CYII="
    )
)

from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW, PIPE, Popen
import wave
from os import devnull
from os.path import join, abspath, split, isfile
from threading import Thread, Timer
from requests import get, post, exceptions
from re import sub as re_sub
from time import sleep
from ctypes import windll, c_buffer
from Queue import Queue
from sys import path as syspath

mod_pth = abspath(split(__file__)[0])
syspath.append(mod_pth + "\\lib")
# import pyaudio
from _pyaudio import pyaudio
import speech_recognition as sr
from base64 import b64decode, b64encode
from io import BytesIO
from cStringIO import StringIO
from math import floor
from random import random
import wx

CHUNK = 1024
ACV = wx.ALIGN_CENTER_VERTICAL

false = False
true = True

MIC1 = (
    "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"
    "gg=="
)
MIC2 = (
    "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"
    "IFSTGnPSngAAAABJRU5ErkJggg=="
)
MIC3 = (
    "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"
    "hBBCCBEO/w+C+oRgRY5J9AAAAABJRU5ErkJggg=="
)
MIC4 = (
    "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"
    "dXYNAAAAAElFTkSuQmCC"
)
MIC5 = (
    "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"
    "hYe7CUN/AAAAAElFTkSuQmCC"
)
MICS = (True, MIC1, MIC2, MIC3, MIC4, MIC5)
GEAR1 = (
    "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"
)
GEAR2 = (
    "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"
    "EAAAAABJRU5ErkJggg=="
)
GEAR3 = (
    "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"
    "gg=="
)
GEAR4 = (
    "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"
    "iU9zrbACrNsAAAAASUVORK5CYII="
)
GEAR5 = (
    "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"
)
GEAR6 = (
    "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"
    "FZD0vDAAAAAASUVORK5CYII="
)
GEAR7 = (
    "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"
    "f+BidDLf6FuFAAAAAElFTkSuQmCC"
)
GEAR8 = (
    "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAMAAABrrFhUAAAABGdBTUEAALGPC/xhBQAA"
    "AIFQTFRF/9Za///////3///v//fv//fm//fW//fe/+/O/+/F/++1/++9/+at/+a1/+al"
    "/+aU/+ac/96M/96U996c/96E996U996M/95799aE/9Zr99Z7/9Zj99Zr99Zz/85a/85S"
    "985j/85C/8wz98VS98VC/8Uh/70Z970x97Uh97UQ760AZBYUegAAAAF0Uk5TAEDm2GYA"
    "AAABYktHRACIBR1IAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3goSBgseSTbI"
    "UAAACshJREFUeNrtnWlX4zoMhtN4S2kpbQoXuFxK59DD0v//Ay8clm6xrcWJ1Un0dZjW"
    "fmLplWTHLYrBBstiythqZ9aons3fVMdm+jR9batTs7o/AJrm/0Ggx+u/X16gKp/1JBI6"
    "LwDX5wjQoyhQ+W0AMAAYAAwAzlPatTFGq74CUD/CZlUXAL4qCeukpE3KIVMZHoByl0Y4"
    "EeWTRidzLACHX6flrH5ERcMBoI9zRyVn9YMrGgYA3VA/KDGrH+oEDABGVBWtiUUtHYAS"
    "VUQqak1HB+BEldH+st60BEBWJ0UF5qHaASCrkWAC83CtADBk5B17QGw8RAA69IUZlMCG"
    "xmNbAODOCUBwCdAAqOD3OWEuEJwK7X+FgRtZQTA8IhIAVUkDUIRHFHACEoDIt+UoCyM+"
    "4JICiKy3PBsKkYdSJgSgBS4A+lMhACCvtpxK6H0seABlRZacbOVAIA7iZ2LlSQBoZZpE"
    "ALTECAiKTSoJAE0W3Oxx0CUBYGRGQHo2hASgREogxz2RAJzUCEiWQhwAJVQCGVKIm42V"
    "7AC0FYoCIFcC6SKFASBZAskqhQEgWgKpUogAIFsCocuUAUC4BBJrFTgA6RIIrVYVFcBZ"
    "OAC+XwEGYMRLIC0OQgHEYkspCADqWUEBuHOQQIq3AgFkj4Cow4+Y0QL/LHMfDHn4ETNc"
    "GACdZAFo46x1hJfyDg4/QqINImmHzSpFEaAd9SyZwy83eMgCAUghgYacNJx8O8QPwKIF"
    "AZBgK+j4DCeCQFNEi68hcOUOAcCWwIYznIrqAD9+UPLioEYA4G4FacNJHBRx3UG7Y4CJ"
    "Mftgmtc9CZxGUym6Y3EAvD6YsrziIfjtwVAAlMIoAFYfTDlm+Rhzv1AogDWwoucdGX0w"
    "bdgFdGQdhz8F9Ohir84yJDD2Xx0jAu4/qJI4AB35Iw35EH9WVtro0FWCBRDMjkGH2SKv"
    "zxMP4GnI0C03n4s9B9hxxvAFCpbkAAY2bpUKgO+jYAdabejhUA7hKuaDA2tANCsAHmkO"
    "XaKCP4atbJUKAGIFeEKBgXXx9NE1Ohr2CY7q/GAdqHCm2dv/uFWo8dKHXAEOSeDUDzQ6"
    "fsGlxHBWPwyArrB2kh1bbhu3hO8dYp8X4CFUeDvKjkv2PoaGjV4b9FBtmlQwMjLHbuNr"
    "yOg1YaCKgR8RCtCFNCyrLTnOj3gKJAIHoUAn2MbUwdHjnR+1Cg0JgfGNnriHYfwOwB4g"
    "vKFODAV7BOjXHGjP1QzEJYobB8nF9gvl70yP93b7bhQaU/RW/CBEXmb72bFS/B3s0riD"
    "rS3i2qR5oWMughaMuPrJX0dZbVba/FlXVSpWKBQxf+5ZSkIokDT/FMcInJQlYLpzfnS3"
    "tZPDGzZfPNYiwmDWhWjyA1B5lyEiAxEAoJVrxsDZcUsxoGwz700aCsrMMaDNM8QmZyro"
    "smoQPBS09hqLyuX8uGG0eIY3I3yEH7T4CHTe1Q97FCYb+k6Pj/sL5Xa/t6WiN+Fy1Fm+"
    "Nc/rM6bjbkigIMr1+pjrLAcKalDGd0dK2/lCdN02IXFO2Ykj2vzO7wkFXT0KJ8D5j9Pj"
    "z9dSunsUvxrsevTTREexx3y+0NXb6Q822GCDJc8wDWnX/euUpzr/MZuKZVnSkYRjLm3F"
    "tO7zcc0fs46UmGIOBSDKYtqYTZXAzFmt/4MxqyqJdRoJk47ZpfmwTrsSScds03yYPbMI"
    "sBtzlci6BJB0zAOAAcAAYAAwABgADAAGAAOAvgLofS3Q+2rwHPsBOs2Y9dARGnqCiT4t"
    "ww23acfc832BM90Z0pwxD2cLBhtssDM2XY3HY6uEjGb0dUyuuw1iN6u/bCIBwajrg5L6"
    "sv61+VjnX4wdH1vVs3rfZnl/ZiHDYelxfWTTfItglOG4vKlPbZIJQZYXJqYNAD5CQW7n"
    "78wJbN1sM5fZ+Xc26jACHoQCldf5uymNx3XAupPEcCXeYhxUddDm3bTmM746e1lHbNZ+"
    "a6bM+P6uqeN22W4oGGV9ff6yhtg448vLLUeBGmbztp5A7is0dA21qcnj/C37gKnhlrxQ"
    "Hgm4RgcDIHWhLOMipRplCbNjKVdpzXAEUhXKIzGXqVU11lIUyoKu0yvmaALsQlnWhYqu"
    "xhsrOy6lXalpCQTohfLIydspd3MKApokEq/V3fuEyYQfDux0cb2YWmBLIGGhzL1YWf/z"
    "uv205wlr+terL7vfBTM9rdsPBSX3au3p2/bHnskJiVusdrbYfbibURAgCuUR++7y5Xbf"
    "/iW5oJ6uDux271PGtFDQSt776/x7RfB0e2hvS0L77351ZLP9MU4oBCbtzf9gp1a/b49t"
    "MyE6/74dHmuatkQgwU9sPG4b7D+MH4xXTXZ9BIkQCgChkH/gqto22qtmzn+1qjBd8uak"
    "qAUHOPm5qU0zgO0zeP175r+6PxntJZZAVAr4P7Q03foMGgqvfQBWpw/QIP2gSuwBDcv6"
    "zQvgjbkAVquHhpzCzpNKIfuI/N3Wb3v43dXTy86ervY+6sIPYHWF3jBDAhiR8t59F3oP"
    "ALj5/bPFy7Etdv8WALCyzTlTjhXQHE7Wgflv734G/Ofl1P7oaAg4lUJ0KEgWAzyCOgnN"
    "f7v+/qum+X8QgABY+R5hBQsFOo0KeOubzRawAhYvzfbtBVdBAPfeKUyS5AEl1fkbiiCP"
    "DroXn7lgGuSVQkQoACRjnB9e1m9hAF8TvPUCuP36mIcwgUB5HSuUQfUgo+l/t4WEgCcv"
    "gKfvVCoMYBHMokOhYM6vBl1o59eF5//+/ehe/Pb9QfdhAsG2Y6hQBvYrLSLvPbDnLSQE"
    "AgBEosBtpJnpCwUz7l5AJIKEJXCXCMcBRJRwFXNlT3YMbgs62o7fK0QCYABsGMBDNJg3"
    "ZceX8JYo1vkhErgpEAAiucAqvphPC+U5oiNjkM7v6YN5CiEIAIYU+rJj1I6Nw+93P4Ik"
    "EAwgIoXXIEGf0w8OOezBv5gEFkgALCk8DQX4ffLfnSHgeyAbmATCAVRhAPfQMwWT6XRC"
    "27Au9eftzcAjb1AJhAOISeFFIcoiRcCUAEBzpbBLu4FKIAJAMQsTuBI0/5gEOhKAmBRa"
    "OQDW4fk/FjQAFwmksBOr4BKIAhCTwkoKgIgE3pABREqCeyFxcIqQQByAcIc81B3rNAJG"
    "JHDCABCTQicBQKQPdroligAQKwkkSKFDSSAWwBlI4RpeBFAAjKVL4QQngWgA3O5Ybglc"
    "sgFY2SXBElMEkADEumN5pTBWBEwSAND87lg2CVwXCQCwNoralkDYVhATQJruWCv2jJZA"
    "EoCKtVGUTwJ9Z6LQAMR2x14RfTAWAKFSeEOQQBoA/kZRDgmsEgIoJErhI0UCqQCm8koC"
    "jS8CGABiUujERYC7xACsOCFYkySQDCAihRkqgg2+CGAB0NJaQxuSBNIBhDeKMqyAZ1wf"
    "jA8gKIUXsoLgY9EGgNBGUYZc0JEkkAOguJXVGlyDt4JSAbCyKmJvP/y1aAmAd6Mo0/bA"
    "kiCBPABa2PbI8p30dhwdQHNJkLEt6p6xEsgE0FASLPL2xSeviCIgAYDj7tht/r2xIz9Y"
    "F60CONwqe8i+L3TSGADMnwegsLeZG0FNoWCDekmeB+DDDRafSfHtTNI5Obe8u7tbArsS"
    "XABnbwOAAcAAYADQawDRFyf/dou+Ovu3W+zl6b/fIq/P98DCFyj0lUCf5h++RKUnkXB+"
    "cI3O3BWDDZbD/gdwSXx0uHlWjgAAAABJRU5ErkJggg=="
)
GEAR9 = (
    "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"
)
GEAR10 = (
    "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAMAAABrrFhUAAAABGdBTUEAALGPC/xhBQAA"
    "AIFQTFRF///////3///v//fv//fm//fW//fe/+/O/+/F/++1/++9/+at/+a1/+al/+aU"
    "/+ac/96M/96U996c/96E996U996M/95799aE/9Zr99Z7/9Zj99Zr/9Za99Zz/85a/85S"
    "985j/85C/8wz98VS98VC/8Uh/70Z970x97Uh97UQ760A14t0ugAAAAF0Uk5TAEDm2GYA"
    "AAABYktHRACIBR1IAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3goSBgskjzoR"
    "4gAACnhJREFUeNrtXWtz2joQxVpJhjBwyaSlNNML00xxZ/L/f+Btb5pgjC3tQ5aW2udz"
    "gqXj3T27q4cXixkzisBYV1/grJnY/G3dhZ3S9MHVt3AwHQL65v+LgQnb/7S8wNRDmEgk"
    "9IME+ClHgAlFgXoYMwEzATMBMwH3Ke1grQUzVQLMu7A5k4OAt0rCeS1pk/HEVEZGQHVJ"
    "I7yK8gnIyZyIgOvHgR7rJ1Q0EgKgmzsaPdaPrmgEBEBP/WDUWD/WCQQEWFVVNDCLWj4B"
    "RlURabg1HZ8Ar6qMHi7r7UgE6OqkmMA8zDgE6Gok2MA8/CgEWDblmT0gNh4mARB6YAEl"
    "cKHxuBEI8PdEQNAEeASY4PO8MhcIToX3X2HCra4gGB4RiwBTayNgER5RwAlYBESeVqIs"
    "jPiAT0pAxN7KLChEXkqVkABQaAD8t8IggG1tJZVw8LXQCahqtuQUKwcCcZA+E6dPAlCW"
    "aRMRABojICo2mSQEAFtwi8dBn4QAqzMC8rMhIgFGpQRK3JNIgNcaAdlSSCPAKJVAgRTS"
    "ZuM0OwDPQkkE6JVAvkhRCNAsgWyVohCgWgK5UkggQLcEYs1UQIByCWTWKngCtEsgtlo1"
    "XALuwgHo/Qo0AVa9BPLiIJaAWGypFBFAeldYAvw9SCDHW5EEFI+ApM2PlNEi/6xwH4y4"
    "+ZEyXBwBkMQAwHrnPONQ3tXmR0y0ISTtuFmlKALAc/eSebq54UMWioAUEmjZScPN0zF+"
    "gBYtDAEJloK6ezgJDPRF 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"
    "YII="
)
GEAR11 = (
    "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"
)
GEAR12 = (
    "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"
)
GEARS = (
    False, GEAR1, GEAR2, GEAR3, GEAR4, GEAR5,
    GEAR6, GEAR7, GEAR8, GEAR9, GEAR10, GEAR11, GEAR12
)

LANGS = {
    'Detect language': 'auto',
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese (Simplified)': 'zh',
    'Chinese (Traditional)': 'zt',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hebrew': 'iw',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kannada': 'kn',
    'Korean': 'ko',
    'Lao': 'lo',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
}

VOICES = [
    'English',
    'Chinese (Simplified)',
    # 'Chinese (Traditional)',
    'French',
    'German',
    'Italian',
    'Japanese',
    'Korean',
    'Portuguese',
    'Russian',
    'Spanish',
    'Arabic',
    'Czech',
    'Danish',
    'Dutch',
    'Finnish',
    'Greek',
    'Haitian Creole',
    'Hindi',
    'Hungarian',
    'Latin',
    'Norwegian',
    'Polish',
    'Slovak',
    'Swedish',
    'Thai',
    'Turkish'
]
STTVOICES = {
    "Afrikaans": "af",
    "Basque": "eu",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Arabic (Egypt)": "ar-EG",
    "Arabic (Jordan)": "ar-JO",
    "Arabic (Kuwait)": "ar-KW",
    "Arabic (Lebanon)": "ar-LB",
    "Arabic (Qatar)": "ar-QA",
    "Arabic (UAE)": "ar-AE",
    "Arabic (Morocco)": "ar-MA",
    "Arabic (Iraq)": "ar-IQ",
    "Arabic (Algeria)": "ar-DZ",
    "Arabic (Bahrain)": "ar-BH",
    "Arabic (Lybia)": "ar-LY",
    "Arabic (Oman)": "ar-OM",
    "Arabic (Saudi Arabia)": "ar-SA",
    "Arabic (Tunisia)": "ar-TN",
    "Arabic (Yemen)": "ar-YE",
    "Czech": "cs",
    "Dutch": "nl-NL",
    "English (Australia)": "en-AU",
    "English (Canada)": "en-CA",
    "English (India)": "en-IN",
    "English (New Zealand)": "en-NZ",
    "English (South Africa)": "en-ZA",
    "English (UK)": "en-GB",
    "English (US)": "en-US",
    "Finnish": "fi",
    "French": "fr-FR",
    "Galician": "gl",
    "German": "de-DE",
    "Hebrew": "he",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Italian": "it-IT",
    "Indonesian": "id",
    "Japanese": "ja",
    "Korean": "ko",
    "Latin": "la",
    "Mandarin Chinese": "zh-CN",
    "Traditional Taiwan": "zh-TW",
    "Simplified China": "zh-CN",
    "Simplified Hong Kong": "zh-HK",
    "Yue Chinese (Traditional Hong Kong)": "zh-yue",
    "Malaysian": "ms-MY",
    "Norwegian": "no-NO",
    "Polish": "pl",
    "Pig Latin": "xx-piglatin",
    "Portuguese": "pt-PT",
    "Portuguese (Brasil)": "pt-BR",
    "Romanian": "ro-RO",
    "Russian": "ru",
    "Serbian": "sr-SP",
    "Slovak": "sk",
    "Spanish (Argentina)": "es-AR",
    "Spanish (Bolivia)": "es-BO",
    "Spanish (Chile)": "es-CL",
    "Spanish (Colombia)": "es-CO",
    "Spanish (Costa Rica)": "es-CR",
    "Spanish (Dominican Republic)": "es-DO",
    "Spanish (Ecuador)": "es-EC",
    "Spanish (El Salvador)": "es-SV",
    "Spanish (Guatemala)": "es-GT",
    "Spanish (Honduras)": "es-HN",
    "Spanish (Mexico)": "es-MX",
    "Spanish (Nicaragua)": "es-NI",
    "Spanish (Panama)": "es-PA",
    "Spanish (Paraguay)": "es-PY",
    "Spanish (Peru)": "es-PE",
    "Spanish (Puerto Rico)": "es-PR",
    "Spanish (Spain)": "es-ES",
    "Spanish (US)": "es-US",
    "Spanish (Uruguay)": "es-UY",
    "Spanish (Venezuela)": "es-VE",
    "Swedish": "sv-SE",
    "Turkish": "tr",
    "Zulu": "zu"
}

STT_LANGS = {
    u'Euskara': 'eu-ES',
    u'Hrvatski': 'hr_HR',
    u'Fran\xe7ais': 'fr-FR',
    u'Galego': 'gl-ES',
    u'Lingua lat\u012bna': 'la',
    u'Espa\xf1ol': {
        u'Honduras': 'es-HN',
        u'Chile': 'es-CL',
        u'Rep\xfablica Dominicana': 'es-DO',
        u'Uruguay': 'es-UY',
        u'El Salvador': 'es-SV',
        u'Venezuela': 'es-VE',
        u'Panam\xe1': 'es-PA',
        u'Costa Rica': 'es-CR',
        u'Guatemala': 'es-GT',
        u'M\xe9xico': 'es-MX',
        u'Estados Unidos': 'es-US',
        u'Colombia': 'es-CO',
        u'Puerto Rico': 'es-PR',
        u'Paraguay': 'es-PY',
        u'Per\xfa': 'es-PE',
        u'Argentina': 'es-AR',
        u'Bolivia': 'es-BO',
        u'Nicaragua': 'es-NI',
        u'Ecuador': 'es-EC',
        u'Espa\xf1a': 'es-ES'
    },
    u'Magyar': 'hu-HU',
    u'Sloven\u010dina': 'sk-SK',
    u'Bahasa Melayu': 'ms-MY',
    u'\u65e5\u672c\u8a9e': 'ja-JP',
    u'P\u0443\u0441\u0441\u043a\u0438\u0439': 'ru-RU',
    u'\ud55c\uad6d\uc5b4': 'ko-KR',
    u'IsiZulu': 'zu-ZA',
    u'\xcdslenska': 'is-IS',
    u'Bahasa Indonesia': 'id-ID',
    u'Nederlands': 'nl-NL',
    u'Afrikaans': 'af-ZA',
    u'\u4e2d\u6587': {
        u'\u4e2d\u6587 (\u53f0\u7063)': 'cmn-Hant-TW',
        u'\u7cb5\u8a9e (\u9999\u6e2f)': 'yue-Hant-HK',
        u'\u666e\u901a\u8bdd (\u9999\u6e2f)': 'cmn-Hans-HK',
        u'\u666e\u901a\u8bdd (\u4e2d\u56fd\u5927\u9646)': 'cmn-Hans-CN'
    },
    u'Suomi': 'fi-FI',
    u'\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438': 'bg-BG',
    u'Polski': 'pl-PL',
    u'Catal\xe0': 'ca-ES',
    u'T\xfcrk\xe7e': 'tr-TR',
    u'English': {
        u'Canada': 'en-CA',
        u'United States': 'en-US',
        u'Australia': 'en-AU',
        u'South Africa': 'en-ZA',
        u'India': 'en-IN',
        u'United Kingdom': 'en-GB',
        u'New Zealand': 'en-NZ'
    },
    u'Rom\xe2n\u0103': 'ro-RO',
    u'Deutsch': 'de-DE',
    u'\u0421\u0440\u043f\u0441\u043a\u0438': 'sr-RS',
    u'Svenska': 'sv-SE',
    u'Italiano': {
        u'Italia': 'it-IT',
        u'Svizzera': 'it-CH'
    },
    u'Norsk bokm\xe5l': 'nb-NO',
    u'Portugu\xeas': {
        u'Brasil': 'pt-BR',
        u'Portugal': 'pt-PT'
    },
    u'\u010ce\u0161tina': 'cs-CZ'
}


# ===============================================================================

class Text:
    label1 = "Default source language:"
    label2 = "Default target language:"
    spkEnd = "SpeakingFinished"
    noVoice = 'IntelliSpeech: Voice "%s" is not yet available'
    detFail = "IntelliSpeech: Language detection failed"
    trnslFail = "IntelliSpeech: Translation failed"
    connTimeout = "IntelliSpeech: Connection timeout"
    connError = "IntelliSpeech: Connection error"
    httpError = "IntelliSpeech: HTTP error"
    tempFolder = "Folder for storing temporary audio files"
    folders = ("System temporary folder", "Other folder (such as RAM disk)")
    mp3Fldr = "Select the folder for storing temporary audio files ..."
    mp3Tool = (
        "Here you can select the folder for storing temporary audio files.\n"
        "If the field is left blank, it will to use the system temporary folder."
    )
    unknLng = (
        'IntelliSpeech: An unexpected result of language detection occured.\n'
        'The language "%s" is unknown.'
    )
    defDev = "Default output device"
    defMic = "Default input device"
    sttFailed = "Speech to text conversion failed"
    decFailed = "Decoding failed. ffmpeg returned error code: %s"
    tryDefDev = "I'm trying to use the default output device ..."


# ===============================================================================

def Get_GoogleTTS_TK(a):
    def RL(a, b):
        for c in range(0, len(b) - 2, 3):
            d = b[c + 2]
            d = ord(d) - 87 if d >= "a" else int(d)
            d = a >> d if b[c + 1] == "+" else a << d
            a = (a + d) & 4294967295 if b[c] == "+" else a ^ d
        return a

    b = int(floor(random() * 1000000))
    c = "&tk="
    d = []
    for f in range(len(a)):
        g = ord(a[f])
        if g <= 128:
            d += [g]
        else:
            if g <= 2048:
                d += [g >> 6 | 192]
            elif g & 64512 == 55296 and f + 1 < len(a) and ord(a[f + 1]) & 64512 == 56320:
                g = 65536 + ((g & 1023) << 10) + ord(a[f + 1]) & 1023
                d += [g >> 18 | 240]
                d += [g >> 12 & 63 | 128]
                f += 1
            else:
                d += [g >> 12 | 224]
                d += [g >> 6 & 63 | 128]
            d += [g & 63 | 128]
    a = b or 0
    for e in d:
        a += e
        a = RL(a, "+-a^+6")
    a = RL(a, "+-3^+b+-f")
    if a <= 0:
        a = (a & 2147483647) + 2147483648
    a = int(a % 1E6)
    return str(a) + "." + str(a ^ b)


# ===============================================================================

def smartWrap(txt, width):
    txt = txt.replace("\n", " ")
    txt = txt.replace(". ", ".")
    txt = re_sub(' +', ' ', txt)
    tmp = txt.split(".")
    tmp2 = []
    tmp3 = ""
    for itm in tmp:
        if len(tmp3) + len(itm) <= width - 1:
            tmp3 += "%s." % itm
        else:
            tmp2.append(tmp3)
            tmp3 = "%s." % itm
    tmp2.append(tmp3[:-1])
    return tmp2


def smartWrap2(txt, width):
    tmp = txt.split(" ")
    tmp2 = []
    tmp3 = ""
    for itm in tmp:
        if len(tmp3) + len(itm) <= width - 1:
            tmp3 += "%s " % itm
        else:
            tmp2.append(tmp3)
            tmp3 = "%s " % itm
    tmp2.append(tmp3[:-1])
    return tmp2


# ===============================================================================

def removeSpans(txt):
    result = ""
    ix = 0
    while ix > -1:
        ix = txt.find("</span>", ix + 1)
        if ix > -1:
            iy = txt.rfind(">", 0, ix - 1)
            result += txt[iy + 1:ix]
    return result


# ===============================================================================

def BigEnd(n):
    s = '%x' % n
    if len(s) & 1:
        s = '0' + s
    tmp = s.decode('hex')
    tmp = "".join([tmp[i:i + 1] for i in range(len(tmp))][::-1])
    while len(tmp) < 4:
        tmp += "\x00"
    return tmp


# ===============================================================================

class Animation(wx.Frame):
    def __init__(self, worker, pics, onTop, delay, mirror, color):
        worker.SetAnimation(self)
        style = wx.SIMPLE_BORDER | wx.FRAME_SHAPED | wx.FRAME_NO_TASKBAR
        if onTop:
            style |= wx.STAY_ON_TOP
        wx.Frame.__init__(self, None, -1, "Animation", style=style)
        self.SetBackgroundColour(wx.Colour(*color))
        self.worker = worker
        self.pics = pics
        self.delay = delay
        self.hasShape = False
        self.delta = (0, 0)
        self.cnt = 0
        self.dir = 1
        self.mirror = mirror
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_UP, self.Exit)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.bmp = self.CreateBitmap(pics[1])
        w, h = self.bmp.GetWidth(), self.bmp.GetHeight()
        self.SetClientSize((w, h))
        self.run = True
        t = Thread(target=self.Animate)
        t.start()
        self.Centre()
        self.Show(True)

    def set(self, pics, delay):
        self.pics = pics
        self.delay = delay
        self.bmp = self.CreateBitmap(self.pics[1])
        self.cnt = 1
        self.dir = 1
        self.Refresh(False)  # call OnPaint !!!

    def Reverse(self):
        self.mirror = not self.mirror
        self.cnt = 1 if self.cnt == 1 else (len(self.pics) + 1 - self.cnt)

    def CreateBitmap(self, png):
        stream = StringIO(b64decode(png))
        bmp = wx.Image(stream)
        bmp = bmp.Mirror(True) if self.mirror else bmp
        bmp.ConvertAlphaToMask()
        return bmp.ConvertToBitmap()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc = wx.GCDC(dc)
        dc.DrawBitmap(self.bmp, 0, 0, True)
        evt.Skip()

    def Animate(self):
        while self.run:
            self.cnt += self.dir
            if self.pics[0]:
                if self.cnt == len(self.pics):
                    self.dir = -1
                    self.cnt = len(self.pics) - 2
                elif self.cnt == 0:
                    self.dir = 1
                    self.cnt = 2
            else:
                if self.cnt == len(self.pics):
                    self.cnt = 1
            self.bmp = self.CreateBitmap(self.pics[self.cnt])
            r = wx.Region(self.bmp)
            self.hasShape = self.SetShape(r)
            self.Refresh(False)  # call OnPaint
            sleep(self.delay)

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)

    def Exit(self, evt=None):
        self.run = False
        self.worker.gif = None
        self.Destroy()


# ===============================================================================

class DeviceTest(object):

    def __init__(self, pyAud, ix):
        self.pyAud = pyAud
        self.ix = ix

    def device_ok(self):
        try:
            stream = self.pyAud.open(
                format=8,
                channels=1,
                rate=22050,
                output=True,
                output_device_index=self.ix
            )
            stream.close()
        except:
            return False
        return True


# ===============================================================================

class InputDeviceTest(object):

    def __init__(self, pyAud, ix):
        self.pyAud = pyAud
        self.ix = ix

    def device_ok(self):
        try:
            stream = self.pyAud.open(
                format=8,
                channels=1,
                rate=22050,
                input=True,
                input_device_index=self.ix
            )
            stream.close()
        except:
            return False
        return True


# ===============================================================================

class TTS_Worker(Thread):
    track = None

    def __init__(self, plugin):
        Thread.__init__(self)
        self.plugin = plugin
        self.queue = self.plugin.queue
        self.runFlag = True
        self.setDaemon(True)
        self.start()

    def run(self):
        while self.runFlag:
            item = self.queue.get()
            if item != "STOP":
                self.speakIt(*item)

    def play(self, ix):
        def callback(in_data, frame_count, time_info, status):
            data = self.track.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # open stream using callback
        p = self.plugin.pyAudio
        trck = self.track
        stream = None
        try:
            stream = p.open(
                format=p.get_format_from_width(trck.getsampwidth()),
                channels=trck.getnchannels(),
                rate=trck.getframerate(),
                output=True,
                stream_callback=callback,
                output_device_index=ix
            )
        except IOError as e:
            eg.PrintError(
                u"IntelliSpeech/PyAudio error: %s [%s]\n%s" % (
                    e.args[0],
                    e.args[1],
                    self.plugin.text.tryDefDev
                )
            )

        if not stream:
            try:
                stream = p.open(
                    format=p.get_format_from_width(trck.getsampwidth()),
                    channels=trck.getnchannels(),
                    rate=trck.getframerate(),
                    output=True,
                    stream_callback=callback
                )
            except IOError as e:
                eg.PrintError(
                    u"IntelliSpeech/PyAudio error: %s [%s]" % (
                        e.args[0],
                        e.args[1]
                    )
                )

        if not stream:
            return

        # start the stream
        stream.start_stream()

        # wait for stream to finish
        while stream.is_active() and not self.plugin.stopTTS:
            sleep(0.1)

        # stop stream
        stream.stop_stream()
        stream.close()
        trck.close()

    def speakIt(self, txt, src, vol, ix):
        self.plugin.stopTTS = False
        txtList = []
        lst = smartWrap(txt, 100)
        for item in lst:
            if len(item) > 100:
                lst2 = smartWrap2(item, 100)
                for item2 in lst2:
                    txtList.append(item2)
            else:
                txtList.append(item)
        if txtList:
            res = ""
            for idx, part in enumerate(txtList):
                if self.plugin.stopTTS:
                    return
                body = {
                    'ie': 'UTF-8',
                    'client': 'tw-ob',
                    'tl': src,
                    'q': part,
                    'total': len(txtList),
                    'idx': idx,
                    'textlen': len(part),
                    'tk': Get_GoogleTTS_TK(part)
                }
                try:
                    resp = get(u"http://translate.google.com/translate_tts", params=body)
                    if resp.ok and resp.headers['content-type'] == 'audio/mpeg' and \
                        int(resp.headers['content-length']) == len(resp.content):
                        res += resp.content
                except Exception as e:
                    raise
            if res:
                retCode, data = self.plugin.popen(res, vol)
                if retCode:
                    eg.PrintError(self.plugin.text.decFailed % str(retCode))
                    return
                self.track = wave.open(StringIO(data), 'rb')
                self.track.rewind()
                self.play(ix)
                self.plugin.TriggerEvent(self.plugin.text.spkEnd)

    def stop(self):
        self.runFlag = False
        self.queue.put("STOP")


# ===============================================================================

class STT_Worker(Thread):
    animat = None

    def __init__(self, plugin, lng, intThre, silDur, suffOk, suffKo, mic, mode):
        Thread.__init__(self)
        self.plugin = plugin
        self.lng = lng
        self.intThre = intThre
        self.silDur = silDur
        self.suffOk = suffOk
        self.suffKo = suffKo
        self.mode = mode

        if silDur is not None:
            defMic = self.plugin.InitInputDevices()
            if not defMic:
                return
            mic = mic if mic != self.plugin.text.defMic else defMic
            mic = mic if mic in list(
                self.plugin.inputDevices.iterkeys()
            ) else defMic
            self.mic = self.plugin.inputDevices[mic][0]
        self.start()

    def run(self):
        try:
            r = sr.Recognizer()
            audio = None
            if self.silDur is not None:  # from microphone
                r.energy_threshold = self.intThre
                r.pause_threshold = self.silDur
                with sr.Microphone(device_index=self.mic) as source:
                    audio = r.listen(source)
                if self.animat:
                    self.animat.set(GEARS, 0.15)
            else:  # from file
                retCode, data = self.plugin.popen(self.intThre)
                if retCode:
                    if self.suffKo:
                        wx.CallAfter(
                            self.plugin.TriggerEvent,
                            "SpeechToText.%s" % self.suffKo
                        )
                    eg.PrintError(self.plugin.text.decFailed % str(retCode))
                    if self.animat:
                        self.animat.Exit()
                    return
                if self.animat:
                    self.animat.Reverse()
                with sr.WavFile(BytesIO(data)) as source:
                    audio = r.record(source)
            if audio:
                try:
                    res = r.recognize_google(audio, language=self.lng)
                    if self.mode:
                        self.plugin.TriggerEvent(
                            "SpeechToText.%s" % self.suffOk,
                            payload=res
                        )
                    else:
                        self.plugin.TriggerEvent(
                            "SpeechToText.%s.%s" % (self.suffOk, res)
                        )
                except:
                    if self.suffKo:
                        self.plugin.TriggerEvent("SpeechToText.%s" % self.suffKo)
                    eg.PrintError(self.plugin.text.sttFailed)
        except:
            eg.PrintTraceback()
        if self.animat:
            self.animat.Exit()

    def SetAnimation(self, animat):
        self.animat = animat


# ===============================================================================

class IntelliSpeech(eg.PluginBase):
    text = Text
    stopTTS = False
    devices = {}
    inputDevices = {}
    pyAudio = None

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def __stop__(self):
        self.queue.queue.clear()
        self.queue = None
        self.ttsWorker.stop()
        if self.pyAudio:
            self.pyAudio.terminate()
        self.pyAudio = None

    def __start__(
        self,
        defSrc="",
        defTrg="",
        tempFold=eg.folderPath.TemporaryFiles
    ):
        self.defSrc = defSrc
        self.defTrg = defTrg
        self.INV_LANGS = dict([(val, key) for key, val in LANGS.iteritems()])
        self.queue = Queue()
        self.ttsWorker = TTS_Worker(self)
        self.InitDevices()
        self.InitInputDevices()

    def GetDefaultDevice(self):
        api_ix = self.pyAudio.get_default_output_device_info()['hostApi']
        api_name = self.pyAudio.get_host_api_info_by_index(api_ix)['name']
        def_index = self.pyAudio.get_default_output_device_info()['index']
        return u"%s [%s]" % (
            self.pyAudio.get_default_output_device_info()['name'],
            api_name
        )

    def GetDefaultInputDevice(self):
        try:
            api_ix = self.pyAudio.get_default_input_device_info()['hostApi']
        except:
            return None
        api_name = self.pyAudio.get_host_api_info_by_index(api_ix)['name']
        def_index = self.pyAudio.get_default_input_device_info()['index']
        return u"%s [%s]" % (
            self.pyAudio.get_default_input_device_info()['name'],
            api_name
        )

    def InitDevices(self):
        if self.pyAudio:
            try:
                defDev = self.GetDefaultDevice()
                if defDev:
                    return defDev
            except:
                pass

        self.pyAudio = pyaudio.PyAudio()
        if not self.GetDefaultDevice():
            return

        pyAud = self.pyAudio
        max_devs = pyAud.get_device_count()
        for i in range(max_devs):
            devinfo = pyAud.get_device_info_by_index(i)
            if devinfo['maxOutputChannels'] == 0:
                continue
            hostApiIx = devinfo['hostApi']
            hostApiName = pyAud.get_host_api_info_by_index(hostApiIx)['name']
            name = u"%s [%s]" % (devinfo['name'], hostApiName)
            index = devinfo['index']
            testDev = DeviceTest(pyAud, index)
            if not testDev.device_ok():
                continue
            self.devices[name] = (index, hostApiIx)
        defDev = self.GetDefaultDevice()
        return defDev

    def InitInputDevices(self):
        pyAud = self.pyAudio
        max_devs = pyAud.get_device_count()
        for i in range(max_devs):
            devinfo = pyAud.get_device_info_by_index(i)
            if devinfo['maxInputChannels'] == 0:
                continue
            index = devinfo['index']
            testDev = InputDeviceTest(pyAud, index)
            if not testDev.device_ok():
                continue
            hostApiIx = devinfo['hostApi']
            hostApiName = pyAud.get_host_api_info_by_index(hostApiIx)['name']
            name = u"%s [%s]" % (devinfo['name'], hostApiName)
            self.inputDevices[name] = (index, hostApiIx)
        defDev = self.GetDefaultInputDevice()
        return defDev

    def RefreshDevices(self):
        self.pyAudio.terminate()
        self.pyAudio = None
        self.devices = {}
        self.InitDevices()
        self.iputDevices = {}
        self.InitInputDevices()

    def badConn(self):
        try:
            get('http://www.google.com', timeout=0.5)
            return False
        except exceptions.Timeout:
            eg.PrintError(self.text.connTimeout)
            return True
        except exceptions.HTTPError, e:
            eg.PrintError(self.text.httpError)
            eg.PrintError(str(e.args[0].reason))
            return True
        except exceptions.ConnectionError, e:
            eg.PrintError(self.text.connError)
            eg.PrintError(str(e.args[0].reason))
            return True
        except:
            eg.PrintTraceback()
            return True

    def str2int(self, s):
        s = eg.ParseString(s)
        try:
            s = int(s)
        except:
            s = 0
        return s

    def popen(self, indata, vol=None):
        if vol is not None:
            cmd = '"%s" %s %s %s %s %s %s' % (
                join(mod_pth, "lib\\FFmpeg", "ffmpeg.exe"),
                '-i',
                'pipe:0',
                '-vol %s' % int(vol * 2.56),
                '-f',
                'wav',
                'pipe:1'
            )
            data = indata
        else:
            cmd = '"%s" %s "%s" %s %s %s %s %s %s %s' % (
                join(mod_pth, "lib\\FFmpeg", "ffmpeg.exe"),
                '-i',
                indata.encode('mbcs'),  # test
                '-vn',
                '-acodec pcm_s16le',
                '-ar 16000',
                '-ac 1',
                '-f',
                'wav',
                'pipe:1'
            )
            data = None
        si = STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        proc = Popen(
            cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=open(devnull),
            startupinfo=si,
            shell=False
        )
        data = proc.communicate(data)[0]
        # If ffmpeg converts into a stream (PIPE), in the header of "file" 
        # a length is missing. It must be calculated and added:
        lndt = len(data)
        dataTag = data.find("data")
        data = 'RIFF' + BigEnd(lndt - 8) + \
               data[8:(dataTag + 4)] + \
               BigEnd(lndt - dataTag - 8) + \
               data[(dataTag + 8):]
        proc.stdin.close()
        proc.stdout.close()
        return (proc.returncode, data)

    def Configure(
        self,
        defSrc="",
        defTrg="",
        tempFold=eg.folderPath.TemporaryFiles
    ):
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, -1, self.text.label1)
        choices = list(LANGS.iterkeys())
        choices.remove('Detect language')
        choices.sort()
        choices1 = ['Detect language']
        choices1.extend(choices)
        ctrl1 = wx.Choice(panel, -1, choices=choices1)
        ctrl1.SetStringSelection(defSrc)
        label2 = wx.StaticText(panel, -1, self.text.label2)
        ctrl2 = wx.Choice(panel, -1, choices=choices)
        ctrl2.SetStringSelection(defTrg)
        sizer = wx.FlexGridSizer(2, 2, 10, 10)
        sizer.Add(label1, 0, ACV)
        sizer.Add(ctrl1)
        sizer.Add(label2, 0, ACV)
        sizer.Add(ctrl2)
        # tempFold = tempFold if tempFold else eg.folderPath.TemporaryFiles
        # flag = tempFold != eg.folderPath.TemporaryFiles
        # rb0 = panel.RadioButton(flag==0,self.text.folders[0],style=wx.RB_GROUP)
        # rb1 = panel.RadioButton(flag==1, self.text.folders[1])
        # mp3Ctrl = eg.DirBrowseButton(
        #    panel,
        #    -1,
        #    toolTip = self.text.mp3Tool,
        #    dialogTitle = self.text.mp3Fldr,
        #    buttonText = eg.text.General.browse,
        #    startDirectory = eg.folderPath.TemporaryFiles
        # )
        # mp3Ctrl.SetValue(tempFold)
        # mp3Ctrl.Enable(tempFold != eg.folderPath.TemporaryFiles)

        #        def onRadioBox(evt):
        #            flg = rb1.GetValue()
        #            mp3Ctrl.Enable(flg)
        #            mp3Ctrl.SetValue(tempFold)
        #            mp3Ctrl.SetValue(eg.folderPath.TemporaryFiles)
        #            evt.Skip()
        #        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        #        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        #
        #        staticBox = wx.StaticBox(panel, label = self.text.tempFolder)
        #        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        #        staticBoxSizer.Add(rb0)
        #        staticBoxSizer.Add(rb1, 0, wx.TOP, 5)
        #        staticBoxSizer.Add(mp3Ctrl, 0, wx.TOP|wx.EXPAND, 5)
        panel.sizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 10)
        # panel.sizer.Add(
        #    staticBoxSizer,
        #    1,
        #    wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM,
        #    10
        # )

        while panel.Affirmed():
            panel.SetResult(
                ctrl1.GetStringSelection(),
                ctrl2.GetStringSelection(),
                None  # mp3Ctrl.GetValue()
            )

    def StopTTS(self, all):
        if all:
            self.queue.queue.clear()
        self.stopTTS = True

    def Speek(self, lng, txt, vol, dev):
        if self.badConn():
            return
        defDev = self.InitDevices()
        if not defDev:
            return
        dev = dev if dev != self.text.defDev else defDev
        dev = dev if dev in list(self.devices.iterkeys()) else defDev
        src = LANGS[lng]
        if src == "auto":
            src = self.Detect(txt[:128])
            if src is None:
                return
            else:
                lng = self.INV_LANGS[src]
        if not lng in VOICES:
            eg.PrintError(self.text.noVoice % lng)
            return
        self.queue.put((txt, src, vol, self.devices[dev][0]))

    def Detect(self, txt):
        if self.badConn():
            return
        url = 'http://translate.google.com/translate_a/single'
        part = txt.encode("utf-8")
        body = {
            "client": 'gtx',
            "hl": 'en',
            "sl": "auto",
            "ssel": 0,
            "tl": "en",
            "tsel": 0,
            "q": part,
            "ie": 'UTF-8',
        }
        resp = get(url, params=body)
        src = None
        if resp.ok:
            answ = resp.content
            try:
                if len(answ) > 8 and answ[0] == "[":
                    while ",," in answ:
                        answ = answ.replace(",,", ",None,")
                    answ = answ.replace("[,", "[None,").replace(",]", ",None]")
                    answ = eval(answ)
                    src = answ[-1][0][0]
            except:
                pass
        if src is None:
            eg.PrintError(self.text.detFail)
        elif not src in self.INV_LANGS.iterkeys():
            eg.PrintError(self.text.unknLng % src)
            src = None
        return src

    def Translate(self, src, trg, txt):
        # https://translate.google.com/?
        # oe=UTF-8
        # q=Ein+kleiner+Beispieltext.
        # hl=en
        # langpair=de%7Cen
        # tbb=1
        # ie=UTF-8
        # pli=1#view=home
        # op=translate
        # sl=de
        # tl=en
        # text=Ein%20kleiner%20Beispieltext.

        if self.badConn():
            return
        url = "https://translate.google.com"
        src = LANGS[src]
        if src == "auto":
            src = self.Detect(txt[:128])
            if src is None:
                return
        trg = LANGS[trg]
        if src == trg:
            return txt
        body = {
            "hl": "en",
            "langpair": '{}%7C{}'.format(src, trg),
            "q": txt.encode("utf-8"),
            "tbb": 1,
            "ie": "UTF-8",
            "oe": "UTF-8",
            "op": "translate",
            "sl": src,
            "tl": trg,
            # "text": txt.encode("utf-8"),
        }
        # print "---------------------"
        # print body
        # print "---------------------"
        resp = get(url, params=body)
        # import pprint
        # print type(resp)
        # pprint.pprint(resp.__dict__)
        # print resp.ok
        if not resp.ok:
            eg.PrintError(self.text.trnslFail)
            return
        answ = resp.content
        print "----------------------------"
        print answ
        try:
            if answ.find('<span id=result_box class="long_text">') > 1:
                res1 = answ.split('<span id=result_box class="long_text">')
            else:
                res1 = answ.split('<span id=result_box class="short_text">')
            res2 = res1[1].split('</span></div>')
            res3 = res2[0].replace("\'", "")
            res3 = res3.replace("<br>", "\n")
            res3 = res3.replace('&#39;', "'")
            res3 = res3.replace('&quot;', "'")
            res3 = res3.replace('&amp;', "&")
            res3 = removeSpans(res3)
            return res3.decode('utf-8')
        except:
            eg.PrintError(self.text.trnslFail)
            eg.PrintError(repr(answ))
        # ===============================================================================


class Translate(eg.ActionBase):
    class text:
        label1 = "Source language:"
        label2 = "Target language:"
        label3 = "Text to be translated:"
        label4 = "Volume (1 - 100%):"
        label5 = "Output device:"

    def __call__(
        self,
        src="",
        trg="",
        txt="",
        vol=100,
        dev=""
    ):
        dev = dev if dev else self.plugin.text.defDev
        txt = eg.ParseString(txt)
        result = self.plugin.Translate(src, trg, txt)
        if self.value:
            return result
        if result:
            vol = vol if isinstance(vol, int) else self.plugin.str2int(vol)
            self.plugin.Speek(trg, result, vol, dev)

    def Configure(
        self,
        src="",
        trg="",
        txt="",
        vol=100,
        dev=""
    ):
        dev = dev if dev else self.plugin.text.defDev
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, -1, self.text.label1)
        choices2 = list(LANGS.iterkeys())
        choices2.remove('Detect language')
        choices2.sort()
        choices1 = ['Detect language']
        choices1.extend(choices2)
        ctrl1 = wx.Choice(panel, -1, choices=choices1)
        src = self.plugin.defSrc if not src else src
        ctrl1.SetStringSelection(src)
        label2 = wx.StaticText(panel, -1, self.text.label2)
        if not self.value:
            choices2 = [i for i in choices2 if i in VOICES]
        ctrl2 = wx.Choice(panel, -1, choices=choices2)
        trg = self.plugin.defTrg if not trg else trg
        ctrl2.SetStringSelection(trg)
        label3 = wx.StaticText(panel, -1, self.text.label3)
        ctrl3 = wx.TextCtrl(panel, -1, txt, style=wx.TE_MULTILINE)
        if not self.value:
            label4 = wx.StaticText(panel, -1, self.text.label4)
            ctrl4 = eg.SmartSpinIntCtrl(
                panel,
                -1,
                vol,
                min=1,
                max=100
            )

            label5 = wx.StaticText(panel, -1, self.text.label5)
            devs = [self.plugin.text.defDev]
            devs.extend(list(self.plugin.devices.iterkeys()))
            devs.sort()
            ctrl5 = wx.Choice(panel, -1, choices=devs)
            ctrl5.SetStringSelection(dev)

            rows = 5
        else:
            rows = 3
        sizer = wx.FlexGridSizer(rows, 2, 10, 10)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(2)
        sizer.Add(label1, 0, ACV)
        sizer.Add(ctrl1)
        sizer.Add(label2, 0, ACV)
        sizer.Add(ctrl2)
        sizer.Add(label3, 0, wx.TOP, 3)
        sizer.Add(ctrl3, 1, wx.EXPAND)
        if not self.value:
            sizer.Add(label4, 0, ACV)
            sizer.Add(ctrl4)
            sizer.Add(label5, 0, ACV)
            sizer.Add(ctrl5)
        panel.sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                ctrl1.GetStringSelection(),
                ctrl2.GetStringSelection(),
                ctrl3.GetValue(),
                ctrl4.GetValue() if not self.value else 100,
                ctrl5.GetStringSelection() if not self.value else ""
            )


# ===============================================================================

class Speak(eg.ActionBase):
    class text:
        label1 = "Source language:"
        label2 = "Text to be spoken:"
        label3 = "Volume (1 - 100%):"
        label4 = "Output device:"

    def __call__(
        self,
        src="",
        txt="",
        vol=100,
        dev=""
    ):
        dev = dev if dev else self.plugin.text.defDev
        txt = eg.ParseString(txt)
        vol = vol if isinstance(vol, int) else self.plugin.str2int(vol)
        self.plugin.Speek(src, txt, vol, dev)

    def GetLabel(self, src, txt, vol, dev):
        return "%s: %s: %s" % (self.name, src, txt[:24])

    def Configure(
        self,
        src="",
        txt="",
        vol=100,
        dev=""
    ):
        dev = dev if dev else self.plugin.text.defDev
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, -1, self.text.label1)
        choices = list(LANGS.iterkeys())
        choices = [item for item in choices if item in VOICES]
        choices.sort()
        choices1 = ['Detect language']
        choices1.extend(choices)
        ctrl1 = wx.Choice(panel, -1, choices=choices1)
        src = self.plugin.defTrg if not src else src
        ctrl1.SetStringSelection(src)
        label2 = wx.StaticText(panel, -1, self.text.label2)
        ctrl2 = wx.TextCtrl(panel, -1, txt, style=wx.TE_MULTILINE)
        label4 = wx.StaticText(panel, -1, self.text.label4)
        devs = [self.plugin.text.defDev]
        devs.extend(list(self.plugin.devices.iterkeys()))
        devs.sort()
        ctrl4 = wx.Choice(panel, -1, choices=devs)
        ctrl4.SetStringSelection(dev)
        label3 = wx.StaticText(panel, -1, self.text.label3)
        ctrl3 = eg.SmartSpinIntCtrl(
            panel,
            -1,
            vol,
            min=1,
            max=100
        )
        sizer = wx.FlexGridSizer(3, 2, 10, 10)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)
        sizer.Add(label1, 0, ACV)
        sizer.Add(ctrl1)
        sizer.Add(label2, 0, wx.TOP, 3)
        sizer.Add(ctrl2, 1, wx.EXPAND)
        sizer.Add(label3, 0, ACV)
        sizer.Add(ctrl3)
        sizer.Add(label4, 0, ACV)
        sizer.Add(ctrl4)
        panel.sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                ctrl1.GetStringSelection(),
                ctrl2.GetValue(),
                ctrl3.GetValue(),
                ctrl4.GetStringSelection()
            )


# ===============================================================================

class Detect(eg.ActionBase):
    class text:
        label = "Text to be detected:"

    def __call__(self, txt=""):
        txt = eg.ParseString(txt)
        lng = self.plugin.Detect(txt[:128])
        if lng is not None:
            return (lng, self.plugin.INV_LANGS[lng])

    def Configure(
        self,
        txt=""
    ):
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        label = wx.StaticText(panel, -1, self.text.label)
        ctrl = wx.TextCtrl(panel, -1, txt, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.BOTTOM, 8)
        sizer.Add(ctrl, 1, wx.EXPAND)
        panel.sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                ctrl.GetValue(),
            )


# ===============================================================================

class StopTTS(eg.ActionBase):

    def __call__(self):
        self.plugin.StopTTS(self.value)


# ===============================================================================

class SpeechToText(eg.ActionBase):
    class text:
        lang = "Language:"
        dial = "Dialect:"
        intThre = "Silence/Noise signal threshold:"
        silDur = "Silence duration threshold [s]:"
        file = "Input file:"
        mic = "Input device:"
        suffOkLbl = "Event suffix on success:"
        suffKoLbl = "Event suffix at failure:"
        gif = "Show animated indicator on the desktop"
        test = "Test ..."
        toolTip = "If the field is left blank, the event will not be triggered."
        browseFile = 'Choose a file'
        toolTipFile = '''Type filename or click browse to choose file'''
        fMask = (
            "WAV files (*.wav)|*.wav"
            "|AAC files (*.aac)|*.aac"
            "|AC3 files (*.ac3)|*.ac3"
            "|AMR files (*.amr)|*.amr"
            "|GSM files (*.gsm)|*.gsm"
            "|M4A files (*.m4a)|*.m4a"
            "|MP3 files (*.mp3)|*.mp3"
            "|OGG files (*.ogg)|*.ogg"
            "|VOX files (*.vox)|*.vox"
            "|FLAC files (*.flac)|*.flac"
            "|FLV files (*.flv)|*.flv"
            "|MKV files (*.mkv)|*.mkv"
            "|MP4 files (*.mp4)|*.mp4"
            "|AVI files (*.avi)|*.avi"
            "|3GP files (*.3gp)|*.3gp"
            "|All files (*.*)|*.*"
        )
        suffOk = "Success"
        suffKo = "Failure"
        noFile = 'I can not find the file "%s" !'
        mode = "Recognized text to use as an:"
        modes = ("event suffix", "event payload")
        testText = u"some recognized text"

    def __call__(
        self,
        lang=[],
        intThre=2500,
        silDur=0.8,
        suffOk=None,
        suffKo=None,
        gif=True,
        mic=None,
        mode=1
    ):
        mic = mic if mic else self.plugin.text.defMic
        suffOk = self.text.suffOk if suffOk is None else suffOk
        suffKo = self.text.suffKo if suffKo is None else suffKo
        if not lang:
            return
        lng = lang[0]
        code = STT_LANGS[lng]
        lng = code if isinstance(
            code,
            (str, unicode)
        ) else code[lang[1]]
        if silDur is not None:
            intThre = int(intThre) if isinstance(intThre, (int, float)) else \
                int(eg.ParseString(intThre))
            silDur = float(silDur) if isinstance(silDur, (int, float)) else \
                float(eg.ParseString(silDur))
            silDur = silDur if silDur >= 0.5 else 0.5
        else:
            intThre = eg.ParseString(intThre)
            if not isfile(intThre):
                if suffKo:
                    self.plugin.TriggerEvent(
                        "SpeechToText.%s" % suffKo,
                        payload=self.text.noFile % intThre)
                eg.PrintError(self.text.noFile % intThre)
                return
        worker = STT_Worker(
            self.plugin,
            lng,
            intThre,
            silDur,
            suffOk,
            suffKo,
            mic,
            mode
        )
        if gif:
            if silDur is not None:
                pics = MICS
                mirror = False
                color = (255, 0, 0)
            else:
                pics = GEARS
                mirror = True
                color = (255, 239, 206)
            wx.CallAfter(Animation, worker, pics, True, 0.15, mirror, color)

    def GetLabel(
        self,
        lang,
        intThre,
        silDur,
        suffOk,
        suffKo,
        gif,
        mic,
        mode
    ):
        if lang:
            lng = STT_LANGS[lang[0]]
            lng = lang[0] if isinstance(lng, (str, unicode)) \
                else "%s - %s" % (
                unicode(lang[0]),
                unicode(lang[1])
            )
            if self.value == "Mic":
                return "%s: %s" % (self.name, lng)
            else:
                return "%s: %s: %s" % (self.name, lng, intThre)
        else:
            return self.name

    def Configure(
        self,
        lang=[],
        intThre=2500,
        silDur=0.8,
        suffOk=None,
        suffKo=None,
        gif=True,
        mic=None,
        mode=1
    ):
        text = self.text
        mic = mic if mic else self.plugin.text.defMic
        suffOk = text.suffOk if suffOk is None else suffOk
        suffKo = text.suffKo if suffKo is None else suffKo
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, -1, text.lang)
        choices = list(STT_LANGS.iterkeys())
        choices.sort()
        ctrl1 = wx.Choice(panel, -1, choices=choices)
        if lang:
            ctrl1.SetStringSelection(lang[0])
        label2 = wx.StaticText(panel, -1, text.dial)
        ctrl2 = wx.Choice(panel, -1, choices=[])

        langSizer = wx.BoxSizer(wx.HORIZONTAL)
        langSizer.Add(ctrl1)
        langSizer.Add(label2, 0, wx.LEFT | wx.RIGHT | ACV, 10)
        langSizer.Add(ctrl2)
        sizer = wx.GridBagSizer(10, 10)
        sizer.Add(label1, (0, 0), flag=ACV)
        sizer.Add(langSizer, (0, 1))

        if self.value == "Mic":
            label3 = wx.StaticText(panel, -1, text.intThre)
            ctrl3 = eg.SmartSpinIntCtrl(
                panel,
                -1,
                intThre,
                min=1,
                max=9600
            )
            label4 = wx.StaticText(panel, -1, text.silDur)
            ctrl4 = eg.SmartSpinNumCtrl(
                panel,
                -1,
                silDur,
                min=0.5,
                max=60.0
            )
            label8 = wx.StaticText(panel, -1, text.mic)
            mics = [self.plugin.text.defMic]
            mics.extend(list(self.plugin.inputDevices.iterkeys()))
            mics.sort()
            ctrl8 = wx.Choice(panel, -1, choices=mics)
            ctrl8.SetStringSelection(mic)

            sizer.Add(label8, (1, 0), flag=ACV)
            sizer.Add(ctrl8, (1, 1))
            sizer.Add(label3, (2, 0), flag=ACV)
            sizer.Add(ctrl3, (2, 1))
            sizer.Add(label4, (3, 0), flag=ACV)
            sizer.Add(ctrl4, (3, 1))
            ix = 4
        else:
            label3 = wx.StaticText(panel, -1, text.file)
            ctrl3 = eg.FileBrowseButton(
                panel,
                -1,
                toolTip=text.toolTipFile,
                dialogTitle=text.browseFile,
                buttonText=eg.text.General.browse,
                startDirectory=eg.folderPath.Music,
                initialValue=intThre if \
                    isinstance(intThre, (str, unicode)) else "",
                fileMask=text.fMask,
            )
            sizer.Add(label3, (1, 0), flag=ACV)
            sizer.Add(ctrl3, (1, 1), flag=wx.EXPAND)
            ix = 2

            def onFile(evt):
                wx.CallAfter(enableButtons)
                evt.Skip()

            ctrl3.Bind(wx.EVT_TEXT, onFile)

        label9 = wx.StaticText(panel, -1, text.mode)
        rb0 = panel.RadioButton(mode == 0, text.modes[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode == 1, text.modes[1])
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        btnIds = (wx.NewIdRef(), wx.NewIdRef())
        label5 = wx.StaticText(panel, -1, text.suffOkLbl)
        ctrl5 = wx.TextCtrl(panel, -1, suffOk)
        btn5 = wx.Button(panel, btnIds[0], text.test)
        label6 = wx.StaticText(panel, -1, text.suffKoLbl)
        ctrl6 = wx.TextCtrl(panel, -1, suffKo)
        ctrl6.SetToolTip(text.toolTip)
        btn6 = wx.Button(panel, btnIds[1], text.test)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(ctrl5, 1, wx.EXPAND | wx.RIGHT, 5)
        sizer5.Add(btn5)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(ctrl6, 1, wx.EXPAND | wx.RIGHT, 5)
        sizer6.Add(btn6)
        ctrl7 = wx.CheckBox(panel, 0, text.gif)
        ctrl7.SetValue(gif)
        sizer.Add(label9, (ix, 0), flag=ACV)
        sizer.Add(modeSizer, (ix, 1))
        sizer.Add(label5, (ix + 1, 0), flag=ACV)
        sizer.Add(sizer5, (ix + 1, 1), flag=wx.EXPAND)
        sizer.Add(label6, (ix + 2, 0), flag=ACV)
        sizer.Add(sizer6, (ix + 2, 1), flag=wx.EXPAND)
        sizer.Add(ctrl7, (ix + 3, 0), (1, 2))
        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)

        def enableButtons(flag1=None):
            flag1 = flag1 if flag1 is not None else ctrl5.GetValue() != ""
            flag2 = ctrl2.GetSelection() != -1 if ctrl2.IsShown() else True
            flag3 = ctrl1.GetSelection() != -1
            flag4 = self.value == "Mic" or ctrl3.GetValue() != ""
            panel.EnableButtons(flag1 and flag2 and flag3 and flag4)

        def onOkSuffix(evt):
            enable = evt.GetString() != ""
            wx.CallAfter(enableButtons, flag1=enable)
            btn5.Enable(enable)
            evt.Skip()

        ctrl5.Bind(wx.EVT_TEXT, onOkSuffix)

        def onKoSuffix(evt=None):
            btn6.Enable(ctrl6.GetValue() != "")
            if evt:
                evt.Skip()

        ctrl6.Bind(wx.EVT_TEXT, onKoSuffix)
        onKoSuffix()

        def onButton(evt):
            if evt.GetId() == btnIds[0]:
                if rb1.GetValue():
                    self.plugin.TriggerEvent(
                        "SpeechToText.%s" % ctrl5.GetValue(),
                        payload=text.testText
                    )
                else:
                    self.plugin.TriggerEvent(
                        "SpeechToText.%s.%s" % (ctrl5.GetValue(), text.testText)
                    )
            else:
                self.plugin.TriggerEvent("SpeechToText.%s" % ctrl6.GetValue())
            evt.Skip()

        btn5.Bind(wx.EVT_BUTTON, onButton)
        btn6.Bind(wx.EVT_BUTTON, onButton)

        def onDialect(evt):
            wx.CallAfter(enableButtons)
            evt.Skip()

        ctrl2.Bind(wx.EVT_CHOICE, onDialect)

        def langUpdate(evt=None):
            sel = ctrl1.GetStringSelection()
            val = STT_LANGS[sel] if sel in list(STT_LANGS.iterkeys()) else None
            flg = isinstance(val, dict)
            label2.Show(flg)
            ctrl2.Show(flg)
            if flg:
                ctrl2.Clear()
                choices = list(val.iterkeys())
                choices.sort()
                ctrl2.SetItems(choices)
                if not evt and len(lang) > 1:
                    ctrl2.SetStringSelection(lang[1])
            else:
                ctrl2.SetSelection(-1)
            if evt:
                evt.Skip()
            wx.CallAfter(enableButtons)

        ctrl1.Bind(wx.EVT_CHOICE, langUpdate)
        wx.CallAfter(langUpdate)

        while panel.Affirmed():
            panel.SetResult(
                [ctrl1.GetStringSelection(), ctrl2.GetStringSelection()],
                ctrl3.GetValue(),
                ctrl4.GetValue() if self.value == "Mic" else None,
                ctrl5.GetValue(),
                ctrl6.GetValue(),
                ctrl7.GetValue(),
                ctrl8.GetStringSelection() if self.value == "Mic" else None,
                int(rb1.GetValue())
            )


# ===============================================================================

class RefreshAudioDevices(eg.ActionBase):

    def __call__(self):
        self.plugin.RefreshDevices()


# ===============================================================================

ACTIONS = (
    (
        Translate,
        "Translate",
        "Translate text",
        "Translates the specified text into the selected language.",
        True
    ),
    (
        Translate,
        "TranslateAndSpeak",
        "Translate and speak text",
        "Translates and speaks the specified text.",
        False
    ),
    (
        Speak,
        "Speak",
        "Speak text",
        "Speaks the specified text.",
        None
    ),
    (
        StopTTS,
        "StopCurrent",
        "Stop current speech",
        "Stops current speech.",
        False
    ),
    (
        StopTTS,
        "StopAll",
        "Stop all speeches",
        "Stops current speech and clears the queue.",
        True
    ),
    (
        Detect,
        "Detect",
        "Detect language",
        "Detects the language of the specified text.",
        None
    ),
    (
        SpeechToText,
        "MicToText",
        "Speech from microphone to text",
        "Converts speech (from the microphone) to written text.",
        "Mic"
    ),
    (
        SpeechToText,
        "FileToText",
        "Speech from file to text",
        "Converts speech (from a file) to written text.",
        "File"
    ),
    (
        RefreshAudioDevices,
        "RefreshAudioDevices",
        "Refresh audio devices",
        "Refreshes the list of audio devices.",
        None
    ),
)
# ===============================================================================
