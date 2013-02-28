from slovastick_app.audio import audio_lib

class Instrument():
    def __init__(self):
        pass

    def get_instrument(self, settings=None):
        return """
instr %s1
    iInsFullName    = p1
    iStart          = p2
    iDur            = p3
    iFreq           = p4
    iPan            = p5   
    iVol            = p6

    kenv        envlpx  iVol*0.5, .02, iDur, .1, 2, .3, .01
    a1          oscil kenv, iFreq, 3
    aL, aR      pan2 a1, iPan
                outs aL, aR
endin
""" % settings["insPrefix"]

    def get_score_init(self, settings=None):
        return """
f1 0 32 -2 0 .0635 .0963 .1270 .1609 
; function 2 is the attack envelope
f2 0 257 7 0 120 6 16 4 121 5
; function 3 is the waveform
f3 0 2049 10 1 1 .25 .1111 .0625
"""