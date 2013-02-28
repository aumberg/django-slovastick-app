# ~*~ coding: utf-8 ~*~

import re
import django.conf

from slovastick_app import lib
from slovastick_app.audio import audio_lib

class Instrument():
    def __init__(self):
        pass

    def get_instrument(self, settings=None):
        return """
instr %s1
    iFile = p4
    iPan = p5

    ainput soundin iFile
    aL, aR pan2 ainput, iPan
    outs aL*.7, aR*.7
endin
""" % settings["insPrefix"]

    def get_score(self, info, settings):
        if info["self"] in ["ъ", "ь"] :
            return ""

        result = ";--- alphabet\n"

        return self.templ % {
            "insPrefix":    settings["insPrefix"],
            "iStart":       settings["iStart"],
            "iFile":        self.url % info["self"],
            "iPan":         self.get_pan(),
        }

    def get_pan(self):
        self.pan = 0.6 if 0.4 == self.pan else 0.4
        
        return self.pan

    pan = 0.4

    templ = "i %(insPrefix)s1 %(iStart)s 1 %(iFile)s %(iPan)s\n "

    url = "\"" + lib.pathStatic + "/wav/dmitri/%s.wav\""