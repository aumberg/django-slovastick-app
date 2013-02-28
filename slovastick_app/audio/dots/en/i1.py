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

    kamp    linseg  0.4, 0.015, iVol, iDur-0.065, iVol, 0.05, 0.0
    asig    pluck   kamp, iFreq, iFreq, 0, 1
    af1     reson   asig, 110, 80
    af2     reson   asig, 220, 200
    af3     reson   asig, 440, 400
    aout    balance af3*0.5+5*asig, asig
    aL, aR  pan2    aout, iPan
            outs aL, aR
endin
""" % settings["insPrefix"]
