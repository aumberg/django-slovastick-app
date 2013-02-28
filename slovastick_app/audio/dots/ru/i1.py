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

    gi1 ftgen 1, 0, 4096, 8,  0.8, 1024, 0, 2048, -1, 1024, 0.2  ;triangle

    iamp = iVol/5
    a1   oscil  iamp, iFreq, 1
    kenv expseg 1, iFreq, .01
    a1 = a1 * kenv
    a1, a2 pan2 a1, iPan
    outs   a1, a2
endin
""" % settings["insPrefix"]

    def get_score(self, info, settings):
        settings.update(self.updater)

        return audio_lib.get_score_standart(info, settings)

    updater = {
        "startAppend": {
            "1": 0,
            "2": 0.06,
            "3": 0.12,
            "4": 0.01,
            "5": 0.07,
            "6": 0.13,
            "7": 0.15,
            "8": 0.17
        },      
        "iDur": {
            "1": 0.1,
            "2": 0.08,
            "3": 0.05,
            "4": 0.1,
            "5": 0.08,
            "6": 0.05,
            "7": 0.03,
            "8": 0.03,
        },
        "iFreq": {
            "1": audio_lib.note["D5"],
            "2": audio_lib.note["F5"],
            "3": audio_lib.note["A5"],
            "4": audio_lib.note["C6"],
            "5": audio_lib.note["E6"],
            "6": audio_lib.note["G6"],
            "7": audio_lib.note["D4"],
            "8": audio_lib.note["B6"] 
        }
    }


